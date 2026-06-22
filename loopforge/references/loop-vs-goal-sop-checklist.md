# Loop vs Goal vs SOP vs Checklist

Use this file when routing is ambiguous.

## Loop

An AI-agent workflow loop is a reusable mechanism where evidence from each round can change the next action.

It must have:

- a trigger
- facts or inputs to observe
- a next-action rule
- verification evidence
- state or records that survive the round
- terminal states
- authority boundaries

Good loop test:

```text
If the latest evidence cannot change what the agent does next, this is not a loop.
```

## Goal

A goal is one execution contract for a specific outcome.

Use a goal when the user mainly needs:

- one concrete result
- success criteria
- constraints
- iteration policy for this task
- stop and pause conditions

A loop may include `execution_handoff`, but the loop itself is not the execution container.

## SOP

An SOP is a fixed sequence. It can repeat, but feedback does not decide the next action.

Use SOP when the task is:

- follow these steps every time
- run this checklist on schedule
- no branch based on observed evidence

## Checklist

A checklist confirms coverage. It asks whether items were covered, not what the agent should do next.

Use checklist when the output is only:

- pass/fail coverage
- missing-item list
- static review criteria

## One-Shot Work

One-shot work can still be a loop instance when each round's evidence changes the next move, such as debugging or investigation.

Do not reject a loop only because it may run once. Reject it when there is no feedback-driven next action.

## Out Of Scope

General systems-thinking feedback loops, growth flywheels, reinforcing loops, balancing loops, and causal-loop diagrams are not Loopforge's job unless the user asks to convert them into an AI-agent workflow loop.
