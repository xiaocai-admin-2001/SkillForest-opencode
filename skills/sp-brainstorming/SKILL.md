---
name: brainstorming
description: Facilitates structured idea-to-design discovery before implementation in OpenCode workflows. Use for new features, behavior changes, architecture choices, or ambiguous product requests that need a reviewed plan first.
---

# Brainstorming Ideas Into Designs

Turn rough requests into approved design decisions and a concrete spec.

## Core Rule

Do not start implementation until the user has approved the design.

## When To Use

- new feature requests
- UX or flow redesign
- unclear requirements
- multiple valid architecture options
- cross-cutting behavior changes

## Workflow

1. Explore context (code, docs, recent changes).
2. Ask one clarifying question at a time.
3. Propose 2-3 approaches with trade-offs.
4. Recommend one approach with rationale.
5. Present design sections incrementally and confirm alignment.
6. Write approved design spec.
7. Ask user to review spec before planning/implementation.

## Clarifying Questions

Focus on:

- goal and success criteria
- user constraints (time, scope, compatibility)
- non-goals
- rollout and risk tolerance

Prefer multiple-choice prompts when possible.

## Design Output Sections

Keep concise and practical:

- problem statement
- selected approach and rejected alternatives
- architecture/components
- data flow and state boundaries
- error handling and observability
- testing and verification strategy
- phased delivery plan

## Scale Guard

If request scope is too broad, decompose into independent sub-projects and brainstorm only the first slice.

## Spec Path

Default location:

`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`

After writing, do a quick self-review:

- remove TODO/TBD placeholders
- resolve internal contradictions
- remove ambiguous language
- ensure scope matches one implementation plan

## User Review Gate

Ask user to review spec before planning:

"Spec written at `<path>`. Please review and request changes before implementation planning."

## OpenCode Notes

- Explore repository context before asking questions whenever the codebase can answer them.
- Keep design sections short enough to survive long tool-heavy sessions.
- After approval, transition into planning rather than coding immediately.

## Visual Companion

If upcoming questions are strongly visual (layout, mockups, diagrams), offer browser companion once in a standalone message.

Use browser for visual comparisons; use terminal for textual trade-offs and requirements.

## Anti-Patterns

- jumping into code before approval
- asking multiple unrelated questions in one message
- proposing only one approach with no trade-offs
- generating long specs without decision points
- mixing implementation details before design is agreed

If accepted, load:
`skills/brainstorming/visual-companion.md`
