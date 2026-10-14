# Arranjos

Repositório de arranjos e orquestrações próprios (louvor/worship para orquestra de igreja).

## Memória de estilo

Cada arranjo é um **projeto musicalmente independente** na sua pasta em `arranjos/`: conceito,
estilo, material temático e decisões de um não se aplicam ao outro. O que é compartilhado é só
a parte técnica em `ferramentas/` (escritor de MusicXML `mxl.py`, prévia em PDF `previa_pdf.py`,
estrutura de grade). Não regere nem altere arquivos de outro projeto.

- Arranjos orquestrais "Camp" (ex.: `uma-carta-viva`): leia `docs/estilo-orquestracao.md`
  (forma, textura, papel de cada naipe, modulações e checklist).
- Arranjos Pop/Black/Soul gospel (ex.: `grandes-coisas`, coro SATB + banda + metais): leia
  `docs/estilo-gospel-soul.md` (groove, coro, reharmonização, vamp e modulações).

Regras:
- As obras de referência têm **direitos autorais**. Siga apenas as ideias gerais e as técnicas;
  **nunca copie** melodias, contracantos, voicings ou fills específicos delas.
- Todo material temático (motivos, fills, contracantos) deve ser **original**, derivado da
  canção que está sendo arranjada.
- Escreva pensando em orquestra de igreja: linhas importantes dobradas, partes de
  substituição, tessituras confortáveis e respeito ao espaço da voz.

## Playback (Sibelius + NotePerformer 5)

- Bateria padrão: **Drum Set (Sticks, Rock)** do NotePerformer 5. Em `ferramentas/mxl.py` a
  tabela `KIT` usa as notas desse mapa (= General MIDI: bumbo 36, caixa 38, aro 37, chimbal 42/44/46,
  crash 49, ride 51, tons 50/47/43). O Sibelius lê `<midi-unpitched>` como a **nota exata**:
  não somar +1, porque isso desloca todas as peças.
- Todo instrumento leva `<instrument-sound>` (ids do `sounds.xml` do MusicXML) para o Sibelius
  escolher o som certo na importação.
