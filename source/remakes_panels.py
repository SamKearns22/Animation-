#!/usr/bin/env python3
"""Remakes critique panels: one clean sheet per character (no names, no references), for critique.py pack.

MAP
  sheet ...... tiles then faces, wrapped into rows
  main ....... the six people (remakes_cast), KG front and side, Navi, the Goron (remakes_creatures); panels.json

    python3 source/remakes_panels.py OUTDIR    (run from the repo root)
"""
import json, os, sys
sys.path.insert(0, 'source')
from PIL import Image
import burnham as B
import remakes_cast as RC
import remakes_creatures as CR
OUT = sys.argv[1]
REF = 'references/remakes'

def sheet(tiles, faces, th=900, fh=420, maxw=1900):
    ims = [t.convert('RGB').resize((max(1, int(t.width * th / t.height)), th)) for t in tiles]
    ims += [f.convert('RGB').resize((max(1, int(f.width * fh / f.height)), fh)) for f in faces]
    rows, row, w = [], [], 20
    for i in ims:                                   # wrap into rows at most maxw wide
        if row and (w + i.width + 20 > maxw or i.height != row[0].height):
            rows.append(row); row, w = [], 20
        row.append(i); w += i.width + 20
    rows.append(row)
    W = max(sum(i.width + 20 for i in r) + 20 for r in rows)
    H = sum(r[0].height + 20 for r in rows) + 20
    im = Image.new('RGB', (W, H), (250, 248, 244))
    y = 20
    for r in rows:
        x = 20
        for i in r:
            im.paste(i, (x, y)); x += i.width + 20
        y += r[0].height + 20
    return im

panels = []
B.SS = 1
for who in ('link', 'zelda', 'malon', 'saria', 'ruto', 'gunman'):
    tiles = [RC.figure_tile(who, y) for y in RC.VIEWS_NEEDED.get(who, (0,))]
    tiles += [RC.figure_tile(who, 0, j) for j in RC.poses(who).values()]
    faces = [RC.face_tile(who, m) for m in RC.FACES_NEEDED.get(who, ())]
    p = os.path.join(OUT, who + '.jpg'); sheet(tiles, faces).save(p, quality=90)
    panels.append((who, p, [os.path.join(REF, f) for f in RC.REFS[who] if 'kg' not in f]))
B.SS = 1
kt = CR.tiles('kg')
p = os.path.join(OUT, 'kg-front.jpg'); sheet([t for _, t in kt[:5]], [t for _, t in CR.faces('kg')], maxw=2700).save(p, quality=90)
panels.append(('kg-front', p, [os.path.join(REF, f) for f in CR.REFS['kg']]))
p = os.path.join(OUT, 'kg-side.jpg'); sheet([t for _, t in kt[5:]], [], maxw=2800).save(p, quality=90)
panels.append(('kg-side', p, [os.path.join(REF, f) for f in CR.REFS['kg']]))
for who in ('navi', 'goron'):
    p = os.path.join(OUT, who + '.jpg'); sheet([t for _, t in CR.tiles(who)], []).save(p, quality=90)
    panels.append((who, p, [os.path.join(REF, f) for f in CR.REFS[who]]))
for who, p, r in panels:
    print(who, Image.open(p).size)
json.dump(panels, open(os.path.join(OUT, 'panels.json'), 'w'))
