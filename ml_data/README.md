# ML Training Data for Schubert-Style Composition

**Generated**: 2025-11-29
**Source**: 94 Schubert lieder from OpenScore corpus
**Status**: Ready for ML model training

---

## 📁 Files Overview

This directory contains 11 files with ML-ready training data:

### 1. Vocabularies (`vocabularies.json`)
**Size**: 68 KB
**Format**: JSON

Contains mappings between musical elements and integer tokens:

- **chord_vocab**: 888 unique chord types → integer IDs
- **chord_vocab_inv**: Reverse mapping (ID → chord name)
- **interval_vocab**: 31 interval values (-12 to +15 semitones) → integer IDs
- **interval_vocab_inv**: Reverse mapping (ID → interval)
- **key_vocab**: 22 keys → integer IDs
- **key_vocab_inv**: Reverse mapping (ID → key name)

**Special tokens** (first 4 indices in each vocab):
- `<PAD>` (0): Padding for variable-length sequences
- `<START>` (1): Sequence start marker
- `<END>` (2): Sequence end marker
- `<UNK>` (3): Unknown/out-of-vocabulary items

**Usage**:
```python
import json
with open('vocabularies.json') as f:
    vocabs = json.load(f)

# Encode a chord
chord_id = vocabs['chord_vocab']['G_major']

# Decode an ID
chord_name = vocabs['chord_vocab_inv'][str(chord_id)]
```

### 2. Training Data (`train_data.json`)
**Size**: 132 KB
**Format**: JSON
**Songs**: 71 (75.5%)

Contains:
- **indices**: Original song indices (for tracking)
- **harmonies**: 71 encoded chord progressions (100 chords each)
- **melodies**: 71 encoded interval sequences (50 intervals each)
- **cadences**: 71 encoded cadential patterns (4 chords each)
- **metadata**: 71 feature dicts with key, mode, time signature info

**Usage**:
```python
import json
with open('train_data.json') as f:
    train = json.load(f)

# Get first training example
harmony = train['harmonies'][0]  # List of chord IDs
melody = train['melodies'][0]    # List of interval IDs
metadata = train['metadata'][0]  # Feature dict
```

### 3. Validation Data (`val_data.json`)
**Size**: 27 KB
**Format**: JSON
**Songs**: 14 (14.9%)

Same structure as training data, used for hyperparameter tuning and model selection.

### 4. Test Data (`test_data.json`)
**Size**: 17 KB
**Format**: JSON
**Songs**: 9 (9.6%)

Same structure as training data, held out for final evaluation.

### 5-6. Chord Transition Matrices
**Files**:
- `chord_transition_matrix.npy` (6.1 MB): Raw counts
- `chord_transition_probs.npy` (6.1 MB): Normalized probabilities

**Shape**: (888, 888) - one row/column per chord type
**Format**: NumPy binary (.npy)
**Sparsity**: 99.5% (only 4,129 non-zero transitions out of 788,544 possible)

**Usage**:
```python
import numpy as np

# Load probabilities
probs = np.load('chord_transition_probs.npy')

# Generate next chord
current_chord_id = 100
next_chord_probs = probs[current_chord_id]  # Probability distribution
next_chord_id = np.random.choice(888, p=next_chord_probs)
```

**Interpretation**:
- `probs[i, j]` = probability of transitioning from chord i to chord j
- Each row sums to 1.0 (valid probability distribution)
- High diagonal values = chord repetition (tonic prolongation)

### 7-8. Interval Bigram Matrices
**Files**:
- `interval_bigram_matrix.npy` (7.7 KB): Raw counts
- `interval_bigram_probs.npy` (7.7 KB): Normalized probabilities

**Shape**: (31, 31) - one row/column per interval
**Format**: NumPy binary (.npy)
**Non-zero**: 273 transitions out of 961 possible

