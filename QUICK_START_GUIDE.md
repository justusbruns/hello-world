# Quick Start Guide: Adding Schubert Scores

## Step-by-Step Process

### 1. Choose a Work

Start with popular works from the priority list:
- D667 - Trout Quintet ✓ (example included)
- D899 - Four Impromptus ✓ (example included)
- D759 - Symphony No. 8 "Unfinished"
- D328 - Erlkönig
- D810 - String Quartet "Death and the Maiden"

### 2. Find and Download the Score

#### Option A: IMSLP (Recommended)

1. Go to https://imslp.org/wiki/Category:Schubert,_Franz
2. Search for the work by Deutsch number or title
3. Look for scores in these formats (in order of preference):
   - MusicXML (`.xml` or `.musicxml`)
   - MIDI (`.mid`)
   - MuseScore (`.mscz`) - can be converted to MusicXML
4. Download and save to appropriate folder:
   ```bash
   scores/chamber/D810_death_and_maiden.musicxml
   ```

#### Option B: MuseScore

1. Go to https://musescore.com
2. Search: "Schubert D[number]" or work title
3. Download in MusicXML or MuseScore format
4. Save to appropriate category folder

### 3. Research the Work

Gather this information (minimum):

**Essential:**
- [ ] Deutsch number (D###)
- [ ] Original title (German)
- [ ] English title
- [ ] Composition year
- [ ] Musical key
- [ ] Category (lieder, piano, chamber, etc.)
- [ ] Instrumentation

**Good to have:**
- [ ] Opus number
- [ ] Exact composition date
- [ ] Where it was composed
- [ ] Dedicatee
- [ ] Premiere information
- [ ] Influences
- [ ] Movement structure

**Research sources:**
- Wikipedia article for the work
- IMSLP page (often has dates and opus numbers)
- Grove Music Online (if you have access)
- Liner notes from recordings

### 4. Create Metadata File

Copy an example metadata file as a template:

```bash
cp metadata/D667_trout_quintet.json metadata/D810_death_and_maiden.json
```

Edit the new file with the work's information.

### 5. Key Metadata Fields Explained

```json
{
  "work_id": "D810",  // Deutsch number
  "title": {
    "original": "Streichquartett Nr. 14",  // German title
    "english": "String Quartet No. 14",     // English
    "alternative": ["Death and the Maiden"] // Nickname
  },
  "category": "chamber",  // lieder, piano, chamber, symphony, sacred, stage_work
  "composition_date": {
    "year": 1824,
    "month": 3,  // If known
    "circa": false  // true if date is approximate
  },
  "key": "D minor",
  "instrumentation": ["violin", "violin", "viola", "cello"],
  "historical_context": {
    "period": "Late Period (1824-1828)",  // Early, Middle, or Late
    "location_composed": "Vienna, Austria"
  },
  "scores": [
    {
      "format": "musicxml",
      "filename": "scores/chamber/D810_death_and_maiden.musicxml",
      "source": "IMSLP",
      "license": "Public Domain"
    }
  ]
}
```

### 6. Update the Catalog

Edit `metadata/catalog_index.json` to add your new work:

```json
{
  "work_id": "D810",
  "title": "String Quartet No. 14 'Death and the Maiden'",
  "category": "chamber",
  "year": 1824,
  "metadata_file": "metadata/D810_death_and_maiden.json",
  "score_files": ["scores/chamber/D810_death_and_maiden.musicxml"]
}
```

Update the statistics section too.

### 7. Commit Your Changes

```bash
git add scores/chamber/D810_death_and_maiden.musicxml
git add metadata/D810_death_and_maiden.json
git add metadata/catalog_index.json
git commit -m "Add String Quartet No. 14 'Death and the Maiden' (D810)"
git push
```

## Example Workflow

Let's add Erlkönig (D328), one of Schubert's most famous lieder:

### 1. Download Score
- Go to IMSLP: https://imslp.org/wiki/Erlkönig,_D.328_(Schubert,_Franz)
- Download MusicXML version
- Save as: `scores/lieder/D328_erlkonig.musicxml`

### 2. Research (Quick Wikipedia lookup)
- Composed: 1815
- Text by: Johann Wolfgang von Goethe
- Key: G minor
- For: Voice and piano
- Famous dramatic ballad about Death

### 3. Create Metadata

```json
{
  "work_id": "D328",
  "title": {
    "original": "Erlkönig",
    "english": "The Elf King",
    "alternative": ["The Erl-King"]
  },
  "category": "lieder",
  "composition_date": {
    "year": 1815,
    "circa": false
  },
  "key": "G minor",
  "opus_number": "Op. 1",
  "instrumentation": ["voice", "piano"],
  "duration_minutes": 4,
  "text_source": {
    "poet": "Johann Wolfgang von Goethe",
    "poem_title": "Erlkönig",
    "language": "German"
  },
  "historical_context": {
    "period": "Early Period (1810-1817)",
    "location_composed": "Vienna, Austria"
  },
  "scores": [
    {
      "format": "musicxml",
      "filename": "scores/lieder/D328_erlkonig.musicxml",
      "source": "IMSLP",
      "license": "Public Domain"
    }
  ],
  "tags": ["dramatic", "ballad", "death", "nature", "supernatural"],
  "notes": "One of Schubert's most famous and dramatic lieder. Tells the story of a father and child pursued by the supernatural Erlking. Highly innovative use of piano to depict galloping horse."
}
```

### 4. Update catalog and commit

```bash
git add .
git commit -m "Add Erlkönig (D328)"
git push
```

Done! 🎵

## Tips

1. **Start with famous works** - They're easier to research
2. **Use Wikipedia** - Good starting point for basic info
3. **Check IMSLP thoroughly** - Often has composition dates in the description
4. **Don't worry about perfection** - You can always improve metadata later
5. **One work at a time** - Don't overwhelm yourself
6. **Focus on major works first** - Symphonies, famous piano pieces, major lieder cycles

## Priority Works List

### Easiest to Start (Famous, well-documented):
1. D328 - Erlkönig
2. D839 - Ave Maria
3. D759 - Symphony No. 8 "Unfinished"
4. D810 - String Quartet "Death and the Maiden"

### Important Piano Works:
1. D935 - Four Impromptus Op. 142
2. D960 - Piano Sonata No. 21
3. D780 - Six Moments Musicaux

### Song Cycles (these are collections, might want to do as single entries):
1. D795 - Die schöne Müllerin (20 songs)
2. D911 - Winterreise (24 songs)
3. D957 - Schwanengesang (14 songs)

## Questions?

Refer to the main documentation in `SCHUBERT_PROJECT.md` for detailed information about:
- Metadata schema
- Score sources
- Schubert's life and periods
- File naming conventions
