"""
Local smoke test for the Google Sheets sink (src/sinks/sheets.py).

Appends one clearly-marked TEST row via the Apps Script webhook, then confirms
dedupe sees its URL. Delete the TEST row from the sheet afterwards.

Run from the repo root (needs SHEETS_WEBHOOK_URL in .env or the environment;
SHEETS_WEBHOOK_TOKEN too if you set a token on the script):

    python -m scripts.test_sheet
"""
from src.sinks import sheets  # importing src runs load_dotenv() in src/__init__.py

TEST_URL = "https://www.reddit.com/r/test/soundcave-smoke-test"

_lead = {
    "title": "TEST — SoundCave sink smoke test (safe to delete)",
    "community": "test",
    "segment": "DJ / electronic producer",
    "intent_score": 99,
    "signal_type": "needs_flyer",
    "promo_policy": "open",
    "author": "u/soundcave-test",
    "url": TEST_URL,
    "reasoning": "Smoke test — written by scripts/test_sheet.py.",
}

if __name__ == "__main__":
    print("-> appending a TEST row via the webhook ...")
    sheets.create_lead(_lead, "(draft reply placeholder)")
    print("   OK: create_lead returned with no error")

    print("-> checking dedupe sees the TEST url ...")
    print("   url_exists ->", sheets.url_exists(TEST_URL))

    print("\nDone. If both worked, delete the TEST row from the sheet.")
