"""The blind judge's outline sheet for ANY film's cast (Patriots 5 chat 6; generalised from
notes/learn/kemi-build/judge.py so every film gets it): each person headless, black, front / 3/4 / back / seated 3/4,
shuffled, numbered, about 300 px tall (phone size). The key goes to notes/judge/FILM-key.json; the judges' answers
go to notes/judge/FILM-cast.json (castsheet.judge_faults reads it).

    python3 source/castjudge.py FILM OUT.jpg [who ...]
    python3 source/castjudge.py record FILM SHEET ANSWERS.json     (ANSWERS: {"A": [{"n","said","conf","why"}], ...})
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
VIEWS = ((0, False, 'front'), (45, False, 'three-quarter'), (180, False, 'back'), (45, True, 'seated 3/4'))


def sheet(film, out, who=None):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import castsheet as CS
    import sitting as S
    cast, PP = CS._setup(film, None)
    B, V = PP.B, PP.V
    who = who or [w for w, sp in cast.items() if sp.get('sex') in ('man', 'woman')]
    tiles = []
    for w in who:
        for yaw, seated, name in VIEWS:
            sp = dict(cast[w]); sp['hair_style'] = 'back'
            if 'kit_house' in sp:
                sp['kit_house'] = dict(sp['kit_house'], hair='bald')
            for k in ('hat', 'hat_c', 'specs'):
                sp.pop(k, None)
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            s = 0.5 * sp['height'] / 1.75
            cam = B.Cam(2.0, 540, 470)
            j = S.pose(sp, 'upright') if seated else None
            y0 = 840 - 928 * s
            V.person(tile, cam, 540, y0, s, dict(sp), 0.0, yaw, j)
            a = np.asarray(tile.convert('RGB')).copy()
            neck = int((y0 - 470) * 2.0 + 960 + ((j.get('bob', 0) if j else 0) * s * 2)) + 6
            m = np.abs(a.astype(int) - 255).sum(2) > 30
            m[:max(0, neck)] = False
            ys, xs = np.nonzero(m)
            o = Image.fromarray(np.where(m[..., None], 20, 255).astype(np.uint8).repeat(3, 2)).crop(
                (xs.min() - 10, ys.min() - 10, xs.max() + 10, ys.max() + 10))
            k = 300 / o.height
            tiles.append(((w, name), o.resize((int(o.width * k), 300), Image.LANCZOS)))
    random.Random(624).shuffle(tiles)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    per = 6
    rows = [tiles[i:i + per] for i in range(0, len(tiles), per)]
    W = max(sum(t.width + 30 for _, t in r) for r in rows) + 30
    page = Image.new('RGB', (W, len(rows) * 360 + 20), 'white'); d = ImageDraw.Draw(page)
    n = 0
    for ri, r in enumerate(rows):
        x, y = 30, 40 + ri * 360
        for key, t in r:
            n += 1
            page.paste(t, (x, y)); d.text((x, y - 32), str(n), fill='black', font=f); x += t.width + 30
    page.save(out, quality=90)
    os.makedirs(os.path.join(ROOT, 'notes', 'judge'), exist_ok=True)
    json.dump({str(i + 1): list(k) for i, (k, _) in enumerate(tiles)},
              open(os.path.join(ROOT, 'notes', 'judge', f'{film}-key.json'), 'w'))
    return out


def record(film, sheet_path, answers):
    """Middle verdict of the judges per figure (by confidence signed by sex: man +, woman -), as castsheet reads."""
    key = json.load(open(os.path.join(ROOT, 'notes', 'judge', f'{film}-key.json')))
    judges = json.load(open(answers))
    verdicts = []
    for n, (who, view) in key.items():
        said = []
        for jl in judges.values():
            for a in jl:
                if str(a['n']) == n:
                    said.append(a)
        sc = sorted(said, key=lambda a: a['conf'] * (1 if a['said'] == 'man' else -1))
        mid = sc[len(sc) // 2]
        verdicts.append(dict(who=who, view=view, said=mid['said'], conf=mid['conf'], why=mid['why'],
                             of=[f"{a['said']} {a['conf']}" for a in said]))
    rec = dict(sheet=os.path.relpath(sheet_path, ROOT), made_by='source/castjudge.py', judges=judges,
               judge=f'{len(judges)} fresh helpers, none told the cast; each verdict the middle',
               verdicts=verdicts)
    json.dump(rec, open(os.path.join(ROOT, 'notes', 'judge', f'{film}-cast.json'), 'w'), indent=1)
    return verdicts


if __name__ == '__main__':
    if sys.argv[1] == 'record':
        for v in record(sys.argv[2], sys.argv[3], sys.argv[4]):
            print(v['who'], v['view'], v['said'], v['conf'], v['of'])
    else:
        print(sheet(sys.argv[1], sys.argv[2], sys.argv[3:] or None))
