# Diagnostic Playbook

Use this order. It prevents fake fixes and isolates the real layer.

## 1. Define The Failure

Ask or infer:
- What is slow: download, upload, ping, DNS lookup, only some sites, or all traffic?
- Connection type: Wi-Fi, Ethernet, hotspot, VPN, proxy, corporate network
- Claimed plan speed and actual measured speed
- Whether other devices on the same network are also slow
- Whether the problem appears only with VPN/proxy on

## 2. Baseline Metrics

Collect:
- Throughput: speed test or `networkQuality`
- Latency and loss: stable IP ping and domain ping
- DNS: resolver list and lookup timing
- Route: default gateway, active interface, VPN routes
- Wi-Fi: RSSI/noise/channel when available
- MTU: interface MTU
- Background traffic: top network or process snapshot

## 3. Interpret Patterns

Low IP ping, slow domain lookup:
- Suspect DNS resolver, DoH, proxy DNS, captive portal, or VPN DNS.

High gateway ping:
- Suspect Wi-Fi signal, interference, router load, bad cable, or local LAN issue.

Good gateway ping, high public IP ping:
- Suspect ISP, VPN, routing, bufferbloat, or remote test server.

Fast without VPN, slow with VPN:
- Suspect split tunnel, DNS through VPN, MTU, firewall inspection, or VPN server load.

Download slow, upload normal:
- Suspect Wi-Fi PHY rate, server selection, ISP shaping, router CPU, VPN bottleneck.

Upload slow, download normal:
- Suspect cloud sync, bufferbloat, ISP upload cap, VPN overhead.

Only one browser slow:
- Stop. This is a browser issue, not this skill's scope. Report handoff to a future browser skill.

Whole Mac slow:
- Stop. This is system performance, not this skill's scope. Report handoff to a future Mac performance skill.

## 4. Candidate Fixes

Prefer:
- Change the test server or test method before changing the machine.
- Move closer to router or test Ethernet before tuning TCP.
- Identify bandwidth hogs before changing DNS.
- Compare VPN on/off before editing split tunnel.
- Verify MTU symptoms before changing MTU.

Avoid:
- "Optimize everything" scripts
- MTU changes without packet-size evidence
- DNS changes without DNS timing evidence
- Killing processes without identifying ownership and impact
