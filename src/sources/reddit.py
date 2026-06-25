"""
Reddit listening source.

Reads PUBLIC threads from configured subreddits using the official Reddit API
(PRAW) in read-only mode. This is within Reddit's API terms for low-volume
read use -- we never post here, we only gather candidate signals.
"""
import os
import praw

from ..config import POSTS_PER_COMMUNITY, SEARCH_LIMIT, SIGNAL_KEYWORDS


def _client() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ.get("REDDIT_USER_AGENT", "soundcave-gtm-agent/0.1"),
        read_only=True,
    )


def _matches_signal(title: str, body: str) -> bool:
    text = f"{title} {body}".lower()
    return any(kw in text for kw in SIGNAL_KEYWORDS)


def _to_candidate(submission, community: dict) -> dict:
    return {
        "id": submission.id,
        "title": submission.title or "",
        "body": (submission.selftext or "")[:4000],
        "url": f"https://www.reddit.com{submission.permalink}",
        "author": str(submission.author) if submission.author else "[deleted]",
        "community": community["name"],
        "platform": "reddit",
        "promo_policy": community["promo_policy"],
        "segment_hint": community["segment_hint"],
    }


def fetch_candidates(community: dict) -> list[dict]:
    """
    Return candidate threads from one subreddit: recent posts that match a
    signal keyword, plus direct keyword searches. Deduped by post id.
    """
    reddit = _client()
    sub = reddit.subreddit(community["name"])
    seen: dict[str, dict] = {}

    # 1) recent posts that happen to contain a signal keyword
    for submission in sub.new(limit=POSTS_PER_COMMUNITY):
        if _matches_signal(submission.title, submission.selftext or ""):
            seen[submission.id] = _to_candidate(submission, community)

    # 2) targeted keyword searches (catches older still-active threads)
    for kw in ("flyer", "cover art", "artwork", "designer"):
        try:
            for submission in sub.search(kw, sort="new", time_filter="month", limit=SEARCH_LIMIT):
                seen.setdefault(submission.id, _to_candidate(submission, community))
        except Exception as e:  # a single sub's search failing shouldn't kill the run
            print(f"  ! search '{kw}' failed in r/{community['name']}: {e}")

    return list(seen.values())
