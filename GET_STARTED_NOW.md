# Get Started NOW: Download Your First Schubert Scores

This guide gets you up and running in 30 minutes with actual Schubert scores ready for analysis.

## Quick Setup (5 minutes)

### 1. Install Python Dependencies

```bash
cd /path/to/hello-world
pip install music21 requests
```

That's it! You can install more later from `tools/requirements.txt` but these two are enough to start.

## Option A: Fastest Start - OpenScore Lieder (10 minutes)

The OpenScore Lieder corpus has high-quality MusicXML files of Schubert's songs.

### Step 1: Clone the Repository

```bash
python tools/download_scores.py --openscore
```

This downloads the entire corpus (may take 5-10 minutes depending on connection).

### Step 2: Find Schubert Works

```bash
# List all Schubert files
find external/OpenScore-Lieder -name "*Schubert*" -name "*.musicxml"
```

### Step 3: Copy to Your Collection

```bash
# Create directory if needed
mkdir -p scores/musicxml/lieder

# Copy some famous lieder
cp external/OpenScore-Lieder/[path]/Erlkönig*.musicxml scores/musicxml/lieder/D328_erlkonig.musicxml
cp external/OpenScore-Lieder/[path]/Ave_Maria*.musicxml scores/musicxml/lieder/D839_ave_maria.musicxml
```

✅ **You now have machine-readable Schubert scores!**

## Option B: Manual Download - Specific Works (15 minutes)

Download specific works you want to analyze.

### Famous Work: Erlkönig (D328)

#### From MuseScore.com:

1. Go to: https://musescore.com/
2. Search: "Schubert Erlkönig"
3. Find a complete version
4. Click "Download" → Select **MusicXML**
5. Save as: `scores/musicxml/lieder/D328_erlkonig.musicxml`

#### From IMSLP:

1. Go to: https://imslp.org/wiki/Erlkönig,_D.328_(Schubert,_Franz)
2. Scroll to "Sheet Music" section
3. Look for files with "MusicXML" or "MuseScore" format
4. Download and save to: `scores/musicxml/lieder/D328_erlkonig.musicxml`

### Famous Work: "Trout" Quintet (D667)

1. Go to: https://imslp.org/wiki/Piano_Quintet_in_A_major,_D.667_(Schubert,_Franz)
2. Find MusicXML version (or MuseScore file)
3. Download and save as: `scores/musicxml/chamber/D667_trout_quintet.musicxml`

### Famous Work: "Unfinished" Symphony (D759)

1. Go to: https://imslp.org/wiki/Symphony_No.8,_D.759_(Schubert,_Franz)
2. Find MusicXML version
3. Save as: `scores/musicxml/symphonies/D759_unfinished.musicxml`

## Test Your Setup (5 minutes)

### 1. Verify Score Files

```bash
# List what you've downloaded
find scores/ -name "*.musicxml"
```

### 2. Run Your First Analysis

```bash
# Analyze key and harmony
python tools/analyze_scores.py scores/musicxml/lieder/D328_erlkonig.musicxml --key --harmony
```

You should see output like:
```json
{
  "key": "G minor",
  "mode": "minor",
  "tonic": "G",
  ...
}
```

### 3. Convert to MIDI (hear it!)

```bash
# Convert to MIDI
python tools/convert_formats.py \
  scores/musicxml/lieder/D328_erlkonig.musicxml \
  scores/midi/lieder/D328_erlkonig.mid

# Play the MIDI file with your system's MIDI player
```

### 4. Validate Score Quality

```bash
python tools/convert_formats.py scores/musicxml/ . --validate
```

## Your First Analysis Project

Now that you have scores, try this simple analysis:

### Project: Compare Keys of Schubert's Works

```bash
# Analyze keys of multiple works
for file in scores/musicxml/*/*.musicxml; do
    echo "Analyzing: $(basename $file)"
    python tools/analyze_scores.py "$file" --key
    echo "---"
done
```

### Project: Melodic Interval Analysis

Create a file `my_first_analysis.py`:

