# Uma Carta Viva (GET Worship): versão instrumental "Camp Inspired"

Status: **grade escrita até o Refrão 2 (c. 1–75)**. Falta a Ponte e o Final.

Arquivos: `uma-carta-viva.musicxml` (MusicXML 3.1, abrir no Sibelius) · `previa-verovio.pdf` (prévia rápida, sem a gravação do Sibelius) · `gerar_partitura.py` (gera a grade: `python3 gerar_partitura.py`)
Referência de estilo: `docs/estilo-orquestracao.md`
Fonte: orquestração sinfônica fornecida (MusicXML, 73 c.)

---

## 1. Análise da fonte

| Item | Valor |
|---|---|
| Tonalidade | Ré maior (sem modulação) |
| Compasso / andamento | 6/8, ♩. = 51 ("Moderato") |
| Extensão da melodia | Lá3 a Ré5 (refrão entre Lá3 e Si4) |
| Final da fonte | Termina no c. 73 sem resolução (G com A/G). O final precisa ser criado |

### Forma e harmonia (redução; cifras aproximadas, a conferir)

| Seção (fonte) | Compassos | Harmonia por compasso (meio compasso quando houver `–`) |
|---|---|---|
| Introdução | 1–9 | D \| D \| D \| Em7 \| Em7 \| D/F# \| D/F# \| G(add9) \| G (anacruse da melodia) |
| Estrofe [A] | 10–17 | A/C# – G/B \| D – Em7 \| D/F# \| D \| A/C# – G/B \| Bm/F# – Em7 \| D \| D – D/F# |
| Pré-refrão [B] | 18–25 | Em7 \| Em7 \| D/F# \| D/F# \| G \| G \| **Gm6** (empréstimo) \| Gm6 – A |
| Refrão [C] | 26–41 (2×8) | D \| D \| Em7 \| Em7 \| Bm7 – Bm7/A \| A – D/F# \| G(add9) \| G – A/G ‖ (repete) |
| Interlúdio [D] | 42–49 | D \| D \| Em7 \| Em7 \| D/F# ("Oh") \| D/F# \| G \| G |
| Pré-refrão 2 [E] | 50–57 | Em7 \| Em7 \| D/F# \| D/F# \| G \| G \| G \| G(sus) (mf→f) |
| Refrão 2 [F] | 58–73 (2×8) | igual ao Refrão, *f* |

