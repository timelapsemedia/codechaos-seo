---
name: lostplace-hdr
description: Urbex-/Lost-Place-HDR-Look für Videos und Fotos (Tim, 2026-10-20: global Pflicht für Lost-Place-Videos). Kräftiger lokaler Kontrast und Mikrostruktur, Schatten mit Zeichnung, keine grauen Lichter, satte Farben – zeitlich stabil (kein Flackern, keine Halos, kein Rauschen/Banding). Nutzen bei jedem Lost-Place-, Urbex-, Ruinen- oder Verfall-Video/-Foto, bei „HDR-Look“, „knackiges HDR“, „wie die großen Lost-Place-Kanäle“, Thumbnails solcher Videos und bei Fragen zur Aufnahme (Osmo Pocket 3, D-Log M, HLG).
---

# Lost-Place-HDR (Urbex-Look)

Gilt für jedes Lost-Place-Video (Tim, 2026-10-20). Ziel: Look der großen Urbex-Fotografen/-Kanäle (Referenz: Scholzdigital-Stil
– Treppenhaus/Gefängnis, Rundbau mit Wendeltreppe; Thumbnail-Stil „ES IST ALLES NOCH DA“), aber **als Video sauber**.

## Was „gut“ ist – und was „überzogen“
| gut | überzogen (vermeiden) |
|---|---|
| Mikrostruktur in Putz, Holz, Rost, Moos tritt hervor | Halos an Fensterrahmen/Horizont |
| Schatten mit Zeichnung, aber dunkel; echte Licht-/Schattenzonen | alles gleich hell, flach-grau („HDR-Brei“) |
| Fenster/Himmel weiß oder mit Zeichnung, nicht grau | graue, schmutzige Lichter/Himmel |
| kräftige, aber glaubwürdige Farben (Graffiti, Herbstlaub) | „nukleare“ Farben, Farbrauschen in Schatten |
| ruhiges Bild über die ganze Einstellung | Pumpen/Flackern von Helligkeit oder Struktur |
| Haut natürlich | Haut grau-körnig, überschärft |

## Material zuerst
- 8-bit H.264 BT.709 (Osmo Pocket 3 „Normal“ 8 bit) hat wenig Reserve: lokales Tonemapping aus **einer** Belichtung, Lichter sind
  geclippt und nicht rettbar → sauber weiß lassen.
- **Für künftige Drehs (Tim empfehlen):** Pocket 3 auf **10-bit H.265** (geht auch im Normal-Profil); besser **D-Log M 10-bit**
  (bis ~12,7 Blenden lt. DJI). Belichtung + Weißabgleich in M sperren (kein Auto-Pumpen beim Gehen hell↔dunkel),
  ISO niedrig, 1/48 s bei 23,976 fps (außen ND). Schlüsselräume vom Stativ zusätzlich −2 EV und +1 EV drehen → echte
  Mertens-Fusion möglich.
- HDR10/HLG-Upload lohnt nur mit Log/HLG-Material. Aus 8-bit SDR: **HDR-Look in SDR Rec.709** ausliefern.

## Verarbeitungskette (Video, 8-bit SDR → Urbex-HDR)
Umsetzung: `C:/zeitsprung-pipeline/zs/urbex_hdr.py` (torch/GPU), Stufe **nach** Grade + bisherigem Tonemapping, gleich für echte
Clips und fertige Einschübe (KI-Zeitreisen, Postkarten). Alles in float, keine 8-bit-Zwischenstufen.
1. **Entrauschen vor jedem Kontrast** (zeitlich, schonend; DJI entrauscht intern schon – mehr macht Haut wachsig).
2. **Clip-/Lichtmaske:** Kanal ≥ 250/255 bzw. L > 0,9 → Detailgewinn → 0 („Smooth Highlights“, keine grauen Fenster).
3. **Mehrskalen-Zerlegung auf log-Luminanz** mit **Guided Filter** (kein Bilateral: Gradientenumkehr/Banding):
   fein r≈2–4 px (4K) Gewinn 1,2–1,5 · mittel r≈16–32 px Gewinn 1,4–2,0 („Structure/Grunge“) · grob r≈1–3 % Breite Basis,
   log-Kompression β 0,6–0,8 (Schatten heben). Alternativ Fast Local Laplacian (σr 0,1–0,2, α 0,5–0,75, β 0,6–0,8).
