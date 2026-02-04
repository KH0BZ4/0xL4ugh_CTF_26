# SCA1 - Hardware

- CTF: 0xL4ugh CTF 2025
- Category: Hardware / Side Channel Analysis
- Solver: W4ST3D
- Flag: `0xL4ugh{DPA4BabyGogoGaga}`

---

## Challenge
> This challenge requires recovering the AES secret key given a set of power traces and their corresponding plaintexts.
>
> Instance: http://46.62.131.109:3923/sca1.npz

---

## Overview
A classic Side Channel Analysis challenge involving Correlation Power Analysis (CPA) on AES-128 encryption. We are given power traces captured during AES encryption operations and must recover the secret key by correlating power consumption with hypothetical intermediate values.

---

## Root Cause
The AES implementation leaks information through power consumption. The power drawn by the device correlates with the Hamming Weight of intermediate values during the S-Box substitution in the first round of AES.

---

## Exploitation Steps

### 1. Understand the Leakage Model
- **Target Operation**: Output of the AES S-Box substitution in the first round
- **Leakage Model**: Hamming Weight (HW) of the intermediate value
  - `Intermediate Value = SBox(Plaintext_Byte ^ Key_Byte)`

### 2. Implement CPA Attack
For each key byte (0-15) and each candidate value (0-255):
1. Compute hypothetical intermediate values for all traces
2. Calculate Hamming Weight of each intermediate value
3. Correlate with actual power traces using Pearson correlation
4. Select candidate with highest correlation

### 3. Run the Attack
```bash
# Download challenge data
mkdir -p solve
curl -o solve/sca1.npz http://46.62.131.109:3923/sca1.npz

# Run solver
python solve/solve_sca.py
```

### 4. Results
The attack successfully recovers the key using ~20,000 traces:
- **Recovered HEX**: `44 50 41 34 42 61 62 79 47 6f 67 6f 47 61 67 61`
- **Recovered ASCII**: `DPA4BabyGogoGaga`

---

## Files
- `solve/solve_sca.py`: Main Python script performing the CPA attack
- `solve/inspect_data.py`: Helper script to inspect the `.npz` data structure
- `solve/sca1.npz`: Challenge data file (traces and plaintexts)
