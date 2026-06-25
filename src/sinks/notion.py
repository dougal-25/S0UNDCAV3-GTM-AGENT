"""
The "act" / output step: write qualified leads into a Notion database.

Dedupes by Thread URL so re-runs don't create duplicates (the GitHub Actions
runner is ephemeral, so we keep no local state -- Notion IS the state).
Property names below MUST match your Notion database exactly (see README).
"""
import os
import requests

NOTION_VERSION = "2022-06-28"
_BASE = "https://api.notion.com/v1"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def url_exists(url: str) -> bool:
    """True if a lead with this Thread URL is already in the database."""
    db_id = os.environ["NOTION_DB_ID"]
    r = requests.post(
        f"{_BASE}/databases/{db_id}/query",
        headers=_headers(),
        json={"filter": {"property": "Thread URL", "url": {"equals": url}}, "page_size": 1},
        timeout=30,
    )
    r.raise_for_status()
    return len(r.json().get("results", [])) > 0


def _paragraphs(text: str) -> list[dict]:
    blocks = []
    for chunk in [p for p in text.split("\n") if p.strip()][:40]:
        blocks.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk[:1900]}}]},
        })
    return blocks


def create_lead(lead: dict, draft: str) -> None:
    db_id = os.environ["NOTION_DB_ID"]
    props = {
        "Thread":       {"title": [{"text": {"content": lead["title"][:200]}}]},
        "Community":    {"select": {"name": f"r/{lead['community']}"}},
        "ICP segment":  {"select": {"name": lead.get("segment", "Other / not ICP")}},
        "Intent score": {"number": int(lead.get("intent_score", 0))},
        "Signal type":  {"select": {"name": lead.get("signal_type", "unknown")[:100]}},
        "Promo policy": {"select": {"name": lead.get("promo_policy", "help_only")}},
        "Status":       {"select": {"name": "New"}},
        "Author":       {"rich_text": [{"text": {"content": lead.get("author", "")[:200]}}]},
        "Thread URL":   {"url": lead["url"]},
    }
    children = (
        [{"object": "block", "type": "heading_3",
          "heading_3": {"rich_text": [{"type": "text", "text": {"content": "Why it surfaced"}}]}}]
        + _paragraphs(lead.get("reasoning", ""))
        + [{"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "Draft reply (review before posting)"}}]}}]
        + _paragraphs(draft)
    )
    r = requests.post(
        f"{_BASE}/pages",
        headers=_headers(),
        json={"parent": {"database_id": db_id}, "properties": props, "children": children},
        timeout=30,
    )
    if r.status_code >= 300:
        print(f"  ! Notion create failed ({r.status_code}): {r.text[:300]}")
    r.raise_for_status()
