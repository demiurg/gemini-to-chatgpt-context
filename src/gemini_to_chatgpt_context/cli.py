"""Command-line interface for Gemini to ChatGPT Context."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .converter import filter_since, load_entries, write_archive


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Gemini Apps Takeout JSON to a Markdown archive."
    )
    parser.add_argument("input", type=Path, help="Path to MyActivity.json")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("output"), help="Generated-file directory"
    )
    parser.add_argument(
        "--since",
        type=_parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activity records on or after this UTC date.",
    )
    args = parser.parse_args()

    entries = load_entries(args.input)
    if args.since:
        entries = filter_since(entries, args.since)
    archive = args.output_dir / "gemini_conversations.md"
    write_archive(entries, archive)
    print(f"Wrote {len(entries)} Gemini activity entries to {archive}")
    return 0


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Expected a date in YYYY-MM-DD format.") from error
