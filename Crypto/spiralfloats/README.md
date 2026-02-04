# SpiralFloats - Crypto

- CTF: 0xL4ugh CTF 2025
- Category: Crypto
- Solver: W4ST3D
- Flag: `0xL4ugh{B1naryS3archM0not0n1c}`

---

## Challenge
> "A flag was turned into a real number, pushed through a spiral, then partially erased. Dumb brute won't cut it."
>
> The flag format is `0xL4ugh{}`.

---

## Overview
The flag is converted to a floating-point number, transformed through an iterative "spiral" function using the golden ratio, and output as a decimal string with specific digits masked (`?`). We must reverse the transformation and recover the masked digits to retrieve the flag.

---

## Root Cause
The spiral function is **monotonic** and invertible. By implementing an inverse spiral function and using a guided brute-force approach on the masked digits (exploiting the monotonicity), we can recover the original flag integer.

---

## Exploitation Steps

### 1. Understand the Spiral Function
The spiral iteratively transforms a real number `x`:
```python
r = i / iterations
x = r * sqrt(x*x + 1) + (1 - r) * (x + phi)
```

### 2. Implement Inverse Spiral
Solve the quadratic equation from the forward step:
`y = r * sqrt(x^2 + 1) + (1 - r) * (x + phi)`

Step backwards from iteration 80 to 0 to recover original `x`.

### 3. Determine Flag Length
Initial `x` is: `x = R(flag_int) * 10^(-flen)`

Test different lengths until the inverted value starts with digits corresponding to `0xL4ugh{`. Flag length is **30 bytes**.

### 4. Guided Brute-force Recovery
Masked indices: 8, 16, 25, 33, 42, 50, 59, 67

For each hole:
1. Try digits 0-9
2. Invert the spiral
3. Check if revealed bytes form valid ASCII
4. Select digit producing readable text

### Step-by-Step Recovery
| Hole Index | Digit | Recovered Partial Flag |
|------------|-------|------------------------|
| 8          | 5     | `0xL4ugh{` |
| 16         | 5     | `0xL4ugh{` |
| 25         | 9     | `...B1nar` |
| 33         | 3     | `...yS3_` |
| 42         | 3     | `...arc` |
| 50         | 5     | `...M0n` |
| 59         | 6     | `...ot0n` |
| 67         | 1     | `...1c}` |

---

## Files
- `prob.sage`: Challenge source code
- `solve.sage`: Main solver implementing inverse spiral and recovery logic
- `check_inverse.sage`: Verification script for inverse function
- `sweep.sage`: Helper script for scanning digit combinations