```python
from music21 import converter
from pathlib import Path
import statistics

def analyze_intervals(score_path):
    """Analyze melodic intervals in a score."""
    score = converter.parse(str(score_path))

    # Get the top part (usually melody)
    part = score.parts[0]
    notes = [n for n in part.flatten().notes if hasattr(n, 'pitch')]

    # Calculate intervals
    intervals = []
    for i in range(len(notes) - 1):
        interval = notes[i + 1].pitch.midi - notes[i].pitch.midi
        intervals.append(interval)

    # Statistics
    print(f"Score: {score_path.name}")
    print(f"  Total melodic intervals: {len(intervals)}")
    print(f"  Average interval: {statistics.mean(intervals):.2f} semitones")
    print(f"  Most common: {statistics.mode(intervals)} semitones")
    print(f"  Largest leap: {max(intervals)} semitones")
    print(f"  Smallest leap: {min(intervals)} semitones")
    print()

# Analyze all your scores
scores_dir = Path('scores/musicxml')
for score_file in scores_dir.rglob('*.musicxml'):
    analyze_intervals(score_file)
```

Run it:
```bash
python my_first_analysis.py
```

## Priority Downloads Checklist

Once you're comfortable, download these priority works:

### Lieder (Songs) - Start Here ✓
- [ ] D328 - Erlkönig
- [ ] D839 - Ave Maria
- [ ] D531 - Der Tod und das Mädchen
- [ ] D550 - Die Forelle
- [ ] D118 - Gretchen am Spinnrade

**Best source**: OpenScore Lieder Corpus or MuseScore

### Piano Works - Great for Analysis
- [ ] D899 - Four Impromptus Op. 90 (already have metadata!)
- [ ] D935 - Four Impromptus Op. 142
- [ ] D960 - Piano Sonata No. 21

**Best source**: MuseScore (search "Schubert D899", etc.)

### Chamber Music - Complex but Rewarding
- [ ] D667 - Trout Quintet (already have metadata!)
- [ ] D810 - Death and the Maiden Quartet

**Best source**: IMSLP

### Symphonies - Large Works
- [ ] D759 - Symphony No. 8 "Unfinished"
- [ ] D944 - Symphony No. 9 "Great"

**Best source**: IMSLP

## Common Issues & Solutions

### "music21 not found"
```bash
pip install music21
# First time setup
python -c "from music21 import configure; configure.run()"
```

### "Can't parse this file"
- File might be corrupted - try re-downloading
- Format might not be supported - convert with MuseScore first
- Try: `python tools/convert_formats.py problem_file.mscz fixed_file.musicxml`

### "No such file or directory"
Make sure directories exist:
```bash
mkdir -p scores/{musicxml,midi,humdrum}/{lieder,chamber,piano,symphonies}
```

### MuseScore files (.mscz) won't convert
Install MuseScore desktop app: https://musescore.org/download
Then music21 can use it for conversion.

## What to Do Next

### 1. Build Your Core Collection (1-2 hours)
Download 10-15 famous works from the priority list above

### 2. Explore the Analyses (30 minutes)
```bash
# Try all analysis types
python tools/analyze_scores.py your_score.musicxml --all
```

### 3. Create Metadata (1 hour)
For each score you download, create a metadata JSON file:
```bash
# Copy template
cp metadata/D667_trout_quintet.json metadata/D328_erlkonig.json
# Edit with work-specific info
```

### 4. Start Your Research Question
- What keys did Schubert prefer?
- How do melodic intervals differ between lieder and piano works?
- What harmonic progressions are common?
- How does rhythmic complexity vary across periods?

## Quick Reference Commands

```bash
# Download OpenScore corpus
python tools/download_scores.py --openscore

# List priority works
python tools/download_scores.py --list-priorities

# Analyze a score
python tools/analyze_scores.py path/to/score.musicxml --all

# Convert format
python tools/convert_formats.py input.mscz output.musicxml

# Batch convert directory
python tools/convert_formats.py scores/source/ scores/musicxml/ --format musicxml --batch

# Validate all scores
python tools/convert_formats.py scores/musicxml/ . --validate
```

## Resources for Finding Scores

1. **OpenScore Lieder** ⭐⭐⭐⭐⭐
   - Command: `python tools/download_scores.py --openscore`
   - Many Schubert lieder in high quality

2. **MuseScore.com** ⭐⭐⭐⭐
   - URL: https://musescore.com/sheetmusic?text=Schubert
   - Easy downloads, good quality, MusicXML available

3. **IMSLP** ⭐⭐⭐⭐
   - URL: https://imslp.org/wiki/Category:Schubert,_Franz
   - Most complete, public domain, some MusicXML

4. **Kern Scores** ⭐⭐⭐⭐ (Advanced)
   - URL: http://kern.humdrum.org/
   - Best for computational analysis (Humdrum format)

---

**You're ready!** Start with Option A (OpenScore) or download 2-3 works manually (Option B), then run your first analysis. Good luck! 🎵
