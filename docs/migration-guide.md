# Migration guide

## Scope

Google Takeout provides Gemini Apps data as an activity log, not a reliable
conversation archive. This tool writes a chronological Markdown archive and
does not invent thread boundaries that are absent from the source export.

The current converter reads:

```text
Takeout/My Activity/Gemini Apps/MyActivity.json
```

It normalizes response HTML and writes `gemini_conversations.md`, retaining the
original timestamp and source record index for each entry.

Use `--since YYYY-MM-DD` to make an inclusive UTC date-filtered archive. This
is useful when migrating only recent or personal Gemini activity; records with
an invalid or missing timestamp are excluded from a date-filtered export.

## What ChatGPT receives

ChatGPT does not receive a native Gemini-chat import. It receives Markdown
files you choose to upload in the ChatGPT Project UI. Those files appear as
Project sources and can be used as shared context; they do not become 5,000
individual conversations in the ChatGPT sidebar.

The intended upload set is a compact, reviewed `personal_context.md`,
`open_tasks.md`, and relevant topic files. The full archive is optional and is
for historical lookup, not daily context.

Do not treat the archive or model-generated summaries as authoritative without
checking their dated source records.

## Categorization and limitations

- A Gemini activity entry is not necessarily a complete chat.
- Gemini may omit or truncate response content in Takeout.
- Attachments are retained in the source export but are not yet linked in the
  generated archive.
- The tool will first provide frequency reports and exact filters, then topic
  and fact/task *candidates* with source references. It should never silently
  turn model inference into personal truth.
- Candidate fact/task extraction and a human review queue are planned work;
  see the [delivery plan](implementation-plan.md).

## Security

The local archive can include private financial, health, legal, employment,
housing, and third-party information. Keep the source export private, redact
unnecessary sensitive details, and upload only the minimum useful context.
