# Grandes Coisas (Ministério Atitude): versão coro + orquestra, linha Pop/Black/Soul

Status: **Etapa 0, análise da fonte e proposta de estrutura.** Aguardando as decisões da § 5.

Referências de estilo: `docs/estilo-gospel-soul.md` (groove, coro, harmonia, vamp) +
`docs/estilo-orquestracao.md` (escrita da orquestra, dobras e substituições).
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
| Melodia Voz | Melodia do solista | Base da Etapa 1 (lead sheet) |
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

- **Coro S-A-T-B (B opcional) + solista** na frente; banda gospel (bateria, baixo, Hammond, piano/Rhodes,
  guitarra) como motor; **horn section** (Tpts, Saxes, Tbns) com hits e riff original;
  **cordas e madeiras** como camada "cinema" (pads, runs, brilho).
- O material da canção já tem três ganchos fortes para o estilo:
  1. **O baixo cromático do pré** (E–D#–D–C#): dá para uma linha de cordas/trombones e
     para reharmonizar com dominantes de passagem (E7 – B7/D# …).
  2. **"Eu vou cantar, eu vou celebrar"**: frase curta e rítmica, ideal para o **vamp** com
     camadas de coro, call-and-response e modulações.
  3. **"Todos dirão, todos dirão"**: chamada e resposta natural (solista chama, coro responde).
- **Riff original de metais** para a Intro/Interlúdio/Final, criado a partir da rítmica
  sincopada de "Grandes coisas o Senhor já fez por mim" (não copiar a melodia: só a célula
  rítmica e o contorno geral).

## 3. Estrutura proposta (rascunho para discussão)

Durações em ciclos de acordes; os compassos exatos saem na Etapa 1.

| # | Seção | Tom | Coro / solista | Banda + orquestra | Din. |
|---|---|---|---|---|---|
| 1 | **Intro** | G | — (ou "oohs" do coro no fim) | Riff original de metais sobre G – C – D/F# – C, hits com a bateria; cordas em pad | **f** |
| 2 | **Parte 1** | G | **Solista** | Banda enxuta (bateria *pocket*, baixo, Rhodes); Hammond em pad; cordas *pp* | mp |
| 3 | **Pré 1** | G | **Coro feminino em uníssono** entra | Cordas descem com o baixo cromático; cresc. | mp → mf |
| 4 | **Refrão 1** | G | **Coro S-A-T(B)** em bloco | Metais respondem nos respiros; pandeirola | mf/f |
| 5 | **Interlúdio** | G | — | Riff dos metais (versão curta) | f |
| 6 | **Parte 2** | G | **Coro em uníssono** na melodia + solista *ad lib* | Saxes em contracanto suave; cordas "oohs" | mf |
| 7 | **Pré 2** | G | **Coro em 2–3 vozes** | Tutti cresc.; run de cordas no fim | mf → f |
| 8 | **Refrão 2 ×2** | G | Coro S-A-T; 2ª vez com solista por cima | Tutti; metais em bloco | f |
| 9 | **Breakdown → Vamp** "Eu vou cantar, eu vou celebrar" | G → **Ab** → **A** | Camadas: S → +A → +T; solista chama | Começa com bateria + baixo + palmas; entra o órgão, depois metais e cordas; **2 modulações de meio tom** | p → ff |
| 10 | **"Todos dirão" + Refrão final** | **A** | Call-and-response, depois S-A-T no agudo | *Shout chorus* dos metais, madeiras 8va | **ff** |
| 11 | **Final** | A | Tag "Que grandes coisas Deus já fez por mim" ×3 (a última em rit.) | *Church ending* (IV – iv6 – I/V…) com fermata + hit | ff |

## 4. Etapas de trabalho

| Etapa | Entrega | Formato |
|---|---|---|
| **0. Análise + estrutura** | Este documento + memória de estilo gospel | `.md` (**feito**) |
| **1. Lead sheet limpo** | Melodia corrigida (o Moises tem ruído e deslocamentos), cifra e letra, no tom e andamento definidos, já na forma nova (vamp, modulações) | MusicXML + PDF de prévia |
| **2. Seção rítmica + harmonia gospel** | Reharmonização por seção, linha de baixo, groove de bateria por seção, cifra do teclado | MusicXML (Rhythm, Baixo, Bateria, Piano) |
| **3. Coro** | Arranjo S-A-T-B (B opcional) com letra, respirações e cortes, seção por seção | MusicXML (pautas de coro + solista) |
| **4. Metais e saxes** | Riff da intro, hits, respostas, shout chorus | MusicXML (grade parcial) |
| **5. Cordas, madeiras e percussão** | Pads, runs, dobras, percussão por seção | Grade completa |
| **6. Revisão e partes** | Playback (Sibelius + NotePerformer), partes individuais, substituições, redução de cordas | MusicXML + partes |

Em cada etapa você ouve/revisa antes de seguirmos para a próxima.

## 5. Decisões pendentes (para fechar a Etapa 0)

1. ~~Andamento~~: **♩ = 150** (decidido).
2. **Tonalidade:** em discussão, ver § 6.
3. ~~Coro~~: **S-A-T-B** (decidido). O baixo é escrito para cantar, mas a música tem que fechar sem ele: nada de essencial só no baixo (S-A-T completam o acorde; o baixo dobra a fundamental ou faz respostas/ostinatos graves).
4. **Orquestra disponível:** formação completa (madeiras, saxes, metais, cordas) ou um grupo
   menor? Tem órgão/Hammond, guitarra e Rhodes na banda?
5. **Duração/forma:** manter a forma completa (≈ 5 min com o vamp) ou uma versão mais curta?

## 6. Tonalidade para o coro (opções em discussão)

### Extensão da melodia por seção (altura do guia, voz masculina)

| Seção | Extensão | Núcleo (80 % do tempo) | Nota média |
|---|---|---|---|
| Partes 1 e 2 (solista) | Mi3–Mi4 | Mi3–Ré4 | Lá3 |
| Pré-refrão | Lá3–**Lá4** | Lá3–Sol4 | Mib4 |
| Refrão | Fá#3–Sol4 | Sol3–Sol4 | Dó4 |
| Breakdown ("Eu vou cantar…") | Si3–Sol4 | Dó4–Sol4 | Mi4 |

O problema de Sol não é o refrão em si (Sol–Sol). O problema é que **não sobra espaço para
subir**: o pré chega a Lá4 (Lá5 nas sopranos), e qualquer modulação no vamp leva o coro para
Lá5/Si5. Além disso, os versos ficam graves para o solista se ele for homem e o tom baixar
muito. A decisão depende de **quem canta os versos** e de **para onde o vamp sobe**.

### Opções (melodia nas sopranos; o coro canta do pré em diante)

| Opção | Pré (pico) | Refrão (sopranos) | Versos (solista homem / mulher) | Orquestra | Comentário |
|---|---|---|---|---|---|
| **A. Fá → Sol** (recomendada) | Sol5 | Fá4–Fá5 | Ré3–Dó4 / Ré4–Dó5 | Ótima (Fá e Sol) | Começa 1 tom abaixo e **termina no tom original** no clímax. O vamp sobe Fá → Sol (1 tom) ou Fá → Fá# → Sol (meio tom duas vezes; Fá# fica pesado para a orquestra, mas dura poucos compassos) |
| **B. Mib → Fá (→ Sol)** | Fá5 | Mib4–Mib5 | Dó3–Sib3 (grave) / Dó4–Sib4 | Ótima para metais | Mais confortável para o coro e com mais espaço para subir 2×. Só funciona bem com **solista mulher** (ou homem barítono com versos reescritos) |
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
