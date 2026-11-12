#!/usr/bin/env python3
"""MAP  The blind name test (Blessed, Walliams' face job, 12 Nov). likeness.py measures shapes; this asks the question
Sam asks: "who is that?". Walliams passed likeness.py (64-67%, first in the line-up) and Sam still could not tell who
he was; Brand passed both. So a famous head also goes to a FRESH helper who is told nothing: it sees the drawing big,
at phone size and in the film's frame, and must name the person, then pick from a line-up of look-alikes.

    python3 source/nametest.py pack OUT_DIR BIG.png [FRAME.jpg] --lineup "A,B,C,..."   build the pack + the prompt
    python3 source/nametest.py score OUT_DIR TRUE_NAME                                    read the helper's answer

Pass: named unprompted in its top 3, AND picked first from the line-up. Calibrate on a head Sam already recognises
(Brand passed, 12 Nov) before trusting a fail. The helper is started with prompt.txt (`pack` prints it; an Agent with only Read
and Write); after it answers, it is sent lineup.txt (SendMessage; it sits in OUT_DIR-key, out of the helper's folder) for step 2, so the list cannot steer step 1. It
must never see file names, notes or the film's text.

Map: pack 30 | score 75
"""
import json
import os
import random
import sys

from PIL import Image, ImageDraw


def _tile(im, h):
    k = h / im.height
    return im.resize((max(1, int(im.width * k)), h), Image.LANCZOS)


def pack(out, big, frame=None, lineup=()):
    os.makedirs(out, exist_ok=True)
    head = Image.open(big).convert('RGB')
    small = _tile(head, 150)                              # about how big a 240 px head reads on a phone held normally
    sheet = Image.new('RGB', (head.width + small.width + 60, head.height), (255, 255, 255))
    sheet.paste(head, (0, 0))
    sheet.paste(small, (head.width + 30, head.height - small.height - 20))
    sheet.save(os.path.join(out, 'a.jpg'), quality=90)
    files = ['a.jpg']
    if frame:
        Image.open(frame).convert('RGB').save(os.path.join(out, 'b.jpg'), quality=90)
        files.append('b.jpg')
    names = list(lineup)
    random.Random(len(names)).shuffle(names)
    key = out.rstrip('/') + '-key'                         # kept out of the helper's folder
    os.makedirs(key, exist_ok=True)
    json.dump(dict(lineup=names), open(os.path.join(key, 'pack.json'), 'w'))
    paths = ', '.join(os.path.abspath(os.path.join(out, f)) for f in files)
    ans = os.path.abspath(os.path.join(out, 'answer.json'))
    prompt = f"""You are a fresh pair of eyes for a cartoon studio. Look at these pictures and nothing else: {paths}.
Each shows a flat cartoon caricature of one real, famous person (the small copy is about phone size; b.jpg, if there,
is a frame from the film). Who is it? Give your top 3 guesses (real people), each with a confidence 0-100, and the 3
visual cues behind your first guess. If it looks like nobody in particular, say so with low confidence. Write JSON to
{ans}: {{"guesses": [["name", conf], ...], "cues": ["...", ...]}}, then reply with the same JSON only."""
    step2 = f"""Step 2: keep your step-1 guesses as they are. Now rank this line-up, best match first: {', '.join(names)}.
Rewrite {ans} adding "ranking": [all names in order] and "what_would_make_it_obvious": "one sentence". Reply with the
JSON only."""
    open(os.path.join(key, 'lineup.txt'), 'w').write(step2)
    open(os.path.join(out, 'prompt.txt'), 'w').write(prompt)
    return prompt


def score(out, true_name):
    a = json.load(open(os.path.join(out, 'answer.json')))
    low = true_name.lower().split()[-1]
    named = [i for i, (n, c) in enumerate(a['guesses'][:3]) if low in n.lower()]
    first = bool(a['ranking']) and low in a['ranking'][0].lower()
    conf = a['guesses'][named[0]][1] if named else 0
    ok = bool(named) and first
    print(f"named unprompted: {'#%d at %s%%' % (named[0] + 1, conf) if named else 'no'}  "
          f"(guesses: {', '.join('%s %s' % tuple(g) for g in a['guesses'][:3])})")
    print(f"line-up: {'first' if first else 'NOT first: ' + ', '.join(a['ranking'][:3])}")
    print(f"cues: {'; '.join(a.get('cues', []))}")
    print(f"would make it obvious: {a.get('what_would_make_it_obvious', '')}")
    print('PASS' if ok else 'FAIL')
    return ok


if __name__ == '__main__':
    if sys.argv[1] == 'pack':
        lu = sys.argv[sys.argv.index('--lineup') + 1].split(',') if '--lineup' in sys.argv else []
        rest = [x for x in sys.argv[3:] if not x.startswith('--') and x not in (','.join(lu),)]
        print(pack(sys.argv[2], rest[0], rest[1] if len(rest) > 1 else None, lu))
    elif sys.argv[1] == 'score':
        score(sys.argv[2], sys.argv[3])
