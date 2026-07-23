#!/usr/bin/env python3
import json, site, sys
print(json.dumps({"executable": sys.executable, "prefix": sys.prefix, "userSite": site.ENABLE_USER_SITE}))
