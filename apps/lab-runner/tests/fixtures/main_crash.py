#!/usr/bin/env python3
import os, signal, time
if os.fork() == 0:
    time.sleep(300)
os.kill(os.getpid(), signal.SIGKILL)
