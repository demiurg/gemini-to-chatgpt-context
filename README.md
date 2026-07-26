# Gemini to ChatGPT Context

Turn a Google Takeout **Gemini Apps** export into a local, traceable Markdown
archive that can be curated for use in a ChatGPT Project.

This is a context migration, not a native chat-history import: ChatGPT cannot
recreate Gemini conversations in its sidebar.

The generated files become ChatGPT **Project sources** only when you upload
them through the ChatGPT Project UI. See the [delivery plan](docs/implementation-plan.md)
for the exact local-to-ChatGPT workflow.

## Quick start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
uv run gemini-to-chatgpt-context \
  "Takeout/My Activity/Gemini Apps/MyActivity.json" \
  --since 2026-03-30 \
  --output-dir output
```

The command creates `output/gemini_conversations.md`. Each entry retains its
timestamp and `MyActivity.json` record index.

`--since YYYY-MM-DD` is inclusive and filters in UTC. Omit it to process the
entire export.

## Development

```bash
uv run ruff check .
uv run pytest
uv build
```

## Privacy

Takeout exports and generated output may contain sensitive data. `Takeout/`,
Takeout ZIP files, and `output/` are ignored by Git. Review and redact context
before uploading it to any ChatGPT Project.

## Documentation

- [Export Gemini Apps activity with Google Takeout](docs/google-takeout.md)
- [Upload files to a ChatGPT Project](docs/chatgpt-handoff.md)
- [Migration guide](docs/migration-guide.md)
- [Architecture](docs/architecture.md)
- [Implementation plan](docs/implementation-plan.md)
- [Testing strategy](docs/testing.md)
- [Third-party notices](docs/third-party-notices.md)

## License

MIT. See [LICENSE](LICENSE).
