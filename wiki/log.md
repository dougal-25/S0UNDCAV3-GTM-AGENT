# Log

Append-only. Most recent at bottom.

## [2026-06-25] adopt | brought into dwcw as its own repo
- Moved generated v1 from `Downloads/SOUNDCAVE MARKETING/` into
  `projects/soundcave-gtm-agent/`; git-init'd as an independent repo, excluded
  from the dwcw monorepo via root `.gitignore` per-project block.
- Fixed a local-run bug: `python-dotenv` was in requirements but `load_dotenv()`
  was never called, so `python -m src.run` would KeyError on import. Now loaded
  in `src/__init__.py` before the Anthropic clients are built. No-op on Actions.
- Hardened project `.gitignore`; installed gitleaks pre-push secret guard +
  `.gitleaks.toml`.
- Seeded wiki: spec/overview, decision 0001 (architecture & guardrails),
  feature page for the v1 loop.
- Still not live: Notion DB not created, creds not wired, no run executed yet.
