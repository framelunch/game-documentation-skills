# game-idea-researcher

A Claude Code skill that researches niche indie game ideas based on real player demand,
community trends, and proven indie business models.

## What it does

When invoked, the skill:

1. Asks you (in Japanese) for a target year and your game concept
2. Fetches pain-point posts from Reddit game communities
3. Fetches high-engagement game launches from Hacker News
4. Searches Indie Hackers for revenue benchmarks and monetization strategies
5. Synthesizes findings into 3–5 niche game idea proposals
6. Saves a structured report to `reports/{year}/{YYYYMMDD}/{HHMMSS}.md`

Each proposal includes a monetization plan, marketing approach, and a 5-axis scorecard:
Feasibility / Development Timeline / Profitability / Competitive Advantage / Small-Team Suitability.

## Directory structure

```
.
├── SKILL.md                          # Skill definition: workflow steps only
├── scripts/
│   ├── fetch_reddit.py               # Fetches posts from 16 game subreddits
│   ├── fetch_hn.py                   # Fetches game posts via HN Algolia API
│   ├── fetch_indiehackers.py         # Placeholder (IH research uses WebSearch)
│   └── analyze_data.py               # Merges Reddit + HN output into a summary
├── references/
│   ├── reddit-research.md            # How to interpret Reddit data
│   ├── hn-research.md                # How to interpret HN data
│   ├── indiehackers-research.md      # WebSearch queries for Indie Hackers
│   ├── synthesis-criteria.md         # What makes a gap worth proposing
│   ├── monetization-strategies.md    # Monetization options by platform/audience
│   ├── marketing-strategies.md       # Marketing channels by phase
│   └── evaluation-rubric.md          # 5-axis scoring criteria (1–5 per axis)
└── reports/                          # Generated reports (git-ignored)
    └── {year}/{YYYYMMDD}/{HHMMSS}.md
```

## Scripts

All scripts use only Python standard library — no dependencies to install.

| Script | Purpose | Key options |
|--------|---------|-------------|
| `fetch_reddit.py` | Fetch top posts from 16 game subreddits | `--year`, `--keywords`, `--limit` |
| `fetch_hn.py` | Fetch game posts from HN via Algolia API | `--year`, `--keywords`, `--min-points` |
| `analyze_data.py` | Merge Reddit + HN JSON into a markdown summary | `--reddit`, `--hn`, `--game-overview` |

### Quick test

```bash
python scripts/fetch_hn.py --year 2025 --output /tmp/hn.json
python scripts/fetch_reddit.py --year 2025 --output /tmp/reddit.json
python scripts/analyze_data.py --reddit /tmp/reddit.json --hn /tmp/hn.json --output /tmp/summary.md
```

## Data sources

| Source | Access method | What it provides |
|--------|--------------|-----------------|
| Reddit | Public JSON API (no auth) | Player pain points, feature requests, monetization frustrations |
| Hacker News | Algolia Search API (no auth) | Indie game launches, revenue discussions, technical approaches |
| Indie Hackers | WebSearch (`site:indiehackers.com`) | Revenue benchmarks, monetization strategies, solo dev success stories |

## Output report structure

```
reports/{year}/{YYYYMMDD}/{HHMMSS}.md
├── Original Prompt
├── Game Overview
├── Research Summary (Reddit / HN / Indie Hackers)
├── Top Player Pain Points
├── Game Idea Proposals (3–5 ideas)
│   ├── Concept + Core Loop + Unique Angle
│   ├── Evidence (with signal strength label)
│   ├── Monetization plan
│   ├── Marketing plan
│   └── 5-axis Scorecard
├── Monetization Strategy Overview
├── Marketing Strategy Overview
├── Competitive Landscape
└── Recommended Next Steps
```
