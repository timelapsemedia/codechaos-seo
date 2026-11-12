---
site: codechaos-official.de
url: /en/psy-loudness-data/
title: "Hitech, Psycore & Psytrance Loudness Data: LUFS of 553 Releases | Code Chaos"
description: "Measured: current hitech and psycore releases sit at about -8.3 LUFS (553 tracks), full-on and dark psytrance near -7.9, hardcore at -6. Medians, ranges, method."
h1: "What hitech, psytrance and hardcore releases actually measure"
typ: article
schema: Article + Dataset + FAQPage
hreflang_de: /psy-lautheit-daten/
---

You've probably heard it a hundred times: "master psy hot". Here's what released tracks really do, measured with the same tools we use for every Code Chaos master. The hitech loudness figure comes from 553 current releases; the other values from 16 tracks per genre.

**Short answer:** current hitech and psycore releases sit at about −8.3 LUFS integrated in the median (middle half −9.7 to −6.9), full-on and dark psytrance at about −7.9, hardcore and uptempo at about −6.0, and dubstep and drum and bass at about −7.2.

<!-- TABELLEN: tabellen_codechaos_en.md hier einsetzen -->

## How to read these numbers

- **Integrated loudness (LUFS):** average loudness after ITU-R BS.1770. The bracket is the middle half of the releases.
- **DR:** dynamic range after the DR-database method (second-highest peak against the loudest 20 % of RMS blocks).
- **Side/mid:** how wide the mix is. Psy sits far lower than metal (around −13 to −16 dB) because kick, bass and most leads are close to mono.
- **Correlation below 150 Hz:** 1.00 means the low end is fully mono. Every hitech and psytrance release we measured sits at 1.00.
- **Tonal balance:** each band relative to 1 kHz in the median release. Psy carries 22 to 23 dB more energy below 125 Hz than at 1 kHz, hardcore and bass music around 16.

## What stands out

- **Hitech isn't mastered louder than psytrance.** Despite the tempo, the 553-track median is −8.3 LUFS against −7.9 for psytrance. At 180 to 240 BPM the kick and bass need room to stay separate, and if you limit harder you blur exactly that.
- **Hardcore is the loudest and least dynamic.** It's about −6 LUFS with a DR under 3, because the distorted kick is the whole mix.
- **The low end is mono, always.** Correlation below 150 Hz is 1.00 in the hitech and psytrance medians. A stereo bass or a widened kick layer moves a track away from that, and it is the first thing to check on mono club systems.
- **The top end isn't bright.** The air band sits 12 to 16 dB under 1 kHz, about the same as many metal records.

## How the data was collected

- **Hitech loudness:** 553 hitech and psycore tracks from the Code Chaos reference corpus, integrated loudness after BS.1770.
- **All other values:** 16 released tracks per genre, lossless where possible. Dynamics values marked with an asterisk come mostly from lossy files; MP3 reads DR about 1 dB high in our control measurement.
- **Software:** our own measuring core, true peak with 4× oversampling, bands above 12.5 kHz only from full-band files.
- **Only aggregates:** we don't publish single tracks or artists.

## What this means for your master

A value in the table describes the genre. It doesn't grade your track, and close to the median means typical, not better. On a hitech track, the questions we'd ask first are whether the kick and bass sit on the same root note and in phase, whether the low end is mono, and how much loudness the mix can carry before the kick loses its click.

If you'd like your track measured against this corpus and mastered for release, we're here: [Request mastering](/en/mastering/#request). Free plugin to check kick and bass phase yourself: [Kick/Bass Scope](/plugins/kick-bass-scope/).

## Psytrance loudness FAQ

**How loud should a psytrance master be?**
In our data the middle half of full-on and dark psytrance releases sits between −8.9 and −7.6 LUFS, median −7.9. Go as loud as the kick and bass stay separate, then you check true peak.

**How many LUFS should my premaster be?**
Honestly, the premaster's loudness doesn't matter much. Keep the mix bus free of limiting and leave peaks around −6 to −3 dBFS.

**What LUFS for hitech and psycore?**
The median of 553 current hitech and psycore releases is −8.3 LUFS, the middle half runs from −9.7 to −6.9.

**Should the bass in psytrance be mono?**
In every hitech and psytrance median we measured, correlation below 150 Hz is 1.00, so yes: the low end of released psy is mono.
