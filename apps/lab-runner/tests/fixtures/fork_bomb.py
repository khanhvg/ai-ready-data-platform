#!/usr/bin/env python3
import os, pathlib, time
if os.environ.get("RUNNER_ADVERSARIAL_CONTAINER") != "1" or not pathlib.Path("/.dockerenv").exists():
    raise SystemExit("FORK_BOMB_REFUSED_OUTSIDE_OPERATION_CONTAINER")
children=[]
while True:
    try:
        pid=os.fork()
        if pid == 0:
            time.sleep(300)
            os._exit(0)
        children.append(pid)
    except OSError as exc:
        print(f"bounded:{len(children)}:{exc.errno}", flush=True)
        break
time.sleep(300)
