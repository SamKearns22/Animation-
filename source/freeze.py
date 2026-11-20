"""freeze: every finished film keeps a saved copy, and one command draws it again from that copy.

Why (one-route-kit, Change 1): finished films re-draw from the live, shared drawing code, so the code can never be
tidied without risking them. Each film gets a BOOKMARK (a git tag, `film/NAME`) at the save its posted video came
from; `recut` draws a picture from that saved copy in a separate folder; the shared code is never touched.

    python3 source/freeze.py list                         the films, their bookmark and save
    python3 source/freeze.py tag [--push]                 make (or move) the bookmarks from films.json; --push sends them
    python3 source/freeze.py recut NAME [--at T] [--out F.png] [--span T0 T1 --out F.mp4]   draw from the saved copy
    python3 source/freeze.py check [NAME ...] [--at F1,F2]   draw each film's frame(s) from its saved copy and compare with
                                                          the posted video (fractions of the film; default 0.4)
    python3 source/freeze.py count [--check] [--lower]    old-film files loaded, steps swapped: may never rise

The registry is source/data/freeze/films.json (film, module, videos, save, how to draw one frame). A film whose
working data folder is gitignored lists the steps that rebuild it under "regen" (and "fixups" for a tool that sits elsewhere
on this machine); `recut` runs them in the saved copy first.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REG = os.path.join(HERE, 'data', 'freeze', 'films.json')
BASE = os.path.join(HERE, 'data', 'freeze', 'count-baseline.json')
DATA = os.path.join(HERE, 'data', 'freeze', 'data')
SCRATCH = os.path.join(tempfile.gettempdir(), 'freeze')

# a file that belongs to one finished film (not the shared kit); gta_* is the film in progress, never counted
FILM = re.compile(r'^(ad_vanced_notice|bayeux|beaver_asteroid|blessed|burnham|channel_trailer|concept_mother|cryminister|'
                  r'daughter|mother|kitchen|shot$|s\d_|deck_the_halls|duel|ed$|ed_variants|elder_swindon|flying_whales|'
                  r'whale$|gta|halo|hutt|islamocommunism|maul|midterminal|milburn|mossad|netan|newsdesk|patriots|peepee|'
                  r'poker_mon|polanski|power_crime|prepper|press_secretary|professional|protest_tiers|rap|remakes|roadster|'
                  r'russiadent|salt|sam$|shocking|strictly|terfwarts|thepark|park$|traitors|trial_|walker$|wolf$|horror_|'
                  r'animation_test|satire_parts|series$|wolf)')


def sh(*a, cwd=ROOT, check=True):
    return subprocess.run(a, cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()


def load():
    return json.load(open(REG))


def tagname(name, video=None):
    return f'film/{name}' + (f'+{os.path.splitext(video)[0]}' if video else '')


def cmd_list():
    reg = load()
    for n, d in reg.items():
        extra = '' if len(set(d['saves'].values())) < 2 else '  (other saves: ' + ', '.join(
            f'{v}={s}' for v, s in d['saves'].items() if s != d['save']) + ')'
        print(f"{n:24} {d['save']}  {', '.join(d['videos'])}{extra}")
    print(len(reg), 'films')


def cmd_tag(push):
    reg = load()
    for n, d in reg.items():
        sh('git', 'tag', '-f', tagname(n), d['save'])
        for v, s in d['saves'].items():
            if s != d['save']:
                sh('git', 'tag', '-f', tagname(n, v), s)
    tags = sh('git', 'tag', '-l', 'film/*').split()
    print(len(tags), 'bookmarks made')
    if push:
        print(sh('git', 'push', '-f', 'origin', *[f'refs/tags/{t}' for t in tags], check=False) or 'pushed')


def worktree(name, tag=None):
    """The saved copy, in its own folder (never the live project)."""
    tag = tag or tagname(name)
    path = os.path.join(SCRATCH, tag.replace('/', '_').replace('+', '_'))
    if os.path.isdir(path):
        sh('git', 'worktree', 'remove', '--force', path, check=False)
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(SCRATCH, exist_ok=True)
    sh('git', 'worktree', 'add', '--detach', path, tag)
    d = load()[name]
    arc = os.path.join(DATA, f'{name}.tar.gz')
    if os.path.exists(arc):
        sh('tar', 'xzf', arc, '-C', path)
    for f, old, new in d.get('fixups', []):      # only where a tool sits at a different place on this machine
        fp = os.path.join(path, f)
        text = open(fp).read()
        open(fp, 'w').write(text.replace(old, new))
    for step in d.get('regen', []):
        subprocess.run(step, shell=True, cwd=path, check=True, capture_output=True)
    return path


FRAME = '''
import sys, os
sys.path.insert(0, 'source')
import {module} as M
{pre}
img = M.{fn}({t})
img.convert('RGB').save({out!r})
'''


def draw(name, t, out, wt=None, timeout=900):
    """One picture at film time t from the saved copy. Returns the folder used."""
    d = load()[name]
    wt = wt or worktree(name)
    if d.get('recipe') == 'stills':           # the older films: python3 MODULE.py stills OUT_DIR T
        import glob
        od = out + '.d'
        shutil.rmtree(od, ignore_errors=True)
        os.makedirs(od)
        r = subprocess.run([sys.executable, f"source/{d['module']}.py", 'stills', os.path.abspath(od), str(t)],
                           cwd=wt, capture_output=True, text=True, timeout=timeout)
        got = sorted(glob.glob(os.path.join(od, '*.png')), key=os.path.getmtime)
        if not got:
            raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200] if (r.stderr or r.stdout).strip() else 'no picture')
        shutil.copy(got[-1], out)
        return wt
    arg = round(t * d['index_fps']) if d.get('index_fps') else t     # some films draw by frame number
    if d.get('recipe') == 'crab':               # the 3D crab dance: node render.mjs stills OUT.png W H T
        r = subprocess.run(['node', 'render.mjs', 'stills', os.path.abspath(out), str(d['size'][0]), str(d['size'][1]), str(t)],
                           cwd=os.path.join(wt, 'source', 'strictly_crabs'), capture_output=True, text=True, timeout=timeout)
        if not os.path.exists(out):
            raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200] if (r.stderr or r.stdout).strip() else 'no picture')
        return wt
    if d.get('recipe') == 'shot':               # the kitchen test: python3 source/shot.py still SHOT OUT_DIR W H T
        od = out + '.d'
        shutil.rmtree(od, ignore_errors=True)
        os.makedirs(od)
        W, H = d['size']
        r = subprocess.run([sys.executable, 'source/shot.py', 'still', d['shotfile'], os.path.abspath(od), str(W), str(H), str(t)],
                           cwd=wt, capture_output=True, text=True, timeout=timeout)
        if not os.path.exists(os.path.join(od, 'draw.png')):
            raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200] if (r.stderr or r.stdout).strip() else 'no picture')
        shutil.copy(os.path.join(od, 'draw.png'), out)
        return wt
    code = FRAME.format(module=d['module'], pre=d.get('pre', ''), fn=d.get('fn', 'frame_image'), t=arg, out=out)
    r = subprocess.run([sys.executable, '-c', code], cwd=wt, capture_output=True, text=True, timeout=timeout)
    if r.returncode or not os.path.exists(out):
        raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200] if (r.stderr or r.stdout).strip()
                           else 'no picture')
    return wt


def film_frame(name, t):
    """A finished film's own picture at time t, drawn from its saved copy (never the live code), cached for the day.
    The kit tests compare the kit's redraw against THIS, so a change to the shared kit can never move the reference."""
    from PIL import Image
    d = load()[name]
    sha = sh('git', 'rev-parse', '--short=10', tagname(name))
    cache = os.path.join(SCRATCH, 'frames')
    os.makedirs(cache, exist_ok=True)
    png = os.path.join(cache, f'{name}-{sha}-{t}.png')
    if not os.path.exists(png):
        wt = os.path.join(SCRATCH, tagname(name).replace('/', '_').replace('+', '_'))
        if not os.path.isdir(wt):
            wt = worktree(name)
        draw(name, t, png, wt)
    return Image.open(png).convert('RGB')


