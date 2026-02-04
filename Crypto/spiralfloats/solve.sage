
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import RealField, sqrt
import string

R = RealField(1024)
phi = R((1 + sqrt(5)) / 2)

masked_str = "?7086013?3756162?51694057?5285516?54803756?9202316?39221780?4895755?50591029"
current_chars = list(masked_str)
current_chars[0] = '6' 
filled_chars = [c if c != '?' else '0' for c in current_chars]

def inverse_spiral(y_final, phi, iterations=81):
    def step(y_val, idx):
        N = R(iterations)
        i = R(idx)
        r = i / N
        C = y_val - (1-r)*phi
        if idx == 0: return y_val - phi
        A = r**2 - (1-r)**2
        B = 2 * C * (1-r)
        D = r**2 - C**2
        if abs(A) < 1e-20: return -D/B
        delta = B**2 - 4*A*D
        if delta < 0: return R(0) 
        sqrt_delta = sqrt(delta)
        sol1 = (-B + sqrt_delta) / (2*A)
        sol2 = (-B - sqrt_delta) / (2*A)
        def check(x_cand):
            val = r * sqrt(x_cand**2 + 1) + (1 - r) * (x_cand + phi)
            return abs(val - y_val) < 1e-5
        if check(sol1): return sol1
        if check(sol2): return sol2
        return max(sol1, sol2)

    x = y_final
    for i in reversed(range(iterations)):
        x = step(x, i)
    return x

N_best = 30
dummy = b'0xL4ugh{' + b'\x00' * (N_best - 8)
flen_est = len(str(bytes_to_long(dummy)))

def check_bytes(x_val):
    s = str(x_val)
    if s.startswith("0."): s = s[2:]
    val = int(s[:flen_est])
    try:
        b = long_to_bytes(val)
        return b
    except:
        return b''

best_chars = list(filled_chars)
best_chars[8] = '5'
best_chars[16] = '5'
best_chars[25] = '9' 
best_chars[33] = '3' 
best_chars[42] = '3' 
best_chars[50] = '5'
best_chars[59] = '6'

# Inspect Hole 67
print("\nHole 67 Candidates (assuming d50=5, d59=6):")
for d in range(10):
    test_chars = list(best_chars)
    test_chars[67] = str(d)
    y = R("".join(test_chars)[:2] + "." + "".join(test_chars)[2:])
    x = inverse_spiral(y, phi)
    b = check_bytes(x)
    print(f"d={d}: {b}")
