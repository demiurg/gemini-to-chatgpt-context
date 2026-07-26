"""Command-line interface for Gemini to ChatGPT Context."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .converter import copy_attachments, filter_since, load_entries, write_archive


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
    parser.add_argument(
        "--copy-attachments",
        action="store_true",
        help="Copy attachments referenced by selected records into the output directory.",
    )
    args = parser.parse_args()

    entries = load_entries(args.input)
    if args.since:
        entries = filter_since(entries, args.since)
    archive = args.output_dir / "gemini_conversations.md"
    write_archive(entries, archive)
    print(f"Wrote {len(entries)} Gemini activity entries to {archive}")
    if args.copy_attachments:
        result = copy_attachments(entries, args.input.parent, args.output_dir)
        print(
            f"Copied {result.copied} attachments; {result.missing} missing, "
            f"{result.unsafe} skipped for unsafe paths."
        )
    return 0


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Expected a date in YYYY-MM-DD format.") from error