O baixo da Intro e do Interlúdio sobe por grau (**D–E–F#–G**). Esse vai ser o fio condutor
dos interlúdios.

---

## 2. Conceito da versão

- **Instrumental.** A melodia passa entre os **naipes de big band** (Trompetes, Saxofones,
  Trombones). Madeiras e cordas fazem a moldura (pads, dobras 8va, ecos e runs).
- Arco no estilo Camp: entrada tutti, verso enxuto, crescimento em camadas, modulação
  anunciada, último refrão *ff*, tag e final.
- Todo o material novo (motivo da intro, fills, contracantos, transições) é **original** e
  sai das células da própria canção.

## 3. Estrutura proposta (decisões de 12/10/2026)

**Decisões:** começa em **Mi♭** e modula para **Fá** no Refrão 2 · **♩. = 60** ·
formação Camp padrão + substituições · **Ponte**: o usuário ainda vai mandar a melodia e a
harmonia · **Final**: definir depois da Ponte.

A ♩.=60 cada compasso de 6/8 dura 2 s.

| # | Seção | Comp. | Tom | Melodia com… | Textura / função | Din. |
|---|---|---|---|---|---|---|
| 1 | **Intro** | 8 | Eb | Motivo-assinatura criado a partir da cabeça do refrão: **Tpt 1 + A.Sax 1** em bloco com Tpt 2&3; **Tbns** respondem | Tutti sobre o baixo subindo Eb–Fm7–Eb/G–Ab; madeiras 8va; cordas pad; últimos 2 c. em decresc. | **f** → mf |
| 2 | **Vamp** | 2 | Eb | — | Redução súbita: piano + ostinato em colcheias de 6/8 (Clarinetes), shaker, baixo | *subito* mp |
| 3 | **Estrofe** | 8 | Eb | **A.Sax 1 solo** (frase 1) e **T.Sax solo** (frase 2) | Cordas em pad, Fl/Cl com ecos curtos nas respostas, Tpts tacet | mp |
| 4 | **Pré-refrão 1** | 8 | Eb | **Tbn 1 solo** cantabile (Trompas em pad) | Abm6 destacado (Tbns + Trompas); baixo sobe; prato suspenso em swell no último c. | mp → mf |
| 5 | **Refrão 1** | 16 | Eb | c. 1–8: **Tpt 1 + A.Sax 1** em uníssono, com respostas de Tbns. c. 9–16: **soli de Saxes** (A1, A2, T, Bari) | Bateria plena; cordas em pad e hits; Trompas no contracanto médio; fills de Tpt nos respiros | mf |
| 6 | **Interlúdio** | 8 | Eb | Retorno do motivo da Intro (reduzido); o "Oh" da fonte vira **Tbns + Trompas soli** em notas longas | Run de cordas no fim; baixo Eb–F–G–Ab | mf → mp |
| 7 | **Pré-refrão 2** | 8 + 1 | Eb → | **T.Sax + Tbn 1 em oitavas**; ostinato nas Clarinetes; *grad. cresc.* | **+1 c. de transição em C7sus4 → C7** (V de Fá): fill de bateria, run de cordas, swell de prato, baixo subindo | mf → **f** |
| 8 | **Refrão 2** | 16 | **F** | **Bloco de trompetes** (Tpt 1 lead, Tpt 2&3 fechados) + **Tbn 1&2 8vb**; madeiras 8va | Contracanto de Trompas + A.Sax; cordas em pad agudo + runs; pandeirola; tutti | **ff** |
| 9 | **Ponte** | ? | F | *aguardando melodia/harmonia* | Ideia: redução (cordas + piano + soli de Tbns), com crescimento até o retorno | ? |
| 10 | **Refrão final / Tag / Final** | ? | F (ou nova subida) | *definir depois da Ponte* | Opções: Tag com bVI–bVII–I + fermata add9 · stinger · final suave | — |

### Harmonia transposta (Eb, seções 1–7)

| Seção | Harmonia |
|---|---|
| Intro / Interlúdio | Eb \| Eb \| Eb \| Fm7 \| Fm7 \| Eb/G \| Eb/G \| Ab(add9) \| Ab |
| Estrofe | Bb/D – Ab/C \| Eb – Fm7 \| Eb/G \| Eb \| Bb/D – Ab/C \| Cm/G – Fm7 \| Eb \| Eb – Eb/G |
| Pré-refrão | Fm7 \| Fm7 \| Eb/G \| Eb/G \| Ab \| Ab \| Abm6 \| Abm6 – Bb |
| Refrão | Eb \| Eb \| Fm7 \| Fm7 \| Cm7 – Cm7/Bb \| Bb – Eb/G \| Ab(add9) \| Ab – Bb/Ab |

### Harmonia do Refrão 2 (F)
F \| F \| Gm7 \| Gm7 \| Dm7 – Dm7/C \| C – F/A \| Bb(add9) \| Bb – C/Bb

### Tessitura da melodia
- Em Eb: Bb3 a Eb5 (concerto).
- Em F: C4 a F5 (concerto), Tpt 1 escrito Ré4 a Sol5. Confortável para lead com bloco abaixo.

## 3b. Bateria: pop 6/8 "quadrado" e constante

A ideia é a mesma dos arranjos do Camp: um groove reto, que não muda de caráter. Em cada
seção só muda a "cor" (aro, caixa, ride), e há fills curtos no fim das seções.

| Seção | Mãos | Pés |
|---|---|---|
| Intro / Refrão 1 / Pré 2 (c. 55–58) | Chimbal em colcheias + **caixa no 4** (acentuada) | Bumbo no **1, 3 e 6** |
| Vamp | Só chimbal | Bumbo no 1 |
| Estrofe / Pré 1 (início) | Chimbal + **aro (cross-stick) no 4** | Bumbo no **1 e 3** |
| Pré 1 (c. 23+) / Interlúdio / Pré 2 | Chimbal + **caixa no 4** | Bumbo no 1 e 3 |
| Refrão 2 | **Ride** em colcheias + caixa no 4 | Bumbo no 1, 3 e 6 |

- Prato de ataque (crash) a cada 4 compassos nos refrões.
- Fills de meio compasso (semicolcheias caixa/tons) nos c. 8, 18, 26, 34, 42, 50, 58, 67 e 75.
- A percussão acompanha por seção: shaker (verso/interlúdio), pandeirola (refrões/Pré 2) e
  prato suspenso em swell antes das chegadas.

## 4. Instrumentação (formato Camp padrão)

Fl 1&2 · Ob · Cl 1&2 · Fg/Clarone · A.Sax 1&2 · T.Sax · Bari Sax · Tpt 1 · Tpt 2&3 ·
Trompa 1&2 · Tbn 1&2 · Tbn 3/Tuba · Percussão (shaker, pandeirola, prato suspenso, mark tree,
tímpano opc.) · Bateria · Rhythm (cifra) · Piano · Vln 1&2 · Vla · Vc · Cb

Partes de substituição: Cl 3 (Viola) · A.Sax (Trompa) · T.Sax/Barítono TC (Tbn 1&2) ·
Bari/Tuba (Tbn 3) · Redução de cordas para teclado.

## 5. Próximos passos

1. Aprovar ou ajustar esta estrutura (tonalidade, andamento, quem leva a melodia em cada seção).
2. Escrever a grade em MusicXML seção por seção: primeiro melodia + harmonia (*lead sheet*
   da versão), depois o bloco de metais e saxes, depois a moldura (madeiras/cordas) e a
   rítmica.
3. Revisar e gerar as partes e as substituições.
