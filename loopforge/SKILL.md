---
name: loopforge
description: Compile, validate, repair, and package AI-agent workflow loop specs. Use to extract, forge, doctor, or package repeatable agent workflow loops, or distinguish loops from goals, SOPs, checklists, cron jobs, one-shot tasks, and systems-thinking feedback loops. Do not use for official loop search, direct execution, or pure /goal commands.
metadata:
  lifecycle_stage: library
  context_budget_tier: production
  source_inspiration: Forward Future Loop Library, qiaomu-goal-meta-skill, yao-meta-skill
---

# Loopforge

Turn fuzzy workflows into reusable AI-agent workflow loop specs.

## Route

Choose one path:

- `Extract`: convert notes, transcripts, prompts, artifacts, or history into a loop spec.
- `Forge`: create a new loop spec from the user's intended recurring workflow.
- `Doctor`: audit and minimally repair an existing loop spec.
- `Package`: prepare a loop spec for reuse or publication.

Do not handle:

- official published loop search; send that to the official Loop Library skill or catalog
- direct loop execution; hand off to the runtime
- pure `/goal` writing; use a goal skill when available
- general systems-thinking feedback-loop analysis

## Intake

Ask one high-leverage question by default; ask up to three only when answers materially change the spec. Default only when grounded or safe no-op. Ask for permissions, security, production writes, external messages, private data, and validation.

## Required Reading

- For boundary decisions, read `references/loop-vs-goal-sop-checklist.md`.
- For spec fields, read `references/loop-spec-v1.md`.
- For repair work, read `references/loop-doctor.md`.
- For examples or pattern help, read `references/case-patterns.md` and `references/templates.md`.

## Output Contract

Return one:

- a concise prompt-mode loop the user can copy
- a full `loop-spec-v1` YAML or JSON spec, followed by a copy-ready Loop Prompt companion unless the user asks for machine-only output
- a doctor verdict: `Ready`, `Repair needed`, or `Not actually a loop`
- a package checklist for reuse or publication

Every spec must satisfy `references/loop-spec-v1.md`: identity, trigger/exclusion, inputs, authority, state, round, `next_action_rule`, `working_signal`, `acceptance_gate`, terminal states, outputs, provenance, and optional `execution_handoff`.

When outputting YAML/JSON, also finish with the module-based `Loop Prompt` from `references/templates.md`. YAML/JSON is the source; the prompt is the copy/use entry.

## Validation

For YAML/JSON specs, run:

```bash
python3 scripts/lint_loop_spec.py <spec-file>
```

Use `--profile template` for reusable templates with declared placeholders. Use `--profile runnable` when the loop is ready to run and placeholders must be gone.

If the linter fails, fix the spec before presenting it as ready.
