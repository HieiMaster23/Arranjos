"""Grandes Coisas - Etapa 3: coro SATB (+ grade completa com a seção rítmica).

Gera (MusicXML 3.1):
  - `grandes-coisas-coro.musicxml`  : Soprano, Contralto, Tenor, Baixo (com letra)
  - `grandes-coisas-grade.musicxml` : coro SATB + Teclado, Órgão, Guitarra, Baixo, Bateria

Fontes únicas: forma/melodia/letra/harmonia em `gerar_leadsheet.py`, banda em `gerar_ritmica.py`.
As vozes internas saem da harmonia gospel (tons do acorde mais próximos, com condução de
vozes e limites de tessitura); texturas por seção em `texture()`.
Alturas em MIDI (altura real); o Tenor usa clave de sol 8vb.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ferramentas"))
import gerar_leadsheet as LS  # noqa: E402
import gerar_ritmica as R  # noqa: E402
from mxl import Score, Instrument, chord_pcs, midi, parse_pitch, STEPS, STEP_SEMI  # noqa: E402

BAR = LS.BAR
START, FORM, NBARS = LS.START, LS.FORM, LS.NBARS
VOZES = ["S", "A", "T", "B"]

# tessituras (altura real, MIDI): (mínimo, máximo confortável para harmonia)
RANGE = {"S": (62, 77), "A": (57, 74), "T": (50, 65), "B": (41, 60)}


# ------------------------------------------------------------------ utilidades harmônicas
def scale_of(bar):
    return [3, 5, 7, 8, 10, 0, 2] if LS.key_of(bar) == "Eb" else [5, 7, 9, 10, 0, 2, 4]


def diatonic(m, steps, bar):
    """Move a nota m por graus da escala (steps > 0 sobe)."""
    sc = scale_of(bar)
    pc = m % 12
    if pc not in sc:  # nota cromática: aproxima para a nota da escala mais próxima abaixo
        while m % 12 not in sc:
            m -= 1
    i = sc.index(m % 12)
    out = m
    for _ in range(abs(steps)):
        j = (i + (1 if steps > 0 else -1)) % 7
        delta = (sc[j] - sc[i]) % 12 if steps > 0 else -((sc[i] - sc[j]) % 12)
        out += delta
        i = j
    return out


def tones(sym):
    pcs, r, b, _root, _bass = chord_pcs(sym)
    return set(pcs), r, b


def pick(cands, prev, avoid=()):
    if not cands:
        return None
    return min(cands, key=lambda c: (c % 12 in avoid, abs(c - prev) if prev else 0, -c))


def above(m, sym, bar, prev, cap):
    ts, r, b = tones(sym)
    if m % 12 in ts:
        c = [x for x in range(m + 3, min(m + 8, cap) + 1) if x % 12 in ts and x % 12 != m % 12]
        got = pick(c, prev)
        if got:
            return got
        return m  # sem espaço: uníssono com a melodia
    d = diatonic(m, 2, bar)
    return d if d <= cap else m


def below(m, sym, bar, prev, lo, hi, avoid=()):
    ts, r, b = tones(sym)
    if m % 12 in ts:
        c = [x for x in range(max(m - 9, lo), min(m - 3, hi) + 1) if x % 12 in ts and x % 12 != m % 12]
        got = pick(c, prev, avoid)
        if got:
            return got
    d = diatonic(m, -2, bar)
    while d > hi:
        d -= 12
    while d < lo:
        d += 12
    return d


def bass_of(sym, prev):
    ts, r, b = tones(sym)
    c = [x for x in range(41, 58) if x % 12 == b]  # Fá2–Lá3
    return pick(c, prev or 48)


# ------------------------------------------------------------------ grafia
LETTER_STEPS = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6}


def spell(m, sym, bar):
    """Nome da nota: pela cifra (tons do acorde) ou pela escala do tom; senão bemóis."""
    pc = m % 12
    octv = m // 12 - 1
    s = sym.replace("(", "").replace(")", "")
    if "/" in s and not s.endswith("6/9"):
        s, bass = s.split("/")
        if midi(bass + "4") % 12 == pc:
            return fix(bass, octv, m)
    root = s[0] + ("b" if len(s) > 1 and s[1] == "b" else ("#" if len(s) > 1 and s[1] == "#" else ""))
    rpc = midi(root + "4") % 12
    rel = (pc - rpc) % 12
    ts, _r, _b = tones(sym)
    if pc in ts:
        steps = LETTER_STEPS[rel]
        if rel == 3 and "#9" in s:
            steps = 1
        if rel == 6 and ("dim" in s or "m7b5" in s):
            steps = 4
        if rel == 9 and "dim" in s:
            steps = 6  # 7ª diminuta (Adim7: Sol bemol)
        letter = STEPS[(STEPS.index(root[0]) + steps) % 7]
        return fix(letter, octv, m)
    flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    return f"{flats[pc]}{octv}"


def simple(name, m):
    """Evita grafias difíceis para o coro (Dób, Fáb, Mi#, Si#, dobrados): usa a enarmônica simples."""
    body = name.rstrip("0123456789-")
    if "bb" in body or "##" in body or body in ("Cb", "Fb", "E#", "B#"):
        flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        return f"{flats[m % 12]}{m // 12 - 1}"
    return name


def fix(letter_or_name, octv, m):
    """Ajusta acidente/oitava para que o nome soe exatamente m."""
    letter = letter_or_name[0]
    base = STEP_SEMI[STEPS.index(letter)]
    for o in (octv - 1, octv, octv + 1):
        alter = m - (12 * (o + 1) + base)
        if -2 <= alter <= 2:
            acc = "b" * -alter if alter < 0 else "#" * alter
            return simple(f"{letter}{acc}{o}", m)
    raise ValueError((letter_or_name, m))


# ------------------------------------------------------------------ texturas
def sec(bar):
    return R.section_of(bar)


def texture(bar, pos):
    """Papel de cada voz no instante (bar, pos)."""
    title, i, length = sec(bar)
    rest = {"S": None, "A": None, "T": None, "B": None}
    if title in ("Intro",):
        return rest
    if title in ("Parte 1",):
        return {"S": "mel", "A": "mel", "T": "oh", "B": "oh"}
    if title in ("Parte 2",):
        return {"S": "ooh", "A": "ooh", "T": "mel8", "B": "mel8"}
    if title in ("Pré-refrão", "Pré-refrão 2"):
        bx = "root" if (title == "Pré-refrão 2" or i >= 8) else None
        return {"S": "mel", "A": "below", "T": "below2", "B": bx}
    if title in ("Refrão", "Interlúdio"):
        return {"S": "above", "A": "mel", "T": "below2", "B": "root"}
    if title == "Refrão 2":
        if i <= 12:
            return {"S": "above", "A": "mel", "T": "below2", "B": "root"}
        return {"S": "desc", "A": "mel", "T": "mel8", "B": "root"}
    if title == "Vamp":
        if i < 2:
            return {"S": None, "A": None, "T": "mel8", "B": "mel16"}
        if i < 4:
            return {"S": None, "A": "mel", "T": "mel8", "B": "mel16"}
        if i < 6:
            return {"S": "mel", "A": "below", "T": "mel8", "B": "root"}
        return {"S": "mel", "A": "below", "T": "below2", "B": "root"}
    if title in ("Vamp (Fá)", "Preparação", "Final"):
        return {"S": "mel", "A": "below", "T": "below2", "B": "root"}
    if title == "Refrão final":
        t = (i * BAR + pos)
        if 8 * BAR <= t < 8 * BAR + 10:        # "To-dos di-rão," (mulheres chamam)
            return {"S": "mel", "A": "below", "T": None, "B": None}
        if 8 * BAR + 10 <= t < 9 * BAR + 12:   # "to-dos di-rão" (homens respondem)
            return {"S": None, "A": None, "T": "mel8", "B": "below8"}
        return {"S": "mel", "A": "below", "T": "below2", "B": "root"}
    return rest


# ------------------------------------------------------------------ geração
def melody_events():
    """Eventos da melodia em tempo absoluto: (início, dur, midi, nome, sílaba, flags)."""
    out = []
    for bar, pos, dur, pitch, syl, flags in sorted(LS.MEL):
        if dur <= 0:
            continue
        nm = LS.target(pitch, bar)
        out.append(((bar - 1) * BAR + pos, dur, midi(nm), nm, syl, flags))
    return out


def chord_changes(start, end):
    pts = [start]
    for t in range(start + 1, end):
        b, p = t // BAR + 1, t % BAR
        if any(q == p for q, _ in R.CH[b]) and t > start:
            pts.append(t)
    return pts


def harmonize():
    ev = {v: [] for v in VOZES}
    prev = {v: None for v in VOZES}
    slur_open = {v: False for v in VOZES}
    jsegs = {}
    mel = melody_events()
    for start, dur, m, nm, syl, flags in mel:
        bar0, pos0 = start // BAR + 1, start % BAR
        roles = texture(bar0, pos0)
        cuts = chord_changes(start, start + dur)
        for v in VOZES:
            role = roles[v]
            if role is None or role in ("oh", "ooh", "desc"):
                continue
            if role in ("mel", "mel8", "mel16"):
                down = {"mel": 0, "mel8": 1, "mel16": 2}[role]
                tm = m - 12 * down
                s_, a_, o_ = parse_pitch(nm)
                name = f"{s_}{'b' * -a_ if a_ < 0 else '#' * a_}{o_ - down}"
                ev[v].append((start, dur, tm, name, syl, flags))
                prev[v] = tm
                slur_open[v] = ("(" in flags) or (slur_open[v] and ")" not in flags)
                continue
            # vozes harmônicas: recalcula em cada troca de acorde sob a nota
            if role == "root" or role == "below8":
                segs = []
                for k, a in enumerate(cuts):
                    e = cuts[k + 1] if k + 1 < len(cuts) else start + dur
                    bb, pp = a // BAR + 1, a % BAR
                    sym = R.chord_at(bb, pp)
                    x = bass_of(sym, prev[v]) if role == "root" else \
                        below(m - 12, sym, bb, prev[v], RANGE["B"][0], RANGE["B"][1])
                    segs.append((a, e - a, x, spell(x, sym, bb)))
                    prev[v] = x
            else:
                segs = jsegs.setdefault((start, v), None)
                if segs is None:
                    sol = joint(start, dur, m, nm, cuts, roles, prev)
                    for vv, ss in sol.items():
                        jsegs[(start, vv)] = ss
                    segs = jsegs[(start, v)]
                if segs:
                    prev[v] = segs[-1][2]
            # junta segmentos iguais (ligadura) e marca melisma nos seguintes
            merged = []
            for a, d, x, nmx in segs:
                if merged and merged[-1][2] == x:
                    s0, d0, x0, n0 = merged[-1]
                    merged[-1] = (s0, d0 + d, x0, n0)
                else:
                    merged.append((a, d, x, nmx))
            # ligadura de expressão: segue a da melodia; só cria uma nova se nenhuma estiver aberta
            extra = len(merged) > 1 and not slur_open[v] and "(" not in flags and ")" not in flags
            for k, (a, d, x, nmx) in enumerate(merged):
                fl = ""
                if k == 0 and ("(" in flags or extra):
                    fl += "("
                if k == len(merged) - 1 and (")" in flags or extra):
                    fl += ")"
                ev[v].append((a, d, x, nmx, syl if k == 0 else "_", fl))
            if "(" in flags:
                slur_open[v] = True
            if ")" in flags:
                slur_open[v] = False
    return ev


HARM_ROLES = ("above", "below", "below2")
LIM = {"S": (60, 77), "A": (55, 74), "T": (48, 65)}


def joint(start, dur, m, nm, cuts, roles, prev):
    """Escolhe juntas as vozes harmônicas (S/A/T) para cada trecho de acorde sob a nota."""
    hv = [v for v in ("S", "A", "T") if roles[v] in HARM_ROLES]
    fixed = {v: (m if roles[v] == "mel" else m - 12) for v in ("S", "A", "T") if roles[v] in ("mel", "mel8")}
    out = {v: [] for v in hv}
    last = dict(prev)
    for k, a in enumerate(cuts):
        e = cuts[k + 1] if k + 1 < len(cuts) else start + dur
        bar, pos = a // BAR + 1, a % BAR
        sym = R.chord_at(bar, pos)
        pcs, r, bpc, *_ = chord_pcs(sym)
        ts = set(pcs)
        third = pcs[1]
        chordal = m % 12 in ts
        cands = {}
        for v in hv:
            lo, hi = LIM[v]
            if roles[v] == "above":
                lo, hi = m + 1, min(m + 9, hi)
            elif roles[v] == "below":
                lo, hi = max(m - 10, lo), min(m - 1, hi)
            if chordal:
                c = [x for x in range(lo, hi + 1) if x % 12 in ts]
            else:  # nota de passagem: terça/sexta diatônica em movimento paralelo
                c = [diatonic(m, 2, bar)] if roles[v] == "above" else \
                    [x for x in (diatonic(m, -2, bar), diatonic(m, -2, bar) - 12, diatonic(m, -5, bar))
                     if lo - 2 <= x <= hi]
            c = c or [m if roles[v] != "below2" else max(lo, min(hi, m - 12))]
            cands[v] = c
        best = None

        def rec(i, cur):
            nonlocal best
            if i == len(hv):
                cost = score(cur, fixed, m, ts, third, r, last, roles)
                if best is None or cost < best[0]:
                    best = (cost, dict(cur))
                return
            v = hv[i]
            for x in cands[v]:
                cur[v] = x
                rec(i + 1, cur)
            del cur[v]
        rec(0, {})
        for v in hv:
            x = best[1][v]
            out[v].append((a, e - a, x, spell(x, sym, bar)))
            last[v] = x
    return out


def score(cur, fixed, m, ts, third, root, last, roles):
    allv = dict(fixed)
    allv.update(cur)
    order = [allv[v] for v in ("S", "A", "T") if v in allv]
    cost = 0
    # ordem S >= A >= T (cruzamento proibido, uníssono penalizado)
    for hi_, lo_ in zip(order, order[1:]):
        if lo_ > hi_:
            return 1e9
        if lo_ == hi_:
            cost += 6
        if hi_ - lo_ > 12:
            cost += 10
    pcs_used = [x % 12 for x in order] + [m % 12]
    if third in ts and third not in pcs_used and m % 12 in ts:
        cost += 5
    cost += 3 * (len(pcs_used) - len(set(pcs_used)))
    if root in pcs_used and len(set(pcs_used)) < 3:
        cost += 1
    for v, x in cur.items():
        if last.get(v) is not None:
            cost += abs(x - last[v]) * 1.0
        # acima do "belt" confortável: Tenor > Mi4, Soprano > Ré5, Contralto > Dó5
        if v == "T" and x > 64:
            cost += 4 * (x - 64)
        if v == "S" and x > 74:
            cost += 4 * (x - 74)
        if v == "A" and x > 72:
            cost += 3 * (x - 72)
    return cost


def segs_ref(ev, v, t):
    for a, d, x, *_ in reversed(ev[v]):
        if a <= t < a + d:
            return x
    return None


def pc_at(ev, v, t):
    x = segs_ref(ev, v, t)
    return x % 12 if x is not None else -1


def responses(ev):
    """Parte 1: T+B respondem 'Oh' no 2º compasso de cada verso (sobre a nota longa)."""
    b0 = START["Parte 1"]
    pt, pb = 57, 44
    for k in range(8):
        bar = b0 + 2 * k + 1
        sym = R.chord_at(bar, 8)
        ts, r, b = tones(sym)
        t = pick([x for x in range(55, 63) if x % 12 in ts and x % 12 != b], pt)
        bb = bass_of(sym, pb)
        a = (bar - 1) * BAR + 8
        ev["T"].append((a, 6, t, spell(t, sym, bar), "Oh", ""))
        ev["B"].append((a, 6, bb, spell(bb, sym, bar), "Oh", ""))
        pt, pb = t, bb


def pads(ev, voices, first, nbars, ranges, word):
    """Pads ('Ooh'/'Oh'): uma nota por acorde, ligando acordes iguais."""
    prev = {v: None for v in voices}
    regions = []
    for bar in range(first, first + nbars):
        for k, (p, sym) in enumerate(R.CH[bar]):
            end = R.CH[bar][k + 1][0] if k + 1 < len(R.CH[bar]) else BAR
            a = (bar - 1) * BAR + p
            if regions and regions[-1][2] == sym and regions[-1][0] + regions[-1][1] == a:
                regions[-1] = (regions[-1][0], regions[-1][1] + end - p, sym, regions[-1][3])
            else:
                regions.append((a, end - p, sym, bar))
    for idx, (a, d, sym, bar) in enumerate(regions):
        ts, r, b = tones(sym)
        used = set()
        for v in voices:
            lo, hi = ranges[v]
            c = [x for x in range(lo, hi + 1) if x % 12 in ts and x % 12 not in used and x % 12 != r]
            x = pick(c, prev[v] or (lo + hi) // 2)
            used.add(x % 12)
            prev[v] = x
            ev[v].append((a, d, x, spell(x, sym, bar), word if idx == 0 else "_", ""))


def final_chord(ev):
    """Último compasso: acorde aberto F6/9 com fermata (melodia 'mim' vai para o Tenor)."""
    last = (NBARS - 1) * BAR
    for v in VOZES:
        ev[v] = [e for e in ev[v] if e[0] < last]
        # corta o que atravessa o último compasso
        ev[v] = [(a, last - a, x, n, s, f.replace(")", "")) if a + d > last else (a, d, x, n, s, f)
                 for a, d, x, n, s, f in ev[v]]
    sym = "F6/9"
    for v, x in (("S", 72), ("A", 69), ("T", 65), ("B", 53)):  # Dó5, Lá4, Fá4, Fá3
        ev[v].append((last, BAR, x, spell(x, sym, NBARS), "_", ")!"))


# ------------------------------------------------------------------ escrita
def to_measures(events):
    bars = {b: [] for b in range(1, NBARS + 1)}
    for start, dur, x, nm, syl, flags in sorted(events, key=lambda e: e[0]):
        t, end = start, start + dur
        pieces = []
        while t < end:
            b = t // BAR + 1
            seg = min(end, b * BAR) - t
            for pp, d in LS.split_dur(t % BAR, seg):
                pieces.append((b, pp, d))
            t += seg
        for i, (b, pp, d) in enumerate(pieces):
            fl = "~" if i < len(pieces) - 1 else ""
            if i == 0 and "(" in flags:
                fl += "("
            if i == len(pieces) - 1:
                fl += "".join(c for c in flags if c in ")!")
            lyr = f"|{syl}" if i == 0 and syl != "_" else ""
            bars[b].append((pp, d, f"{nm}/{d}{fl}{lyr}"))
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


TXT = {
    "S": {"Parte 1": "uníssono com as contraltos", "Pré-refrão": "melodia", "Refrão": "acima da melodia",
          "Parte 2": "\"Ooh\" (pad)", "Vamp": "entra no 5º compasso", "Vamp (Fá)": "melodia, tutti"},
    "A": {"Parte 1": "melodia (uníssono com as sopranos)", "Refrão": "melodia", "Parte 2": "\"Ooh\" (pad)",
          "Vamp": "entra no 3º compasso"},
    "T": {"Parte 1": "respostas", "Parte 2": "melodia 8vb (uníssono com os baixos)", "Vamp": "melodia 8vb"},
    "B": {"Parte 1": "respostas", "Pré-refrão": "entra em \"Eu vou cantar\"", "Parte 2": "melodia (uníssono com os tenores)",
          "Vamp": "melodia (8va abaixo dos tenores)"},
}


def choir_parts(sc):
    s = sc.add(Instrument("Soprano", "S.", midi_program=53, sound_id="voice.soprano"))
    a = sc.add(Instrument("Contralto", "A.", midi_program=53, sound_id="voice.alto"))
    t = sc.add(Instrument("Tenor", "T.", clef="G8", midi_program=53, sound_id="voice.tenor"))
    b = sc.add(Instrument("Baixo (coro)", "B.", clef="F", midi_program=53, sound_id="voice.bass"))
    return {"S": s, "A": a, "T": t, "B": b}


def build_choir():
    ev = harmonize()
    responses(ev)
    pads(ev, ["S", "A"], START["Parte 2"], 16, {"S": (65, 72), "A": (60, 67)}, "Ooh")
    pads(ev, ["S"], START["Refrão 2"] + 13, 12, {"S": (70, 77)}, "Oh")
    final_chord(ev)
    return ev, {v: to_measures(ev[v]) for v in VOZES}


def report(ev):
    print("Extensão por voz e seção (altura real):")
    for v in VOZES:
        by = {}
        for a, d, x, nm, *_ in ev[v]:
            title = sec(a // BAR + 1)[0]
            lo, hi = by.get(title, (999, 0))
            by[title] = (min(lo, x), max(hi, x))
        allx = [e[2] for e in ev[v]]
        print(f"  {v}: {min(allx)}–{max(allx)}  " + "; ".join(f"{t}: {lo}-{hi}" for t, (lo, hi) in by.items()))


def setup(sc, parts_first):
    sc.keys = {1: -3, START["Vamp (Fá)"]: -1}
    sc.tempos[1] = (150, "Pop/Black gospel")
    for mark, title, length, key in FORM:
        b = START[title]
        if mark:
            sc.marks[b] = (mark, title)
        else:
            parts_first.dir(b, "textb", title)
        if b > 1:
            sc.barlines[b - 1] = "light-light"


def main():
    ev, meas = build_choir()
    report(ev)
    # --- só o coro
    sc = Score("Grandes Coisas", "Ministério Atitude", "Coro SATB · Etapa 3", NBARS, beats_div=BAR, time=(4, 4))
    parts = choir_parts(sc)
    sc.group(0, 3, "bracket", "Coro")
    setup(sc, parts["S"])
    for v, p in parts.items():
        fill_choir(p, v, meas[v])
    sc.write(os.path.join(HERE, "grandes-coisas-coro.musicxml"))
    # --- grade completa
    g = Score("Grandes Coisas", "Ministério Atitude", "Coro SATB + banda · grade (Etapas 1–3)", NBARS,
              beats_div=BAR, time=(4, 4))
    parts = choir_parts(g)
    g.group(0, 3, "bracket", "Coro")
    setup(g, parts["S"])
    for v, p in parts.items():
        fill_choir(p, v, meas[v])
    band = R.band_parts(g)
    g.group(4, 8, "bracket", "Banda")
    R.fill_band(band)
    g.write(os.path.join(HERE, "grandes-coisas-grade.musicxml"))
    print("ok: grandes-coisas-coro.musicxml, grandes-coisas-grade.musicxml")


def fill_choir(p, v, meas):
    for mark, title, length, key in FORM:
        b = START[title]
        if title in TXT[v]:
            p.dir(b, "text", TXT[v][title])
        dyn = LS.DYN.get(title)
        if dyn:
            p.dir(b, "dyn", dyn)
    p.dir(START["Final"] + 6, "text", "rit.")
    for b in range(1, NBARS + 1):
        p.put(b, meas[b])


if __name__ == "__main__":
    main()
