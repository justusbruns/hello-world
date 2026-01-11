# Schubert Digital Scores Collection

A comprehensive collection of Franz Schubert's musical works in machine-readable formats with detailed metadata.

## Overview

This repository aims to collect, organize, and annotate digital scores of Franz Schubert's compositions. Each work includes:
- Machine-readable score files (MusicXML, MIDI, MEI, etc.)
- Comprehensive metadata (composition date, instrumentation, historical context)
- Cross-references using the Deutsch catalog numbering system

## Directory Structure

```
.
├── scores/               # Score files organized by format AND category
│   ├── musicxml/        # MusicXML format (best for analysis)
│   │   ├── lieder/      # Art songs
│   │   ├── chamber/     # Chamber music
│   │   ├── piano/       # Piano works
│   │   ├── symphonies/  # Symphonic works
│   │   ├── sacred/      # Sacred music
│   │   └── stage_works/ # Operas
│   ├── humdrum/         # Humdrum/Kern format (computational analysis)
│   │   └── [same subdirs]
│   ├── midi/            # MIDI format (playback & performance analysis)
│   │   └── [same subdirs]
│   ├── mei/             # MEI format (scholarly editions)
│   │   └── [same subdirs]
│   └── source/          # Original downloads (.mscz, etc.)
│       └── [same subdirs]
├── metadata/            # JSON metadata files for each work
│   ├── schema.json      # Metadata schema definition
│   ├── catalog_index.json  # Central catalog of all works
│   └── D###_*.json      # Individual work metadata files
├── tools/               # Python analysis & conversion tools
│   ├── download_scores.py   # Download from various sources
│   ├── convert_formats.py   # Convert between formats
│   ├── analyze_scores.py    # Musical analysis tools
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Tools documentation
├── external/            # External repositories (OpenScore, etc.)
└── analysis/            # Analysis results and reports
```

## Metadata Schema

Each work has a JSON metadata file following our schema (see `metadata/schema.json`). Key fields include:

### Core Identification
- **work_id**: Deutsch catalog number (e.g., "D667")
- **title**: Original, English, and alternative titles
- **category**: Work type (lieder, symphony, chamber, piano, sacred, stage_work)

### Compositional Information
- **composition_date**: Year, month, or date range
- **key**: Musical key signature
- **opus_number**: Published opus number if applicable
- **instrumentation**: List of instruments/voices
- **movements**: Detailed movement information

### Historical Context
- **period**: Early (1810-1817), Middle (1818-1823), or Late (1824-1828)
- **location_composed**: Geographic location
- **dedicatee**: Person work was dedicated to
- **premiere**: First performance details

### Musical Context
- **influences**: Composers, poets, or works that influenced this piece
- **related_works**: Connected Schubert compositions
- **text_source**: For vocal works - poet and poem information

### Digital Resources
- **scores**: Array of score files with format, source, and license information

## Sources for Schubert Scores

### Primary Sources

1. **IMSLP (Petrucci Music Library)**
   - URL: https://imslp.org/wiki/Category:Schubert,_Franz
   - Formats: PDF, MusicXML, MIDI
   - License: Public Domain
   - Coverage: Extensive, nearly complete works

2. **MuseScore**
   - URL: https://musescore.com/sheetmusic?text=Schubert
   - Formats: .mscz (MuseScore), MusicXML, MIDI
   - License: Creative Commons / Public Domain
   - Coverage: Popular works, community transcriptions

3. **Verovio Humdrum**
   - URL: https://verovio.humdrum.org/
   - Format: Humdrum (computational music analysis format)
   - License: Various open licenses
   - Coverage: Selected works with high-quality encoding

4. **OpenScore Lieder Corpus**
   - Specialized corpus for German art songs
   - Format: MusicXML, MEI
   - License: Open access
   - Coverage: Significant number of Schubert lieder

5. **Kern Scores**
   - URL: http://kern.humdrum.org/
   - Format: Humdrum **kern
   - License: Open access
   - Coverage: Selected chamber and piano works

## Quick Start

**New to the project?** See [GET_STARTED_NOW.md](GET_STARTED_NOW.md) for a 30-minute quick start guide.

**Want to download scores?** See [SCORE_ACQUISITION_GUIDE.md](SCORE_ACQUISITION_GUIDE.md) for detailed information about formats and sources.

**Using the tools?** See [tools/README.md](tools/README.md) for complete tool documentation.

## Getting Started

### 1. Install Dependencies

```bash
# Install Python packages for analysis
pip install -r tools/requirements.txt

# Or just the essentials to start
pip install music21 requests
```

### 2. Collecting Scores

For each Schubert work you want to add:

1. Find the **Deutsch catalog number** (D number)
2. Download machine-readable scores from sources above
3. Save to appropriate category folder in `scores/`
4. Name files using format: `D###_short_title.extension`

Example:
```bash
scores/chamber/D667_trout_quintet.musicxml
scores/piano/D899_impromptus.musicxml
scores/lieder/D328_erlkonig.musicxml
```

### 2. Creating Metadata

For each work, create a JSON file in `metadata/`:

```bash
metadata/D667_trout_quintet.json
```

Use the schema in `metadata/schema.json` as a guide. See example files:
- `metadata/D667_trout_quintet.json` (chamber music example)
- `metadata/D899_impromptus.json` (piano music example)

### 3. Essential Information to Include

**Minimum required fields:**
- work_id (Deutsch number)
- title (at least original and English)
- category
- composition_date (at least year)

**Highly recommended:**
- key
- instrumentation
- historical_context.period
- scores array (linking to actual score files)
- tags

**For Lieder (art songs):**
- text_source.poet
- text_source.poem_title
- text_source.language

### 4. Finding Work Information

