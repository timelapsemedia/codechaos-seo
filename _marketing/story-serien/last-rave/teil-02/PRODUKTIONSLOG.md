# LAST RAVE Teil 2 – Produktionslog

Skript: Tim (08.11.2026, deutsche Fassung). Hook-Variante A. 210 BPM.

## 25.11.2026 (Routine story-serien; Lauf 1 startete den Kaggle-Stapel und brach 08:16 am Limit ab, Lauf 2 übernahm)
- Bilder: 19 auf Kaggle (Qwen-Image-Edit + Lightning 8 Schritte, 2x T4, 5351 s, 0 $). In voller Größe/Kontaktbogen und Ecken (Signaturen) geprüft.
  - Neu: a03 (Fantasieschrift auf dem Messgerät, Szene draußen) -> Display nur Balkenanzeige, Schlafzimmer. a04 (Apple-Logo, Laptop nicht versteckt) -> 2 Versuche, jetzt ohne sichtbaren Laptop (Versteck erzählt der Sprechertext). a10 (zugeklappter Laptop auf der Straße) -> 3 Versuche zeigten zwei Laptops; lokal auf den einen aufgeklappten Laptop beschnitten (Original bilder_v3/a10.png). Alle 0 $, kein --voll.
- Overlays (1080×1920, aus Bildpixel × 1,40625 gemessen): a01 „200+“ im Display, a06 „140“→„143“, a14 „LAST_RAVE.wav“ im Dateifenster, a17 „53.54 / 9.97“.
- Sound: Kick+Bass Engine, Programm „Hitech Gallop 200“, Grundton E1, 210 BPM (Renderer kickbass_rolling, 08.11.); Sound-Moment a16 −12,6 LUFS gemessen.
- Stimme: ElevenLabs (Serienstimme aus serien.json), 18 Zeilen, 49,4 s.
- Werkzeug: folge_build.py Cache nach Zeitstempel, Ausklang am Ende, --nur-audio schreibt keine props mehr (erster Nur-Ton-Lauf hatte das Video zerstört, sofort neu gebaut).
- Render: 63,1 s, −14,1 LUFS, True Peak −1,3 dBTP. Endkontrolle begründet freigegeben (E:/story-serien/last-rave/final/last-rave_teil-02_A.freigabe.md).
