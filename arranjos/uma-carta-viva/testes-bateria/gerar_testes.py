"""Arquivos de diagnóstico da bateria para Sibelius + NotePerformer 5 (Drum Set Sticks).

Cada arquivo tem 1 compasso por peça do kit (com o nome escrito em cima) e depois
4 compassos do groove pop 6/8. A diferença entre os arquivos é só COMO a nota MIDI de
cada peça é informada ao Sibelius:
  A-sem-midi : nenhuma nota MIDI -> o Sibelius usa só a posição na pauta + cabeça de nota
  B-gm       : nota General MIDI exata (bumbo 36, caixa 38...)
  C-spec     : nota GM + 1 (leitura literal da especificação MusicXML; era a versão anterior)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "ferramentas"))
from mxl import Score, Instrument  # noqa: E402

PECAS = [("kick", "Bumbo"), ("snare", "Caixa"), ("xstick", "Aro (cross-stick)"), ("tom1", "Tom 1 (agudo)"),
         ("tom2", "Tom 2 (médio)"), ("ftom", "Surdo (floor tom)"), ("hh", "Chimbal fechado"),
         ("hhopen", "Chimbal aberto"), ("hhfoot", "Chimbal no pé"), ("ride", "Ride"), ("crash", "Crash")]
GROOVE = [("p:crash/2 p:hh/2 p:hh/2 p:hh+snare/2> p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/4 p:kick/2"),
          ("p:hh/2 p:hh/2 p:hh/2 p:hh+snare/2> p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/4 p:kick/2"),
          ("p:hh/2 p:hh/2 p:hh/2 p:hh+xstick/2 p:hh/2 p:hh/2", "p:kick/4 p:kick/2 r/6"),
          ("p:hh/2 p:hh/2 p:hh/2 p:snare/1 p:snare/1 p:tom1/1 p:tom1/1 p:tom2/1 p:ftom/1", "p:kick/4 p:kick/2 r/6")]

for tag, mode in (("A-sem-midi", "none"), ("B-gm", "gm"), ("C-spec", "spec")):
    n = len(PECAS) + len(GROOVE) + 1
    sc = Score(f"Teste bateria {tag}", "diagnóstico", "Sibelius + NotePerformer", n)
    sc.tempos = {1: (60, "")}
    dr = sc.add(Instrument("Drum Set (Sticks)", "Bat.", clef="perc", percussion=True, sound="drums"))
    dr.drum_midi = mode
    for i, (k, nome) in enumerate(PECAS, 1):
        if k in ("kick", "hhfoot"):
            dr.put(i, "r/12", " ".join([f"p:{k}/2"] * 6))
        else:
            dr.put(i, " ".join([f"p:{k}/2"] * 6), "r/12")
        dr.dir(i, "textb", f"{i}. {nome}")
    for j, (m, f) in enumerate(GROOVE):
        dr.put(len(PECAS) + 1 + j, m, f)
    dr.dir(len(PECAS) + 1, "textb", "Groove")
    dr.put(n, "p:crash+snare/6^ r/6", "p:kick/6 r/6")
    sc.write(os.path.join(HERE, f"teste-bateria-{tag}.musicxml"))
    print("ok", tag)
