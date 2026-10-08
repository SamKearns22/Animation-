#!/usr/bin/env python3
"""A map of a big film file: every top-level def and class with its line number and first docstring line, so a note
can be answered by reading the right 40 lines instead of searching 3,000. Usage: python3 codemap.py FILE.py > map.md"""
import ast
import sys

src = open(sys.argv[1]).read()
tree = ast.parse(src)
print(f'# Code map: {sys.argv[1]} ({len(src.splitlines())} lines). Regenerate: python3 source/codemap.py {sys.argv[1]}\n')
for n in tree.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        doc = (ast.get_docstring(n) or '').strip().split('\n')[0][:110]
        print(f'- {n.lineno}: `{"class " if isinstance(n, ast.ClassDef) else ""}{n.name}` {doc}')
    elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id.isupper():
        print(f'- {n.lineno}: {n.targets[0].id} (data)')
