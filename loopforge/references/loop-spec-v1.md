# Loop Spec v1

Use YAML or JSON. YAML is easier for humans; JSON is better for automation.

When producing a spec for a user, include a copy-ready Loop Prompt after the YAML/JSON unless the user asks for machine-only output.

## Required Fields

```yaml
spec_version: 1
kind: agent-workflow-loop
status: draft | provisional | tested | published
name:
purpose:
use_when:
do_not_use_when:
parameters: {}
inputs: []
authority:
  may_read: []
  may_write: []
  must_ask_before: []
state:
  stores: []
  update_rule:
round:
  observe:
  choose:
  act:
  verify:
  record:
next_action_rule:
working_signal:
acceptance_gate:
terminal_states:
  success:
  clean_noop:
  blocked:
  approval_required:
  exhausted:
  stagnated:
outputs: []
provenance:
  sources: []
  generated_at:
execution_handoff:
  enabled: false
  target:
  notes:
```

## Field Rules

- `use_when` describes when feedback can change the next action.
- `do_not_use_when` names near-neighbor tasks that should route elsewhere.
- `authority.must_ask_before` covers destructive writes, production, external messages, paid actions, private data, and account changes.
- `round.observe` names the evidence source.
- `round.choose` explains how evidence selects the next action.
- `round.verify` names concrete proof: command, log, file, screenshot, API response, human approval, or external read-back.
- `round.record` preserves enough state for the next round.
- `next_action_rule` is the core of the loop. If it is missing, this is probably an SOP.
- `working_signal` is the leading indicator that the current attempt is improving.
- `acceptance_gate` is the condition before declaring success.
- `terminal_states` must include success, clean no-op, blocked, approval required, exhausted, and stagnated.
- `execution_handoff` is optional and runtime-neutral. Do not hard-code `/goal`, cron, GitHub Actions, or any private runtime as the only target.

## Status

- `draft`: useful but incomplete
- `provisional`: internally coherent but not field-tested
- `tested`: verified on at least one realistic case
- `published`: ready for external reuse, with provenance and notices
