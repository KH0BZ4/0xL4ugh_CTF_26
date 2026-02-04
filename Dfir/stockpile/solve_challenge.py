import socket
import sys
import time

def solve():
    host = "challenges4.ctf.sd"
    port = 33225

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            print("Connected!")
            break
        except ConnectionRefusedError:
            print("Connection refused, retrying in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

    def read_until(match):
        buffer = ""
        while match not in buffer:
            chunk = s.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk
            print(chunk, end="")
        return buffer

    # Q1
    read_until("Please enter your answer:")
    s.sendall(b"app.finance.com\n")

    # Q2
    read_until("Please enter your answer:")
    s.sendall(b"2025-02-07 04:37:06 UTC\n")

    # Q3
    read_until("Please enter your answer:")
    s.sendall(b"2025-02-07 04:41:24 UTC\n")

    # Q4
    read_until("Please enter your answer:")
    s.sendall(b"314AA91A2AD7770F67BF43897996A54042E35B6373AE5D6FEB81E03A077255A7\n")

    # Q5
    read_until("Please enter your answer:")
    s.sendall(b"3.121.219.28:8888\n")

    # Q6
    read_until("Please enter your answer:")
    s.sendall(b"whoami\n")

    # Q7
    read_until("Please enter your answer:")
    s.sendall(b"Software\Microsoft\Windows\CurrentVersion\Run\n")

    # Q8
    read_until("Please enter your answer:")
    s.sendall(r"C:\Windows\Temp\monitorStock.exe".encode() + b"\n")

    # Q9 - Time of copy to C:\Windows\Temp
    read_until("Please enter your answer:")
    s.sendall(b"2025-02-07 04:43:51 UTC\n")
    
    # Q10 - Persistence Key Time
    read_until("Please enter your answer:")
    s.sendall(b"2025-02-07 04:45:03 UTC\n")

    # Q11 - Framework
    read_until("Please enter your answer:")
    
    frameworks = [
        "Empire", "PowerShell Empire", "Cobalt Strike", "CobaltStrike", 
        "Metasploit", "Meterpreter", "Covenant", "Sliver", "Havoc", 
        "Brute Ratel", "PoshC2", "Mythic", "Merlin"
    ]
    
    for fw in frameworks:
        print(f"Trying Q11: {fw}")
        s.sendall(f"{fw}\n".encode())
        response = read_until("Please enter your answer:")
        if "That's right!" in response or "Correct!" in response or "Congratulations" in response:
            print(f"Q11 Correct! Answer: {fw}")
            print(response)
            break
        print("Q11 Failed, retrying...")

    s.close()

if __name__ == "__main__":
    solve()
