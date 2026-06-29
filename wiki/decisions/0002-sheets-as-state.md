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
- **Auth:** an **Apps Script web app** bound to the sheet (`scripts/apps_script/Code.gs`),
  deployed to run as the sheet owner. The agent POSTs lead rows to its `/exec`
  URL (`SHEETS_WEBHOOK_URL`, optional shared secret `SHEETS_WEBHOOK_TOKEN`). No
  Google Cloud, no service-account keys. _(We started with a service account but
  the owner's Workspace org enforces `iam.disableServiceAccountKeyCreation`,
  which blocks downloadable keys — the Apps Script route sidesteps it entirely.)_
- **Columns** (the sheet's header row) are the source of truth for column order
  and MUST match `HEADERS` in `src/sinks/sheets.py` and the table in the README.

## Consequences

- Setup trades Notion's "integration token + share DB" for "paste + deploy an
  Apps Script web app". Comparable one-time effort, no external credentials, and
  a much nicer surface day-to-day.
- The "why it surfaced" reasoning and the draft reply, which lived in the Notion
  page **body**, are now their own **columns** in the sheet.
- This is a reversal of a load-bearing decision, recorded here per the wiki rule.
  Do not re-add a Notion sink without a follow-up decision.
- Unchanged: human-in-the-loop / never auto-post (0001 §1), scheduled workflow
  (0001 §2), promo-policy gating (0001 §3), Haiku-scores/Sonnet-drafts (0001 §5).
