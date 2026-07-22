#!/usr/bin/env python3
import json, os, pathlib
print(json.dumps({"pid": os.getpid(), "ppid": os.getppid(), "session": os.getsid(0), "cgroup": pathlib.Path("/proc/self/cgroup").read_text()}))
