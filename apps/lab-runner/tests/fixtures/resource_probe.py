#!/usr/bin/env python3
import argparse, os, time
p=argparse.ArgumentParser(); p.add_argument("kind",choices=("memory","cpu","files","fds")); a=p.parse_args()
if a.kind=="memory":
    blocks=[bytearray(8*1024*1024) for _ in range(32)]
    cgroup=__import__("pathlib").Path("/sys/fs/cgroup")
    RESULT={"allocatedBytes":len(blocks)*8*1024*1024,"memoryMax":(cgroup/"memory.max").read_text().strip(),"memorySwapMax":(cgroup/"memory.swap.max").read_text().strip(),"memoryPeak":int((cgroup/"memory.peak").read_text().strip()),"memoryCurrent":int((cgroup/"memory.current").read_text().strip()),"memoryEvents":(cgroup/"memory.events").read_text().strip().splitlines()}
elif a.kind=="cpu":
    while True: pass
elif a.kind=="files":
    for i in range(5000): open(f"/workspace/state/f-{i}","wb").close()
else:
    fds=[]
    while True: fds.append(os.open("/dev/null",os.O_RDONLY))
