# Landing pages — waitlist + hook testing

A small set of waitlist landing pages built to **test which hook converts best**.
The winning hook then feeds back into the [hooks bank](../hooks-bank.md) and the
content the [growth strategy](../../wiki/spec/growth-strategy.md) ships.

## Files

```
landing/
├── index.html                     # CONTROL (data-variant="control")
├── styles.css                     # shared styles — every page links this
├── app.js                         # shared form handler (tags signups by variant)
├── landing-copy.md                # the copy + rationale, as a reusable doc
└── variants/
    ├── pain-point/index.html      # hero: "Six pieces of artwork. By Friday. Again."
    ├── show-and-tell/index.html   # hero: "10 release-ready covers before your coffee goes cold."
    └── contrarian/index.html      # hero: "Stop paying £150 for cover art before the song's even out."
```

Open any `index.html` directly in a browser to preview it.

## The experiment

Every page is **identical except the hero hook** — same layout, same styles, same
offer. That isolation is the point: if one converts better, it's the *hook*, not
the design. Each page tags its `<body data-variant="…">`, and `app.js` includes
that `variant` value in the waitlist payload — so every signup is attributable to
the hook that produced it.

| Variant | Hook type | The angle it tests |
|---|---|---|
| `control` | Benefit / speed | "Release-ready artwork, in the time it takes to name the track." |
| `pain-point` | Pain-first | Names the recurring deadline grind every release |
| `show-and-tell` | Volume / speed proof | Quantified, visible result ("10 covers") |
| `contrarian` | Strong opinion | "Don't overspend before the song's proven" |

## How to run it (experiment-driven)

1. **Wire the form** to a real backend (the Apps Script webhook in
   `scripts/apps_script/Code.gs`, Formspree, or your API) so signups are captured
   with their `variant` tag.
2. **Deploy each page to its own URL** (any static host).
3. **Drive comparable traffic** to each — e.g. point different posts/ads at
   different variants, or use a split-test tool.
4. **Measure waitlist conversion %** per variant (signups ÷ visits).
5. **Kill the losers, scale the winner.** Promote the winning hook into the
   [hooks bank](../hooks-bank.md), the control page, and the post/video scripts.
6. **Re-test** as the [content planner](../../wiki/features/content_planner.md)
   surfaces new hooks from community listening — hook testing is a loop, not a
   one-off.

## Honesty note

These are front-end mocks: the form logs to the console and shows a thank-you
state until wired to a backend. The product is pre-launch — copy promises a
waitlist + early access, not a live product. Don't overstate; don't invent
testimonials or pricing.
