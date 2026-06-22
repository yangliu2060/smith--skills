---
name: storm-research-agent
description: "STORM 调研助手：用多视角证据分析选题、产品、工具或工作流是否值得推进。"
---

# storm-research-agent

## Boundary

这个技能只做写作前的调研和决策支持。除非用户明确要求，不写最终帖子、不创建 X 草稿、不写飞书、不创建发布暂存、不发送消息、不发布。

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