**Usage**:
```python
import numpy as np

# Load probabilities
bigram_probs = np.load('interval_bigram_probs.npy')

# Generate next interval
current_interval_id = 15  # e.g., +2 semitones (whole step up)
next_interval_probs = bigram_probs[current_interval_id]
next_interval_id = np.random.choice(31, p=next_interval_probs)
```

### 9. N-gram Library (`ngram_library.json`)
**Size**: 237 KB
**Format**: JSON

Contains pre-computed n-gram patterns with frequency counts:

- **melodic_bigrams**: 50 most common 2-interval patterns
- **melodic_trigrams**: 50 most common 3-interval patterns
- **melodic_tetragrams**: 30 most common 4-interval patterns
- **chord_bigrams**: 4,129 unique 2-chord patterns
- **chord_trigrams**: 5,925 unique 3-chord patterns

**Format**: Keys are string representations of tuples, values are counts.

**Usage**:
```python
import json
import ast

with open('ngram_library.json') as f:
    ngrams = json.load(f)

# Get melodic bigrams (as tuples)
bigrams = {ast.literal_eval(k): v for k, v in ngrams['melodic_bigrams'].items()}

# Most common melodic bigram
most_common = max(bigrams.items(), key=lambda x: x[1])
print(f"Most common bigram: {most_common[0]} (count: {most_common[1]})")
```

### 10. Dataset Summary (`dataset_summary.json`)
**Size**: 636 bytes
**Format**: JSON

Quick reference with statistics:
- Dataset sizes (train/val/test splits)
- Vocabulary sizes
- Sequence statistics
- Matrix shapes
- N-gram counts

---

## 📊 Data Statistics

### Dataset Split
- **Total songs**: 94
- **Training**: 71 songs (75.5%)
- **Validation**: 14 songs (14.9%)
- **Test**: 9 songs (9.6%)

*Note*: Random split with seed=42 for reproducibility

### Vocabulary Sizes
- **Chords**: 888 unique types (+ 4 special tokens)
- **Intervals**: 31 values from -12 to +15 semitones (+ 4 special tokens)
- **Keys**: 22 keys (+ 1 unknown token)

### Sequence Lengths
- **Harmonic progressions**: 100 chords per song (fixed)
- **Melodic sequences**: 50 intervals per song (fixed)
- **Cadences**: 4 chords per song (fixed)

### Pattern Counts
- **Total n-grams**: 10,184 patterns
  - Melodic bigrams: 50
  - Melodic trigrams: 50
  - Melodic tetragrams: 30
  - Chord bigrams: 4,129
  - Chord trigrams: 5,925

---

## 🎯 Usage Guide

### Loading Data for Training

```python
import json
import numpy as np

# Load vocabularies
with open('ml_data/vocabularies.json') as f:
    vocabs = json.load(f)

# Load training data
with open('ml_data/train_data.json') as f:
    train = json.load(f)

# Load transition matrices
chord_probs = np.load('ml_data/chord_transition_probs.npy')
interval_probs = np.load('ml_data/interval_bigram_probs.npy')

print(f"Training examples: {len(train['harmonies'])}")
print(f"Chord vocab size: {len(vocabs['chord_vocab'])}")
```

### Creating PyTorch Dataset

```python
import torch
from torch.utils.data import Dataset, DataLoader

class SchubertDataset(Dataset):
    def __init__(self, data_path):
        with open(data_path) as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data['harmonies'])

    def __getitem__(self, idx):
        return {
            'harmony': torch.tensor(self.data['harmonies'][idx]),
            'melody': torch.tensor(self.data['melodies'][idx]),
            'cadence': torch.tensor(self.data['cadences'][idx]),
            'key': self.data['metadata'][idx]['key_idx'],
            'mode': self.data['metadata'][idx]['mode_idx']
        }

# Create dataloaders
train_dataset = SchubertDataset('ml_data/train_data.json')
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

for batch in train_loader:
    # Training loop here
    pass
```

### Markov Chain Generation (Simple)

