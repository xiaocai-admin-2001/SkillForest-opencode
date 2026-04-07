---
name: opencode-skill-quality-reviewer
description: Reviews local skills against OpenCode authoring standards and updates quality score records. Use when auditing one skill or the full skill library so manager scores stay meaningful.
---

# OpenCode Skill Quality Reviewer

Audit local skills with repeatable, file-based scoring instead of guesswork.

## Core Rule

Quality scores must come from a documented review pass, not from usage count alone.

## When To Use

- after creating or rewriting a skill
- when manager scores look stale or misleading
- before sorting or cleaning the skill library by score
- when you want a batch quality pass over all local skills

## Workflow

1. Load `opencode-skill-best-practices` to review the target standard.
2. Run the scoring script against one skill or the full library.
3. Read the generated score breakdown and recommendations.
4. Fix the weakest areas.
5. Re-run the scorer to refresh `skill_quality_reviews.json`.

## Commands

Review all skills:

```bash
python scripts/review_skill_quality.py --all
```

Review one skill:

```bash
python scripts/review_skill_quality.py --skill cek-commit
```

Write to a custom file:

```bash
python scripts/review_skill_quality.py --all --output C:/temp/skill_scores.json
```

## Score Dimensions

- metadata quality
- structure clarity
- local OpenCode alignment
- registry alignment
- maintainability

## Output File

Default output:

`C:/Users/Administrator/.claude/skills/skill-registry/skill_quality_reviews.json`

The skill manager reads this file and combines quality score with usage-derived heat score.

## Notes

- This scorer is deterministic and heuristic, so it is good for library-wide baselines.
- For critical skills, use the generated recommendations as a first pass and then do a human rewrite review.
