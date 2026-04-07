---
name: git:commit
description: Creates atomic git commits with conventional messages and emoji in local OpenCode repositories. Use when local changes are ready to commit and need clean structure, verification, split decisions, and concise reporting.
argument-hint: Optional flags like --no-verify to skip pre-commit checks
model: haiku
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git diff:*), Bash(git commit:*), Bash(git config:*), Bash(git branch:*), Bash(git checkout:*), Bash(pnpm lint:*), Bash(npm run lint:*), Bash(yarn lint:*), Bash(bun lint:*)
---

# Claude Command: Commit

Create safe, reviewable commits with clear messages.

## Core Rule

Each commit should capture one clear intent and include only the evidence needed to trust it.

## When To Use

- when user explicitly asks to commit local changes
- when staged or unstaged edits need atomic grouping
- when a clean conventional message is needed

## Workflow

1. Check current branch and staged status.
2. If on `main` or `master`, ask whether to create a feature branch first.
3. Unless `--no-verify` is passed, run project-appropriate verification checks before commit.
4. If nothing is staged, stage tracked and untracked relevant files.
5. Inspect full staged diff.
6. Decide whether to split into multiple atomic commits.
7. Create commit message(s) using conventional format with emoji.
8. Commit and report concise result.

## OpenCode Tool Alignment

- use git commands through `Bash`
- use existing staged state when the user has already curated files
- use local verification output as commit evidence instead of assumptions

## Verification Rule

Before commit, prefer the smallest command set that proves the staged change is safe enough to record.

- lint/type-only change -> lint/typecheck may be enough
- behavior change -> run tests for affected scope
- release-sensitive change -> run broader verification if available

## Commit Message Format

Format:

`<emoji> <type>: <imperative summary>`

Preferred mapping:

- ✨ `feat`
- 🐛 `fix`
- 📝 `docs`
- ♻️ `refactor`
- ✅ `test`
- 🔧 `chore`
- ⚡️ `perf`
- 🚨 `fix` (lint/type warnings)
- 🔒️ `fix` (security)

Keep subject under 72 chars, present tense, imperative mood.

## Split Rules

Split into separate commits when changes have different intent, such as:

- source code behavior + docs
- refactor + feature
- dependency updates + bug fix
- unrelated modules touched in one diff

## Command Options

- `--no-verify`: skip pre-commit checks

## Branch Naming Convention

When creating a branch from `main`/`master`, use:

```
<type>/<git-username>/<description>
```

Example: `feat/alice/add-export-command`

## Output Expectations

After committing, report:

- branch name
- files included
- commit hash and message
- whether checks were run or skipped
