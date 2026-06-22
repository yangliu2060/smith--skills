---
name: claude-review
description: "把 plan、架构文档、用户文档或 work-log 交给 Claude Code 做无界面评审。适合在实现前或阶段边界获得外部视角；技能会单次调用 `claude --print`，对 plan/架构目标自动串联 `plan-eng-review`，并返回结构化 Markdown 报告。"
argument-hint: "<plan|architecture|docs|work-log> <file_or_dir> [--deep]"
---

# claude-review — Claude 无界面评审

用一次 `claude --print` 获得 Claude 的独立评审，不开启完整交互会话。

## When To Invoke

| Situation | Type |
|---|---|
| Detailed implementation plan, about to start coding | `plan` |
| Module boundaries / system diagram drafted | `architecture` |
| README / API docs / user-facing docs before shipping | `docs` |
| STATUS.md / errors.md after a work session — verify honesty | `work-log` |

## Usage

```bash
~/.codex/skills/claude-review/scripts/claude-review <type> <file_or_dir> [--deep]
```

**Examples:**

```bash
# Review plan before implementation (auto-chains plan-eng-review)
~/.codex/skills/claude-review/scripts/claude-review plan ./docs/plan.md

# Architecture review with deep consultation (also chains office-hours)
~/.codex/skills/claude-review/scripts/claude-review architecture ./docs/design.md --deep

# Quality-check docs before shipping (single pass, no chain)
~/.codex/skills/claude-review/scripts/claude-review docs ./README.md

# Audit a work directory for buried failures
~/.codex/skills/claude-review/scripts/claude-review work-log ./.codexfree/
```

## What Happens

1. Script validates inputs and resolves absolute path
2. Assembles a headless-mode prompt (no AskUserQuestion, single final report)
3. Calls `claude --print --permission-mode bypassPermissions` once
4. For `plan` / `architecture`: Claude auto-invokes its `plan-eng-review` skill in the same session and consolidates
5. For `--deep` (plan / architecture only): Claude additionally chains the `office-hours` skill
6. Report streamed to stdout AND saved to `.claude-review/<timestamp>-<type>.md` in the current working directory

All skill chaining happens inside ONE Claude session — you pay for one `--print` invocation regardless of how many sub-skills are chained.

## Output Format

The report is always Markdown with this structure:

```
# Review Report — <type>
**Target:** <absolute path>
**Timestamp:** <UTC ISO>

## Executive Summary
...

## Critical Issues (must fix before proceeding)
...

## High-Priority Findings (should fix soon)
...

## Suggestions (nice to have)
...

## Chained: plan-eng-review  (only for plan/architecture)
...

## Chained: office-hours  (only with --deep)
...

## Decision
approve | revise | block
<1-2 sentence rationale>
```

Codex should read the report, treat `revise` findings as required fixes, then re-invoke the skill on the updated artifact. `block` means the artifact has fundamental problems and needs a rewrite, not a patch.

## Decision Taxonomy

| Decision | Meaning | Codex action |
|---|---|---|
| `approve` | Artifact is ready to proceed | Continue to next phase |
| `revise` | Issues found, fixable in place | Fix issues, re-invoke skill |
| `block` | Fundamental problem, not patchable | Halt; escalate to user |

## Why Headless?

Calling Claude interactively burns tokens on greetings, clarification, and tool overhead. `--print` mode:
- Single request → single response → exit
- All tool use happens inside one session
- No context carried across invocations
- Much lower token cost than a conversation

The tradeoff: Claude cannot ask follow-up questions. The script's prompt assumes sensible defaults and instructs Claude to produce a complete report in one pass.

## Skill Chain Reference

| Type | Initial review | Chains `plan-eng-review` | Chains `office-hours` |
|---|---|---|---|
| `plan` | ✅ | ✅ | only with `--deep` |
| `architecture` | ✅ | ✅ | only with `--deep` |
| `docs` | ✅ | ❌ | ❌ |
| `work-log` | ✅ | ❌ | ❌ |

`docs` and `work-log` don't chain because `plan-eng-review` is an architecture-review skill, not a copy-editing or audit skill.

## Prerequisites

- `claude` CLI installed (`npm install -g @anthropic-ai/claude-code`)
- User is logged into Claude Code (`claude --version` works)
- For `plan` / `architecture`: the `plan-eng-review` skill must be installed in the user's Claude skill directory (part of the gstack plugin)
- For `--deep`: the `office-hours` skill must be installed

## Files

- `scripts/claude-review` — main bash wrapper
- `references/review-prompts.md` — lens definitions for each review type (Claude reads these via the bash-assembled prompt)
