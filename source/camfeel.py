#!/usr/bin/env python3
"""camfeel: rule 72's camera feel (tool chat, Sam Y 12 Nov; Blessed note 51: "the zoom in is sudden and violent").

MAP (rule 61):
  FAST, JERK 26     the limits: how fast a measured move may go, and how suddenly it may start or stop
  _cam 40           any film's camera: B.Cam (zoom, centre) or a perspective camera (sets.Cam: project, at)
  sample 52         the camera every frame, cut into shots (a cut is never a move); _step 75: one frame to the next
  moves 101         each shot's moves: where the camera is moving, its top speed, and how it starts and stops
  sharp_spans 124   the acting list's rows marked 'sharp' (or 'snap zoom', 'whip pan'), as times
  faults 150        a fast or sudden move the acting list doesn't mark sharp; a move across a cut that changes speed
  main 188          python3 source/camfeel.py FILM [--all]: the moves and the faults

Every camera move is measured (eased in and out, never rushed) unless the acting list's row for it says sharp.
Speeds are what the viewer sees: a zoom as how fast the picture grows (doublings a second), a pan as how fast the
picture slides (frame widths a second, at the zoom of that moment).
"""
import importlib
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FAST = dict(zoom=0.7, pan=0.45)    # a measured move stays under: 0.7 doublings a second, 0.45 frame widths a second
#   (calibrated 12 Nov on Blessed: the release pan Sam called sudden, note 51, peaks at 1.08 widths a second; the
#    TV-room push he has passed peaks at 0.67 doublings a second)
JERK = 0.5                         # a measured move eases in and out: its first and last moving frames stay under half
#                                    its top speed (a cut in a still camera, or a stop dead, is sudden)
STILL = 0.02                       # slower than this (doublings or widths a second) is a held camera
FELT = 0.15                        # a move slower than this at its top is a drift: its start and stop aren't felt
CUT = 0.25                         # one frame that changes the picture by this (doublings or widths), with the frames
#                                    either side under a quarter of it, is a cut inside the shot, not a move
W = 1080.0


def _cam(c):
    """What the check can read of whatever the film's cam_for(t) returns: ('2d', zoom, centre x, centre y) for B.Cam
    (or anything holding one in .cam), ('3d', cam) for a perspective camera with project() and a look-at point (sets.Cam),
    or None."""
    for obj in (c, getattr(c, 'cam', None)):
        if obj is None:
            continue
        if hasattr(obj, 'project') and hasattr(obj, 'at'):
            return ('3d', obj)
        z, x, y = getattr(obj, 'z', None), getattr(obj, 'cx', None), getattr(obj, 'cy', None)
        if all(isinstance(v, (int, float)) for v in (z, x, y)):
            return ('2d', float(z), float(x), float(y))
    return None


def _shot_at(film, t):
    return next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')


def sample(film, fps=12):
    """[(shot, [(t, camera), ...])] in film order, one entry per shot; None if the film has no readable camera."""
    fn = getattr(film, 'cam_for', None)
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    if fn is None or not end:
        return None
    out, cur = [], None
    for i in range(int(end * fps)):
        t = i / fps
        try:
            c = _cam(fn(t))
        except Exception:
            c = None
        if c is None:
            continue
        shot = _shot_at(film, t)
        if cur is None or cur[0] != shot:
            cur = (shot, [])
            out.append(cur)
        cur[1].append((t, c))
    return out or None


def _step(a, b):
    """How the picture changes from camera a to camera b: (doublings of size, frame widths slid)."""
    if a[0] == '2d' and b[0] == '2d':
        _, z0, x0, y0 = a
        _, z1, x1, y1 = b
        return abs(math.log2(max(z1, 1e-6) / max(z0, 1e-6))), math.hypot(x1 - x0, y1 - y0) * (z0 + z1) / 2 / W
    if a[0] == '3d' and b[0] == '3d':                   # the first camera's look-at point, seen by both
        p = a[1].at
        (x0, y0), k0 = a[1].project(p)
        (x1, y1), k1 = b[1].project(p)
        s0, s1 = getattr(a[1], 'shake', (0, 0)), getattr(b[1], 'shake', (0, 0))   # a shake is not a move
        return (abs(math.log2(max(k1, 1e-9) / max(k0, 1e-9))),
                math.hypot(x1 - s1[0] - x0 + s0[0], y1 - s1[1] - y0 + s0[1]) / W)
    return 0.0, 0.0


def _speeds(pts):
    """Per step: (t, zoom speed in doublings/s, pan speed in frame widths/s)."""
    out = []
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        dt = (t1 - t0) or 1e-6
        zs, ps = _step(a, b)
        out.append(((t0 + t1) / 2, zs / dt, ps / dt))
    return out


def moves(shot, pts):
    """Each run of moving steps in a shot: dict(shot, t0, t1, kind, top, start, stop, at) (speeds in the units above)."""
    sp = _speeds(pts)
    v = [max(s[1] / 12, s[2] / 12) for s in sp]          # each step's change (12 drawings a second)
    cuts = {i for i in range(len(sp)) if v[i] > CUT and all(v[k] < v[i] / 4 for k in (i - 1, i + 1) if 0 <= k < len(sp))}
    out, run = [], []
    for i, s in enumerate(sp + [(None, 0.0, 0.0)]):
        if s[0] is not None and i not in cuts and max(s[1], s[2]) > STILL:
            run.append(s)
            continue
        if run:
            kind = 'zoom' if max(r[1] for r in run) / FAST['zoom'] >= max(r[2] for r in run) / FAST['pan'] else 'pan'
            k = 1 if kind == 'zoom' else 2
            top = max(r[k] for r in run)
            at = max(run, key=lambda r: r[k])[0]
            out.append(dict(shot=shot, t0=run[0][0], t1=run[-1][0], kind=kind, top=top, at=at,
                            start=run[0][k] / top if top else 0, stop=run[-1][k] / top if top else 0,
                            at_start=run[0] is sp[0] or sp.index(run[0]) - 1 in cuts,
                            at_end=run[-1] is sp[-1] or sp.index(run[-1]) + 1 in cuts, speeds=[r[k] for r in run]))
            run = []
    return out


