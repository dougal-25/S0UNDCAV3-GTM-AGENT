# 0001 — Architecture & guardrails

**Date:** 2026-06-25 (recorded at adoption; decisions predate this and came with
the generated v1)
**Status:** Accepted — load-bearing. Do not quietly reverse.

## Context

A GTM agent for a music-product soft launch. The obvious temptation is to build
a fully model-driven agent that clicks around communities and posts on its own.
That is the wrong shape for this domain.

## Decisions

### 1. Human-in-the-loop, always — the agent never posts
The agent only drafts and queues; the human reviews and posts. In music scenes
conversions are peer-to-peer and promo bots make communities **hate** you. Doug
stays the face. This is a strategy decision, not a caution setting.

### 2. v1 is a scheduled workflow, not an agent loop
Discovery and listening are deterministic — there's no reason to let a model
click around Reddit. The model sits only where judgment is needed: *is this a
real lead?* (score) and *what's the right reply?* (draft). Cheaper, more
predictable, far easier to debug. Upgrade to a model-driven loop only when a
fixed pipeline genuinely can't express the goal (see README "Agentic upgrade").

### 3. Promo-policy gating per community
Each community in `config.py` carries a `promo_policy`: `open` / `help_only` /
`strict`. SoundCave may be named ONLY where policy is `open`, and even there
once, casually, never as an ad. Every draft helps first. Misjudging this burns
the community permanently.

### 4. Notion is the state — _SUPERSEDED by [0002](0002-sheets-as-state.md)_
The Actions runner is ephemeral — no local persistence. Dedupe by Thread URL
against the store. Never assume a local store survives between runs. _(The store
is now a **Google Sheet**, not Notion — see [decision 0002](0002-sheets-as-state.md).
The ephemeral-runner / dedupe-by-URL principle is unchanged.)_

### 5. Model split: Haiku scores, Sonnet drafts
Scoring is high-volume and cheap → Haiku. Drafting is low-volume and
quality-sensitive → Sonnet. Model IDs live in `config.py`, swappable.

## Consequences

- Tuning the campaign (communities, segments, keywords, thresholds) happens in
  `config.py`, never in the loop.
- Adding auto-posting, or naming SoundCave in `help_only`/`strict` rooms, is a
  reversal of a load-bearing decision and must not happen silently.
