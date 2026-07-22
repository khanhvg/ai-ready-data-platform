#!/usr/bin/env python3
import os, sys
stream=sys.stderr.buffer if os.environ.get("FLOOD_STDERR")=="1" else sys.stdout.buffer
chunk=b"x"*65536
while True:
    stream.write(chunk); stream.flush()
