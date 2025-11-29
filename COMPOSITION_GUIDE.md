# Schubert-Style Lied Composer - User Guide

**Version**: 1.0
**Date**: 2025-11-29
**Model Type**: Hybrid (Markov + Interval Bigrams + Rules)

---

## 🎼 Overview

This system generates original Schubert-style lieder (German art songs) using machine learning trained on 94 authentic Schubert compositions. The hybrid approach combines:

1. **Markov Chain** harmony generation (stable, idiomatic chord progressions)
2. **Interval Bigram** melody generation (singable, Schubert-like melodies)
3. **Rule-based** structure (proper cadences, voice leading)

---

## 🚀 Quick Start

### Generate Your First Song

```bash
python3 tools/compose.py
```

This will create:
- `generated/herbstlied_composition.json` - Full composition data
- `generated/herbstlied.musicxml` - Notation file (open in MuseScore)

### Custom Generation

```python
from tools.compose import SchubertComposer

# Initialize composer
composer = SchubertComposer(ml_data_dir='ml_data', seed=42)

# Compose a song
composition = composer.compose_song(
    key="A major",              # Key signature
    time_signature="3/4",       # Waltz time
    num_measures=32,            # Song length
    tempo=80,                   # BPM
    title="Frühlingsträume",   # German title
    harmony_temperature=0.7,    # 0.1-2.0 (lower = more predictable)
    melody_temperature=1.0      # 0.1-2.0 (higher = more creative)
)

# Save outputs
composer.save_composition(composition, 'my_song.json')
composer.composition_to_musicxml(composition, 'my_song.musicxml')
```

---

## 📊 Architecture

### Component 1: Markov Harmony Generator

**Purpose**: Generate idiomatic chord progressions

**How it works**:
1. Starts with tonic chord of specified key
2. Uses learned transition probabilities from 94 Schubert songs
3. Each chord probabilistically determines the next chord
4. Automatically adds authentic cadence (V-I) at end

**Parameters**:
- `key`: "G major", "c minor", etc. (22 keys available)
- `length`: Number of chords to generate
- `temperature`: 0.1-2.0
  - **0.5**: Very conservative (only most common transitions)
  - **0.8**: Schubert-like (recommended)
  - **1.0**: Natural distribution
  - **1.5**: More experimental

**Technical details**:
- Uses 888×888 transition probability matrix
- Trained on 4,129 observed chord transitions
- 99.5% sparse (most transitions are musically invalid)

**Example progressions**:
```
G major → C major → D major → G major (I-IV-V-I)
A minor → D minor → E major → A minor (i-iv-V-i)
```

### Component 2: Interval Melody Generator

**Purpose**: Generate singable, expressive melodies

**How it works**:
1. Starts at pitch appropriate for specified key
2. Uses interval bigram probabilities (what interval follows what)
3. Generates pitch sequence note-by-note
4. Constrains to comfortable vocal range (C4-G5, MIDI 60-79)

**Parameters**:
- `length`: Number of notes
- `start_pitch`: Starting MIDI pitch (60-79)
- `temperature`: 0.1-2.0
  - **0.8**: Predictable, scalar motion
  - **1.0**: Natural Schubert-like flow (recommended)
  - **1.2**: More adventurous leaps
- `pitch_range`: (min, max) MIDI pitches

**Technical details**:
- Uses 31×31 interval bigram matrix
- Intervals range from -12 to +15 semitones
- Trained on melodic patterns from 94 songs
- Automatic range constraint (reflects at boundaries)

**Melodic characteristics**:
- Small intervals preferred (±1-2 semitones)
- Scalar motion common
- Balanced ascending/descending
- Singable range enforced

### Component 3: Structure Rules

**Purpose**: Ensure musical coherence

**Features**:
1. **Proper cadences**: Automatically adds V-I at phrase ends
2. **Key-appropriate chords**: Starts on tonic
3. **Metrical organization**: Aligns chords with beats
4. **Form templates**: (Future: verse/refrain, through-composed)

---

## 🎹 Parameters Guide

### Key Selection

**Available keys** (from corpus):
- **Most common**: G major, A major, D major
- **Minor keys**: c minor, a minor, b minor, d minor

**Auto-select popular key**:
```python
key = None  # System picks weighted by Schubert's preferences
mode = 'major'  # or 'minor'
```

### Time Signatures

**Schubert's favorites**:
- `2/4` - March-like, rhythmic (24% of corpus)
- `3/4` - Waltz, flowing (21% of corpus)
- `6/8` - Lilting, compound meter (19% of corpus)
- `2/2` - Cut time, flowing (16%)
- `4/4` - Common time (14%)

### Tempo

**Typical ranges**:
- **Slow (Langsam)**: 60-72 BPM
- **Moderate (Mäßig)**: 80-96 BPM
- **Fast (Schnell)**: 108-132 BPM

