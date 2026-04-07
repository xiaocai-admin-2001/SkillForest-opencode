---
name: verification-before-completion
description: Validates completion claims with fresh command evidence in OpenCode workflows. Use when status updates, handoffs, commits, PRs, or bug-fix reports depend on tests, lint, build, or reproduction results.
---

# Verification Before Completion

## Core Rule

No completion claim without fresh evidence from the exact command that proves it.

If the command was not run in the current workflow, report uncertainty instead of success.

## When To Use

- before saying a task is done
- before commit or PR creation
- after a bug fix or refactor
- when reporting test, lint, or build status

## Claim Gate

Before any success statement, run this sequence:

1. Identify the claim (tests pass, build passes, bug fixed, requirement complete).
2. Select one command that directly proves it.
3. Run the full command (not partial scope unless claim is partial).
4. Read output and exit status.
5. Report the result with evidence.

## Workflow

1. Identify the exact claim.
2. Run the smallest command that directly proves it.
3. Quote the key output line or result count.
4. State pass/fail with exact scope.

## Evidence Matrix

| Claim | Required evidence |
|---|---|
| Tests pass | Test command output shows 0 failures |
| Lint is clean | Linter output shows 0 errors |
| Build succeeds | Build command exits 0 |
| Bug is fixed | Reproduction test now passes |
| Regression covered | Test fails before fix and passes after fix |
| Task is complete | Requirement checklist is verified item-by-item |

## Response Patterns

Good:

```text
Ran `npm test` -> 128 passed, 0 failed.
All tests are passing.
```

```text
Ran `pytest tests/api/test_auth.py` -> 1 failed.
Auth flow is not fixed yet; failure is in token refresh path.
```

Bad:

```text
Should be fixed now.
Looks good.
Done.
```

## Red Flags

Stop and verify if any of these appear:

- "should", "probably", "seems"
- success wording before command output
- commit/PR preparation without fresh validation
- trust in previous runs or subagent reports

## Minimum Pre-Commit Verification

Use project-appropriate commands:

```bash
# Example only; adapt to project
npm test
npm run lint
npm run build
```

If one fails, report failure first, then next action.

## OpenCode Notes

- Fresh evidence in the current workflow beats memory from earlier turns.
- Tool output is the source of truth; subagent success messages are not.
- If verification is intentionally partial, state the exact scope instead of implying full success.

## Completion Template

```text
Verification run:
- Command: <command>
- Result: <pass/fail + key numbers>
- Evidence: <important output line>

Status:
- <accurate claim>
```
