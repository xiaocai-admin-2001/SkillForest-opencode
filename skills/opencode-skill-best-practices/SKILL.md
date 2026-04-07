---
name: opencode-skill-best-practices
description: Adapts skill authoring best practices to the local OpenCode environment. Use when creating, restructuring, or reviewing local skills, commands, and skill metadata.
---

# OpenCode Skill Best Practices

Translate general skill-writing principles into rules that fit this local OpenCode environment.

## Core Rule

Write skills for actual OpenCode behavior, not for an abstract platform.

That means the skill must match:

- current tool names and constraints
- local folder layout under `C:/Users/Administrator/.claude/skills`
- optional OpenCode frontmatter extensions already used in this repo
- local discovery and display needs in `SKILLS_REGISTRY.csv`

## When To Use

- creating a new local skill
- porting a skill from Anthropic, AgentSys, Superpowers, or elsewhere
- rewriting metadata for better trigger quality
- shortening an overgrown `SKILL.md`
- aligning a skill with local tools, registry, and UI display

## OpenCode Authoring Model

In this environment, skills are discovered by metadata first and then executed through local tools and workflow rules.

Optimize for three things at the same time:

1. Trigger accuracy: the right skill is selected.
2. Execution clarity: the steps are easy to follow with local tools.
3. Maintainability: the skill is easy to review in the registry and skill manager.

## Frontmatter Rules

### Required fields

- `name`: stable skill identifier already used in local ecosystem
- `description`: one-line discovery text that says what it does and when to use it

### Optional local fields

Use only when they materially help behavior:

- `argument-hint`: for command-like skills that accept flags or extra input
- `model`: only when the task truly benefits from a smaller or specific model
- `allowed-tools`: only when tool restrictions are part of the skill contract

Do not add optional fields by default.

## Naming Rules

- Keep existing installed skill IDs stable unless you are intentionally migrating them.
- Prefer names that are short, specific, and easy to reference in conversation.
- Prefixes like `cek-`, `sp-`, `ags-`, `tob-` are acceptable when they already organize your library.
- Avoid vague names like `helper`, `utils`, `workflow`, or `tools` without domain context.

## Description Formula

Use this format:

```text
<What the skill does>. Use when <task, trigger, or situation>.
```

Good examples:

- `Investigates bugs with evidence-first root cause analysis. Use before proposing fixes for failing tests, runtime errors, or unstable behavior.`
- `Creates atomic git commits with conventional messages. Use when local changes are ready to commit and need clean commit structure.`

Bad examples:

- `Helps with development`
- `Useful for many coding tasks`
- `Can do debugging and coding and planning`

## Recommended SKILL.md Structure

Use a compact structure that matches how OpenCode actually works:

1. `# Title`
2. `## Core Rule`
3. `## When To Use`
4. `## Workflow`
5. `## Checks / Output Template / Anti-Patterns` as needed
6. `## Related References` for one-level-deep supporting files

Default to short sections, direct language, and actionable bullets.

## Progressive Disclosure

- Keep main `SKILL.md` focused on decisions and workflow.
- Move long references, examples, scripts, or edge-case material into sibling files.
- Link supporting files directly from `SKILL.md`.
- Avoid reference chains like `SKILL.md -> advanced.md -> details.md`.

If a file is longer than about 100 lines, add a short table of contents at the top.

## OpenCode Tool Alignment

When a skill recommends actions, align them with the tools available here.

- file reads -> `Read`
- file search -> `Glob`
- content search -> `Grep`
- code edits -> `apply_patch`
- terminal commands -> `Bash`
- structured planning -> `TodoWrite`
- multi-step exploration -> `Task`

Do not write workflows that depend on tools not available in this environment.

## Workflow Design Rules

- Prefer one clear default path over many equivalent options.
- Use checklists for complex tasks.
- Add a validation loop when mistakes are costly.
- Make escalation points explicit: when to stop, ask, verify, or decompose.
- Favor "do X, then verify Y" over abstract advice.

## OpenCode-Specific Integration

When you change or add a local skill, also review:

- `C:/Users/Administrator/.claude/skills/SKILLS_REGISTRY.csv`
- skill display names and purpose text used by the skill manager
- whether the skill name is understandable in Chinese-facing UI context

The registry entry should explain the skill's practical purpose, not just its origin.

## Migration Rules For Imported Skills

When adapting an imported skill from Anthropic or another ecosystem:

1. Preserve the useful core behavior.
2. Remove platform assumptions that do not apply locally.
3. Rewrite metadata for local trigger quality.
4. Replace generic tool references with OpenCode-compatible actions.
5. Shorten repeated doctrine into compact rules and templates.

## Validation Checklist

Before considering a skill rewrite complete:

- [ ] `name` is still stable and recognizable
- [ ] `description` clearly states what + when
- [ ] body structure is short and scannable
- [ ] workflow can be executed with local tools
- [ ] supporting files are linked only one level deep
- [ ] registry purpose text matches the rewritten skill
- [ ] the skill reads well in both raw markdown and skill manager UI

## Rewrite Template

Use this pattern when refactoring a local skill:

```text
1. Keep the original intent.
2. Rewrite description for trigger quality.
3. Reduce the body to core rule, use cases, workflow, checks.
4. Move bulky examples or doctrine to supporting files if needed.
5. Update registry purpose and notes.
6. Re-read the final file as if it were loaded cold during a task.
```

## Anti-Patterns

- copying Anthropic guidance word-for-word without local adaptation
- adding optional frontmatter fields with no behavioral reason
- descriptions that list everything and trigger nothing
- long manifesto-style files with no executable workflow
- imported skills whose registry purpose is still generic or wrong
- advice that conflicts with local tool restrictions

## Bottom Line

The best local skill is easy to trigger, easy to execute, and easy to maintain.

If a rule does not improve real OpenCode behavior, remove or rewrite it.