**Reference Resources:**
- **Grove Music Online**: Comprehensive work lists and analysis
- **Wikipedia**: Good starting point for basic information
- **IMSLP**: Often includes composition dates and opus numbers
- **The Hyperion Schubert Edition**: Detailed liner notes for lieder
- **Bärenreiter Urtext editions**: Scholarly information

**Deutsch Catalog:**
The standard reference is Otto Erich Deutsch's thematic catalog:
- "Franz Schubert: Thematisches Verzeichnis seiner Werke in chronologischer Folge" (1978)

## Major Works to Prioritize

### Symphonies
- D759 - Symphony No. 8 "Unfinished"
- D944 - Symphony No. 9 "Great"

### Piano Works
- D899 - Four Impromptus Op. 90
- D935 - Four Impromptus Op. 142
- D960 - Piano Sonata No. 21 in B-flat major
- D958 - Piano Sonata No. 19 in C minor
- D780 - Six Moments Musicaux

### Chamber Music
- D667 - Piano Quintet "Trout"
- D810 - String Quartet No. 14 "Death and the Maiden"
- D956 - String Quintet in C major
- D929 - Piano Trio No. 2 in E-flat major

### Lieder (Essential Collections)
- D911 - Winterreise (24 songs)
- D795 - Die schöne Müllerin (20 songs)
- D957 - Schwanengesang (14 songs)
- D328 - Erlkönig
- D839 - Ave Maria

### Sacred Music
- D678 - Mass No. 5 in A-flat major
- D950 - Mass No. 6 in E-flat major

## File Format Preferences

For detailed format information, see [SCORE_ACQUISITION_GUIDE.md](SCORE_ACQUISITION_GUIDE.md).

1. **Humdrum/Kern** (.krn) - ⭐⭐⭐⭐⭐ Best for computational analysis
2. **MusicXML** (.xml, .musicxml) - ⭐⭐⭐⭐ Best for interchange, widely supported
3. **MEI** (.mei) - ⭐⭐⭐⭐ Highly detailed, scholarly encoding
4. **MIDI** (.mid) - ⭐⭐⭐ Good for playback and performance analysis
5. **MuseScore** (.mscz) - Can be converted to MusicXML

### Automated Tools

Use the provided Python tools for downloading and converting:

```bash
# Download from OpenScore Lieder corpus
python tools/download_scores.py --openscore

# Convert between formats
python tools/convert_formats.py input.mscz output.musicxml

# Analyze scores
python tools/analyze_scores.py score.musicxml --all
```

## Contributing

### Adding a New Work

1. Create a branch: `git checkout -b add-D###-work-title`
2. Add score files to appropriate `scores/` subdirectory
3. Create metadata JSON file in `metadata/`
4. Update the catalog (if we create one)
5. Commit and push

### Metadata Quality Checklist

- [ ] Deutsch number verified
- [ ] Titles include original and English
- [ ] Composition date researched and cited
- [ ] Key and instrumentation confirmed
- [ ] At least one score file included
- [ ] Score source and license documented
- [ ] Historical period identified
- [ ] Related works cross-referenced

## Schubert's Life and Periods

**Franz Schubert (1797-1828)**
- Born: January 31, 1797, Vienna
- Died: November 19, 1828, Vienna (age 31)
- Composed over 1,000 works in his short life

**Compositional Periods:**

1. **Early Period (1810-1817)**: Age 13-20
   - Student works, early lieder
   - First five symphonies
   - Influenced by Mozart, Haydn

2. **Middle Period (1818-1823)**: Age 21-26
   - "Trout" Quintet, "Unfinished" Symphony
   - Major lieder including Erlkönig
   - Die schöne Müllerin song cycle

3. **Late Period (1824-1828)**: Age 27-31
   - String Quintet in C major
   - Last three piano sonatas
   - Winterreise song cycle
   - "Great" C major Symphony
   - Peak of compositional mastery

## License

Schubert's works are in the **public domain** worldwide (died 1828).

Individual digital scores may have specific licenses:
- **Public Domain**: Free to use
- **Creative Commons**: Check specific CC license
- **Open Access**: Free to use with attribution

Always document the source and license in the metadata.

## Computational Analysis

This collection is designed for computational musicology. Available tools:

### Python Analysis Tools (see tools/)

1. **download_scores.py** - Automated score downloading
2. **convert_formats.py** - Format conversion pipeline
3. **analyze_scores.py** - Musical analysis (key, harmony, melody, rhythm)

### Analysis Capabilities

- **Key detection** - Automatic key identification
- **Harmonic analysis** - Chord progression extraction
- **Melodic analysis** - Interval patterns, contour
- **Rhythmic analysis** - Duration patterns, complexity
- **Form analysis** - Structural segmentation
- **Comparative analysis** - Cross-work comparisons

### Example Analyses

```python
# Analyze key of all piano works
from tools.analyze_scores import ScoreAnalyzer
from pathlib import Path

for score in Path('scores/musicxml/piano').glob('*.musicxml'):
    analyzer = ScoreAnalyzer(score)
    key_info = analyzer.analyze_key()
    print(f"{score.stem}: {key_info['key']}")
```

See [tools/README.md](tools/README.md) for complete examples.

## Future Enhancements

- [ ] Automated IMSLP scraper
- [ ] MuseScore API integration
- [ ] Harmonic progression visualizer
- [ ] Melodic similarity finder (query by example)
- [ ] Web dashboard for browsing collection
- [ ] Audio recordings cross-reference
- [ ] Full-text search of poetry in lieder
- [ ] Export to various catalog formats
- [ ] Integration with musicological databases
- [ ] Machine learning for style classification

## Contact & Questions

For questions about the structure or contributions, please open an issue.

---

*"The world does not need music but needs musicians like Schubert."* - Johannes Brahms
