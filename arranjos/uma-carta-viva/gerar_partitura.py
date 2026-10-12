"""Uma Carta Viva (GET Worship) - versão instrumental "Camp Inspired".

Gera `uma-carta-viva.musicxml` (MusicXML 3.1). Tudo é escrito em altura real; o escritor
(`ferramentas/mxl.py`) cuida da transposição dos instrumentos transpositores.

Forma (ver estrutura.md):
  1-8  Intro (Eb)        9-10 Vamp          11-18 [A] Estrofe
  19-26 [B] Pré-refrão   27-42 [C] Refrão   43-50 [D] Interlúdio
  51-58 [E] Pré-refrão 2 59 transição       60-75 [F] Refrão 2 (F)
  76-  Ponte (a definir)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ferramentas"))
from mxl import (Score, Instrument, Ev, parse_voice, parse_pitch, pitch_str, midi, chord_pcs,  # noqa: E402
                 STEPS, STEP_SEMI)

NBARS = 75
BAR = 12
H = 6  # meio compasso (semínima pontuada)

# ------------------------------------------------------------------ harmonia (altura real)
# compasso -> lista de (offset, cifra)
CH = {}


def ch(bar, *syms):
    if len(syms) == 1:
        CH[bar] = [(0, syms[0])]
    else:
        CH[bar] = [(0, syms[0]), (H, syms[1])]


INTRO = [("Eb",), ("Fm7",), ("Eb/G",), ("Ab(add9)",), ("Ab", "Bb/Ab"), ("Gm7", "Cm7"),
         ("Fm7", "Ab/Bb"), ("Bb7sus4", "Bb7")]
for i, c in enumerate(INTRO, 1):
    ch(i, *c)
ch(9, "Eb"); ch(10, "Ab/Eb", "Eb")
ESTROFE = [("Bb/D", "Ab/C"), ("Eb", "Fm7"), ("Eb",), ("Eb",), ("Bb/D", "Ab/C"), ("Cm/G", "Fm7"),
           ("Eb/Bb",), ("Eb", "Eb/G")]
for i, c in enumerate(ESTROFE):
    ch(11 + i, *c)
PRE = [("Fm7",), ("Fm7",), ("Eb/G",), ("Eb/G",), ("Abmaj7",), ("Ab(add9)",), ("Abm6",), ("Abm6", "Bb")]
for i, c in enumerate(PRE):
    ch(19 + i, *c)
REFRAO = [("Eb",), ("Eb",), ("Fm7",), ("Fm7",), ("Cm7", "Cm7/Bb"), ("Bbsus4", "Eb/G"),
          ("Ab(add9)",), ("Ab", "Bb/Ab")]
for k in range(2):
    for i, c in enumerate(REFRAO):
        ch(27 + 8 * k + i, *c)
INTER = [("Eb",), ("Eb",), ("Fm7",), ("Fm7",), ("Eb/G",), ("Eb/G",), ("Ab(add9)",), ("Ab",)]
for i, c in enumerate(INTER):
    ch(43 + i, *c)
PRE2 = [("Fm7",), ("Fm7",), ("Eb/G",), ("Eb/G",), ("Abmaj7",), ("Ab(add9)",), ("Abmaj7",), ("Ab6/9",)]
for i, c in enumerate(PRE2):
    ch(51 + i, *c)
ch(59, "C7sus4", "C7")
REFRAO_F = [("F",), ("F",), ("Gm7",), ("Gm7",), ("Dm7", "Dm7/C"), ("Csus4", "F/A"),
            ("Bb(add9)",), ("Bb", "C/Bb")]
for k in range(2):
    for i, c in enumerate(REFRAO_F):
        ch(60 + 8 * k + i, *c)

KEY_EB = ["Eb", "F", "G", "Ab", "Bb", "C", "D"]
KEY_F = ["F", "G", "A", "Bb", "C", "D", "E"]


def key_scale(bar):
    return KEY_F if bar >= 60 else KEY_EB


def chord_at(bar, off):
    sym = CH[bar][0][1]
    for o, s in CH[bar]:
        if o <= off:
            sym = s
    return sym


def chord_spans(bar):
    """[(offset, dur, cifra)]"""
    c = CH[bar]
    out = []
    for i, (o, s) in enumerate(c):
        end = c[i + 1][0] if i + 1 < len(c) else BAR
        out.append((o, end - o, s))
    return out


# ------------------------------------------------------------------ melodia (altura real, Eb)
# Transcrita da fonte (Ré) e transposta 2m acima. Chaves = compassos NOVOS.
MEL_EB = {
    10: "r/6 G4/2( Ab4/2 Bb4/2)",
    11: "D5/3( Eb5/3 C5/3 D5/3)", 12: "Bb4/3( C5/3 Ab4/3 Ab4/1 Ab4/2)", 13: "Ab4/1( G4/4~ G4/1~ G4/6)",
    14: "r/6 G4/2( Ab4/2 Bb4/2)",
    15: "D5/3( Eb5/3 C5/3 D5/3)", 16: "Bb4/3( C5/3 Ab4/3 Ab4/1 Ab4/2)", 17: "Ab4/1( G4/4~ G4/1~ G4/6)",
    18: "r/6 Eb4/2( F4/2 G4/2)",
    19: "G4/4( Bb3/2 F4/6~", 20: "F4/6) Eb4/2( F4/2 G4/2)", 21: "G4/4( Bb3/2 F4/6~",
    22: "F4/4) r/1 Eb4/1( Eb4/2 F4/1 G4/1 Ab4/2)", 23: "G4/4( F4/2 Eb4/6~", 24: "Eb4/6) Eb4/2( F4/1 G4/1 Ab4/2)",
    25: "G4/4( Bb3/2 F4/6~", 26: "F4/6) r/6",
    27: "Bb4/4 G4/2 Bb4/4 G4/2", 28: "F4/3( Eb4/1 Eb4/2) Eb4/2( G4/1 Bb4/3~", 29: "Bb4/4) G4/2 Bb4/4 G4/2",
    30: "F4/4( Eb4/2 F4/2 C5/2 Bb4/2~", 31: "Bb4/4) r/2 Bb4/4 G4/2", 32: "F4/4( Eb4/2 F4/1 G4/1 F4/2 Eb4/2)",
    33: "Eb4/2( F4/4 G4/6)", 34: "G4/4( F4/1 Eb4/1 F4/6)",
    46: "r/12",
    47: "Bb4/12~", 48: "Bb4/12", 49: "C5/12~", 50: "C5/6 G4/2( Ab4/2 Bb4/2)",
    51: "Bb4/4( F4/2 Ab4/6~", 52: "Ab4/6) G4/2( Ab4/2 Bb4/2)", 53: "Bb4/4( G4/2 Bb4/6~",
    54: "Bb4/4) r/1 G4/1( G4/2 Ab4/1 Bb4/1 C5/2)", 55: "Bb4/4( Ab4/2 C5/6~", 56: "C5/6) G4/2( Ab4/1 Bb4/1 C5/2)",
    57: "Bb4/4( F4/2 C5/6~", 58: "C5/6) r/6",
}
for k in range(8):  # 2a metade do refrão = igual à 1a
    MEL_EB[35 + k] = MEL_EB[27 + k]


def mel(bar):
    return MEL_EB[bar]


def mel_f(bar):
    """Refrão 2 em Fá: mesma melodia do refrão 1 subida 1 tom."""
    src = MEL_EB[27 + (bar - 60) % 8]
    return shift_tokens(src, 1, 2)


# ------------------------------------------------------------------ utilidades de altura
def tpos(p):
    s, a, o = parse_pitch(p)
    return s, a, o


def shift_pitch(p, diatonic, chromatic):
    s, a, o = parse_pitch(p)
    idx = STEPS.index(s) + diatonic
    no = o + idx // 7
    ns = STEPS[idx % 7]
    target = midi(p) + chromatic
    na = target - (12 * (no + 1) + STEP_SEMI[STEPS.index(ns)])
    return pitch_str(ns, na, no)


def octave(p, n):
    s, a, o = parse_pitch(p)
    return pitch_str(s, a, o + n)


def shift_tokens(toks, diatonic, chromatic):
    out = []
    for t in toks.split():
        body, rest = t.split("/", 1)
        if body == "r":
            out.append(t)
            continue
        if body.startswith("["):
            ps = [shift_pitch(x, diatonic, chromatic) for x in body[1:-1].split(",")]
            out.append("[" + ",".join(ps) + "]/" + rest)
        else:
            out.append(shift_pitch(body, diatonic, chromatic) + "/" + rest)
    return " ".join(out)


def oct_tokens(toks, n):
    return shift_tokens(toks, 7 * n, 12 * n)


def spelled_tones(sym):
    """[(pc, step, alter)] das notas do acorde, grafadas a partir da fundamental."""
    pcs, r, b, root, bass = chord_pcs(sym)
    rs, ra, _ = parse_pitch(root + "4")
    deg = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6}
    out = []
    for pc in pcs:
        iv = (pc - r) % 12
        st = STEPS[(STEPS.index(rs) + deg[iv]) % 7]
        alt = (pc - STEP_SEMI[STEPS.index(st)] + 6) % 12 - 6
        out.append((pc, st, alt))
    return out


def bass_name(sym):
    pcs, r, b, root, bass = chord_pcs(sym)
    return bass or root


def place(step, alter, target, lo, hi):
    """Escolhe a oitava mais próxima de `target` dentro de [lo, hi] (midi)."""
    best = None
    for o in range(0, 9):
        p = pitch_str(step, alter, o)
        m = midi(p)
        if lo <= m <= hi:
            if best is None or abs(m - target) < abs(midi(best) - target):
                best = p
    if best is None:
        raise ValueError(f"sem oitava para {step}{alter} em [{lo},{hi}]")
    return best


def nearest_tone(sym, target, lo, hi, exclude=()):
    best = None
    for pc, st, al in spelled_tones(sym):
        if pc in exclude:
            continue
        for o in range(0, 9):
            p = pitch_str(st, al, o)
            m = midi(p)
            if lo <= m <= hi and (best is None or abs(m - target) < abs(midi(best) - target)):
                best = p
    if best is None:
        return nearest_tone(sym, target, lo, hi + 12) if hi - lo < 30 else None
    return best


def note_of(name, target, lo=0, hi=127):
    s, a, _ = parse_pitch(name + "4")
    return place(s, a, target, lo, hi)


# ------------------------------------------------------------------ geradores de textura
def pad_voices(bars, n, start, lo, hi, prefer_no_root=True):
    """Condução de vozes para pads (busca exaustiva da melhor combinação).
    Retorna {bar: [(off, dur, [p_agudo..p_grave])]}."""
    from itertools import combinations
    prev = [midi(x) for x in start]
    res = {}
    for bar in bars:
        segs = []
        for off, dur, sym in chord_spans(bar):
            tones = spelled_tones(sym)
            r = chord_pcs(sym)[1]
            cands = []
            for pc, st, al in tones:
                for o in range(0, 9):
                    p = pitch_str(st, al, o)
                    if lo <= midi(p) <= hi:
                        cands.append((midi(p), p, pc))
            cands.sort(reverse=True)
            best = None
            for combo in combinations(cands, n):
                ms = [c[0] for c in combo]
                if len(set(ms)) < n:
                    continue
                pcs_used = [c[2] for c in combo]
                pen = sum(abs(m - pv) for m, pv in zip(ms, prev))
                pen += 6 * (len(pcs_used) - len(set(pcs_used)))
                if prefer_no_root and len(tones) > n and r in pcs_used:
                    pen += 2
                for a, b in zip(ms, ms[1:]):
                    gap = a - b
                    if gap == 1: pen += 8
                    elif gap == 2: pen += 5
                    elif gap > 12: pen += 4
                if best is None or pen < best[0]:
                    best = (pen, [c[1] for c in combo])
            chosen = best[1]
            prev = [midi(x) for x in chosen]
            segs.append((off, dur, chosen))
        res[bar] = segs
    return res


def segs_to_tokens(segs_by_bar, voice_idx, tie_same=True, art=""):
    """Converte resultado de pad_voices em tokens para uma voz (ou lista de vozes => acorde)."""
    out = {}
    bars = sorted(segs_by_bar)
    flat = []
    for b in bars:
        for off, dur, ps in segs_by_bar[b]:
            pv = [ps[i] for i in voice_idx] if isinstance(voice_idx, (list, tuple)) else [ps[voice_idx]]
            flat.append((b, off, dur, pv))
    for i, (b, off, dur, pv) in enumerate(flat):
        tie = tie_same and i + 1 < len(flat) and flat[i + 1][3] == pv
        body = pv[0] if len(pv) == 1 else "[" + ",".join(pv) + "]"
        tok = f"{body}/{dur}{'~' if tie else ''}{art}"
        out.setdefault(b, []).append(tok)
    return {b: " ".join(t) for b, t in out.items()}


def harmonize(tokens, bar, nbelow, min_gap=3):
    """Bloco: para cada nota da melodia gera `nbelow` vozes abaixo (notas do acorde ou
    terças/quintas diatônicas para notas de passagem). Retorna lista de strings (uma por voz)."""
    evs = parse_voice(tokens)
    scale = key_scale(bar)
    voices = [[] for _ in range(nbelow)]
    pos = 0
    for e in evs:
        flags = ""
        if e.tie: flags += "~"
        if e.slur_start: flags += "("
        if e.slur_stop: flags += ")"
        for a, f in (("accent", ">"), ("strong-accent", "^"), ("staccato", "."), ("tenuto", "-"), ("fermata", "!")):
            if a in e.arts: flags += f
        if not e.pitches:
            for v in voices:
                v.append(f"r/{e.dur}")
            pos += e.dur
            continue
        lead = e.pitches[0]
        lm = midi(lead)
        sym = chord_at(bar, pos)
        tones = spelled_tones(sym)
        rr = chord_pcs(sym)[1]
        if len(tones) > 3:
            tones = [t_ for t_ in tones if (t_[0] - rr) % 12 != 2] or tones
        pcs = [t[0] for t in tones]
        below = []
        if lm % 12 in pcs or e.dur >= 4:
            cur = lm
            for _ in range(nbelow):
                best = None
                for pc, st, al in tones:
                    if pc == lm % 12:
                        continue
                    if any(pc == midi(x) % 12 for x in below):
                        continue
                    for o in range(1, 8):
                        p = pitch_str(st, al, o)
                        m = midi(p)
                        if m <= cur - min_gap and (best is None or m > midi(best)):
                            best = p
                if best is None:  # repete com dobra
                    for pc, st, al in tones:
                        for o in range(1, 8):
                            p = pitch_str(st, al, o)
                            m = midi(p)
                            if m <= cur - min_gap and (best is None or m > midi(best)):
                                best = p
                below.append(best)
                cur = midi(best)
        else:
            s, a, o = parse_pitch(lead)
            alters = {x[0]: parse_pitch(x + "4")[1] for x in scale}
            for d in (2, 4, 5)[:nbelow]:
                j = STEPS.index(s) - d
                ls = STEPS[j % 7]
                below.append(pitch_str(ls, alters[ls], o + j // 7))
        for v, p in zip(voices, below):
            v.append(f"{p}/{e.dur}{flags}")
        pos += e.dur
    return [" ".join(v) for v in voices]


def guide_line(bars, start, lo, hi, prefer=(3, 7, 9, 6, 4), hold=True):
    """Linha de notas-guia (3a/7a) com condução por grau. Retorna {bar: tokens}."""
    prev = midi(start)
    flat = []
    for bar in bars:
        for off, dur, sym in chord_spans(bar):
            pcs, r, b, root, bass = chord_pcs(sym)
            tones = spelled_tones(sym)
            ivs = {(pc - r) % 12: (pc, st, al) for pc, st, al in tones}
            want = []
            for d in prefer:
                for iv in {3: (3, 4), 7: (10, 11), 9: (2,), 6: (9,), 4: (5,)}[d]:
                    if iv in ivs:
                        want.append(ivs[iv])
            if not want:
                want = tones
            best = None
            for rank, (pc, st, al) in enumerate(want):
                for o in range(1, 8):
                    p = pitch_str(st, al, o)
                    m = midi(p)
                    if lo <= m <= hi:
                        pen = abs(m - prev) + rank * 0.6
                        if best is None or pen < best[0]:
                            best = (pen, p)
            p = best[1]
            prev = midi(p)
            flat.append((bar, off, dur, p))
    out = {}
    for i, (bar, off, dur, p) in enumerate(flat):
        tie = hold and i + 1 < len(flat) and flat[i + 1][3] == p
        out.setdefault(bar, []).append(f"{p}/{dur}{'~' if tie else ''}")
    return {b: " ".join(t) for b, t in out.items()}


def bass_line(bars, pattern, lo, hi, start="Eb2"):
    """pattern: 'long' (por acorde), 'half' (semínima pontuada), 'pop' (long-short: 4+2)."""
    prev = midi(start)
    out = {}
    for bar in bars:
        toks = []
        for off, dur, sym in chord_spans(bar):
            p = note_of(bass_name(sym), prev, lo, hi)
            # evita saltos grandes: prefere a oitava mais próxima
            prev = midi(p)
            if pattern == "long":
                toks.append(f"{p}/{dur}")
            else:
                for h in range(dur // H):
                    if pattern == "half":
                        toks.append(f"{p}/{H}")
                    elif pattern == "pop":
                        toks.append(f"{p}/4 {p}/2")
        out[bar] = " ".join(toks)
    return out


def piano_arp(bars, start_rh=("Bb4", "G4", "Eb4")):
    """Piano 6/8: MD acordes em semínima pontuada; ME arpejo (baixo-5a-10a)."""
    rh = segs_to_tokens(pad_voices(bars, 3, start_rh, midi("C4"), midi("C5")), [0, 1, 2], tie_same=False)
    lh = {}
    prevb = midi("Eb2")
    for bar in bars:
        toks = []
        for off, dur, sym in chord_spans(bar):
            bn = note_of(bass_name(sym), prevb, midi("C2"), midi("Bb2"))
            prevb = midi(bn)
            f5 = nearest_tone(sym, midi(bn) + 7, midi(bn) + 3, midi(bn) + 12, exclude={midi(bn) % 12})
            t10 = nearest_tone(sym, midi(bn) + 15, midi(f5) + 2, midi(f5) + 12,
                               exclude={midi(bn) % 12, midi(f5) % 12})
            for h in range(dur // H):
                toks.append(f"{bn}/2 {f5}/2 {t10}/2")
        lh[bar] = " ".join(toks)
    return rh, lh


def piano_pop(bars, start_rh=("Bb4", "G4", "Eb4")):
    rhseg = pad_voices(bars, 3, start_rh, midi("D4"), midi("D5"))
    rh = {}
    for bar in bars:
        toks = []
        for off, dur, ps in rhseg[bar]:
            c = "[" + ",".join(ps) + "]"
            for h in range(dur // H):
                toks.append(f"{c}/4 {c}/2")
        rh[bar] = " ".join(toks)
    lh = {}
    prevb = midi("Eb2")
    for bar in bars:
        toks = []
        for off, dur, sym in chord_spans(bar):
            bn = note_of(bass_name(sym), prevb, midi("C2"), midi("Bb2"))
            prevb = midi(bn)
            toks.append(f"[{bn},{octave(bn, 1)}]/{dur}")
        lh[bar] = " ".join(toks)
    return rh, lh


def ostinato(bars):
    """Ostinato de colcheias (5-8-9 / 3-9-8) - motor do verso, estilo Camp."""
    out = {}
    for bar in bars:
        toks = []
        for off, dur, sym in chord_spans(bar):
            pcs, r, b, root, bass = chord_pcs(sym)
            rs, ra, _ = parse_pitch(root + "4")
            r8 = place(rs, ra, midi("C5"), midi("G4"), midi("F5"))
            f = nearest_tone(sym, midi(r8) - 5, midi(r8) - 9, midi(r8) - 1, exclude={r})
            sc_ = key_scale(bar)
            nn = [x for x in sc_ if x[0] == STEPS[(STEPS.index(rs) + 1) % 7]][0]
            ns, na, _ = parse_pitch(nn + "4")
            nine = place(ns, na, midi(r8) + 2, midi(r8) + 1, midi(r8) + 3)
            t3 = nearest_tone(sym, midi(r8) + 4, midi(nine) + 1, midi(r8) + 7, exclude={r})
            for h in range(dur // H):
                if (off // H + h) % 2 == 0:
                    toks.append(f"{f}/2( {r8}/2 {nine}/2")
                else:
                    toks.append(f"{t3}/2 {nine}/2 {r8}/2)")
        if toks[-1].endswith("/2") and " ".join(toks).count("(") > " ".join(toks).count(")"):
            toks[-1] = toks[-1][:-1] + "2)"
        out[bar] = " ".join(toks)
    return out


# ------------------------------------------------------------------ bateria (pop 6/8 reto)
def drums(kind, crash=False):
    """Retorna (mãos, pés). Groove pop 6/8 quadrado e constante:
    chimbal em colcheias, caixa (ou aro) no 4, bumbo no 1 e no 3 (+6 no refrão)."""
    first = "p:crash/2" if crash else "p:hh/2"
    if kind == "vamp":
        return (f"{first} p:hh/2 p:hh/2 p:hh/2 p:hh/2 p:hh/2", "p:kick/6 r/6")
    if kind == "verse":
        return (f"{first} p:hh/2 p:hh/2 p:hh+xstick/2 p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/6")
    if kind == "pre":
        return (f"{first} p:hh/2 p:hh/2 p:hh+snare/2 p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/6")
    if kind == "chorus":
        return (f"{first} p:hh/2 p:hh/2 p:hh+snare/2> p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/4 p:kick/2")
    if kind == "chorus_ride":
        f = "p:crash/2" if crash else "p:ride/2"
        return (f"{f} p:ride/2 p:ride/2 p:ride+snare/2> p:ride/2 p:ride/2", "p:kick/4 p:kick/2 r/4 p:kick/2")
    if kind == "fill":
        return (f"{first} p:hh/2 p:hh/2 p:snare/1 p:snare/1 p:tom1/1 p:tom1/1 p:tom2/1 p:ftom/1",
                "p:kick/4 p:kick/2 r/6")
    if kind == "fill_small":
        return (f"{first} p:hh/2 p:hh/2 p:hh+snare/2 p:snare/2 p:snare/2>", "p:kick/4 p:kick/2 r/6")
    if kind == "fill_big":
        return ("p:snare/1> p:snare/1 p:snare/1 p:snare/1 p:tom1/1 p:tom1/1 "
                "p:snare/1> p:snare/1 p:tom1/1 p:tom2/1 p:ftom/1 p:ftom/1",
                "p:kick/6 p:kick/6")
    if kind == "hits":  # transição: ataques com prato
        return ("p:crash+snare/4^ r/2 p:snare/1 p:snare/1 p:tom1/1 p:tom2/1 p:ftom/1 p:ftom/1",
                "p:kick/4 r/2 p:kick/6")
    if kind == "rest":
        return ("r/12",)
    raise KeyError(kind)


# ------------------------------------------------------------------ partitura
sc = Score("Uma Carta Viva", "GET Worship", "Arr. instrumental “Camp Inspired”", NBARS)
sc.keys = {1: -3, 60: -1}
sc.tempos = {1: (60, "Com expressão – pop 6/8")}
sc.marks = {1: ("", "Introdução"), 9: ("", "Vamp"), 11: ("A", "Estrofe"), 19: ("B", "Pré-refrão"),
            27: ("C", "Refrão"), 43: ("D", "Interlúdio"), 51: ("E", "Pré-refrão 2"),
            59: ("", "Transição"), 60: ("F", "Refrão 2 (Fá)")}
for b in (8, 10, 18, 26, 42, 50, 58):
    sc.barlines[b] = "light-light"
sc.barlines[59] = "light-light"
sc.barlines[NBARS] = "light-light"  # a música continua na Ponte

# transposições: escrito = real + intervalo
FL = sc.add(Instrument("Flauta 1 & 2", "Fl.", midi_program=74, sound_id="wind.flutes.flute"))
OB = sc.add(Instrument("Oboé", "Ob.", midi_program=69, sound_id="wind.reed.oboe"))
CL = sc.add(Instrument("Clarinete 1 & 2 (Si♭)", "Cl.", diatonic=1, chromatic=2, key_offset=2, midi_program=72, sound_id="wind.reed.clarinet"))
FG = sc.add(Instrument("Fagote / Clarone", "Fg.", clef="F", midi_program=71, sound_id="wind.reed.bassoon"))
AS = sc.add(Instrument("Sax Alto 1 & 2", "S.A.", diatonic=5, chromatic=9, key_offset=3, midi_program=66, sound_id="wind.reed.saxophone.alto"))
TS = sc.add(Instrument("Sax Tenor", "S.T.", diatonic=8, chromatic=14, key_offset=2, midi_program=67, sound_id="wind.reed.saxophone.tenor"))
BS = sc.add(Instrument("Sax Barítono", "S.Bar.", diatonic=12, chromatic=21, key_offset=3, midi_program=68, sound_id="wind.reed.saxophone.baritone"))
T1 = sc.add(Instrument("Trompete 1 (Si♭)", "Tpt. 1", diatonic=1, chromatic=2, key_offset=2, midi_program=57, sound_id="brass.trumpet"))
T23 = sc.add(Instrument("Trompete 2 & 3 (Si♭)", "Tpt. 2-3", diatonic=1, chromatic=2, key_offset=2, midi_program=57, sound_id="brass.trumpet"))
HN = sc.add(Instrument("Trompa 1 & 2 (Fá)", "Tpa.", diatonic=4, chromatic=7, key_offset=1, midi_program=61, sound_id="brass.french-horn"))
TB = sc.add(Instrument("Trombone 1 & 2", "Tbn. 1-2", clef="F", midi_program=58, sound_id="brass.trombone"))
TU = sc.add(Instrument("Trombone 3 / Tuba", "Tbn. 3/Tu.", clef="F", midi_program=59, sound_id="brass.trombone"))
# PC = rascunho da percussão auxiliar; no fim é dividido em 3 instrumentos de 1 linha
PC = Instrument("Percussão", "Perc.", clef="perc", percussion=True, sound="aux")
SH = sc.add(Instrument("Shaker", "Shk.", clef="perc", percussion=True, sound="aux", lines=1,
                       sound_id="rattle.shaker", gm_key=70))
TA = sc.add(Instrument("Pandeirola", "Pand.", clef="perc", percussion=True, sound="aux", lines=1,
                       sound_id="drum.tambourine", gm_key=54))
SC = sc.add(Instrument("Prato suspenso", "Pr. susp.", clef="perc", percussion=True, sound="aux", lines=1,
                       sound_id="metal.cymbal.suspended", gm_key=49))
DR = sc.add(Instrument("Bateria", "Bat.", clef="perc", percussion=True, sound="drums"))
GT = sc.add(Instrument("Rhythm (Violão/Guitarra)", "Rhy.", midi_program=26, diatonic=0, sound_id="pluck.guitar.acoustic"))
GT.sound = "slash"
PN = sc.add(Instrument("Piano", "Pno.", staves=2, clefs=["G", "F"], midi_program=1, sound_id="keyboard.piano"))
BX = sc.add(Instrument("Baixo", "Bx.", clef="F", diatonic=7, chromatic=12, midi_program=34, sound_id="pluck.bass.electric"))
V1 = sc.add(Instrument("Violino 1", "Vl. 1", midi_program=49, sound_id="strings.violin"))
V2 = sc.add(Instrument("Violino 2", "Vl. 2", midi_program=49, sound_id="strings.violin"))
VA = sc.add(Instrument("Viola", "Vla.", clef="C", midi_program=49, sound_id="strings.viola"))
VC = sc.add(Instrument("Violoncelo", "Vc.", clef="F", midi_program=49, sound_id="strings.cello"))
CB = sc.add(Instrument("Contrabaixo", "Cb.", clef="F", diatonic=7, chromatic=12, midi_program=44, sound_id="strings.contrabass"))

sc.group(0, 3, "bracket")
sc.group(4, 6, "bracket")
sc.group(7, 11, "bracket")
sc.group(12, 15, "bracket")
sc.group(16, 18, "bracket")
sc.group(19, 23, "bracket")

ALL = [FL, OB, CL, FG, AS, TS, BS, T1, T23, HN, TB, TU, PC, DR, GT, PN, BX, V1, V2, VA, VC, CB]


def dyn(parts, bar, d, off=0):
    for p in parts:
        p.dir(bar, "dyn", d, off)
        if p is PN:
            pass


def cresc(parts, bar, off=0, bar_end=None, off_end=BAR - 1, kind="cresc"):
    for p in parts:
        p.dir(bar, kind, 1, off)
        p.dir(bar_end or bar, "wedge-stop", 1, off_end)


def text(p, bar, t, off=0, bold=False):
    p.dir(bar, "textb" if bold else "text", t, off)


def put_map(inst, m, staff=1):
    for b, toks in m.items():
        inst.put(b, toks, staff=staff)


def chord_tok(voices):
    """Junta vozes de mesmo ritmo num único token de acorde por evento."""
    evl = [parse_voice(v) for v in voices]
    out = []
    for i in range(len(evl[0])):
        es = [ev[i] for ev in evl]
        e0 = es[0]
        flags = ("~" if e0.tie else "") + ("(" if e0.slur_start else "") + (")" if e0.slur_stop else "")
        for a, f in (("accent", ">"), ("strong-accent", "^"), ("staccato", "."), ("tenuto", "-"), ("fermata", "!")):
            if a in e0.arts: flags += f
        if not e0.pitches:
            out.append(f"r/{e0.dur}")
        else:
            ps = []
            for e in es:
                for p in e.pitches:
                    if p not in ps:
                        ps.append(p)
            out.append(("[" + ",".join(ps) + "]" if len(ps) > 1 else ps[0]) + f"/{e0.dur}{flags}")
    return " ".join(out)


# cifras na parte de Rhythm e no Piano; slashes na Rhythm
for b in range(1, NBARS + 1):
    for off, s in CH[b]:
        GT.harm(b, s, off)
    GT.put(b, "B4/6 B4/6")

# ================================================================== INTRO (1-8)  f
INTRO_LEAD = {
    1: "Bb4/4( G4/2 Bb4/4 Eb5/2)",
    2: "Eb5/4( C5/2 Ab4/4 C5/2)",
    3: "Bb4/4( G4/2 Bb4/4 Eb5/2)",
    4: "Eb5/6~ Eb5/2 C5/2( Bb4/2)",
    5: "C5/4( Eb5/2 D5/4 Bb4/2)",
    6: "D5/4( Bb4/2 Eb5/4 G4/2)",
    7: "C5/4( Ab4/2 Bb4/4 C5/2)",
    8: "Bb4/12",
}
for b, t in INTRO_LEAD.items():
    v2, v3 = harmonize(t, b, 2)
    if b == 8:
        v2, v3 = "Ab4/6 G4/6", "Eb4/6 D4/6"  # sus4 -> 3
    T1.put(b, t)
    T23.put(b, chord_tok([v2, v3]))
    AS.put(b, chord_tok([t, v2]))
    TS.put(b, v3)
    CL.put(b, chord_tok([t, v2]))
    OB.put(b, t)
    FL.put(b, chord_tok([oct_tokens(t, 1), oct_tokens(v2, 1)]))
    TB.put(b, chord_tok([oct_tokens(t, -1), oct_tokens(v3, -1)]) if b < 8 else
           "[Eb3,Ab3]/6 [D3,Ab3]/6")
# Trompas: notas-guia sustentadas (contracanto médio)
put_map(HN, guide_line(range(1, 9), "G4", midi("C4"), midi("Eb5")))
# graves
bass_intro = bass_line(range(1, 9), "pop", midi("Bb1"), midi("Bb2"), "Eb2")
put_map(BX, bass_intro)
put_map(TU, bass_line(range(1, 9), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
put_map(BS, oct_tokens_map := {b: oct_tokens(v, 1) for b, v in bass_line(range(1, 9), "long", midi("Bb1"), midi("Bb2"), "Eb2").items()})
put_map(FG, oct_tokens_map)
put_map(VC, oct_tokens_map)
put_map(CB, bass_line(range(1, 9), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
# cordas: pad agudo
padI = pad_voices(range(1, 9), 3, ("G5", "Eb5", "Bb4"), midi("Bb4"), midi("Ab5"))
put_map(V1, segs_to_tokens(padI, 0))
put_map(V2, segs_to_tokens(padI, 1))
put_map(VA, segs_to_tokens(pad_voices(range(1, 9), 1, ("Bb3",), midi("G3"), midi("Eb4")), 0))
rh, lh = piano_pop(range(1, 9))
put_map(PN, rh, 1); put_map(PN, lh, 2)
for b in range(1, 9):
    DR.put(b, *drums("fill" if b == 8 else "chorus", crash=(b in (1, 5))))
text(DR, 1, "Pop 6/8 reto – constante", bold=True)
text(DR, 8, "Fill", off=6)
PC.put(1, "r/12"); PC.put(4, "r/6 p:aux/6*"); PC.put(5, "p:aux/6 r/6")
text(PC, 4, "Sus. Cym.", off=6)
cresc([PC], 4, off=6, off_end=11)
dyn([x for x in ALL if x not in (PC,)], 1, "f")
cresc([x for x in ALL if x not in (PC, GT)], 7, off=6, bar_end=8, off_end=11, kind="dim")

# ================================================================== VAMP (9-10)  subito mp
osti = ostinato(range(9, 11))
put_map(CL, osti)
rh, lh = piano_arp(range(9, 19))
for b in range(9, 19):
    PN.put(b, rh[b], staff=1)
    PN.put(b, lh[b], staff=2)
put_map(BX, bass_line(range(9, 19), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
put_map(CB, bass_line(range(9, 19), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
put_map(VC, {b: oct_tokens(v, 1) for b, v in bass_line(range(9, 19), "long", midi("Bb1"), midi("Bb2"), "Eb2").items()})
DR.put(9, *drums("vamp")); DR.put(10, *drums("vamp"))
text(DR, 9, "Chimbal + bumbo (leve)")
PC.put(9, "p:auxx/2 p:auxx/2 p:auxx/2 p:auxx/2> p:auxx/2 p:auxx/2")
PC.put(10, "p:auxx/2 p:auxx/2 p:auxx/2 p:auxx/2> p:auxx/2 p:auxx/2")
text(PC, 9, "Shaker")
for p in (CL, PN, BX, CB, VC, DR, PC, GT):
    p.dir(9, "text", "subito", 0)
dyn([CL, PN, BX, CB, VC, DR, PC, GT], 9, "mp")

# ================================================================== ESTROFE (11-18)
AS.put(10, mel(10)); text(AS, 10, "Solo (S.A. 1)", off=6)
for b in range(11, 14):
    AS.put(b, mel(b))
TS.put(14, mel(14)); text(TS, 14, "Solo", off=6)
for b in range(15, 18):
    TS.put(b, mel(b))
dyn([AS], 10, "mp", 6); dyn([TS], 14, "mp", 6)
# ecos de madeira nas respirações da melodia
FL.put(14, "Bb5/2( Ab5/2 G5/2) r/6"); CL.put(14, "G5/2( F5/2 Eb5/2) r/6")
FL.put(18, "Eb6/2( D6/2 Bb5/2) r/6"); CL.put(18, "G5/2( F5/2 D5/2) r/6")
dyn([FL, CL], 14, "mp")
# pad de cordas
padA = pad_voices(range(11, 27), 3, ("G4", "Eb4", "Bb3"), midi("G3"), midi("Bb4"))
put_map(V1, {b: v for b, v in segs_to_tokens(padA, 0).items()})
put_map(V2, {b: v for b, v in segs_to_tokens(padA, 1).items()})
put_map(VA, {b: v for b, v in segs_to_tokens(padA, 2).items()})
dyn([V1, V2, VA], 11, "mp")
for b in range(11, 19):
    DR.put(b, *drums("fill_small" if b == 18 else "verse"))
    PC.put(b, "p:auxx/2 p:auxx/2 p:auxx/2 p:auxx/2> p:auxx/2 p:auxx/2")
text(DR, 11, "Aro (cross-stick) no 4")
text(GT, 11, "Arpejado")

# ================================================================== PRÉ-REFRÃO 1 (19-26)
TB.put(18, mel(18)); text(TB, 18, "Solo (Tbn. 1)", off=6); dyn([TB], 18, "mp", 6)
for b in range(19, 27):
    TB.put(b, mel(b))
put_map(HN, segs_to_tokens(pad_voices(range(19, 27), 2, ("Eb4", "Bb3"), midi("G3"), midi("Eb4")), [0, 1]))
dyn([HN], 19, "mp")
# Abm6: trombone 3 e fagote reforçam a cor
put_map(TU, bass_line(range(19, 27), "long", midi("Bb1"), midi("Bb2"), "F2"))
put_map(FG, {b: oct_tokens(v, 1) for b, v in bass_line(range(19, 27), "long", midi("Bb1"), midi("Bb2"), "F2").items()})
dyn([TU, FG], 19, "mp")
rh, lh = piano_arp(range(19, 27))
put_map(PN, rh, 1); put_map(PN, lh, 2)
put_map(BX, bass_line(range(19, 27), "half", midi("Bb1"), midi("Bb2"), "F2"))
put_map(CB, bass_line(range(19, 27), "long", midi("Bb1"), midi("Bb2"), "F2"))
put_map(VC, {b: oct_tokens(v, 1) for b, v in bass_line(range(19, 27), "long", midi("Bb1"), midi("Bb2"), "F2").items()})
for b in range(19, 27):
    DR.put(b, *drums("fill" if b == 26 else ("pre" if b >= 23 else "verse")))
    if b < 25:
        PC.put(b, "p:auxx/2 p:auxx/2 p:auxx/2 p:auxx/2> p:auxx/2 p:auxx/2")
text(DR, 23, "Caixa no 4")
text(DR, 26, "Fill", off=6)
PC.put(25, "r/12"); PC.put(26, "p:aux/12*"); text(PC, 26, "Sus. Cym.")
cresc([PC], 26, off=0, off_end=11)
osti2 = ostinato(range(23, 27))
put_map(CL, osti2); dyn([CL], 23, "mp")
cresc([V1, V2, VA, HN, CL, PN, DR, BX], 25, bar_end=26)

# ================================================================== REFRÃO 1 (27-42)  mf
# c. 27-34: Tpt 1 + S.A. 1 em uníssono
for b in range(27, 35):
    T1.put(b, mel(b))
    AS.put(b, mel(b))
text(T1, 27, "Solo (aberto)"); text(AS, 27, "S.A. 1 com Tpt. 1")
# respostas dos trombones nas notas longas da melodia
TB.put(33, "r/6 [Eb4,C4]/2( [D4,Bb3]/2 [C4,Ab3]/2)")
TB.put(34, "r/6 [F4,D4]/2( [Eb4,C4]/2 [D4,Bb3]/2)")
# c. 35-42: soli de saxes (S.A.1 lead, S.A.2, S.T., Bari 8vb)
for b in range(35, 43):
    v2, v3 = harmonize(mel(b), b, 2)
    AS.put(b, chord_tok([mel(b), v2]))
    TS.put(b, v3)
    BS.put(b, oct_tokens(mel(b), -1))
text(AS, 35, "Soli de saxes", bold=True)
# trompetes: fills nas respirações do soli
T1.put(41, "r/6 Bb4/2( C5/2 D5/2)"); T23.put(41, "r/6 [G4,Eb4]/2( [Ab4,Eb4]/2 [Bb4,F4]/2)")
T1.put(42, "Eb5/4 r/2 r/6"); T23.put(42, "[Bb4,G4]/4 r/2 r/6")
dyn([T1, T23], 41, "mf", 6)
# contracanto: trompas + sax tenor (27-34) com notas-guia
gl = guide_line(range(27, 43), "G4", midi("C4"), midi("D5"))
put_map(HN, gl)
for b in range(27, 35):
    TS.put(b, gl[b])
# trombones/tuba: pad grave no soli
padTb = pad_voices(range(35, 43), 2, ("Bb3", "G3"), midi("Eb3"), midi("C4"))
put_map(TB, segs_to_tokens(padTb, [0, 1]))
dyn([TB], 35, "mp")
# graves e base
bl = bass_line(range(27, 43), "pop", midi("Bb1"), midi("Bb2"), "Eb2")
put_map(BX, bl)
put_map(CB, bass_line(range(27, 43), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
lng = {b: oct_tokens(v, 1) for b, v in bass_line(range(27, 43), "long", midi("Bb1"), midi("Bb2"), "Eb2").items()}
put_map(VC, lng); put_map(FG, lng)
put_map(TU, bass_line(range(27, 43), "long", midi("Bb1"), midi("Bb2"), "Eb2"))
for b in range(27, 35):
    BS.put(b, oct_tokens(bl[b], 1))
rh, lh = piano_pop(range(27, 43))
put_map(PN, rh, 1); put_map(PN, lh, 2)
padC = pad_voices(range(27, 43), 3, ("Bb4", "G4", "Eb4"), midi("Bb3"), midi("C5"))
put_map(V1, segs_to_tokens(padC, 0)); put_map(V2, segs_to_tokens(padC, 1)); put_map(VA, segs_to_tokens(padC, 2))
for b in range(27, 43):
    DR.put(b, *drums("fill" if b in (34, 42) else "chorus", crash=(b in (27, 31, 35, 39))))
    PC.put(b, "p:aux/2 p:aux/2 p:aux/2 p:aux/2> p:aux/2 p:aux/2")
text(PC, 27, "Pandeirola")
text(GT, 27, "Colcheias (strum)")
text(DR, 34, "Fill", off=6); text(DR, 42, "Fill", off=6)
dyn([T1, AS, TS, HN, BS, BX, CB, VC, FG, TU, PN, V1, V2, VA, DR, PC, GT], 27, "mf")

# ================================================================== INTERLÚDIO (43-50)
MOT = {43: "Bb4/4( G4/2 Bb4/4 Eb5/2)", 44: "D5/3( Eb5/3 C5/6)", 45: "Eb5/4( C5/2 Ab4/4 C5/2)", 46: "Bb4/12"}
for b, t in MOT.items():
    v2, v3 = harmonize(t, b, 2)
    AS.put(b, chord_tok([t, v2]))
    TS.put(b, v3)
    CL.put(b, chord_tok([t, v2]))
text(AS, 43, "Saxes – motivo da intro"); dyn([AS, TS, CL], 43, "mf")
# "Oh" -> trombones + trompas soli
for b in range(47, 51):
    t = mel(b)
    v2, v3 = harmonize(t, b, 2, min_gap=3)
    HN.put(b, chord_tok([t, v2]) if b < 50 else chord_tok(["C5/6 r/6", "Ab4/6 r/6"]))
    tb_lead = oct_tokens(t, -1)
    w2, _ = harmonize(tb_lead, b, 1, min_gap=3) + [None]
    if b < 50:
        TB.put(b, chord_tok([tb_lead, w2]))
    else:
        TB.put(b, "C4/6 G3/2( Ab3/2 Bb3/2)")  # Tbn 1 já emenda na melodia do Pré 2
text(HN, 47, "Soli (Tpa. + Tbn.)"); dyn([HN, TB], 47, "mf")
padD = pad_voices(range(43, 51), 3, ("Bb4", "G4", "Eb4"), midi("Bb3"), midi("C5"))
put_map(V1, segs_to_tokens(padD, 0)); put_map(V2, segs_to_tokens(padD, 1)); put_map(VA, segs_to_tokens(padD, 2))
V1.put(50, "Eb5/6 Bb4/1( C5/1 D5/1 Eb5/1 F5/1 G5/1)"); V2.put(50, "G4/6 Bb4/1( C5/1 D5/1 Eb5/1 F5/1 G5/1)")
rh, lh = piano_arp(range(43, 51))
put_map(PN, rh, 1); put_map(PN, lh, 2)
bl = bass_line(range(43, 51), "half", midi("Bb1"), midi("Bb2"), "Eb2")
put_map(BX, bl)
lng = bass_line(range(43, 51), "long", midi("Bb1"), midi("Bb2"), "Eb2")
put_map(CB, lng); put_map(VC, {b: oct_tokens(v, 1) for b, v in lng.items()})
put_map(TU, {b: v for b, v in lng.items() if b >= 47})
for b in range(43, 51):
    DR.put(b, *drums("fill_small" if b == 50 else "pre"))
    PC.put(b, "p:auxx/2 p:auxx/2 p:auxx/2 p:auxx/2> p:auxx/2 p:auxx/2")
text(PC, 43, "Shaker")
cresc([V1, V2, VA, PN, BX, DR], 46, kind="dim")
dyn([V1, V2, VA, PN, BX, CB, VC, DR, PC], 47, "mp")

# ================================================================== PRÉ-REFRÃO 2 (51-58)  grad. cresc.
TS.put(50, "r/6 G4/2( Ab4/2 Bb4/2)")
for b in range(51, 59):
    TS.put(b, mel(b))
    TB.put(b, oct_tokens(mel(b), -1))
text(TS, 50, "S.T. + Tbn. 1 (8vb)", off=6); dyn([TS], 50, "mf", 6)
put_map(CL, ostinato(range(51, 59))); dyn([CL], 51, "mp")
put_map(HN, segs_to_tokens(pad_voices(range(51, 59), 2, ("Eb4", "C4"), midi("Bb3"), midi("F4")), [0, 1]))
dyn([HN], 51, "mp")
padT = pad_voices(range(55, 59), 2, ("Eb5", "C5"), midi("Ab4"), midi("Eb5"))
put_map(T23, segs_to_tokens(padT, [0, 1])); dyn([T23], 55, "mp")
put_map(AS, segs_to_tokens(pad_voices(range(53, 59), 2, ("G4", "Eb4"), midi("C4"), midi("Ab4")), [0, 1]))
dyn([AS], 53, "mp")
padE = pad_voices(range(51, 59), 3, ("Ab4", "F4", "C4"), midi("C4"), midi("Eb5"))
put_map(V1, segs_to_tokens(padE, 0)); put_map(V2, segs_to_tokens(padE, 1)); put_map(VA, segs_to_tokens(padE, 2))
rh, lh = piano_pop(range(51, 59))
put_map(PN, rh, 1); put_map(PN, lh, 2)
put_map(BX, bass_line(range(51, 59), "pop", midi("Bb1"), midi("Bb2"), "F2"))
lng = bass_line(range(51, 59), "long", midi("Bb1"), midi("Bb2"), "F2")
put_map(CB, lng); put_map(VC, {b: oct_tokens(v, 1) for b, v in lng.items()}); put_map(TU, lng)
put_map(BS, {b: oct_tokens(v, 1) for b, v in lng.items()}); put_map(FG, {b: oct_tokens(v, 1) for b, v in lng.items()})
for b in range(51, 58):
    DR.put(b, *drums("chorus" if b >= 55 else "pre", crash=(b == 55)))
    PC.put(b, "p:aux/2 p:aux/2 p:aux/2 p:aux/2> p:aux/2 p:aux/2")
text(PC, 51, "Pandeirola")
text(V1, 51, "grad. cresc.", bold=True)
dyn([V1, V2, VA, PN, BX, CB, VC, TU, BS, FG, DR, PC], 51, "mp")
cresc([V1, V2, VA, HN, CL, PN, BX, CB, VC, TU, BS, FG, AS, T23, DR], 55, bar_end=58, off_end=5)
# c. 58: tutti sobe para a transição
T1.put(58, "r/6 Ab4/2( Bb4/2 C5/2)")
T23.put(58, "[C5,Ab4]/6 [F4,C4]/2( [G4,Eb4]/2 [Ab4,F4]/2)")
AS.put(58, "[Eb4,C4]/6 Ab4/2( Bb4/2 C5/2)")
DR.put(58, *drums("fill"))
PC.put(58, "r/6 p:aux/6*"); text(PC, 58, "Sus. Cym.", off=6)
dyn([T1, DR], 58, "f", 6)
text(DR, 58, "Fill", off=6)

# ================================================================== TRANSIÇÃO (59)  C7sus4 -> C7
TR_LEAD = "F5/4^ r/2 E5/2( F5/2 G5/2)"
T1.put(59, "F5/4^ r/2 E5/2( F5/2 G5/2)")
T23.put(59, "[C5,Bb4]/4^ r/2 [Bb4,G4]/2( [C5,A4]/2 [E5,Bb4]/2)")
TB.put(59, "[F4,C4]/4^ r/2 [C4,Bb3]/2( [D4,A3]/2 [E4,Bb3]/2)")
HN.put(59, "[F4,C4]/4^ r/2 [G4,E4]/6")
AS.put(59, "[C5,F4]/4^ r/2 [Bb4,E4]/2( [C5,F4]/2 [E5,G4]/2)")
TS.put(59, "Bb4/4^ r/2 G4/2( A4/2 Bb4/2)")
BS.put(59, "C3/4^ r/2 C3/6")
FG.put(59, "C3/4^ r/2 C3/6"); TU.put(59, "[C2,C3]/4^ r/2 [C2,C3]/6")
CL.put(59, "[F5,C5]/4^ r/2 [E5,Bb4]/2( [F5,C5]/2 [G5,E5]/2)")
OB.put(59, "F5/4^ r/2 E5/2( F5/2 G5/2)")
FL.put(59, "[F6,C6]/4^ r/2 C6/1( D6/1 E6/1 F6/1 G6/1 A6/1)")
V1.put(59, "C5/1( D5/1 E5/1 F5/1 G5/1 A5/1 Bb5/1 C6/1 D6/1 E6/1 F6/1 G6/1)")
V2.put(59, "C4/1( D4/1 E4/1 F4/1 G4/1 A4/1 Bb4/1 C5/1 D5/1 E5/1 F5/1 G5/1)")
VA.put(59, "[F4,C4]/4^ r/2 [E4,Bb3]/6")
VC.put(59, "C3/4^ r/2 C3/6"); CB.put(59, "C2/4^ r/2 C2/6")
BX.put(59, "C2/4^ r/2 C2/2 D2/2 E2/2")
PN.put(59, "[Bb4,C5,F5]/4^ r/2 [Bb4,E5,G5]/6", staff=1); PN.put(59, "[C2,C3]/4^ r/2 [C2,C3]/6", staff=2)
DR.put(59, *drums("hits"))
PC.put(59, "p:aux/6* p:aux/6*"); text(PC, 59, "Sus. Cym. (swell)")
cresc([PC], 59, off=0, off_end=11)
dyn([FL, OB, CL, FG, AS, TS, BS, T1, T23, HN, TB, TU, PN, BX, V1, V2, VA, VC, CB, DR], 59, "f")
cresc([FL, OB, CL, AS, TS, T1, T23, TB, V1, V2, DR], 59, off=6, off_end=11)

# ================================================================== REFRÃO 2 (60-75) Fá  ff
for b in range(60, 76):
    t = mel_f(b)
    v2, v3 = harmonize(t, b, 2)
    T1.put(b, t)
    T23.put(b, chord_tok([v2, v3]))
    TB.put(b, chord_tok([oct_tokens(t, -1), oct_tokens(v3, -1)]))
    TS.put(b, oct_tokens(t, -1))
    OB.put(b, t)
    CL.put(b, chord_tok([t, v2]))
    FL.put(b, chord_tok([oct_tokens(t, 1), oct_tokens(v2, 1)]))
    V1.put(b, oct_tokens(t, 1))
text(T1, 60, "Lead – bloco de trompetes", bold=True)
text(TB, 60, "Tbn. 1 = lead 8vb")
# contracanto: trompas + saxes altos (2 vozes em condução de vozes, região média)
padHn = pad_voices(range(60, 76), 2, ("A4", "F4"), midi("C4"), midi("Bb4"))
put_map(HN, segs_to_tokens(padHn, [0, 1]))
put_map(AS, segs_to_tokens(padHn, [0, 1]))
text(HN, 60, "Contracanto (Tpa. + S.A.)")
padF = pad_voices(range(60, 76), 2, ("F5", "C5"), midi("F4"), midi("F5"))
put_map(V2, segs_to_tokens(padF, 0)); put_map(VA, segs_to_tokens(padF, 1))
bl = bass_line(range(60, 76), "pop", midi("C2"), midi("C3"), "F2")
put_map(BX, bl)
put_map(BS, {b: oct_tokens(v, 1) for b, v in bl.items()})
lng = bass_line(range(60, 76), "long", midi("C2"), midi("C3"), "F2")
put_map(CB, lng); put_map(VC, {b: oct_tokens(v, 1) for b, v in lng.items()})
put_map(FG, {b: oct_tokens(v, 1) for b, v in lng.items()})
put_map(TU, {b: chord_tok([v, oct_tokens(v, 1)]) for b, v in lng.items()})
rh, lh = piano_pop(range(60, 76), ("C5", "A4", "F4"))
put_map(PN, rh, 1); put_map(PN, lh, 2)
for b in range(60, 76):
    DR.put(b, *drums("fill" if b in (67, 75) else "chorus_ride", crash=(b in (60, 64, 68, 72))))
    PC.put(b, "p:aux/2 p:aux/2 p:aux/2 p:aux/2> p:aux/2 p:aux/2")
text(DR, 60, "Condução no prato (ride) – mesmo groove")
text(PC, 60, "Pandeirola")
text(DR, 67, "Fill", off=6); text(DR, 75, "Fill → Ponte", off=6)
dyn([FL, OB, CL, FG, AS, TS, BS, T1, T23, HN, TB, TU, PN, BX, V1, V2, VA, VC, CB, DR, PC, GT], 60, "ff")
text(T1, 75, "→ PONTE (a definir)", off=6, bold=True)


# ------------------------------------------------------------------ percussão auxiliar -> 3 instrumentos
# Cada som vira um instrumento de 1 linha (o NotePerformer/Sibelius toca o som certo).
def _target(bar, toks):
    if "*" in toks or bar in (5,):
        return SC
    if "auxx" in toks:
        return SH
    if "aux" in toks:
        return TA
    return None


for b, md in sorted(PC.measures.items()):
    voices = md["staff"].get(1)
    raw = " ".join(f"{'p:aux' if e.drum else 'r'}{'x' if e.drum and 'auxx' in e.drum else ''}/{e.dur}"
                   f"{'*' if 'tremolo' in e.arts else ''}{'>' if 'accent' in e.arts else ''}"
                   for e in voices[0]) if voices else ""
    tgt = _target(b, raw)
    if tgt is None:
        continue
    tgt.put(b, raw.replace("p:auxx", "p:line").replace("p:aux", "p:line"))
    for d in md["dirs"]:
        if d[1] in ("dyn", "cresc", "dim", "wedge-stop"):
            tgt.m(b)["dirs"].append(d)
# dinâmica de entrada de cada instrumento
for inst in (SH, TA, SC):
    first = min(inst.measures) if inst.measures else None
    if first and not any(d[1] == "dyn" for d in inst.m(first)["dirs"]):
        inst.dir(first, "dyn", "mf" if inst is SC else "mp")
SC.dir(4, "text", "rulo (baqueta macia)", 6)

# ------------------------------------------------------------------ verificação de tessitura (real)
RANGES = {  # (mín, máx) em altura real
    FL: ("C4", "C7"), OB: ("Bb3", "F6"), CL: ("D3", "Bb5"), FG: ("Bb1", "Eb4"),
    AS: ("Db3", "Ab5"), TS: ("Ab2", "Eb5"), BS: ("Db2", "Ab4"), T1: ("E3", "G5"),
    T23: ("E3", "F5"), HN: ("B2", "F5"), TB: ("E2", "Bb4"), TU: ("D1", "Bb3"),
    PN: ("A0", "C8"), BX: ("E1", "G3"), V1: ("G3", "A6"), V2: ("G3", "E6"), VA: ("C3", "E5"),
    VC: ("C2", "A4"), CB: ("E1", "G3"),
}
problems = []
for inst, (lo, hi) in RANGES.items():
    for b, md in inst.measures.items():
        for st, voices in md["staff"].items():
            for v in voices:
                for e in v:
                    for p in e.pitches:
                        if not (midi(lo) <= midi(p) <= midi(hi)):
                            problems.append(f"{inst.name} c.{b}: {p} fora de {lo}-{hi}")
if problems:
    print("AVISOS DE TESSITURA:")
    print("\n".join(problems))

out = os.path.join(HERE, "uma-carta-viva.musicxml")
sc.write(out)
print("ok ->", out)

# ------------------------------------------------------------------ arquivo de teste só com a percussão
# Serve para testar rápido no Sibelius + NotePerformer se a bateria está tocando.
teste = Score("Uma Carta Viva – teste de bateria", "GET Worship", "Arr. instrumental “Camp Inspired”", NBARS)
teste.keys, teste.tempos, teste.marks, teste.barlines = sc.keys, sc.tempos, sc.marks, sc.barlines
for inst in (SH, TA, SC, DR):
    teste.add(inst)
teste.group(0, 3, "bracket")
out2 = os.path.join(HERE, "teste-bateria.musicxml")
teste.write(out2)
print("ok ->", out2)
