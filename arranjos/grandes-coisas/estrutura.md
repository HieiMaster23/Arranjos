# Grandes Coisas (Ministério Atitude): versão coro + banda + metais, linha Pop/Black/Soul

Status: **Etapa 3 revisada (coro simplificado, 15/10)**: coro SATB (+ grade completa coro + banda). Ver § 9.

Arquivos: `grandes-coisas-leadsheet.musicxml` (abrir no Sibelius) · `previa-leadsheet.pdf`
(prévia: `python3 ../../ferramentas/previa_pdf.py grandes-coisas-leadsheet.musicxml previa-leadsheet.pdf`)
· `grandes-coisas-ritmica.musicxml` + `previa-ritmica.pdf` (Etapa 2; gerar: `python3 gerar_ritmica.py`)
· `grandes-coisas-coro.musicxml` + `previa-coro.pdf` (Etapa 3, só o coro) e
`grandes-coisas-grade.musicxml` (coro SATB + banda) e `grandes-coisas-coro-reduzido.musicxml` +
`previa-coro-reduzido.pdf` (SATB em 2 pautas: S/A na clave de sol, T/B na clave de fá); gerar todos:
`python3 gerar_coro.py`
· `previa-audio.mp3`: prévia de áudio da grade (General MIDI, só para ouvir o escopo); gerar:
`../../ferramentas/previa_audio.sh grandes-coisas-grade.musicxml previa-audio.mp3 --rit 144 --vel Soprano=105 --vel Contralto=100 --vel Tenor=100 --vel "Baixo (coro)=95" --vel "Teclado (piano)=70" --vel "Órgão (Hammond)=55" --vel Guitarra=60 --vel Baixo=95 --vel Bateria=85`
· `gerar_leadsheet.py` (gera o lead sheet: `python3 gerar_leadsheet.py`)

Referência de estilo: `docs/estilo-gospel-soul.md` (groove, coro, harmonia, vamp, metais).
Projeto musicalmente independente dos outros arranjos do repositório (só as ferramentas de
`ferramentas/` são compartilhadas).
Fonte: guia transcrito por IA (Moises): Melodia, Baixo, Bateria e Harmonias 1–7 (MIDI) + cifra
do Cifra Club (enviada como imagem). Os MIDIs ficam fora do repositório; o mapa abaixo usa a
numeração de compassos deles.

---

## 1. Análise da fonte

| Item | Valor |
|---|---|
| Tonalidade | **Sol maior** (cifra e MIDI concordam) |
| Grade do Moises | 4/4, ♩ = 150, 160 compassos (≈ 4:15). **Cada acorde dura 2 compassos** dessa grade |
| Andamento real | **♩ = 150** (confirmado pelo usuário em 14/10: "a música é animada mesmo"). Cada verso da letra ocupa 2 compassos |
| Extensão da melodia | Mi3–Lá4 no guia (voz masculina). Em Sol, para o coro feminino: Mi4–Lá5; o refrão fica entre Ré4/Ré5 e Sol5 |
| Groove do guia | Teclado em colcheias contínuas (Harmonia 4), baixo em colcheias na fundamental, bateria pop reta |

### Forma e harmonia (cifra × compassos do MIDI)