4. **Schutzgewichte:** Lichter `1−smoothstep(0,75;0,95;L)`; tiefe Schatten: Gewinn senken, wo Signal < 2–3·σRauschen;
   |Detail| ≤ 0,3–0,5 Blenden (gegen Halos).
5. **Globale Tonkurve:** leichte S-Kurve, **tiefer Schwarzpunkt** (Schatten dunkel mit Zeichnung). Kurvenparameter **pro
   Einstellung konstant** (Szenengrenzen), nie pro Bild aus Statistik; wenn doch: EMA nur über Vergangenheit, α 0,03–0,1.
6. **Farbe:** Chroma aus Luminanzverhältnis `C_out=(C_in/L_in)^s·L_out`, s 0,6–0,8; **Vibrance** +10–25 % (gewichtet auf
   wenig gesättigte Pixel); Sättigung in tiefen Schatten und Lichtern zurück.
7. **Haut:** Hautmaske (Hue ~0–50°) → Detail fein/mittel ×0,5, Sättigung ≤ +5 %, Farbtonverschiebung < 3°; Gesichter Dritter
   werden ohnehin verpixelt (Mosaik).
8. **Himmel/Fenster:** Halos entstehen dort zuerst → mittlere Skala sanft, Mikroglättung hoch.
9. **Vignette:** Ecken −0,2…−0,4 EV, Abfall ab ~55 % Radius, konstant (in der ZeitSprung-Pipeline macht das der Endpass).
10. **Ausgabe:** 10-bit HEVC (gegen Banding in Verläufen), Dither beim letzten Schritt, **kein Korn**.

## Gate (messen, nicht schätzen) – `C:/zeitsprung-pipeline/tools/hdr_messung.py`
| Kriterium | Ziel (Startwerte, an Referenzen kalibrieren) |
|---|---|
| geclippte Lichter (Kanal ≥ 254) Ausgabe vs Quelle | darf nicht steigen, < 1–2 % |
| abgesoffene Schatten (Luma ≤ 2) | < 1 % |
| Luma P5 / P50 | P5 ≈ 0,03–0,08 · P50 ≈ 0,35–0,45 |
| lokaler RMS-Kontrast (64-px-Kacheln) Ausgabe/Quelle | 1,3–1,8× |
| Halo: Gradientenumkehr an starken Kanten | < 0,5 % |
| Rauschen dunkle Flächen (Hochpass-std) Ausgabe/Quelle | < 1,3× |
| zeitlich global: Frame-zu-Frame-ΔmeanY minus Quelle (std) | ≈ 0, keine Spitzen in einer Einstellung |
| zeitlich lokal: Kachel-Inkohärenz 1−max(0,ρ), P95 | < 0,1 |
| Chroma C* Mittel/P95, Farbclipping | moderat ↑, Clipping < 0,5 % |
| Haut ΔHue | < 3° |
| **Flecken** in Flächen, die in der Quelle ruhig sind (Bandpass 4–16 px@4K, Ausgabe/Quelle) | < 1,2× |
| **Blaustich** tiefe Schatten (Lab b*, Luma < 0,08) Zuwachs | < +1,5 |
Vorher/Nachher-Werte immer als Beleg liefern; A/B-Standbilder + 5-s-Stück Tim zeigen, bevor ein Look für eine ganze Folge gilt.

## Quellen (Recherche 2026-10-20)
Eilertsen et al. 2017 „A comparative review of tone-mapping algorithms for HDR video“ (Zeitkohärenz, Rauschen, Bewertung);
Paris 2011 / Aubry 2014 (Local Laplacian); He (Guided Filter); Hessel/Morel 2020 (Simulated Exposure Fusion); Boitard 2012/14
(Brightness Coherency); Photomatix-Doku/FAQ, Aurora HDR (Stilregler, Halo-Abhilfe); YouTube-HDR-Hilfe. Die Repos
Hans1984/HDR-Collection, Jonashwang/awesome-hdr-imaging (Linklisten), kaist-ami/HDR-NSFF (Mehrbelichtungs-NeRF),
vivianhylee/high-dynamic-range-image (Debevec aus Belichtungsreihen) sind für Einzelbelichtungs-Video nicht direkt nutzbar.
Patentiert (nicht nachbauen): Noise-aware TMO (Eilertsen 2015), Motion-path filtering (Aydin 2014).

