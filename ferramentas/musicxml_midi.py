"""MusicXML (gerado por ferramentas/mxl.py) -> MIDI, para prévias de áudio rápidas.

Uso: python3 ferramentas/musicxml_midi.py entrada.musicxml saida.mid [--rit COMPASSO] [--vel PARTE=VEL ...]
     --rit N   : ritardando do compasso N até o fim (150 -> ~105) e fermata no último acorde
Requer: pip install mido

Lê: <divisions>, <pitch>/<unpitched>, <chord/>, <rest/>, <tie>, <backup>/<forward>,
<transpose> (altura real = escrita + chromatic), <midi-instrument> (canal, programa e
nota de percussão), <sound tempo>. Dinâmicas são ignoradas (volume fixo por parte).
Para renderizar em áudio: fluidsynth + ffmpeg (ver ferramentas/previa_audio.sh).
"""
import sys
import xml.etree.ElementTree as ET

import mido

STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
TPQ = 480


def parse(path):
    root = ET.parse(path).getroot()
    insts = {}  # id do instrumento -> (canal, programa, nota de percussão)
    names = {}
    for sp in root.iter("score-part"):
        pid = sp.get("id")
        names[pid] = sp.findtext("part-name")
        for mi in sp.iter("midi-instrument"):
            insts[mi.get("id")] = (int(mi.findtext("midi-channel") or 1) - 1,
                                   int(mi.findtext("midi-program") or 1) - 1,
                                   int(mi.findtext("midi-unpitched")) if mi.find("midi-unpitched") is not None else None)
    tempos = {}  # tempo absoluto (em semínimas) -> bpm
    bar_starts = []
    parts = {}
    for part in root.iter("part"):
        pid = part.get("id")
        div = 4
        trans = 0
        t = 0.0  # em semínimas
        notes = []
        open_ties = {}
        starts = []
        for meas in part.iter("measure"):
            starts.append(t)
            mstart = t
            last_start = t
            mlen = 0.0
            for el in meas:
                if el.tag == "attributes":
                    if el.findtext("divisions"):
                        div = int(el.findtext("divisions"))
                    tr = el.find("transpose")
                    if tr is not None:
                        trans = int(tr.findtext("chromatic") or 0) + 12 * int(tr.findtext("octave-change") or 0)
                elif el.tag == "direction":
                    snd = el.find("sound")
                    if snd is not None and snd.get("tempo"):
                        tempos[t] = float(snd.get("tempo"))
                elif el.tag == "backup":
                    t -= int(el.findtext("duration")) / div
                elif el.tag == "forward":
                    t += int(el.findtext("duration")) / div
                elif el.tag == "note":
                    dur = int(el.findtext("duration") or 0) / div
                    is_chord = el.find("chord") is not None
                    st = last_start if is_chord else t
                    if not is_chord:
                        last_start = t
                    fermata = el.find("notations/fermata") is not None
                    if el.find("rest") is None:
                        inst = el.find("instrument")
                        key = None
                        if el.find("pitch") is not None:
                            p = el.find("pitch")
                            key = 12 * (int(p.findtext("octave")) + 1) + STEP[p.findtext("step")] + int(float(p.findtext("alter") or 0)) + trans
                            ch = None
                        else:
                            iid = inst.get("id") if inst is not None else None
                            ch, _prog, key = insts.get(iid, (9, 0, 38))
                        ties = [x.get("type") for x in el.findall("tie")]
                        tk = (key, ch)
                        if "stop" in ties and tk in open_ties:
                            n = open_ties.pop(tk)
                            n["dur"] = st + dur - n["start"]
                            n["fermata"] |= fermata
                            if "start" in ties:
                                open_ties[tk] = n
                        else:
                            n = {"start": st, "dur": dur, "key": key, "ch": ch, "fermata": fermata}
                            notes.append(n)
                            if "start" in ties:
                                open_ties[tk] = n
                    if not is_chord:
                        t += dur
                mlen = max(mlen, t - mstart)
            t = mstart + mlen
        parts[pid] = notes
        bar_starts = bar_starts or starts
    return names, insts, parts, tempos, bar_starts


def write_midi(path_in, path_out, rit_bar=None, vel=None):
    names, insts, parts, tempos, bars = parse(path_in)
    vel = vel or {}
    mid = mido.MidiFile(ticks_per_beat=TPQ)
    meta = mido.MidiTrack()
    mid.tracks.append(meta)
    # mapa de andamento (+ ritardando opcional)
    tmap = dict(tempos) or {0.0: 120.0}
    base = tmap[min(tmap)]
    end = max((n["start"] + n["dur"]) for ns in parts.values() for n in ns)
    if rit_bar:
        r0 = bars[rit_bar - 1]
        steps = 12
        for k in range(steps + 1):
            tmap[r0 + (end - r0) * k / steps] = base * (1 - 0.3 * k / steps)
    last = 0
    for tq in sorted(tmap):
        tick = int(round(tq * TPQ))
        meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tmap[tq]), time=tick - last))
        last = tick
    used = set()
    for pid, notes in parts.items():
        inst = next((v for k, v in insts.items() if k.startswith(pid + "-")), (0, 0, None))
        drums = all(n["ch"] is not None for n in notes) and notes
        ch = 9 if drums else inst[0]
        while not drums and ch in used | {9}:
            ch = (ch + 1) % 16
        used.add(ch)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        tr.append(mido.MetaMessage("track_name", name=names[pid]))
        if not drums:
            tr.append(mido.Message("program_change", channel=ch, program=inst[1]))
        v = vel.get(names[pid], 90)
        evs = []
        for n in notes:
            d = n["dur"] * (2.5 if n["fermata"] else 1.0)
            if drums:
                d = max(0.1, min(d, 0.5))
            on = int(round(n["start"] * TPQ))
            off = int(round((n["start"] + d) * TPQ)) - 4
            evs.append((on, 1, mido.Message("note_on", channel=ch, note=n["key"], velocity=v)))
            evs.append((max(off, on + 1), 0, mido.Message("note_off", channel=ch, note=n["key"], velocity=0)))
        evs.sort(key=lambda e: (e[0], e[1]))
        last = 0
        for tick, _o, msg in evs:
            tr.append(msg.copy(time=tick - last))
            last = tick
    mid.save(path_out)
    return len(parts)


if __name__ == "__main__":
    args = sys.argv[1:]
    rit = None
    vel = {}
    if "--rit" in args:
        i = args.index("--rit")
        rit = int(args[i + 1])
        del args[i:i + 2]
    while "--vel" in args:
        i = args.index("--vel")
        k, v = args[i + 1].rsplit("=", 1)
        vel[k] = int(v)
        del args[i:i + 2]
    n = write_midi(args[0], args[1], rit, vel)
    print(f"{args[1]}: {n} partes")
