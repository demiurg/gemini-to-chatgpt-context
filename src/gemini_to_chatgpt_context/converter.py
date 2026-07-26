"""Parse Google Takeout Gemini Apps JSON and produce a traceable archive."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

from .html_markdown import html_to_markdown


@dataclass(frozen=True)
class ActivityEntry:
    source_index: int
    timestamp: datetime | None
    raw_time: str
    title: str
    response: str
    prompts: tuple[tuple[str, str], ...]


def load_entries(source: Path) -> list[ActivityEntry]:
    """Load recognized Gemini activity records from a Takeout JSON array."""
    payload = json.loads(source.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError("Expected MyActivity.json to contain a JSON array.")

    entries: list[ActivityEntry] = []
    for index, record in enumerate(payload):
        if not isinstance(record, dict) or "Gemini" not in str(record.get("header", "")):
            continue
        raw_time = str(record.get("time", ""))
        timestamp = _parse_time(raw_time)
        prompts = tuple(
            (str(item.get("name", "User")), str(item.get("value", "")).strip())
            for item in record.get("subtitles", [])
            if isinstance(item, dict) and item.get("value")
        )
        response = "\n\n".join(
            html_to_markdown(str(item.get("html", "")))
            for item in record.get("safeHtmlItem", [])
            if isinstance(item, dict) and item.get("html")
        ).strip()
        entries.append(
            ActivityEntry(
                source_index=index,
                timestamp=timestamp,
                raw_time=raw_time,
                title=str(record.get("title", "Untitled Gemini activity")).strip(),
                response=response,
                prompts=prompts,
            )
        )
    return sorted(
        entries,
        key=lambda entry: (entry.timestamp is None, entry.timestamp, entry.source_index),
    )


def write_archive(entries: list[ActivityEntry], destination: Path) -> None:
    """Write chronological activity entries grouped by UTC calendar date."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[ActivityEntry]] = defaultdict(list)
    for entry in entries:
        date = entry.timestamp.date().isoformat() if entry.timestamp else "Unknown date"
        grouped[date].append(entry)

    lines = [
        "# Gemini conversations archive",
        "",
        "This is a chronological activity archive. Entries are grouped by date and title; ",
        "they are not asserted to be original Gemini conversation threads.",
        "",
    ]
    for date, items in grouped.items():
        lines.extend([f"## {date}", ""])
        for entry in items:
            timestamp = (
                entry.timestamp.isoformat() if entry.timestamp else entry.raw_time or "unknown"
            )
            lines.extend(
                [
                    f"### {entry.title or 'Untitled Gemini activity'}",
                    "",
                    f"- Time: {timestamp}",
                    f"- Source record: `MyActivity.json[{entry.source_index}]`",
                    "",
                ]
            )
            for name, prompt in entry.prompts:
                lines.extend([f"#### {name}", "", prompt, ""])
            if entry.response:
                lines.extend(["#### Gemini response", "", entry.response, ""])
            if not entry.prompts and not entry.response:
                lines.extend(["_No text content was included in this activity record._", ""])
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def filter_since(entries: list[ActivityEntry], cutoff: date) -> list[ActivityEntry]:
    """Return entries created on or after ``cutoff`` in UTC.

    Records without a valid timestamp cannot be shown in a date-filtered export.
    """
    return [entry for entry in entries if entry.timestamp and entry.timestamp.date() >= cutoff]


def _parse_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)
