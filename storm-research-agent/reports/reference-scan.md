# Reference Scan

## External Benchmark

- `yaojingang/yao-meta-skill` was cloned and inspected during packaging.
- Borrowed standards:
  - lean `SKILL.md`
  - deferred `references/`
  - `agents/interface.yaml`
  - `manifest.json`
  - trigger eval cases
  - output risk and artifact design reports
  - Production gates: validate, resource boundary, trigger eval

## User Source

- Existing `storm-research-agent` skill in `.claude/skills/storm-research-agent/`.
- User requirement: Chinese audience; bilingual output only when requested.

## Local Fit

- Project routing lives in `00_system/skills-routing.md`.
- Research output belongs in `03_analysis/`.
- Final writing remains owned by Smith writing skills.

## Not Borrowed

- No scripts were added because this skill is judgment-heavy, not deterministic.
- No governed package gates were added because this is a local Production skill, not release-critical infrastructure.
- No full Review Studio or packaging archive was added because current reuse does not justify that cost.
