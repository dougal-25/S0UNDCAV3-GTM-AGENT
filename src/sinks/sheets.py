"""
The "act" / output step: append qualified leads to a Google Sheet.

Google Sheets IS the state (see wiki decision 0002). The Actions runner is
ephemeral, so we keep no local state -- dedupe is by Thread URL against the sheet
itself.

Auth is a Google service account: put its full JSON key in the
GOOGLE_SERVICE_ACCOUNT_JSON env var (a GitHub Actions secret in CI), and share
the target sheet with that service account's email as an Editor. SHEET_ID is the
key from the sheet URL: docs.google.com/spreadsheets/d/<SHEET_ID>/edit.

The column order in HEADERS MUST match the sheet's header row exactly (see README).
"""
import json
import os
from datetime import date

import gspread
from google.oauth2.service_account import Credentials

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Column order -- must match the header row in the sheet exactly.
HEADERS = [
    "Thread", "Community", "ICP segment", "Intent score", "Signal type",
    "Promo policy", "Status", "Author", "Thread URL", "Why it surfaced",
    "Draft reply", "Date added",
]
_URL_COL = HEADERS.index("Thread URL") + 1  # gspread columns are 1-indexed

_ws = None


def _worksheet():
    """Lazily authorise and cache the first worksheet of the leads sheet."""
    global _ws
    if _ws is None:
        info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        creds = Credentials.from_service_account_info(info, scopes=_SCOPES)
        client = gspread.authorize(creds)
        _ws = client.open_by_key(os.environ["SHEET_ID"]).sheet1
    return _ws


def url_exists(url: str) -> bool:
    """True if a lead with this Thread URL is already in the sheet."""
    # col_values() re-reads from the API each call, so rows appended earlier in
    # this same run are seen -- dedupe stays correct within a run.
    return url in _worksheet().col_values(_URL_COL)


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
    _worksheet().append_row(row, value_input_option="USER_ENTERED")
