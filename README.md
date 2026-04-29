# 🔥 Web Stress Test — Multi-Vector Load Testing Tool

> Authorized penetration testing tool for server capacity evaluation under multi-vector load.

---

## 📋 Overview

Python-based stress tester that attacks at **Layer 3, 4, and 7** simultaneously — 5 attack vectors, 2000+ threads, fully configurable.

---

## ⚡ Attack Vectors

| Vector | Layer | What It Does |
|--------|-------|-------------|
| **HTTP Flood** | L7 | 270+ random paths, spoofed headers, session reuse |
| **TCP Flood** | L4 | Raw socket connections, exhausts backlog |
| **Slowloris** | L7 | Holds 9000+ connections open with partial headers |
| **UDP Flood** | L4 | 50 threads × 4 ports × random payloads |
| **ICMP Flood** | L3 | Oversized packets (65KB each) — needs root |

---

## ⚙️ Config

```python
TARGET   = "example.com"   # Change this
PORT     = 80              # 443 for HTTPS
THREADS  = 2000            # Total threads
DURATION = 600             # Seconds (10 min)
```

---

## 🚀 Usage

```bash
# Install
pip3 install requests urllib3

# Run
sudo python3 stress_test.py          # Full (with ICMP)
python3 stress_test.py               # User mode (ICMP skipped)
```

---

## 📊 Live Output

```
[⏱] 045s | [🔥] Hits: 14,291 | [⚡] Rate: 317/s | [⏳] Remaining: 555s
[⏱] 300s | [🔥] Hits: 81,556 | [⚡] Rate: 271/s | [⏳] Remaining: 300s
[✅] Completed! Total hits: 147,891
```

---

## 🛡️ Mitigation Checklist

| Problem | Fix |
|---------|-----|
| HTTP Flood | Rate limiting, WAF, CAPTCHA |
| TCP Flood | SYN cookies, connlimit iptables |
| Slowloris | `client_header_timeout`, nginx event-driven |
| UDP Flood | Firewall, port filtering |
| ICMP Flood | `icmp_echo_ignore_all=1` |
| Everything | CDN (Cloudflare, Akamai) |

---

## ⚠️ Legal

> **Authorized testing only.** Unauthorized use = CFAA violation (up to 10 yrs).

---

## 🏁 Quick Start

```bash
pip3 install requests urllib3
# Edit TARGET in script
sudo python3 stress_test.py
```
