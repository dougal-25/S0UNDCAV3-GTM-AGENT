"""
The first judgment step ("reason"): is this thread an actual lead?

Uses a cheap model to score buying intent 0-100, tag the ICP segment, and
name the signal type. This is where the agent decides what's worth your time.
"""
import json
import os
from pathlib import Path

from anthropic import Anthropic

from ..config import SCORING_MODEL, SEGMENTS

_PROMPT = (Path(__file__).parent.parent / "prompts" / "score.md").read_text()
_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


def score(candidate: dict) -> dict:
    """
    Return the candidate enriched with: intent_score (int), segment (str),
    signal_type (str), reasoning (str), worth_engaging (bool).
    """
    user = (
        f"Community: r/{candidate['community']} (promo policy: {candidate['promo_policy']})\n"
        f"Segment hint: {candidate['segment_hint']}\n"
        f"Allowed segments: {', '.join(SEGMENTS)}\n\n"
        f"TITLE: {candidate['title']}\n\n"
        f"BODY:\n{candidate['body']}"
    )
    resp = _client.messages.create(
        model=SCORING_MODEL,
        max_tokens=400,
        system=_PROMPT,
        messages=[{"role": "user", "content": user}],
    )
    raw = "".join(b.text for b in resp.content if b.type == "text")
    try:
        data = json.loads(_strip_fences(raw))
    except json.JSONDecodeError:
        data = {"intent_score": 0, "segment": "Other / not ICP",
                "signal_type": "parse_error", "reasoning": raw[:300],
                "worth_engaging": False}
    return {**candidate, **data}
