#!/usr/bin/env python3
"""Liest eine Standard-MIDI-Datei ohne Zusatzbibliotheken und gibt JSON aus: Tempo, Taktart, Länge in Takten, Spuren, Noten, Tonumfang, Töne außerhalb einer Skala."""
import json, struct, sys

NOTEN = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MODI = {'ionisch': [0, 2, 4, 5, 7, 9, 11], 'dur': [0, 2, 4, 5, 7, 9, 11], 'aeolisch': [0, 2, 3, 5, 7, 8, 10], 'moll': [0, 2, 3, 5, 7, 8, 10],
        'phrygisch': [0, 1, 3, 5, 7, 8, 10], 'dorisch': [0, 2, 3, 5, 7, 9, 10], 'lydisch': [0, 2, 4, 6, 7, 9, 11], 'mixolydisch': [0, 2, 4, 5, 7, 9, 10],
        'lokrisch': [0, 1, 3, 5, 6, 8, 10], 'harmonisch_moll': [0, 2, 3, 5, 7, 8, 11], 'phrygisch_dominant': [0, 1, 4, 5, 7, 8, 10]}

def varlen(b, i):
    v = 0
    while True:
        c = b[i]; i += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, i

def main():
    path = sys.argv[1]
    skala = sys.argv[2] if len(sys.argv) > 2 else None
    b = open(path, 'rb').read()
    if b[:4] != b'MThd':
        print(json.dumps({'fehler': 'keine Standard-MIDI-Datei'})); return
    fmt, ntrk, div = struct.unpack('>HHH', b[8:14])
    i = 8 + struct.unpack('>I', b[4:8])[0]
    tempos, sigs, noten, spuren, max_tick = [], [], [], [], 0
    for t in range(ntrk):
        if b[i:i + 4] != b'MTrk': break
        ln = struct.unpack('>I', b[i + 4:i + 8])[0]; j = i + 8; end = j + ln; tick = 0; run = 0; name = None; count = 0
        while j < end:
            d, j = varlen(b, j); tick += d
            st = b[j]
            if st == 0xFF:
                typ = b[j + 1]; l, j2 = varlen(b, j + 2); data = b[j2:j2 + l]; j = j2 + l
                if typ == 0x51: tempos.append((tick, round(60_000_000 / int.from_bytes(data, 'big'), 3)))
                elif typ == 0x58: sigs.append((tick, f"{data[0]}/{2 ** data[1]}"))
                elif typ == 0x03: name = data.decode('latin-1', 'replace')
                continue
            if st in (0xF0, 0xF7):
                l, j2 = varlen(b, j + 1); j = j2 + l; continue
            if st & 0x80: run = st; j += 1
            hi = run & 0xF0
            n = 1 if hi in (0xC0, 0xD0) else 2
            data = b[j:j + n]; j += n
            if hi == 0x90 and len(data) == 2 and data[1] > 0:
                noten.append(data[0]); count += 1
        max_tick = max(max_tick, tick)
        spuren.append({'name': name, 'noten': count})
        i = end
    sig = sigs[0][1] if sigs else '4/4'
    zaehler, nenner = (int(x) for x in sig.split('/'))
    takt_ticks = div * 4 * zaehler / nenner if div < 0x8000 else None
    res = {'datei': path, 'format': fmt, 'ppq': div, 'tempi_bpm': sorted({t for _, t in tempos}) or ['keins gesetzt (Standard 120)'], 'taktart': sig,
           'takte': round(max_tick / takt_ticks, 2) if takt_ticks else None, 'spuren': spuren, 'noten_gesamt': len(noten)}
    if noten:
        res['tonumfang'] = f"{NOTEN[min(noten) % 12]}{min(noten) // 12 - 1} – {NOTEN[max(noten) % 12]}{max(noten) // 12 - 1}"
        haeuf = {}
        for n in noten: haeuf[NOTEN[n % 12]] = haeuf.get(NOTEN[n % 12], 0) + 1
        res['tonklassen'] = dict(sorted(haeuf.items(), key=lambda x: -x[1]))
    if skala and noten:
        teile = skala.lower().replace('-', ' ').split()
        root = NOTEN.index(teile[0].upper().replace('IS', '#')) if teile[0].upper().replace('IS', '#') in NOTEN else None
        modus = '_'.join(teile[1:]) if len(teile) > 1 else 'moll'
        if root is None or modus not in MODI:
            res['skala_fehler'] = f"Skala „{skala}“ unbekannt. Modi: {', '.join(MODI)}"
        else:
            erlaubt = {(root + s) % 12 for s in MODI[modus]}
            aus = [n for n in noten if n % 12 not in erlaubt]
            res['skala'] = skala
            res['ausserhalb_skala'] = {'anzahl': len(aus), 'prozent': round(100 * len(aus) / len(noten), 1), 'tonklassen': sorted({NOTEN[n % 12] for n in aus})}
    print(json.dumps(res, ensure_ascii=False))

try:
    main()
except Exception as ex:
    print(json.dumps({'fehler': f'{type(ex).__name__}: {ex}'}))
