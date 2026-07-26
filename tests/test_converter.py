from datetime import date
from pathlib import Path

from gemini_to_chatgpt_context.converter import (
    copy_attachments,
    filter_since,
    load_entries,
    write_archive,
)
from gemini_to_chatgpt_context.html_markdown import html_to_markdown


def test_html_to_markdown_preserves_basic_structure() -> None:
    source = "<h2>Title</h2><p>Hello <strong>world</strong>.</p><ul><li>One</li></ul>"
    assert html_to_markdown(source) == "## Title\n\nHello **world**.\n\n- One"


def test_archive_keeps_date_and_source_index(tmp_path: Path) -> None:
    source = tmp_path / "MyActivity.json"
    source.write_text(
        """[
          {"header":"Gemini Apps", "title":"Second", "time":"2025-01-02T00:00:00Z",
           "safeHtmlItem":[{"html":"<p>Answer</p>"}]},
          {"header":"Gemini Apps", "title":"First", "time":"2025-01-01T00:00:00Z",
           "subtitles":[{"name":"Prompted", "value":"Question"}]}
        ]""",
        encoding="utf-8",
    )
    destination = tmp_path / "output" / "gemini_conversations.md"
    write_archive(load_entries(source), destination)
    rendered = destination.read_text(encoding="utf-8")
    assert rendered.index("## 2025-01-01") < rendered.index("## 2025-01-02")
    assert "MyActivity.json[1]" in rendered
    assert "#### Prompted" in rendered
    assert "#### Gemini response" in rendered


def test_filter_since_is_inclusive_and_omits_unknown_dates(tmp_path: Path) -> None:
    source = tmp_path / "MyActivity.json"
    source.write_text(
        """[
          {"header":"Gemini Apps", "title":"Before", "time":"2026-03-29T23:59:59Z"},
          {"header":"Gemini Apps", "title":"Cutoff", "time":"2026-03-30T00:00:00Z"},
          {"header":"Gemini Apps", "title":"No time"}
        ]""",
        encoding="utf-8",
    )
    entries = filter_since(load_entries(source), date(2026, 3, 30))
    assert [entry.title for entry in entries] == ["Cutoff"]


def test_copy_attachments_creates_manifest_and_preserves_source(tmp_path: Path) -> None:
    source = tmp_path / "MyActivity.json"
    attachment = tmp_path / "report.pdf"
    attachment.write_bytes(b"sample pdf")
    source.write_text(
        """[
          {"header":"Gemini Apps", "title":"Read report", "time":"2026-03-30T00:00:00Z",
           "attachedFiles":["report.pdf", "missing.pdf", "../unsafe.pdf"]}
        ]""",
        encoding="utf-8",
    )
    destination = tmp_path / "output"
    result = copy_attachments(load_entries(source), tmp_path, destination)
    assert result.copied == 1
    assert result.missing == 1
    assert result.unsafe == 1
    assert attachment.read_bytes() == b"sample pdf"
    assert (destination / "attachments" / "report.pdf").read_bytes() == b"sample pdf"
    manifest = (destination / "attachments_manifest.md").read_text(encoding="utf-8")
    assert "missing" in manifest
    assert "unsafe path" in manifest
