---
name: storm-research-agent
description: Chinese-first STORM-style research and decision-support skill for validating topics, ideas, X posts, articles, products, tools, or workflows before writing. Use when the user asks for STORM research, multi-perspective research, contradiction maps, blind-spot analysis, evidence-grounded briefs, bilingual Chinese/English research output, or a decision card about whether something is worth turning into content, a business action, or a project. Excludes final social-post writing, X Article drafting, publishing, Feishu writes, and generic translation-only requests.
---

# storm-research-agent

## Boundary

Use this skill for research and decision support before writing. Do not write final posts, create X drafts, write to Feishu, create publish staging, send messages, or publish unless the user explicitly asks.

When the current project has a `03_analysis/` directory, save research output there. Otherwise, return the brief inline or use the path requested by the user. Stop before downstream writing or publishing skills.

## Default Language

Default to Chinese for Chinese-speaking readers.

Use English only when the user explicitly asks for English output. If the user asks for “双语”, “中英文两个版本”, or “Chinese and English versions”, produce 中文版 first and English version second. Both versions must preserve the same claims, sources, confidence scores, and decision.

## Required Inputs

Need:

- topic
- decision context

If either is missing, ask one concise question before continuing.

## Execution

Read `references/workflow.md` before running the research workflow.

Read `references/output-contract.md` before saving or reporting the result.

Use the output-risk profile in `reports/output-risk-profile.md` as the final self-check.

## Output Contract

Every valid result must include:

- research contract
- evidence pack with `sourced`, `inferred`, or `needs verification`
- five perspectives
- at least three contradictions
- at least one blind spot
- synthesis brief
- peer review with confidence scores
- final decision card

If sources are weak, say so and recommend the smallest next source to fetch.

## Package Evidence

This skill follows a Yao-style Production package shape:

- `manifest.json` for lifecycle metadata
- `agents/interface.yaml` for portable interface and compatibility
- `references/` for deferred workflow and output contract
- `evals/` for trigger regression cases
- `reports/` for output risk, artifact design, reference scan, and validation evidence
