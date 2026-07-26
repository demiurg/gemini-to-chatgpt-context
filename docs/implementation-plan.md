# Delivery plan

## The actual workflow

```text
Gemini Takeout → local catalog → archive + reports → curated context files
                                                        ↓
                                             upload through ChatGPT Project UI
```

The tool does not create ChatGPT conversations, nor can it place content in a
ChatGPT Project through a public end-user import API. Its job is to create the
best possible Project sources locally; the owner creates the Project and
uploads the selected files in ChatGPT.

## Outputs

```text
output/
├── reports/
│   ├── activity_summary.md       # counts, date range, missing-text/schema warnings
│   └── activity_by_date.csv      # daily and monthly frequency for charts/filtering
├── archive/
│   ├── gemini_activity_2025-01.md
│   └── ...                       # chronological, size-limited Markdown chunks
├── review/
│   ├── candidates.md             # proposed facts/tasks/topics with source IDs
│   └── review_queue.md           # conflicts, sensitive items, uncertain groupings
└── chatgpt-upload/
    ├── personal_context.md       # approved durable facts/preferences/projects
    ├── open_tasks.md             # approved active work and unresolved questions
    ├── topics/                   # approved focused files, only when useful
    └── upload_manifest.md        # recommended file order and Project instructions
```

`render` means writing these local Markdown files to disk. They appear in
ChatGPT only after the owner uploads selected files to a Project; they appear
there as **Project sources**, not as recreated Gemini chats.

## How categorization scales

1. **Catalog every activity record.** Create one normalized record with source
   index, timestamp, title, prompt/response text, and attachment references.
2. **Report before interpreting.** Generate daily/monthly frequency counts,
   date range, duplicate titles, missing text, and schema variants. This gives
   you a filterable map of thousands of records.
3. **Create the faithful archive.** Sort by timestamp, chunk by month and file
   size, and include the source index. If Takeout supplies a conversation ID,
   group on it; this export does not, so we must not invent exact chats.
4. **Classify candidates, not history.** Assign topic candidates such as
   housing/work/purchases using a transparent rule or model, with a confidence
   and source record. A record can have multiple topics.
5. **Extract candidates.** Identify possible durable facts, preferences,
   decisions, recurring projects, and open tasks. This is separate from
   archive conversion and remains reviewable at scale.
6. **Review and publish.** Only approved candidates become the compact files
   intended for upload to ChatGPT.

This keeps 5,000 records manageable: the archive is for lookup, reports are
for navigation, and the compact curated files are the high-value context.

## ChatGPT handoff

1. Create a private ChatGPT Project with **default memory** if you want its
   context to also help non-Project chats on a non-Enterprise account.
2. Upload `personal_context.md`, `open_tasks.md`, and relevant topic files.
   Add archive chunks only if you need historical lookup.
3. Paste the generated Project instructions from `upload_manifest.md`.
4. Ask a Project chat to identify stale or contradictory items; correct the
   local source files and upload replacements.

Project file limits currently depend on plan (5 Free; 25 Go/Plus; 40
Pro/Business/Enterprise/Edu), so the tool must produce a small upload set and
size-limited archive chunks. [Official Project documentation](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)

## Account access boundary

There are two separate optional integrations:

- **ChatGPT Project upload:** manual through the ChatGPT UI. This project has
  no consumer-ChatGPT account automation or API integration planned.
- **Model-assisted classification/extraction:** optional, future, and only
  after the user explicitly chooses a provider. An OpenAI API workflow would
  require an `OPENAI_API_KEY`, is separately billed from ChatGPT, and would
  send selected Takeout text to the API. The default remains local-only.

## Build order

1. Finish the local catalog and `activity_summary.md`/`activity_by_date.csv`.
2. Replace the single archive with month- and size-limited chunks plus a
   searchable index.
3. Implement deterministic filters: date range, text/title search, and source
   ID selection.
4. Add transparent topic-candidate classification and candidate extraction.
5. Add review decisions, redaction, conflict handling, and approved-file
   rendering.
6. Create `upload_manifest.md` and validate the upload set against the chosen
   ChatGPT plan's file limit.
7. Optionally add an explicitly configured API-assisted extraction provider.
