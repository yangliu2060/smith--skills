# Upgrade Check

## Upgrade

`storm-research-agent` upgraded from a single-file skill to a Yao-style Production package.

## Added

- `agents/interface.yaml`
- `manifest.json`
- `references/workflow.md`
- `references/output-contract.md`
- `evals/trigger_cases.json`
- `evals/semantic_config.json`
- `evals/baseline_description.txt`
- `evals/improved_description.txt`
- `reports/output-risk-profile.md`
- `reports/artifact-design-profile.md`
- `reports/reference-scan.md`

## Preserved

- Chinese-first behavior for research output.
- Bilingual output only when explicitly requested.
- No external writes, X drafts, staging, or publishing by default.

## Boundary

This is Production, not Library or Governed.

## Verification

- Yao `validate_skill.py`: pass, no failures, no warnings.
- Yao `resource_boundary_check.py`: pass, no failures, no warnings.
- Yao `context_sizer.py`: pass, warning false, initial load 835 tokens within the 1000-token Production budget.
- Yao `trigger_eval.py`: pass, false positives 0, false negatives 0, precision 1.0, recall 1.0.
- System `quick_validate.py`: pass.

## Trigger Fix

The first trigger eval missed real Chinese user wording such as `先别写稿`, `五个视角`, `反方观点`, `证据强弱`, and `下一步最小实验`. `evals/semantic_config.json` now maps those phrases to the existing STORM research concepts instead of weakening the threshold.

## Next Directions

1. Add three real run samples from actual X material.
2. Add confusion cases against `smith-longtwitter`, `smith-xarticle`, and `x-article-translator`.
3. Revisit whether a deterministic formatter is worth adding after repeated real runs.
