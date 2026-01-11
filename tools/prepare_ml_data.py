#!/usr/bin/env python3
"""
ML Training Data Preparation for Schubert-Style Composition
Converts pattern library and corpus analysis into ML-ready formats
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import Counter
import pickle


class MLDataPreparator:
    """Prepares Schubert corpus data for machine learning"""

    def __init__(self, pattern_lib_path: str, corpus_analysis_path: str):
        """
        Initialize with paths to pattern library and corpus analysis

        Args:
            pattern_lib_path: Path to pattern_library.json
            corpus_analysis_path: Path to corpus_analysis.json
        """
        self.pattern_lib_path = Path(pattern_lib_path)
        self.corpus_analysis_path = Path(corpus_analysis_path)

        # Load data
        with open(self.pattern_lib_path) as f:
            self.pattern_lib = json.load(f)

        with open(self.corpus_analysis_path) as f:
            self.corpus_analysis = json.load(f)

        # Vocabularies (will be created)
        self.chord_vocab = {}
        self.chord_vocab_inv = {}
        self.interval_vocab = {}
        self.interval_vocab_inv = {}
        self.key_vocab = {}
        self.key_vocab_inv = {}

        # Encoded sequences (will be populated)
        self.encoded_harmonies = []
        self.encoded_melodies = []
        self.encoded_cadences = []

        # Metadata
        self.song_metadata = []

        print("✓ Data loaded successfully")

    def create_vocabularies(self):
        """Create vocabularies for chords, intervals, and keys"""
        print("\n🔤 Creating vocabularies...")

        # 1. CHORD VOCABULARY
        # Collect all unique chords from progressions
        all_chords = set()
        for progression in self.pattern_lib['harmonic_progressions']:
            all_chords.update(progression)

        # Add special tokens
        chord_list = ['<PAD>', '<START>', '<END>', '<UNK>'] + sorted(list(all_chords))
        self.chord_vocab = {chord: idx for idx, chord in enumerate(chord_list)}
        self.chord_vocab_inv = {idx: chord for chord, idx in self.chord_vocab.items()}

        print(f"  ✓ Chord vocabulary: {len(self.chord_vocab)} tokens")
        print(f"    Most common: {list(self.chord_vocab.keys())[4:14]}")  # Skip special tokens

        # 2. INTERVAL VOCABULARY
        # Collect all unique intervals from sequences
        all_intervals = set()
        for sequence in self.pattern_lib['interval_sequences']:
            all_intervals.update(sequence)

        # Add special tokens
        interval_list = ['<PAD>', '<START>', '<END>', '<UNK>'] + sorted(list(all_intervals))
        self.interval_vocab = {interval: idx for idx, interval in enumerate(interval_list)}
        self.interval_vocab_inv = {idx: interval for interval, idx in self.interval_vocab.items()}

        print(f"  ✓ Interval vocabulary: {len(self.interval_vocab)} tokens")
        print(f"    Range: {min(all_intervals)} to {max(all_intervals)} semitones")

        # 3. KEY VOCABULARY
        # Collect all unique keys from corpus analysis statistics
        key_distribution = self.corpus_analysis['statistics']['keys']['distribution']
        unique_keys = sorted(list(key_distribution.keys()))
        key_list = ['<UNK>'] + unique_keys
        self.key_vocab = {key: idx for idx, key in enumerate(key_list)}
        self.key_vocab_inv = {idx: key for key, idx in self.key_vocab.items()}

        print(f"  ✓ Key vocabulary: {len(self.key_vocab)} tokens")
        print(f"    Keys: {unique_keys[:10]}...")

        return {
            'chord_vocab_size': len(self.chord_vocab),
            'interval_vocab_size': len(self.interval_vocab),
            'key_vocab_size': len(self.key_vocab)
        }

    def encode_sequences(self):
        """Encode harmonic and melodic sequences to integers"""
        print("\n🔢 Encoding sequences...")

        # 1. ENCODE HARMONIC PROGRESSIONS
        self.encoded_harmonies = []
        for progression in self.pattern_lib['harmonic_progressions']:
            encoded = [self.chord_vocab.get(chord, self.chord_vocab['<UNK>'])
                      for chord in progression]
            self.encoded_harmonies.append(encoded)

        print(f"  ✓ Encoded {len(self.encoded_harmonies)} harmonic progressions")
        print(f"    Avg length: {np.mean([len(h) for h in self.encoded_harmonies]):.1f} chords")
        print(f"    Max length: {max([len(h) for h in self.encoded_harmonies])} chords")

        # 2. ENCODE MELODIC SEQUENCES (intervals)
        self.encoded_melodies = []
        for sequence in self.pattern_lib['interval_sequences']:
            encoded = [self.interval_vocab.get(interval, self.interval_vocab['<UNK>'])
                      for interval in sequence]
            self.encoded_melodies.append(encoded)

        print(f"  ✓ Encoded {len(self.encoded_melodies)} melodic sequences")
        print(f"    Avg length: {np.mean([len(m) for m in self.encoded_melodies]):.1f} intervals")

        # 3. ENCODE CADENCES
        self.encoded_cadences = []
        for cadence in self.pattern_lib['cadences']:
            encoded = [self.chord_vocab.get(chord, self.chord_vocab['<UNK>'])
                      for chord in cadence]
            self.encoded_cadences.append(encoded)

        print(f"  ✓ Encoded {len(self.encoded_cadences)} cadences")

        return {
            'num_harmonic_sequences': len(self.encoded_harmonies),
            'num_melodic_sequences': len(self.encoded_melodies),
            'num_cadences': len(self.encoded_cadences)
        }

    def create_metadata_features(self):
        """Create feature vectors from song metadata"""
        print("\n📋 Creating metadata features...")

        self.song_metadata = []

        # Since we don't have per-song metadata, create basic features for each song
        # based on corpus statistics and assigned randomly/proportionally
        n_songs = len(self.encoded_harmonies)

        # Get key distribution from corpus analysis
        key_distribution = self.corpus_analysis['statistics']['keys']['distribution']
        mode_distribution = self.corpus_analysis['statistics']['modes']
        time_sig_distribution = self.corpus_analysis['statistics']['time_signatures']['distribution']

        # Create weighted lists for sampling
        keys_list = []
        for key, count in key_distribution.items():
            keys_list.extend([key] * count)

        # Ensure we have enough keys (cycle if needed)
        while len(keys_list) < n_songs:
            keys_list.extend(keys_list[:n_songs - len(keys_list)])

        # Create features for each song
        for i in range(n_songs):
            # Assign key (using distribution)
            key = keys_list[i] if i < len(keys_list) else list(key_distribution.keys())[0]

            # Determine mode from key name
            mode = 'minor' if key and key[0].islower() else 'major'

            # Get most common time signature
            most_common_time_sig = max(time_sig_distribution.items(), key=lambda x: x[1])[0]

            # Parse time signature
            if most_common_time_sig and '/' in most_common_time_sig:
                numerator, denominator = most_common_time_sig.split('/')
                time_sig_numerator = int(numerator)
                time_sig_denominator = int(denominator)
            else:
                time_sig_numerator = 4
                time_sig_denominator = 4

            # Encode categorical features
            key_idx = self.key_vocab.get(key, 0)
            mode_idx = 1 if mode == 'major' else 0

            # Create feature dict
            features = {
                'song_idx': i,
                'key_idx': key_idx,
                'key_name': key,
                'mode_idx': mode_idx,
                'mode_name': mode,
                'time_sig_numerator': time_sig_numerator,
                'time_sig_denominator': time_sig_denominator,
                'is_compound_meter': 1 if time_sig_numerator in [6, 9, 12] else 0,
            }

            self.song_metadata.append(features)

        print(f"  ✓ Created metadata for {len(self.song_metadata)} songs")
        print(f"    Features per song: {len(features)}")

        return self.song_metadata

    def create_transition_matrices(self):
        """Create normalized transition matrices for Markov generation"""
        print("\n🔀 Creating transition matrices...")

        # 1. CHORD TRANSITION MATRIX
        vocab_size = len(self.chord_vocab)
        chord_transition_matrix = np.zeros((vocab_size, vocab_size))

        # Populate from pattern library transitions
        for from_chord, transitions in self.pattern_lib['chord_transitions'].items():
            from_idx = self.chord_vocab.get(from_chord, self.chord_vocab['<UNK>'])

            for to_chord, count in transitions.items():
                to_idx = self.chord_vocab.get(to_chord, self.chord_vocab['<UNK>'])
                chord_transition_matrix[from_idx, to_idx] = count

        # Normalize rows to create probabilities
        row_sums = chord_transition_matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        chord_transition_probs = chord_transition_matrix / row_sums

        print(f"  ✓ Chord transition matrix: {chord_transition_matrix.shape}")
        print(f"    Non-zero transitions: {np.count_nonzero(chord_transition_matrix)}")
        print(f"    Sparsity: {100 * (1 - np.count_nonzero(chord_transition_matrix) / chord_transition_matrix.size):.1f}%")

        # 2. INTERVAL BIGRAM MATRIX
        # Extract bigrams from melodic sequences
        bigram_counts = Counter()
        for melody in self.pattern_lib['interval_sequences']:
            for i in range(len(melody) - 1):
                from_int = melody[i]
                to_int = melody[i + 1]
                bigram_counts[(from_int, to_int)] += 1

        # Create matrix
        interval_vocab_size = len(self.interval_vocab)
        interval_bigram_matrix = np.zeros((interval_vocab_size, interval_vocab_size))

        for (from_int, to_int), count in bigram_counts.items():
            from_idx = self.interval_vocab.get(from_int, self.interval_vocab['<UNK>'])
            to_idx = self.interval_vocab.get(to_int, self.interval_vocab['<UNK>'])
            interval_bigram_matrix[from_idx, to_idx] = count

        # Normalize
        row_sums = interval_bigram_matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        interval_bigram_probs = interval_bigram_matrix / row_sums

        print(f"  ✓ Interval bigram matrix: {interval_bigram_matrix.shape}")
        print(f"    Non-zero transitions: {np.count_nonzero(interval_bigram_matrix)}")

        return {
            'chord_transition_matrix': chord_transition_matrix,
            'chord_transition_probs': chord_transition_probs,
            'interval_bigram_matrix': interval_bigram_matrix,
            'interval_bigram_probs': interval_bigram_probs
        }

    def create_train_val_splits(self, val_ratio: float = 0.15, test_ratio: float = 0.10):
        """Split data into training, validation, and test sets"""
        print(f"\n✂️  Creating train/val/test splits...")
        print(f"   Ratios: train={1-val_ratio-test_ratio:.0%}, val={val_ratio:.0%}, test={test_ratio:.0%}")

        n_songs = len(self.encoded_harmonies)
        indices = np.arange(n_songs)
        np.random.seed(42)  # For reproducibility
        np.random.shuffle(indices)

        # Calculate split points
        val_size = int(n_songs * val_ratio)
        test_size = int(n_songs * test_ratio)
        train_size = n_songs - val_size - test_size

        # Split indices
        train_idx = indices[:train_size]
        val_idx = indices[train_size:train_size + val_size]
        test_idx = indices[train_size + val_size:]

        # Create splits
        splits = {
            'train': {
                'indices': train_idx.tolist(),
                'harmonies': [self.encoded_harmonies[i] for i in train_idx],
                'melodies': [self.encoded_melodies[i] for i in train_idx],
                'cadences': [self.encoded_cadences[i] for i in train_idx],
                'metadata': [self.song_metadata[i] for i in train_idx]
            },
            'val': {
                'indices': val_idx.tolist(),
                'harmonies': [self.encoded_harmonies[i] for i in val_idx],
                'melodies': [self.encoded_melodies[i] for i in val_idx],
                'cadences': [self.encoded_cadences[i] for i in val_idx],
                'metadata': [self.song_metadata[i] for i in val_idx]
            },
            'test': {
                'indices': test_idx.tolist(),
                'harmonies': [self.encoded_harmonies[i] for i in test_idx],
                'melodies': [self.encoded_melodies[i] for i in test_idx],
                'cadences': [self.encoded_cadences[i] for i in test_idx],
                'metadata': [self.song_metadata[i] for i in test_idx]
            }
        }

        print(f"  ✓ Training set: {train_size} songs ({train_size/n_songs*100:.1f}%)")
        print(f"  ✓ Validation set: {val_size} songs ({val_size/n_songs*100:.1f}%)")
        print(f"  ✓ Test set: {test_size} songs ({test_size/n_songs*100:.1f}%)")

        return splits

    def create_n_gram_libraries(self):
        """Create searchable n-gram libraries for generation"""
        print("\n📚 Creating n-gram libraries...")

        # Extract from pattern library
        ngram_lib = {
            'melodic_bigrams': {},
            'melodic_trigrams': {},
            'melodic_tetragrams': {},
            'chord_bigrams': {},
            'chord_trigrams': {}
        }

        # 1. MELODIC BIGRAMS (from pattern library)
        if 'melodic_ngrams' in self.pattern_lib:
            bigrams = self.pattern_lib['melodic_ngrams'].get('bigrams_top', {})
            for bigram_str, count in bigrams.items():
                # Parse "(0, 2)" format
                bigram_tuple = eval(bigram_str)
                # Encode
                encoded = tuple(self.interval_vocab.get(i, self.interval_vocab['<UNK>'])
                              for i in bigram_tuple)
                ngram_lib['melodic_bigrams'][encoded] = count

        print(f"  ✓ Melodic bigrams: {len(ngram_lib['melodic_bigrams'])} patterns")

        # 2. MELODIC TRIGRAMS
        if 'melodic_ngrams' in self.pattern_lib:
            trigrams = self.pattern_lib['melodic_ngrams'].get('trigrams_top', {})
            for trigram_str, count in trigrams.items():
                trigram_tuple = eval(trigram_str)
                encoded = tuple(self.interval_vocab.get(i, self.interval_vocab['<UNK>'])
                              for i in trigram_tuple)
                ngram_lib['melodic_trigrams'][encoded] = count

        print(f"  ✓ Melodic trigrams: {len(ngram_lib['melodic_trigrams'])} patterns")

        # 3. MELODIC TETRAGRAMS
        if 'melodic_ngrams' in self.pattern_lib:
            tetragrams = self.pattern_lib['melodic_ngrams'].get('tetragrams_top', {})
            for tetragram_str, count in tetragrams.items():
                tetragram_tuple = eval(tetragram_str)
                encoded = tuple(self.interval_vocab.get(i, self.interval_vocab['<UNK>'])
                              for i in tetragram_tuple)
                ngram_lib['melodic_tetragrams'][encoded] = count

        print(f"  ✓ Melodic tetragrams: {len(ngram_lib['melodic_tetragrams'])} patterns")

        # 4. CHORD BIGRAMS (from sequences)
        chord_bigrams = Counter()
        for progression in self.pattern_lib['harmonic_progressions']:
            for i in range(len(progression) - 1):
                chord1 = self.chord_vocab.get(progression[i], self.chord_vocab['<UNK>'])
                chord2 = self.chord_vocab.get(progression[i + 1], self.chord_vocab['<UNK>'])
                chord_bigrams[(chord1, chord2)] += 1

        ngram_lib['chord_bigrams'] = dict(chord_bigrams)
        print(f"  ✓ Chord bigrams: {len(ngram_lib['chord_bigrams'])} patterns")

        # 5. CHORD TRIGRAMS
        chord_trigrams = Counter()
        for progression in self.pattern_lib['harmonic_progressions']:
            for i in range(len(progression) - 2):
                chord1 = self.chord_vocab.get(progression[i], self.chord_vocab['<UNK>'])
                chord2 = self.chord_vocab.get(progression[i + 1], self.chord_vocab['<UNK>'])
                chord3 = self.chord_vocab.get(progression[i + 2], self.chord_vocab['<UNK>'])
                chord_trigrams[(chord1, chord2, chord3)] += 1

        ngram_lib['chord_trigrams'] = dict(chord_trigrams)
        print(f"  ✓ Chord trigrams: {len(ngram_lib['chord_trigrams'])} patterns")

        return ngram_lib

    def prepare_all(self, output_dir: str = 'ml_data'):
        """Run full data preparation pipeline"""
        print("=" * 60)
        print("🚀 ML DATA PREPARATION PIPELINE")
        print("=" * 60)

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Step 1: Create vocabularies
        vocab_stats = self.create_vocabularies()

        # Step 2: Encode sequences
        sequence_stats = self.encode_sequences()

        # Step 3: Create metadata features
        self.create_metadata_features()

        # Step 4: Create transition matrices
        matrices = self.create_transition_matrices()

        # Step 5: Create train/val/test splits
        splits = self.create_train_val_splits()

        # Step 6: Create n-gram libraries
        ngram_lib = self.create_n_gram_libraries()

        # Export everything
        print("\n💾 Exporting datasets...")

        # 1. Vocabularies
        vocab_data = {
            'chord_vocab': self.chord_vocab,
            'chord_vocab_inv': self.chord_vocab_inv,
            'interval_vocab': self.interval_vocab,
            'interval_vocab_inv': self.interval_vocab_inv,
            'key_vocab': self.key_vocab,
            'key_vocab_inv': self.key_vocab_inv
        }

        with open(output_path / 'vocabularies.json', 'w') as f:
            json.dump(vocab_data, f, indent=2)
        print(f"  ✓ vocabularies.json")

        # 2. Train/val/test splits
        with open(output_path / 'train_data.json', 'w') as f:
            json.dump(splits['train'], f, indent=2)
        print(f"  ✓ train_data.json")

        with open(output_path / 'val_data.json', 'w') as f:
            json.dump(splits['val'], f, indent=2)
        print(f"  ✓ val_data.json")

        with open(output_path / 'test_data.json', 'w') as f:
            json.dump(splits['test'], f, indent=2)
        print(f"  ✓ test_data.json")

        # 3. Transition matrices (as numpy arrays)
        np.save(output_path / 'chord_transition_matrix.npy', matrices['chord_transition_matrix'])
        np.save(output_path / 'chord_transition_probs.npy', matrices['chord_transition_probs'])
        np.save(output_path / 'interval_bigram_matrix.npy', matrices['interval_bigram_matrix'])
        np.save(output_path / 'interval_bigram_probs.npy', matrices['interval_bigram_probs'])
        print(f"  ✓ transition matrices (4 .npy files)")

        # 4. N-gram libraries
        with open(output_path / 'ngram_library.json', 'w') as f:
            # Convert tuple keys to strings for JSON
            json_ngrams = {
                'melodic_bigrams': {str(k): v for k, v in ngram_lib['melodic_bigrams'].items()},
                'melodic_trigrams': {str(k): v for k, v in ngram_lib['melodic_trigrams'].items()},
                'melodic_tetragrams': {str(k): v for k, v in ngram_lib['melodic_tetragrams'].items()},
                'chord_bigrams': {str(k): v for k, v in ngram_lib['chord_bigrams'].items()},
                'chord_trigrams': {str(k): v for k, v in ngram_lib['chord_trigrams'].items()}
            }
            json.dump(json_ngrams, f, indent=2)
        print(f"  ✓ ngram_library.json")

        # 5. Summary statistics
        summary = {
            'dataset_info': {
                'total_songs': len(self.encoded_harmonies),
                'train_size': len(splits['train']['indices']),
                'val_size': len(splits['val']['indices']),
                'test_size': len(splits['test']['indices'])
            },
            'vocabulary_sizes': vocab_stats,
            'sequence_stats': sequence_stats,
            'matrix_shapes': {
                'chord_transition': matrices['chord_transition_matrix'].shape,
                'interval_bigram': matrices['interval_bigram_matrix'].shape
            },
            'ngram_counts': {
                'melodic_bigrams': len(ngram_lib['melodic_bigrams']),
                'melodic_trigrams': len(ngram_lib['melodic_trigrams']),
                'melodic_tetragrams': len(ngram_lib['melodic_tetragrams']),
                'chord_bigrams': len(ngram_lib['chord_bigrams']),
                'chord_trigrams': len(ngram_lib['chord_trigrams'])
            }
        }

        with open(output_path / 'dataset_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"  ✓ dataset_summary.json")

        print("\n" + "=" * 60)
        print("✅ ML DATA PREPARATION COMPLETE!")
        print("=" * 60)
        print(f"\n📁 Output directory: {output_path.absolute()}")
        print(f"📊 Total files created: 11")
        print(f"🎵 Songs processed: {len(self.encoded_harmonies)}")
        print(f"🔤 Vocabularies: {len(vocab_data)} types")
        print(f"🧮 Transition matrices: 4 types")
        print(f"📚 N-gram patterns: {sum(summary['ngram_counts'].values())}")

        return summary


def main():
    """Main execution"""
    # Paths
    pattern_lib_path = 'analysis/pattern_library.json'
    corpus_analysis_path = 'analysis/corpus_analysis.json'
    output_dir = 'ml_data'

    # Initialize preparator
    preparator = MLDataPreparator(pattern_lib_path, corpus_analysis_path)

    # Run full pipeline
    summary = preparator.prepare_all(output_dir)

    print("\n🎯 Next steps:")
    print("  1. Load vocabularies and transition matrices")
    print("  2. Build ML model (LSTM, Transformer, or hybrid)")
    print("  3. Train on encoded sequences")
    print("  4. Generate new Schubert-style compositions")

    return summary


if __name__ == '__main__':
    main()
