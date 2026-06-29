# How I used AI to 10x my output

*Context: written for the Fleek **Organic Growth Lead — SEO & AI Search (AEO/GEO)**
application. The artifact referenced throughout is this repo: a go-to-market
system I designed and built solo, with AI doing the heavy lifting at every step.*

---

## TL;DR

I built a complete go-to-market engine — a market-listening AI agent, a content
strategy, a hooks library, and a live landing page — as one person, in days, not
months. AI wasn't a writing assistant bolted on at the end; it was the operating
system. That's the same way this role asks you to work: **AI-forward by default,
builder not briefer, experiment-driven, owning the number end to end.**

## What I built

A scheduled GTM agent for a music product's soft launch (SoundCave — AI media
generation for musicians). Each run it:

1. **Listens** in the communities where buyers actually are (Reddit, read-only).
2. **Scores** every thread for buying intent with a cheap model (Claude Haiku).
3. **Drafts** a genuinely helpful, peer-voice reply with a stronger model (Claude
   Sonnet), gated by each community's promo policy.
4. **Queues** qualified leads to Notion for human review — it never auto-posts.

Around that engine I built the growth motion it feeds: a documented strategy
(`wiki/spec/growth-strategy.md`), a 4-week content calendar, a hooks bank, and a
working waitlist landing page (`gtm/`). The whole thing was architected,
written, and documented with Claude Code.

> Honest status: the system is **code-complete, not yet live** (no production run
> executed). The point here is the *method and the output volume*, not vanity metrics.

## Where the AI leverage actually came from

| I did the thinking | AI multiplied the doing |
|---|---|
| Defined ICP, channels, guardrails | Wrote the pipeline, prompts, and docs |
| Decided what a "lead" is and the voice | Scores every thread + drafts every reply at volume |
| Set the content strategy | Generated the hooks bank + landing copy from real buyer language |
| Owned the architecture decisions | Built, refactored, and documented them as I went |

One person covered the work of a **researcher, copywriter, designer, SDR,
analyst, and engineer** — because each of those was an AI step I directed rather
than a hire I waited on.

## Why this maps to the Organic Growth Lead (SEO & AI Search) role

The role is written for exactly this way of working. Direct mapping:

- **"AI-forward by default — use LLMs and agents daily to multiply output."**
  The engine *is* an agent that does research, drafting, and monitoring on a
  schedule. AI is the default unit of work, not an afterthought.

- **"Win head questions through earned mentions in the sources LLMs actually cite
  — Reddit, YouTube, review sites."** My entire distribution strategy is
  help-first earned presence in those sources. That *is* AEO/GEO: be genuinely
  useful in the threads LLMs quote, so the product becomes part of the answer.
  I've already specced the target head questions and the agent that mines them
  (`gtm/hooks-bank.md`, `wiki/features/content_engine.md`).

- **"Builder, not briefer — ship the page yourself."** I designed and shipped the
  landing page (`gtm/landing/index.html`) and the programmatic-ready hooks bank
  myself — no agency, no waiting on a queue.

- **"Content across the full intent curve / programmatic pages from marketplace
  data."** The hooks bank is structured by segment × platform × hook type — the
  same template logic that scales to programmatic page generation. The agent's
  listening layer is a marketplace-data feed for content angles.

- **"Measurement — most AI search value is zero-click; build the instrumentation."**
  I baked a "How did you hear about us?" attribution field into the waitlist form
  and made signup-source tracking a first-class part of the strategy, precisely
  because the citations won't show as clicks.

- **"Experiment-driven — hypothesis, holdout, kill or scale."** The strategy's
  LEARN step is exactly this: track which hooks/communities/segments convert,
  cut what doesn't, pour into what does — the mechanism for going from the first
  100 users to the next 900.

## The one-paragraph version (paste-able)

> I use AI as my operating system, not a sidekick. For a recent product launch I
> built a full go-to-market engine solo: an AI agent that listens in the
> communities where buyers gather, scores every thread for intent with a cheap
> model, and drafts human-voice replies with a stronger one — plus the content
> strategy, hooks library, and a shipped landing page around it. AI did the work
> of a researcher, copywriter, designer, and SDR while I owned the strategy and
> the architecture. The distribution play is itself answer-engine optimisation:
> earn genuinely useful mentions in the Reddit/YouTube sources LLMs cite, so the
> product becomes part of the answer — with zero-click attribution instrumented
> from day one. That's how I'd own organic and AI search end to end: builder not
> briefer, experiment-driven, and AI-forward by default.

---

*Repo map: agent pipeline in `src/`; strategy and decisions in `wiki/`; growth
assets and the landing page in `gtm/`.*
