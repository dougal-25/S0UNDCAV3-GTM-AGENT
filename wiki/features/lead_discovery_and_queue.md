# Feature — Lead discovery & lead queue (v1 loop)

**Status:** Shipped (code complete) · **Not yet live** (creds not wired, no run executed)

## What it does

The end-to-end v1 loop. For each configured subreddit:

1. **gather** — `src/sources/reddit.py` pulls recent posts + targeted keyword
   searches via PRAW (read-only), keeps those matching a `SIGNAL_KEYWORDS`
   phrase, dedupes by post id.
2. **score** — `src/reason/classify.py` (Haiku) rates buying intent 0–100, tags
   the ICP segment, names the signal type, returns `worth_engaging`.
3. **gate** — leads below `INTENT_THRESHOLD` or `worth_engaging=false` are
   skipped; already-queued threads (by URL) are skipped; drafting stops at
   `MAX_DRAFTS_PER_RUN`.
4. **draft** — `src/reason/draft.py` (Sonnet) writes a peer reply, gated by the
   community's `promo_policy`.
5. **act** — `src/sinks/sheets.py` appends the lead as a row to the Google Sheet
   (one column per field, incl. "why it surfaced" + draft reply), deduped by
   Thread URL ([decision 0002](../decisions/0002-sheets-as-state.md)).
6. **observe** — `src/run.py` prints a run summary.

## Config knobs (`src/config.py`)

- `COMMUNITIES` — subs + per-sub `promo_policy` and `segment_hint`
- `SEGMENTS` — ICP segments the classifier may assign
- `SIGNAL_KEYWORDS` — broad recall net; precision is the model's job
- `INTENT_THRESHOLD` (60), `POSTS_PER_COMMUNITY` (25), `SEARCH_LIMIT` (15),
  `MAX_DRAFTS_PER_RUN` (20)

## Acceptance criteria

- [x] Pulls candidates from each configured sub without one sub's failure
      killing the run
- [x] Scores intent + segment; only surfaces leads ≥ threshold
- [x] Drafts respect `promo_policy` (SoundCave named only in `open` rooms)
- [x] Writes to the Google Sheet with dedupe by Thread URL
- [x] Local runs load `.env` (fixed at adoption — was missing `load_dotenv()`)
- [x] Leads sheet created with the exact column schema (see README)
- [ ] Creds wired (`.env` locally / repo secrets for Actions)
- [ ] First real run executed and reviewed

## Known gaps / next

- **v2 — sample asset in the draft:** generate a real SoundCave flyer/cover per
  lead (Fal/Replicate) and attach it. README calls this the single biggest
  conversion lever. Needs a spec page + sign-off before building.
- **v2 — conversion tracking:** `Converted` status + weekly rollup by
  segment/community/signal type.
- Discord & Gearspace sources deferred (per-server bot invites; fragile reads).

## History

- 2026-06-25 — adopted into dwcw; fixed the local-run `.env` loading bug.
