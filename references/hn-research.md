# Hacker News Research Guide

## Purpose

This guide explains how to interpret `scripts/fetch_hn.py` output and extract
actionable signals for indie game market research.

HN's audience is technical, so signals here differ from Reddit:
- **Upvotes/points** = technical merit + novelty + discussion value
- **Comments** = controversy or genuine curiosity (both are positive signals)
- **Show HN** posts = the developer shipped something real

## Key Fields to Read

```json
{
  "posts": [
    {
      "title": "Show HN: I made a ...",
      "points": 342,
      "num_comments": 87,
      "engagement_score": 516,    // points + num_comments * 2
      "hn_url": "https://news.ycombinator.com/item?id=...",
      "url": "https://...",       // the game's actual URL
      "author": "...",
      "created_at": "2025-..."
    }
  ]
}
```

## What HN Signals Mean for Game Research

### Show HN game launches

A "Show HN" post with high points means:
- A solo/small-team dev shipped a real game
- The HN community found it genuinely interesting
- The concept has technically-minded early adopters

Look for patterns: what types of games get the most engagement?

### High engagement = validated concept

| Engagement | Signal |
|------------|--------|
| > 300 | Major success — concept resonates broadly |
| 100–300 | Strong signal — niche with real enthusiasts |
| 30–100 | Solid — niche but proven |
| < 30 | Weak — interesting but limited audience |

### Comment patterns

- Many comments on a game post = people have **opinions** about this genre
- Comments asking "how did you build this?" = replicable approach
- Comments saying "I've always wanted a game like this" = market gap confirmation

## Typical High-Performing HN Game Categories

Based on historical HN patterns:

1. **Browser-based games** — zero install friction, immediate play
2. **Programming/puzzle games** — fits HN's technical audience
3. **Strategy/simulation with interesting systems** — engineers love complex systems
4. **Nostalgic remakes with modern twists** — emotional + technical angle
5. **Single-developer success stories** — "I made X in Y months, here's my revenue"

## Revenue/Business Discussions to Watch For

HN discussions often include developer revenue disclosures:
- "I made $X in the first month"
- "Steam launch results: N wishlists → N sales"
- "App Store revenue after 6 months"

These are gold — concrete proof that a niche can monetize. Look for:
- Games that earned more than expected ("surprised by the response")
- Games in unexpected niches that outperformed mainstream games
- Solo devs reporting sustainable income

## Technical Signals Relevant to Small Teams

Watch for mentions of:
- **Godot** — free, open-source, growing community
- **Unity** — established but licensing controversy created openings
- **Bevy / Rust games** — technical novelty, HN loves these
- **No-code/low-code tools** — signals non-programmer game dev opportunity
- **Web-based** (HTML5/JavaScript) — low barrier, easy distribution

## Search Query Coverage

The default queries target:
- `indie game`, `Show HN game`, `Show HN indie` — direct game posts
- `small team game`, `solo developer game` — solo/small team angle
- `roguelike`, `cozy game`, `idle game`, `puzzle game` — popular genres
- `mobile game`, `steam game`, `browser game` — platform-specific

To expand coverage, add genre-specific queries like `farming sim`, `city builder`,
or `visual novel`.

## Combining HN + Reddit Signals

The most actionable opportunities appear when:
1. Reddit has multiple pain-point posts about a type of game
2. HN has a successful "Show HN" in an adjacent category

This combination shows: **the need is real (Reddit) AND the technical path is proven (HN)**.
