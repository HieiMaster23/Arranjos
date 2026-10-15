#!/usr/bin/env bash
# Prévia de áudio (MP3) de um MusicXML: MusicXML -> MIDI -> FluidSynth (FluidR3_GM) -> MP3.
# Uso: ferramentas/previa_audio.sh entrada.musicxml saida.mp3 [opções do musicxml_midi.py]
# Requer: apt-get install fluidsynth fluid-soundfont-gm ffmpeg ; pip install mido
set -euo pipefail
src="$1"; out="$2"; shift 2
tmp="$(mktemp -d)"
python3 "$(dirname "$0")/musicxml_midi.py" "$src" "$tmp/previa.mid" "$@"
fluidsynth -ni -q -F "$tmp/previa.wav" -r 44100 -g 0.6 /usr/share/sounds/sf2/FluidR3_GM.sf2 "$tmp/previa.mid"
ffmpeg -y -loglevel error -i "$tmp/previa.wav" -af "loudnorm=I=-16:TP=-1.5" -codec:a libmp3lame -b:a 192k "$out"
rm -rf "$tmp"
echo "$out"
