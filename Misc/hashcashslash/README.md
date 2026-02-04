# HashCashSlash - Misc

- CTF: 0xL4ugh CTF 2025
- Category: Misc
- Solver: W4ST3D
- Flag: `0xL4ugh{FLAG_NOT_CAPTURED_IN_NOTES}`

---

## Challenge
> "Hash (#), Cash ($), and Slash (\\) - are these three characters enough to pwn?"

---

## Overview
A restricted shell challenge allowing only three characters: `#`, `$`, and `\`. The goal is to escape the restriction using bash variable expansion tricks, then locate and retrieve the flag from an internal service.

---

## Root Cause
The restricted shell validates input against a regex but then passes it to `eval`. Bash variable expansion (`$0`, `$#`, `$$`) combined with escape characters allows constructing a payload that spawns a new shell instance, bypassing the restriction entirely.

---

## Exploitation Steps

### 1. Bypass Restricted Shell
The payload `\$$#` works as follows:
1. `\$` → literal `$`
2. `$#` → number of positional parameters (usually `0`)
3. Result: `$0` → spawns a new shell instance

```python
payload = "\\$$#"
```

### 2. Enumerate the Environment
Once in the shell as `ctf` user:
- `/flag` and `/root` are inaccessible
- Enumerate running processes via `/proc/*/cmdline`

### 3. Discover Internal Service
Found background service:
```
socat TCP-LISTEN:42158,bind=127.0.0.1,reuseaddr,fork EXEC:cat /flag
```

### 4. Retrieve Flag
```bash
nc 127.0.0.1 42158
```

---

## Usage
```bash
python3 final_exploit.py
```

The script:
1. Connects to remote challenge
2. Sends `\$$#` to spawn shell
3. Connects to internal service on port 42158
4. Prints the flag

---

## Files
- `final_exploit.py`: Complete automated solver
- `solve_socket.py`: Fuzzer for testing character combinations
- `explore.py`: Environment probing script
- `possible_techniques.md`: Initial research notes
