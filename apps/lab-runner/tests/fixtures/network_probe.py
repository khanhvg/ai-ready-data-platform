#!/usr/bin/env python3
import json, socket
results={}
for family,kind,target in [
    (socket.AF_INET,socket.SOCK_STREAM,("169.254.169.254",80)),
    (socket.AF_INET,socket.SOCK_DGRAM,("1.1.1.1",53)),
]:
    try:
        sock=socket.socket(family,kind); sock.settimeout(.5); sock.connect(target); results[str(target)]=True
    except OSError:
        results[str(target)]=False
try:
    socket.getaddrinfo("example.com",443); results["dns"]=True
except OSError:
    results["dns"]=False
print(json.dumps(results,sort_keys=True))