_SHARP = re.compile(r'\bsharp\b|snap[- ]zoom|whip[- ]pan|crash[- ]zoom', re.I)


def sharp_spans(film, text):
    """The times the acting list marks sharp: [(t0, t1, row text)]. A row marks the shots it names (a SHOTS name as a
    word) and the line it starts with (its number: that line's start to end, from LINES)."""
    m = re.search(r'^##+ *(The )?acting list.*?$(.*?)(?=^## |\Z)', text, re.M | re.S | re.I)
    rows = [ln for ln in (m.group(2).splitlines() if m else []) if ln.strip().startswith('|')][2:]
    shots = getattr(film, 'SHOTS', [])
    lines = {str(ln.get('n')): ln for ln in getattr(film, 'LINES', []) or [] if isinstance(ln, dict)}
    out = []
    for row in rows:
        if not _SHARP.search(row):
            continue
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        for s in shots:
            if re.search(r'(?<![\w-])' + re.escape(str(s[0])) + r'(?![\w-])', row):
                out.append((s[1], s[2], row))
        n = re.match(r'(\d+)', cells[0]) if cells else None
        if n and n.group(1) in lines:
            ln = lines[n.group(1)]
            out.append((ln['start'], ln['end'], row))
    return out


def faults(film, text=None, fps=12):
    """Rule 72: a camera move faster than FAST, or one that starts or stops suddenly (JERK), with no acting list row
    marking it sharp; and a move carried across a cut that jumps in speed there (a move across a cut is one move).
    A shot with a row in the notes' exceptions (| camera feel | SHOT | why | looked |) is left out."""
    if text is None:
        import preflight
        path = preflight.notes_path(film, film.__name__)
        text = open(path).read() if os.path.exists(path) else ''
    import waivers
    table = waivers.rows(text)
    return [x for x in _faults(film, text, fps) if not waivers.waived(table, 'camera feel', x.split(' ')[3])]


def _faults(film, text, fps):
    shots = sample(film, fps)
    if shots is None:
        return ['CAMERA FEEL: shot *: the film gives no camera the check can read (cam_for(t) returning a B.Cam or '
                'a sets.Cam): rule 72 not checked (give it one, or a row in the exceptions: | camera feel | * | why '
                '| looked |)']
    sharp = sharp_spans(film, text)
    out = []
    allm = [(m, i) for i, (shot, pts) in enumerate(shots) for m in moves(shot, pts)]
    for m, i in allm:
        if any(t0 - 0.1 <= m['at'] <= t1 + 0.1 for t0, t1, _ in sharp):
            continue
        why = []
        if m['top'] > FAST[m['kind']]:
            unit = 'doublings' if m['kind'] == 'zoom' else 'frame widths'
            why.append(f'fast ({m["top"]:.2f} {unit} a second at {m["at"]:.2f} s; measured stays under '
                       f'{FAST[m["kind"]]})')
        if m['top'] > FELT and m['start'] > JERK and not m['at_start']:   # (a move begun at a cut, or cut off
            why.append(f'starts at {m["start"]:.0%} of its top speed (no ease in)')   # by one, is seen mid-move)
        if m['top'] > FELT and m['stop'] > JERK and not m['at_end']:
            why.append(f'stops from {m["stop"]:.0%} of its top speed (no ease out)')
        if why:
            out.append(f'CAMERA FEEL: shot {str(m["shot"]).replace(" ", "_")} {m["t0"]:.2f}-{m["t1"]:.2f} s, the {m["kind"]}: ' +
                       '; '.join(why) + ' (rule 72: measured unless the acting list marks it sharp)')
    for (a, i), (b, j) in zip(allm, allm[1:]):          # one move across a cut: the speed carries on
        if j == i + 1 and a['at_end'] and b['at_start'] and a['kind'] == b['kind']:
            v0, v1 = a['speeds'][-1], b['speeds'][0]
            if max(v0, v1) > FAST[a['kind']] / 2 and min(v0, v1) < 0.5 * max(v0, v1):
                out.append(f'CAMERA FEEL: shot {str(b["shot"]).replace(" ", "_")} starts with the {a["kind"]} '
                           f'carried across the cut at {b["t0"]:.2f} s (from {a["shot"]}): it jumps from {v0:.2f} to {v1:.2f} a second (rule 72: a move across a cut is '
                           'one move)')
    return out


def main():
    name = sys.argv[1]
    film = importlib.import_module(name)
    shots = sample(film)
    if shots is None:
        print(f'{name}: no readable camera (cam_for)')
        return
    if '--all' in sys.argv:
        for shot, pts in shots:
            for m in moves(shot, pts):
                print(f'{shot:12s} {m["t0"]:6.2f}-{m["t1"]:6.2f} {m["kind"]:4s} top {m["top"]:.2f} at {m["at"]:.2f} '
                      f'start {m["start"]:.0%} stop {m["stop"]:.0%}')
    f = faults(film)
    print(f'camera feel ({name}):', 'clean' if not f else f'{len(f)} fault(s)')
    for x in f:
        print(' -', x)


if __name__ == '__main__':
    main()
