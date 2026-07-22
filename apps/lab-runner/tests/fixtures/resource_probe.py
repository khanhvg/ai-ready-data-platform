#!/usr/bin/env python3
import argparse, os, resource, time
p=argparse.ArgumentParser(); p.add_argument("kind",choices=("memory","cpu","files","fds")); a=p.parse_args()
if a.kind=="memory":
    blocks=[]
    while True: blocks.append(bytearray(8*1024*1024))
elif a.kind=="cpu":
    while True: pass
elif a.kind=="files":
    for i in range(5000): open(f"/workspace/state/f-{i}","wb").close()
else:
    fds=[]
    while True: fds.append(os.open("/dev/null",os.O_RDONLY))
