"""Step 1 tally: reads out1..6.txt (one line per note: ID | KIND | CAT | PREVENT | CAUSE | why) and items.json."""
import json, collections, glob, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(here, 'items.json')))
def read(paths):
    r = {}
    for p in paths:
        for ln in open(p):
            f = [x.strip() for x in ln.split('|')]
            if len(f) >= 5 and f[0].isdigit():
                r[int(f[0])] = f
    return r
main = read(sorted(glob.glob(os.path.join(here, 'out[1-6].txt'))))
print('sorted', len(main), 'of', len(items), 'missing', len(items) - len(main))
notes = {i: f for i, f in main.items() if f[1] == 'N'}
cat = collections.Counter(f[2] for f in notes.values())
print('Sam notes', len(notes)); print('by subject', dict(cat.most_common()))
body = {i: f for i, f in notes.items() if f[2] in ('BODY', 'CONTACT', 'HANDS')}
pv = collections.Counter(f[3] for f in body.values())
print('body/pose/contact/hands notes', len(body), dict(pv))
for c in ('BODY', 'CONTACT', 'HANDS'):
    print(' ', c, dict(collections.Counter(f[3] for f in body.values() if f[2] == c)))
y = pv['Y']; p = pv['P']; n = len(body)
print(f'prevented Y {y}/{n} = {100*y/n:.0f}%;  Y+P {y+p}/{n} = {100*(y+p)/n:.0f}%')
print('all notes: Y', sum(1 for f in notes.values() if f[3]=='Y'), 'P', sum(1 for f in notes.values() if f[3]=='P'))
print('may cause (R)', sum(1 for f in notes.values() if f[4] == 'R'), dict(collections.Counter(f[2] for f in notes.values() if f[4]=='R')))
film = collections.defaultdict(lambda: [0, 0, 0, 0])
for i, f in notes.items():
    fm = items[i-1][0]; film[fm][0] += 1
    if f[2] in ('BODY', 'CONTACT', 'HANDS'):
        film[fm][1] += 1; film[fm][2] += f[3] == 'Y'; film[fm][3] += f[3] == 'P'
print('film: notes, body-ish, Y, P')
for fm, v in sorted(film.items(), key=lambda x: -x[1][1]): print(' ', fm, v)
if os.path.exists(os.path.join(here, 'out_sample.txt')):
    s = read([os.path.join(here, 'out_sample.txt')])
    both = [i for i in s if i in main]
    agree = lambda k: sum(s[i][k] == main[i][k] for i in both)
    print(f'second sort agreement on {len(both)}: kind {agree(1)}, subject {agree(2)}, prevent {agree(3)}')
    bb = [i for i in both if main[i][1]=='N' and main[i][2] in ('BODY','CONTACT','HANDS')]
    print('  on body-ish notes', len(bb), 'prevent agree', sum(s[i][3]==main[i][3] for i in bb),
          'second sort Y', sum(s[i][3]=='Y' for i in bb), 'first sort Y', sum(main[i][3]=='Y' for i in bb))
