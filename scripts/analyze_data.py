#!/usr/bin/env python3
"""
analyze_data.py - Synthesize Reddit and HN data into a structured research summary.

Usage:
    python scripts/analyze_data.py \
        --reddit /tmp/reddit_raw.json \
        --hn /tmp/hn_raw.json \
        --game-overview "A cozy farming simulation game for mobile" \
        --output /tmp/analysis_summary.md

Outputs a markdown summary ready to be read by Claude for game idea synthesis.
"""

import argparse
import json
import sys
from datetime import datetime, timezone


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found: {path}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse {path}: {e}", file=sys.stderr)
        return {}


def format_date(utc_timestamp: float) -> str:
    if not utc_timestamp:
        return "unknown"
    return datetime.fromtimestamp(utc_timestamp, tz=timezone.utc).strftime("%Y-%m-%d")


def render_reddit_section(reddit: dict, game_overview: str) -> str:
    lines = []
    year = reddit.get("target_year", "?")
    total = reddit.get("total_posts", 0)
    pain_count = reddit.get("pain_point_posts_count", 0)
    keyword_count = reddit.get("keyword_relevant_count", 0)
    keywords = reddit.get("keywords_used", [])

    lines.append(f"## Reddit Research Summary (Year: {year})")
    lines.append(f"- Total posts analyzed: {total}")
    lines.append(f"- Pain-point posts: {pain_count}")
    if keywords:
        lines.append(f"- Keyword-relevant posts: {keyword_count} (keywords: {', '.join(keywords)})")
    lines.append("")

    # Top pain points
    pain_posts = reddit.get("top_pain_points", [])[:15]
    if pain_posts:
        lines.append("### Top Pain Points (by engagement)")
        lines.append("")
        for i, post in enumerate(pain_posts, 1):
            lines.append(f"{i}. **[{post['subreddit']}]** {post['title']}")
            lines.append(f"   - Score: {post['score']} | Comments: {post['num_comments']} | Engagement: {post['engagement_score']}")
            lines.append(f"   - URL: {post['url']}")
            if post.get("selftext", "").strip():
                snippet = post["selftext"][:200].replace("\n", " ")
                lines.append(f"   - Body: {snippet}...")
            lines.append("")

    # Keyword-relevant posts
    kw_posts = reddit.get("keyword_relevant_posts", [])[:10]
    if kw_posts and keywords:
        lines.append("### Game-Concept Relevant Posts")
        lines.append("")
        for i, post in enumerate(kw_posts, 1):
            lines.append(f"{i}. **[{post['subreddit']}]** {post['title']}")
            lines.append(f"   - Engagement: {post['engagement_score']} | Pain point: {post['is_pain_point']}")
            lines.append(f"   - URL: {post['url']}")
            lines.append("")

    # Monetization frustrations (filter from all posts)
    all_posts = reddit.get("all_posts", [])
    monetization_signals = [
        p for p in all_posts
        if any(kw in p["title"].lower() for kw in [
            "pay to win", "pay-to-win", "gacha", "too many ads", "energy system",
            "premium game", "no ads", "paywall", "free to play"
        ])
    ][:8]

    if monetization_signals:
        lines.append("### Monetization Frustration Signals")
        lines.append("")
        for post in monetization_signals:
            lines.append(f"- [{post['subreddit']}] {post['title']} (score: {post['score']})")
            lines.append(f"  {post['url']}")
        lines.append("")

    return "\n".join(lines)


def render_hn_section(hn: dict) -> str:
    lines = []
    year = hn.get("target_year", "?")
    total = hn.get("total_posts", 0)
    show_hn_count = hn.get("show_hn_count", 0)
    business_count = hn.get("business_relevant_count", 0)

    lines.append(f"## Hacker News Research Summary (Year: {year})")
    lines.append(f"- Total posts analyzed: {total}")
    lines.append(f"- Show HN game launches: {show_hn_count}")
    lines.append(f"- Business/revenue relevant: {business_count}")
    lines.append("")

    # Top Show HN launches
    show_posts = hn.get("show_hn_posts", [])[:10]
    if show_posts:
        lines.append("### Top Show HN Game Launches (by engagement)")
        lines.append("")
        for i, post in enumerate(show_posts, 1):
            lines.append(f"{i}. **{post['title']}**")
            lines.append(f"   - Points: {post['points']} | Comments: {post['num_comments']} | Engagement: {post['engagement_score']}")
            lines.append(f"   - HN: {post['hn_url']}")
            if post.get("url"):
                lines.append(f"   - Game: {post['url']}")
            lines.append("")

    # Business / revenue discussions
    biz_posts = hn.get("business_relevant_posts", [])[:8]
    if biz_posts:
        lines.append("### Revenue & Business Discussions")
        lines.append("")
        for i, post in enumerate(biz_posts, 1):
            lines.append(f"{i}. **{post['title']}**")
            lines.append(f"   - Engagement: {post['engagement_score']} | {post['hn_url']}")
            lines.append("")

    return "\n".join(lines)


def render_header(game_overview: str, year: int) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""# Game Research Data Summary

**Generated:** {now}
**Target Year:** {year}

## Game Overview (User Input)

{game_overview}

---
"""


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize Reddit and HN data into a research summary for game idea analysis"
    )
    parser.add_argument("--reddit", type=str, default="/tmp/reddit_raw.json",
                        help="Path to Reddit JSON output")
    parser.add_argument("--hn", type=str, default="/tmp/hn_raw.json",
                        help="Path to HN JSON output")
    parser.add_argument("--game-overview", type=str, default="",
                        help="User's game concept description")
    parser.add_argument("--output", type=str, default="/tmp/analysis_summary.md",
                        help="Output markdown file path")
    args = parser.parse_args()

    reddit = load_json(args.reddit)
    hn = load_json(args.hn)

    year = reddit.get("target_year") or hn.get("target_year") or datetime.now().year

    sections = [
        render_header(args.game_overview or "(not provided)", year),
        render_reddit_section(reddit, args.game_overview),
        "---\n",
        render_hn_section(hn),
        "---\n",
        "## Next Steps\n\nRead this summary, then consult references/indiehackers-research.md for WebSearch queries to run on Indie Hackers.\nThen synthesize all findings into game idea proposals per the SKILL.md template.\n",
    ]

    output_content = "\n".join(sections)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_content)

    print(f"Analysis summary saved to: {args.output}")
    print(f"Reddit posts: {reddit.get('total_posts', 0)} | Pain points: {reddit.get('pain_point_posts_count', 0)}")
    print(f"HN posts: {hn.get('total_posts', 0)} | Show HN: {hn.get('show_hn_count', 0)}")


if __name__ == "__main__":
    main()
