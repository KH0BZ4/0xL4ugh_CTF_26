# Bitcoin - Crypto

- CTF: 0xL4ugh CTF 2025
- Category: Crypto
- Points: 500
- Solver: W4ST3D
- Flag: `0xL4ugh{B1tc0in_Squiggl3_d3m0_By_Zwique_7cdc0aaa1a738665}`

---

## Challenge
> A "Curve Oracle Service" holds a secret private key $d$. The service has two phases:
> 1. **Phase 1 (Oracle):** Accepts two points $C_1$ and $C_2$, computes $S = C_2 - d \cdot C_1$
> 2. **Phase 2 (Decryption):** Provides ElGamal ciphertexts to decrypt using the recovered key

---

## Overview
This is an **Invalid Curve Attack** on elliptic curve cryptography. The server performs point operations using a secret key but fails to validate that input points lie on the intended secp256k1 curve, allowing us to use a weaker singular curve to recover the private key.

---

## Root Cause
The oracle performs elliptic curve point subtraction using the private key $d$ but **fails to validate** that input points $C_1$ and $C_2$ lie on the standard secp256k1 curve ($y^2 = x^3 + 7$). This allows supplying points from a **Singular Curve** ($y^2 \equiv x^3 \pmod p$) where the discrete log problem is trivial.

---

## Exploitation Steps

### 1. Invalid Curve Attack Theory
On the singular curve $y^2 \equiv x^3 \pmod p$, there exists an isomorphism:
$$\phi(x, y) \equiv x \cdot y^{-1} \pmod p$$

Scalar multiplication becomes simple field multiplication:
$$\phi(d \cdot P) \equiv d \cdot \phi(P) \pmod p$$

### 2. Recover Private Key $d$
1. Choose point $P(1, 1)$ satisfying $1^2 = 1^3$
2. Send $C_1 = P(1, 1)$ and $C_2 = P(1, 1)$ to the oracle
3. Oracle computes $S = C_2 - d \cdot C_1$
4. Map points to integers: $s_{map} = \frac{x_S}{y_S}$
5. Solve linear equation in $\mathbb{F}_p$:
   $$d \equiv (c_{2,map} - s_{map}) \cdot (c_{1,map})^{-1} \pmod p$$

### 3. Decrypt Challenge Ciphertexts
With $d$ recovered:
1. Receive ciphertext $(C_1, C_2)$
2. Compute shared secret $S = d \cdot C_1$
3. Recover plaintext $P = C_2 - S$

### 4. Run the Solver
```bash
pip install pwntools ecdsa sympy gmpy2
python3 solve.py <PORT>
```

---

## Files
- `solve.py`: Main exploit script
- `find_params.py`: Helper to find valid singular curve points
- `verify_p.py`: Verification script
