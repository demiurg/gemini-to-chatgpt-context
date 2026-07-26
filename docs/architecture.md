# Architecture

## Current slice

```text
CLI → converter → HTML normalization → Markdown archive
```

`cli.py` owns argument parsing, `converter.py` parses and orders Gemini Apps
activity records, and `html_markdown.py` converts safe HTML response fragments.
The archive preserves a timestamp and source-array index for each record.

## Target architecture

```text
input detection → source parsing → normalization → provenance-aware archive
                                          └→ candidate extraction → review → curated outputs
```

| Component | Responsibility |
| --- | --- |
| `sources` | Detect extracted Takeout directories, JSON, and later ZIP exports; parse supported schema variants. |
| `models` | Typed activity, attachment, provenance, candidate, and review-decision records. |
| `normalize` | Convert HTML and normalize timestamps, text, and attachment paths without losing evidence. |
| `archive` | Group only with source evidence; render searchable chronological Markdown and manifests. |
| `candidates` | Produce dated, source-backed candidates for facts, decisions, projects, and tasks. |
| `review` | Store human approve/edit/reject decisions, redactions, conflicts, and freshness status. |
| `render` | Materialize reviewed `personal_context.md`, `open_tasks.md`, and topic files. |
| `cli` | Compose stages, provide dry-run/audit options, and never send data to a remote service by default. |

The raw export remains immutable evidence. Each derived item carries a source
record index, timestamp, and transformation/version metadata.
