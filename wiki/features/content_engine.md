# Feature — Content engine (insight mode)

**Status:** Specced · **Not implemented** (documentation-only; next build after sign-off)

## Why

The v1 agent goes 1:1: each thread becomes one scored lead and one drafted
reply. The [growth strategy](../spec/growth-strategy.md) needs a *second* use of
the same listening layer — not "who do I reply to?" but "what should I make
content about, and in what words?". That's the LISTEN → EXTRACT half of the loop,
automated.

This is the highest-leverage upgrade for the content motion and it reuses
everything already built. It carries **zero bot risk**: its output is briefs for
a human, never posts.

## What it does

Runs on the *same* gathered threads as the lead agent, but aggregates across many
instead of acting on one:

1. **Listen** — reuse `src/sources/reddit.py::fetch_candidates` unchanged.
2. **Extract** — a new reason step (Haiku, batched) that pulls from a batch of
   threads:
   - **Pain points** in the ICP's own words (voice-of-customer language).
   - **Head questions** the ICP keeps asking (the AEO/GEO targets).
   - **Content angles** — what would make a great showcase post/video, tagged by
     segment + platform (Reddit/X) + hook type.
3. **Output** — a new sink writes a **content brief** (not a lead) to Notion (or
   a markdown digest): top pain points this week, ranked head questions, and
   3–5 suggested hooks ready to drop into [`gtm/hooks-bank.md`](../../gtm/hooks-bank.md).

## How it reuses the existing system

- **Source:** `src/sources/reddit.py` — no change.
- **Reason:** a sibling to `src/reason/classify.py` (same Anthropic client
  pattern, same fence-stripping JSON handling) with a new prompt
  `src/prompts/insights.md`.
- **Sink:** a sibling to `src/sinks/notion.py` writing to a "Content briefs" DB,
  or a markdown file for a zero-setup start.
- **Config:** add an `INSIGHT_MODE` switch / a separate entrypoint
  (`python -m src.insights`) so the lead loop and the insight loop run
  independently off the same cron.

## Acceptance criteria (when built)

- [ ] Aggregates a run's threads into pain points + head questions + content angles
- [ ] Tags each angle by segment, platform, and hook type
- [ ] Emits a human-readable weekly brief; no posting, no auto-publish
- [ ] Shares the Reddit source and client patterns with v1 (no duplication)

## Out of scope

- Generating the actual visuals (needs the SoundCave product pipeline; see the
  v2 sample-asset item in the [README roadmap](../../README.md)).
- Any auto-posting — forbidden by
  [decision 0001](../decisions/0001-architecture-and-guardrails.md).
