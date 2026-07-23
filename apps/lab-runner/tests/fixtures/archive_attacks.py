#!/usr/bin/env python3
import argparse, io, tarfile
p=argparse.ArgumentParser(); p.add_argument("kind",choices=("traversal","symlink","hardlink","fifo","oversize")); p.add_argument("output"); a=p.parse_args()
with tarfile.open(a.output,"w") as tf:
    info=tarfile.TarInfo("../escape" if a.kind=="traversal" else "workspace/attack")
    if a.kind=="symlink": info.type=tarfile.SYMTYPE; info.linkname="/etc/passwd"
    elif a.kind=="hardlink": info.type=tarfile.LNKTYPE; info.linkname="workspace/other"
    elif a.kind=="fifo": info.type=tarfile.FIFOTYPE
    else:
        data=b"x"*(1024 if a.kind!="oversize" else 129*1024*1024); info.size=len(data); tf.addfile(info,io.BytesIO(data)); raise SystemExit
    tf.addfile(info)
