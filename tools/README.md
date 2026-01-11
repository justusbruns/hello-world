# Schubert Score Analysis Tools

Python utilities for downloading, converting, and analyzing Schubert's musical scores.

## Installation

```bash
# Install Python dependencies
pip install -r tools/requirements.txt

# For MuseScore format conversion support (optional)
# Download MuseScore from: https://musescore.org/
```

## Tools Overview

### 1. `download_scores.py` - Score Downloader

Download scores from various sources and organize them automatically.

**Features:**
- Direct URL downloads
- Clone OpenScore Lieder corpus
- List priority works
- Auto-update catalog

**Usage:**

```bash
# List priority works to download
python tools/download_scores.py --list-priorities

# Clone OpenScore Lieder corpus (includes many Schubert lieder)
python tools/download_scores.py --openscore

# Download a specific score from URL
python tools/download_scores.py \
  --work-id D810 \
  --url https://example.com/death_and_maiden.musicxml \
  --category chamber \
  --format musicxml
```

### 2. `convert_formats.py` - Format Converter

Convert between different music notation formats.

**Supported Formats:**
- MusicXML (`.xml`, `.musicxml`, `.mxl`)
- MIDI (`.mid`, `.midi`)
- Humdrum (`.krn`)
- MEI (`.mei`)
- MuseScore (`.mscz`)
- LilyPond (`.ly`)
- ABC Notation (`.abc`)

**Usage:**

```bash
# Convert single file
python tools/convert_formats.py input.mscz output.musicxml

# Batch convert entire directory
python tools/convert_formats.py \
  scores/source/piano/ \
  scores/musicxml/piano/ \
  --format musicxml \
  --batch

# Validate scores
python tools/convert_formats.py scores/musicxml/ . --validate
```

### 3. `analyze_scores.py` - Musical Analyzer

Perform computational analysis on scores.

**Analyses Available:**
- **Key analysis**: Detect key, mode, tonic
- **Harmony analysis**: Extract chord progressions
- **Rhythm analysis**: Duration patterns, rhythmic density
- **Melody analysis**: Pitch range, intervals, contour
- **Form analysis**: Structure, measures, parts

**Usage:**

```bash
# Run all analyses
python tools/analyze_scores.py scores/musicxml/piano/D899.musicxml --all

# Specific analyses
python tools/analyze_scores.py scores/musicxml/chamber/D667.musicxml --key --harmony

# Save results to JSON
python tools/analyze_scores.py \
  scores/musicxml/piano/D899.musicxml \
  --all \
  --output analysis_results.json
```

## Workflow Examples

### Complete Workflow: Add New Work

1. **Download score:**
```bash
# Manually from IMSLP/MuseScore, or:
python tools/download_scores.py --work-id D810 --url [URL] --category chamber --format musicxml
```

2. **Convert to multiple formats:**
```bash
# Convert to MIDI for playback
python tools/convert_formats.py \
  scores/musicxml/chamber/D810.musicxml \
  scores/midi/chamber/D810.mid

# Convert to Humdrum for advanced analysis
python tools/convert_formats.py \
  scores/musicxml/chamber/D810.musicxml \
  scores/humdrum/chamber/D810.krn
```

3. **Analyze the score:**
```bash
python tools/analyze_scores.py scores/musicxml/chamber/D810.musicxml --all
```

4. **Create metadata entry:**
```bash
# Copy template and edit
cp metadata/D667_trout_quintet.json metadata/D810_death_maiden.json
# Edit the file with work-specific information
```

### Batch Processing Pipeline

Process multiple scores at once:

