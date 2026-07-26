# ChatGPT Project handoff

## What to upload

Do **not** begin by uploading every archive chunk. The useful everyday context
should be compact, current, and reviewed.

Upload in this order once the corresponding files are available:

1. `personal_context.md` — durable preferences, constraints, decisions, and
   recurring projects.
2. `open_tasks.md` — active work and unresolved questions.
3. The 2–4 topic files relevant to current work, such as `housing.md`,
   `work.md`, or `parenting.md`.
4. `upload_manifest.md` — instructions and a map of the source files.
5. Only then, optional monthly archive files needed for historical lookup.

The current implementation produces only `gemini_conversations.md`, the raw
chronological archive. It is useful for inspection but is not yet the right
everyday upload file. Build the curated files first, then upload them.

## Fit the Project file limit

Current Project file limits are 5 files on Free, 25 on Go/Plus, and 40 on
Pro/Business/Enterprise/Edu. Choose files intentionally rather than treating a
Project as a complete backup. [OpenAI Projects documentation](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)

| Plan | Recommended upload set |
| --- | --- |
| Free (5 files) | `personal_context.md`, `open_tasks.md`, up to 2 active topic files, `upload_manifest.md`. No raw archive by default. |
| Go/Plus (25 files) | The 5 core files, then only the most useful recent/active monthly archive chunks. Reserve space for future topic files. |
| Pro/Business/Enterprise/Edu (40 files) | The core files, all valuable topic files, and selected archive chunks. Do not upload irrelevant history solely because capacity exists. |

If a topic becomes inactive, remove its archive chunk before removing a curated
file. The local `output/` directory remains the full archive of record.

## Create the Project

1. In ChatGPT, create a private Project named something like **Personal Gemini
   context**.
2. Choose **default memory** if you want the Project’s context to also help
   your general ChatGPT chats on a non-Enterprise account.
3. Upload the selected files, starting with the compact curated files.
4. Add these Project instructions:

   ```text
   Treat uploaded Gemini material as historical reference, not unquestioned fact.
   Prefer explicitly confirmed and newest dated information. For an ambiguous,
   sensitive, or conflicting item, ask me rather than assuming. Prefer
   personal_context.md and open_tasks.md over raw archive files.
   ```

5. Start a Project chat: “Summarize the active projects and open tasks in the
   uploaded sources. List conflicts or stale items that I should review.”

Files appear as **Project sources**. They do not become recreated Gemini chats
in the ChatGPT sidebar.

## Attachments

Run the converter with `--copy-attachments` to materialize files referenced by
the selected Gemini activity into `<output-dir>/attachments/`. Review
`attachments_manifest.md`, then manually upload only valuable documents and
essential images. The tool copies rather than moves them so that Takeout remains
the original evidence archive.

## Update cycle

When a decision or task changes, edit/regenerate the local curated file,
review the diff, and replace the matching Project source. Do not rely on an old
archive entry to represent current facts.