def duration(path):
    return float(sh('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path))


def cmd_recut(name, rest):
    at = float(rest[rest.index('--at') + 1]) if '--at' in rest else None
    out = rest[rest.index('--out') + 1] if '--out' in rest else f'{name}-recut.png'
    d = load()[name]
    if at is None:
        at = round(duration(os.path.join(ROOT, 'animations', d['videos'][0])) * 0.4, 2)
    wt = draw(name, at, os.path.abspath(out))
    print(f'{name}: drawn at {at} s from saved copy {d["save"]} (folder {wt}) -> {out}')


def _grey(path, size=(96, 170)):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(path).convert('L').resize(size), dtype=float)


def video_frames(video, wt, fps=4, size=(96, 170)):
    """The posted video's frames, small, from the copy saved with the bookmark."""
    import numpy as np
    src = os.path.join(wt, 'animations', video)
    if not os.path.exists(src):
        src = os.path.join(ROOT, 'animations', video)
    w, h = size
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={fps},scale={w}:{h},format=gray', '-f', 'rawvideo', '-'],
                       capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    return a.reshape(-1, h, w).astype(float), fps


def compare(png, video, wt, t):
    """How near the redrawn picture is to the posted video: best match over the film's length, and where it was."""
    import numpy as np
    a = _grey(png)
    fr, fps = video_frames(video, wt)
    diffs = np.abs(fr - a[None]).mean(axis=(1, 2))
    i = int(diffs.argmin())
    at = min(len(fr) - 1, int(t * fps))
    return float(diffs[at]), float(diffs[i]), i / fps


def side_by_side(png, video, wt, at, dest):
    """Left: drawn again from the saved copy. Right: the posted video where it matches best."""
    from PIL import Image
    src = os.path.join(wt, 'animations', video)
    if not os.path.exists(src):
        src = os.path.join(ROOT, 'animations', video)
    tmp = dest + '.v.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', src, '-frames:v', '1', tmp], capture_output=True)
    a, b = Image.open(png).convert('RGB'), Image.open(tmp).convert('RGB')
    h = 360
    a, b = (x.resize((round(x.width * h / x.height), h)) for x in (a, b))
    c = Image.new('RGB', (a.width + b.width + 6, h), 'white')
    c.paste(a, (0, 0))
    c.paste(b, (a.width + 6, 0))
    c.save(dest)
    os.remove(tmp)


