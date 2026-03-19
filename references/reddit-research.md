# Reddit Research Guide

## Purpose

This guide explains how to interpret the output of `scripts/fetch_reddit.py` for
game idea research. The script returns JSON with pain-point posts, engagement scores,
and subreddit-specific data.

## Key Fields to Read

```json
{
  "top_pain_points": [...],      // posts flagged as player pain points — start here
  "posts_by_subreddit": {...},   // drill into specific genres
  "all_posts": [...]             // full cross-subreddit list by engagement
}
```

Each post entry contains:
- `title` — the post title (primary signal)
- `selftext` — first 500 chars of body text
- `score` — Reddit upvotes
- `num_comments` — comment count
- `engagement_score` — `score + num_comments * 3` (comments weighted 3x)
- `is_pain_point` — true if the post expresses an unmet player need
- `flair` — post category label

## High-Signal Subreddits by Research Goal

| Goal | Subreddits to focus on |
|------|------------------------|
| Unmet genre needs | `SuggestAGame`, `tipofmyjoystick` |
| Mobile market gaps | `iosgaming`, `AndroidGaming` |
| Indie dev sentiment | `indiegames`, `indiegaming`, `IndieDev`, `solodev` |
| Niche audiences | `cozygames`, `patientgamers`, `truegaming` |
| Steam market | `SteamDeals`, `SteamDeck`, `gamedev` |

## Pain Point Signal Patterns

### Direct "game doesn't exist" signals (highest confidence)
- "I wish there was a game that..."
- "Why is there no game like..."
- "Can't find a game that..."
These are the clearest market gaps. If multiple posts say the same thing, it's a validated opportunity.

### Request patterns (high confidence)
- Posts in `SuggestAGame` and `tipofmyjoystick` — every post is a game request by definition
- Upvoted suggestions with many comments = many people share the need

### Frustration signals (medium confidence)
- "Pay to win", "no ads game", "no gacha" — indicates premium/fair monetization opportunity
- "Frustrated with X mechanic" — indicates improvement opportunity

### Cozy / casual signals
- "cozy game that", "looking for cozy" — strong mobile opportunity
- "ios game that", "android game that" — platform-specific gaps

## Engagement Score Interpretation

| Score | Interpretation |
|-------|---------------|
| > 500 | Viral signal — broad audience cares deeply |
| 100–500 | Strong signal — real demand, good niche size |
| 50–100 | Moderate signal — niche but validated |
| < 50 | Weak signal — may be idiosyncratic |

## Genre Clustering

Group pain-point posts into genre clusters to spot patterns:
- **Cozy/Relaxing**: farming sims, life sims, puzzle games, ambient experiences
- **Strategy/Management**: city builders, factory games, resource management
- **Roguelikes/Roguelites**: procedural, high replayability
- **Narrative/Story**: visual novels, walking sims, mystery games
- **Idle/Incremental**: passive progression, minimal input required
- **Multiplayer/Social**: co-op, competitive, social deduction

## Common Monetization Frustrations

Phrases that signal revenue opportunity for fair-priced alternatives:
- "pay to win" / "pay-to-win"
- "too many ads"
- "gacha mechanics"
- "energy system"
- "can't progress without paying"
- "premium price but still has IAP"

These signal that players will pay a fair one-time price or support ethical IAP.

## Keyword Selection Tips

The `--keywords` flag does simple substring matching on title + body text. Short or
generic words cause false positives (e.g. `nature` matches "by its very nature",
`survival` matches "survival of the fittest" in non-game contexts).

Prefer **compound or specific terms** over bare single words:

| Instead of | Use |
|-----------|-----|
| `animal` | `animal game`, `wildlife sim` |
| `nature` | `nature game`, `outdoor adventure` |
| `survival` | `survival game`, `survival sim` |
| `cozy` | `cozy game` |

When the game concept is very specific (e.g. "animal parenting"), use genre terms
that players actually type, not descriptive adjectives.

## Notes on Data Limitations

- Reddit's public API returns ~25 top posts per subreddit (sorted by score)
- For years older than 2 years, coverage is incomplete (Reddit limits historical data)
- The `t=year` filter is approximate — filter client-side using `created_utc`
- Supplement with manual browsing for niche subreddits not in the default list
