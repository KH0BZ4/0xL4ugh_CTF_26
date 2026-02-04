from pwn import *

# Set up the connection
r = remote('challenges4.ctf.sd', 33047)

# Receive any initial data
try:
    print(r.recv(timeout=2).decode())
except:
    print("No initial data")

# Interactive mode to test manually first
r.interactive()