def cmd_check(names, fracs, jobs=4):
    from concurrent.futures import ThreadPoolExecutor
    reg = load()
    names = names or list(reg)

    def one(n):
        d = reg[n]
        v = next((x for x in d['videos'] if x.endswith('.mp4')), None)
        if d.get('no_frame'):
            return n, 'NOT DRAWN', d['no_frame']
        if not v:
            return n, 'NOT DRAWN', 'only a still picture is posted'
        rows = []
        try:
            wt = worktree(n)
            dur = duration(os.path.join(wt, 'animations', v)) if os.path.exists(os.path.join(wt, 'animations', v)) \
                else duration(os.path.join(ROOT, 'animations', v))
            for f in fracs:
                t = round(dur * f, 2)
                out = os.path.join(SCRATCH, f'{n}-{f}.png')
                draw(n, t, out, wt)
                same, best, at = compare(out, v, wt, t)
                side_by_side(out, v, wt, at, os.path.join(SCRATCH, f'sbs-{n}-{f}.png'))
                rows.append(f't={t} same-time diff {same:.1f}, best {best:.1f} (at {at:.1f}s)')
        except Exception as e:
            return n, 'NOT DRAWN', str(e)[:160]
        ok = all(float(r.split('best ')[1].split(' ')[0]) < 22 for r in rows)
        return n, 'ok' if ok else 'LOOK', '; '.join(rows)
    with ThreadPoolExecutor(jobs) as ex:
        for n, s, m in ex.map(one, names):
            print(f'{n:24} {s:9} {m}', flush=True)


# ---- the count: may never rise ---------------------------------------------------------------------------------
MEASURE_SWAPS = r'''
import sys, types, ast, json, re
sys.path.insert(0, '.')
import gta_cast
film = re.compile(FILM)
mods = [m for m, x in sys.modules.items() if getattr(x, '__file__', None) and x.__file__.startswith(HERE)]
loaded = sorted(m for m in mods if film.match(m) and not m.startswith('gta'))
swaps = []
for mn in mods:
    mod = sys.modules[mn]
    defs = {n.name for n in ast.parse(open(mod.__file__).read()).body if isinstance(n, ast.FunctionDef)}
    for n in defs:
        f = getattr(mod, n, None)
        if isinstance(f, types.FunctionType) and f.__module__ != mn:
            swaps.append(f'{mn}.{n}<-{f.__module__}')
print(json.dumps({'loaded': loaded, 'swaps': sorted(swaps)}))
'''


def static_loads():
    """Kit files that load a finished film's file directly (imports and named strings), and the old films the people
    kit can reach: the numbers from the proposal's measure (graph + reach), made one command."""
    import ast
    mods = {}
    for dp, dn, fn in os.walk(HERE):
        if '__pycache__' in dp:
            continue
        for f in fn:
            if f.endswith('.py'):
                p = os.path.join(dp, f)
                mods[os.path.relpath(p, HERE)[:-3].replace('/', '.')] = p
    top = {m.split('.')[-1]: m for m in mods}
    g = {}
    for m, p in mods.items():
        src = open(p, errors='replace').read()
        deps = set()
        try:
            t = ast.parse(src)
        except Exception:
            continue
        for n in ast.walk(t):
            if isinstance(n, ast.Import):
                for a in n.names:
                    deps.add(a.name.split('.')[0])
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                deps.add(n.module.split('.')[0])
            elif (isinstance(n, ast.Call) and getattr(n.func, 'attr', None) in ('import_module', '__import__')
                  and n.args and isinstance(n.args[0], ast.Constant)):
                deps.add(str(n.args[0].value).split('.')[0])
        g[m.split('.')[-1]] = sorted(d for d in deps if d in top)
    films = {k for k in g if FILM.match(k) and not k.startswith('gta')}
    kit = [k for k in g if k not in films and not k.startswith('gta')]
    loads = sorted(k for k in kit if any(d in films for d in g[k]))
    seen, st = set(), ['people', 'places']
    while st:
        x = st.pop()
        for d in g.get(x, []):
            if d not in seen:
                seen.add(d)
                st.append(d)
    return loads, sorted(x for x in seen if x in films)


