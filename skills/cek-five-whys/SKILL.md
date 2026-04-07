---
name: kaizen:why
description: Performs iterative Five Whys root cause analysis from symptom to systemic cause. Use when debugging, reviewing incidents, or explaining why a repeated failure keeps happening.
argument-hint: Optional issue or symptom description
---

# Five Whys Analysis

Use Five Whys to move from symptom to cause without stopping at the first technical explanation.

## Core Rule

Do not stop at the first broken component; keep asking why until you reach a process, design, or control gap.

## When To Use

- repeated bug or incident analysis
- postmortem follow-up
- flaky test or workflow failure that keeps returning
- situations where "human error" sounds like a fake root cause

## Workflow

1. State the symptom precisely.
2. Ask why it happened.
3. Ask why the previous answer was possible.
4. Continue until you hit a systemic cause.
5. Validate by walking from root cause back to symptom.
6. Propose fixes at the root-cause layer.

## Command Form

`/why [issue_description]`

## Variables

- `ISSUE`: problem or symptom to analyze
- `DEPTH`: default 5, but stop earlier or branch if evidence says so

## OpenCode Notes

- Use with `systematic-debugging` after evidence is collected.
- Use with `verification-before-completion` once a root-cause fix is claimed.
- Branch analysis is allowed when one symptom has multiple independent causes.

## Examples

### Example 1: Production Bug

```
Problem: Users see 500 error on checkout
Why 1: Payment service throws exception
Why 2: Request timeout after 30 seconds
Why 3: Database query takes 45 seconds
Why 4: Missing index on transactions table
Why 5: Index creation wasn't in migration scripts
Root Cause: Migration review process doesn't check query performance

Solution: Add query performance checks to migration PR template
```

### Example 2: CI/CD Pipeline Failures

```
Problem: E2E tests fail intermittently
Why 1: Race condition in async test setup
Why 2: Test doesn't wait for database seed completion
Why 3: Seed function doesn't return promise
Why 4: TypeScript didn't catch missing return type
Why 5: strict mode not enabled in test config
Root Cause: Inconsistent TypeScript config between src and tests

Solution: Unify TypeScript config, enable strict mode everywhere
```

### Example 3: Multi-Branch Analysis

```
Problem: Feature deployment takes 2 hours

Branch A (Build):
Why 1: Docker build takes 90 minutes
Why 2: No layer caching
Why 3: Dependencies reinstalled every time
Why 4: Cache invalidated by timestamp in Dockerfile
Root Cause A: Dockerfile uses current timestamp for versioning

Branch B (Tests):
Why 1: Test suite takes 30 minutes
Why 2: Integration tests run sequentially
Why 3: Test runner config has maxWorkers: 1
Why 4: Previous developer disabled parallelism due to flaky tests
Root Cause B: Flaky tests masked by disabling parallelism

Solutions: 
A) Remove timestamp from Dockerfile, use git SHA
B) Fix flaky tests, re-enable parallel test execution
```

## Anti-Patterns

- stopping at the first component failure
- accepting "human error" as final answer
- proposing symptom fixes before validating the chain

## Notes

- Don't stop at symptoms; keep digging for systemic issues
- Multiple root causes may exist - explore different branches
- Document each "why" for future reference
- Consider both technical and process-related causes
- The magic isn't in exactly 5 whys - stop when you reach the true root cause
- Stop when you hit systemic/process issues, not just technical details
- Multiple root causes are common—explore branches separately
- If "human error" appears, keep digging: why was error possible?
- Document every "why" for future reference
- Root cause usually involves: missing validation, missing docs, unclear process, or missing automation
- Test solutions: implement → verify symptom resolved → monitor for recurrence
