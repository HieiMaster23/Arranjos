"""Escritor mínimo de MusicXML 3.1 (partwise) pensado para importação no Sibelius.

Convenções:
- Tudo é escrito em ALTURA REAL (concert pitch); o escritor transpõe para a altura escrita
  dos instrumentos transpositores e grava o elemento <transpose>.
- Durações em unidades de semicolcheia (divisions = 4 por semínima):
  1 = semicolcheia, 2 = colcheia, 3 = colcheia pontuada, 4 = semínima,
  6 = semínima pontuada, 8 = mínima, 9 = mínima+colcheia(não usar), 12 = mínima pontuada.
- Tokens de nota (string): "Eb4/4", "r/6", "[Eb4,G4,Bb4]/6", sufixos:
    ~  liga para a próxima      (  início de ligadura de expressão   )  fim de ligadura
    >  acento   ^ marcato   .  staccato   -  tenuto   !  fermata   *  trêmolo (3 traços)
  Para percussão: "p:snare/2", "p:hh/2" (ver DRUM_MAP); cabeças x vêm do mapa.
- Letra: "Eb4/4|Gran-" (sílaba após "|"; hífen no fim = a palavra continua; "‿" junta
  sílabas numa nota, ex.: "do‿o").
"""
from xml.sax.saxutils import escape

DIV = 4
STEPS = "CDEFGAB"
STEP_SEMI = [0, 2, 4, 5, 7, 9, 11]
DUR_TYPES = {1: ("16th", 0), 2: ("eighth", 0), 3: ("eighth", 1), 4: ("quarter", 0),
             6: ("quarter", 1), 8: ("half", 0), 12: ("half", 1), 16: ("whole", 0),
             7: ("quarter", 2)}

# instrumento de percussão: (display-step, display-octave, notehead, stem)
# Posições = mapa padrão do "Drum Set" do Sibelius (pauta de 5 linhas).
DRUM_MAP = {
    "kick": ("F", 4, None, "down"),
    "snare": ("C", 5, None, "up"),
    "xstick": ("C", 5, "x", "up"),
    "tom1": ("E", 5, None, "up"),
    "tom2": ("D", 5, None, "up"),
    "ftom": ("A", 4, None, "up"),
    "hh": ("G", 5, "x", "up"),
    "hhopen": ("G", 5, "circle-x", "up"),
    "hhfoot": ("D", 4, "x", "down"),
    "ride": ("F", 5, "x", "up"),
    "crash": ("A", 5, "x", "up"),
    # percussão auxiliar em pauta de 1 linha (nota na linha)
    "line": ("E", 4, None, "up"),
    "linex": ("E", 4, "x", "up"),
}
# nome do instrumento e nota MIDI General MIDI de cada peça do kit
KIT = {  # notas = mapa "Drum Set (Sticks, Rock)" do NotePerformer 5 (= General MIDI)
    "kick": ("Kick drum", 36), "snare": ("Snare", 38), "xstick": ("Side stick", 37),
    "tom1": ("Tom-tom (high)", 50), "tom2": ("Tom-tom (medium)", 47), "ftom": ("Tom-tom (low)", 43),
    "hh": ("Hi-hat (closed)", 42), "hhopen": ("Hi-hat (open)", 46), "hhfoot": ("Hi-hat (pedal)", 44),
    "ride": ("Ride cymbal", 51), "crash": ("Crash Cymbal", 49),
}


# ---------------------------------------------------------------- alturas
def parse_pitch(s):
    """'Eb4' -> (step, alter, octave)"""
    step = s[0].upper()
    i = 1
    alter = 0
    while i < len(s) and s[i] in "b#":
        alter += -1 if s[i] == "b" else 1
        i += 1
    return step, alter, int(s[i:])


def pitch_str(step, alter, octave):
    return step + ("b" * -alter if alter < 0 else "#" * alter) + str(octave)


def midi(p):
    step, alter, octv = parse_pitch(p) if isinstance(p, str) else p
    return 12 * (octv + 1) + STEP_SEMI[STEPS.index(step)] + alter