### Length

**Typical structures**:
- **Short song**: 16-24 measures
- **Standard lied**: 32-48 measures
- **Extended**: 64+ measures

### Temperature Settings

**Harmony Temperature** (controls predictability):
- **0.3-0.5**: Very conservative, common progressions only
- **0.6-0.8**: **Recommended** - Schubert-like balance
- **0.9-1.1**: Natural distribution from corpus
- **1.2-2.0**: Experimental, unexpected turns

**Melody Temperature** (controls creativity):
- **0.5-0.8**: Scalar, predictable motion
- **0.9-1.1**: **Recommended** - natural melodic flow
- **1.2-1.5**: More leaps, adventurous
- **1.6-2.0**: Very experimental (may be unsingable)

---

## 📁 Output Formats

### JSON Composition File

Complete composition data in structured format:

```json
{
  "metadata": {
    "title": "Song title",
    "composer": "ML Model (Schubert Style)",
    "key": "G major",
    "time_signature": "3/4",
    "tempo": 72,
    "num_measures": 16
  },
  "harmony": {
    "chord_ids": [4, 830, 881, ...],
    "chord_names": ["G_major", "C_major", ...]
  },
  "melody": {
    "pitches": [67, 69, 71, 72, ...]
  },
  "structure": {
    "beats_per_measure": 3,
    "chords_per_measure": 3,
    "notes_per_measure": 3
  }
}
```

### MusicXML File

Standard notation format compatible with:
- **MuseScore** (free, open-source)
- **Finale**
- **Sibelius**
- **Dorico**
- **GarageBand** (import)

**Contains**:
- Vocal part with melody
- Piano part (currently simplified - rests only)
- Key signature, time signature, tempo
- Proper measure organization

**To open**:
```bash
musescore generated/herbstlied.musicxml
```

---

## 🎵 Usage Examples

### Example 1: Simple Waltz in G Major

```python
composer = SchubertComposer(seed=42)

composition = composer.compose_song(
    key="G major",
    time_signature="3/4",
    num_measures=16,
    tempo=72,
    title="Walzer",
    harmony_temperature=0.8,
    melody_temperature=1.0
)
```

### Example 2: Melancholic Minor Song

```python
composition = composer.compose_song(
    key="c minor",
    time_signature="2/4",
    num_measures=24,
    tempo=66,
    title="Trauerlied",
    harmony_temperature=0.7,  # Conservative harmonies
    melody_temperature=0.9    # Smooth melody
)
```

### Example 3: Lively 6/8 Song

```python
composition = composer.compose_song(
    key="D major",
    time_signature="6/8",
    num_measures=32,
    tempo=96,
    title="Frühlingsfreude",
    harmony_temperature=0.9,  # More variety
    melody_temperature=1.1    # Energetic melody
)
```

### Example 4: Random Schubert-Style Song

```python
composition = composer.compose_song(
    key=None,  # Auto-select popular key
    mode='major',
    time_signature=random.choice(['3/4', '2/4', '6/8']),
    num_measures=random.randint(16, 48),
    tempo=random.randint(66, 96),
    title="Zufälliges Lied"
)
```

### Example 5: Batch Generation

```python
# Generate 10 songs
for i in range(10):
    composition = composer.compose_song(
        key=None,  # Random popular key
        time_signature="3/4",
        num_measures=24,
        tempo=80,
        title=f"Lied Nr. {i+1}",
        harmony_temperature=0.8,
        melody_temperature=1.0
    )

    composer.save_composition(
        composition,
        f'generated/lied_{i+1}.json'
    )
    composer.composition_to_musicxml(
        composition,
        f'generated/lied_{i+1}.musicxml'
    )
```

---

## 🔧 Advanced Usage

### Custom Starting Chord

```python
harmony_gen = MarkovHarmonyGenerator()

# Start on subdominant (IV)
start_chord = harmony_gen.chord_vocab.get('C_major')  # IV in G major

chord_ids = harmony_gen.generate_progression(
    key="G major",
    length=32,
    start_chord=start_chord
)
```

### Custom Pitch Range

```python
melody_gen = IntervalMelodyGenerator()

# Narrow range for beginner singers
melody = melody_gen.generate_melody(
    length=40,
    start_pitch=65,  # F4
    pitch_range=(60, 72)  # C4-C5 (one octave)
)
```

### Analyzing Generated Composition

```python
import json

with open('generated/herbstlied_composition.json') as f:
    comp = json.load(f)

# Get statistics
print(f"Key: {comp['metadata']['key']}")
print(f"Chords: {len(comp['harmony']['chord_ids'])}")
print(f"Unique chords: {len(set(comp['harmony']['chord_names']))}")
print(f"Melody range: {min(comp['melody']['pitches'])}-{max(comp['melody']['pitches'])}")
print(f"Pitch span: {max(comp['melody']['pitches']) - min(comp['melody']['pitches'])} semitones")
```

