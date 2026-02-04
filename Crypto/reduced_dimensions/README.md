# Reduced Dimensions - Crypto

- CTF: 0xL4ugh CTF 2025
- Category: Crypto
- Solver: W4ST3D
- Flag: `0xL4ugh{FLAG_NOT_CAPTURED_IN_NOTES}`

---

## Challenge
> "I'm super bored of working on regular RSA. So, I implemented a 2022 optimization on it. Go ahead and check this out."

---

## Overview
The challenge implements an RSA-like cryptosystem using Quaternions represented as $4 \times 4$ matrices. While the encryption appears secure, a linear relationship between quaternion components allows trivial factorization of $n$.

---

## Root Cause
The quaternion components are constructed with linear relationships to the primes $p$ and $q$. By finding a linear combination that eliminates both $m$ and $q$, we can directly compute a multiple of $p$ from the ciphertext and factor $n$.

---

## Exploitation Steps

### 1. Understand the Quaternion Construction
The quaternion components relate to message $m$ and primes $p, q$:
- $a_0 = m$
- $a_1 = m + 3p + 7q$
- $a_2 = m + 11p + 13q$
- $a_3 = m + 17p + 19q$

### 2. Find the Linear Relationship
Compute $L = 2a_2 - a_1 - a_3$:
$$ L = 2(m + 11p + 13q) - (m + 3p + 7q) - (m + 17p + 19q) $$
$$ L = (2m - m - m) + (22p - 3p - 17p) + (26q - 7q - 19q) $$
$$ L = 0m + 2p + 0q = 2p $$

### 3. Factor n
The same combination on ciphertext components:
$$ \gcd(2c_2 - c_1 - c_3, n) = p $$

### 4. Decrypt
With $n$ factored, solve the RSA problem in $GL_2(\mathbb{F}_p)$ and $GL_2(\mathbb{F}_q)$ separately, then recombine using CRT.

### 5. Run Solver
```bash
python3 solve.py
```

---

## Files
- `reproduce_attack.py`: Test script verifying the mathematical attack
- `solve.py`: Final solution script extracting the flag