def transpose(p, diatonic, chromatic):
    step, alter, octv = parse_pitch(p)
    idx = STEPS.index(step) + diatonic
    noct = octv + idx // 7
    nstep = STEPS[idx % 7]
    target = midi(p) + chromatic
    nalter = target - (12 * (noct + 1) + STEP_SEMI[STEPS.index(nstep)])
    return pitch_str(nstep, nalter, noct)


# ---------------------------------------------------------------- tokens
class Ev:
    __slots__ = ("pitches", "dur", "tie", "tie_stop", "tie_set", "tie_stop_set", "slur_start", "slur_stop", "arts", "drum", "grace",
                 "lyric", "syllabic")

    def __init__(self):
        self.pitches = []  # vazio = pausa
        self.dur = 0
        self.tie = False
        self.tie_stop = False
        self.tie_set = set()
        self.tie_stop_set = set()
        self.slur_start = self.slur_stop = False
        self.arts = set()
        self.drum = None
        self.lyric = None  # sílaba ("Gran-" = continua com hífen; "_" = sílaba vazia)
        self.syllabic = None


def parse_token(tok):
    e = Ev()
    if "|" in tok:
        tok, e.lyric = tok.split("|", 1)
    body, dur = tok.rsplit("/", 1)
    flags = ""
    while dur and not dur[-1].isdigit():
        flags = dur[-1] + flags
        dur = dur[:-1]
    e.dur = int(dur)
    for f in flags:
        if f == "~": e.tie = True
        elif f == "(": e.slur_start = True
        elif f == ")": e.slur_stop = True
        elif f == ">": e.arts.add("accent")
        elif f == "^": e.arts.add("strong-accent")
        elif f == ".": e.arts.add("staccato")
        elif f == "-": e.arts.add("tenuto")
        elif f == "!": e.arts.add("fermata")
        elif f == "*": e.arts.add("tremolo")
    if body == "r":
        return e
    if body.startswith("p:"):
        e.drum = body[2:].split("+")
        return e
    if body.startswith("["):
        e.pitches = [x.strip() for x in body[1:-1].split(",") if x.strip()]
    else:
        e.pitches = [body]
    return e


def parse_voice(s):
    if isinstance(s, list):
        return [x if isinstance(x, Ev) else parse_token(x) for x in s]
    return [parse_token(t) for t in s.split()]


# ---------------------------------------------------------------- estruturas
class Instrument:
    def __init__(self, name, abbr, clef="G", staves=1, diatonic=0, chromatic=0, octave_change=0,
                 midi_program=1, percussion=False, clefs=None, key_offset=0, lines=5, sound=None,
                 sound_id=None, gm_key=None):
        self.name, self.abbr = name, abbr
        self.clefs = clefs or [clef] * staves
        self.staves = staves
        # transposição: escrito = real + intervalo (diatonic/chromatic positivos sobem)
        self.wd, self.wc, self.oc = diatonic, chromatic, octave_change
        self.midi_program = midi_program
        self.percussion = percussion
        self.key_offset = key_offset  # quintas a somar à armadura real
        self.lines = lines
        self.sound = sound
        self.sound_id = sound_id  # MusicXML <instrument-sound> (o Sibelius usa para escolher o instrumento)
        self.gm_key = gm_key  # percussão de 1 som: nota GM
        # measures[n] = {"staff": {staff_no: [voice_events,...]}, "dirs": [...], "harm": [...]}
        self.measures = {}

    def m(self, n):
        return self.measures.setdefault(n, {"staff": {}, "dirs": [], "harm": [], "barline": None})

    def put(self, n, *voices, staff=1):
        """voices: strings/listas de tokens. Cada voz deve somar o compasso inteiro."""
        self.m(n)["staff"][staff] = [parse_voice(v) for v in voices]

    def dir(self, n, kind, value=None, offset=0, staff=1, placement="above"):
        self.m(n)["dirs"].append((offset, kind, value, staff, placement))

    def harm(self, n, symbol, offset=0):
        self.m(n)["harm"].append((offset, symbol))


