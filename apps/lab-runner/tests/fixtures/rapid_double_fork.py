#!/usr/bin/env python3
import os, time
if os.fork() == 0:
    if os.fork() == 0:
        time.sleep(300)
    os._exit(0)
os.wait()
