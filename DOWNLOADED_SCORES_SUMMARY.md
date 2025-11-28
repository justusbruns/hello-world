# Downloaded Scores Summary

**Date**: 2025-11-28
**Source**: OpenScore Lieder Corpus
**Total Scores**: 94 Schubert lieder in MusicXML format

## 🎵 Complete Song Cycles

### 1. Winterreise, D.911 (24 songs) ✓ COMPLETE
One of Schubert's greatest masterpieces, composed in 1827.

**Songs included:**
1. Gute Nacht
2. Die Wetterfahne
3. Gefror'ne Thränen
4. Erstarrung (multiple versions)
5. Der Lindenbaum
6. Wasserflut
7. Auf dem Flusse
8. Rückblick
9. Irrlicht
10. Rast (Spätere Fassung)
11. Frühlingstraum
12. Einsamkeit (Urspruengliche Fassung)
13. Die Post
14. Der greise Kopf
15. Die Krähe
16. Letzte Hoffnung
17. Im Dorfe
18. Der stürmische Morgen
19. Täuschung
20. Der Wegweiser
21. Das Wirthshaus
22. Muth
23. Die Nebensonnen
24. Der Leiermann

**Location**: `scores/musicxml/lieder/D911_Winterreise_*.mxl`

### 2. Die schöne Müllerin, D.795 (20 songs) ✓ COMPLETE
Beautiful song cycle about a young miller, composed in 1823.

**Songs included:**
1. Das Wandern
2. Wohin?
3. Halt!
4. Danksagung an den Bach
5. Am Feierabend
6. Der Neugierige
7. Ungeduld
8. Morgengruß
9. Des Müllers Blumen
10. Tränenregen
11. Mein!
12. Pause
13. Mit dem grünen Lautenbande
14. Der Jäger
15. Eifersucht und Stolz
16. Die liebe Farbe
17. Die böse Farbe
18. Trockne Blumen
19. Der Müller und der Bach
20. Des Baches Wiegenlied

**Location**: `scores/musicxml/lieder/D795_Die_schöne_Müllerin_*.mxl`

### 3. Schwanengesang, D.957 (14 songs) ✓ COMPLETE
Posthumously published collection (1828), Schubert's last songs.

**Songs included:**
1. Liebesbotschaft
2. Kriegers Ahnung
3. Frühlingssehnsucht
4. Ständchen
5. Aufenthalt
6. In der Ferne
7. Abschied
8. Der Atlas
9. Ihr Bild
10. Das Fischermädchen
11. Die Stadt
12. Am Meer
13. Der Doppelgänger
14. Die Taubenpost

**Location**: `scores/musicxml/lieder/D957_Schwanengesang_*.mxl`

## 📚 Other Lieder Collections

### 4 Gesänge aus "Wilhelm Meister", D.877 (4 songs)
Settings of Goethe's poetry from Wilhelm Meister.

**Location**: `scores/musicxml/lieder/D877_*.mxl`

### 4 Lieder, Op.96 (4 songs)
Collection of four art songs.

**Location**: `scores/musicxml/lieder/Unknown_4_Lieder_Op96_*.mxl`

### Various Opus Collections
- **Op.22** (2 songs)
- **Op.52** (7 songs)
- **Op.59** (4 songs)
- **Op.60** (2 songs)
- **Op.92** (1 song)
- **Miscellaneous** (11 individual songs)

## 📊 Statistics

### By Work Type
- **Complete Song Cycles**: 3 (58 songs total)
- **Song Collections**: 7 collections (36 songs)
- **Total**: **94 songs in MusicXML format**

### By Compositional Period
- **Early Period (1810-1817)**: Some individual songs
- **Middle Period (1818-1823)**: Die schöne Müllerin (D.795)
- **Late Period (1824-1828)**: Winterreise (D.911), Schwanengesang (D.957)

### File Formats
- **MusicXML (.mxl)**: 94 files
- **Location**: `scores/musicxml/lieder/`
- **Source**: OpenScore Lieder Corpus (high-quality, machine-readable)

## ✅ Validation

All scores have been verified:
- ✓ Files are valid MusicXML format
- ✓ Can be parsed by music21 library
- ✓ Key detection works successfully
- ✓ Ready for computational analysis

### Test Results