class Score:
    def __init__(self, title, composer, arranger, measures, beats_div=12, time=(6, 8)):
        self.title, self.composer, self.arranger = title, composer, arranger
        self.n = measures
        self.bar_len = beats_div
        self.time = time
        self.parts = []
        self.groups = []  # (start_idx, end_idx, symbol, name)
        self.keys = {1: 0}  # compasso -> quintas (altura real)
        self.marks = {}  # compasso -> (letra, texto)
        self.tempos = {}  # compasso -> (bpm_dotted_quarter, texto)
        self.barlines = {}  # compasso -> 'light-light' | 'light-heavy'
        self.time_changes = {}

    def add(self, inst):
        self.parts.append(inst)
        return inst

    def group(self, start, end, symbol="bracket", name=""):
        self.groups.append((start, end, symbol, name))

    # ------------------------------------------------------------ escrita
    def write(self, path):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
               '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" '
               '"http://www.musicxml.org/dtds/partwise.dtd">',
               '<score-partwise version="3.1">',
               f'  <work><work-title>{escape(self.title)}</work-title></work>',
               '  <identification>',
               f'    <creator type="composer">{escape(self.composer)}</creator>',
               f'    <creator type="arranger">{escape(self.arranger)}</creator>',
               '    <encoding><software>ferramentas/mxl.py</software>'
               '<supports element="accidental" type="yes"/><supports element="beam" type="yes"/>'
               '<supports element="stem" type="yes"/></encoding>',
               '  </identification>',
               '  <credit page="1"><credit-type>title</credit-type>'
               f'<credit-words default-x="1400" default-y="4000" justify="center" valign="top" font-size="24">{escape(self.title)}</credit-words></credit>',
               '  <credit page="1"><credit-type>composer</credit-type>'
               f'<credit-words default-x="2700" default-y="3850" justify="right" valign="top" font-size="11">{escape(self.composer)}</credit-words></credit>',
               '  <credit page="1"><credit-type>arranger</credit-type>'
               f'<credit-words default-x="2700" default-y="3800" justify="right" valign="top" font-size="11">{escape(self.arranger)}</credit-words></credit>',
               '  <part-list>']
        gstarts = {}
        gends = {}
        for gi, (s, e, sym, nm) in enumerate(self.groups, 1):
            gstarts.setdefault(s, []).append((gi, sym, nm))
            gends.setdefault(e, []).append(gi)
        for i, p in enumerate(self.parts):
            for gi, sym, nm in gstarts.get(i, []):
                out.append(f'    <part-group type="start" number="{gi}">'
                           + (f'<group-name>{escape(nm)}</group-name>' if nm else '')
                           + f'<group-symbol>{sym}</group-symbol><group-barline>yes</group-barline></part-group>')
            pid = f"P{i+1}"
            out.append(f'    <score-part id="{pid}"><part-name>{escape(p.name)}</part-name>'
                       f'<part-abbreviation>{escape(p.abbr)}</part-abbreviation>')
            if p.percussion and p.sound == "drums":
                for k, (nm, key) in KIT.items():
                    out.append(f'      <score-instrument id="{pid}-{k}"><instrument-name>{nm}</instrument-name>'
                               f'<instrument-sound>drum.group.set</instrument-sound></score-instrument>')
                # drum_midi: "spec" = nota GM + 1 (como diz a especificação MusicXML),
                #            "gm" = nota GM exata, "none" = sem nota MIDI (só posição na pauta)
                mode = getattr(p, "drum_midi", "gm")
                for k, (nm, key) in KIT.items():
                    if mode == "none":
                        continue
                    val = key + 1 if mode == "spec" else key  # Sibelius/NotePerformer: nota exata
                    out.append(f'      <midi-instrument id="{pid}-{k}"><midi-channel>10</midi-channel>'
                               f'<midi-program>1</midi-program><midi-unpitched>{val}</midi-unpitched></midi-instrument>')
            else:
                snd = f'<instrument-sound>{p.sound_id}</instrument-sound>' if p.sound_id else ''
                out.append(f'      <score-instrument id="{pid}-I1"><instrument-name>{escape(p.name)}</instrument-name>'
                           f'{snd}</score-instrument>')
                if p.percussion:
                    out.append(f'      <midi-instrument id="{pid}-I1"><midi-channel>10</midi-channel>'
                               f'<midi-program>1</midi-program><midi-unpitched>{p.gm_key}</midi-unpitched></midi-instrument>')
                else:
                    ch = (i % 15) + 1
                    ch = ch + 1 if ch >= 10 else ch
                    out.append(f'      <midi-instrument id="{pid}-I1"><midi-channel>{ch}</midi-channel>'
                               f'<midi-program>{p.midi_program}</midi-program></midi-instrument>')
            out.append('    </score-part>')
            for gi in gends.get(i, []):
                out.append(f'    <part-group type="stop" number="{gi}"/>')
        out.append('  </part-list>')
        for i, p in enumerate(self.parts):
            out.extend(self._write_part(i, p))
        out.append('</score-partwise>')
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")

    def _key_at(self, n):
        k = 0
        for mm in sorted(self.keys):
            if mm <= n:
                k = self.keys[mm]
        return k

    def _write_part(self, idx, p):
        pid = f"P{idx+1}"
        o = [f'  <part id="{pid}">']
        self._syllabify(p)
        self._link_ties(p)
        pending = {}
        for n in range(1, self.n + 1):
            md = p.m(n)
            o.append(f'    <measure number="{n}">')
            attrs = []
            if n == 1:
                attrs.append(f'<divisions>{DIV}</divisions>')
            if n == 1 or n in self.keys:
                if not p.percussion:
                    fifths = self._key_at(n) + p.key_offset
                    if fifths > 7: fifths -= 12
                    if fifths < -7: fifths += 12
                    attrs.append(f'<key><fifths>{fifths}</fifths><mode>major</mode></key>')
            if n == 1 or n in self.time_changes:
                b, bt = self.time_changes.get(n, self.time)
                attrs.append(f'<time><beats>{b}</beats><beat-type>{bt}</beat-type></time>')
            if n == 1:
                if p.staves > 1:
                    attrs.append(f'<staves>{p.staves}</staves>')
                for si, c in enumerate(p.clefs, 1):
                    num = f' number="{si}"' if p.staves > 1 else ''
                    if c == "G": attrs.append(f'<clef{num}><sign>G</sign><line>2</line></clef>')
                    elif c == "F": attrs.append(f'<clef{num}><sign>F</sign><line>4</line></clef>')
                    elif c == "C": attrs.append(f'<clef{num}><sign>C</sign><line>3</line></clef>')
                    elif c == "perc": attrs.append(f'<clef{num}><sign>percussion</sign></clef>')
                if p.percussion and p.lines != 5:
                    attrs.append(f'<staff-details><staff-lines>{p.lines}</staff-lines></staff-details>')
                if p.wd or p.wc or p.oc:
                    # MusicXML: intervalo de escrito -> real
                    attrs.append(f'<transpose><diatonic>{-p.wd}</diatonic><chromatic>{-p.wc}</chromatic>'
                                 + (f'<octave-change>{-p.oc}</octave-change>' if p.oc else '') + '</transpose>')
            if attrs:
                o.append('      <attributes>' + ''.join(attrs) + '</attributes>')
            # marcas globais só nas partes "de topo" (Sibelius as trata como system text)
            if idx == 0:
                if n in self.marks:
                    letter, text = self.marks[n]
                    o.append('      <direction placement="above"><direction-type>'
                             f'<rehearsal font-weight="bold" enclosure="square">{escape(letter)}</rehearsal>'
                             '</direction-type></direction>')
                    if text:
                        o.append('      <direction placement="above"><direction-type>'
                                 f'<words font-weight="bold">{escape(text)}</words></direction-type></direction>')
                if n in self.tempos:
                    bpm, text = self.tempos[n]
                    compound = self.time[1] == 8  # 6/8: andamento em semínima pontuada
                    o.append('      <direction placement="above"><direction-type>'
                             + (f'<words font-weight="bold">{escape(text)}</words></direction-type><direction-type>' if text else '')
                             + '<metronome><beat-unit>quarter</beat-unit>' + ('<beat-unit-dot/>' if compound else '')
                             + f'<per-minute>{bpm}</per-minute></metronome></direction-type>'
                             f'<sound tempo="{bpm*1.5 if compound else bpm:g}"/></direction>')
            # cifras (harmony) — ordenadas por offset, intercaladas por forward
            events_written = False
            for staff in range(1, p.staves + 1):
                voices = md["staff"].get(staff)
                if voices is None:
                    voices = [parse_voice(f"r/{self.bar_len}")]
                    voices[0][0].arts.add("measure-rest")
                for vi, evs in enumerate(voices, 1):
                    prev_ev = pending.pop((staff, vi), None)
                    chain = ([prev_ev] if prev_ev is not None else []) + list(evs)
                    for k in range(1, len(chain)):
                        a, b_ = chain[k-1], chain[k]
                        if a.tie and a.pitches and b_.pitches:
                            common = set(a.pitches) & set(b_.pitches)
                            a.tie_set |= common
                            b_.tie_stop_set |= common
                    if evs and evs[-1].tie:
                        pending[(staff, vi)] = evs[-1]
                    if events_written:
                        o.append(f'      <backup><duration>{self.bar_len}</duration></backup>')
                    events_written = True
                    voice_no = vi + (staff - 1) * 4
                    o.extend(self._write_voice(p, n, md, evs, staff, voice_no,
                                               first=(staff == 1 and vi == 1)))
            bl = self.barlines.get(n)
            if n == self.n:
                bl = bl or "light-heavy"
            if bl:
                o.append(f'      <barline location="right"><bar-style>{bl}</bar-style></barline>')
            o.append('    </measure>')
        o.append('  </part>')
        return o

    def _link_ties(self, p):
        """Resolve as ligaduras (inclusive entre compassos) antes de escrever o XML."""
        prev = {}
        for n in range(1, self.n + 1):
            for staff, voices in p.m(n)["staff"].items():
                for vi, evs in enumerate(voices, 1):
                    for e in evs:
                        a = prev.get((staff, vi))
                        if a is not None and a.tie and a.pitches and e.pitches:
                            common = set(a.pitches) & set(e.pitches)
                            a.tie_set |= common
                            e.tie_stop_set |= common
                        prev[(staff, vi)] = e

    def _syllabify(self, p):
        """Define begin/middle/end/single das sílabas (voz 1 de cada pauta, em ordem)."""
        for staff in range(1, p.staves + 1):
            cont = False
            for n in range(1, self.n + 1):
                voices = p.m(n)["staff"].get(staff)
                if not voices:
                    continue
                for e in voices[0]:
                    if not e.lyric:
                        continue
                    hy = e.lyric.endswith("-")
                    e.syllabic = ("middle" if hy else "end") if cont else ("begin" if hy else "single")
                    cont = hy

    def _directions_xml(self, p, md, staff, offset_from, offset_to, cur):
        """Gera direções (dinâmica, texto, wedges) e cifras com offset no intervalo."""
        o = []
        items = [d for d in md["dirs"] if d[3] == staff and offset_from <= d[0] < offset_to]
        harms = [h for h in md["harm"] if offset_from <= h[0] < offset_to] if staff == 1 else []
        for off, kind, value, st, plc in sorted(items, key=lambda x: x[0]):
            offs = f'<offset>{off-cur}</offset>' if off != cur else ''
            stf = f'<staff>{st}</staff>' if p.staves > 1 else ''
            if kind == "dyn":
                o.append(f'      <direction placement="below"><direction-type><dynamics><{value}/></dynamics>'
                         f'</direction-type>{offs}{stf}</direction>')
            elif kind == "text":
                o.append(f'      <direction placement="{plc}"><direction-type><words font-style="italic">{escape(value)}</words>'
                         f'</direction-type>{offs}{stf}</direction>')
            elif kind == "textb":
                o.append(f'      <direction placement="{plc}"><direction-type><words font-weight="bold">{escape(value)}</words>'
                         f'</direction-type>{offs}{stf}</direction>')
            elif kind in ("cresc", "dim", "wedge-stop"):
                t = {"cresc": "crescendo", "dim": "diminuendo", "wedge-stop": "stop"}[kind]
                o.append(f'      <direction placement="below"><direction-type><wedge type="{t}" number="{value or 1}"/>'
                         f'</direction-type>{offs}{stf}</direction>')
        for off, sym in sorted(harms):
            o.append(self._harmony_xml(sym, off - cur))
        return o

    def _harmony_xml(self, sym, offset):
        root, kind, text, bass, degrees = parse_chord_symbol(sym)
        rs, ra, _ = parse_pitch(root + "4")
        x = f'      <harmony print-frame="no"><root><root-step>{rs}</root-step>'
        if ra: x += f'<root-alter>{ra}</root-alter>'
        x += f'</root><kind text="{escape(text)}">{kind}</kind>'
        if bass:
            bs, ba, _ = parse_pitch(bass + "4")
            x += f'<bass><bass-step>{bs}</bass-step>' + (f'<bass-alter>{ba}</bass-alter>' if ba else '') + '</bass>'
        for val, alt, typ in degrees:
            x += f'<degree><degree-value>{val}</degree-value><degree-alter>{alt}</degree-alter><degree-type>{typ}</degree-type></degree>'
        if offset:
            x += f'<offset>{offset}</offset>'
        return x + '</harmony>'

    def _write_voice(self, p, n, md, evs, staff, voice_no, first):
        o = []
        total = sum(e.dur for e in evs)
        if total != self.bar_len and not (self.time_changes.get(n)):
            raise ValueError(f"{p.name} c.{n} pauta {staff} voz {voice_no}: soma {total} != {self.bar_len}")
        beams = compute_beams(evs, beat=6 if self.time[1] == 8 else 4)
        cur = 0
        slur_open = False
        for i, e in enumerate(evs):
            if first or voice_no in (1, 5):
                if voice_no == 1 or (voice_no == 5 and staff == 2):
                    o.extend(self._directions_xml(p, md, staff, cur, cur + e.dur, cur))
            o.extend(self._note_xml(p, e, staff, voice_no, beams[i], n))
            cur += e.dur
        return o

    def _note_xml(self, p, e, staff, voice, beam, mnum):
        o = []
        typ, dots = DUR_TYPES[e.dur]
        stf = f'<staff>{staff}</staff>' if p.staves > 1 else ''
        if not e.pitches and not e.drum:
            if "measure-rest" in e.arts:
                o.append(f'      <note><rest measure="yes"/><duration>{e.dur}</duration><voice>{voice}</voice>{stf}</note>')
            else:
                o.append(f'      <note><rest/><duration>{e.dur}</duration><voice>{voice}</voice>'
                         f'<type>{typ}</type>' + '<dot/>' * dots + f'{stf}</note>')
            return o
        heads = []
        if e.drum:
            for d in e.drum:
                st, oc, nh, stem = DRUM_MAP[d]
                heads.append(("drum", d, st, oc, nh, stem))
        else:
            for ptxt in e.pitches:
                wp = transpose(ptxt, p.wd, p.wc) if (p.wd or p.wc) else ptxt
                if p.oc:
                    s_, a_, oc_ = parse_pitch(wp)
                    wp = pitch_str(s_, a_, oc_ + p.oc)
                heads.append(("pitch", wp))
        for hi, h in enumerate(heads):
            x = '      <note>'
            if hi > 0:
                x += '<chord/>'
            if h[0] == "drum":
                _, d, st, oc, nh, stem = h
                x += f'<unpitched><display-step>{st}</display-step><display-octave>{oc}</display-octave></unpitched>'
            else:
                s_, a_, oc_ = parse_pitch(h[1])
                x += f'<pitch><step>{s_}</step>' + (f'<alter>{a_}</alter>' if a_ else '') + f'<octave>{oc_}</octave></pitch>'
            x += f'<duration>{e.dur}</duration>'
            src_p = e.pitches[hi] if h[0] == "pitch" else None
            t_stop = src_p is not None and src_p in e.tie_stop_set
            t_start = src_p is not None and src_p in e.tie_set
            if t_stop:
                x += '<tie type="stop"/>'
            if t_start:
                x += '<tie type="start"/>'
            if h[0] == "drum":
                iid = d if p.sound == "drums" else "I1"
                x += f'<instrument id="P{self.parts.index(p)+1}-{iid}"/>'
            x += f'<voice>{voice}</voice><type>{typ}</type>' + '<dot/>' * dots
            if h[0] == "pitch" and p.sound != "slash":
                acc = accidental_for(h[1], self._key_at(mnum) + p.key_offset)
                if acc:
                    x += f'<accidental>{acc}</accidental>'
            if h[0] == "drum":
                x += f'<stem>{h[5]}</stem>'
                if h[4]:
                    x += f'<notehead>{h[4]}</notehead>'
            elif p.sound == "slash":
                x += '<stem>none</stem><notehead>slash</notehead>'
            x += stf
            if hi == 0 and beam:
                for lvl, val in beam:
                    x += f'<beam number="{lvl}">{val}</beam>'
            nots = []
            if t_stop:
                nots.append('<tied type="stop"/>')
            if t_start:
                nots.append('<tied type="start"/>')
            if hi == 0:
                if e.slur_start: nots.append('<slur type="start" number="1"/>')
                if e.slur_stop: nots.append('<slur type="stop" number="1"/>')
                arts = [a for a in ("accent", "strong-accent", "staccato", "tenuto") if a in e.arts]
                if arts:
                    nots.append('<articulations>' + ''.join(f'<{a}/>' for a in arts) + '</articulations>')
                if "fermata" in e.arts:
                    nots.append('<fermata type="upright"/>')
                if "tremolo" in e.arts:
                    nots.append('<ornaments><tremolo type="single">3</tremolo></ornaments>')
            if nots:
                x += '<notations>' + ''.join(nots) + '</notations>'
            if hi == 0 and e.lyric and e.lyric != "_":
                txt = e.lyric[:-1] if e.lyric.endswith("-") else e.lyric
                # "do‿o" = elisão (duas sílabas na mesma nota)
                body = '<elision>‿</elision>'.join(f'<text>{escape(t)}</text>' for t in txt.split("‿"))
                x += f'<lyric number="1"><syllabic>{e.syllabic or "single"}</syllabic>{body}</lyric>'
            x += '</note>'
            o.append(x)
        return o


