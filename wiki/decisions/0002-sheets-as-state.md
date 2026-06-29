# 0002 — Google Sheets is the state (supersedes 0001 §4)

**Date:** 2026-06-29
**Status:** Accepted — supersedes decision **[0001](0001-architecture-and-guardrails.md) §4 ("Notion is the state")**.

## Context

v1 used a Notion database as the lead store and source of truth. In practice a
**Google Sheet is a better home** for this data: faster to build and reshape,
trivial to sort/filter/pivot, easier to share with collaborators, and a more
natural surface for the human review-and-post workflow (and for later conversion
tracking / weekly rollups). The owner explicitly preferred Sheets.

Nothing else about the architecture changes — the agent still only drafts and
queues, a human still posts, and the store is still the single source of truth
the ephemeral runner dedupes against.

## Decision

- **Google Sheets replaces Notion as the state.** One sheet ("SoundCave GTM —
  Leads") is the database. Dedupe is by the **Thread URL** column.
- The Notion sink (`src/sinks/notion.py`) is **retired** (removed; recoverable
  from git history). The new sink is `src/sinks/sheets.py`.
- **Auth:** a Google Cloud **service account** with the Sheets API enabled. Its
  JSON key lives in `GOOGLE_SERVICE_ACCOUNT_JSON` (a GitHub Actions secret in CI,
  `.env` locally); the sheet is shared with the service account's `client_email`
  as an Editor. The sheet key lives in `SHEET_ID`.
- **Columns** (the sheet's header row) are the source of truth for column order
  and MUST match `HEADERS` in `src/sinks/sheets.py` and the table in the README.

## Consequences

- Setup trades Notion's "integration token + share DB" for "service account +
  share sheet". Slightly more involved one-time setup, much nicer day-to-day.
- The "why it surfaced" reasoning and the draft reply, which lived in the Notion
  page **body**, are now their own **columns** in the sheet.
- This is a reversal of a load-bearing decision, recorded here per the wiki rule.
  Do not re-add a Notion sink without a follow-up decision.
- Unchanged: human-in-the-loop / never auto-post (0001 §1), scheduled workflow
  (0001 §2), promo-policy gating (0001 §3), Haiku-scores/Sonnet-drafts (0001 §5).
