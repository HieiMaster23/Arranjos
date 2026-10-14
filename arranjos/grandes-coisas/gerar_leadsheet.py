"""Grandes Coisas (Ministério Atitude) - Etapa 1: lead sheet da versão coro + banda + metais.

Gera `grandes-coisas-leadsheet.musicxml` (MusicXML 3.1): melodia do coro (altura das vozes
femininas; homens cantam 8vb), cifra, letra e a forma nova (ver estrutura.md).

A melodia foi limpa a partir do guia do Moises (voz masculina, em Sol) e é escrita aqui na
altura do guia; o gerador transpõe para Mib (+6ªm) e, a partir do vamp, para Fá (+7ªm).
Posições em semicolcheias dentro do compasso (0-15); durações em semicolcheias.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ferramentas"))
from mxl import Score, Instrument, transpose  # noqa: E402

BAR = 16
OK_DUR = (16, 12, 8, 6, 4, 3, 2, 1)

# ------------------------------------------------------------------ forma
# (marca, título, nº de compassos, tom: "Eb" | "F")
FORM = [
    ("A", "Intro", 8, "Eb"),
    ("B", "Parte 1", 16, "Eb"),
    ("C", "Pré-refrão", 11, "Eb"),
    ("D", "Refrão", 12, "Eb"),
    ("E", "Interlúdio", 8, "Eb"),
    ("F", "Parte 2", 16, "Eb"),
    ("G", "Pré-refrão 2", 11, "Eb"),
    ("H", "Refrão 2", 25, "Eb"),
    ("I", "Vamp", 16, "Eb"),
    ("", "Lançamento", 2, "Eb"),
    ("J", "Vamp (Fá)", 8, "F"),
    ("K", "Todos dirão", 9, "F"),
    ("L", "Refrão final", 12, "F"),
    ("M", "Final", 10, "F"),
]
START = {}
n = 1
for mark, title, length, key in FORM:
    START[title] = n
    n += length
NBARS = n - 1

# ------------------------------------------------------------------ harmonia
INTRO = ["Eb", "Eb", "Ab", "Ab", "Bb/D", "Bb/D", "Ab", "Ab"]
VERSO = ["Eb", "Eb", "Bb/D", "Bb/D", "Cm", "Cm", "Ab", "Ab"] * 2
PRE = ["C", "G/B", "Bb", "F/A", "C", "G/B", "Bb", "F/A", "Ab", "Bb", "Bb"]
REFRAO = ["Eb", "Eb", "Ab", "Bb", "Cm7", "Cm7", "Ab", "Bb", "Cm7", "Bb", "Ab", "Bb"]
REFRAO_F = ["F", "F", "Bb", "C", "Dm7", "Dm7", "Bb", "C", "Dm7", "C", "Bb", "C"]
CHORDS = {
    "Intro": INTRO,
    "Parte 1": VERSO,
    "Pré-refrão": PRE,
    "Refrão": REFRAO,
    "Interlúdio": INTRO,
    "Parte 2": VERSO,
    "Pré-refrão 2": PRE,
    "Refrão 2": REFRAO + ["Eb"] + REFRAO,
    "Vamp": ["Eb", "Eb"] + ["Ab", "Bb"] * 7,
    "Lançamento": ["C7sus4", "C7"],
    "Vamp (Fá)": ["Bb", "C"] * 4,
    "Todos dirão": ["Dm7", "C", "Bb", "C"] * 2 + ["F"],
    "Refrão final": REFRAO_F,
    "Final": ["F", "Bb", "C", "F", "Bb", "C", "Dm7", "Bb", "Bbm6", "F(add9)"],
}

# ------------------------------------------------------------------ melodia (altura do guia, em Sol)
# evento: (compasso absoluto, posição, duração, nota do guia, sílaba, flags)
MEL = []


def ev(bar, pos, dur, pitch, syl="_", flags=""):
    MEL.append((bar, pos, dur, pitch, syl, flags))


def verso(b):
    """Parte 1/2: 8 versos de 2 compassos."""
    def frase_a(b0, sy):
        for (bb, p, d, pt), s in zip([(0, 2, 4, "G3"), (0, 6, 4, "D4"), (0, 10, 4, "B3"), (0, 14, 4, "A3"),
                                      (1, 2, 2, "A3"), (1, 4, 2, "G3"), (1, 6, 8, "B3")], sy.split()):
            ev(b0 + bb, p, d, pt, s)

    def frase_b(b0, sy, fim):
        notas = [(0, 0, 2, "E3"), (0, 2, 2, "E3"), (0, 4, 2, "E3"), (0, 6, 4, "B3"),
                 (0, 10, 2, "E3"), (0, 12, 2, "E3"), (0, 14, 4, "E3"), (1, 2, 10, "B3")]
        if fim == "dou":
            notas = notas[:4] + [(0, 10, 2, "B3"), (0, 12, 2, "E3"), (0, 14, 4, "E3"), (1, 2, 12, "D4")]
        if fim == "nou":
            notas = [(0, 0, 2, "E3"), (0, 2, 4, "E3"), (0, 6, 4, "B3"), (0, 10, 2, "B3"),
                     (0, 12, 2, "E3"), (0, 14, 2, "E3"), (1, 0, 2, "E3"), (1, 2, 12, "D4")]
        for (bb, p, d, pt), s in zip(notas, sy.split()):
            ev(b0 + bb, p, d, pt, s)

    frase_a(b, "Nas- ceu em meu co- ra- ção")
    frase_a(b + 2, "Um can- to de gra- ti- dão")
    frase_b(b + 4, "Quan- do‿o Se- nhor me li- ber- tou", "tou")
    frase_b(b + 6, "A mi- nha sor- te‿e- le mu- dou", "dou")
    frase_a(b + 8, "O meu la- men- to‿a- ca- bou")
    frase_a(b + 10, "A a- le- gri- a che- gou")
    frase_b(b + 12, "Quan- do‿o Se- nhor me li- ber- tou", "tou")
    frase_b(b + 14, "Tu- do‿em fes- ta e- le tor- nou", "nou")


def eu_vou_cantar(b):
    """'Eu vou cantar, eu vou celebrar' (2 compassos; também é a frase do vamp)."""
    for (bb, p, d, pt), s in zip([(0, 0, 2, "E4"), (0, 2, 2, "E4"), (0, 4, 2, "D4"), (0, 6, 4, "E4"),
                                  (0, 10, 2, "E4"), (0, 12, 2, "E4"), (0, 14, 2, "E4"), (1, 0, 2, "D4"),
                                  (1, 2, 12, "F#4")],
                                 "Eu vou can- tar, eu vou ce- le- brar".split()):
        ev(b + bb, p, d, pt, s)


def gran_des(b):
    """Anacruse do refrão (2º tempo e meio do compasso anterior)."""
    ev(b, 8, 4, "D4", "Gran-")
    ev(b, 12, 4, "G4", "des")


def pre(b):
    # "Então a minha boca se encheu de risos"
    for (bb, p, d, pt), s in zip([(0, 2, 4, "B3"), (0, 6, 4, "B3"), (0, 10, 4, "E4"), (0, 14, 4, "F#4"),
                                  (1, 2, 2, "B3"), (1, 4, 2, "B3"), (1, 6, 4, "B3"), (1, 10, 4, "F#4")],
                                 "En- tão a mi- nha bo- ca se‿en-".split()):
        ev(b + bb, p, d, pt, s)
    ev(b + 1, 14, 4, "G4", "cheu", "(")
    ev(b + 2, 2, 4, "F#4", "_", ")")
    ev(b + 2, 6, 4, "E4", "de")
    ev(b + 2, 10, 4, "D4", "ri-")
    ev(b + 2, 14, 6, "B3", "sos", "(")
    ev(b + 3, 4, 10, "A3", "_", ")")
    # "Estou vivendo agora como os que sonham"
    for (bb, p, d, pt), s in zip([(4, 2, 4, "B3"), (4, 6, 4, "B3"), (4, 10, 4, "E4"), (4, 14, 4, "F#4"),
                                  (5, 2, 2, "B3"), (5, 4, 2, "B3"), (5, 6, 4, "B3"), (5, 10, 4, "F#4"),
                                  (5, 14, 4, "G4"), (6, 2, 4, "F#4"), (6, 6, 2, "E4"), (6, 8, 2, "D4"),
                                  (6, 10, 4, "D4")],
                                 "Es- tou vi- ven- do a- go- ra co- mo os que so-".split()):
        ev(b + bb, p, d, pt, s)
    ev(b + 6, 14, 6, "B3", "nham", "(")
    ev(b + 7, 4, 10, "A3", "_", ")")
    eu_vou_cantar(b + 8)
    gran_des(b + 10)


def refrao(b, hold_next=8, pickup_next=False, last_short=False):
    """Refrão de 12 compassos (a anacruse 'Gran-des' fica no compasso anterior)."""
    def coisas(b0):
        ev(b0, 0, 10, "F#4", "coi-")
        ev(b0, 10, 2, "E4", "sas", "(")
        ev(b0, 12, 2, "F#4")
        ev(b0, 14, 10, "G4", "_", ")")

    coisas(b)
    for (bb, p, d, pt), s in zip([(1, 8, 4, "D4"), (1, 12, 4, "D4"), (2, 0, 2, "D4"), (2, 2, 2, "C4"),
                                  (2, 4, 2, "C4"), (2, 6, 4, "C4")], "o Se- nhor já fez por".split()):
        ev(b + bb, p, d, pt, s)
    ev(b + 2, 10, 2, "A3", "mim", "(")
    ev(b + 2, 12, 2, "B3")
    ev(b + 2, 14, 6, "A3", "_", ")")
    gran_des(b + 3)
    coisas(b + 4)
    for (bb, p, d, pt), s in zip([(5, 8, 4, "D4"), (5, 12, 4, "D4"), (6, 0, 2, "D4"), (6, 2, 2, "C4"),
                                  (6, 4, 6, "C4"), (6, 10, 4, "B3"), (6, 14, 14, "A3")],
                                 "E- le pre- pa- rou pra mim".split()):
        ev(b + bb, p, d, pt, s)
    todos_dirao(b + 8)
    que_grandes(b + 9, hold_next, last_short)
    if pickup_next:
        gran_des(b + 12)


def todos_dirao(b):
    for (bb, p, d, pt), s in zip([(0, 0, 2, "G3"), (0, 2, 2, "G3"), (0, 4, 2, "G3"), (0, 6, 4, "D4"),
                                  (0, 10, 2, "G3"), (0, 12, 2, "G3"), (0, 14, 4, "G3"), (1, 2, 8, "D4")],
                                 "To- dos di- rão, to- dos di- rão".split()):
        ev(b + bb, p, d, pt, s)


def que_grandes(b, hold_next=8, short=False):
    """'Que grandes coisas Deus já fez por mim': anacruse no compasso b (pos. 14)."""
    ev(b, 14, 2, "G3", "Que")
    for (bb, p, d, pt), s in zip([(1, 2, 4, "D4"), (1, 6, 4, "B3"), (1, 10, 6, "A3"), (2, 0, 2, "F#3"),
                                  (2, 2, 2, "B3"), (2, 4, 4, "A3"), (2, 8, 2, "G3"), (2, 10, 2, "G3")],
                                 "gran- des coi- sas Deus já fez por".split()):
        ev(b + bb, p, d, pt, s)
    ev(b + 2, 12, 2, "A3", "mim", "(")
    ev(b + 2, 14, 2 if short else 2 + hold_next, "G3", "_", ")")


# --- montagem da forma
verso(START["Parte 1"])
pre(START["Pré-refrão"])
refrao(START["Refrão"])                      # "mim" segura no 1º c. do Interlúdio
verso(START["Parte 2"])
pre(START["Pré-refrão 2"])
refrao(START["Refrão 2"], pickup_next=True)  # c. 13 = chegada + anacruse da repetição
refrao(START["Refrão 2"] + 13)              # "mim" segura no 1º c. do Vamp
for k in range(7):
    eu_vou_cantar(START["Vamp"] + 2 + 2 * k)
for k in range(4):
    eu_vou_cantar(START["Vamp (Fá)"] + 2 * k)
K = START["Todos dirão"]
todos_dirao(K)
que_grandes(K + 1, short=True)
todos_dirao(K + 4)
que_grandes(K + 5)                          # segura no c. de chegada (K+8)
gran_des(K + 8)
refrao(START["Refrão final"])               # segura no 1º c. do Final
M = START["Final"]
que_grandes(M)                               # tag 1
que_grandes(M + 3)                         # tag 2
que_grandes(M + 6, hold_next=16)             # tag 3: "mim" até o último compasso (fermata)


# ------------------------------------------------------------------ conversão para compassos
def key_of(bar):
    for mark, title, length, key in FORM:
        if START[title] <= bar < START[title] + length:
            return key
    return "F"


def target(pitch, bar):
    # guia (Sol, voz masculina) -> voz feminina: Mib = +6ª menor, Fá = +7ª menor
    return transpose(pitch, 5, 8) if key_of(bar) == "Eb" else transpose(pitch, 6, 10)


def split_dur(pos, length):
    out = []
    while length > 0:
        for d in OK_DUR:
            if d > length:
                continue
            if d >= 8 and pos % 4:
                continue
            if d in (4, 6) and pos % 2:
                continue
            if d == 16 and pos:
                continue
            if d == 12 and pos not in (0, 4):
                continue
            out.append((pos, d))
            pos += d
            length -= d
            break
    return out


def build_measures():
    bars = {b: [] for b in range(1, NBARS + 1)}
    for bar, pos, dur, pitch, syl, flags in sorted(MEL):
        if dur <= 0:
            continue
        tp = target(pitch, bar)
        start = (bar - 1) * BAR + pos
        end = start + dur
        pieces = []
        t = start
        while t < end:
            b = t // BAR + 1
            p = t % BAR
            seg = min(end, b * BAR) - t
            for pp, d in split_dur(p, seg):
                pieces.append((b, pp, d))
            t += seg
        for i, (b, pp, d) in enumerate(pieces):
            fl = ""
            if i < len(pieces) - 1:
                fl += "~"
            if i == 0 and "(" in flags:
                fl += "("
            if i == len(pieces) - 1 and ")" in flags:
                fl += ")"
            lyr = f"|{syl}" if i == 0 and syl != "_" else ""
            bars[b].append((pp, d, f"{tp}/{d}{fl}{lyr}"))
    out = {}
    for b, evs in bars.items():
        evs.sort()
        toks = []
        cur = 0
        for pp, d, tok in evs:
            if pp < cur:
                raise ValueError(f"sobreposição no c. {b}, pos {pp}")
            for rp, rd in split_dur(cur, pp - cur):
                toks.append(f"r/{rd}")
            toks.append(tok)
            cur = pp + d
        for rp, rd in split_dur(cur, BAR - cur):
            toks.append(f"r/{rd}")
        out[b] = " ".join(toks)
    return out


# ------------------------------------------------------------------ partitura
QUEM = {  # quem canta (texto no início de cada seção)
    "Intro": "Banda + metais (riff)",
    "Parte 1": "Mulheres (S+A) em uníssono · T+B respondem nos finais de frase",
    "Pré-refrão": "S-A-T; B entra em \"Eu vou cantar\"",
    "Refrão": "S-A-T-B · melodia nas contraltos",
    "Interlúdio": "Riff dos metais",
    "Parte 2": "Homens (T+B) em uníssono, 8vb · mulheres em \"oohs\"",
    "Pré-refrão 2": "S-A-T-B",
    "Refrão 2": "S-A-T-B (2ª vez: contracanto das sopranos)",
    "Vamp": "Camadas: T+B (8vb) → +A → +S",
    "Lançamento": "Hit tutti + virada",
    "Vamp (Fá)": "Tutti",
    "Todos dirão": "Mulheres chamam · homens respondem",
    "Refrão final": "S-A-T-B, ff",
    "Final": "Tag 3× (rit. na 3ª)",
}
DYN = {"Intro": "f", "Parte 1": "mp", "Pré-refrão": "mp", "Refrão": "f", "Interlúdio": "f",
       "Parte 2": "mf", "Pré-refrão 2": "mf", "Refrão 2": "f", "Vamp": "p", "Vamp (Fá)": "ff",
       "Todos dirão": "ff", "Refrão final": "ff"}


def main():
    sc = Score("Grandes Coisas", "Ministério Atitude",
               "Versão coro (SATB) + banda + metais · lead sheet (Etapa 1)", NBARS, beats_div=BAR, time=(4, 4))
    sc.keys = {1: -3, START["Vamp (Fá)"]: -1}
    sc.tempos[1] = (150, "Pop/Black gospel")
    coro = sc.add(Instrument("Coro (melodia)", "Coro", midi_program=54, sound_id="voice.vocals"))
    for mark, title, length, key in FORM:
        b = START[title]
        if mark:
            sc.marks[b] = (mark, title)
        else:
            coro.dir(b, "textb", title)
        coro.dir(b, "text", QUEM[title])
        if title in DYN:
            coro.dir(b, "dyn", DYN[title])
        sc.barlines[b - 1] = "light-light" if b > 1 else None
        for i, sym in enumerate(CHORDS[title]):
            coro.harm(b + i, sym)
        assert len(CHORDS[title]) == length, title
    sc.barlines = {k: v for k, v in sc.barlines.items() if v and k >= 1}
    sc.barlines[START["Vamp (Fá)"] - 1] = "light-light"
    coro.dir(START["Final"] + 6, "text", "rit.")
    meas = build_measures()
    last = meas[NBARS].split()
    last[-1] = last[-1] + "!"   # fermata no último "mim"
    meas[NBARS] = " ".join(last)
    for b in range(1, NBARS + 1):
        coro.put(b, meas[b])
    out = os.path.join(HERE, "grandes-coisas-leadsheet.musicxml")
    sc.write(out)
    print(f"{out}: {NBARS} compassos (~{NBARS * 4 * 60 / 150 / 60:.1f} min a ♩=150)")


if __name__ == "__main__":
    main()
