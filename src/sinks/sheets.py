"""
The "act" / output step: append qualified leads to a Google Sheet via an
Apps Script web-app webhook.

Why a webhook and not the Sheets API: the target Google account's org policy
blocks service-account keys (iam.disableServiceAccountKeyCreation), so instead of
authenticating from outside we drive the sheet from a container-bound Apps Script
deployed as a web app. It runs as the sheet's owner -- no Google Cloud, no keys,
nothing for the org policy to block. See wiki decision 0002 and the script to
deploy in scripts/apps_script/Code.gs.

Env:
  SHEETS_WEBHOOK_URL    the Apps Script web-app /exec URL
  SHEETS_WEBHOOK_TOKEN  optional shared secret (must match the script's TOKEN property)

The column order in HEADERS MUST match the sheet's header row AND the order the
Apps Script's appendRow expects.
"""
import os
from datetime import date

import requests

# Column order -- must match the header row in the sheet exactly.
HEADERS = [
    "Thread", "Community", "ICP segment", "Intent score", "Signal type",
    "Promo policy", "Status", "Author", "Thread URL", "Why it surfaced",
    "Draft reply", "Date added",
]
_TIMEOUT = 30


def _post(payload: dict) -> dict:
    """POST a JSON action to the Apps Script web app and return its JSON reply."""
    body = {**payload, "token": os.environ.get("SHEETS_WEBHOOK_TOKEN", "")}
    r = requests.post(os.environ["SHEETS_WEBHOOK_URL"], json=body, timeout=_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(f"sheets webhook error: {data['error']}")
    return data


def url_exists(url: str) -> bool:
    """True if a lead with this Thread URL is already in the sheet."""
    return bool(_post({"action": "exists", "url": url}).get("exists"))


def create_lead(lead: dict, draft: str) -> None:
    row = [
        lead["title"][:500],
        f"r/{lead['community']}",
        lead.get("segment", "Other / not ICP"),
        int(lead.get("intent_score", 0)),
        lead.get("signal_type", "unknown"),
        lead.get("promo_policy", "help_only"),
        "New",
        lead.get("author", ""),
        lead["url"],
        lead.get("reasoning", ""),
        draft,
        date.today().isoformat(),
    ]
    _post({"action": "create", "row": row})
