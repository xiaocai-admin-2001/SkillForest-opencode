---
name: test-driven-development
description: Enforces red-green-refactor workflow in local OpenCode development. Use before writing production code, and when adding regression tests for bug fixes or behavior changes.
---

# Test-Driven Development (TDD)

## Core Rule

Write a failing test first, then minimal code to pass, then refactor safely.

If the test did not fail first, it does not prove new behavior.

## When To Use

- new feature behavior
- bug fix with regression risk
- refactor that changes observable behavior

## TDD Loop

1. Red: add one test for one behavior.
2. Verify red: run test and confirm expected failure.
3. Green: add minimal production code.
4. Verify green: run focused and related tests.
5. Refactor: improve structure without changing behavior.
6. Repeat for next behavior.

## OpenCode Notes

- Use repository-native test commands instead of forcing one framework.
- Keep the failing-first proof in current tool output so later verification is easy to cite.
- Pair this skill with `verification-before-completion` before claiming implementation is done.

## Red Checklist

- test name describes behavior clearly
- test checks outcome, not implementation details
- failure reason matches missing behavior (not typo/setup issue)

Example run:

```bash
npm test path/to/test
```

## Green Checklist

- smallest change to make failing test pass
- no extra features hidden in same change
- no broad refactor before passing state

## Refactor Checklist

- all tests stay green
- duplicate logic reduced
- naming and boundaries improved

## Regression Fix Pattern

For bug fixes:

1. Write failing test that reproduces bug.
2. Confirm it fails.
3. Implement fix.
4. Confirm test passes.
5. Run related suite to catch side effects.

## Anti-Patterns

- writing production code first
- writing tests after implementation
- accepting a test that passes immediately
- testing mocks instead of behavior
- bundling feature work and refactor in one green step

## Quick Completion Gate

Before claiming done:

- [ ] new behavior has a failing-first test
- [ ] test now passes
- [ ] related tests pass
- [ ] no unverified assumptions remain

If any box is unchecked, continue the cycle.