**Sample analysis (D795, Song 1 - "Das Wandern")**:
```json
{
  "key": "B♭ major",
  "mode": "major",
  "tonic": "B♭",
  "correlation": 0.853
}
```

## 🎯 Analysis Opportunities

With these 94 lieder, you can now analyze:

### Musical Features
- **Key preferences** across song cycles
- **Harmonic progressions** in different periods
- **Melodic intervals** and contours
- **Rhythm patterns** in accompaniment
- **Text-music relationships** (prosody)
- **Form and structure** of individual songs

### Comparative Studies
- Compare **Winterreise** (dark, introspective) vs **Die schöne Müllerin** (lighter, narrative)
- Early vs late period compositional style
- Settings of different poets (Müller, Heine, Rellstab)
- Vocal range and tessitura across songs

### Specific Research Questions
1. What keys did Schubert favor for melancholic vs joyful songs?
2. How do melodic intervals differ between the three major cycles?
3. What harmonic progressions are most common?
4. How does piano accompaniment texture vary?
5. Are there recurring melodic or harmonic motifs?

## 🚀 Quick Start Analysis

### Analyze all song keys
```bash
for file in scores/musicxml/lieder/D911_*.mxl; do
    echo "$(basename $file)"
    python tools/analyze_scores.py "$file" --key
done
```

### Compare harmony across cycles
```bash
# Winterreise
python tools/analyze_scores.py scores/musicxml/lieder/D911_Winterreise_D911_1_Gute_Nacht.mxl --harmony -o winterreise_harmony.json

# Die schöne Müllerin
python tools/analyze_scores.py scores/musicxml/lieder/D795_Die_schöne_Müllerin_D795_1_Das_Wandern.mxl --harmony -o mullerin_harmony.json
```

### Batch analysis
```python
from pathlib import Path
from tools.analyze_scores import ScoreAnalyzer

results = {}
for score in Path('scores/musicxml/lieder').glob('D911_*.mxl'):
    analyzer = ScoreAnalyzer(score)
    results[score.name] = analyzer.analyze_key()

# Save or analyze results
import json
with open('winterreise_keys.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## 📁 Directory Structure

```
scores/musicxml/lieder/
├── D795_Die_schöne_Müllerin_D795_*.mxl (20 files)
├── D911_Winterreise_D911_*.mxl (24 files)
├── D957_Schwanengesang_D957_*.mxl (14 files)
├── D877_4_Gesänge_aus_Wilhelm_Meister_*.mxl (4 files)
└── [Various other lieder] (32 files)
```

## 🎓 Notable Songs Included

### Famous Individual Songs
- **D795** - "Das Wandern" (The Wandering)
- **D795** - "Wohin?" (Where to?)
- **D911** - "Gute Nacht" (Good Night)
- **D911** - "Der Lindenbaum" (The Linden Tree)
- **D911** - "Der Leiermann" (The Hurdy-Gurdy Man)
- **D957** - "Ständchen" (Serenade)
- **D957** - "Der Doppelgänger" (The Double)

## 📚 References

### About the Cycles
- **Winterreise**: 24 songs on poems by Wilhelm Müller (1827)
- **Die schöne Müllerin**: 20 songs on poems by Wilhelm Müller (1823)
- **Schwanengesang**: 14 songs on poems by Rellstab, Heine, Seidl (1828)

### Source Information
- **Corpus**: OpenScore Lieder
- **Repository**: https://github.com/OpenScore/Lieder
- **Format**: MusicXML (.mxl)
- **License**: Open Access (varies by edition)
- **Quality**: High-quality, editorially reviewed

## ✨ Next Steps

### Immediate
1. ✅ Scores downloaded (94 lieder)
2. ✅ Organized by work
3. ✅ Validated with music21
4. ⏳ Create metadata JSON files for major cycles
5. ⏳ Run batch analysis on all songs

### Future Downloads
To expand the collection, download:
- **Piano works** (D899, D935, D960) from MuseScore/IMSLP
- **Chamber music** (D667, D810, D956) from IMSLP
- **Symphonies** (D759, D944) from IMSLP
- **More lieder** from Kern Scores (Humdrum format)

## 🎉 Success!

You now have **94 machine-readable Schubert lieder** ready for computational analysis!

The three major song cycles (Winterreise, Die schöne Müllerin, Schwanengesang) represent some of the greatest achievements in German art song literature.