# ---------------------------------------------------------------- acidentes
def key_alters(fifths):
    order_sharp = "FCGDAEB"
    alt = {s: 0 for s in STEPS}
    if fifths > 0:
        for s in order_sharp[:fifths]: alt[s] = 1
    elif fifths < 0:
        for s in order_sharp[::-1][:-fifths]: alt[s] = -1
    return alt


_acc_state = {}


def accidental_for(pitch, fifths):
    """Acidente simples: mostra quando difere da armadura (sem memória de compasso;
    o Sibelius recalcula a grafia dos acidentes na importação)."""
    s, a, _ = parse_pitch(pitch)
    ka = key_alters(fifths)[s]
    if a == ka:
        return None
    return {-2: "flat-flat", -1: "flat", 0: "natural", 1: "sharp", 2: "double-sharp"}[a]


# ---------------------------------------------------------------- vigas
def compute_beams(evs, beat=6):
    res = [None] * len(evs)
    pos = 0
    groups = []
    cur = []
    for i, e in enumerate(evs):
        b = pos // beat
        beamable = e.dur < 4 and (e.pitches or e.drum)
        if cur and (not beamable or (cur[-1][1] != b) or (pos % beat == 0)):
            groups.append(cur)
            cur = []
        if beamable:
            cur.append((i, b))
        pos += e.dur
    if cur:
        groups.append(cur)
    for g in groups:
        if len(g) < 2:
            continue
        idxs = [i for i, _ in g]
        for k, i in enumerate(idxs):
            lv1 = "begin" if k == 0 else ("end" if k == len(idxs) - 1 else "continue")
            beam = [(1, lv1)]
            if evs[i].dur in (1, 3) and evs[i].dur == 1:
                prev16 = k > 0 and evs[idxs[k-1]].dur == 1
                next16 = k < len(idxs) - 1 and evs[idxs[k+1]].dur == 1
                if prev16 and next16: beam.append((2, "continue"))
                elif prev16: beam.append((2, "end"))
                elif next16: beam.append((2, "begin"))
                else: beam.append((2, "forward hook" if k < len(idxs) - 1 else "backward hook"))
            res[i] = beam
    return res