def measure():
    r = subprocess.run([sys.executable, '-c', f'HERE={HERE!r}\nFILM={FILM.pattern!r}\n' + MEASURE_SWAPS], cwd=HERE,
                       capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stderr.strip().splitlines()[-1])
    dyn = json.loads(r.stdout.strip().splitlines()[-1])
    loads, reach = static_loads()
    return {'film_files_loaded_by_gta_cast': len(dyn['loaded']), 'steps_swapped': len(dyn['swaps']),
            'kit_files_loading_a_film_file': len(loads), 'old_films_reached_by_people_kit': len(reach)}, dyn, loads, reach


def count_faults(lower=False):
    """For the handover check: a rise in any count is a fault; a fall is welcome (use --lower to keep it)."""
    try:
        now = measure()[0]
    except Exception as e:
        return [f'FREEZE: the count could not be made ({e}); run python3 source/freeze.py count']
    if not os.path.exists(BASE):
        json.dump(now, open(BASE, 'w'), indent=1)
        return []
    base = json.load(open(BASE))
    faults = [f'FREEZE: {k} rose from {base[k]} to {v}: new work may not load a finished film\'s file or swap a kit step '
              f'(python3 source/freeze.py count lists them)' for k, v in now.items() if v > base.get(k, v)]
    if lower and not faults:
        json.dump(now, open(BASE, 'w'), indent=1)
    return faults


def bookmark_faults():
    """Every film in the registry has its bookmark, on the save the registry names; a finished video in animations/
    that no film lists is a fault (a new finished film gets its bookmark the day it is posted: freeze.py tag)."""
    reg = load()
    have = set(sh('git', 'tag', '-l', 'film/*').split())
    out = []
    for n, d in reg.items():
        t = tagname(n)
        if t not in have:
            out.append(f'FREEZE: {n} has no bookmark ({t}); run python3 source/freeze.py tag')
        elif sh('git', 'rev-parse', '--short=8', t + '^{commit}') != d['save'][:8]:
            out.append(f'FREEZE: {t} is not on the save {d["save"]} the registry names')
    listed = {v for d in reg.values() for v in d['videos']} | set(SHELVED)
    for f in sorted(os.listdir(os.path.join(ROOT, 'animations'))):
        if f.endswith(('.mp4', '.png')) and f not in listed:
            out.append(f'FREEZE: animations/{f} belongs to no film in source/data/freeze/films.json: add it, then '
                       f'run python3 source/freeze.py tag --push')
    return out


SHELVED = ('shocking-behaviour-vertical.mp4',)   # never on GitHub (Sam, 18 Oct); named in the notes


def drift_baseline(name, now):
    """How far live code is from a posted film (a share of pixels). The first reading becomes the line it may not cross."""
    f = os.path.join(HERE, 'data', 'freeze', 'drift-baseline.json')
    b = json.load(open(f)) if os.path.exists(f) else {}
    if name not in b:
        b[name] = round(now, 2)
        json.dump(b, open(f, 'w'), indent=1)
    return b[name]


def cmd_count(rest):
    now, dyn, loads, reach = measure()
    base = json.load(open(BASE)) if os.path.exists(BASE) else None
    for k, v in now.items():
        print(f'{k}: {v}' + (f'  (baseline {base[k]})' if base else ''))
    if '--list' in rest or not base:
        print('film files loaded:', ' '.join(dyn['loaded']))
        print('steps swapped:', ' '.join(dyn['swaps']))
    if not base:
        json.dump(now, open(BASE, 'w'), indent=1)
        print('baseline written')
        return 0
    f = count_faults(lower='--lower' in rest)
    for x in f:
        print(x)
    print('Checks: freeze count: ' + ('RISEN' if f else 'not risen'))
    return 1 if f and '--check' in rest else 0


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    pos = [a for i, a in enumerate(rest) if not a.startswith('--') and (i == 0 or not rest[i - 1].startswith('--'))]
    if cmd == 'list':
        cmd_list()
    elif cmd == 'tag':
        cmd_tag('--push' in rest)
    elif cmd == 'recut':
        cmd_recut(pos[0], rest)
    elif cmd == 'check':
        fr = [float(x) for x in rest[rest.index('--at') + 1].split(',')] if '--at' in rest else [0.4]
        names = [a for a in pos if a not in (rest[rest.index('--at') + 1] if '--at' in rest else '')]
        cmd_check(names, fr)
    elif cmd == 'count':
        return cmd_count(rest)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
