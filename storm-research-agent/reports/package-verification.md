# Package Verification

Date: 2026-06-19

## Source Standard

Primary reference: `yaojingang/yao-meta-skill`, cloned and inspected during packaging.

Read standards:

- `SKILL.md`
- `references/operating-modes.md`
- `references/resource-boundaries.md`
- `references/skill-engineering-method.md`
- `references/gate-selection.md`
- `references/output-quality-risk.md`
- `references/packaging-contracts.md`
- `evals/README.md`
- validator script help and source for validation, resource boundary, context sizing, trigger eval, and governance checks

## Selected Mode

Production mode.

Reason: this is a reusable local project skill with routing and output-quality risk, but it is not a public marketplace package or infrastructure-critical governed package.

## Validation Evidence

- `python3 <yao-meta-skill>/scripts/validate_skill.py storm-research-agent`
  - Result: `ok: true`
  - Failures: `[]`
  - Warnings: `[]`
- `python3 <yao-meta-skill>/scripts/resource_boundary_check.py storm-research-agent`
  - Result: `ok: true`
  - Initial load: `835 / 1000` production budget tokens
  - Unused resource dirs: `[]`
  - Deferred governance: not required
- `python3 <yao-meta-skill>/scripts/context_sizer.py --json storm-research-agent`
  - Warning: `false`
  - Initial load: `835 / 1000` production budget tokens
- `python3 <yao-meta-skill>/scripts/trigger_eval.py --description-file storm-research-agent/evals/improved_description.txt --baseline-description-file storm-research-agent/evals/baseline_description.txt --cases storm-research-agent/evals/trigger_cases.json --semantic-config storm-research-agent/evals/semantic_config.json`
  - False positives: `0`
  - False negatives: `0`
  - Precision: `1.0`
  - Recall: `1.0`
  - Buckets: `5/5` should trigger, `5/5` should not trigger, `2/2` near neighbor
- `python3 <skill-creator>/scripts/quick_validate.py storm-research-agent`
  - Result: `Skill is valid!`

## Final Boundary

No Feishu writes, no X draft creation, no staging, and no publishing happened during this upgrade.
