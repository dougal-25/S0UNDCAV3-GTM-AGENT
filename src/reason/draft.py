"""
The second judgment step ("reason"): draft the reply.

Writes a genuinely helpful, human, peer-to-peer reply. The community's
promo_policy gates whether SoundCave may be mentioned at all. You still
review and post every draft yourself -- the agent never speaks unattended.
"""
import os
from pathlib import Path

from anthropic import Anthropic

from ..config import DRAFTING_MODEL

_PROMPT = (Path(__file__).parent.parent / "prompts" / "draft.md").read_text()
_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def draft_reply(lead: dict) -> str:
    user = (
        f"Community: r/{lead['community']}\n"
        f"Promo policy: {lead['promo_policy']}\n"
        f"ICP segment: {lead.get('segment')}\n"
        f"Signal type: {lead.get('signal_type')}\n\n"
        f"THREAD TITLE: {lead['title']}\n\n"
        f"THREAD BODY:\n{lead['body']}"
    )
    resp = _client.messages.create(
        model=DRAFTING_MODEL,
        max_tokens=600,
        system=_PROMPT,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()
