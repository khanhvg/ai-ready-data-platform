#!/usr/bin/env python3
import os, signal, time
if os.fork() == 0:
    os.setsid()
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    if os.fork() == 0:
        time.sleep(300)
    os._exit(0)
os.wait()
