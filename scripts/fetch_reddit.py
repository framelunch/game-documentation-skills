#!/usr/bin/env python3
"""
fetch_reddit.py - Fetch posts from game-related subreddits using Reddit's public JSON API.

Usage:
    python scripts/fetch_reddit.py --year 2025 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2025 --limit 50 --keywords "cozy,farming,mobile"

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


GAME_SUBREDDITS = [
    # Pain point / request subreddits (highest signal)
    "SuggestAGame",
    "tipofmyjoystick",
    # Indie game communities
    "indiegaming",
    "indiegames",
    "IndieDev",
    "solodev",
    # Platform-specific
    "iosgaming",
    "AndroidGaming",
    "SteamDeck",
    "SteamDeals",
    # Genre communities
    "cozygames",
    "patientgamers",
    # Development communities
    "gamedev",
    "gamedesign",
    # Broad gaming
    "truegaming",
    "gaming",
]

# Multi-word phrases signaling unmet player needs (single words avoided to prevent false positives)
PAIN_SIGNAL_KEYWORDS = [
    # Existence gaps
    "i wish there was a game", "wish there was a game",
    "why isn't there a game", "why is there no game",
    "nobody has made a game", "no one has made a game",
    "i can't find a game", "can't find a game",
    "doesn't exist", "does not exist",
    "no game that", "no game like",
    # Desires
    "would love a game", "dream game",
    "looking for a game", "suggest a game",
    "game request", "game recommendation",
    # Frustration
    "frustrated with", "i'm frustrated", "so frustrated",
    "underserved", "missing feature", "market gap",
    # Genre-specific requests
    "cozy game that", "mobile game that",
    "ios game that", "android game that",
    "i need a game", "i want a game",
    "i need a cozy", "i want a cozy",
    "looking for cozy", "looking for a cozy",
    # Monetization frustration (signals premium opportunity)
    "premium game", "no gacha", "no ads game",
    "pay to win", "pay-to-win", "too many ads",
    "energy system", "no energy", "paywall",
]

# Subreddits where every post is a game request by definition
PAIN_POINT_SUBREDDITS = {"SuggestAGame", "tipofmyjoystick"}

HEADERS = {
    "User-Agent": "GameIdeaResearch/1.0 (educational research tool)",
}


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API.

    For current/recent years uses t=year (past 12 months).
    For older years uses t=all + client-side year filtering (Reddit returns ~1000 posts max).
    """
    current_year = datetime.now(timezone.utc).year
    time_filter = "year" if target_year is None or target_year >= current_year - 1 else "all"
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            posts = data.get("data", {}).get("children", [])
            return [p["data"] for p in posts]
    except Exception as e:
        print(f"  Warning: Failed to fetch r/{subreddit}: {e}")
        return []


def is_pain_point(post: dict) -> bool:
    """Detect posts expressing unmet player needs."""
    if post.get("subreddit") in PAIN_POINT_SUBREDDITS:
        return True
    title = post.get("title", "").lower()
    flair = (post.get("link_flair_text") or "").lower()
    body = post.get("selftext", "").lower()[:300]
    return any(kw in title or kw in flair or kw in body for kw in PAIN_SIGNAL_KEYWORDS)


def is_keyword_relevant(post: dict, keywords: list[str]) -> bool:
    """Check if post is relevant to any of the provided keywords."""
    if not keywords:
        return True
    text = (post.get("title", "") + " " + post.get("selftext", "")).lower()
    return any(kw.lower() in text for kw in keywords)


def date_range_for_year(year: int) -> tuple[float, float]:
    """Return (start_unix, end_unix) for the target year.
    Uses rolling 12-month window for current/future years."""
    now = datetime.now(timezone.utc)
    if year >= now.year:
        try:
            one_year_ago = now.replace(year=now.year - 1)
        except ValueError:
            one_year_ago = now.replace(year=now.year - 1, day=28)
        return one_year_ago.timestamp(), now.timestamp()
    else:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return start.timestamp(), end.timestamp()


def filter_by_year(post: dict, year: int) -> bool:
    created = post.get("created_utc", 0)
    start, end = date_range_for_year(year)
    return start <= created <= end


def engagement_score(post: dict) -> int:
    """Score = upvotes + comments * 3 (comments signal active discussion)."""
    return post.get("score", 0) + post.get("num_comments", 0) * 3


def normalize_post(raw: dict, subreddit: str, keywords: list[str]) -> dict:
    return {
        "subreddit": subreddit,
        "title": raw.get("title", ""),
        "selftext": raw.get("selftext", "")[:600],
        "score": raw.get("score", 0),
        "num_comments": raw.get("num_comments", 0),
        "flair": raw.get("link_flair_text", ""),
        "url": f"https://reddit.com{raw.get('permalink', '')}",
        "created_utc": raw.get("created_utc", 0),
        "engagement_score": engagement_score(raw),
        "is_pain_point": is_pain_point(raw),
        "keyword_relevant": is_keyword_relevant(raw, keywords),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch game subreddit posts for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in list)")
    parser.add_argument("--keywords", type=str, default=None,
                        help="Comma-separated keywords to flag relevant posts (e.g. 'cozy,farming,mobile')")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else GAME_SUBREDDITS
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
    target_year = args.year

    print(f"Fetching posts from {len(subreddits)} subreddits for year {target_year}...")
    if keywords:
        print(f"Keyword filter active: {keywords}")

    all_posts: list[dict] = []
    pain_posts: list[dict] = []
    keyword_posts: list[dict] = []
    posts_by_subreddit: dict[str, list[dict]] = {}

    for sub in subreddits:
        print(f"  Fetching r/{sub}...")
        raw_posts = fetch_subreddit_posts(sub, limit=args.limit, sort="top", target_year=target_year)

        sub_entries = []
        for raw in raw_posts:
            if not filter_by_year(raw, target_year):
                continue

            entry = normalize_post(raw, sub, keywords)
            all_posts.append(entry)
            sub_entries.append(entry)

            if entry["is_pain_point"]:
                pain_posts.append(entry)
            if entry["keyword_relevant"] and keywords:
                keyword_posts.append(entry)

        if sub_entries:
            sub_entries.sort(key=lambda x: x["engagement_score"], reverse=True)
            posts_by_subreddit[sub] = sub_entries

        time.sleep(1)  # polite rate limiting

    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    keyword_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "keywords_used": keywords,
        "total_posts": len(all_posts),
        "pain_point_posts_count": len(pain_posts),
        "keyword_relevant_count": len(keyword_posts),
        "subreddits_searched": subreddits,
        # Pain point posts sorted by engagement — read this first
        "top_pain_points": pain_posts[:60],
        # Keyword-relevant posts — game-concept specific
        "keyword_relevant_posts": keyword_posts[:40],
        # Top posts across all subreddits
        "all_posts": all_posts[:100],
        # By subreddit — use for genre-specific analysis
        "posts_by_subreddit": posts_by_subreddit,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts total.")
    print(f"  Pain-point posts: {len(pain_posts)}")
    print(f"  Keyword-relevant: {len(keyword_posts)}")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