---

## 📈 Model Performance

### Strengths

✅ **Harmonically coherent**: Progressions sound authentic
✅ **Proper cadences**: Songs end convincingly
✅ **Singable melodies**: Stay in comfortable range
✅ **Style consistency**: Recognizably Schubert-like
✅ **Fast generation**: <1 second per song
✅ **No training needed**: Uses pre-computed probabilities

### Limitations

⚠️ **Piano part simplified**: Currently just placeholders
⚠️ **No text setting**: Doesn't align with German poetry yet
⚠️ **No dynamics**: No expression markings
⚠️ **Simple rhythm**: One note/chord per beat
⚠️ **No phrase structure**: Doesn't learn verse/refrain forms
⚠️ **Limited long-term coherence**: Markov has no "memory" beyond one step

### Planned Improvements (Future Phases)

- [ ] LSTM for better long-term melodic structure
- [ ] Text-music alignment (German poetry)
- [ ] Sophisticated piano accompaniment patterns
- [ ] Dynamics and articulation
- [ ] Rhythmic variation (not just quarter notes)
- [ ] Form templates (verse/refrain, through-composed)
- [ ] Multiple vocal ranges (soprano, tenor, etc.)

---

## 🎓 Understanding the Output

### Chord Names Format

Format: `{Root}_{Quality}`

**Examples**:
- `G_major` - G major triad
- `C_minor` - C minor triad
- `D_dominant-seventh` - D7 chord
- `E-_major` - E-flat major
- `F#_diminished` - F# diminished

### MIDI Pitch Numbers

Standard MIDI mapping:
- **60** = C4 (Middle C)
- **67** = G4
- **69** = A4
- **72** = C5
- **79** = G5

**Vocal ranges**:
- Soprano: C4-A5 (60-81)
- Alto: G3-E5 (55-76)
- Tenor: C3-A4 (48-69)
- Bass: E2-E4 (40-64)

---

## 🐛 Troubleshooting

### "ImportError: No module named 'music21'"

Install music21:
```bash
pip install music21
```

### "File not found: ml_data/vocabularies.json"

Run data preparation first:
```bash
python3 tools/prepare_ml_data.py
```

### Generated melody is too repetitive

Increase melody temperature:
```python
melody_temperature=1.3  # More variety
```

### Harmonies sound too random

Decrease harmony temperature:
```python
harmony_temperature=0.6  # More conservative
```

### MusicXML file won't open

Make sure you have MuseScore or another notation program installed:
```bash
# On Ubuntu/Debian
sudo apt install musescore3

# On macOS
brew install musescore
```

### Want to generate in a specific style

Adjust both temperatures together:
```python
# Romantic, expressive style
harmony_temperature=0.9
melody_temperature=1.2

# Classical, restrained style
harmony_temperature=0.6
melody_temperature=0.8
```

---

## 📚 Technical References

### Data Sources
- **Corpus**: 94 Schubert lieder from OpenScore
- **Pattern library**: analysis/pattern_library.json
- **Training data**: ml_data/ directory

### Key Files
- **Composer**: tools/compose.py
- **Data prep**: tools/prepare_ml_data.py
- **Analysis**: tools/analyze_corpus.py, tools/mine_patterns.py

### Model Components
1. `MarkovHarmonyGenerator`: 888×888 transition matrix
2. `IntervalMelodyGenerator`: 31×31 bigram matrix
3. `SchubertComposer`: Main orchestration class

---

## 🎯 Next Steps

### For Users
1. Generate several songs with different parameters
2. Open in MuseScore and listen
3. Experiment with temperature settings
4. Try different keys and time signatures

### For Developers
1. Implement sophisticated piano accompaniment (use texture patterns)
2. Add text-music alignment for German poetry
3. Train LSTM for better long-term structure
4. Add dynamics and articulation rules
5. Implement form templates (ABA, through-composed, etc.)

---

## 📖 Example Session

```bash
# 1. Generate a song
python3 tools/compose.py

# 2. Open in MuseScore
musescore generated/herbstlied.musicxml

# 3. Export to MIDI for playback
# (Do this in MuseScore: File → Export → MIDI)

# 4. Generate multiple variations
python3 << EOF
from tools.compose import SchubertComposer
composer = SchubertComposer(seed=None)  # Random each time

for i in range(5):
    comp = composer.compose_song(
        key="G major",
        num_measures=24,
        title=f"Variation {i+1}"
    )
    composer.composition_to_musicxml(comp, f'generated/var_{i+1}.musicxml')
EOF
```

---

**Happy Composing! 🎵**

For questions or issues, see the full documentation in the repository.