```python
import numpy as np
import json

# Load vocabularies and transition matrix
with open('ml_data/vocabularies.json') as f:
    vocabs = json.load(f)

chord_probs = np.load('ml_data/chord_transition_probs.npy')
chord_vocab_inv = vocabs['chord_vocab_inv']

# Generate chord progression
def generate_progression(start_chord, length=16):
    progression = [start_chord]

    for _ in range(length - 1):
        current_id = progression[-1]
        next_probs = chord_probs[current_id]

        # Sample next chord
        next_id = np.random.choice(len(chord_probs), p=next_probs)
        progression.append(next_id)

    # Decode to chord names
    return [chord_vocab_inv[str(i)] for i in progression]

# Start with G major (common Schubert key)
start_id = vocabs['chord_vocab']['G_major']
progression = generate_progression(start_id, length=16)
print("Generated progression:", progression)
```

### N-gram Melody Generation

```python
import json
import ast
import numpy as np

# Load n-grams
with open('ml_data/ngram_library.json') as f:
    ngrams = json.load(f)

# Convert bigram strings to tuples
bigrams = {}
for k, v in ngrams['melodic_bigrams'].items():
    bigrams[ast.literal_eval(k)] = v

# Create probability distribution
def bigram_to_probs(bigrams, current_interval):
    """Get next interval probabilities given current interval"""
    matching = {}
    for (i1, i2), count in bigrams.items():
        if i1 == current_interval:
            matching[i2] = count

    if not matching:
        return None

    # Normalize
    total = sum(matching.values())
    return {k: v/total for k, v in matching.items()}

# Generate melody
def generate_melody(start_interval=0, length=20):
    melody = [start_interval]

    for _ in range(length - 1):
        probs = bigram_to_probs(bigrams, melody[-1])
        if probs:
            intervals = list(probs.keys())
            probabilities = list(probs.values())
            next_interval = np.random.choice(intervals, p=probabilities)
            melody.append(next_interval)
        else:
            break

    return melody

melody = generate_melody(length=20)
print("Generated melody (intervals):", melody)
```

---

## 🔬 Data Characteristics

### Harmonic Analysis

**Chord Type Distribution**:
- The chord vocabulary is dominated by **triads** (major, minor, diminished, augmented)
- **Seventh chords** are common (dominant-seventh, diminished-seventh, half-diminished)
- **Extended harmonies** present (ninth chords, eleventh chords)
- **Altered chords** (augmented sixths, Neapolitan chords)

**Transition Patterns**:
- **High diagonal values** in transition matrix = chord repetition (Schubert prolongs harmonies)
- **Strong I-V-I** patterns (tonic-dominant-tonic)
- **Common progressions**: I-IV-V, I-vi-IV-V, ii-V-I
- **Sparse matrix** (99.5%) = most chord transitions are rare/unidiomatic

### Melodic Analysis

**Interval Distribution**:
- **Small intervals dominate**: ±1, ±2 semitones (stepwise motion)
- **Zero interval common**: Repeated notes
- **Large leaps rare**: >5 semitones uncommon
- **Range**: -12 to +15 semitones (octave down to octave+3rd up)

**Melodic Characteristics**:
- **Singable contours**: Balanced ascending/descending motion
- **Scalar patterns**: Many bigrams form scale segments
- **Neighbor tones**: Step away and return patterns common
- **Arpeggios**: Chord outline patterns present

### Key Distribution

**Most Common Keys** (from corpus):
1. G major (10 songs)
2. A major (8 songs)
3. c minor (8 songs)
4. D major (7 songs)
5. a minor (7 songs)

**Mode Distribution**:
- Major: 62%
- Minor: 38%

**Time Signature Distribution**:
1. 2/4 (24%)
2. 3/4 (21%)
3. 6/8 (19%)
4. 2/2 (16%)
5. 4/4 (14%)

---

## 🧮 Technical Details

### Encoding Scheme

**Chords**: Integer encoding based on alphabetically sorted unique chord types
- Example: "G_major" → 456 (arbitrary index)
- Special tokens occupy indices 0-3

