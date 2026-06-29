# SoundCave GTM Agent

**Finds real buyers in public communities, scores their intent with Claude, and writes you a ready-to-send, personalized reply for each — queued to a Google Sheet for human review. It never auto-posts.**

A small, scheduled AI system built for the SoundCave soft launch. Each run it listens in the music communities where your buyers gather, finds people who need release/event visuals and have no design budget, scores how real each lead is, drafts a genuinely helpful peer reply for the good ones, and drops them into a Google Sheet. **You stay the human who engages.**

This repo is more than the script: it's an **end-to-end, AI-built GTM system** — the listening **agent** (`src/`), the **growth strategy** it feeds (`wiki/spec/growth-strategy.md`), and the **executable marketing assets** to run it (`gtm/` — hooks bank, content calendar, waitlist landing page). The goal is concrete: **the first 100 real users, then a repeatable process for the next 900.**

```
listen  →  pull candidate threads from Reddit matching a buying signal
score   →  rate intent 0–100 + tag the ICP segment         (Claude Haiku)
draft   →  write a peer reply for leads that clear the bar   (Claude Sonnet)
queue   →  append each qualified lead to a Google Sheet for review
```

> **Why it's built this way.** Discovery and listening are deterministic — there's no reason to let a model click around Reddit. So this v1 is a scheduled workflow with Claude making only the judgment calls (*is this a real lead?* and *what's the right reply?*), not a fully model-driven loop. It's cheaper, more predictable, and far easier to debug. The upgrade path to a genuinely agentic loop is in the [Roadmap](#roadmap).

## Who it targets (ICP)

Independent DJs and electronic producers; event/club-night promoters; small
labels and artist managers; **and independent artists outside the dance scene**
(singer-songwriters, bands, hip-hop, bedroom pop). Edit `src/config.py`
(`COMMUNITIES`, `SEGMENTS`, `SIGNAL_KEYWORDS`) to retune the campaign.

## Growth strategy — the first 100 users

The agent finds leads; the [growth strategy](wiki/spec/growth-strategy.md) turns
them into users. It's a content-led, founder-led, help-first motion run from one
personal account per platform (X + Reddit), built as a repeatable loop:

```
LISTEN → EXTRACT → CREATE → DISTRIBUTE → CAPTURE → CONVERT → LEARN
```

The same help-first motion is also an **AEO/GEO play**: earn genuinely useful
mentions in the sources LLMs cite (Reddit, YouTube, roundups) so SoundCave
becomes part of the answer when someone asks "how do I make a cheap EP cover?".
Bot-safety is built in — one real account, a human posts every time, the agent
never does. Full write-up, channels, cadence, and metrics:
[`wiki/spec/growth-strategy.md`](wiki/spec/growth-strategy.md).

## Marketing assets (`gtm/`)

Ready-to-run collateral for the campaign:

- [`gtm/hooks-bank.md`](gtm/hooks-bank.md) — opening lines by hook type, segment, and AEO target question.
- [`gtm/content-calendar.md`](gtm/content-calendar.md) — a 4-week rollout cadence + per-post checklist.
- [`gtm/landing/index.html`](gtm/landing/index.html) — a working waitlist landing page (open it in a browser); copy in [`landing-copy.md`](gtm/landing/landing-copy.md).

## The Google Sheet

Leads are appended as rows to a Google Sheet — **Sheets is the state**
([decision 0002](wiki/decisions/0002-sheets-as-state.md)). The first row is a
header with these columns, **in this exact order** (the code in
`src/sinks/sheets.py` matches on it):

| Column          | Notes                                            |
|-----------------|--------------------------------------------------|
| `Thread`        | The thread title                                 |
| `Community`     | e.g. `r/edmproduction`                           |
| `ICP segment`   | matches `SEGMENTS` in config                     |
| `Intent score`  | 0–100                                            |
| `Signal type`   | e.g. `needs_flyer`, `design_cost_complaint`      |
| `Promo policy`  | `open` / `help_only` / `strict`                  |
| `Status`        | seeded with `New`; add `Reviewing/Posted/Converted` |
| `Author`        | Reddit username                                  |
| `Thread URL`    | used for dedupe — must exist                     |
| `Why it surfaced` | the classifier's one-line reasoning            |
| `Draft reply`   | the Sonnet-drafted reply to review before posting |
| `Date added`    | ISO date the lead was appended                   |

Unlike the old Notion version, the "why it surfaced" note and the draft reply are
their own **columns**, not a page body.

## Setup

1. **Reddit API creds**: create a "script" app at
   <https://www.reddit.com/prefs/apps> → gives you a client id + secret.
2. **Google Sheets**: in Google Cloud, create a **service account** with the
   **Sheets API** enabled and download its JSON key. Create (or reuse) the leads
   sheet with the header row above, **share it with the service account's
   `client_email` as an Editor**, and copy the sheet key from its URL
   (`docs.google.com/spreadsheets/d/<SHEET_ID>/edit`). Put the full JSON in
   `GOOGLE_SERVICE_ACCOUNT_JSON` and the key in `SHEET_ID`.
3. **Anthropic**: an API key from the Anthropic console.
4. Copy `.env.example` → `.env` and fill it in (local runs), **or** add the same
   keys as GitHub repository secrets (scheduled runs).

## Run it

Local, on demand:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# put creds in .env, then:
python -m src.run
```

On a schedule: push to GitHub, add the secrets, and `.github/workflows/gtm-agent.yml`
runs it daily at ~8am UK. Trigger a manual run any time from the **Actions** tab
(`Run workflow`) to test.

## Tuning

- `INTENT_THRESHOLD` — raise for fewer, higher-quality leads.
- `POSTS_PER_COMMUNITY` / `SEARCH_LIMIT` — how deep it scans per sub.
- `MAX_DRAFTS_PER_RUN` — cost guardrail on drafting calls.
- `COMMUNITIES` — add/remove subs and set each one's `promo_policy` honestly.

## Roadmap

**v2**
- **Content engine (insight mode)**: reuse the Reddit listener to aggregate
  threads into pain points, head questions, and content angles — feeding the
  [growth strategy](wiki/spec/growth-strategy.md) instead of going 1:1. Specced
  in [`wiki/features/content_engine.md`](wiki/features/content_engine.md).
- **Sample asset in the outreach**: call your SoundCave pipeline (Fal/Replicate)
  to generate an actual flyer/cover in the relevant style and attach it to the
  draft. This is the single biggest conversion lever.
- **Conversion tracking**: a `Converted` status + a weekly rollup of which
  segments/communities/signal types actually convert, to refocus the campaign.
- **Discord & Gearspace**: deferred from v1 because Discord needs a bot invited
  per server and Gearspace reading is fragile. Add a Discord bot source once you
  have a couple of servers where you're a welcome regular.

**Agentic upgrade** (when judgment about *what to do next* starts mattering)
Re-home the loop in the Claude Agent SDK / Claude Code so the model itself
decides each run: which communities to prioritise this week, whether to go
deeper on a hot thread, when to generate a sample vs. just reply. Same tools
(Reddit, Google Sheets, SoundCave, web search) become its action space; the cron just
triggers it. Reach for this only when a fixed pipeline genuinely can't express
what you want — not before.
