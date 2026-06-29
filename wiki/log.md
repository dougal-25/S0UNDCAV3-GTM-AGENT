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

## [2026-06-29] build | content GTM strategy + growth assets + Fleek application pack
- Added the growth motion the agent feeds into: `wiki/spec/growth-strategy.md`
  (first-100-users content loop, Reddit/X channels, AEO/GEO framing, bot-safety,
  metrics) and `wiki/features/content_engine.md` (next build: insight mode reusing
  the Reddit source — specced, not implemented).
- Created `gtm/`: hooks bank, 4-week content calendar, and a working waitlist
  landing page (`gtm/landing/index.html` + standalone copy). No backend yet.
- Added `docs/ai-leverage-summary.md` — "how I used AI to 10x output," mapped to
  the Fleek Organic Growth Lead (SEO & AI Search / AEO/GEO) role.
- Reframed `README.md` to present the repo as an end-to-end AI-built GTM system
  (agent + strategy + assets). No agent code touched.

## [2026-06-29] decision | Google Sheets replaces Notion as the state
- ADR `wiki/decisions/0002-sheets-as-state.md` supersedes 0001 §4. The lead store
  is now a Google Sheet ("SoundCave GTM — Leads"), dedupe still by Thread URL.
- Code: new `src/sinks/sheets.py` (gspread + service account); `run.py` rewired;
  `src/sinks/notion.py` removed; `requirements.txt` swaps `requests` for
  `gspread`/`google-auth`.
- Secrets: `.env.example` + workflow now use `GOOGLE_SERVICE_ACCOUNT_JSON` +
  `SHEET_ID` instead of `NOTION_API_KEY` / `NOTION_DB_ID`.
- Created the actual sheet in Doug's Drive (headers in place). Still to do: wire
  the service-account creds and run once.
- Updated CLAUDE.md, README, and all wiki references from Notion → Sheets.
