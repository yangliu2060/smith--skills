# Report Template

Use this structure when reporting results to the user.

## Diagnosis

- `[VERIFIABLE]` Baseline speed:
- `[VERIFIABLE]` Latency and packet loss:
- `[VERIFIABLE]` DNS:
- `[VERIFIABLE]` Active route/interface:
- `[VERIFIABLE]` Wi-Fi signal:
- `[VERIFIABLE]` VPN/proxy state:
- `[VERIFIABLE]` Background process signal:

## Findings

List findings in priority order. Each finding needs evidence and confidence.

Format:

```text
1. [JUDGMENT 高] Finding title
   Evidence: measured fact
   Why it matters: short reason
   Next action: one action only
```

## Proposed Actions

Safe checks already done:
- ...

Low-risk actions I can do after confirmation:
- Action:
- Why:
- Rollback:
- Verification:

Risky actions I reject for now:
- Action:
- Reason:

## Before/After

Use the same test before and after.

```text
Metric: before -> after
Download:
Upload:
Latency:
Packet loss:
DNS lookup:
```

## Reusable Prompt

When useful, give a compact prompt:

```text
/goal make my network faster safely.
First run read-only baseline checks: speed, latency, packet loss, DNS, MTU, Wi-Fi signal, proxy/VPN state, and bandwidth-hogging processes.
Do not change DNS, MTU, proxy, VPN, firewall, network locations, or kill processes without asking me first.
Find the top 1-3 likely causes, propose one reversible change at a time, show rollback steps, then rerun the same before/after tests.
```
