"""Grandes Coisas - Etapa 2: seção rítmica + harmonia gospel.

Gera `grandes-coisas-ritmica.musicxml`: Coro (melodia guia, da Etapa 1), Teclado (piano),
Órgão (Hammond), Guitarra, Baixo e Bateria, com a harmonia gospel de `HARM`.

Forma, compassos e melodia vêm de `gerar_leadsheet.py` (fonte única). Tudo em altura real;
o escritor (`ferramentas/mxl.py`) transpõe guitarra e baixo (escritos 8va).
Posições/durações em semicolcheias (16 por compasso de 4/4).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ferramentas"))
import gerar_leadsheet as LS  # noqa: E402
from mxl import Score, Instrument, chord_pcs  # noqa: E402

BAR = LS.BAR
START, FORM, NBARS = LS.START, LS.FORM, LS.NBARS

# ------------------------------------------------------------------ harmonia gospel
HARM = LS.CHORDS  # fonte única: gerar_leadsheet.py
CH = {}  # compasso -> [(pos, cifra)]
for _m, title, length, _k in FORM:
    assert len(HARM[title]) == length, title
    for i, c in enumerate(HARM[title]):
        CH[START[title] + i] = [(0, c[0]), (8, c[1])] if isinstance(c, tuple) else [(0, c)]


def chord_at(bar, pos):
    sym = CH[bar][0][1]
    for p, s in CH[bar]:
        if p <= pos:
            sym = s
    return sym


def next_chord(bar):
    return CH[bar + 1][0][1] if bar < NBARS else chord_at(bar, 15)


# ------------------------------------------------------------------ estilo por seção
STYLE = {"Intro": "cheio", "Parte 1": "leve", "Pré-refrão": "pre", "Refrão": "cheio",
         "Interlúdio": "cheio", "Parte 2": "medio", "Pré-refrão 2": "pre", "Refrão 2": "cheio",
         "Vamp": "vamp", "Vamp (Fá)": "vamp2", "Preparação": "prep", "Refrão final": "cheio2",
         "Final": "final"}


def section_of(bar):
    for _m, title, length, _k in FORM:
        if START[title] <= bar < START[title] + length:
            return title, bar - START[title], length
    raise ValueError(bar)


# ------------------------------------------------------------------ alturas
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def near(pc, lo, hi):
    for m in range(lo, hi + 1):
        if m % 12 == pc:
            return m
    raise ValueError((pc, lo, hi))


def voicing(sym, prev, lo, hi, top_max, n=4, drop_root=True):
    """Voicing fechado com condução de vozes (escolhe o mais próximo do anterior)."""
    pcs, r, b, _root, _bass = chord_pcs(sym)
    tones = list(dict.fromkeys(pcs))
    if drop_root and len(tones) >= 4:
        tones = [t for t in tones if t != r]
    # prioridade: 3ª, 7ª, 13ª/6ª, 9ª, 11ª, #11, b9, 5ª (a fundamental fica com o baixo)
    prio = [4, 3, 10, 11, 9, 2, 5, 6, 1, 8, 7, 0]
    tones = sorted(tones, key=lambda t: prio.index((t - r) % 12))[:n]
    best = None
    for start in range(lo, hi + 1):
        if start % 12 not in tones:
            continue
        v = [start]
        for t in sorted(tones, key=lambda t: (t - start) % 12)[1:]:
            v.append(v[0] + (t - start) % 12)
        if v[-1] > top_max:
            continue
        cost = sum(abs(a - c) for a, c in zip(v, prev)) if prev else abs(v[0] - (lo + hi) // 2)
        if best is None or cost < best[0]:
            best = (cost, v)
    return best[1]


def bass_note(sym, lo=28, hi=39):
    pcs, r, b, _root, _bass = chord_pcs(sym)
    return near(b, lo, hi)


def tok_pitches(ms):
    return "[" + ",".join(name(m) for m in ms) + "]" if len(ms) > 1 else name(ms[0])


# ------------------------------------------------------------------ montagem em compassos
def to_measures(events, nbars=NBARS):
    """events: (abs_start, dur, corpo, flags). Uma voz; quebra nas barras com ligadura."""
    bars = {b: [] for b in range(1, nbars + 1)}
    for start, dur, body, flags in sorted(events):
        t, end = start, start + dur
        pieces = []
        while t < end:
            b = t // BAR + 1
            seg = min(end, b * BAR) - t
            for pp, d in LS.split_dur(t % BAR, seg):
                pieces.append((b, pp, d))
            t += seg
        for i, (b, pp, d) in enumerate(pieces):
            fl = ("~" if i < len(pieces) - 1 and not body.startswith("p:") else "")
            if i == 0:
                fl += flags.replace("!", "")
            if i == len(pieces) - 1 and "!" in flags:
                fl += "!"
            bars[b].append((pp, d, f"{body}/{d}{fl}"))
    out = {}
    for b, evs in bars.items():
        evs.sort()
        toks, cur = [], 0
        for pp, d, tok in evs:
            if pp < cur:
                raise ValueError(f"sobreposição c. {b} pos {pp}: {tok}")
            toks += [f"r/{rd}" for _, rd in LS.split_dur(cur, pp - cur)]
            toks.append(tok)
            cur = pp + d
        toks += [f"r/{rd}" for _, rd in LS.split_dur(cur, BAR - cur)]
        out[b] = " ".join(toks)
    return out


def A(bar, pos):
    return (bar - 1) * BAR + pos


# ------------------------------------------------------------------ padrões rítmicos
# (pos, dur, push?) ; push = antecipa o acorde do compasso seguinte (colcheia antes)
PAT_KEYS = {
    "leve": [(0, 8, 0), (8, 6, 0), (14, 2, 1)],
    "medio": [(0, 4, 0), (6, 2, 0), (8, 4, 0), (14, 2, 1)],
    "pre": [(p, 2, p == 14) for p in range(0, 16, 2)],
    "cheio": [(0, 4, 0), (6, 2, 0), (8, 4, 0), (12, 2, 0), (14, 2, 1)],
    "vamp": [(p, 2, p == 14) for p in range(0, 16, 2)],
}
PAT_KEYS["vamp2"] = PAT_KEYS["vamp"]
PAT_KEYS["cheio2"] = PAT_KEYS["cheio"]
PAT_KEYS["final"] = PAT_KEYS["cheio"]
PAT_KEYS["prep"] = PAT_KEYS["cheio"]

PAT_BASS = {  # (pos, dur, grau) ; R = nota do baixo do acorde, O = 8va, 5 = quinta, P = antecipação
    "leve": [(0, 6, "R"), (6, 2, "R"), (8, 4, "R"), (14, 2, "P")],
    "medio": [(0, 4, "R"), (6, 2, "R"), (8, 4, "R"), (12, 2, "5"), (14, 2, "P")],
    "pre": [(p, 2, "P" if p == 14 else "R") for p in range(0, 16, 2)],
    "cheio": [(0, 4, "R"), (6, 2, "O"), (8, 2, "R"), (10, 2, "5"), (12, 2, "R"), (14, 2, "P")],
    "vamp": [(0, 4, "R"), (6, 2, "O"), (8, 2, "R"), (10, 2, "5"), (12, 2, "R"), (14, 2, "P")],
}
PAT_BASS["vamp2"] = PAT_BASS["vamp"]
PAT_BASS["cheio2"] = PAT_BASS["cheio"]
PAT_BASS["final"] = PAT_BASS["cheio"]
PAT_BASS["prep"] = PAT_BASS["cheio"]

PAT_GTR = {  # guitarra: contratempos no verso/pré/vamp, acordes longos no refrão
    "leve": [(2, 2, 0), (6, 2, 0), (10, 2, 0), (14, 2, 0)],
    "medio": [(2, 2, 0), (6, 2, 0), (10, 2, 0), (14, 2, 0)],
    "pre": [(2, 2, 0), (6, 2, 0), (10, 2, 0), (14, 2, 0)],
    "cheio": [(0, 8, 0), (8, 6, 0), (14, 2, 1)],
    "vamp": [(2, 2, 0), (6, 2, 0), (10, 2, 0), (14, 2, 0)],
    "vamp2": [(0, 4, 0), (6, 2, 0), (8, 4, 0), (14, 2, 1)],
}
PAT_GTR["cheio2"] = PAT_GTR["cheio"]
PAT_GTR["final"] = PAT_GTR["cheio"]
PAT_GTR["prep"] = PAT_GTR["cheio"]


def events_for(pattern_of, make, special=None):
    evs = []
    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        st = STYLE[title]
        sp = special(bar, title, i, length) if special else None
        if sp is not None:
            evs += sp
            continue
        pat = pattern_of.get(st)
        if not pat:
            continue
        for item in pat:
            evs += make(bar, *item)
    return evs


def ending(bar, title, i, length):
    """Compassos especiais comuns: preparação (hits) e últimos compassos do Final."""
    return None


# ------------------------------------------------------------------ teclado (piano)
def build_piano():
    rh_ev, lh_ev = [], []
    prev = [None]

    def special(bar, title, i, length):
        if title == "Preparação":
            hits = [(0, 4), (6, 2), (12, 4)] if i == 0 else [(0, 2), (6, 10)]
            return [("H", bar, p, d) for p, d in hits]
        if title == "Final" and i >= 7:
            if i == length - 1:
                return [("H", bar, 0, 16)]
            return [("H", bar, 0, 8), ("H", bar, 8, 8)]
        if title == "Intro" and i == 0:
            return None
        return None

    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        st = STYLE[title]
        sp = special(bar, title, i, length)
        items = [(p, d, 0) for _h, _b, p, d in sp] if sp else PAT_KEYS[st]
        for p, d, push in items:
            sym = next_chord(bar) if push and next_chord(bar) != chord_at(bar, p) else chord_at(bar, p)
            v = voicing(sym, prev[0], 55, 64, 74)
            prev[0] = v
            fl = "!" if (title == "Final" and i == length - 1) else ("." if d <= 2 and st in ("pre", "vamp", "vamp2") else "")
            rh_ev.append((A(bar, p), d, tok_pitches(v), fl))
        # mão esquerda: baixo em oitavas, muda junto com o acorde
        lh_items = [(p, 8 if len(CH[bar]) > 1 or st != "leve" else 16) for p in ([0, 8] if (len(CH[bar]) > 1 or st != "leve") else [0])]
        if sp:
            lh_items = [(p, d) for _h, _b, p, d in sp]
        for p, d in lh_items:
            b = bass_note(chord_at(bar, p), 36, 47)
            fl = "!" if (title == "Final" and i == length - 1) else ""
            lh_ev.append((A(bar, p), d, tok_pitches([b, b + 12]), fl))
    return to_measures(rh_ev), to_measures(lh_ev)


# ------------------------------------------------------------------ órgão (pad)
def build_organ():
    ev, lh = [], []
    prev = None
    # regiões de acorde contínuas (liga compassos com o mesmo acorde)
    regions = []
    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        silent = (title == "Vamp" and i < 2) or title == "Preparação"
        for k, (p, sym) in enumerate(CH[bar]):
            end = CH[bar][k + 1][0] if k + 1 < len(CH[bar]) else BAR
            if silent:
                regions.append(None)
                continue
            if regions and regions[-1] and regions[-1][2] == sym and regions[-1][0] + regions[-1][1] == A(bar, p):
                s0, d0, _ = regions[-1]
                regions[-1] = (s0, d0 + end - p, sym)
            else:
                regions.append((A(bar, p), end - p, sym))
    for r in regions:
        if not r:
            continue
        s0, d0, sym = r
        v = voicing(sym, prev, 53, 62, 72, n=4, drop_root=False)
        prev = v
        last = s0 + d0 == NBARS * BAR
        ev.append((s0, d0, tok_pitches(v), "!" if last else ""))
        lh.append((s0, d0, name(bass_note(sym, 36, 47)), "!" if last else ""))
    return to_measures(ev), to_measures(lh)


# ------------------------------------------------------------------ guitarra
def build_guitar():
    ev = []
    prev = None
    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        st = STYLE[title]
        if title == "Parte 1" and i < 8:
            continue  # entra na 2ª metade da Parte 1
        if title == "Vamp" and i < 4:
            continue
        if title == "Preparação":
            items = [(0, 4, 0), (6, 2, 0), (12, 4, 0)] if i == 0 else [(0, 2, 0), (6, 10, 0)]
        elif title == "Final" and i >= 7:
            items = [(0, 16, 0)] if i == length - 1 else [(0, 8, 0), (8, 8, 0)]
        else:
            items = PAT_GTR[st]
        for p, d, push in items:
            sym = next_chord(bar) if push and next_chord(bar) != chord_at(bar, p) else chord_at(bar, p)
            pcs, r, b, _x, _y = chord_pcs(sym)
            tri = [r, pcs[1], pcs[2]] if len(pcs) >= 3 else pcs
            v = voicing_from(tri, prev)
            prev = v
            short = d <= 2 and st in ("leve", "medio", "pre", "vamp")
            fl = "!" if (title == "Final" and i == length - 1) else ("." if short else "")
            ev.append((A(bar, p), d, tok_pitches(v), fl))
    return to_measures(ev)


def voicing_from(tones, prev, lo=55, hi=64, top_max=72):
    best = None
    for start in range(lo, hi + 1):
        if start % 12 not in tones:
            continue
        v = [start]
        for t in sorted(set(tones), key=lambda t: (t - start) % 12)[1:]:
            v.append(v[0] + (t - start) % 12)
        if v[-1] > top_max:
            continue
        cost = sum(abs(a - c) for a, c in zip(v, prev)) if prev else abs(v[0] - 59)
        if best is None or cost < best[0]:
            best = (cost, v)
    return best[1]


# ------------------------------------------------------------------ baixo
def build_bass():
    ev = []
    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        st = STYLE[title]
        if title == "Preparação":
            items = [(0, 4, "R"), (6, 2, "R"), (12, 4, "R")] if i == 0 else [(0, 2, "R"), (6, 2, "R"), (8, 6, "R"), (14, 2, "P")]
        elif title == "Final" and i >= 7:
            items = [(0, 16, "R")] if i == length - 1 else [(0, 8, "R"), (8, 8, "R")]
        elif title == "Vamp" and i < 2:
            items = [(0, 4, "R"), (14, 2, "P")]
        else:
            items = PAT_BASS[st]
        for p, d, g in items:
            sym = chord_at(bar, p)
            root = bass_note(sym)
            if g == "P":
                nxt = next_chord(bar) if p >= 14 else sym
                m = bass_note(nxt)
            elif g == "O":
                m = root + 12
            elif g == "5":
                pcs, r, b, _x, _y = chord_pcs(sym)
                m = root + ((r + 7 - root) % 12 or 12)
                if m - root > 9:
                    m -= 12
            else:
                m = root
            fl = "!" if (title == "Final" and i == length - 1) else ""
            ev.append((A(bar, p), d, name(m), fl))
    return to_measures(ev)


# ------------------------------------------------------------------ bateria
def drum_bar(bar):
    title, i, length = section_of(bar)
    st = STYLE[title]
    last = i == length - 1
    first = i == 0
    hits = {p: set() for p in range(0, 16, 2)}

    def add(ps, *pieces):
        for p in ps:
            hits.setdefault(p, set()).update(pieces)

    if title == "Preparação":
        if i == 0:
            add([0], "crash", "kick")
            add([6], "crash", "kick", "snare")
            add([12], "crash", "kick", "snare")
            return [(p, 2 if p != 12 else 4, sorted(v)) for p, v in sorted(hits.items()) if v and p in (0, 6, 12)]
        return fill(full=True)
    if title == "Final" and i >= 7:
        if last:
            return [(0, 16, ["crash", "kick"])]
        add([0], "ride", "kick")
        add([4, 12], "ride")
        add([8], "ride", "snare")
        if i == 7:
            add([0], "crash")
        return [(p, 4, sorted(v)) for p, v in sorted(hits.items()) if v]
    if st == "leve":
        add(range(0, 16, 2), "hh")
        add([4, 12], "xstick")
        add([0, 8, 14], "kick")
    elif st == "medio":
        add(range(0, 16, 2), "hh")
        add([4, 12], "snare")
        add([0, 6, 8, 14], "kick")
    elif st == "pre":
        add(range(0, 16, 2), "hh")
        add([4, 12], "snare")
        add([0, 4, 8, 12], "kick")
    elif st in ("cheio", "cheio2", "final"):
        for p in range(0, 16, 2):
            add([p], "hh" if p % 4 == 0 else "hhopen")
        add([4, 12], "snare")
        add([0, 6, 8, 14], "kick")
        if i % 4 == 0:
            add([0], "crash")
    elif st == "vamp":
        add(range(0, 16, 2), "hh")
        add([0, 4, 8, 12], "kick")
        if i >= 2:
            add([4, 12], "snare")
        if i >= 4:
            add([6, 14], "kick")
    elif st == "vamp2":
        add(range(0, 16, 2), "ride")
        add([4, 12], "snare")
        add([0, 4, 8, 12], "kick")
        if i % 2 == 0:
            add([0], "crash")
    if first and title not in ("Parte 1",):
        add([0], "crash")
    if last and title not in ("Final",):
        return [(p, 2, sorted(v)) for p, v in sorted(hits.items()) if v and p < 8] + fill()
    return [(p, 2, sorted(v)) for p, v in sorted(hits.items()) if v]


def fill(full=False):
    """Virada em semicolcheias (2ª metade do compasso, ou o compasso inteiro)."""
    seq = (["snare"] * 8 if full else []) + ["snare", "snare", "snare", "snare", "tom1", "tom1", "tom2", "ftom"]
    start = 0 if full else 8
    out = [(start + k, 1, [pc]) for k, pc in enumerate(seq)]
    out[0] = (out[0][0], 1, sorted(set(out[0][2]) | {"kick"}))
    return out


def build_drums():
    """Duas vozes: mãos (haste para cima) e bumbo (haste para baixo)."""
    hands, feet = [], []
    for bar in range(1, NBARS + 1):
        title, i, length = section_of(bar)
        fl = "!" if (title == "Final" and i == length - 1) else ""
        for p, d, pcs in drum_bar(bar):
            up = [x for x in pcs if x != "kick"]
            if up:
                hands.append((A(bar, p), d, "p:" + "+".join(up), fl))
            if "kick" in pcs:
                feet.append((A(bar, p), d if fl else min(d, 2), "p:kick", fl))
    return to_measures(hands), to_measures(feet)


# ------------------------------------------------------------------ textos por seção
TXT = {
    "Bateria": {"Intro": "Groove cheio (chimbal aberto nos contratempos)", "Parte 1": "Aro no 2 e 4",
                "Pré-refrão": "Bumbo nos 4 tempos", "Refrão": "Groove cheio", "Parte 2": "Caixa no 2 e 4",
                "Vamp": "Bumbo + chimbal → + caixa → groove", "Vamp (Fá)": "Condução no ride",
                "Preparação": "Hits com a banda + virada", "Final": "Tag; meia-pulsação na rit."},
    "Baixo": {"Parte 1": "Antecipações em colcheia (\"and\" do 4)", "Pré-refrão": "Colcheias, linha cromática C–B–Bb–A",
              "Refrão": "Linha ativa com oitavas", "Vamp": "Só o 1 e a antecipação → linha cheia"},
    "Teclado": {"Parte 1": "Pad leve, acordes abertos", "Pré-refrão": "Colcheias (\"pumping\") curtas",
                "Refrão": "Comping sincopado", "Vamp": "Colcheias curtas"},
    "Órgão": {"Intro": "Drawbars cheios, Leslie rápido nos refrões", "Parte 1": "Pad suave (Leslie lento)",
              "Vamp": "Entra no 3º compasso, swells"},
    "Guitarra": {"Parte 1": "Entra no c. 17: contratempos curtos (clean)", "Refrão": "Acordes longos, deixar soar",
                 "Vamp": "Entra no 5º compasso"},
}


def main():
    sc = Score("Grandes Coisas", "Ministério Atitude",
               "Coro (SATB) + banda + metais · Etapa 2: seção rítmica", NBARS, beats_div=BAR, time=(4, 4))
    sc.keys = {1: -3, START["Vamp (Fá)"]: -1}
    sc.tempos[1] = (150, "Pop/Black gospel")
    coro = sc.add(Instrument("Coro (melodia guia)", "Coro", midi_program=54, sound_id="voice.vocals"))
    tec = sc.add(Instrument("Teclado (piano)", "Tecl.", staves=2, clefs=["G", "F"], midi_program=1,
                            sound_id="keyboard.piano"))
    org = sc.add(Instrument("Órgão (Hammond)", "Org.", staves=2, clefs=["G", "F"], midi_program=17,
                            sound_id="keyboard.organ.drawbar"))
    gtr = sc.add(Instrument("Guitarra", "Gtr.", diatonic=7, chromatic=12, midi_program=28,
                            sound_id="pluck.guitar.electric"))
    bx = sc.add(Instrument("Baixo", "Bx.", clef="F", diatonic=7, chromatic=12, midi_program=34,
                           sound_id="pluck.bass.electric"))
    dr = sc.add(Instrument("Bateria", "Bat.", clef="perc", percussion=True, sound="drums"))
    sc.group(1, 5, "bracket", "Seção rítmica")

    for mark, title, length, key in FORM:
        b = START[title]
        if mark:
            sc.marks[b] = (mark, title)
        else:
            coro.dir(b, "textb", title)
        if b > 1:
            sc.barlines[b - 1] = "light-light"
        dyn = LS.DYN.get(title)
        for part, nm in ((tec, "Teclado"), (org, "Órgão"), (gtr, "Guitarra"), (bx, "Baixo"), (dr, "Bateria")):
            if nm in TXT and title in TXT[nm]:
                part.dir(b, "text", TXT[nm][title])
            if dyn:
                part.dir(b, "dyn", dyn)
    for bar, items in CH.items():
        for p, sym in items:
            tec.harm(bar, sym, offset=p)
            gtr.harm(bar, sym, offset=p)

    mel = LS.build_measures()
    last = mel[NBARS].split()
    last[-1] += "!"
    mel[NBARS] = " ".join(last)
    rh, lh = build_piano()
    orh, olh = build_organ()
    g, bs, (dh, df) = build_guitar(), build_bass(), build_drums()
    for b in range(1, NBARS + 1):
        coro.put(b, mel[b])
        tec.put(b, rh[b], staff=1)
        tec.put(b, lh[b], staff=2)
        org.put(b, orh[b], staff=1)
        org.put(b, olh[b], staff=2)
        gtr.put(b, g[b])
        bx.put(b, bs[b])
        dr.put(b, dh[b], df[b])
    out = os.path.join(HERE, "grandes-coisas-ritmica.musicxml")
    sc.write(out)
    print(f"{out}: {NBARS} compassos")


if __name__ == "__main__":
    main()
