# Spec — Growth strategy: the first 100 users (and the next 900)

> **Why this page exists.** The agent finds and qualifies leads, but a queue of
> leads is not a growth motion. This is the motion: how SoundCave goes from a
> soft-launch waitlist to its first 100 real users, run as a *repeatable,
> instrumented process* so the same machine delivers the next 900. Read
> alongside [overview](overview.md) and
> [decision 0001](../decisions/0001-architecture-and-guardrails.md).

## The goal, stated plainly

**Get the first 100 real users.** That's it. Everything below is the cheapest,
most durable path to that number — built so nothing has to be reinvented for
user 101 through 1,000.

## Thesis

In music scenes you don't grow by advertising; you grow by being a genuinely
useful regular in the rooms your buyers already live in. So:

- **Content-led** — the work is creating things people want to see, not running ads.
- **Founder-led** — one real human (Doug), one personal account per platform.
- **Help-first** — every post earns its place by being useful on its own.
- **Show, don't sell** — SoundCave makes visuals; the visuals *are* the
  marketing. A jaw-dropping EP cover made in 20 seconds sells harder than any copy.
- **Drive to one place** — every piece of content points at the waitlist.

This is the same posture as the agent's
[guardrails](../decisions/0001-architecture-and-guardrails.md): never spam, never
auto-post, respect each room. That posture is also the bot-safety strategy (below).

## It's also an AEO/GEO play (answer-engine optimisation)

The same help-first motion doubles as **answer-engine optimisation**. When a
musician asks Google *or an LLM* "how do I make a cheap EP cover?", the answer is
increasingly assembled from the sources LLMs cite — **Reddit threads, YouTube
videos, roundups, review sites**. Earning genuinely useful, well-upvoted
mentions in those exact places is how SoundCave becomes part of the answer
without owning the page.

Practically, that means:

- **Target head questions** the ICP actually asks ("best tool for single cover
  art", "how do people afford gig posters", "AI cover art that doesn't look AI").
- **Win them via earned mentions + UGC**, not just our own pages — the agent's
  listening layer already surfaces these threads.
- **Instrument zero-click attribution**: a "How did you hear about us?" field on
  the waitlist, plus tracking which threads/videos get cited, because most of
  this value never shows up as a click.

## The repeatable loop

Deliberately mirrors the agent's pipeline so the human motion and the automated
motion are the same shape:

```
LISTEN → EXTRACT → CREATE → DISTRIBUTE → CAPTURE → CONVERT → LEARN
```

1. **Listen** — the existing Reddit listener (`src/sources/reddit.py`) surfaces
   what the ICP is asking and the exact words they use.
2. **Extract** — aggregate threads into pain points, voice-of-customer language,
   and content angles (the [content engine](../features/content_engine.md), next build).
3. **Create** — produce showcase content: generate real SoundCave visuals for
   real scenarios — before/after, style reveals, "10 covers in 2 minutes".
4. **Distribute** — post from one personal account. Reddit: help-first,
   story-framed, disclosed. X: build-in-public + visual demos.
5. **Capture** — every piece drives to the waitlist landing page (`gtm/landing/`).
6. **Convert** — onboard signups 1:1 and warm-DM the best leads (the agent's
   lead queue feeds this).
7. **Learn** — track which hooks/communities/segments convert; kill what doesn't,
   scale what does. This is what makes 100 → 1,000 a process, not luck.

## Channels

### Reddit — earn trust, then show
- **One personal/founder account.** Never a brand account in community subs — Reddit
  punishes those instantly. Build karma first by genuinely helping.
- **Respect each sub's `promo_policy`** (`src/config.py`): help-only in most,
  story-framed show-and-tell only where policy is `open` (e.g. r/musicmarketing).
- **Disclose** you're building SoundCave when it's relevant — undisclosed shilling
  is what gets you (and the product) hated. Disclosed help is welcomed.
- **No link-spam, no DM blasting.** The agent drafts; the human posts, in their voice.

### X — build in public
- **One personal/founder account.** Regular visual demos, before/afters, style
  showcases, pain-point threads.
- **Meta-content is a hook in itself**: "I built an AI agent to find SoundCave's
  first 100 users — here's what it learned about what musicians actually want."
- A branded `@soundcave` handle can run alongside later; the founder account leads.

See [`gtm/hooks-bank.md`](../../gtm/hooks-bank.md) for concrete opening lines and
[`gtm/content-calendar.md`](../../gtm/content-calendar.md) for cadence.

## Bot-safety rules (non-negotiable)

The fastest way to lose is to look like a bot or a spam ring:

- **One real account per platform.** No account farms — multi-account posting the
  same content is the #1 ban trigger on both Reddit and X.
- **A human posts every time.** The agent only drafts and queues; it never posts
  ([decision 0001](../decisions/0001-architecture-and-guardrails.md)).
- **Help-first, disclose, no link-spam.** Aged, genuine, useful accounts are
  invisible to spam filters.

## Cadence (first 4 weeks)

- **Week 0** — warm network (friends/industry test the tool); set up the two
  accounts; ship the waitlist landing page; seed first showcase pieces.
- **Weeks 1–4** — X roughly daily; Reddit 3–4 high-value posts/week; convert and
  log every signup's source.

## Definition of done & metrics

- **Done = 100 waitlist signups.**
- **Leading indicators:** posts/week, impressions, profile visits, click-through
  to the landing page, waitlist conversion %, and signup source ("how did you
  hear about us?") so winning channels are obvious.
- **Scaling to 1,000:** keep the loop, drop the channels/hooks that don't
  convert, and hand more of LISTEN/EXTRACT to the agent's content engine.

## Status

- **Strategy: defined** (this page). Assets shipped: hooks bank, content
  calendar, landing page (see `gtm/`).
- **Next build:** the agent [content engine](../features/content_engine.md) to
  automate LISTEN → EXTRACT.
- **Not yet live:** waitlist destination (landing page is a front-end mock until
  a form backend + domain are wired).
