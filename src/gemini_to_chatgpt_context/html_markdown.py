"""Small, dependency-free HTML normalization for Takeout response fragments.

The structure follows the approach credited in docs/third-party-notices.md, but uses
``html.parser`` so text content and entity decoding are handled safely.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser


class _MarkdownParser(HTMLParser):
    _block_tags = {"p", "div", "section", "article", "blockquote", "pre"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._list_depth = 0
        self._in_pre = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"br", "hr"}:
            self.parts.append("\n")
        elif tag in self._block_tags:
            self.parts.append("\n\n")
        elif tag in {"ul", "ol"}:
            self._list_depth += 1
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n" + "  " * max(self._list_depth - 1, 0) + "- ")
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self._in_pre:
            self.parts.append("`")
        elif tag == "pre":
            self._in_pre = True
            self.parts.append("\n\n```\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._block_tags:
            self.parts.append("\n\n")
        elif tag in {"ul", "ol"}:
            self._list_depth = max(0, self._list_depth - 1)
            self.parts.append("\n")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self._in_pre:
            self.parts.append("`")
        elif tag == "pre":
            self._in_pre = False
            self.parts.append("\n```\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_markdown(value: str) -> str:
    """Convert a Gemini HTML fragment to readable, conservative Markdown."""
    if not value:
        return ""
    parser = _MarkdownParser()
    parser.feed(value)
    parser.close()
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
