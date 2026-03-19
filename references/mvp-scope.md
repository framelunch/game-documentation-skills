# MVP Scope Guide

Use this reference during Step 5 (synthesis) to propose a realistic MVP for each game idea.

## What an MVP is (and isn't)

An MVP is the smallest version of the game that:
1. Lets a real player complete one satisfying session
2. Validates the core loop — the one mechanic that makes the game feel unique
3. Can be shared publicly to get honest feedback

An MVP is **not** a demo, a prototype, or a full game. It should feel complete for what it promises, even if it's short.

## How to define the MVP scope

### Step 1: Identify the single core loop

Strip the concept down to one sentence:
> "Player does X to get Y, then returns to Z."

Everything that isn't X, Y, or Z is post-MVP. Write down what that means for this specific concept.

### Step 2: Apply the cut list

For each feature category, judge whether it belongs in MVP or post-launch:

| Feature category | MVP? | Rule of thumb |
|-----------------|------|---------------|
| Core mechanic (the thing that's fun) | Always | No MVP without it |
| One playable level / map | Always | Players need something to do |
| Win / fail condition | Always | Session needs a resolution |
| Sound effects (basic) | Yes | Silence kills immersion |
| Art (placeholder OK) | Yes | Needs to be readable, not beautiful |
| Multiple levels / maps | No | One good level beats five mediocre |
| Character customization | No | Add after retention is proven |
| Story / cutscenes | No, usually | Unless story IS the core loop |
| Multiple playable characters | No | One character, done right |
| Achievement system | No | Post-launch engagement mechanic |
| Cloud save / leaderboard | No | Technical debt, add later |
| Settings menu (full) | No | Mute button is enough |
| Tutorial | Maybe | Replace with good onboarding design |

### Step 3: Estimate the timeline honestly

Use this formula:
> Realistic estimate = (your gut estimate) × 1.5

Then check against the platform's minimum bar:

| Platform | Minimum bar to ship |
|----------|---------------------|
| Mobile (iOS/Android) | App Store review takes 1–3 days. Game must not crash. |
| Steam | $100 submission fee. Needs a store page with screenshots + trailer. |
| Both | Two submission pipelines, two compliance reviews — add 1–2 weeks. |

Timeline anchors by scope:

| MVP size | Typical timeline (solo dev) |
|----------|-----------------------------|
| Micro (1 mechanic, 1 level) | 2–4 weeks |
| Small (1 mechanic, 3–5 levels, basic progression) | 1–2 months |
| Medium (core loop complete, light meta) | 2–4 months |
| Large (full genre expectations met) | 4–8 months |

If the estimate exceeds 3 months, look for cuts. A shipped micro-MVP beats an abandoned medium one.

### Step 4: Define the "done" condition

A good MVP scope statement reads like this:
> "MVP is done when a player can [do the core action] for [N minutes / sessions], reach [a clear end state], and feel [the intended emotion]."

Example:
> "MVP is done when a player can explore a field as a fox, collect 5 food items, and return to the den before the hawk catches them — in a single 5-minute session — and feel the tension and relief of a narrow escape."

## What to include in the report

For each proposed game idea, include:

```markdown
**MVP Scope:**
- Core loop implemented: [one sentence]
- Content included: [N levels / maps / encounters]
- Features excluded from MVP: [bullet list]
- "Done" condition: [one sentence per the formula above]

**MVP Development Timeline:**
- Estimate: [N weeks / months]
- Breakdown:
  - Core mechanic: N weeks
  - Art (placeholder / final): N weeks
  - Audio: N days
  - Platform submission + QA: N weeks
- First milestone (playable internally): [N weeks from start]
```

## Red flags in MVP planning

- **"Just one more feature"** — every added feature multiplies integration risk
- **Art-first development** — beautiful assets before working mechanics is a trap
- **Targeting both platforms simultaneously** — ship one first, port second
- **No defined end state** — if "done" is fuzzy, the MVP never ships

## Signal: is the MVP the right size?

Ask: "If I showed this to 10 strangers, would they understand what the game is about?"

- Yes, and they'd want to keep playing → right size
- Yes, but it feels thin → add one more content beat, not features
- No, it's confusing → cut further or fix the onboarding
- No, it feels incomplete by genre standards → you may have under-scoped