## Kalibriert (Zollhaus, 2026-10-20) – Startwerte für `look.urbex` (8-bit Osmo Pocket 3, nach Grade + bisherigem Tonemapping)
```yaml
urbex: {eps_fine: 0.02, eps_mid: 0.08, eps_base: 0.25, fine_gain: 2.0, mid_gain: 3.0, base_beta: 0.55,
        chroma_s: 1.0, vibrance: 0.35, coring: 0.025, mid_coring: 0.03, mid_lift: 0.35, detail_limit: 0.45,
        dark_smooth: 0.10}
```
Gemessen (6 Szenen + 2 bewegte Stücke): Lichter-Clipping nie gestiegen, Rauschen dunkel 0,67–0,80× (unter Quelle),
Flackern global 0,06–0,19 %, Kachel-Inkohärenz P95 0,03–0,05, ~0,13 s je 4K-Bild auf GTX 1660 S.

**Lehren aus der Kalibrierung (nicht wiederholen):**
- **eps im Log-Raum:** Textur hat dort Varianz ~0,003–0,04 → eps 4e-4 machte jede Struktur zur „Kante“, Detailebenen leer,
  Lokalkontrast sank (0,93×). eps fein 0,02 / mittel 0,08 / Basis 0,25.
- **8-bit-Blöcke in dunklen Verläufen** (violette Stufen im Türrahmen) werden von der mittleren Skala massiv verstärkt.
  Coring hilft nicht – nur **Mikroglättung dunkler Flächen VOR der Zerlegung** (`dark_smooth`, Guided Filter r≈16 px@4K) +
  Chroma-Glättung (`chroma_r`) + Schatten-Entsättigung (`sh_desat`). Danach Rauschen unter Quellniveau.
- **Mess-Fallen:** RMS-Kontrast (std/mean) sinkt, wenn die Mitten heller werden, obwohl das Bild knackiger ist → nur zusammen
  mit Bildvergleich bewerten. Gradientenumkehr misst an Laub-/Astkanten Werte bis ~1,5 % ohne sichtbare Halos → Halo-Urteil
  an Fensterrahmen/Horizont im Bild prüfen.
- Starke Basis-Kompression (β 0,55) + Mitten-Lift (0,35) erst sinnvoll MIT dark_smooth, sonst Rauschen ×2.
- Kein Pro-Bild-Statistik-Parameter → zeitlich stabil ohne Extra-Filter.
- Einschübe (KI-Zeitreisen, Postkarten) auf Segment-Ebene bauen; die Urbex-Stufe läuft in der Pipeline auch über `insert`.

## v2 (2026-10-20, Tim: „außen sehr geil, aber innen rechts Artefakte“) – Pflicht für Innenräume
- **Ursache per Ablation:** Flecken (wässrige Kleckse auf Holzwand/Boden, 1,45–1,79×) kamen fast nur von der Mittel-Verstärkung
  (mid_gain ×3 verstärkt Kompressionsmatsch dunkler, ruhiger 8-bit-Flächen). Geglättete Gewichte allein halfen nicht (1,43×).
- **Lösung:** strukturabhängige Mittel-Verstärkung `mid_adapt` – volle Verstärkung nur bei echter Struktur (lokale Mitteldetail-
  Energie, auf Schrotrauschen normiert: E·√(Y/0,25), Schwelle ma_lo 0,065 … ma_hi 0,11) ODER hell (Y 0,40 … 0,60); dunkle ruhige
  Flächen ≈ ×1. Dazu Farbe dunkel grob glätten (`chroma_r_dark` 24 px@4K, Farbflecken lila/gelb), tiefstes Schwarz nicht anheben
  (`lift_lo` −3,5), `sh_desat` 0,65 (Petrol-/Blaustich). Ergebnis: innen 0,97–1,14×, außen unverändert (0,93×), Flackern gleich/besser.
- **Messfalle:** Rauschmaß mit σ 2 px sieht grobe Flecken nicht → Flecken-Kriterium (Bandpass 4–16 px) ist jetzt im Gate.
- Parameter v2: `E:/Urbex NEU/Gasthaus Zollhaus/ki/hdr_test/urbex_v2.json`. Immer innen UND außen in 100 % prüfen, nicht nur halbe Größe.
