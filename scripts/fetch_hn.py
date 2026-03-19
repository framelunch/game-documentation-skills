#!/usr/bin/env python3
"""
fetch_hn.py - Fetch game-related posts from Hacker News via Algolia Search API.

Usage:
    python scripts/fetch_hn.py --year 2025 --output /tmp/hn_raw.json
    python scripts/fetch_hn.py --year 2025 --min-points 5 --keywords "puzzle,mobile"

HN Algolia API is public and requires no authentication.
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


# Search queries targeting indie games on HN
GAME_QUERIES = [
    "indie game",
    "Show HN game",
    "Show HN indie",
    "Show HN mobile game",
    "small team game",
    "solo developer game",
    "game released",
    "game launched",
    "mobile game revenue",
    "steam game launch",
    "puzzle game",
    "roguelike",
    "cozy game",
    "idle game",
    "browser game",
    "godot game",
    "unity indie",
]

ALGOLIA_BASE = "https://hn.algolia.com/api/v1/search"

# Title must contain at least one to confirm game relevance
GAME_RELATED_KEYWORDS = [
    "game", "gaming", "indie", "steam", "mobile game", "puzzle", "roguelike",
    "rpg", "cozy", "idle", "browser game", "gamedev", "game dev", "unity",
    "godot", "unreal", "playthrough", "player", "gameplay",
]

# Signals that this post discusses revenue / business outcomes
BUSINESS_KEYWORDS = [
    "revenue", "earning", "made $", "$k", "mrr", "launch", "steam sales",
    "app store", "monetiz", "profit", "income", "download", "wishlist",
]


def is_game_related(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in GAME_RELATED_KEYWORDS)


def is_business_relevant(title: str, story_text: str = "") -> bool:
    """True if the post discusses game revenue or business outcomes."""
    text = (title + " " + story_text).lower()
    return any(kw in text for kw in BUSINESS_KEYWORDS)


def is_keyword_relevant(title: str, story_text: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    text = (title + " " + story_text).lower()
    return any(kw.lower() in text for kw in keywords)


def date_range_for_year(year: int) -> tuple[int, int]:
    """Return (start_unix, end_unix) for the target year.
    Uses rolling 12-month window for current/future years."""
    now = datetime.now(timezone.utc)
    if year >= now.year:
        try:
            one_year_ago = now.replace(year=now.year - 1)
        except ValueError:
            one_year_ago = now.replace(year=now.year - 1, day=28)
        return int(one_year_ago.timestamp()), int(now.timestamp())
    else:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return int(start.timestamp()), int(end.timestamp())


def fetch_hn_posts(query: str, year: int, min_points: int = 5) -> list[dict]:
    """Fetch HN stories matching a query within the given year."""
    year_start, year_end = date_range_for_year(year)

    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{year_start},created_at_i<{year_end},points>={min_points}",
        "hitsPerPage": 20,
    })
    url = f"{ALGOLIA_BASE}?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GameIdeaResearch/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("hits", [])
    except Exception as e:
        print(f"  Warning: HN query '{query}' failed: {e}")
        return []


def normalize_post(hit: dict, matched_query: str, keywords: list[str]) -> dict:
    title = hit.get("title", "")
    story_text = hit.get("story_text", "") or ""
    points = hit.get("points", 0)
    num_comments = hit.get("num_comments", 0)
    return {
        "object_id": hit.get("objectID", ""),
        "title": title,
        "url": hit.get("url", ""),
        "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
        "points": points,
        "num_comments": num_comments,
        "author": hit.get("author", ""),
        "created_at": hit.get("created_at", ""),
        "matched_query": matched_query,
        # points + comments * 2 (comments signal active discussion)
        "engagement_score": points + num_comments * 2,
        "is_business_relevant": is_business_relevant(title, story_text),
        "is_show_hn": title.lower().startswith("show hn"),
        "keyword_relevant": is_keyword_relevant(title, story_text, keywords),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch game-related HN posts for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year (default: current year)")
    parser.add_argument("--min-points", type=int, default=5,
                        help="Minimum HN points threshold (default: 5)")
    parser.add_argument("--output", type=str, default="/tmp/hn_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--queries", type=str, default=None,
                        help="Comma-separated query list (default: built-in list)")
    parser.add_argument("--keywords", type=str, default=None,
                        help="Comma-separated keywords to flag concept-relevant posts")
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else GAME_QUERIES
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
    target_year = args.year

    print(f"Fetching HN posts for year {target_year} using {len(queries)} queries...")
    if keywords:
        print(f"Keyword filter active: {keywords}")

    seen_ids: set[str] = set()
    all_posts: list[dict] = []
    show_hn_posts: list[dict] = []
    business_posts: list[dict] = []
    keyword_posts: list[dict] = []

    for query in queries:
        print(f"  Searching: '{query}'...")
        hits = fetch_hn_posts(query, target_year, min_points=args.min_points)

        for hit in hits:
            post = normalize_post(hit, query, keywords)
            if not is_game_related(post["title"]):
                continue
            if post["object_id"] in seen_ids:
                continue

            seen_ids.add(post["object_id"])
            all_posts.append(post)

            if post["is_show_hn"]:
                show_hn_posts.append(post)
            if post["is_business_relevant"]:
                business_posts.append(post)
            if post["keyword_relevant"] and keywords:
                keyword_posts.append(post)

        time.sleep(0.5)

    # Sort all lists by engagement
    for lst in [all_posts, show_hn_posts, business_posts, keyword_posts]:
        lst.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "keywords_used": keywords,
        "total_posts": len(all_posts),
        "show_hn_count": len(show_hn_posts),
        "business_relevant_count": len(business_posts),
        "keyword_relevant_count": len(keyword_posts),
        "queries_used": queries,
        # Show HN game launches — highest signal for "what shipped and resonated"
        "show_hn_posts": show_hn_posts[:40],
        # Posts discussing revenue, launch numbers, monetization
        "business_relevant_posts": business_posts[:30],
        # Concept-keyword relevant posts
        "keyword_relevant_posts": keyword_posts[:30],
        # All posts by engagement
        "all_posts": all_posts[:100],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_posts)} unique HN posts.")
    print(f"  Show HN launches: {len(show_hn_posts)}")
    print(f"  Business-relevant: {len(business_posts)}")
    print(f"  Keyword-relevant: {len(keyword_posts)}")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
