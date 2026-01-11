#!/usr/bin/env python3
"""
Score Format Converter
Converts between different music notation formats using music21.
"""

import argparse
from pathlib import Path
from typing import List, Optional

try:
    from music21 import converter, environment
except ImportError:
    print("Error: music21 not installed. Install with: pip install music21")
    exit(1)


class FormatConverter:
    """Convert music scores between different formats."""

    SUPPORTED_FORMATS = {
        'musicxml': ['.xml', '.musicxml', '.mxl'],
        'midi': ['.mid', '.midi'],
        'humdrum': ['.krn'],
        'mei': ['.mei'],
        'lilypond': ['.ly'],
        'abc': ['.abc'],
        'musescore': ['.mscz'],
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def convert_file(self, input_path: Path, output_path: Path) -> bool:
        """
        Convert a single score file to another format.

        Args:
            input_path: Path to input file
            output_path: Path to output file

        Returns:
            True if conversion successful
        """
        try:
            if self.verbose:
                print(f"Converting {input_path} → {output_path}")

            # Parse input file
            score = converter.parse(str(input_path))

            # Write output file
            output_format = self._detect_format(output_path)
            score.write(output_format, fp=str(output_path))

            if self.verbose:
                print(f"✓ Converted successfully")
            return True

        except Exception as e:
            print(f"✗ Error converting {input_path}: {e}")
            return False

    def batch_convert(self, input_dir: Path, output_dir: Path,
                     output_format: str, pattern: str = "*") -> List[Path]:
        """
        Batch convert all scores in a directory.

        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            output_format: Target format (musicxml, midi, etc.)
            pattern: Glob pattern for input files

        Returns:
            List of successfully converted file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        converted = []

        # Find all input files
        input_files = []
        for format_name, extensions in self.SUPPORTED_FORMATS.items():
            for ext in extensions:
                input_files.extend(input_dir.glob(f"{pattern}{ext}"))

        print(f"Found {len(input_files)} files to convert")

        for input_file in input_files:
            # Generate output filename
            output_ext = self._get_extension(output_format)
            output_file = output_dir / f"{input_file.stem}{output_ext}"

            if self.convert_file(input_file, output_file):
                converted.append(output_file)

        print(f"\n✓ Converted {len(converted)}/{len(input_files)} files")
        return converted

    def _detect_format(self, file_path: Path) -> str:
        """Detect music21 format name from file extension."""
        ext = file_path.suffix.lower()

        format_map = {
            '.xml': 'musicxml',
            '.musicxml': 'musicxml',
            '.mxl': 'musicxml',
            '.mid': 'midi',
            '.midi': 'midi',
            '.krn': 'humdrum',
            '.mei': 'mei',
            '.ly': 'lilypond',
            '.abc': 'abc',
            '.mscz': 'musescore',
        }

        return format_map.get(ext, 'musicxml')

    def _get_extension(self, format_name: str) -> str:
        """Get file extension for format name."""
        ext_map = {
            'musicxml': '.musicxml',
            'midi': '.mid',
            'humdrum': '.krn',
            'mei': '.mei',
            'lilypond': '.ly',
            'abc': '.abc',
        }
        return ext_map.get(format_name, '.xml')

    def validate_score(self, file_path: Path) -> bool:
        """
        Validate a score file by attempting to parse it.

        Args:
            file_path: Path to score file

        Returns:
            True if valid
        """
        try:
            score = converter.parse(str(file_path))

            if self.verbose:
                print(f"✓ {file_path.name} is valid")
                print(f"  Parts: {len(score.parts)}")
                print(f"  Measures: {len(score.parts[0].getElementsByClass('Measure'))}")

                # Try to get key
                try:
                    key = score.analyze('key')
                    print(f"  Key: {key}")
                except:
                    pass

            return True

        except Exception as e:
            print(f"✗ {file_path.name} is invalid: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Convert music score formats')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('output', help='Output file or directory')
    parser.add_argument('--format', '-f',
                       choices=['musicxml', 'midi', 'humdrum', 'mei', 'lilypond'],
                       default='musicxml',
                       help='Output format (default: musicxml)')
    parser.add_argument('--batch', '-b', action='store_true',
                       help='Batch convert directory')
    parser.add_argument('--validate', '-v', action='store_true',
                       help='Validate input file(s) without converting')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress verbose output')

    args = parser.parse_args()

    converter_tool = FormatConverter(verbose=not args.quiet)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.validate:
        if input_path.is_file():
            converter_tool.validate_score(input_path)
        elif input_path.is_dir():
            for file in input_path.rglob("*"):
                if file.is_file() and file.suffix in ['.xml', '.musicxml', '.mid', '.krn']:
                    converter_tool.validate_score(file)

    elif args.batch:
        if not input_path.is_dir():
            print("Error: Input must be a directory for batch conversion")
            return

        converter_tool.batch_convert(input_path, output_path, args.format)

    else:
        if not input_path.is_file():
            print("Error: Input must be a file")
            return

        converter_tool.convert_file(input_path, output_path)

    print("\nExamples:")
    print("  # Convert single file")
    print("  python tools/convert_formats.py input.mscz output.musicxml")
    print()
    print("  # Batch convert directory to MIDI")
    print("  python tools/convert_formats.py scores/source/ scores/midi/ --format midi --batch")
    print()
    print("  # Validate all scores in directory")
    print("  python tools/convert_formats.py scores/musicxml/ . --validate")


if __name__ == "__main__":
    main()
