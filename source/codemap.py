#!/usr/bin/env python3
"""A map of a big film file: every top-level def and class with its line number and first docstring line, so a note
can be answered by reading the right 40 lines instead of searching 3,000. Usage: python3 source/codemap.py FILE
(a path, or just the name: `whale`, `whale.py` and `source/whale.py` all work, from any folder)."""
import ast
import os
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)    # quiet when piped into head
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1]
if not os.path.exists(path):
    name = os.path.basename(path)
    path = os.path.join(HERE, name if name.endswith('.py') else name + '.py')
src = open(path).read()
tree = ast.parse(src)
rel = os.path.relpath(path, os.path.dirname(HERE))
print(f'# Code map: {rel} ({len(src.splitlines())} lines). Regenerate: python3 source/codemap.py {rel}\n')
for n in tree.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        doc = (ast.get_docstring(n) or '').strip().split('\n')[0][:110]
        print(f'- {n.lineno}: `{"class " if isinstance(n, ast.ClassDef) else ""}{n.name}` {doc}')
    elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id.isupper():
        print(f'- {n.lineno}: {n.targets[0].id} (data)')