# ---------------------------------------------------------------- cifras
KIND = {
    "": ("major", ""), "m": ("minor", "m"), "7": ("dominant", "7"), "m7": ("minor-seventh", "m7"),
    "maj7": ("major-seventh", "maj7"), "m6": ("minor-sixth", "m6"), "6": ("major-sixth", "6"),
    "sus4": ("suspended-fourth", "sus4"), "7sus4": ("dominant", "7sus4"), "sus2": ("suspended-second", "sus2"),
    "add9": ("major", "add9"), "maj9": ("major-ninth", "maj9"), "6/9": ("major-sixth", "6/9"),
    "m9": ("minor-ninth", "m9"),
    "9": ("dominant-ninth", "9"), "13": ("dominant-13th", "13"), "m11": ("minor-11th", "m11"),
    "7#9": ("dominant", "7"), "7b9": ("dominant", "7"), "maj7#11": ("major-seventh", "maj7"),
    "dim7": ("diminished-seventh", "°7"), "m7b5": ("half-diminished", "ø7"),
}


def parse_chord_symbol(sym):
    s = sym.replace("(", "").replace(")", "")
    bass = None
    if "/" in s and not s.endswith("6/9"):
        s, bass = s.split("/")
    root = s[0]
    i = 1
    while i < len(s) and s[i] in "b#":
        root += s[i]
        i += 1
    q = s[i:]
    kind, text = KIND[q]
    degrees = []
    if q == "add9": degrees = [(9, 0, "add")]; text = ""
    if q == "7sus4": degrees = [(4, 0, "add"), (3, 0, "subtract")]
    if q == "6/9": degrees = [(9, 0, "add")]
    if q == "7#9": degrees = [(9, 1, "add")]
    if q == "7b9": degrees = [(9, -1, "add")]
    if q == "maj7#11": degrees = [(11, 1, "add")]
    return root, kind, text, bass, degrees


