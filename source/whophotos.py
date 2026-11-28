#!/usr/bin/env python3
"""MAP  whophotos: a real person's photos must be OF that person (Patriot 5, 28 Nov). Sam: "You appear to have built
Tommy Robinson, not Danny Tommo. Different people." The plan chat searched a news site for "Tommo", got photos of
Tommy Robinson, and filed them as Danny Tommo's; nothing asked whose face each photo shows, so the face tool, the cast
sheet and the critique all measured the wrong man, and only Sam saw it.

The rule: every photo in references/faces/NAME/ has a line in that folder's who.txt giving the caption it was
published with, and the caption names the person by one of the names on who.txt's first line (a whole phrase,
e.g. "Danny Tommo" or "Daniel Thomas"; "Tommy Robinson" does not name Danny Tommo). facepick refuses a new person
whose folder fails (faults()).

  who.txt:   name: Danny Tommo / Daniel Thomas
             01-front-bbc.jpg: "Daniel Thomas, known as Danny Tommo, on September 09, 2026, in London" (BBC News)
  faults(folder) -> list of plain faults (empty: every photo is captioned with the person's name)

    python3 source/whophotos.py FOLDER
"""
import os
import re
import sys

PHOTO = re.compile(r'\.(jpe?g|png|webp)$', re.I)


def faults(folder):
    p = os.path.join(folder, 'who.txt')
    photos = sorted(f for f in os.listdir(folder) if PHOTO.search(f))
    if not os.path.exists(p):
        return [f'{folder}: no who.txt, so nothing says whose face these {len(photos)} photos show']
    lines = [ln.strip() for ln in open(p, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    if not lines or not lines[0].lower().startswith('name:'):
        return [f'{p}: the first line must be "name: FULL NAME / OTHER NAME"']
    names = [n.strip().lower() for n in lines[0].split(':', 1)[1].split('/') if n.strip()]
    caps = {}
    for ln in lines[1:]:
        if ':' in ln:
            f, c = ln.split(':', 1)
            caps[f.strip()] = c.strip()
    out = []
    for f in photos:
        c = caps.get(f)
        if c is None:
            out.append(f'{f}: no caption in who.txt (whose face is it?)')
        elif not any(re.search(r'\b' + re.escape(n) + r'\b', c.lower()) for n in names):
            out.append(f'{f}: its caption does not name {" / ".join(names)}: {c[:90]}')
    return out


if __name__ == '__main__':
    fs = faults(sys.argv[1])
    print('\n'.join(fs) or 'whophotos: every photo is captioned with the person\'s name')
    sys.exit(1 if fs else 0)
