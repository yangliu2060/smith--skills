# Safety Rules

Network fixes can break connectivity, VPN access, DNS resolution, or remote work. Treat the machine as a live system.

## Hard Rules

- Do not modify settings before collecting a baseline.
- Do not run `sudo` commands without explicit user confirmation.
- Do not disable VPN, firewall, proxy, Little Snitch, AdGuard, Clash, Surge, Tailscale, or security tools blindly.
- Do not delete network locations, profiles, launch agents, or configuration files without a named rollback path.
- Do not batch multiple fixes. One change per pass.
- Do not present ISP speed as guaranteed device speed. Wi-Fi, NIC, router, cable, CPU, VPN, and server choice can cap results.

## Risk Classes

Safe read-only:
- OS/network inventory
- DNS config display
- ping and packet loss tests
- route table display
- interface MTU display
- process list and network usage snapshots

Low-risk but still ask first:
- DNS cache flush
- mDNSResponder restart
- DHCP renew
- Quitting a clearly identified user app that is consuming bandwidth

Risky:
- DNS server changes
- MTU changes
- VPN/proxy/split-tunnel edits
- network service order changes
- firewall/filter changes
- deleting stale network locations or profiles
- Windows TCP auto-tuning changes

## Rollback Requirement

Before any modification, state:
- Current value
- New value
- Command or UI path to restore the old value
- Verification command

If the old value cannot be captured, do not modify it.
