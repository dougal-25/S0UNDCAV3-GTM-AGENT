# Wiki

The brain of this project. LLM-maintained, human-curated. Code answers *what* and *how*; this wiki answers *why* and *for whom*.

## Structure

```
wiki/
├── index.md          # Catalogue of every page (always-current)
├── log.md            # Append-only chronological log of changes
├── spec/             # What we're building, who for, what it is NOT
│   └── overview.md
├── features/         # One page per feature: status, acceptance criteria, open questions
├── decisions/        # ADRs: every non-trivial choice + reasoning
├── personas/         # Target users — what they actually need
└── research/         # Competitor teardowns, references, user interviews
```

## Link style

Project wikis use **standard markdown** links — `[Overview](spec/overview.md)` — never `[[wikilinks]]`. Filenames repeat across projects, so wikilinks misroute. Markdown links are path-relative and work in GitHub, VS Code, and the terminal.

## Log entry format

`## [YYYY-MM-DD] <ingest|build|decision|lint> | <one-line summary>`

Then 1–3 bullet lines on what happened.
