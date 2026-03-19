---
name: game-idea-researcher
description: >
  Research niche game ideas based on trends, user pain points, and community signals
  from Reddit, Hacker News, and Indie Hackers. Produces a structured report with
  game idea proposals, monetization strategies, marketing strategies, and a 5-axis
  evaluation scorecard (feasibility, development timeline, profitability, competitive
  advantage, small-team suitability). Use this skill whenever the user wants to:
  discover underserved game niches, validate a game concept against real player demand,
  research what features players are asking for, identify market gaps for indie games
  on mobile or Steam, or analyze community feedback to generate game business ideas.
  Trigger for: "game idea", "indie game research", "game market gap", "what games
  should I make", "game concept validation", "穴場ゲーム", "ゲームアイデア調査".
---

# Game Idea Researcher

## Step 0: Gather context (ask in Japanese)

Before doing any research, ask the user these questions **in Japanese**:

```
以下を教えてください：

1. **調査対象の年号**：どの年のデータを調査しますか？（例：2024、2025）
2. **ゲームの概要**：どんなゲームを作りたいですか？（ジャンル、テーマ、ターゲット層、参考にしたいゲームなど、思いつく限り教えてください）
3. **元のプロンプト**：このリサーチを依頼した背景や目的があれば教えてください（レポートに含めます）
```

Store the answers as:
- `{year}` — the 4-digit target year
- `{game_overview}` — the user's game description
- `{user_prompt}` — the original prompt/background (use the conversation history if the user says "上記の通り" or similar)

## Step 1: Reddit research

Extract 2–5 keywords from `{game_overview}` (genre terms, platform, theme). Then run:

```bash
python scripts/fetch_reddit.py \
  --year {year} \
  --limit 25 \
  --keywords "{keyword1},{keyword2},..." \
  --output /tmp/reddit_raw_{year}.json
```

→ Interpretation guide: `references/reddit-research.md`

## Step 2: Hacker News research

Use the same keywords as Step 1:

```bash
python scripts/fetch_hn.py \
  --year {year} \
  --min-points 5 \
  --keywords "{keyword1},{keyword2},..." \
  --output /tmp/hn_raw_{year}.json
```

→ Interpretation guide: `references/hn-research.md`

## Step 3: Merge data

```bash
python scripts/analyze_data.py \
  --reddit /tmp/reddit_raw_{year}.json \
  --hn /tmp/hn_raw_{year}.json \
  --game-overview "{game_overview}" \
  --output /tmp/analysis_summary_{year}.md
```

Read `/tmp/analysis_summary_{year}.md` before proceeding.

## Step 4: Indie Hackers research (WebSearch)

Run 3–4 WebSearch queries from `references/indiehackers-research.md`.

## Step 5: Synthesize into game ideas

Read `references/synthesis-criteria.md` to decide which gaps are worth proposing and how to rank them.
Read `references/monetization-strategies.md` for monetization options per idea.
Read `references/marketing-strategies.md` for marketing channel selection.
Read `references/evaluation-rubric.md` for the 5-axis scoring criteria.

Produce 3–5 game idea proposals aligned with `{game_overview}`.

## Step 6: Generate the report

Save to:
```
reports/{year}/{YYYYMMDD}/{HHMMSS}.md
```

Use this structure:

```markdown
# Game Idea Research Report — {year}

**Generated:** {YYYY-MM-DD HH:MM:SS}
**Target Year:** {year}

---

## Original Prompt

{user_prompt}

---

## Game Overview

{game_overview}

---

## Research Summary

### Reddit Signals
- Total posts analyzed: N
- Pain-point posts: N
- Key subreddits: ...

### Hacker News Signals
- Total posts analyzed: N
- Notable launches: ...

### Indie Hackers Insights
- Key revenue benchmarks: ...
- Successful monetization patterns: ...

---

## Top Player Pain Points

1. **[Pain Point Title]** — [subreddit, engagement score]
   > "[quote from post title]"
   Opportunity: ...

2. ...

---

## Game Idea Proposals

### Idea 1: [Game Title / Concept Name]

**Concept:** [2–3 sentence description]
**Target Platform:** App / Steam / Both
**Core Loop:** [what the player does every session]
**Unique Angle:** [what makes this niche / underserved]
**Evidence:** [sources and signal strength — see references/synthesis-criteria.md]

**Monetization:**
- Primary: ...
- Secondary: ...

**Marketing:**
- Key channels: ...
- Community hook: ...

**Scorecard:**
| Axis | Score | Notes |
|------|-------|-------|
| Feasibility | ⭐⭐⭐⭐☆ (4/5) | ... |
| Development Timeline | ⭐⭐⭐☆☆ (3/5) | ... |
| Profitability | ⭐⭐⭐⭐☆ (4/5) | ... |
| Competitive Advantage | ⭐⭐⭐☆☆ (3/5) | ... |
| Small-Team Suitability | ⭐⭐⭐⭐⭐ (5/5) | ... |

---

### Idea 2: ...

[repeat for each idea]

---

## Monetization Strategy Overview

Recommended for this concept: ...

---

## Marketing Strategy Overview

Recommended channels: ...

---

## Competitive Landscape

[Brief overview of existing games and gaps]

---

## Recommended Next Steps

1. ...
2. ...
3. ...
```
