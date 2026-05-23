# macOS Read-Only Commands

Run commands selectively. Do not dump huge outputs into the final answer; summarize the signal.

## System And Active Network

```bash
sw_vers
networksetup -listallhardwareports
route -n get default
ifconfig
```

## Throughput And Responsiveness

```bash
networkQuality -v
```

If `speedtest-cli` exists:

```bash
speedtest-cli --simple
```

## Latency And Loss

```bash
ping -c 20 1.1.1.1
ping -c 20 8.8.8.8
ping -c 20 google.com
```

Compare IP ping with domain ping. If domain ping is much slower to start or fails while IP ping works, investigate DNS.

## DNS

```bash
scutil --dns
dscacheutil -q host -a name google.com
```

For timing:

```bash
time dscacheutil -q host -a name google.com
```

## Wi-Fi

```bash
system_profiler SPAirPortDataType
```

If available:

```bash
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I
```

Interpretation:
- RSSI closer to 0 is stronger. `-45 dBm` is strong, `-75 dBm` is weak.
- High noise or low RSSI points to Wi-Fi, not ISP.
- 2.4 GHz congestion often caps speed and raises latency.

## MTU

```bash
ifconfig | awk '/^[a-z0-9]/ {iface=$1} /mtu/ {print iface, $0}'
```

Do not change MTU unless symptoms fit and packet-size tests support it.

## Routes, VPN, Proxy

```bash
netstat -rn
scutil --proxy
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
networksetup -getsocksfirewallproxy Wi-Fi
```

The service may not be named `Wi-Fi`; use `networksetup -listallnetworkservices` first when needed.

## Processes

```bash
ps aux | sort -nrk 3 | head -15
ps aux | sort -nrk 4 | head -15
```

For network usage, `nettop` can be useful but noisy:

```bash
nettop -P -L 1
```

Summarize obvious user apps. Do not kill anything without confirmation.

## Reversible Actions That Need Confirmation

Flush DNS cache:

```bash
dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Changing DNS, MTU, proxy, VPN, or network service order requires capturing the old value first and giving rollback steps.
