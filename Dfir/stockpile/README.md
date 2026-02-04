# Stockpile - DFIR

- CTF: 0xL4ugh CTF 2025
- Category: DFIR
- Solver: W4ST3D
- Flag: `0xL4ugh{1t_w4s_just_@_warmup_52b6b6f771}`

---

## Challenge
> Analyze a Windows `Sysmon.evtx` log file to investigate a malware infection initiated by a user named Khaled. Answer 11 questions about the attack timeline, from initial access to persistence.

---

## Overview
A Digital Forensics and Incident Response (DFIR) challenge involving Windows Sysmon log analysis. The investigation traces a complete attack chain: malicious file download, execution, C2 communication, reconnaissance, and persistence establishment.

---

## Root Cause
A user downloaded a malicious executable (`monitorStock.exe`) from a fake finance domain. The malware established C2 communication with a Sliver framework server and set up registry-based persistence.

---

## Investigation & Answers

### 1. Initial Access
Artifacts from the `Downloads` folder logs:
- **Domain:** `app.finance.com`
- **Malicious File:** `monitorStock.exe`
- **Download Time:** `2025-02-07 04:37:06 UTC`

### 2. Execution
- **Execution Time:** `2025-02-07 04:41:24 UTC`
- **File Hash (SHA256):** `314AA91A2AD7770F67BF43897996A54042E35B6373AE5D6FEB81E03A077255A7`

### 3. C2 Communication
Network connection events (Event ID 3):
- **C2 Server:** `3.121.219.28:8888`
- **C2 Framework:** `Sliver` (identified via behavior analysis)

### 4. Discovery & Persistence
- **First Command:** `whoami`
- **Persistence Method:** Registry Run Key
  - **Registry Key:** `Software\Microsoft\Windows\CurrentVersion\Run`
  - **Registry Value:** `C:\Windows\Temp\monitorStock.exe`
  - **File Move Time:** `2025-02-07 04:43:51 UTC`
  - **Persistence Set Time:** `2025-02-07 04:45:03 UTC`

---

## Usage
```bash
# Run automated solver
python3 solve_challenge.py

# Manual evidence searches
python3 search_dump.py
python3 search_c2.py
```

---

## Files
- `Sysmon.evtx`: Evidence file (Windows System Monitor logs)
- `solve_challenge.py`: Automated solver for all 11 questions
- `search_dump.py`: String search utility for `.evtx` files
- `search_c2.py`: C2 framework indicator hunter