| Seção | Compassos (MIDI) | Harmonia | Observações |
|---|---|---|---|
| Contagem | 1 | — | |
| **Intro** | 2–17 | (G \| C \| D/F# \| C) ×2 | Teclado com voicings add9/sus2; a "melodia" que aparece nos c. 6–17 é *ad lib* |
| **Parte 1** ("Nasceu em meu coração…") | 18–33 | (G \| D/F# \| Em \| C) ×2 | Melodia grave (Sol3–Ré4 no guia), frases sincopadas |
| **Pré-refrão** ("Então a minha boca…") | 34–44 | (E \| B/D# \| D \| A/C#) ×2 \| C \| D | **Baixo cromático descendente E–D#–D–C#.** O Moises leu "Em": é **E maior** (V/vi), confirmado pela cifra |
| **Refrão 1** ("Grandes coisas…") | 45–57 | G \| C – D \| Em7 \| C – D \| Em7 \| D \| C – D \| G | Anacruse no c. 44 |
| **Parte 2** | 58–74 | como a Parte 1 | Harmonias 7: notas longas (apoio "ooh") nos c. 66–69 |
| **Pré-refrão 2** | 75–84 | como o Pré 1 | |
| **Refrão 2 + 3** | 85–110 | Refrão ×2 | Teclado mais cheio |
| **Solo / interlúdio** | 111–116 | G \| C \| D/F# \| (Em) | Banda sozinha |
| **Breakdown** ("Eu vou cantar, eu vou celebrar") | 117–126 | C \| D \| … | Baixo sai a partir do c. 119; Harmonia 3 faz uma figura repetida em Lá4/Ré5 (c. 123–126). **Melhor lugar para o vamp gospel** |
| **Refrão final** | 127–148 | "Todos dirão" (Em7 \| C \| D) + Refrão ×2 | |
| **Final** | 149–160 | G \| C \| D/F# \| C … G | Como a Intro |

### O que cada MIDI traz (para referência)

| Arquivo | Conteúdo provável | Uso |
|---|---|---|
| Melodia Voz | Melodia principal (voz guia) | Base da Etapa 1 (lead sheet) |
| Baixo | Linha de baixo (colcheias na fundamental) | Conferir as inversões (D/F#, B/D#, A/C#) |
| Bateria | Groove pop com fills; muito "vazamento" (aro e caixa espalhados) | Só o desenho geral |
| Harmonia 1, 2 | Teclado/pad na Intro, nas Partes e no Pré | Voicings de referência |
| Harmonia 3 | Pad agudo na Intro (Ré-Sol-Ré) e figura repetida no breakdown | Ideia de textura |
| Harmonia 4 | Teclado principal em colcheias contínuas (add9/sus2) | Ritmo harmônico |
| Harmonia 5 | Grave intermitente (mão esquerda/synth) | Descartar ou só conferir |
| Harmonia 6 | Notas de 0,03 tempo (ruído percussivo) | Descartar |
| Harmonia 7 | 4 notas longas (Sol3/Lá3) | Apoio vocal |

---

## 2. Conceito da versão

**Formação (decidida em 14/10):** **coro S-A-T-B** (B opcional, mas previsto; **sem solista**) +
**banda** + **naipe de metais pop: Trompete, Sax e Trombone**. Não há orquestra (cordas e madeiras
saem; se quiser "pad", fica no teclado).

- **Coro na frente**, banda gospel como motor e os 3 metais como *horn section* de pop/soul:
  hits, respostas nos respiros e um riff original.
- **Metais a 3 vozes:** Tpt no lead, Sax no meio e Tbn embaixo. Nos hits, em bloco fechado
  (tríade ou acorde com 9ª/6ª). Nas frases de riff, Tpt + Sax em uníssono ou oitava e Tbn
  com o baixo ou em 3ª/6ª abaixo. Nos tutti mais fortes, uníssono/oitava dos três para ter peso.
- O material da canção já tem três ganchos fortes para o estilo:
  1. **O baixo cromático do pré** (E–D#–D–C# em Sol): linha do Trombone + baixo e
     reharmonização com dominantes de passagem.
  2. **"Eu vou cantar, eu vou celebrar"**: frase curta e rítmica, ideal para o **vamp** com
     camadas de coro, call-and-response e a modulação.
  3. **"Todos dirão, todos dirão"**: chamada e resposta natural entre naipes (mulheres chamam, homens respondem).
- **Riff original de metais** para a Intro/Interlúdio/Final, criado a partir da rítmica
  sincopada de "Grandes coisas o Senhor já fez por mim" (só a célula rítmica e o contorno
  geral, sem copiar a melodia).

## 3. Estrutura proposta (rascunho com compassos)

♩ = 150, 4/4, 2 compassos por acorde (como no original). **Duração-alvo: a mesma do original
(≈ 4:15).** Tonalidade: **Mib → Fá** (proposta, § 6). **Sem solista: o coro canta tudo.** As chamadas e
respostas ficam entre naipes (mulheres × homens, sopranos × resto).

| # | Seção | C. | Tom | Coro | Banda + metais | Din. |
|---|---|---|---|---|---|---|
| 1 | **Intro** | 8 | Eb | — (ou "Oh!" em hit no último c.) | Riff dos metais sobre Eb – Ab – Bb/D – Ab; hits com a bateria | **f** |
| 2 | **Parte 1** | 16 | Eb | **Mulheres em uníssono** (S+A, Dó4–Sib4); nos finais de frase, T+B respondem com hits curtos ("ooh"/"yeah") | Banda enxuta (bateria *pocket*, baixo, teclas); metais tacet | mp |
| 3 | **Pré 1** | 10 | Eb | **S-A-T** em bloco, o B entra no "Eu vou cantar…" | Tbn dobra o baixo cromático (C–B–Bb–A); cresc. | mp → mf |
| 4 | **Refrão 1** | 12 | Eb | **S-A-T-B** em bloco, melodia nas contraltos (+ sopranos em uníssono ou em 3ª acima) | Metais respondem nos respiros | f |
| 5 | **Interlúdio** | 8 | Eb | "Oohs" em pad (opcional) | Riff dos metais (variação) | f |
| 6 | **Parte 2** | 16 | Eb | **Homens em uníssono** (T+B, Dó3–Sib3; T pode ir 8va nos finais) na melodia; mulheres em "oohs"/respostas a 2 vozes | Sax em contracanto suave | mf |
| 7 | **Pré 2** | 10 | Eb | **S-A-T-B** | Tutti cresc.; fill no fim | mf → f |
| 8 | **Refrão 2 ×2** | 24 | Eb | Bloco; 2ª vez com as sopranos num contracanto agudo e A-T-B na melodia | Metais em bloco + hits | f |
| 9 | **Vamp** "Eu vou cantar, eu vou celebrar" | 8 | Eb → **F** | Entra direto no tempo 1 depois do "mim". Camadas a cada 2 c.: T+B (8vb) → +A → +S → tutti | Bateria + baixo + palmas; entram teclas e depois os metais; **modulação no último compasso** (Bb → C7sus4 no 3º tempo) | mp → f |
| 10 | **Vamp em Fá** | 8 | **F** | Tutti | Banda e metais plenos | f |
| 11 | **Preparação** | 2 | F | Anacruse "Gran-des" | Hit tutti + virada (Bb/C, C7sus4 → C7) | f → ff |
| 12 | **Refrão final** | 12 | F | S-A-T-B no agudo; no "Todos dirão", mulheres chamam e homens respondem | *Shout* dos metais | **ff** |
| 13 | **Final** | 10 | F | Tag "Que grandes coisas…" ×3, a última em rit. com acorde aberto | Riff final + *church ending* com fermata e hit | ff |
|  | **Total** | **147** | | | | **≈ 3:55** |

Decisão de 14/10: vamp de 8 c. em Mib, modulação, 8 c. em Fá, preparação de 2 c. e direto
ao Refrão final (a seção separada "Todos dirão" saiu). Ficou ≈ 20 s mais curto que o original;
se quiser compensar, dá para repetir o Refrão final (×2) ou alongar o Final.

## 4. Etapas de trabalho

| Etapa | Entrega | Formato |
|---|---|---|
| **0. Análise + estrutura** | Este documento + memória de estilo gospel | `.md` (**feito**) |
| **1. Lead sheet limpo** | Melodia corrigida (o Moises tem ruído e deslocamentos), cifra e letra, no tom definido, já na forma nova | MusicXML + PDF de prévia |
| **2. Seção rítmica + harmonia gospel** | Reharmonização por seção, linha de baixo, groove de bateria por seção, cifras | MusicXML (Bateria, Baixo, Teclado, Guitarra/cifra) |
| **3. Coro** | S-A-T-B (B opcional) com letra, respirações, cortes e chamadas/respostas entre naipes | MusicXML (4 pautas de coro) |
| **4. Metais** | Riff, hits, respostas e shout para Tpt, Sax e Tbn | MusicXML (grade completa) |
| **5. Revisão e partes** | Playback (Sibelius + NotePerformer), partes individuais, guia de ensaio por naipe | MusicXML + partes |

Em cada etapa você ouve/revisa antes de seguirmos para a próxima.

## 5. Decisões

1. ~~Andamento~~: **♩ = 150** (decidido).
2. ~~Tonalidade~~: **Mib → Fá** (confirmado em 14/10; ver § 6, "Revisão"). Fá → Sol deixava o refrão com Fá5 no topo: alto demais para o som *belt* do pop/black.
3. ~~Coro~~: **S-A-T-B** (decidido). O baixo é escrito para cantar, mas a música tem que fechar sem ele: nada de essencial só no baixo (S-A-T completam o acorde; o baixo dobra a fundamental ou faz respostas/ostinatos graves).
4. ~~Formação~~: **banda (bateria, baixo, teclado, órgão, guitarra) + Trompete, Sax Alto e Trombone, 1 de cada** (decidido).
5. ~~Duração~~: **≈ a do original** (decidido).
6. ~~Solista~~: **sem solista** (decidido): o coro brilha sozinho, em linguagem bem black.

## 6. Tonalidade para o coro (decidido: Mib → Fá)

### Extensão da melodia por seção (altura do guia, voz masculina)

| Seção | Extensão | Núcleo (80 % do tempo) | Nota média |
|---|---|---|---|
| Partes 1 e 2 | Mi3–Mi4 | Mi3–Ré4 | Lá3 |
| Pré-refrão | Lá3–**Lá4** | Lá3–Sol4 | Mib4 |
| Refrão | Fá#3–Sol4 | Sol3–Sol4 | Dó4 |
| Breakdown ("Eu vou cantar…") | Si3–Sol4 | Dó4–Sol4 | Mi4 |

O problema de Sol não é o refrão em si (Sol–Sol). O problema é que **não sobra espaço para
subir**: o pré chega a Lá4 (Lá5 nas sopranos), e qualquer modulação no vamp leva o coro para
Lá5/Si5. Além disso, os versos ficam graves para os homens se o tom baixar
muito. A decisão depende de **quem canta os versos** e de **para onde o vamp sobe**.

### Opções (melodia nas sopranos; o coro canta do pré em diante)

| Opção | Pré (pico) | Refrão (sopranos) | Versos (homens / mulheres) | Metais | Comentário |
|---|---|---|---|---|---|
| **A. Fá → Sol** (recomendada) | Sol5 | Fá4–Fá5 | Ré3–Dó4 / Ré4–Dó5 | Ótima para os metais (Fá e Sol) | Começa 1 tom abaixo e **termina no tom original** no clímax. O vamp sobe Fá → Sol (1 tom) ou Fá → Fá# → Sol (meio tom duas vezes; Fá# fica pesado para os metais, mas dura poucos compassos) |
| **B. Mib → Fá (→ Sol)** | Fá5 | Mib4–Mib5 | Dó3–Sib3 (grave) / Dó4–Sib4 | Ótima para metais | Mais confortável para o coro e com mais espaço para subir 2×, mas os versos ficam graves para os homens (Dó3–Sib3) e o Mib2 é grave para baixo amador |
| C. Mi → Fá → Fá# | Fá#5 | Mi4–Mi5 | Dó#3–Si3 / Dó#4–Si4 | Ruim (Mi e Fá# para sopros em Sib) | Escada clássica de meio tom, mas cansativa para os sopros |
| D. Sol sem modular | Lá5 | Sol4–Sol5 | Mi3–Ré4 / Mi4–Ré5 | Boa | Mantém o original, mas perde o recurso de subida no vamp |

### Outras ideias que ajudam o coro em qualquer tom
- **O pico do pré (Lá4 do guia) só para as sopranos**, com as contraltos numa harmonia abaixo
  (3ª ou 6ª) e os tenores no uníssono das contraltos.
- **Melodia passeando pelos naipes:** Parte 2 com contraltos + tenores na melodia em
  uníssono (região média dos dois); refrão com a melodia nas sopranos e o bloco abaixo.
- **Depois de cada modulação**, o soprano sobe e o tenor fica parado ou desce (voicing
  "aberto por cima"), para os homens não estourarem.
- **Vamp em registro médio:** "Eu vou cantar, eu vou celebrar" fica num âmbito de 5ª;
  dá para escrever as camadas de baixo para cima (tenor → contralto → soprano) e só a
  última camada vai ao agudo.

### E o baixo do coro?
Com o B na fundamental, Fá e Sol são tons muito bons para os baixos (Fá2–Ré4 cobre tudo, e
o pedal de tônica fica em Fá2/Fá3). Em Mib, o Mib2 já é grave para baixo amador, então o
baixo fica mais vezes na oitava de cima. Isso conta mais um ponto para a **opção A**.

### Revisão (14/10): Fá5 no topo do refrão é alto para um refrão pop?

**Sim, para o som que queremos.** Em Fá, as sopranos ficariam ~10 % do refrão em Fá5 e ~10 % em
Mi5 (a cabeça "Grandes coisas" vai ao topo), e o pré chegaria a Sol5. Para canto lírico isso é
normal, mas o som black/pop é ***belt*** (voz de peito/mista), e o teto confortável de *belt*
de uma soprano amadora fica por volta de **Ré5–Mib5**. Acima disso, ela passa para a voz de
cabeça e o som perde o peso.

Distribuição do refrão (tempo em cada nota):

| Nota do guia | % do refrão | em Fá (mulheres) | em **Mib** (mulheres) | em Ré (mulheres) |
|---|---|---|---|---|
| Sol4 | 10 % | Fá5 | **Mib5** | Ré5 |
| Fá#4 | 11 % | Mi5 | Ré5 | Dó#5 |
| Ré4 | 25 % | Dó5 | Sib4 | Lá4 |
| Lá3 | 14 % | Sol4 | Fá4 | Mi4 |
| Sol3 | 22 % | Fá4 | Mib4 | Ré4 |

**Proposta nova: Mib → Fá.**
- Refrão das mulheres em Mib4–Mib5, inteiro dentro do *belt*. O pico do pré (Fá5, 4 % do pré)
  fica só com as sopranos.
- **Melodia nas contraltos** (região de peito ideal), com as sopranos em uníssono ou numa
  harmonia acima. Isso é bem típico do coro black.
- Versos: mulheres em Dó4–Sib4 (ótimo para contraltos) e homens em Dó3–Sib3 (barítonos e
  baixos; os tenores podem subir 8va nos finais de frase).
- O vamp sobe 1 tom para **Fá**, e o refrão final chega a Fá5 só no clímax, quando o *ff* e a
  energia justificam. Se mesmo assim ficar alto, o refrão final pode ter a melodia nas
  contraltos e as sopranos numa 3ª abaixo do topo nas notas mais altas.
- Para os metais, Mib e Fá são ótimos (Tpt em Fá/Sol escrito, Sax alto em Dó/Ré).
- Baixos do coro: fundamental em Mib3 (ou Mib2 opcional).

Alternativa ainda mais baixa: **Ré → Mi** (refrão Ré4–Ré5), mas os versos dos homens ficam em
Si2–Lá3 (grave demais) e Mi é um tom pior para os metais.

## 7. Etapa 1: lead sheet

### Mapa de compassos (♩ = 150, 4/4)

| Marca | Seção | Compassos | Nº | Tom | Acordes |
|---|---|---|---|---|---|
| A | Intro | 1–8 | 8 | Mib | Eb Ab Bb/D |
| B | Parte 1 | 9–24 | 16 | Mib | Eb Bb/D Cm Ab |
| C | Pré-refrão | 25–35 | 11 | Mib | C G/B Bb F/A Ab |
| D | Refrão | 36–47 | 12 | Mib | Eb Ab Bb Cm7 |
| E | Interlúdio | 48–55 | 8 | Mib | Eb Ab Bb/D |
| F | Parte 2 | 56–71 | 16 | Mib | Eb Bb/D Cm Ab |
| G | Pré-refrão 2 | 72–82 | 11 | Mib | C G/B Bb F/A Ab |
| H | Refrão 2 | 83–107 | 25 | Mib | Eb Ab Bb Cm7 |
| I | Vamp | 108–115 | 8 | Mib | Ab Bb Bb→C7sus4 |
| J | Vamp (Fá) | 116–123 | 8 | Fá | Bb C |
| K | Preparação | 124–125 | 2 | Fá | Bb/C C7sus4→C7 |
| L | Refrão final | 126–137 | 12 | Fá | F Bb C Dm7 |
| M | Final | 138–147 | 10 | Fá | F Bb C Dm7 Bbm6 F(add9) |

Total: **147 compassos ≈ 3:55**.

### Como a melodia foi limpa
- A melodia está escrita na altura das **vozes femininas**. Os homens cantam 8vb (Parte 2 e
  camadas graves do vamp).
- Usei principalmente a 1ª passagem de cada seção do guia (c. 18–57 do MIDI), onde o Moises
  está mais estável. Mais adiante a gravação "escorrega" em relação à grade de 150 (deve ser
  ao vivo), e a Parte 2 e o Pré 2 do MIDI ficam deslocados.
- **Ritmo:** a melodia do guia entra quase sempre **no contratempo** (antecipações de
  colcheia), e mantive isso porque é a "levada" da música. O baixo também antecipa as
  mudanças de acorde em colcheia.
- O refrão terminava sobre a chegada do acorde ("mim"): a nota fica segura no 1º compasso da
  seção seguinte (Interlúdio, Final; no fim do Refrão 2 o "mim" é curto e o Vamp entra no tempo 1), e a anacruse "Gran-des" entra nos tempos 3 e 4 do
  compasso de chegada.

### Pontos a conferir com a gravação (§ 7)
1. **Antecipações:** confirme se a voz realmente entra no contratempo ("Nas-ceu em meu…").
   Detalhe: a caixa do guia cai nos tempos 1 e 3 da grade do Moises; na Etapa 2 vou
   escrever a bateria com caixa no **2 e 4** em relação aos acordes. Se soar "invertido",
   desloco a grade.
2. **Pré-refrão, 1º verso:** a divisão de "se‿en-**cheu** de **ri**-sos" (melisma em "cheu" e
   em "sos") foi deduzida pela comparação com o 2º verso; confira as sílabas.
3. **Refrão:** "coi-**sas**" com a volta Mi–Fá#–Sol (no guia) e "mim" com Lá–Si–Lá. Veja se é
   isso ou se a gravação divide outras sílabas nessas notas.
4. **Elisões:** "Quan-do‿o", "sor-te‿e-le", "la-men-to‿a", "Tu-do‿em" ficam numa nota só.
5. **Parte 2:** usei a mesma letra da Parte 1 (a cifra só mostra uma estrofe).
6. **Pré-refrão 2:** no original ele sobe até Lá ("eu vou celebrar"); no lead sheet ficou
   igual ao Pré 1. Se quiser a subida, entra na Etapa 3 (coro).
7. **Vamp, Preparação e Final** (acordes Ab–Bb, C7sus4–C7, Bbm6) são provisórios:
   a harmonia gospel é definida na Etapa 2.

## 8. Etapa 2: seção rítmica + harmonia gospel

Arquivo: `grandes-coisas-ritmica.musicxml` (Coro guia, Teclado, Órgão, Guitarra, Baixo,
Bateria). A harmonia fica em `gerar_leadsheet.py` (`CHORDS`) e vale para o lead sheet e para
a banda. A cifra básica da canção continua no § 1.

### Harmonia (Mib; o Refrão final e o Final são a mesma ideia em Fá)

| Seção | Acordes (1 por compasso; "A → B" = troca no 3º tempo) | Ideia |
|---|---|---|
| Intro / Interlúdio | Eb(add9) · Eb/G · Abmaj9 · Ab6/9 · Bb/D · Bb/D → Cm7 · Abmaj9 · Bb7sus4 | Baixo subindo Eb–G–Ab; Bb7sus4 "gospel" no lugar do V |
| Partes 1 e 2 | Eb(add9) ×2 · Bb/D ×2 · Cm7 · Cm7 → **Eb7/Bb** · Abmaj7 · **Ab/Bb** / … · Abmaj7 → **G7#9** | Baixo descendo C–Bb–Ab com V7/IV; o G7#9 no fim prepara o pré (Dó maior) |
| Pré-refrão | C(add9) · G/B · Bb(add9) · F/A (×2) · Abmaj9 · Bb(add9) · Bb7sus4 | Mantém a **descida cromática C–B–Bb–A–Ab** da canção |
| Refrão | Ebmaj9 · Eb/G · Abmaj9 · Bb7sus4 · **Cm9** · Cm7/Bb · Abmaj7 · Bb7sus4 · Cm7 · Bb/D · Abmaj7 · Bb → Bb7sus4 | A cabeça "coi-sas" (Ré) vira 7ª maior/9ª: cor de gospel sem mudar a melodia |
| **Vamp (Mib)** | Abmaj9 · Bb(add9) · Fm11 · Gm7 → C9 · Abmaj9 → **A°7** · **Ebmaj7/Bb** → C9 · Fm11 → Bb7sus4 · **Gm9 → C7sus4** | Cada ciclo de 2 c. com uma cor nova (IV–#IV°–I/5, V/ii); modula pelo ii–V de Fá |
| **Vamp (Fá)** | Bbmaj9 · Am7 → D9 · Gm11 · Am7 → D9 · Bbmaj9 → **B°7** · Fmaj7/C → D9 · Gm11 → C7sus4 · Am7 → **Bbmaj7#11** | Mesmo desenho um tom acima, mais denso; o Mi da melodia vira #11 no último compasso |
| Preparação | **Ab/Bb → Bb/C** · C7sus4 | Acordes de barra subindo por tom até a dominante |
| **Refrão final (Fá)** | Fmaj9 · F/A → **Cm7** · Bbmaj9 · C7sus4 · Dm9 · Dm7/C → **F7/C** · Bbmaj7 · **A7#9** · Dm7 → Dm7/C · Bbmaj9 → Bbm6 · Am7 → **D7sus4** · Gm9 → C7sus4 | ii–V para o IV, V/vi antes do "Todos dirão", baixo descendo D–C–Bb–A–G |
| **Final (tags)** | F(add9) → **F7/Eb** · Bbmaj9/D · Gm9 → C7sus4 · F/A → **Ab°7** · Gm11 · C13 → C7sus4 · Dm9 → Dm7/C · Bbmaj9 → **Bbm6** · F/C → **Db9** · **F6/9** | Cada tag com uma cor nova; church ending com iv menor e bVI9 → I |

### Groove por seção

| Seção | Bateria | Baixo | Teclado | Órgão | Guitarra |
|---|---|---|---|---|---|
| Intro / Interlúdio / Refrões | Chimbal (aberto no contratempo), caixa 2 e 4, bumbo 1 · "e" do 2 · 3 · "e" do 4; crash a cada 4 c. | Linha ativa (oitava, quinta) com **antecipação** do próximo acorde no "e" do 4 | Comping sincopado com antecipação | Pad (Leslie rápido) | Acordes longos, antecipados |
| Parte 1 | Aro no 2 e 4, bumbo leve | Notas longas + antecipação | Pad leve | Pad suave | Entra só na 2ª metade: contratempos curtos |
| Parte 2 | Caixa no 2 e 4 | Mais movimento | Comping médio | Pad | Contratempos |
| Pré-refrão | Bumbo nos 4 tempos, caixa 2 e 4 | Colcheias na descida cromática | Colcheias curtas ("pumping") | Pad | Contratempos |
| Vamp (Mib) | c. 1–2 bumbo + chimbal → c. 3 + caixa → c. 5 groove; virada no fim | c. 1–2 só o 1 + antecipação, depois linha cheia | Colcheias curtas | Entra no 3º c. | Entra no 5º c. |
| Vamp (Fá) | Condução no ride, crash a cada 2 c. | Linha cheia | Colcheias | Pad | Comping sincopado |
| Preparação | Hits (1, "e" do 2, 4) + virada de 1 compasso | Hits | Hits | — | Hits |
| Final | Groove; na rit., meia pulsação (ride em semínimas, caixa no 3) e fermata | Mínimas → fermata | Mínimas → fermata | Pad → fermata | Mínimas → fermata |

Viradas em semicolcheias (caixa → tons) no 2º meio do último compasso de cada seção.

### Pontos para revisar (Etapa 2)
1. **Caixa no 2 e 4** em relação aos acordes (o guia do Moises tinha no 1 e 3): conferir a
   sensação com a gravação.
2. **Antecipações** do baixo e das teclas no "e" do 4: é a levada do guia; se ficar
   cheio demais com o coro, dá para manter só no baixo.
3. **Reharmonização** (aprovada em 14/10 e ampliada do vamp em diante). Toda nota da melodia
   foi conferida contra o acorde: as notas "fora" são tensões (9ª, 13ª, #11) ou suspensões da
   própria canção. Duas são de propósito no último tag: Lá sobre Bbm6 (7ª maior → 6ª, clichê
   do iv menor) e Sol sobre Db9 (#11).
4. **Teclado e órgão** estão escritos como guia (voicings fechados, padrão por seção); o
   tecladista pode e deve "abrir" e enfeitar. A guitarra está em notas reais (soa 8vb).
5. O lead sheet (Etapa 1) foi regerado com essas cifras.

## 9. Etapa 3: coro SATB

Arquivos: `grandes-coisas-coro.musicxml` (S, A, T, B com letra + piano com cifra) e `grandes-coisas-grade.musicxml`
(coro + Teclado, Órgão, Guitarra, Baixo, Bateria). Os dois foram validados contra o XSD oficial
do MusicXML 3.1. O Tenor usa clave de sol 8vb.

### Redução SATB (2 pautas)
`grandes-coisas-coro-reduzido.musicxml`: Mulheres (S haste para cima, A para baixo) e Homens
(T para cima, B para baixo), mais o piano de acompanhamento com a cifra gospel. A letra aparece uma vez quando as duas vozes cantam junto; quando
a voz de baixo canta outro texto/ritmo, ela vai para a 2ª linha (ou para a 1ª se a de cima
estiver calada).

### Versão simplificada (15/10)
Pedido do usuário: SATB, mas bem mais simples (o coro lê um pouco de partitura); Refrão 1 e
Refrão 2 iguais; dissonância só "aqui e ali".

- **Melodia sempre nas sopranos** (não troca mais de naipe; sem contracanto).
- **A, T e B sem melisma:** mudam de nota só na sílaba; nos enfeites da melodia ("coi-sas",
  "mim") seguram a nota. O baixo só troca de nota quando o acorde muda.
- **Vozes "paradas":** repetir a nota é a escolha preferida; quando mudam, é por passo curto.
- **Tríade como regra:** A e T cantam fundamental/3ª/5ª; tensões (7ª, 9ª) só na nota longa de
  "coi-sas" no início das frases do refrão e no acorde final (F6/9).
- **Refrão 2 (as duas vezes) = cópia exata do Refrão 1** (só o último "mim" da 2ª vez é curto,
  porque o vamp entra no tempo 1).
- Nota que atravessa uma troca de acorde (antecipações) usa o acorde que soa por mais tempo e,
  se possível, uma nota comum aos dois.

### Texturas

| Seção | S | A | T | B |
|---|---|---|---|---|
| Intro / Interlúdio | — (seguram o "mim" do refrão) | | | |
| Parte 1 | melodia | melodia (uníssono) | "Oh" nos finais de verso | "Oh" |
| Pré-refrão 1 | melodia | abaixo | abaixo | entra em "Eu vou cantar" |
| Refrões 1 e 2 / Pré 2 | melodia | abaixo | abaixo | fundamental |
| Parte 2 | "Ooh" (pad) | "Ooh" (pad) | melodia 8vb | melodia (uníssono com T) |
| Vamp (Mib) c. 1–2 | — | — | melodia 8vb | melodia 15ma abaixo (oitavas com T) |
| Vamp c. 3–4 | melodia | melodia (uníssono) | idem | idem |
| Vamp c. 5–8 / Vamp (Fá) / Refrão final / Final | melodia | abaixo | abaixo | fundamental |
| "To-dos di-rão," / "to-dos di-rão" | mulheres chamam (S melodia, A abaixo) | | homens respondem (T melodia 8vb, B abaixo) | |

Extensões (altura real): **S** Dó4–Fá5 (Fá5 só curto) · **A** Lá3–Ré5 · **T** Dó3–Fá4 · **B** Sol2–Sib3.

### Pontos para revisar (Etapa 3)
1. **Respostas da Parte 1** e pads da Parte 2 estão em "Oh"/"Ooh" (sem inventar letra).
2. **Vamp:** tenores e baixos em oitavas no início (baixos uma oitava abaixo dos tenores).
3. Se ainda pesar no ensaio, o próximo passo de simplificação é juntar T+B em uníssono
   nos refrões (o coro fica a 3 vozes nesses trechos).
