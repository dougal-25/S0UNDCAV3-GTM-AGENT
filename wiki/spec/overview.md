# Spec — SoundCave GTM agent

## What it is

A scheduled go-to-market agent for **SoundCave's soft launch**. Each run it
listens in the music communities where SoundCave's buyers gather, finds people
who need release/event visuals and have no design budget, scores their buying
intent, drafts a genuinely helpful peer reply, and drops qualified leads into a
**Google Sheet** for Doug to review and post.

SoundCave = AI media generation for music (flyers, cover/single/EP art, promo
graphics, social posts) in named styles (e.g. Etchings), fast and cheap, for
people with no design budget or patience for a designer.

## Why it exists

In music scenes, conversion is **peer-to-peer**. You don't grow by advertising;
you grow by being a helpful regular in the rooms your buyers already live in.
The bottleneck is attention: Doug can't read every relevant subreddit daily.
This agent does the listening and the first-draft writing so Doug only spends
time on the human part — reviewing and posting in his own voice.

## The loop

```
gather  → pull candidate threads from Reddit matching a signal keyword   (PRAW, read-only)
reason  → score buying intent 0–100 + tag ICP segment                     (Claude Haiku)
reason  → draft a peer reply for leads that clear the bar                  (Claude Sonnet)
act     → append each qualified lead to a Google Sheet (dedupe by URL)
observe → print a run summary
```

## Who it targets (ICP)

- Independent DJs / electronic producers
- Event & club-night promoters
- Small labels & artist managers
- **Independent artists outside the dance scene** (singer-songwriters, bands,
  hip-hop, bedroom pop) — explicitly in scope; keep it represented in
  `SEGMENTS` and `COMMUNITIES`.

## What it is NOT

- **Not an auto-poster.** It NEVER posts to any community. It drafts and queues;
  the human engages. This is strategy, not caution — see
  [decision 0001](../decisions/0001-architecture-and-guardrails.md).
- **Not a model-driven agent loop** (in v1). It's a deterministic scheduled
  workflow with Claude making only the two judgment calls (is this a lead? /
  what's the reply?). Deliberate: cheaper, more predictable, easier to debug.
- **Not a promo cannon.** SoundCave is named only in communities whose
  `promo_policy` is `open`, and even there once, casually, never as an ad. Every
  draft helps first.

## State / source of truth

The GitHub Actions runner is ephemeral, so there is no local persistence —
**Google Sheets IS the state** ([decision 0002](../decisions/0002-sheets-as-state.md)).
Dedupe is by Thread URL against the sheet.

## Status

- **v1 loop: shipped** (adopted into dwcw 2026-06-25). See
  [feature page](../features/lead_discovery_and_queue.md).
- **Not yet live:** the leads sheet exists, but the service-account creds aren't
  wired and no run has executed yet.
- **Next (v2):** attach a real SoundCave sample asset per lead (the biggest
  conversion lever); conversion tracking. Both need a spec page + sign-off
  before building.
