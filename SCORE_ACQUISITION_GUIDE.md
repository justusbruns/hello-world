# Score Acquisition Guide for Computational Analysis

This guide focuses on obtaining Schubert scores in formats optimized for computational analysis, not just viewing.

## Best Formats for Analysis (Ranked)

### 1. **Humdrum/Kern** ⭐⭐⭐⭐⭐
- **Best for**: Advanced computational analysis
- **Strengths**:
  - Text-based, easily parsed
  - Excellent for harmonic analysis, voice leading, rhythmic patterns
  - Rich analytical tools (Humdrum Toolkit)
  - Preserves all musical information
- **File extension**: `.krn`
- **Recommended source**: Verovio Humdrum Repertory, KernScores

### 2. **MusicXML** ⭐⭐⭐⭐
- **Best for**: General-purpose analysis and interchange
- **Strengths**:
  - Widely supported by music software
  - Good library support (music21, partitura)
  - Preserves notation and semantic information
  - Can be converted to other formats
- **File extension**: `.xml`, `.musicxml`, `.mxl` (compressed)
- **Recommended source**: IMSLP, MuseScore

### 3. **MEI (Music Encoding Initiative)** ⭐⭐⭐⭐
- **Best for**: Scholarly/critical editions
- **Strengths**:
  - Extremely detailed encoding
  - Supports editorial markup
  - Good for philological research
  - XML-based
- **File extension**: `.mei`
- **Recommended source**: OpenScore, scholarly digital editions

### 4. **MIDI** ⭐⭐⭐
- **Best for**: Performance-based analysis, playback
- **Strengths**:
  - Universal support
  - Good for timing, dynamics, tempo analysis
  - Easy to work with programmatically
- **Weaknesses**: Loses notation details (ties vs slurs, enharmonic spelling)
- **File extension**: `.mid`, `.midi`
- **Recommended source**: Any source (easy to generate from other formats)

### 5. **ABC Notation** ⭐⭐
- **Best for**: Simple melodies, folk music
- **Strengths**: Text-based, human-readable
- **Weaknesses**: Limited for complex scores
- **File extension**: `.abc`

## Format Comparison Table

| Format | Analysis | Notation | Harmony | Structure | Text Support | Tool Support |
|--------|----------|----------|---------|-----------|--------------|--------------|
| Humdrum/Kern | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| MusicXML | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| MEI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| MIDI | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |

## Top Sources for Analysis-Ready Schubert Scores

### 🥇 Priority 1: Kern Scores (Humdrum)

**URL**: http://kern.humdrum.org/

**What they have**:
- High-quality encoded Schubert works
- Excellent for analysis
- Text-based, version-controllable

**How to download**:
```bash
# Browse the catalog and download individual .krn files
# Or use the Humdrum Extras tools for batch downloads
```

**Schubert works available** (examples):
- String quartets
- Piano sonatas
- Selected lieder

### 🥇 Priority 2: OpenScore Lieder Corpus

**URL**: https://github.com/OpenScore/Lieder

**What they have**:
- Large collection of German art songs
- Multiple formats: MusicXML, MEI
- High-quality encoding with text underlay
- Includes many Schubert lieder

**How to download**:
```bash
git clone https://github.com/OpenScore/Lieder.git
cd Lieder
# Find Schubert works in the catalog
find . -name "*Schubert*"
```

### 🥈 Priority 3: IMSLP (Versatile)

**URL**: https://imslp.org/wiki/Category:Schubert,_Franz

**What they have**:
- Most complete catalog
- Multiple formats available
- Mix of quality (user-submitted)

**Recommended workflow**:
1. Search for work by Deutsch number
2. Look for these format indicators:
   - "MusicXML" or "XML"
   - "MuseScore" (.mscz) - can export to MusicXML
   - "Sibelius" - can export to MusicXML
3. Download and convert if needed

**Example works with good digital scores**:
- D956 - String Quintet in C major
- D960 - Piano Sonata No. 21
- D899 - Four Impromptus (already in our collection)

### 🥈 Priority 4: MuseScore Community

**URL**: https://musescore.com/

**How to download**:
1. Search: "Schubert D[number]" or title
2. Click "Download" → Select format:
   - **MusicXML** (best for analysis)
   - **MSCZ** (native format, can convert)
   - **MIDI** (for playback analysis)

**Pro tip**: MuseScore files can be batch-converted using MuseScore CLI:
```bash
musescore file.mscz -o file.musicxml
```

### 🥉 Priority 5: Verovio Humdrum Repertory

**URL**: https://verovio.humdrum.org/

**What they have**:
- Curated collection in Humdrum format
- High-quality encoding
- Online viewer for verification

**How to download**:
- Browse online interface
- Download individual .krn files
- Some bulk download options available

## Batch Acquisition Strategy

### Phase 1: Major Works (High Priority)

Download these first - they're well-documented and available in multiple formats:

#### Symphonies (2 works)
- D759 - Symphony No. 8 "Unfinished"
  - **Best source**: IMSLP (MusicXML available)
- D944 - Symphony No. 9 "Great"
  - **Best source**: IMSLP (MusicXML available)

