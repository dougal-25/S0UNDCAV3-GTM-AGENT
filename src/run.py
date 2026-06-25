"""
SoundCave GTM agent -- run entrypoint.

This is the loop from the diagram, made concrete. For each community it:
  gather   -> pull candidate threads (sources/reddit.py)
  reason   -> score intent + tag segment (reason/classify.py)
  reason   -> draft a peer reply for the ones that clear the bar (reason/draft.py)
  act      -> write qualified leads into Notion (sinks/notion.py)
  observe  -> print a run summary you can read each morning

It is deliberately a SCHEDULED WORKFLOW with Claude making the judgment calls,
not a fully model-driven loop -- that's the right call for v1 (cheaper, more
predictable, easier to debug). See README for the upgrade path to a
model-driven agent and the v2 sample-asset step.

Run locally:   python -m src.run
On a schedule:  see .github/workflows/gtm-agent.yml
"""
import sys
import traceback

from .config import COMMUNITIES, INTENT_THRESHOLD, MAX_DRAFTS_PER_RUN
from .sources import reddit
from .reason import classify, draft as drafter
from .sinks import notion


def run() -> None:
    surfaced = 0
    drafts_made = 0
    scanned = 0

    for community in COMMUNITIES:
        if community["platform"] != "reddit":
            continue  # Discord etc. deferred to v2
        print(f"\n== r/{community['name']} ({community['promo_policy']}) ==")

        try:
            candidates = reddit.fetch_candidates(community)
        except Exception as e:
            print(f"  ! fetch failed: {e}")
            continue
        print(f"  {len(candidates)} candidate(s) matched a signal keyword")

        for cand in candidates:
            scanned += 1
            try:
                lead = classify.score(cand)
            except Exception as e:
                print(f"  ! score failed: {e}")
                continue

            tag = f"[{lead.get('intent_score', 0):>3}] {lead['title'][:60]}"
            if lead.get("intent_score", 0) < INTENT_THRESHOLD or not lead.get("worth_engaging"):
                print(f"  skip {tag}")
                continue

            try:
                if notion.url_exists(lead["url"]):
                    print(f"  seen {tag}")
                    continue
            except Exception as e:
                print(f"  ! dedupe check failed, skipping to be safe: {e}")
                continue

            if drafts_made >= MAX_DRAFTS_PER_RUN:
                print(f"  cap  {tag} (hit MAX_DRAFTS_PER_RUN)")
                continue

            try:
                reply = drafter.draft_reply(lead)
                drafts_made += 1
                notion.create_lead(lead, reply)
                surfaced += 1
                print(f"  ADD  {tag}  -> {lead.get('segment')}")
            except Exception as e:
                print(f"  ! draft/write failed: {e}")

    print(f"\n--- run complete: scanned {scanned}, surfaced {surfaced} new lead(s) to Notion ---")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
