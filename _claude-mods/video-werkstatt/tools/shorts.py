#!/usr/bin/env python3
"""Werkzeuge für Hochkant-Shorts. Gibt JSON aus.

shorts.py standbilder <video> <ausgabe_ordner> <zeiten,komma> [9:16]
shorts.py untertitel <quelle.srt|.json> <ausgabe.ass> <breite> <hoehe> <max_zeichen> <schrift> <groesse> <keywords,komma> <position>
shorts.py einbrennen <video> <untertitel.ass> <ausgabe.mp4>
shorts.py transkribieren <datei> <sprache> <modell> <ausgabe.json>
"""
import json, os, re, shutil, subprocess, sys

def out(d):
    print(json.dumps(d, ensure_ascii=False))

def ts_srt(s):
    m = re.match(r"(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})", s.strip())
    return (int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3))) + int(m.group(4).ljust(3, "0")) / 1000

def ts_ass(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def lese_woerter(quelle):
    """Wörter mit Zeiten: aus Whisper-JSON (word timestamps) exakt, aus SRT proportional zur Zeichenzahl (Näherung)."""
    if quelle.lower().endswith(".json"):
        d = json.load(open(quelle, encoding="utf-8"))
        segs = d.get("segments", d) if isinstance(d, dict) else d
        w = []
        for s in segs:
            for x in s.get("words", []) or []:
                w.append((x["word"].strip(), float(x["start"]), float(x["end"])))
        return w, "exakt (Wort-Zeitstempel)"
    text = open(quelle, encoding="utf-8-sig").read().replace("\r", "")
    w = []
    for b in re.split(r"\n{2,}", text):
        lines = b.strip().split("\n")
        ti = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if ti is None: continue
        a, z = lines[ti].split("-->")
        s, e = ts_srt(a), ts_srt(z.strip().split()[0])
        words = " ".join(lines[ti + 1:]).split()
        total = sum(len(x) + 1 for x in words) or 1
        t = s
        for x in words:
            d = (e - s) * (len(x) + 1) / total
            w.append((x, t, t + d)); t += d
    return w, "geschätzt (aus SRT-Cues verteilt)"

def gruppen(woerter, max_zeichen):
    g, cur = [], []
    for wd in woerter:
        kand = " ".join([x[0] for x in cur] + [wd[0]])
        if cur and (len(kand) > max_zeichen or wd[1] - cur[-1][2] > 0.6 or re.search(r"[.!?]$", cur[-1][0])):
            g.append(cur); cur = []
        cur.append(wd)
    if cur: g.append(cur)
    return g

def untertitel(quelle, ziel, breite, hoehe, max_zeichen, schrift, groesse, keywords, position):
    woerter, genauigkeit = lese_woerter(quelle)
    if not woerter:
        return {"fehler": "keine Wörter in der Quelle"}
    kw = {k.strip().lower() for k in keywords.split(",") if k.strip()}
    # Reels/TikTok: unten ca. 20 % UI (Beschreibung, Buttons), oben ca. 14 %; „mitte“ setzt die Zeile auf ca. 62 % Höhe.
    margin_v = int(hoehe * (0.38 if position == "mitte" else 0.24))
    seiten = int(breite * 0.08)
    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {breite}
PlayResY: {hoehe}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Short,{schrift},{groesse},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,{max(3, groesse // 12)},2,2,{seiten},{seiten},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    zeilen, laengste = [], 0
    for g in gruppen(woerter, max_zeichen):
        txt = " ".join(r"{\c&H00D7FF&}" + w[0] + r"{\c&HFFFFFF&}" if re.sub(r"\W", "", w[0].lower()) in kw else w[0] for w in g)
        laengste = max(laengste, len(" ".join(w[0] for w in g)))
        zeilen.append(f"Dialogue: 0,{ts_ass(g[0][1])},{ts_ass(g[-1][2])},Short,,0,0,0,,{txt}")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(kopf + "\n".join(zeilen) + "\n")
    # Breite grob prüfen: durchschnittliche Zeichenbreite ca. 0,55 × Schriftgröße
    zu_breit = laengste * groesse * 0.55 > breite - 2 * seiten
    return {"ass": ziel, "einblendungen": len(zeilen), "zeiten": genauigkeit, "laengste_zeile_zeichen": laengste,
            "safe_area": {"unterer_rand_px": margin_v, "seitenrand_px": seiten},
            "warnung": "längste Zeile könnte breiter als der sichere Bereich sein – max_zeichen oder Schriftgröße senken" if zu_breit else None}

def standbilder(video, ordner, zeiten, guides):
    os.makedirs(ordner, exist_ok=True)
    dateien = []
    for t in [float(x) for x in zeiten.split(",") if x.strip()]:
        ziel = os.path.join(ordner, f"standbild_{t:07.2f}s.png".replace(" ", "0"))
        vf = "null"
        if guides:
            # Rote Linien: oberer UI-Bereich (14 %), unterer UI-Bereich (20 %), Seitenränder (6 %)
            vf = ("drawbox=x=0:y=ih*0.14:w=iw:h=3:color=red@0.9:t=fill,drawbox=x=0:y=ih*0.80:w=iw:h=3:color=red@0.9:t=fill,"
                  "drawbox=x=iw*0.06:y=0:w=3:h=ih:color=red@0.9:t=fill,drawbox=x=iw*0.94:y=0:w=3:h=ih:color=red@0.9:t=fill")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", vf, ziel], capture_output=True, text=True)
        dateien.append(ziel if r.returncode == 0 and os.path.exists(ziel) else f"Fehler bei {t}s: {r.stderr.strip()[:150]}")
    return {"standbilder": dateien, "hinweis": "Mit Read ansehen; rote Linien = sicherer Bereich für Reels/TikTok/Shorts" if guides else None}

def einbrennen(video, ass, ziel):
    pfad = ass.replace("\\", "/").replace(":", "\\:").replace("'", r"\'")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"ass='{pfad}'", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", ziel], capture_output=True, text=True)
    return {"ausgabe": ziel} if r.returncode == 0 else {"fehler": r.stderr.strip()[-600:]}

def transkribieren(datei, sprache, modell, ziel):
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(modell, compute_type="int8")
        segs, info = m.transcribe(datei, language=sprache, word_timestamps=True, vad_filter=True)
        data = {"segments": [{"start": s.start, "end": s.end, "text": s.text, "words": [{"word": w.word, "start": w.start, "end": w.end} for w in (s.words or [])]} for s in segs]}
        json.dump(data, open(ziel, "w", encoding="utf-8"), ensure_ascii=False)
        return {"json": ziel, "engine": "faster-whisper", "segmente": len(data["segments"])}
    except ImportError:
        pass
    if shutil.which("whisper"):
        od = os.path.dirname(os.path.abspath(ziel))
        r = subprocess.run(["whisper", datei, "--language", sprache, "--model", modell, "--word_timestamps", "True", "--output_format", "json", "--output_dir", od], capture_output=True, text=True)
        if r.returncode == 0:
            erzeugt = os.path.join(od, os.path.splitext(os.path.basename(datei))[0] + ".json")
            if erzeugt != os.path.abspath(ziel): shutil.move(erzeugt, ziel)
            return {"json": ziel, "engine": "openai-whisper"}
        return {"fehler": r.stderr.strip()[-400:]}
    return {"fehler": "Kein Whisper installiert. Installieren: python -m pip install faster-whisper (oder openai-whisper)."}

def main():
    a = sys.argv[1:]
    if not a: return out({"fehler": "Befehl fehlt"})
    if a[0] == "standbilder": return out(standbilder(a[1], a[2], a[3], len(a) > 4 and a[4] == "9:16"))
    if a[0] == "untertitel": return out(untertitel(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), a[6], int(a[7]), a[8], a[9]))
    if a[0] == "einbrennen": return out(einbrennen(a[1], a[2], a[3]))
    if a[0] == "transkribieren": return out(transkribieren(a[1], a[2], a[3], a[4]))
    out({"fehler": f"unbekannt: {a[0]}"})

try:
    main()
except Exception as ex:
    out({"fehler": f"{type(ex).__name__}: {ex}"})
