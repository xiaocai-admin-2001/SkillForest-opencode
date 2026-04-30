---
name: session-history-snapshot
description: Use when ending a coding session, handing off work to a new conversation, or after meaningful local changes when you need a durable project snapshot, progress log, and next-step summary.
---

# Session History Snapshot

## Overview

Use this skill to leave a durable local handoff trail inside a project before ending a conversation.

This skill is for project continuity, not version control. Use it alongside git, not instead of git.

## When to Use

- You changed code, config, docs, or workflow decisions
- You are about to end the current conversation
- You want the next conversation to recover context quickly
- You need a timestamped local diff snapshot and a human-readable summary

Do not use this for tiny no-op chats with no project impact.

## Required Workflow

1. Confirm the project has a local snapshot script
2. Run the project snapshot command with a one-line summary
3. Include next steps when there are follow-up actions
4. Tell the user where the handoff files were written

## Command Pattern

Run this from the project root:

```powershell
pwsh -File "<project>\Scripts\save_project_snapshot.ps1" -Summary "<one line summary>" -NextSteps "step 1; step 2"
```

For `E:\Dev\Projects\RTSPVideoWall`, use:

```powershell
pwsh -File "E:\Dev\Projects\RTSPVideoWall\Scripts\save_project_snapshot.ps1" -Summary "<one line summary>" -NextSteps "step 1; step 2"
```

## Expected Outputs

After running successfully, confirm these files exist:

- `ProjectHistory/latest-summary.md`
- `ProjectHistory/progress-log.md`
- `ProjectHistory/snapshots/*.patch`

## Response Pattern

Report back with:

- what summary was saved
- where the latest summary lives
- where the running log lives
- where the timestamped patch snapshot lives

## Common Mistakes

- Forgetting to run the snapshot step before ending the session
- Writing a vague summary like "updated stuff"
- Forgetting next steps when the work is incomplete
- Treating the snapshot as a replacement for a git commit

## RTSPVideoWall Note

For `E:\Dev\Projects\RTSPVideoWall`, the snapshot workflow is project-standard and should be used whenever a meaningful session ends.
