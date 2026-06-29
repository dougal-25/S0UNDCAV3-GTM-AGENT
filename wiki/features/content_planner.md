# Feature — Content Planner (the full GTM loop)

**Status:** Specced · **Not built** (blueprint for the next phase). Builds on the
[content engine](content_engine.md) and the shipped [lead loop](lead_discovery_and_queue.md).

## Why

The v1 agent finds leads and drafts replies (1:1 outreach). The
[growth strategy](../spec/growth-strategy.md) needs more than that: a system where
the community itself directs **what content to make**, the content gets produced
and scheduled, and what converts feeds back in. This page specs that end-to-end
loop — research → script → create → publish → learn — with one human gate where
it matters.

It's the same listening infrastructure (`src/sources/reddit.py`) pointed at a
bigger job. The objective is unchanged and concrete: **the first 100 users, then
a repeatable engine for the next 900.**

## The loop

```
1. LISTEN    pull threads in the buyers' communities                  (built: sources/reddit.py)
2. MINE      → pain points, voice-of-customer language, head questions (content_engine.md)
3. DIRECT    findings steer: landing-page hooks · content angles · the questions to answer
4. SCRIPT    generate per-platform content: X thread, Reddit post, short-video script
5. PRODUCE   generate the visuals/video for each piece                 (SoundCave)
6. PLAN      assemble into a dated content calendar (auto-generated)
7. PUBLISH   X: scheduled/automated · Reddit: human-posted            (see rule below)
8. LEARN     track what converts → feeds back into step 2
```

Steps 1–6 and 8 are automatable and self-directing — the agent decides what's
worth making from what the community is actually saying. Step 7 has a deliberate
human gate.

## The publishing rule (load-bearing)

**Automate up to the post; automate X publishing; keep Reddit publishing human.**

- **X (own feed):** scheduling your own content is normal and safe — native X
  scheduling (free) or a free-tier scheduler (Buffer/Typefully). Fine to automate.
- **Reddit (community posts/replies):** a **human posts every time.** Auto-posting
  into communities is what gets accounts shadow-banned and brands hated, and it
  breaks the peer-to-peer trust that is the entire moat
  ([decision 0001 §1](../decisions/0001-architecture-and-guardrails.md)). The
  planner hands over a finished, scheduled post; the human pastes it and engages.

This keeps the system free, authentic, and un-bannable. The agent **never**
auto-posts to a community — unchanged from v1.

## Where SoundCave fits

SoundCave is **step 5 (PRODUCE)** — it generates the actual covers/flyers/video
the scripts call for, so the system is self-feeding: the product makes its own
marketing. Scheduling that output to X is fine to automate; to Reddit it stays
human. Same rule.

## How it reuses what exists

- **Listen/Mine:** `src/sources/reddit.py` + the [content engine](content_engine.md)
  insight step — no new listening code.
- **Script/Plan:** new reason steps + prompts (siblings of `src/reason/*`,
  `src/prompts/*`), emitting scripts and a calendar (extends
  [`gtm/content-calendar.md`](../../gtm/content-calendar.md) from hand-written to
  generated).
- **Hooks → landing:** scripts and hooks flow into
  [`gtm/hooks-bank.md`](../../gtm/hooks-bank.md) and the
  [hook-test landing pages](../../gtm/landing/README.md); the winning hook is
  promoted back.
- **Measure:** the waitlist's `variant` + "how did you hear about us?" fields
  (already built into the landing pages) are the learn-step signal.

## Acceptance criteria (when built)

- [ ] Turns a run's threads into ranked content angles + per-platform scripts
- [ ] Produces a dated content calendar a human can execute
- [ ] X items are schedule-ready; Reddit items are human-post-only (enforced)
- [ ] No auto-posting to any community; SoundCave used only for PRODUCE
- [ ] Closes the loop: conversion signal (variant / source) feeds the next cycle

## Out of scope

- The publishing integrations themselves (X scheduler, Reddit is manual) — wire
  after the planner emits content.
- Any change to the human-in-the-loop / never-auto-post guardrail.