**Intervals**: Direct integer encoding of semitone distances
- Example: +2 semitones (whole step up) → maps to vocab index
- Range: -12 (octave down) to +15 (octave + major 2nd up)

**Keys**: Integer encoding of key names
- Major keys: Uppercase (e.g., "G major")
- Minor keys: Lowercase root (e.g., "c minor")

### Normalization

**Transition Matrices**:
- Each row normalized to sum to 1.0
- Valid probability distributions for sampling
- Zero rows (no observed transitions) set to uniform distribution

**Sequences**:
- **Harmonies**: Truncated/padded to 100 chords
- **Melodies**: Truncated/padded to 50 intervals
- **Cadences**: Fixed at 4 chords (final 4 chords of each song)

### Data Format

**JSON files**: Human-readable, easy to inspect and modify
**NumPy files**: Efficient binary format for large matrices
**Vocabulary mappings**: Bidirectional (encode and decode)

---

## 🎼 Model Recommendations

### Approach 1: Markov Chains (Simple, Fast)
**Use**: Transition matrices directly
**Pros**: No training needed, interpretable, fast generation
**Cons**: No long-term structure, no text conditioning

### Approach 2: LSTM (Moderate Complexity)
**Use**: Train on encoded sequences
**Architecture**:
- Input: Previous N chords/intervals
- Hidden: 256-512 LSTM units, 2-3 layers
- Output: Next chord/interval (softmax over vocabulary)

**Pros**: Captures longer dependencies, learns patterns
**Cons**: Requires training, hyperparameter tuning

### Approach 3: Transformer (Advanced)
**Use**: Attention-based sequence model
**Architecture**:
- Embedding: Learned embeddings for chords/intervals
- Encoder: Self-attention layers
- Decoder: Autoregressive generation

**Pros**: Best long-term coherence, state-of-the-art
**Cons**: More training data needed, computationally expensive

### Approach 4: Hybrid (Recommended)
**Combine**:
- Markov chains for harmonic progressions (stable, idiomatic)
- LSTM for melody generation (conditioned on harmony)
- Rule-based for voice leading and piano texture

**Pros**: Leverages strengths of each approach
**Cons**: More complex implementation

---

## 🚀 Next Steps

### Phase 4: Model Development

1. **Choose architecture** (Hybrid recommended for Schubert-style)
2. **Implement model** in PyTorch/TensorFlow
3. **Define loss functions**:
   - Cross-entropy for sequence prediction
   - Style consistency metrics
   - Musicological constraints

### Phase 5: Training

1. **Hyperparameter tuning** on validation set
2. **Monitor metrics**:
   - Perplexity (sequence prediction quality)
   - N-gram overlap with corpus (style similarity)
   - Musical validity (no voice-leading errors)

### Phase 6: Generation Pipeline

1. **Text input**: German poetry (syllable structure)
2. **Key/mood selection**: From key vocabulary
3. **Harmonic generation**: Using Markov chain
4. **Melodic generation**: LSTM conditioned on harmony + text
5. **Piano accompaniment**: Rule-based from texture patterns
6. **Post-processing**: Quantization, voice leading fixes

### Phase 7: Evaluation

1. **Automatic metrics**: Perplexity, style similarity
2. **Human evaluation**: Musicological assessment
3. **Iterative refinement**: Adjust model based on results

---

## 📚 References

- **Source corpus**: OpenScore Lieder (https://github.com/OpenScore/Lieder)
- **Analysis tool**: music21 (https://web.mit.edu/music21/)
- **Schubert catalog**: Deutsch (D) numbers

---

## ⚠️ Notes

- **Reproducibility**: Random seed=42 for train/val/test split
- **Data augmentation**: Not applied (can add transposition later)
- **Evaluation**: Test set should only be used for final evaluation
- **Limitations**: Only 94 songs (relatively small for deep learning)

---

**Data prepared by**: ML Data Preparation Pipeline
**Script**: `tools/prepare_ml_data.py`
**Date**: 2025-11-29