#### Piano Works (8-10 works)
- D899 - Four Impromptus Op. 90 ✓ (in our collection)
- D935 - Four Impromptus Op. 142
- D960 - Piano Sonata No. 21 in B-flat major
- D958 - Piano Sonata No. 19 in C minor
- D850 - Piano Sonata No. 17 in D major
- D780 - Six Moments Musicaux
- D821 - Sonata for Arpeggione and Piano
- **Best source**: MuseScore, IMSLP

#### Chamber Music (5-6 works)
- D667 - Piano Quintet "Trout" ✓ (in our collection)
- D810 - String Quartet No. 14 "Death and the Maiden"
- D956 - String Quintet in C major
- D929 - Piano Trio No. 2 in E-flat major
- D887 - String Quartet No. 15 in G major
- **Best source**: IMSLP (MusicXML), Kern Scores (Humdrum)

#### Essential Lieder (10-15 individual songs)
- D328 - Erlkönig
- D839 - Ave Maria
- D531 - Der Tod und das Mädchen
- D550 - Die Forelle
- D118 - Gretchen am Spinnrade
- **Best source**: OpenScore Lieder Corpus, MuseScore

#### Song Cycles (3 cycles = ~60 songs total)
- D795 - Die schöne Müllerin (20 songs)
- D911 - Winterreise (24 songs)
- D957 - Schwanengesang (14 songs)
- **Best source**: OpenScore Lieder Corpus (complete cycles)

### Phase 2: Secondary Works

After completing Phase 1, expand to:
- Remaining piano sonatas (21 total)
- String quartets (complete)
- Other chamber works
- Sacred music (masses)
- Stage works (operas)

## Recommended Directory Structure

```
scores/
├── humdrum/              # .krn files (best for analysis)
│   ├── symphonies/
│   ├── chamber/
│   ├── piano/
│   └── lieder/
├── musicxml/             # .xml/.musicxml files
│   ├── symphonies/
│   ├── chamber/
│   ├── piano/
│   └── lieder/
├── mei/                  # .mei files (scholarly editions)
│   └── lieder/
├── midi/                 # .mid files (generated or downloaded)
│   ├── chamber/
│   └── piano/
└── source/               # Original files (.mscz, etc.)
    └── [preserve original downloads]
```

## Quality Checklist for Downloaded Scores

Before adding a score to the collection, verify:

- [ ] **Completeness**: All movements/sections present
- [ ] **Accuracy**: Spot-check against known recordings or PDFs
- [ ] **Metadata**: Title, composer, work ID embedded in file
- [ ] **Text encoding**: For vocal works, lyrics properly encoded
- [ ] **Structural markup**: Repeats, endings, sections marked correctly
- [ ] **Playback**: MIDI playback sounds reasonable (if applicable)
- [ ] **License**: Confirmed public domain or appropriate license

## Tools for Verification and Conversion

### Viewing and Verification
- **MuseScore** (free) - View MusicXML, MSCZ, MIDI
- **Verovio** (web) - View Humdrum, MEI, MusicXML online
- **Finale** / **Sibelius** (paid) - Professional notation software

### Format Conversion
```bash
# MuseScore CLI (batch convert)
musescore file.mscz -o file.musicxml
musescore file.mscz -o file.midi

# Verovio (online or CLI)
# Convert between MEI, Humdrum, MusicXML

# music21 (Python)
# Convert between virtually any formats
```

### Validation Tools
- **MusicXML validator**: Check XML syntax
- **Verovio toolkit**: Validate MEI, Humdrum
- **music21**: Programmatic validation in Python

## Python Libraries for Analysis

Once you have the scores, use these for analysis:

### music21 (Most Popular)
```python
from music21 import *
score = converter.parse('D667_trout.musicxml')
score.analyze('key')  # Key analysis
score.parts[0].flat.notes  # Access all notes
```

### partitura (Modern, Performance-focused)
```python
import partitura as pt
score = pt.load_musicxml('D667_trout.musicxml')
note_array = score.note_array()  # Structured note data
```

### Humdrum Toolkit (Command-line)
```bash
kern2midi D667_trout.krn > D667_trout.mid
deg D667_trout.krn  # Scale degree analysis
mint D667_trout.krn  # Melodic interval analysis
```

### pretty_midi (MIDI-focused)
```python
import pretty_midi
midi = pretty_midi.PrettyMIDI('D667_trout.mid')
# Analyze timing, dynamics, etc.
```

## Next Steps

1. **Start with OpenScore Lieder Corpus** - Clone the repo, it's the easiest bulk source
2. **Set up MuseScore** - For downloading and converting from MuseScore.com
3. **Download top 10 works** - Focus on the most famous pieces first
4. **Create conversion pipeline** - Set up tools to normalize all formats to MusicXML + Humdrum
5. **Validate and catalog** - Update metadata with format availability

## Automation Script (Coming Next)

I can create a Python script to:
- Batch download from MuseScore API
- Convert between formats
- Validate scores
- Auto-generate metadata
- Create catalog entries

Would you like me to create these helper scripts?
