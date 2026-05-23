---
name: codex-network-doctor
description: "USE THIS SKILL whenever user says 网络慢、网速慢、网速优化、网络延迟高、Wi-Fi 慢、DNS 慢、MTU 问题、packet loss、VPN/代理影响网速、mDNS 异常、speedtest-cli, or asks Codex to make the internet/network faster. Diagnose network performance with read-only baselines first, separate ISP/Wi-Fi/DNS/MTU/proxy/background-process causes, then propose reversible fixes with before/after verification."
---

# Codex Network Doctor

Use this skill to diagnose and improve local network performance without guessing or making unsafe system changes.

## Scope

Handle:
- Slow internet speed, unstable latency, packet loss, DNS delay, MTU symptoms
- Wi-Fi signal/interference problems
- VPN, proxy, split tunnel, firewall, or filtering conflicts
- Background processes consuming bandwidth
- Stale network locations/profiles and mDNS oddities
- Windows TCP auto-tuning only when the user explicitly says Windows

Do not handle:
- General Mac slowness, browser slowness, local LLM speed, disk cleanup, app crashes
- Router admin changes unless the user explicitly asks and provides access
- Production network, office network, cloud infrastructure, or shared enterprise devices without explicit authorization

## Required Workflow

1. Read `references/safety.md`.
2. Classify the symptom before running commands:
   - Bandwidth: low Mbps or unstable throughput
   - Latency: high ping, jitter, video call lag, game lag
   - DNS: websites pause before loading, IP ping is fine
   - Wi-Fi/LAN: bad signal, far from router, roaming, interference
   - VPN/proxy: only some sites slow, domestic/overseas split is wrong
   - MTU/TCP: stalls, large downloads hang, VPN-specific breakage
   - Background traffic: uploads/sync/downloads consume bandwidth
3. Read `references/diagnostic-playbook.md`.
4. If the machine is macOS, read `references/commands-macos.md`.
5. Establish a before baseline before proposing changes.
6. Make findings evidence-led. Use `[VERIFIABLE]` for measured facts and `[JUDGMENT 高/中/低]` for interpretation.
7. Separate actions into:
   - Safe read-only checks already run
   - Low-risk reversible actions
   - Risky actions requiring explicit confirmation
   - Actions to reject
8. Change only one variable per pass.
9. Run the same verification after each change.
10. Use `references/report-template.md` for the final response.

## Command Policy

Allowed by default:
- Read-only diagnostics such as `networkQuality`, `ping`, `scutil --dns`, `ifconfig`, `route`, `netstat`, `ps`
- Speed or latency tests that do not modify system state

Require explicit user confirmation:
- Killing or throttling processes
- Flushing DNS cache
- Restarting mDNSResponder
- Changing DNS, MTU, proxy, VPN, firewall, TCP parameters, network service order, or network location
- Deleting stale profiles or locations
- Router or modem changes
- Any command requiring `sudo`

Reject unless the user gives a narrow, reversible reason:
- Bulk deletion of network settings
- Disabling security tools blindly
- Random "optimization" commands from the internet
- Multiple simultaneous changes that make before/after verification meaningless

## Output Standard

Always give the user:
- What was tested
- What changed, if anything
- What the evidence says
- What remains unknown
- The exact before/after metrics
- Rollback steps for every modification

When the user wants a prompt to reuse, provide a compact `/goal` style prompt that includes constraints: read-only first, no unsafe changes, one change per pass, rollback, before/after test.
