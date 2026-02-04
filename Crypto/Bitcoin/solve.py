import sys
sys.stdout.reconfigure(line_buffering=True)
print("Starting script...")
import socket
import time
import re
from ecdsa import SECP256k1
import gmpy2
from sympy import sqrt_mod

print("Imports done.")

# Bitcoin curve order (secp256k1)
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663

HOST = 'challenges2.ctf.sd'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 33934

def solve():
    print(f"Connecting to {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[+] Connected to {HOST}:{PORT}")
        intro = s.recv(1024).decode()
        print(f"Intro: {intro}")

        # --- Query 1: Recover d ---
        # Attack using Singular Curve (b=0)
        x, y = 1, 1
        c1_str = f"Point({x}, {y})"
        c2_str = f"Point({x}, {y})" 
        
        print(f"[>] Sending Query 1 C1: {c1_str}")
        s.sendall(c1_str.encode() + b"\n")
        time.sleep(0.5)
        s.recv(1024) # Prompt
        
        print(f"[>] Sending Query 1 C2: {c2_str}")
        s.sendall(c2_str.encode() + b"\n")
        
        response = s.recv(4096).decode()
        # print(f"[<] Response 1: {response}")
        
        matches = re.findall(r"Point\((-?\d+), (-?\d+)\)", response)
        if matches:
            sx = int(matches[0][0])
            sy = int(matches[0][1])
            
            c1_map = (x * pow(y, -1, P)) % P
            c2_map = (x * pow(y, -1, P)) % P
            s_map = (sx * pow(sy, -1, P)) % P
            
            # d = (C2_map - S_map) / C1_map
            num = (c2_map - s_map) % P
            den = c1_map
            d_recovered = (num * pow(den, -1, P)) % P
            print(f"[+] Recovered d: {d_recovered}")
            
            # --- Query 2: Verify d ---
            print("\n[+] Verifying d with Query 2...")
            # Use points on the same singular curve $y^2 = x^3$
            # Let's pick $P2 = (4, 8)$ (since $8^2 = 64, 4^3 = 64$).
            # Map(P2) = 4/8 = 1/2.
            x2, y2 = 4, 8
            c1_verify = f"Point({x2}, {y2})"
            c2_verify = f"Point({x2}, {y2})"
            
            # Predicted S_map
            # S_map_pred = C2_map_v - d * C1_map_v
            # C2_map_v = 1/2
            # C1_map_v = 1/2
            # S_map_pred = 0.5 - d * 0.5 = 0.5 * (1 - d)
            
            val_half = (1 * pow(2, -1, P)) % P
            s_map_expected = (val_half * (1 - d_recovered)) % P
            
            # Expected coordinate: T = S_map_expected. X = T^-2, Y = T^-3.
            # But wait, T = x/y. x = y*T. y^2 = x^3 => y^2 = (yT)^3 => y^2 = y^3 T^3 => 1 = y T^3 => y = T^-3.
            # x = T^-3 * T = T^-2.
            # So coordinates are (T^-2, T^-3).
            
            s_x_expected = pow(s_map_expected, -2, P)
            s_y_expected = pow(s_map_expected, -3, P)
            
            print(f"[+] Expecting S = ({s_x_expected}, {s_y_expected}) (if s_map != 0)")

            s.sendall(c1_verify.encode() + b"\n")
            time.sleep(0.5)
            s.recv(1024)
            s.sendall(c2_verify.encode() + b"\n")
            
            response2 = s.recv(4096).decode()
            print(f"[<] Response 2: {response2}")
            
            matches2 = re.findall(r"Point\((-?\d+), (-?\d+)\)", response2)
            if matches2:
                sx2 = int(matches2[0][0])
                sy2 = int(matches2[0][1])
                print(f"[+] Got S2 = ({sx2}, {sy2})")
                
                if sx2 == s_x_expected and sy2 == s_y_expected:
                    print("[+] VERIFIED: The recovered d is correct!")
                    
                    # Compute Q = d * G
                    # We need standard curve parameters for this
                    G = SECP256k1.generator
                    d_int = int(d_recovered)
                    Q_point = d_int * G
                    Q_x = Q_point.x()
                    Q_y = Q_point.y()
                    
                    print(f"\n[+] Calculated Public Key Q = d * G")
                    print(f"Q.x = {Q_x}")
                    print(f"Q.y = {Q_y}")
                    print(f"Q.x (hex) = {hex(Q_x)}")
                    
                    # Try to consume remaining queries to see if there is a Phase 2
                    for i in range(3, 6):
                        print(f"Sending dummy query {i}...")
                        s.sendall(c1_verify.encode() + b"\n")
                        s.recv(1024)
                        s.sendall(c2_verify.encode() + b"\n")
                        s.recv(4096)
                    
                    # Read Phase 2 Header
                    header = s.recv(4096).decode()
                    print(f"Phase 2 Header: {header}")
                    
                    # There are 5 rounds in Phase 2
                    from ecdsa.ellipticcurve import Point
                    curve = SECP256k1.curve
                    
                    for r in range(1, 6):
                        print(f"--- Round {r} ---")
                        # Read ciphertext
                        # Format: "C1 = Point(x, y)", "C2 = Point(x, y)" ???
                        # We need to see the exact format.
                        # Assuming it might send line by line or in one block.
                        
                        buffer = ""
                        while "Input P" not in buffer and "C2" not in buffer:
                            chunk = s.recv(4096).decode()
                            if not chunk: break
                            buffer += chunk
                            # print(f"DEBUG CHUNK: {chunk}")
                        
                        print(f"Challenge Data: {buffer}")
                        
                        # Parse C1 and C2
                        # Likely format:
                        # C1 > Point(x, y)
                        # C2 > Point(x, y) or similar
                        
                        # Use regex to find all points
                        pts = re.findall(r"Point\((-?\d+), (-?\d+)\)", buffer)
                        if len(pts) >= 2:
                            c1_x, c1_y = int(pts[-2][0]), int(pts[-2][1])
                            c2_x, c2_y = int(pts[-1][0]), int(pts[-1][1])
                            
                            # Create Point objects
                            C1 = Point(curve, c1_x, c1_y)
                            C2 = Point(curve, c2_x, c2_y)
                            
                            # Decrypt: P = C2 - d*C1
                            # P = C2 + (-d * C1)
                            
                            d_int = int(d_recovered)
                            
                            # Compute S = d * C1
                            S = d_int * C1
                            
                            # Negate S
                            # Point negation: (x, -y mod p)
                            S_neg = Point(curve, S.x(), -S.y() % P)
                            
                            # P = C2 + S_neg
                            DecryptedP = C2 + S_neg
                            
                            ans = f"Point({DecryptedP.x()}, {DecryptedP.y()})"
                            print(f"[>] Sending P: {ans}")
                            s.sendall(ans.encode() + b"\n")
                            
                            # Result
                            res = s.recv(4096).decode()
                            print(f"[<] Round Result: {res}")
                            if "flag" in res.lower():
                                break
                        else:
                            print("[-] Could not parse C1, C2 in Phase 2")
                            break
                        
                else:
                    print("[-] VERIFICATION FAILED: d is incorrect or server behavior differs.")
                    
            print(f"\n[+] RECOVERED D (hex): {hex(d_recovered)[2:]}")
            
        else:
            print("[-] No point found in response")

    except Exception as e:
        print(f"[-] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        s.close()

if __name__ == "__main__":
    solve()

