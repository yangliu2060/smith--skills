# Loop Doctor

Use this for audit and repair.

## Verdicts

```text
Verdict: Ready | Repair needed | Not actually a loop
Diagnosis: up to three material findings
Result: repaired loop or no repair needed
```

## Ready

Use when the loop has:

- feedback-driven next action
- concrete verification
- authority boundaries
- terminal states
- preserved state or records

Do not rewrite style-only issues.

## Repair Needed

Use when the loop is basically valid but missing a material piece:

- weak `next_action_rule`
- vague verification
- missing approval boundary
- missing terminal state
- no state record
- unclear trigger or exclusion

Repair the smallest part that makes it valid.

## Not Actually A Loop

Use when:

- feedback cannot change the next action
- it is only a fixed SOP, checklist, template, or one-off command
- it is a general systems feedback-loop analysis, not an AI-agent workflow loop

Return the correct alternative: goal, SOP, checklist, template, or systems analysis.
