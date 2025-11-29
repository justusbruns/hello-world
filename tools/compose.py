#!/usr/bin/env python3
"""
Schubert-Style Lied Composer
Hybrid model combining Markov chains, LSTM, and rule-based generation
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import random


class MarkovHarmonyGenerator:
    """Generates chord progressions using Markov chain transition probabilities"""

    def __init__(self, ml_data_dir: str = 'ml_data'):
        """
        Initialize with ML data directory

        Args:
            ml_data_dir: Path to directory containing vocabularies and transition matrices
        """
        self.ml_data_dir = Path(ml_data_dir)

        # Load vocabularies
        with open(self.ml_data_dir / 'vocabularies.json') as f:
            vocabs = json.load(f)
            self.chord_vocab = vocabs['chord_vocab']
            self.chord_vocab_inv = {int(k): v for k, v in vocabs['chord_vocab_inv'].items()}
            self.key_vocab = vocabs['key_vocab']

        # Load transition probabilities
        self.chord_probs = np.load(self.ml_data_dir / 'chord_transition_probs.npy')

        # Load n-gram library for cadences
        with open(self.ml_data_dir / 'ngram_library.json') as f:
            self.ngrams = json.load(f)

        print("✓ Markov harmony generator initialized")
        print(f"  Chord vocabulary: {len(self.chord_vocab)} types")
        print(f"  Transition matrix: {self.chord_probs.shape}")

    def get_key_root_chord(self, key: str) -> Optional[int]:
        """Get the tonic chord ID for a given key"""
        # Parse key (e.g., "G major" or "c minor")
        parts = key.split()
        if len(parts) != 2:
            return None

        root, mode = parts
        # Create chord name
        if mode.lower() == 'major':
            chord_name = f"{root}_major"
        else:
            chord_name = f"{root}_minor"

        return self.chord_vocab.get(chord_name)

    def generate_progression(
        self,
        key: str = "G major",
        length: int = 32,
        temperature: float = 1.0,
        start_chord: Optional[int] = None
    ) -> List[int]:
        """
        Generate a chord progression using Markov chain

        Args:
            key: Key signature (e.g., "G major")
            length: Number of chords to generate
            temperature: Sampling temperature (higher = more random)
            start_chord: Optional starting chord ID (defaults to tonic)

        Returns:
            List of chord IDs
        """
        # Start with tonic if not specified
        if start_chord is None:
            start_chord = self.get_key_root_chord(key)
            if start_chord is None:
                # Fallback to most common chord
                start_chord = self.chord_vocab.get('G_major', 4)

        progression = [start_chord]

        for _ in range(length - 1):
            current_chord = progression[-1]

            # Get transition probabilities
            probs = self.chord_probs[current_chord].copy()

            # Apply temperature
            if temperature != 1.0:
                probs = np.power(probs, 1.0 / temperature)
                probs /= probs.sum()

            # Sample next chord
            next_chord = np.random.choice(len(probs), p=probs)
            progression.append(next_chord)

        return progression

    def add_cadence(self, progression: List[int], key: str = "G major") -> List[int]:
        """Add an authentic cadence to the end of a progression"""
        # Get tonic chord
        tonic = self.get_key_root_chord(key)
        if tonic is None:
            return progression

        # Try to find dominant chord
        key_parts = key.split()
        root = key_parts[0]

        # Dominant is usually a perfect fifth above tonic
        # For simplicity, look for common dominant seventh chords
        dominant_candidates = [
            f"{root}_dominant-seventh",
            f"{root}_major",
            f"{root}_Dominant Seventh Chord"
        ]

        dominant = None
        for candidate in dominant_candidates:
            if candidate in self.chord_vocab:
                dominant = self.chord_vocab[candidate]
                break

        # Add V-I cadence if we found dominant
        if dominant is not None:
            return progression[:-2] + [dominant, tonic]
        else:
            # Just end on tonic
            return progression[:-1] + [tonic]

    def decode_progression(self, progression: List[int]) -> List[str]:
        """Convert chord IDs to chord names"""
        return [self.chord_vocab_inv.get(chord_id, '<UNK>') for chord_id in progression]


class IntervalMelodyGenerator:
    """Generates melodies using interval bigram probabilities"""

    def __init__(self, ml_data_dir: str = 'ml_data'):
        """
        Initialize with ML data directory

        Args:
            ml_data_dir: Path to directory containing vocabularies and interval matrices
        """
        self.ml_data_dir = Path(ml_data_dir)

        # Load vocabularies
        with open(self.ml_data_dir / 'vocabularies.json') as f:
            vocabs = json.load(f)
            self.interval_vocab = {int(k) if k.lstrip('-').isdigit() else k: v
                                 for k, v in vocabs['interval_vocab'].items()}
            self.interval_vocab_inv = {int(k): v for k, v in vocabs['interval_vocab_inv'].items()}

        # Load interval bigram probabilities
        self.interval_probs = np.load(self.ml_data_dir / 'interval_bigram_probs.npy')

        print("✓ Interval melody generator initialized")
        print(f"  Interval vocabulary: {len(self.interval_vocab)} values")
        print(f"  Bigram matrix: {self.interval_probs.shape}")

    def get_interval_id(self, interval: int) -> int:
        """Get vocabulary ID for an interval value"""
        return self.interval_vocab.get(interval, self.interval_vocab.get('<UNK>', 3))

    def generate_melody(
        self,
        length: int = 40,
        start_pitch: int = 67,  # G4
        temperature: float = 1.0,
        pitch_range: Tuple[int, int] = (60, 79)  # C4 to G5
    ) -> List[int]:
        """
        Generate a melody as a sequence of pitches

        Args:
            length: Number of notes
            start_pitch: Starting MIDI pitch
            temperature: Sampling temperature
            pitch_range: (min_pitch, max_pitch) in MIDI

        Returns:
            List of MIDI pitch numbers
        """
        melody = [start_pitch]
        current_interval_id = self.get_interval_id(0)  # Start with no motion

        for _ in range(length - 1):
            # Get probabilities for next interval
            probs = self.interval_probs[current_interval_id].copy()

            # Apply temperature
            if temperature != 1.0:
                probs = np.power(probs, 1.0 / temperature)
                probs /= probs.sum()

            # Sample next interval ID
            next_interval_id = np.random.choice(len(probs), p=probs)

            # Decode to actual interval
            next_interval = self.interval_vocab_inv.get(next_interval_id, 0)

            # Calculate next pitch
            next_pitch = melody[-1] + next_interval

            # Constrain to range (reflect at boundaries)
            if next_pitch < pitch_range[0]:
                next_pitch = pitch_range[0] + (pitch_range[0] - next_pitch)
            elif next_pitch > pitch_range[1]:
                next_pitch = pitch_range[1] - (next_pitch - pitch_range[1])

            # Clamp to range
            next_pitch = max(pitch_range[0], min(pitch_range[1], next_pitch))

            melody.append(next_pitch)
            current_interval_id = next_interval_id

        return melody

    def intervals_to_pitches(self, intervals: List[int], start_pitch: int = 67) -> List[int]:
        """Convert interval sequence to pitches"""
        pitches = [start_pitch]
        for interval in intervals:
            pitches.append(pitches[-1] + interval)
        return pitches


class SchubertComposer:
    """Main composer class that combines harmony, melody, and texture generation"""

    def __init__(self, ml_data_dir: str = 'ml_data', seed: Optional[int] = None):
        """
        Initialize the Schubert-style composer

        Args:
            ml_data_dir: Path to ML data directory
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.ml_data_dir = Path(ml_data_dir)

        # Initialize generators
        self.harmony_gen = MarkovHarmonyGenerator(ml_data_dir)
        self.melody_gen = IntervalMelodyGenerator(ml_data_dir)

        # Load corpus statistics for defaults
        with open('analysis/corpus_analysis.json') as f:
            self.corpus_stats = json.load(f)

        print("\n✓ SchubertComposer initialized")

    def get_popular_key(self, preference: str = 'major') -> str:
        """Get a popular Schubert key"""
        key_dist = self.corpus_stats['statistics']['keys']['distribution']

        # Filter by preference
        if preference == 'major':
            keys = [k for k in key_dist.keys() if k.split()[1] == 'major']
        elif preference == 'minor':
            keys = [k for k in key_dist.keys() if k.split()[1] == 'minor']
        else:
            keys = list(key_dist.keys())

        # Weight by frequency
        weights = [key_dist[k] for k in keys]
        return random.choices(keys, weights=weights)[0]

    def compose_song(
        self,
        key: Optional[str] = None,
        mode: str = 'major',
        time_signature: str = '3/4',
        num_measures: int = 32,
        tempo: int = 80,
        title: str = "Neues Lied",
        harmony_temperature: float = 0.8,
        melody_temperature: float = 1.0
    ) -> Dict:
        """
        Compose a complete Schubert-style lied

        Args:
            key: Key signature (e.g., "G major") or None for random popular key
            mode: 'major' or 'minor' (used if key is None)
            time_signature: Time signature (e.g., "3/4", "2/4", "6/8")
            num_measures: Number of measures
            tempo: Tempo in BPM
            title: Song title
            harmony_temperature: Temperature for harmony generation (lower = more predictable)
            melody_temperature: Temperature for melody generation

        Returns:
            Dictionary containing all musical elements
        """
        print(f"\n🎼 Composing: {title}")
        print("=" * 60)

        # Select key if not specified
        if key is None:
            key = self.get_popular_key(mode)
        print(f"  Key: {key}")
        print(f"  Time: {time_signature}")
        print(f"  Tempo: {tempo} BPM")
        print(f"  Length: {num_measures} measures")

        # Parse time signature
        numerator, denominator = map(int, time_signature.split('/'))
        beats_per_measure = numerator

        # Calculate number of chords needed (one per beat for simplicity)
        num_chords = num_measures * beats_per_measure

        # Generate harmonic progression
        print("\n  🎹 Generating harmony...")
        chord_ids = self.harmony_gen.generate_progression(
            key=key,
            length=num_chords,
            temperature=harmony_temperature
        )

        # Add proper cadence at the end
        chord_ids = self.harmony_gen.add_cadence(chord_ids, key)

        chord_names = self.harmony_gen.decode_progression(chord_ids)
        print(f"     ✓ Generated {len(chord_ids)} chords")

        # Generate melody
        print("  🎵 Generating melody...")

        # Determine starting pitch based on key
        key_root = key.split()[0]
        # Map note names to MIDI (middle octave)
        note_map = {
            'C': 60, 'C#': 61, 'D': 62, 'E-': 63, 'E': 64,
            'F': 65, 'F#': 66, 'G': 67, 'A-': 68, 'A': 69,
            'B-': 70, 'B': 71
        }
        start_pitch = note_map.get(key_root, 67) + 7  # Start in upper register

        # Generate melody (one note per beat)
        melody_pitches = self.melody_gen.generate_melody(
            length=num_chords,
            start_pitch=start_pitch,
            temperature=melody_temperature,
            pitch_range=(60, 79)  # Comfortable vocal range
        )
        print(f"     ✓ Generated {len(melody_pitches)} notes")

        # Create composition dictionary
        composition = {
            'metadata': {
                'title': title,
                'composer': 'ML Model (Schubert Style)',
                'key': key,
                'time_signature': time_signature,
                'tempo': tempo,
                'num_measures': num_measures
            },
            'harmony': {
                'chord_ids': chord_ids,
                'chord_names': chord_names
            },
            'melody': {
                'pitches': melody_pitches
            },
            'structure': {
                'beats_per_measure': beats_per_measure,
                'chords_per_measure': beats_per_measure,
                'notes_per_measure': beats_per_measure
            }
        }

        print("\n✅ Composition complete!")
        print("=" * 60)

        return composition

    def composition_to_musicxml(self, composition: Dict, output_path: str):
        """Convert composition to MusicXML file using music21"""
        try:
            from music21 import stream, note, chord, key, tempo, meter, metadata
        except ImportError:
            print("❌ Error: music21 not installed. Cannot export to MusicXML.")
            return False

        print(f"\n📝 Exporting to MusicXML: {output_path}")

        # Create score
        score = stream.Score()

        # Add metadata
        md = metadata.Metadata()
        md.title = composition['metadata']['title']
        md.composer = composition['metadata']['composer']
        score.insert(0, md)

        # Create vocal part
        vocal_part = stream.Part()
        vocal_part.id = 'Voice'

        # Add key signature
        key_str = composition['metadata']['key']
        key_obj = key.Key(key_str.split()[0], key_str.split()[1])
        vocal_part.insert(0, key_obj)

        # Add time signature
        time_sig = composition['metadata']['time_signature']
        vocal_part.insert(0, meter.TimeSignature(time_sig))

        # Add tempo
        vocal_part.insert(0, tempo.MetronomeMark(number=composition['metadata']['tempo']))

        # Add melody notes
        melody_pitches = composition['melody']['pitches']
        beats_per_measure = composition['structure']['beats_per_measure']

        for i, pitch in enumerate(melody_pitches):
            n = note.Note(pitch)
            n.quarterLength = 1.0  # One beat per note
            vocal_part.append(n)

        score.insert(0, vocal_part)

        # Create piano part (simplified - just chords)
        piano_part = stream.Part()
        piano_part.id = 'Piano'
        piano_part.insert(0, key_obj)
        piano_part.insert(0, meter.TimeSignature(time_sig))

        # Add chord symbols as chords
        # For now, just create simple triads
        # (More sophisticated piano part would be Phase 5)
        for chord_name in composition['harmony']['chord_names']:
            # Simplified: create a rest for now
            # TODO: Implement proper chord realization
            r = note.Rest()
            r.quarterLength = 1.0
            piano_part.append(r)

        score.insert(0, piano_part)

        # Write to file
        score.write('musicxml', fp=output_path)
        print(f"  ✓ Saved to: {output_path}")

        return True

    def save_composition(self, composition: Dict, output_path: str):
        """Save composition to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(composition, f, indent=2)
        print(f"  ✓ Composition saved to: {output_path}")


def main():
    """Demo: Generate a Schubert-style lied"""
    print("=" * 60)
    print("🎼 SCHUBERT-STYLE LIED COMPOSER")
    print("=" * 60)

    # Initialize composer
    composer = SchubertComposer(ml_data_dir='ml_data', seed=42)

    # Compose a song
    composition = composer.compose_song(
        key="G major",
        time_signature="3/4",
        num_measures=16,
        tempo=72,
        title="Herbstlied",
        harmony_temperature=0.7,  # More conservative harmonies
        melody_temperature=1.0    # Natural melodic flow
    )

    # Save composition
    output_dir = Path('generated')
    output_dir.mkdir(exist_ok=True)

    composer.save_composition(
        composition,
        str(output_dir / 'herbstlied_composition.json')
    )

    # Try to export to MusicXML
    composer.composition_to_musicxml(
        composition,
        str(output_dir / 'herbstlied.musicxml')
    )

    print("\n🎯 Next steps:")
    print("  1. Open herbstlied.musicxml in MuseScore or other notation software")
    print("  2. Listen to MIDI playback")
    print("  3. Refine piano accompaniment (currently simplified)")
    print("  4. Add text (German poetry)")


if __name__ == '__main__':
    main()
