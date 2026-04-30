---
name: weekly-report-writer
description: Use when writing a Chinese weekly report or next-week plan in a fixed, simple work-report format.
---

# Weekly Report Writer

## Overview
Write weekly reports in Chinese with a fixed format.
Keep it short, direct, and specific.

## When to Use
- User asks to write `周报`、`本周任务`、`下周计划`
- User gives rough notes and wants them rewritten into report format
- User wants the same report style reused in later sessions

Do not use when:
- The user wants a long project review or technical design document
- The user wants a casual chat summary instead of a formal weekly report

## Required Output Format
Always use this structure unless the user explicitly asks for a different one:

```text
`YYYYMMDD`

本周任务  
1、事项名称；状态；  
具体内容一段
2、事项名称；状态；  
具体内容一段

下周计划  
1、计划事项；  
具体内容一段
2、计划事项；  
具体内容一段
```

## Writing Rules
- Write in Chinese.
- Keep the tone natural and work-report oriented.
- For each `本周任务`, include:
  - what was actually handled
  - what technical or business issue was solved or narrowed down
  - what result, conclusion, or current state was reached
- Status should be explicit, such as `已完成` or `进行中`.
- For each `下周计划`, include:
  - the next action
  - the concrete direction or focus
- Default to short paragraphs, usually one sentence per item.
- Prefer plain wording like `完成了`、`处理了`、`继续排查`、`继续推进`.
- Do not write vague filler like `持续推进相关工作` unless the concrete direction is also stated.
- Do not over-explain background unless the user asks for a detailed version.
- Do not just rename the original note. Expand it into useful business content.

## Content Priorities
When source material is limited, prioritize these details:
1. What function, module, feature, or issue was worked on
2. What specific handling direction was taken
3. What difficulty, risk, or bottleneck was addressed
4. What current outcome was produced
5. What the next concrete step is

## Default Style Pattern
Use patterns like:
- `完成...，解决/明确...`
- `处理...，当前已...，仍需继续...`
- `明确后续采用...路线`
- `继续推进...，重点验证/排查...`

## Common Mistakes
- Only listing titles without concrete handling details
- Writing generic statements with no actual outcome
- Mixing `已完成` and `进行中` without saying what remains
- Writing next-week plans that repeat this week verbatim without new focus
- Writing paragraphs that are too long for a normal weekly report

## Response Behavior
- If the user provides raw bullets, convert them directly into the template.
- If project context exists, infer concrete details from current work, but do not fabricate unsupported claims.
- If details are missing, prefer conservative, evidence-based wording such as `当前已完成一轮验证`、`仍需继续排查`.