INTERVALS = {
    "": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10], "maj7": [0, 4, 7, 11],
    "m6": [0, 3, 7, 9], "6": [0, 4, 7, 9], "sus4": [0, 5, 7], "7sus4": [0, 5, 7, 10], "sus2": [0, 2, 7],
    "add9": [0, 4, 7, 2], "maj9": [0, 4, 7, 11, 2], "6/9": [0, 4, 7, 9, 2], "m9": [0, 3, 7, 10, 2],
    "9": [0, 4, 7, 10, 2], "13": [0, 4, 7, 10, 2, 9], "m11": [0, 3, 7, 10, 2, 5],
    "7#9": [0, 4, 7, 10, 3], "7b9": [0, 4, 7, 10, 1], "maj7#11": [0, 4, 7, 11, 6],
    "dim7": [0, 3, 6, 9], "m7b5": [0, 3, 6, 10],
}


def chord_pcs(sym):
    s = sym.replace("(", "").replace(")", "")
    bass = None
    if "/" in s and not s.endswith("6/9"):
        s, bass = s.split("/")
    root = s[0]
    i = 1
    while i < len(s) and s[i] in "b#":
        root += s[i]
        i += 1
    r = midi(root + "4") % 12
    pcs = [(r + x) % 12 for x in INTERVALS[s[i:]]]
    b = midi(bass + "4") % 12 if bass else r
    return pcs, r, b, root, bass
