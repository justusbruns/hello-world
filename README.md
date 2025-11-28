# Schubert Digital Scores Collection

A comprehensive collection of Franz Schubert's musical works in machine-readable formats with detailed metadata.

## Quick Start

This repository collects and organizes digital scores of Franz Schubert's compositions with comprehensive metadata including composition dates, instrumentation, historical context, and influences.

**See [SCHUBERT_PROJECT.md](SCHUBERT_PROJECT.md) for complete documentation.**

## Documentation

- **[GET_STARTED_NOW.md](GET_STARTED_NOW.md)** - ⚡ 30-minute quick start guide
- **[SCORE_ACQUISITION_GUIDE.md](SCORE_ACQUISITION_GUIDE.md)** - Detailed guide for downloading analysis-ready scores
- **[SCHUBERT_PROJECT.md](SCHUBERT_PROJECT.md)** - Complete project documentation
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Adding new works step-by-step
- **[tools/README.md](tools/README.md)** - Python tools documentation

## Structure

- `scores/` - Score files organized by format (musicxml, humdrum, midi, mei) and category
- `metadata/` - JSON metadata for each work with detailed information
- `tools/` - Python scripts for downloading, converting, and analyzing scores

## Current Collection

### Chamber & Piano (Metadata Available)
- **D667** - Piano Quintet "Trout" (1819)
- **D899** - Four Impromptus Op. 90 (1827)

### Lieder - Complete Song Cycles ✓
- **D795** - Die schöne Müllerin (20 songs, 1823)
- **D911** - Winterreise (24 songs, 1827)
- **D957** - Schwanengesang (14 songs, 1828)

### Additional Lieder Collections
- D877 - 4 Gesänge aus Wilhelm Meister (4 songs)
- Op.96, Op.22, Op.52, Op.59, Op.60 collections
- Various individual songs including **Erlkönig (D328)** and **Ave Maria (D839)**

**Total: 96 machine-readable scores (94 lieder + 2 others)**

See [DOWNLOADED_SCORES_SUMMARY.md](DOWNLOADED_SCORES_SUMMARY.md) for complete details.

## Quick Start

```bash
# Install dependencies
pip install music21 requests

# Download OpenScore Lieder corpus (easiest start)
python tools/download_scores.py --openscore

# Analyze a score
python tools/analyze_scores.py scores/musicxml/piano/D899.musicxml --all

# Convert formats
python tools/convert_formats.py input.mscz output.musicxml
```

## Score Sources

**Best for Analysis:**
1. **OpenScore Lieder Corpus** - High-quality MusicXML lieder
2. **Kern Scores** - Humdrum format (best for computational analysis)
3. **IMSLP** - Most complete catalog (various formats)
4. **MuseScore** - Community transcriptions (easy downloads)

See [SCORE_ACQUISITION_GUIDE.md](SCORE_ACQUISITION_GUIDE.md) for detailed information.

## Tools

- `tools/download_scores.py` - Download from various sources
- `tools/convert_formats.py` - Convert between formats
- `tools/analyze_scores.py` - Musical analysis (key, harmony, rhythm, etc.)

## Quick Reference

**Schubert's Life:** 1797-1828 (Vienna)
**Total Compositions:** 1000+ works
**Catalog System:** Deutsch numbers (D###)

**Best Formats for Analysis:**
- Humdrum/Kern (.krn) - Computational analysis
- MusicXML (.xml) - General interchange
- MIDI (.mid) - Performance analysis
