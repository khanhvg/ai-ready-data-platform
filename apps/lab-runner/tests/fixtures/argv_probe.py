#!/usr/bin/env python3
import json, os, sys
print(json.dumps({"argv": sys.argv, "envNames": sorted(os.environ)}))
