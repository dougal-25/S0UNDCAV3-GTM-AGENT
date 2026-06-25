"""
Package init. Loads the project-local .env BEFORE any submodule imports run,
so the Anthropic clients (built at import time in reason/classify.py and
reason/draft.py) find their credentials.

Local runs read projects/soundcave-gtm-agent/.env. On GitHub Actions there is
no .env file — load_dotenv() is a no-op and the workflow injects the secrets as
real environment variables instead. Safe in both contexts.
"""
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