```bash
# 1. Clone OpenScore Lieder (one-time)
python tools/download_scores.py --openscore

# 2. Find and copy Schubert lieder to your collection
find external/OpenScore-Lieder -name "*Schubert*" -name "*.musicxml" -exec cp {} scores/musicxml/lieder/ \;

# 3. Batch convert to MIDI
python tools/convert_formats.py \
  scores/musicxml/lieder/ \
  scores/midi/lieder/ \
  --format midi \
  --batch

# 4. Validate all scores
python tools/convert_formats.py scores/musicxml/ . --validate

# 5. Batch analyze (example with loop)
for file in scores/musicxml/piano/*.musicxml; do
    python tools/analyze_scores.py "$file" --all -o "analysis/$(basename "$file" .musicxml).json"
done
```

## Analysis Examples

### Key Analysis
```python
from tools.analyze_scores import ScoreAnalyzer
from pathlib import Path

analyzer = ScoreAnalyzer(Path('scores/musicxml/piano/D899.musicxml'))
key_info = analyzer.analyze_key()
print(f"Detected key: {key_info['key']}")
print(f"Mode: {key_info['mode']}")
```

### Comparative Analysis
```bash
# Analyze multiple works and compare
python tools/analyze_scores.py scores/musicxml/piano/D899.musicxml --key -o D899_analysis.json
python tools/analyze_scores.py scores/musicxml/piano/D935.musicxml --key -o D935_analysis.json

# Compare the JSON outputs to find patterns
```

## Advanced Usage

### Using music21 Directly

```python
from music21 import converter, analysis

# Load score
score = converter.parse('scores/musicxml/chamber/D667.musicxml')

# Get all notes
notes = score.flatten().notes

# Analyze key
key = score.analyze('key')
print(f"Key: {key}")

# Extract melodic intervals from first part
part = score.parts[0]
intervals = []
for n1, n2 in zip(part.flatten().notes[:-1], part.flatten().notes[1:]):
    if hasattr(n1, 'pitch') and hasattr(n2, 'pitch'):
        interval = n2.pitch.midi - n1.pitch.midi
        intervals.append(interval)

print(f"Average melodic interval: {sum(intervals)/len(intervals):.2f} semitones")
```

### Custom Analysis Script

Create your own analysis in `tools/my_analysis.py`:

```python
from music21 import converter
import json

def analyze_work(score_path):
    score = converter.parse(score_path)

    # Your custom analysis here
    result = {
        'total_notes': len(score.flatten().notes),
        'duration_seconds': score.duration.quarterLength / 2,  # Assuming 120 BPM
        # Add more analyses...
    }

    return result

if __name__ == "__main__":
    result = analyze_work('scores/musicxml/piano/D899.musicxml')
    print(json.dumps(result, indent=2))
```

## Troubleshooting

### music21 Installation Issues

```bash
# If music21 fails to install
pip install --upgrade pip setuptools wheel
pip install music21

# Set up music21 environment (first time)
python -c "from music21 import configure; configure.run()"
```

### MuseScore Conversion

For MuseScore file conversion, install MuseScore and add to PATH:

```bash
# Linux/Mac
export PATH=$PATH:/path/to/MuseScore/bin

# Or use music21's converter which will find MuseScore
```

### Large File Processing

For very large scores or batch processing:

```python
# Use music21's corpus cache
from music21 import environment
env = environment.Environment()
env['writeFormat'] = 'musicxml'  # Set default format
```

## Future Enhancements

Planned features:
- [ ] Automatic IMSLP scraper
- [ ] MuseScore.com API integration
- [ ] Harmonic progression visualizer
- [ ] Melodic similarity finder
- [ ] Batch metadata generator
- [ ] Web dashboard for browsing collection

## Contributing

Add your own analysis tools to this directory. Follow the existing code structure:
1. Use argparse for CLI
2. Include docstrings
3. Add usage examples in `--help`
4. Update this README

## Resources

- **music21 documentation**: https://web.mit.edu/music21/doc/
- **Humdrum toolkit**: https://www.humdrum.org/
- **MusicXML specification**: https://www.w3.org/2021/06/musicxml40/
- **OpenScore Lieder**: https://github.com/OpenScore/Lieder
