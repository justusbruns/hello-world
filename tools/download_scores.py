#!/usr/bin/env python3
"""
Schubert Score Downloader
Downloads machine-readable scores from various sources and organizes them.
"""

import os
import json
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse


class ScoreDownloader:
    """Download and organize Schubert scores from multiple sources."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.scores_dir = self.base_dir / "scores"
        self.metadata_dir = self.base_dir / "metadata"

    def download_from_url(self, url: str, work_id: str, category: str,
                          format_type: str, output_filename: Optional[str] = None) -> bool:
        """
        Download a score file from a URL.

        Args:
            url: Direct download URL
            work_id: Deutsch catalog number (e.g., "D667")
            category: Work category (lieder, chamber, piano, etc.)
            format_type: File format (musicxml, humdrum, midi, mei)
            output_filename: Optional custom filename

        Returns:
            True if download successful
        """
        try:
            # Determine output path
            format_dir = self.scores_dir / format_type / category
            format_dir.mkdir(parents=True, exist_ok=True)

            if not output_filename:
                # Extract extension from URL
                parsed = urlparse(url)
                ext = Path(parsed.path).suffix or self._get_extension(format_type)
                output_filename = f"{work_id}.{ext.lstrip('.')}"

            output_path = format_dir / output_filename

            # Download file
            print(f"Downloading {url}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Save file
            with open(output_path, 'wb') as f:
                f.write(response.content)

            print(f"✓ Saved to {output_path}")
            return True

        except Exception as e:
            print(f"✗ Error downloading {url}: {e}")
            return False

    def _get_extension(self, format_type: str) -> str:
        """Get file extension for format type."""
        extensions = {
            'musicxml': '.musicxml',
            'humdrum': '.krn',
            'midi': '.mid',
            'mei': '.mei',
            'mscz': '.mscz',
        }
        return extensions.get(format_type, '.xml')

    def download_from_imslp(self, work_id: str, imslp_url: str) -> bool:
        """
        Download scores from IMSLP page.

        Note: IMSLP requires manual navigation due to its structure.
        This method provides guidance on how to download.

        Args:
            work_id: Deutsch catalog number
            imslp_url: IMSLP work page URL
        """
        print(f"\n📚 IMSLP Download Instructions for {work_id}:")
        print(f"1. Visit: {imslp_url}")
        print(f"2. Look for files marked 'MusicXML', 'MuseScore', or 'MIDI'")
        print(f"3. Download and save to appropriate format folder")
        print(f"4. Rename file to: {work_id}_[title].{'{ext}'}")
        print()
        return False

    def clone_openscore_lieder(self) -> bool:
        """Clone the OpenScore Lieder corpus."""
        try:
            target_dir = self.base_dir / "external" / "OpenScore-Lieder"
            target_dir.parent.mkdir(parents=True, exist_ok=True)

            if target_dir.exists():
                print(f"OpenScore Lieder already cloned at {target_dir}")
                return True

            print("Cloning OpenScore Lieder Corpus (this may take a while)...")
            os.system(f"git clone https://github.com/OpenScore/Lieder.git {target_dir}")
            print(f"✓ Cloned to {target_dir}")

            # Find Schubert works
            print("\nSearching for Schubert works...")
            os.system(f"find {target_dir} -name '*Schubert*' -o -name '*schubert*'")

            return True

        except Exception as e:
            print(f"✗ Error cloning OpenScore Lieder: {e}")
            return False

    def update_catalog(self, work_id: str, score_path: str, format_type: str):
        """Update the catalog index with new score file."""
        catalog_path = self.metadata_dir / "catalog_index.json"

        try:
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)

            # Find work in catalog
            work_found = False
            for work in catalog.get('works', []):
                if work['work_id'] == work_id:
                    if 'score_files' not in work:
                        work['score_files'] = []
                    if score_path not in work['score_files']:
                        work['score_files'].append(score_path)
                    work_found = True
                    break

            if work_found:
                with open(catalog_path, 'w') as f:
                    json.dump(catalog, f, indent=2)
                print(f"✓ Updated catalog for {work_id}")
            else:
                print(f"⚠ Work {work_id} not found in catalog. Add metadata first.")

        except Exception as e:
            print(f"✗ Error updating catalog: {e}")


def main():
    parser = argparse.ArgumentParser(description='Download Schubert scores')
    parser.add_argument('--work-id', help='Deutsch catalog number (e.g., D810)')
    parser.add_argument('--url', help='Direct download URL')
    parser.add_argument('--category', choices=['lieder', 'chamber', 'piano',
                                               'symphonies', 'sacred', 'stage_works'],
                        help='Work category')
    parser.add_argument('--format', choices=['musicxml', 'humdrum', 'midi', 'mei', 'mscz'],
                        help='Score format')
    parser.add_argument('--openscore', action='store_true',
                        help='Clone OpenScore Lieder corpus')
    parser.add_argument('--list-priorities', action='store_true',
                        help='List priority works to download')

    args = parser.parse_args()

    downloader = ScoreDownloader()

    if args.list_priorities:
        print("\n🎵 Priority Schubert Works to Download:\n")
        priorities = [
            ("D759", "Symphony No. 8 'Unfinished'", "symphonies", "IMSLP"),
            ("D944", "Symphony No. 9 'Great'", "symphonies", "IMSLP"),
            ("D810", "String Quartet 'Death and the Maiden'", "chamber", "IMSLP, Kern"),
            ("D956", "String Quintet in C major", "chamber", "IMSLP"),
            ("D960", "Piano Sonata No. 21", "piano", "MuseScore, IMSLP"),
            ("D935", "Four Impromptus Op. 142", "piano", "MuseScore"),
            ("D328", "Erlkönig", "lieder", "OpenScore, MuseScore"),
            ("D839", "Ave Maria", "lieder", "OpenScore, MuseScore"),
            ("D795", "Die schöne Müllerin (cycle)", "lieder", "OpenScore"),
            ("D911", "Winterreise (cycle)", "lieder", "OpenScore"),
        ]

        for work_id, title, category, source in priorities:
            print(f"  {work_id} - {title}")
            print(f"    Category: {category}")
            print(f"    Best source: {source}")
            print()

        return

    if args.openscore:
        downloader.clone_openscore_lieder()
        return

    if args.work_id and args.url and args.category and args.format:
        success = downloader.download_from_url(
            args.url, args.work_id, args.category, args.format
        )
        if success:
            score_path = f"scores/{args.format}/{args.category}/{args.work_id}.{downloader._get_extension(args.format)}"
            downloader.update_catalog(args.work_id, score_path, args.format)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # List priority works")
        print("  python tools/download_scores.py --list-priorities")
        print()
        print("  # Clone OpenScore Lieder corpus")
        print("  python tools/download_scores.py --openscore")
        print()
        print("  # Download a specific score")
        print("  python tools/download_scores.py --work-id D810 --url https://example.com/score.xml \\")
        print("    --category chamber --format musicxml")


if __name__ == "__main__":
    main()
