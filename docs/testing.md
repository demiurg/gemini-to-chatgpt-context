# Testing strategy

## Principle

Tests must use small, synthetic, non-sensitive fixtures. A real Takeout export
is useful only for local manual smoke tests and must never be committed.

## Test layers

| Layer | What to test | Fixture approach |
| --- | --- | --- |
| Unit | HTML conversion, timestamp parsing, sorting, source references, empty/malformed fields. | Inline values or tiny JSON objects. |
| Parser | Known Takeout schema variants, BOM handling, missing response text, attachment metadata. | Versioned synthetic JSON files in `tests/fixtures/`. |
| Rendering | Markdown headings, escaping, stable ordering, manifests, output splitting. | In-memory models and snapshot-style expected text. |
| Integration | CLI exit codes and generated files. | Temporary directory plus a synthetic extracted Takeout layout. |
| Regression | Bugs reported from a private export. | Reduce to the smallest anonymized fixture before committing. |
| Property/fuzz | Randomly incomplete records and unusual Unicode/HTML should not crash the tool. | Generated records; add once parsers become more complex. |

## Do we need a mocked Takeout ZIP?

Not for the current JSON-only command. When ZIP or directory ingestion is
implemented, test it with a real ZIP *created during the test* using Python's
`zipfile` module and synthetic fixture contents. That validates path discovery,
archive safety, and parsing better than mocking `ZipFile`, while requiring no
private export. Unit tests can still mock filesystem errors when testing error
messages.

## Coverage target

Use branch coverage for the local package. Early on, prioritize full coverage
of loss/error paths over an arbitrary percentage. Before the candidate/review
pipeline is released, require at least 90% branch coverage and a regression
fixture for every fixed parsing bug.

Run locally:

```bash
uv run pytest --cov=gemini_to_chatgpt_context --cov-report=term-missing
```
