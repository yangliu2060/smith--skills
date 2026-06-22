# Templates

## Prompt Mode

```text
Loop: <name>
Use when: <trigger>
Do not use when: <exclusions>
Inputs: <facts or files>
Round:
1. Observe <evidence>.
2. Choose <next action based on evidence>.
3. Act <one bounded change>.
4. Verify <proof>.
5. Record <state for next round>.
Continue when: <signal>
Stop when: <terminal states>
Ask before: <authority boundary>
Outputs: <artifacts>
```

## Spec Plus Prompt Output

Use this when creating a YAML/JSON loop spec. Output both parts unless the user asks for machine-only output.

```text
## Loop Spec

<YAML or JSON loop-spec-v1>

## Loop Prompt

You are running this AI-agent workflow loop: <name>.

Module 1: Use When
<use_when>

Module 2: Do Not Use When
<do_not_use_when>

Module 3: Inputs
<inputs and required facts>

Module 4: Authority
You may read: <may_read>
You may write: <may_write>
Ask before: <must_ask_before>

Module 5: One Round
1. Observe: <round.observe>
2. Choose: <round.choose>
3. Act: <round.act>
4. Verify: <round.verify>
5. Record: <round.record>

Module 6: Next Action Rule
<next_action_rule>

Module 7: Working Signal
<working_signal>

Module 8: Acceptance Gate
<acceptance_gate>

Module 9: Stop States
Success: <terminal_states.success>
Clean no-op: <terminal_states.clean_noop>
Blocked: <terminal_states.blocked>
Approval required: <terminal_states.approval_required>
Exhausted: <terminal_states.exhausted>
Stagnated: <terminal_states.stagnated>

Module 10: Outputs
<outputs>

Now run one bounded round. First restate the user's goal and endpoint, then execute only the next valid action.
```

## Doctor Output

```text
Verdict: Ready | Repair needed | Not actually a loop
Diagnosis:
- <finding 1>
- <finding 2>
- <finding 3>
Result:
<minimal repaired loop or correct alternative>
```

## Package Checklist

```text
- SKILL.md has route, exclusions, output contract, and required reading.
- references/ holds long guidance.
- scripts/ holds deterministic lint or render logic.
- THIRD_PARTY_NOTICES.md exists when external sources influenced packaged examples.
- No private paths, accounts, tokens, internal domains, or project-specific rules.
- A runnable lint or self-check passes.
```
