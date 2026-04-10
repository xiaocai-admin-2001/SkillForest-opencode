---
name: context-compression
description: Compresses long-running sessions into a durable working summary that preserves files, decisions, current state, and next steps. Use when conversation history is getting too large, when you need to hand off work, or when token growth is starting to hurt task efficiency.
---

# Context Compression

## Core Rule

Optimize for tokens per task, not tokens per request.

If compression makes the agent re-discover files, decisions, or errors, it failed even if the summary is short.

## When To Use

Use this skill when:

- the session is becoming too long to keep full history comfortably
- you need a compact handoff before continuing implementation
- the conversation contains many explored dead ends and only the durable state should remain
- you are worried the agent may forget modified files, key decisions, or remaining work

Do not use this skill for tiny sessions or one-off questions.

## Workflow

### 1. Keep Only Durable State

Preserve the information needed to continue work without re-fetching:

- user goal and current scope
- files modified, created, or deleted
- key commands run and what they proved
- important errors, root causes, and unresolved risks
- current status and exact next steps

Drop noise:

- repeated exploration that led nowhere
- redundant command output
- conversational filler
- temporary hypotheses that were disproved

### 2. Use Anchored Sections

Always compress into the same structure so critical data is not silently lost.

Use these sections in order:

```markdown
## Goal
## Constraints
## Files Changed
## Evidence
## Decisions
## Current State
## Next Steps
```

If a section has nothing important, write `none` instead of omitting it.

### 3. Prefer Incremental Compression

If a summary already exists, do not rewrite everything from scratch.

- summarize only the newly-truncated span
- merge it into the existing anchored summary
- keep file paths, commit hashes, machine addresses, and config values exact

This reduces drift across repeated compressions.

### 4. Preserve the Artifact Trail

The most common failure is losing track of file state.

For every coding task, explicitly record:

- files read but not changed
- files modified
- files created
- tests added or updated
- binaries or deployment targets touched

Use exact paths.

### 5. Preserve Verification Evidence

When compression follows debugging or implementation work, keep the proof, not just the claim.

Good examples:

- `./build/task_cache_round_utils_test -> task cache round helpers work`
- `make -j2 -> Built target VDPServer`
- `10.31.164.83 task config: mode_type=3, task_frequency=1`

Bad examples:

- `tests passed`
- `build seems fine`
- `config was updated`

### 6. End With an Executable Resume Point

Compression is only complete if the next worker can continue immediately.

State:

- what is done
- what remains
- what should be checked next
- what command, file, or host to inspect first

## Output Template

Use this exact template for compressed summaries:

```markdown
## Goal
- <1-3 bullets>

## Constraints
- <hard constraints, environments, credentials source, safety notes>

## Files Changed
- Modified: `path`
- Added: `path`
- Read only: `path`

## Evidence
- `<command or observation> -> <result>`

## Decisions
- <decision and why>

## Current State
- <what is true now>

## Next Steps
1. <first concrete action>
2. <second concrete action>
```

## OpenCode Notes

- Prefer exact file paths, hostnames, ports, and command names.
- Keep summaries readable by humans; do not use opaque encodings.
- When compression follows coding work, include enough detail that the next step can be done without re-reading the whole repo.
- When compression follows debugging, include symptom, root cause evidence, and verification status.

## Anti-Patterns

- optimizing only for shortest possible summary
- dropping file paths or replacing them with vague descriptions
- saying `fixed` without proof
- rewriting an existing summary from scratch when an incremental merge would work
- preserving large raw outputs instead of the key evidence line

## Related References

- Use `systematic-debugging` when compression follows a debugging investigation.
- Use `verification-before-completion` when status claims depend on fresh command evidence.
- Use `writing-plans` when the next step is implementation planning rather than continued execution.
