# Arranjos

Repositório de arranjos e orquestrações próprios (louvor/worship para orquestra de igreja).

## Memória de estilo

Antes de criar ou revisar qualquer arranjo, leia `docs/estilo-orquestracao.md`. Ele resume a
forma, a textura, o papel de cada naipe, as modulações e o checklist do estilo de referência.
Para arranjos de linha Pop/Black/Soul gospel (coro + banda + orquestra), leia também
`docs/estilo-gospel-soul.md` (groove, coro S-A-T, reharmonização, vamp e modulações).

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
