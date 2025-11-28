#!/usr/bin/env python3
"""
Comprehensive Schubert Corpus Analysis
Analyzes all 94 lieder to extract compositional patterns for ML-based generation
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import statistics

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from music21 import converter, key, chord, note, meter, stream, interval
except ImportError:
    print("Error: music21 not installed. Run: pip install music21")
    sys.exit(1)


class SchubertCorpusAnalyzer:
    """Comprehensive analysis of Schubert lieder corpus."""

    def __init__(self, corpus_dir: Path):
        self.corpus_dir = corpus_dir
        self.results = {
            'metadata': {
                'total_songs': 0,
                'analyzed_songs': 0,
                'failed_songs': []
            },
            'keys': {},
            'harmonies': {},
            'melodies': {},
            'rhythms': {},
            'forms': {},
            'statistics': {}
        }

    def analyze_corpus(self, limit: int = None) -> Dict:
        """Analyze all songs in the corpus."""
        score_files = list(self.corpus_dir.glob("*.mxl"))
        self.results['metadata']['total_songs'] = len(score_files)

        if limit:
            score_files = score_files[:limit]

        print(f"\n🎵 Analyzing {len(score_files)} Schubert lieder...")

        keys_list = []
        modes_list = []
        time_sigs = []
        note_counts = []
        durations = []

        for i, score_file in enumerate(score_files, 1):
            print(f"  [{i}/{len(score_files)}] {score_file.name}...", end=" ")

            try:
                analysis = self.analyze_song(score_file)

                if analysis:
                    # Collect data
                    keys_list.append(analysis['key']['key'])
                    modes_list.append(analysis['key']['mode'])
                    time_sigs.append(analysis['form']['time_signature'])
                    note_counts.append(analysis['melody']['note_count'])
                    durations.append(analysis['form']['duration'])

                    self.results['metadata']['analyzed_songs'] += 1
                    print("✓")
                else:
                    print("✗ (failed)")
                    self.results['metadata']['failed_songs'].append(str(score_file.name))

            except Exception as e:
                print(f"✗ Error: {e}")
                self.results['metadata']['failed_songs'].append(str(score_file.name))

        # Compile statistics
        self._compile_statistics(keys_list, modes_list, time_sigs, note_counts, durations)

        return self.results

    def analyze_song(self, score_path: Path) -> Dict:
        """Analyze a single song comprehensively."""
        try:
            score = converter.parse(str(score_path))

            analysis = {
                'filename': score_path.name,
                'key': self._analyze_key(score),
                'harmony': self._analyze_harmony(score),
                'melody': self._analyze_melody(score),
                'rhythm': self._analyze_rhythm(score),
                'form': self._analyze_form(score)
            }

            return analysis

        except Exception as e:
            print(f"\nError analyzing {score_path.name}: {e}")
            return None

    def _analyze_key(self, score) -> Dict:
        """Analyze key and tonality."""
        try:
            detected_key = score.analyze('key')
            return {
                'key': str(detected_key),
                'tonic': str(detected_key.tonic),
                'mode': detected_key.mode,
                'correlation': detected_key.correlationCoefficient
            }
        except:
            return {'key': 'Unknown', 'mode': 'unknown', 'tonic': 'Unknown', 'correlation': 0}

    def _analyze_harmony(self, score) -> Dict:
        """Extract harmonic progressions."""
        try:
            chords_data = []
            chordified = score.chordify()

            for c in chordified.flatten().getElementsByClass('Chord')[:50]:  # First 50 chords
                try:
                    chords_data.append({
                        'offset': float(c.offset),
                        'pitches': [str(p) for p in c.pitches],
                        'root': str(c.root()) if hasattr(c, 'root') else None,
                        'bass': str(c.bass()) if hasattr(c, 'bass') else None,
                        'duration': float(c.quarterLength)
                    })
                except:
                    pass

            return {
                'chord_count': len(chords_data),
                'chords': chords_data[:10]  # Store first 10 for inspection
            }
        except:
            return {'chord_count': 0, 'chords': []}

    def _analyze_melody(self, score) -> Dict:
        """Analyze melodic content (usually top voice)."""
        try:
            # Get first part (usually vocal melody)
            if len(score.parts) == 0:
                notes_stream = score.flatten().notes
            else:
                notes_stream = score.parts[0].flatten().notes

            notes_list = list(notes_stream)

            # Melodic intervals
            intervals = []
            for i in range(len(notes_list) - 1):
                if hasattr(notes_list[i], 'pitch') and hasattr(notes_list[i+1], 'pitch'):
                    intv = interval.Interval(notes_list[i], notes_list[i+1])
                    intervals.append(intv.semitones)

            # Pitch range
            pitches = [n.pitch.midi for n in notes_list if hasattr(n, 'pitch')]

            return {
                'note_count': len(notes_list),
                'unique_pitches': len(set(pitches)) if pitches else 0,
                'range': {
                    'lowest': min(pitches) if pitches else 0,
                    'highest': max(pitches) if pitches else 0,
                    'span': max(pitches) - min(pitches) if pitches else 0
                },
                'intervals': {
                    'mean': statistics.mean(intervals) if intervals else 0,
                    'median': statistics.median(intervals) if intervals else 0,
                    'most_common': Counter(intervals).most_common(5) if intervals else []
                }
            }
        except Exception as e:
            return {'note_count': 0, 'error': str(e)}

    def _analyze_rhythm(self, score) -> Dict:
        """Analyze rhythmic patterns."""
        try:
            notes_stream = score.flatten().notes

            durations = [n.quarterLength for n in notes_stream]
            duration_counts = Counter(durations)

            return {
                'total_notes': len(durations),
                'unique_durations': len(duration_counts),
                'duration_distribution': dict(duration_counts.most_common(10)),
                'mean_duration': statistics.mean(durations) if durations else 0
            }
        except:
            return {'total_notes': 0}

    def _analyze_form(self, score) -> Dict:
        """Analyze formal structure."""
        try:
            parts = score.parts
            measures = parts[0].getElementsByClass('Measure') if parts else score.getElementsByClass('Measure')

            time_sig = None
            if measures:
                ts = measures[0].timeSignature
                time_sig = f"{ts.numerator}/{ts.denominator}" if ts else "Unknown"

            return {
                'parts': len(parts),
                'measures': len(measures),
                'time_signature': time_sig,
                'duration': float(score.quarterLength) if hasattr(score, 'quarterLength') else 0
            }
        except:
            return {'parts': 0, 'measures': 0, 'time_signature': 'Unknown', 'duration': 0}

    def _compile_statistics(self, keys_list, modes_list, time_sigs, note_counts, durations):
        """Compile overall corpus statistics."""
        key_counts = Counter(keys_list)
        mode_counts = Counter(modes_list)
        time_sig_counts = Counter(time_sigs)

        self.results['statistics'] = {
            'keys': {
                'distribution': dict(key_counts.most_common()),
                'most_common': key_counts.most_common(5),
                'total_unique': len(key_counts)
            },
            'modes': {
                'distribution': dict(mode_counts),
                'major_count': mode_counts.get('major', 0),
                'minor_count': mode_counts.get('minor', 0)
            },
            'time_signatures': {
                'distribution': dict(time_sig_counts.most_common()),
                'most_common': time_sig_counts.most_common(5)
            },
            'note_counts': {
                'mean': statistics.mean(note_counts) if note_counts else 0,
                'median': statistics.median(note_counts) if note_counts else 0,
                'min': min(note_counts) if note_counts else 0,
                'max': max(note_counts) if note_counts else 0
            },
            'durations': {
                'mean_quarter_lengths': statistics.mean(durations) if durations else 0,
                'total_analyzed': len(durations)
            }
        }

    def save_results(self, output_path: Path):
        """Save analysis results to JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Schubert lieder corpus')
    parser.add_argument('--corpus', default='scores/musicxml/lieder',
                       help='Path to corpus directory')
    parser.add_argument('--output', default='analysis/corpus_analysis.json',
                       help='Output JSON file')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of songs to analyze (for testing)')

    args = parser.parse_args()

    corpus_dir = Path(args.corpus)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    analyzer = SchubertCorpusAnalyzer(corpus_dir)
    results = analyzer.analyze_corpus(limit=args.limit)
    analyzer.save_results(output_path)

    # Print summary
    print("\n" + "="*60)
    print("CORPUS ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total songs: {results['metadata']['total_songs']}")
    print(f"Successfully analyzed: {results['metadata']['analyzed_songs']}")
    print(f"Failed: {len(results['metadata']['failed_songs'])}")

    if 'statistics' in results and 'keys' in results['statistics']:
        print(f"\nMost common keys:")
        for key, count in results['statistics']['keys']['most_common']:
            print(f"  {key}: {count} songs")

        print(f"\nMode distribution:")
        print(f"  Major: {results['statistics']['modes']['major_count']}")
        print(f"  Minor: {results['statistics']['modes']['minor_count']}")

        print(f"\nMost common time signatures:")
        for ts, count in results['statistics']['time_signatures']['most_common']:
            print(f"  {ts}: {count} songs")


if __name__ == "__main__":
    main()
