---
name: comsar
description: Musikaufnahmen wissenschaftlich analysieren mit comsar (Rolf Bader / Michael Blaß, Uni Hamburg, Codeberg rbader/comsar). Tonhöhenverlauf (YIN), Melodie als Notenliste, Tonsystem/Skala gegen 900+ Skalen, melodische n-Gramme, Timbre-Track (Spectral Centroid/Spread/Flux, Rauigkeit nach Helmholtz/Bader und Sethares, Schärfe, SPL, Korrelationsdimension), optional Gesang abtrennen. Nutzen bei "analysiere den Track/die Aufnahme", "welche Tonleiter/Skala", "Melodie extrahieren", "Tonhöhe/Pitch-Track", "wie rau/scharf klingt das", "Timbre vergleichen", "Bounce-Klangfarbe über die Zeit", Ethno-/Archivaufnahmen, Mix-Vergleiche über Merkmale.
---

# comsar – Musik- und Klanganalyse

Quelle: https://codeberg.org/rbader/comsar (BSD-3-Clause). Import-Name `comsar`, baut auf `apollon` und `chainsaddiction` auf.

## Installation (PC und Cloud gleich)
Vor der ersten Nutzung prüfen und nur bei Bedarf installieren:
```bash
python3 -c "import comsar" 2>/dev/null || pip install "git+https://codeberg.org/rbader/comsar.git"
```
- Windows: `py -3 -m pip install "git+https://codeberg.org/rbader/comsar.git"` (braucht Git; ohne Git: `py -3 -m pip install bader-comsar`, Stand PyPI ggf. eine Version älter).
- Python 3.9–3.13. Fertige Wheels für apollon/chainsaddiction, kein C-Compiler nötig.
- Gesangstrennung nur bei Bedarf: `pip install "bader-comsar[separation-light]"` (Modell `mdxnet`, ~1,7 GB RAM) oder `[separation]` (Mel-Band-RoFormer, PyTorch). Die Modellgewichte haben laut Autoren keine angegebene Lizenz: nur für Analyse, nicht in Produkte packen.

## Grundgerüst (geprüft mit comsar 0.0.16)
```python
import warnings; warnings.filterwarnings("ignore")
from comsar import PitchTrack, TimbreTrack

pr = PitchTrack().extract("track.wav")      # Spalten Pitch (Hz), SPL; Index time_s
notes = PitchTrack().notes(pr)              # start_s, stop_s, duration_s, frequency, cent, midi
ts = PitchTrack().tonal_system(pr)          # ts.best["name"], ts.best["correlation"], ts.scales (Top 10)
grams = PitchTrack().ngrams(pr, ngram=3, nngram=10)   # häufigste Intervallfolgen in Cent

tt = TimbreTrack().extract("track.wav")     # ein Fenster = 743 ms, 50 % Überlappung
tt.features.to_csv("timbre.csv")
```
Spalten von `tt.features`: SpectralCentroid, SpectralSpread, SpectralFlux, Roughness, Sharpness, SPL,
CorrelationDimension, RoughnessBader/Helmholtz, RoughnessSethares.
`extract()` nimmt auch `(numpy_array, sample_rate, "name")`. Ausgaben auf stdout ("Pitch ... 0.27 s.") sind nur Laufzeiten.

## Parameter, die man für Tims Musik meist ändert
- `PitchTrack(f_min=60, f_max=1200, window_ms=50, overlap=0.8)`: für Basslines `f_min=30, f_max=300`; für schnelle Hitech-Leads kürzere Fenster (`window_ms=25, overlap=0.6`).
- `PitchTrack(source="vocals")` trennt vorher den Gesang ab (Extra-Paket, s. o.).
- `TimbreTrack(window_ms=...)`: kürzere Fenster (z. B. 200 ms) für Drops und Breaks, Standard 743 ms für ganze Tracks. `wavelet_roughness=False` spart Zeit.
- Die Korrelationsdimension ist der langsamste Teil (ca. 12 s für 35 s Audio).

## So berichten
- Werte immer mit Einheit und Zeitbereich nennen, keine Klangurteile ohne Messung.
- Tonsystem: Name der besten Skala plus Korrelation und die nächsten 2–3 Kandidaten (`ts.scales.head(3)`); bei Korrelation unter ~0,7 als unsicher bezeichnen. Haben mehrere Skalen exakt dieselbe Korrelation (häufig bei 12TET-Varianten), sind sie gleichwertig: alle nennen, keine als "die" Skala ausgeben.
- Bei elektronischer Musik ist das Tonsystem oft "12TET"-Varianten; Skalennamen aus scales.csv sind Theorie-Kandidaten, kein Genre-Urteil.
- Vergleiche zwischen Bounces: dieselben Parameter und dieselbe Abtastrate benutzen, Mittelwert und Spannweite je Merkmal als Tabelle.
- Für Hörurteile zusätzlich `earshot` oder audio-labor (`messen`, `vergleichen`) nutzen; comsar liefert Merkmale, kein Mastering-Urteil.
