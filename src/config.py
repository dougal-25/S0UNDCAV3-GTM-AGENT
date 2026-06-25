"""
Central configuration for the SoundCave GTM agent.

Everything that defines WHERE the agent looks and WHAT counts as a lead lives
here, so you can tune the campaign without touching the loop logic.
"""

# ---------------------------------------------------------------------------
# Models (swappable). Scoring is high-volume + cheap -> Haiku.
# Drafting is low-volume + quality-sensitive -> Sonnet.
# ---------------------------------------------------------------------------
SCORING_MODEL = "claude-haiku-4-5-20251001"
DRAFTING_MODEL = "claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Ideal customer profile segments. The classifier tags each thread with one.
# ---------------------------------------------------------------------------
SEGMENTS = [
    "DJ / electronic producer",
    "Event / club-night promoter",
    "Small label / artist manager",
    "Indie artist (non-dance)",   # singer-songwriters, bands, hip-hop, bedroom pop
    "Other / not ICP",
]

# ---------------------------------------------------------------------------
# Communities to listen in.
#   promo_policy:  "open"      -> you can mention SoundCave directly (sparingly)
#                  "help_only" -> help genuinely, no product mention
#                  "strict"    -> heavy anti-promo mods; help only, extra care
#   segment_hint:  the ICP segment most concentrated here (a steer, not a rule)
# Discord servers and Gearspace are deferred to v2 (they need per-server bot
# invites or are fragile to read) -- see README.
# ---------------------------------------------------------------------------
COMMUNITIES = [
    # --- dance / electronic ---
    {"name": "edmproduction",     "platform": "reddit", "promo_policy": "help_only", "segment_hint": "DJ / electronic producer"},
    {"name": "DJs",               "platform": "reddit", "promo_policy": "help_only", "segment_hint": "DJ / electronic producer"},
    {"name": "Beatmatch",         "platform": "reddit", "promo_policy": "help_only", "segment_hint": "DJ / electronic producer"},
    {"name": "DJsetups",          "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Event / club-night promoter"},

    # --- broad creator base (dance + non-dance) ---
    {"name": "WeAreTheMusicMakers", "platform": "reddit", "promo_policy": "strict",    "segment_hint": "Indie artist (non-dance)"},
    {"name": "musicproduction",     "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Indie artist (non-dance)"},
    {"name": "musicians",           "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Indie artist (non-dance)"},
    {"name": "songwriting",         "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Indie artist (non-dance)"},
    {"name": "makinghiphop",        "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Indie artist (non-dance)"},
    {"name": "independentmusic",    "platform": "reddit", "promo_policy": "help_only", "segment_hint": "Indie artist (non-dance)"},

    # --- marketing / promo intent (highest buying signal) ---
    {"name": "musicmarketing",    "platform": "reddit", "promo_policy": "open",      "segment_hint": "Small label / artist manager"},
]

# ---------------------------------------------------------------------------
# High-intent phrases. A thread matching any of these is a candidate; the
# classifier then decides if it's a real lead. Keep these broad -- precision
# is the model's job, recall is the keyword list's job.
# ---------------------------------------------------------------------------
SIGNAL_KEYWORDS = [
    # asset needs
    "flyer", "gig poster", "event poster", "cover art", "album art",
    "single artwork", "single cover", "ep cover", "artwork for my",
    "promo graphic", "promo image", "social media post", "instagram post",
    "visualizer", "visualiser", "lyric video",
    # cost / friction signals
    "hire a designer", "afford a designer", "cost of artwork", "design budget",
    "cheap cover", "free cover art", "where do you get your artwork",
    "who makes your", "how do you make your flyers",
    # tool-seeking
    "canva for music", "design tool", "ai cover", "ai artwork", "ai flyer",
    "tool to make", "app to make",
]

# ---------------------------------------------------------------------------
# How many recent + search-matched posts to pull per community per run,
# and the minimum intent score (0-100) required to surface a lead to Notion.
# ---------------------------------------------------------------------------
POSTS_PER_COMMUNITY = 25       # recent posts scanned per sub
SEARCH_LIMIT = 15              # keyword-search hits scanned per sub
INTENT_THRESHOLD = 60          # only surface leads scoring >= this
MAX_DRAFTS_PER_RUN = 20        # safety cap on drafting calls per run
