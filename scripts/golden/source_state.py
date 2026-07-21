#!/usr/bin/env python3
"""Bind evidence to an unchanged clean tracked source commit."""
from __future__ import annotations
import pathlib, subprocess

ROOT=pathlib.Path(__file__).resolve().parents[2]
class SourceStateError(RuntimeError): pass
def identity(allowed_changes:tuple[str,...]=())->tuple[str,str]:
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    tree=subprocess.check_output(["git","rev-parse","HEAD^{tree}"],cwd=ROOT,text=True).strip()
    status=subprocess.check_output(["git","status","--porcelain=v1","-z","--untracked-files=all"],cwd=ROOT).split(b"\0")
    unexpected=[]
    for entry in status:
        if not entry: continue
        text=entry.decode("utf-8","surrogateescape"); path=text[3:]
        if (text.startswith("?? ") and path.startswith(".artifacts/")) or path in allowed_changes: continue
        unexpected.append(text)
    if unexpected: raise SourceStateError("SOURCE_TREE_NOT_CLEAN:"+unexpected[0])
    if not allowed_changes and (subprocess.run(["git","diff","--quiet","HEAD","--"],cwd=ROOT).returncode or subprocess.run(["git","diff","--cached","--quiet","HEAD","--"],cwd=ROOT).returncode): raise SourceStateError("SOURCE_TREE_NOT_CLEAN")
    return head,tree
def assert_unchanged(expected:tuple[str,str],allowed_changes:tuple[str,...]=())->None:
    if identity(allowed_changes)!=expected: raise SourceStateError("SOURCE_TREE_CHANGED_DURING_RUN")
