#!/usr/bin/env python3
"""
Score Analysis Examples
Demonstrates various computational analyses on Schubert scores.
"""

import argparse
from pathlib import Path
from typing import Dict, List
import json

try:
    from music21 import converter, analysis, chord, key, stream
except ImportError:
    print("Error: music21 not installed. Install with: pip install music21")
    exit(1)


class ScoreAnalyzer:
    """Analyze musical scores for various features."""

    def __init__(self, score_path: Path):
        self.score_path = score_path
        self.score = converter.parse(str(score_path))

    def analyze_key(self) -> Dict:
        """Analyze key of the piece."""
        try:
            detected_key = self.score.analyze('key')
            return {
                'key': str(detected_key),
                'mode': detected_key.mode,
                'tonic': str(detected_key.tonic),
                'correlation': detected_key.correlationCoefficient
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_harmony(self) -> List[Dict]:
        """Extract chord progressions."""
        try:
            chords = []
            chordified = self.score.chordify()

            for c in chordified.flatten().getElementsByClass('Chord')[:20]:  # First 20 chords
                chords.append({
                    'offset': float(c.offset),
                    'pitches': [str(p) for p in c.pitches],
                    'duration': float(c.quarterLength),
                    'root': str(c.root()) if hasattr(c, 'root') else None,
                })

            return chords
        except Exception as e:
            return [{'error': str(e)}]

    def analyze_rhythm(self) -> Dict:
        """Analyze rhythmic patterns."""
        try:
            notes = self.score.flatten().notes

            durations = [n.quarterLength for n in notes]
            duration_histogram = {}
            for d in durations:
                duration_histogram[d] = duration_histogram.get(d, 0) + 1

            return {
                'total_notes': len(notes),
                'duration_types': duration_histogram,
                'avg_duration': sum(durations) / len(durations) if durations else 0,
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_melody(self, part_index: int = 0) -> Dict:
        """Analyze melodic content of a specific part."""
        try:
            if part_index >= len(self.score.parts):
                return {'error': f'Part {part_index} not found'}

            part = self.score.parts[part_index]
            notes = part.flatten().notes

            # Pitch analysis
            pitches = [n.pitch.midi for n in notes if hasattr(n, 'pitch')]

            # Interval analysis
            intervals = []
            for i in range(len(notes) - 1):
                if hasattr(notes[i], 'pitch') and hasattr(notes[i + 1], 'pitch'):
                    interval = notes[i + 1].pitch.midi - notes[i].pitch.midi
                    intervals.append(interval)

            return {
                'part_index': part_index,
                'note_count': len(notes),
                'pitch_range': {
                    'lowest': min(pitches) if pitches else None,
                    'highest': max(pitches) if pitches else None,
                    'span': max(pitches) - min(pitches) if pitches else 0,
                },
                'interval_stats': {
                    'avg_interval': sum(intervals) / len(intervals) if intervals else 0,
                    'max_leap': max(intervals) if intervals else 0,
                    'min_leap': min(intervals) if intervals else 0,
                },
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_form(self) -> Dict:
        """Analyze formal structure."""
        try:
            measures = self.score.parts[0].getElementsByClass('Measure')

            return {
                'total_measures': len(measures),
                'parts': len(self.score.parts),
                'time_signature': str(measures[0].timeSignature) if measures else None,
                'key_signature': str(measures[0].keySignature) if measures else None,
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_all(self) -> Dict:
        """Run all analyses and return combined results."""
        return {
            'file': str(self.score_path.name),
            'key_analysis': self.analyze_key(),
            'form_analysis': self.analyze_form(),
            'rhythm_analysis': self.analyze_rhythm(),
            'melody_analysis': self.analyze_melody(0),
            'harmony_sample': self.analyze_harmony()[:5],  # First 5 chords only
        }

    def compare_with_corpus(self) -> Dict:
        """Compare piece characteristics with typical Schubert characteristics."""
        # This is a simplified example - you would expand this with actual corpus data
        analysis = self.analyze_all()

        # Example: Check if key is typical for Schubert
        schubert_favorite_keys = ['D major', 'A major', 'B-flat major', 'C major',
                                  'D minor', 'B minor', 'C minor']

        key_str = analysis.get('key_analysis', {}).get('key', '')

        return {
            'uses_typical_key': any(k in key_str for k in schubert_favorite_keys),
            'typical_keys': schubert_favorite_keys,
            'detected_key': key_str,
        }


def main():
    parser = argparse.ArgumentParser(description='Analyze Schubert scores')
    parser.add_argument('score', help='Path to score file')
    parser.add_argument('--key', action='store_true', help='Analyze key')
    parser.add_argument('--harmony', action='store_true', help='Analyze harmony')
    parser.add_argument('--rhythm', action='store_true', help='Analyze rhythm')
    parser.add_argument('--melody', action='store_true', help='Analyze melody')
    parser.add_argument('--form', action='store_true', help='Analyze form')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--output', '-o', help='Save results to JSON file')

    args = parser.parse_args()

    score_path = Path(args.score)
    if not score_path.exists():
        print(f"Error: {score_path} not found")
        return

    analyzer = ScoreAnalyzer(score_path)
    results = {}

    print(f"\n🎵 Analyzing {score_path.name}...\n")

    if args.all or not any([args.key, args.harmony, args.rhythm, args.melody, args.form]):
        results = analyzer.analyze_all()
        print(json.dumps(results, indent=2))

    else:
        if args.key:
            results['key'] = analyzer.analyze_key()
            print("Key Analysis:")
            print(json.dumps(results['key'], indent=2))
            print()

        if args.harmony:
            results['harmony'] = analyzer.analyze_harmony()
            print("Harmony Analysis (first 20 chords):")
            print(json.dumps(results['harmony'], indent=2))
            print()

        if args.rhythm:
            results['rhythm'] = analyzer.analyze_rhythm()
            print("Rhythm Analysis:")
            print(json.dumps(results['rhythm'], indent=2))
            print()

        if args.melody:
            results['melody'] = analyzer.analyze_melody()
            print("Melody Analysis (first part):")
            print(json.dumps(results['melody'], indent=2))
            print()

        if args.form:
            results['form'] = analyzer.analyze_form()
            print("Form Analysis:")
            print(json.dumps(results['form'], indent=2))
            print()

    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to {output_path}")

    print("\nExamples:")
    print("  # Analyze all aspects")
    print("  python tools/analyze_scores.py scores/musicxml/piano/D899.musicxml --all")
    print()
    print("  # Analyze only key and harmony")
    print("  python tools/analyze_scores.py scores/musicxml/chamber/D667.musicxml --key --harmony")
    print()
    print("  # Save results to JSON")
    print("  python tools/analyze_scores.py scores/musicxml/piano/D899.musicxml --all -o analysis_results.json")


if __name__ == "__main__":
    main()
