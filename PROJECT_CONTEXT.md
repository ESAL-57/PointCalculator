# PROJECT_CONTEXT.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Project Setup

This project has a React frontend and Django backend.

Core directories:
- `frontend/`: Vite + React app intended for GitHub Pages hosting.
- `backend/`: Django API server that protects private API keys.
- `.github/workflows/`: GitHub Pages deployment workflow for the frontend.

Frontend rules:
- Prefer React components and plain CSS.
- Read public values from `VITE_*` environment variables.
- Call the Django backend through `src/api/client.js`.
- Do not put API keys, tokens, or secrets in frontend code.

Backend rules:
- Store secrets in environment variables only.
- Put browser-facing API routes under `/api/`.
- Keep external API calls inside Django views/services so keys stay private.
- Add apps only when a real feature needs them.

Hosting/API rules:
- GitHub Pages hosts only the built frontend.
- Django must be hosted separately when backend API calls are needed.
- Keep the project minimal until a real feature requires more structure.

## Point Calculator Rules

- A team has 5 players: top, jungle, mid, adc, support.
- Team total must be 165 points or less.
- Base points come from `tier_data.xlsx` by participant tier and position.
- The all-time achieved tier is used only for lower-bound tier rules.
- The 2025~2026 peak tier and season 14 peak tier are used for drop penalty rules.
- If a lower-bound tier applies, base points use the stronger of participant tier and lower-bound tier.
- Calculation logic currently lives in `backend/api/calculator.py`.
- Riot API lookup lives in `backend/api/riot.py` and uses `RIOT_API_KEY`.
- Peak-tier extraction lives in `backend/api/scraper.py`.
- The frontend calls `/api/crawl/player/` before calculation so users only enter Riot ID and tag.
