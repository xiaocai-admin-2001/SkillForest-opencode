---
name: systematic-debugging
description: Investigates bugs and failures with evidence-first root cause analysis in OpenCode workflows. Use before proposing fixes for failing tests, runtime issues, build breaks, flaky behavior, or unclear regressions.
---

# Systematic Debugging

## Core Rule

Do not propose fixes before root cause evidence exists.

## When To Use

- failing tests
- runtime errors
- flaky behavior
- build or CI failures
- performance regressions with unclear cause

## Four-Phase Workflow

### 1) Investigate

1. Capture exact error output and stack traces.
2. Reproduce with explicit steps.
3. Check recent changes (code, config, env, deps).
4. For multi-component systems, log each boundary to locate failure layer.

If it is not reproducible, gather more evidence; do not guess.

### 2) Compare

1. Find a similar working path in the same codebase.
2. Compare broken vs working flow.
3. List concrete differences (inputs, config, order, assumptions).

### 3) Hypothesize

1. State one hypothesis: "X fails because Y".
2. Run one minimal experiment.
3. Evaluate result, then keep or replace hypothesis.

No multi-fix bundles in this phase.

### 4) Fix and Verify

1. Add a failing test or deterministic reproduction.
2. Implement one targeted fix.
3. Re-run reproduction and related tests.
4. Confirm no collateral regressions.

## OpenCode Notes

- Prefer `Read`, `Grep`, and `Glob` for evidence gathering before broad shell exploration.
- Keep hypotheses explicit in the conversation so later fixes have a visible audit trail.
- If the bug spans services or scripts, instrument boundaries first and only then patch code.

## Escalation Rule

If two fix attempts fail, stop and re-open architecture assumptions before a third.

Signals of architecture issue:

- each fix moves failure elsewhere
- heavy coupling prevents isolated changes
- "simple" fix repeatedly expands scope

## Red Flags

Stop and return to phase 1 when you see:

- "quick fix now, investigate later"
- multiple simultaneous code changes
- solution proposal without evidence trail
- manual-only verification for a recurring bug

## Output Template

```text
Debug summary:
- Symptom:
- Reproduction:
- Root cause evidence:
- Fix applied:
- Verification commands and results:
- Remaining risk:
```

## Related References

- `root-cause-tracing.md` for deep call-stack tracing
- `defense-in-depth.md` for post-fix guards
- `condition-based-waiting.md` for flaky timing issues
