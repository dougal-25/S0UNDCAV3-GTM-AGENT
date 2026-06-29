# CLAUDE.md — SoundCave GTM agent

Persistent project context for Claude Code. Read alongside `README.md` (full
setup, sheet schema, roadmap). This file is the **decisions and guardrails** —
not a re-description of the code. Keep it high-signal; every line should change
how you act.

## What this is

A scheduled go-to-market agent for SoundCave's soft launch. Each run it listens
in music communities, finds people who need release/event visuals and have no
design budget, scores buying intent, drafts a peer reply, and queues qualified
leads in a Google Sheet for a human to review and post. SoundCave = AI media generation
for music (flyers, cover/single/EP art, promo graphics) in named styles
(e.g. Etchings).

## Load-bearing decisions (do not quietly reverse these)

- **Human-in-the-loop, always.** The agent NEVER posts to any community. It only
  drafts and queues; the human engages. This is strategy, not caution: in music
  scenes conversions are peer-to-peer, and promo bots make communities hate you.
  Keep the human as the face.
- **v1 is a scheduled workflow with Claude doing the judgment — not a
  model-driven loop.** Discovery and listening are deterministic; the model only
  scores intent and drafts replies. This is the deliberate, cheaper, more
  debuggable choice. Do not refactor into a full agent loop unless a fixed
  pipeline genuinely can't express the goal (see "Agentic upgrade" in README).
- **Respect each community's `promo_policy`** (open / help_only / strict) in
  `config.py`. SoundCave may be named ONLY where policy is "open", and even then
  once, casually, never as an ad. Every draft helps first.
- **Google Sheets is the state.** (Was Notion; see
  `wiki/decisions/0002-sheets-as-state.md`.) The Actions runner is ephemeral —
  dedupe by Thread URL against the sheet; never assume local persistence.

## ICP (drives which rooms it lives in)

Independent DJs / electronic producers; event & club-night promoters; small
labels & artist managers; AND independent artists outside the dance scene
(singer-songwriters, bands, hip-hop, bedroom pop). The non-dance side is in
scope — keep it represented in `SEGMENTS` and `COMMUNITIES`.

## Conventions

- Project-specific repo. Credentials via env vars only; `.env` is gitignored;
  never commit keys, and never put them in this file.
- Models: Haiku for scoring (cheap, high-volume), Sonnet for drafting
  (quality-sensitive). Strings live in `config.py`, swappable.
- Tune the campaign in `config.py` (`COMMUNITIES`, `SEGMENTS`,
  `SIGNAL_KEYWORDS`, thresholds) — not in the loop.

## Where things live

- `wiki/` — intent & decisions (why/for whom). **Read `wiki/spec/overview.md` +
  relevant `wiki/features/*.md` before changing code.** If the wiki is silent on
  what you're building, write the spec page first and get sign-off.
- `src/run.py` — the loop: gather → score → draft → write → summarise
- `src/sources/reddit.py` — listening (PRAW, read-only, public threads)
- `src/reason/{classify,draft}.py` + `src/prompts/*.md` — the judgment steps
- `src/sinks/sheets.py` — append leads to the Google Sheet, dedupe by URL
- `.github/workflows/gtm-agent.yml` — daily cron + manual trigger

## Open threads / next up

1. Wire creds: a Google service account (`GOOGLE_SERVICE_ACCOUNT_JSON`) + the
   leads sheet id (`SHEET_ID`); share the sheet with the service account email.
   The sheet itself already exists ("SoundCave GTM — Leads").
2. v2 — generate a real SoundCave sample (Fal / Replicate) per lead and attach
   it to the draft. Highest conversion lever; build this next.
3. v2 — conversion tracking: a `Converted` status + weekly rollup by
   segment / community / signal type, to refocus the campaign.
4. Discord & Gearspace deferred (per-server bot invites; fragile reads). Add a
   Discord source only for servers where you're already a welcome regular.

## Don't

- Don't add auto-posting.
- Don't name SoundCave in help_only / strict communities.
- Don't put credentials in code, URLs, or this file.
