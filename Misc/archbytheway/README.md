# Arch By The Way - Misc

- CTF: 0xL4ugh CTF 2025
- Category: Misc
- Solver: W4ST3D
- Flag: `0xL4ugh{1_us3_4rch_l1nux_btw_4nd_y0u_sh0uld_t00_p4cm4n_r0ck5}`

---

## Challenge
> "iUseArchBTW iUseArchBTW do you ?"

---

## Overview
The challenge file contains text resembling an Arch Linux conversation. The words repeat in patterns suggesting an esoteric programming language - specifically a Brainfuck substitution cipher where Arch-related words map to Brainfuck operators.

---

## Root Cause
The challenge uses a simple word-to-symbol substitution to encode a Brainfuck program. By identifying the mapping through frequency analysis and standard Brainfuck patterns (loops, increments), we can decode and execute the program.

---

## Exploitation Steps

### 1. Identify the Mapping
Based on frequency analysis and Brainfuck patterns:

| Word | Brainfuck Symbol |
|------|------------------|
| `arch` | `+` |
| `linux` | `-` |
| `the` | `[` |
| `way` | `]` |
| `i` | `>` |
| `use` | `<` |
| `btw` | `.` |

### 2. Decode and Execute
```bash
python3 solve.py
```

The solver:
1. Reads the `.archbtw` file
2. Replaces words with Brainfuck symbols
3. Executes the Brainfuck program
4. Outputs the flag

---

## Files
- `arch.archbtw`: Challenge file (encoded Brainfuck)
- `solve.py`: Python solver script
