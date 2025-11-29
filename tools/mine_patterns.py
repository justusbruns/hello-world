#!/usr/bin/env python3
"""
Deep Pattern Mining - Extract detailed compositional patterns
Analyzes harmonies, melodies, rhythms for ML training
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import statistics

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from music21 import converter, chord, interval, roman, stream, note
except ImportError:
    print("Error: music21 not installed")
    sys.exit(1)


class PatternMiner:
    """Extract detailed patterns from Schubert corpus."""

    def __init__(self, corpus_dir: Path):
        self.corpus_dir = corpus_dir
        self.patterns = {
            'harmonic_progressions': [],
            'chord_transitions': defaultdict(lambda: defaultdict(int)),
            'melodic_ngrams': {
                'bigrams': Counter(),
                'trigrams': Counter(),
                'tetragrams': Counter()
            },
            'interval_sequences': [],
            'cadences': [],
            'piano_textures': [],
            'phrase_lengths': [],
            'key_relationships': defaultdict(list)
        }

    def mine_corpus(self, limit: int = None) -> Dict:
        """Mine patterns from all songs."""
        score_files = list(self.corpus_dir.glob("*.mxl"))
        if limit:
            score_files = score_files[:limit]

        print(f"\n🔍 Mining patterns from {len(score_files)} lieder...")

        for i, score_file in enumerate(score_files, 1):
            print(f"  [{i}/{len(score_files)}] {score_file.name}...", end=" ")

            try:
                self.mine_song(score_file)
                print("✓")
            except Exception as e:
                print(f"✗ {e}")

        self._compile_patterns()
        return self.patterns

    def mine_song(self, score_path: Path):
        """Mine patterns from a single song."""
        score = converter.parse(str(score_path))

        # Extract different pattern types
        self._extract_harmonic_patterns(score)
        self._extract_melodic_patterns(score)
        self._extract_piano_textures(score)

    def _extract_harmonic_patterns(self, score):
        """Extract harmonic progressions and chord transitions."""
        try:
            chordified = score.chordify()
            chords_list = list(chordified.flatten().getElementsByClass('Chord'))

            if len(chords_list) < 2:
                return

            # Extract chord progression
            progression = []
            for c in chords_list[:100]:  # First 100 chords
                try:
                    # Get chord symbol
                    root = c.root().name if hasattr(c, 'root') else 'Unknown'
                    quality = c.commonName if hasattr(c, 'commonName') else 'unknown'
                    chord_symbol = f"{root}_{quality}"
                    progression.append(chord_symbol)
                except:
                    progression.append('unknown')

            self.patterns['harmonic_progressions'].append(progression)

            # Build transition matrix
            for i in range(len(progression) - 1):
                current = progression[i]
                next_chord = progression[i + 1]
                self.patterns['chord_transitions'][current][next_chord] += 1

            # Extract cadences (last 2-4 chords)
            if len(progression) >= 4:
                cadence = progression[-4:]
                self.patterns['cadences'].append(cadence)

        except Exception as e:
            pass

    def _extract_melodic_patterns(self, score):
        """Extract melodic interval patterns (n-grams)."""
        try:
            # Get melody (usually first part or top voice)
            if len(score.parts) > 0:
                melody = score.parts[0].flatten().notes
            else:
                melody = score.flatten().notes

            notes_list = list(melody)

            # Extract intervals
            intervals = []
            for i in range(len(notes_list) - 1):
                if hasattr(notes_list[i], 'pitch') and hasattr(notes_list[i+1], 'pitch'):
                    intv = interval.Interval(notes_list[i], notes_list[i+1])
                    intervals.append(intv.semitones)

            if len(intervals) < 2:
                return

            # Store full sequence
            self.patterns['interval_sequences'].append(intervals[:50])  # First 50 intervals

            # Create n-grams
            # Bigrams
            for i in range(len(intervals) - 1):
                bigram = (intervals[i], intervals[i+1])
                self.patterns['melodic_ngrams']['bigrams'][bigram] += 1

            # Trigrams
            for i in range(len(intervals) - 2):
                trigram = (intervals[i], intervals[i+1], intervals[i+2])
                self.patterns['melodic_ngrams']['trigrams'][trigram] += 1

            # Tetragrams
            for i in range(len(intervals) - 3):
                tetragram = (intervals[i], intervals[i+1], intervals[i+2], intervals[i+3])
                self.patterns['melodic_ngrams']['tetragrams'][tetragram] += 1

        except Exception as e:
            pass

    def _extract_piano_textures(self, score):
        """Analyze piano accompaniment textures."""
        try:
            # If there are 2+ parts, assume part 2+ is piano
            if len(score.parts) < 2:
                return

            piano_part = score.parts[1]  # Usually piano accompaniment

            # Analyze texture in first 8 measures
            measures = list(piano_part.getElementsByClass('Measure'))[:8]

            for measure in measures:
                # Count simultaneous notes (texture density)
                chords_in_measure = measure.getElementsByClass('Chord')
                notes_in_measure = measure.getElementsByClass('Note')

                texture_info = {
                    'chords': len(chords_in_measure),
                    'single_notes': len(notes_in_measure),
                    'density': len(chords_in_measure) + len(notes_in_measure)
                }

                self.patterns['piano_textures'].append(texture_info)

        except Exception as e:
            pass

    def _compile_patterns(self):
        """Compile and summarize extracted patterns."""
        print("\n📊 Compiling pattern statistics...")

        # Chord transition probabilities
        transition_probs = {}
        for chord, next_chords in self.patterns['chord_transitions'].items():
            total = sum(next_chords.values())
            if total > 0:
                probs = {next_chord: count/total
                        for next_chord, count in next_chords.items()}
                transition_probs[chord] = dict(sorted(probs.items(),
                                                     key=lambda x: x[1],
                                                     reverse=True)[:10])  # Top 10

        self.patterns['chord_transition_probs'] = transition_probs

        # Most common melodic patterns
        self.patterns['melodic_ngrams']['bigrams_top'] = dict(
            self.patterns['melodic_ngrams']['bigrams'].most_common(50)
        )
        self.patterns['melodic_ngrams']['trigrams_top'] = dict(
            self.patterns['melodic_ngrams']['trigrams'].most_common(50)
        )
        self.patterns['melodic_ngrams']['tetragrams_top'] = dict(
            self.patterns['melodic_ngrams']['tetragrams'].most_common(30)
        )

        # Clear full counters to save space
        del self.patterns['melodic_ngrams']['bigrams']
        del self.patterns['melodic_ngrams']['trigrams']
        del self.patterns['melodic_ngrams']['tetragrams']

        # Most common cadences
        cadence_counter = Counter([tuple(cad) for cad in self.patterns['cadences']])
        self.patterns['common_cadences'] = dict(cadence_counter.most_common(20))

        print(f"  ✓ Found {len(transition_probs)} chord types")
        print(f"  ✓ Extracted {len(self.patterns['harmonic_progressions'])} progressions")
        print(f"  ✓ Identified {len(self.patterns['melodic_ngrams']['bigrams_top'])} common melodic bigrams")

    def save_patterns(self, output_path: Path):
        """Save patterns to JSON."""
        # Convert tuple keys to strings for JSON
        patterns_serializable = self._make_json_serializable(self.patterns)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(patterns_serializable, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Patterns saved to {output_path}")

    def _make_json_serializable(self, obj):
        """Convert objects to JSON-serializable format."""
        if isinstance(obj, dict):
            return {str(k): self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, Counter):
            return dict(obj)
        elif isinstance(obj, defaultdict):
            return dict(obj)
        else:
            return obj


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Mine deep patterns from Schubert corpus')
    parser.add_argument('--corpus', default='scores/musicxml/lieder',
                       help='Path to corpus directory')
    parser.add_argument('--output', default='analysis/pattern_library.json',
                       help='Output JSON file')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of songs')

    args = parser.parse_args()

    corpus_dir = Path(args.corpus)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    miner = PatternMiner(corpus_dir)
    patterns = miner.mine_corpus(limit=args.limit)
    miner.save_patterns(output_path)

    # Print summary
    print("\n" + "="*60)
    print("PATTERN MINING SUMMARY")
    print("="*60)
    print(f"Harmonic progressions: {len(patterns['harmonic_progressions'])}")
    print(f"Chord types found: {len(patterns['chord_transition_probs'])}")
    print(f"Cadence patterns: {len(patterns['common_cadences'])}")
    print(f"Top melodic bigrams: {len(patterns['melodic_ngrams']['bigrams_top'])}")
    print(f"Top melodic trigrams: {len(patterns['melodic_ngrams']['trigrams_top'])}")

    # Show most common chord transitions
    print("\nMost common chord transitions:")
    all_transitions = []
    for chord, next_chords in patterns['chord_transitions'].items():
        for next_chord, count in next_chords.items():
            all_transitions.append((chord, next_chord, count))

    all_transitions.sort(key=lambda x: x[2], reverse=True)
    for chord, next_chord, count in all_transitions[:10]:
        print(f"  {chord} → {next_chord}: {count} times")


if __name__ == "__main__":
    main()
