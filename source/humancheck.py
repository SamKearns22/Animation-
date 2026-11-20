#!/usr/bin/env python3
"""MAP  humancheck: is every person in every frame a human body? (proposal big-body-moves, Change 1; Sam's Y 20 Nov,
GTA shot 4: "Limbs, neck, torso, all curled around each other ... Utterly inhuman. It really worries me that this
wasn't caught by anything we have so far implemented.")

Why: the old checks measured the skeleton (views.check_arm3: bone lengths, folds) and single joints against solids.
Shot 4's skeleton measured human at every moment (notes/proposals/big-body-moves/learn.md); the horror was in the
DRAWN picture: arms drawn over his back while they reached in front of him, an arm drawn apart from its shoulder, the
gun drawn pointing away from its target. So this tests what is drawn, where it is drawn, every person, every frame.

  hook ............ views._person and lying_flat.draw report each person as they are drawn (HOOK, set while ON)
  frame_begin/end . a writer wraps each drawing; frame_end(t) returns that drawing's faults
  _order .......... an arm drawn over the body while both its elbow and hand are behind the body (an arm out of
                    the back), or hidden behind the body while both are well in front of it (a stump)
  _joined ......... the person redrawn alone (no props): one joined shape; a piece apart = a limb off its joint
  _lying .......... skeleton-route people (lying_flat): lying.body_faults (arm on its own side, a neck shows)
  aim ............. a film reports a fired gun as drawn (muzzle, barrel and target on screen): more than 10 degrees
                    off its target is a fault
  Writer .......... per clip: collects faults per person and kind, writes OUT.bodycheck.txt, refuses (holds the
                    video aside) on an unnamed fault
  critiqued ....... rule 89: records that a fresh critique looked at this video (its pack, newer than the video)
  sendgate ........ PreToolUse hook on SendUserFile: a video made since START reaches Sam only with a body check
                    record that is clean or named, and a critique record

    python3 source/humancheck.py critiqued VIDEO PACKDIR     after the critic's result.md for this video
    python3 source/humancheck.py name VIDEO "why each fault is named to Sam"
    python3 source/humancheck.py show VIDEO
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

START = 1795212000.0          # 20 Nov 2026 22:00 UTC: videos made before the gate are not asked for a record
ON = [False]
_ENTRIES = []
_AIMS = []
_BUSY = [False]               # a redraw by this check is not itself recorded
AIM_DEG = 10.0
MIN_PX = 220                  # a person drawn shorter than this (canvas pixels) is too small for the joined test


def _hook(e):
    if _BUSY[0]:
        return
    f = sys._getframe(2)
    for _ in range(6):                                 # people_hats.head_box measuring a bare head: not a drawing
        if f is None:
            break
        if f.f_code.co_name == 'head_box':
            return
        f = f.f_back
    _ENTRIES.append(e)


def install():
    import views as V
    V.HC_HOOK[0] = _hook
    try:
        import lying_flat as LF
        LF.HC_HOOK[0] = _hook
    except ImportError:
        pass
    ON[0] = True


def frame_begin():
    if not ON[0]:
        install()
    del _ENTRIES[:]
    del _AIMS[:]


def aim(who, muzzle, barrel, target, firing=True):
    """A fired gun as drawn, in canvas pixels: muzzle (x, y), barrel direction (dx, dy), target (x, y)."""
    _AIMS.append((who, muzzle, barrel, target, firing))


def frame_end(t):
    out = []
    for e in list(_ENTRIES):
        who = ((e.get('sp') or {}).get('name') or e.get('who') or 'someone').split(' (')[0]
        try:
            if e['kind'] == 'flat':
                out += [(who, k, x) for k, x in _order(e)]
                out += [(who, k, x) for k, x in _joined(e)]
            elif e['kind'] == 'skeleton':
                out += [(who, k, x) for k, x in _lying(e)]
        except Exception as ex:                    # a check that cannot run is said, never silent
            out.append((who, 'check', f'body check could not run ({type(ex).__name__}: {ex})'))
    for who, (mx, my), (dx, dy), (tx, ty), firing in _AIMS:
        if not firing:
            continue
        a1, a2 = math.atan2(dy, dx), math.atan2(ty - my, tx - mx)
        off = abs((math.degrees(a1 - a2) + 180) % 360 - 180)
        if off > AIM_DEG:
            out.append((who, 'aim', f'the gun points {off:.0f} degrees off its target as drawn'))
    del _ENTRIES[:]
    del _AIMS[:]
    return [(t, w, k, x) for w, k, x in out]


# ---------------------------------------------------------------------------------------------- the tests
def _surface(j, sd, vd, lean, sp, key):
    """The torso's surface depths (nearest, farthest) along the screen line through this joint, the torso an ellipse
    (half-width the shoulders, half-depth 0.6 of them: torso_outline's side view); None where the joint's screen x
    misses the torso (beside it: drawing order does not matter there)."""
    import views as V
    x, y, z = j[key + sd]
    (px, _), _ = V.project(V.leaned((x, y, z), lean), vd)
    a, b = sp.get('shoulders', 150) - 14, 0.6 * sp.get('shoulders', 150)
    ds = []
    for i in range(72):
        th = math.radians(i * 5)
        (qx, _), dq = V.project(V.leaned((a * math.cos(th), y, b * math.sin(th)), lean), vd)
        if abs(qx - px) < 10:
            ds.append(dq)
    return (max(ds), min(ds)) if ds else None


def _order(e):
    import views as V
    j, vd, depth, j2, behind = e['j'], e['view_deg'], e['depth'], e['j2'], e['behind']
    view = V.VIEWS[vd]
    if view == 'front':
        return []
    lean = j.get('lean', 0.0)
    (cx, cy), dc = V.project(V.leaned((0.0, 225.0, 0.0), lean), vd)
    (fx, _), _ = V.project(V.leaned((0.0, 225.0, 100.0), lean), vd)
    face = 1 if fx > cx + 1 else -1 if fx < cx - 1 else 0     # the screen side his chest faces (0: back on)
    sp = e['sp']
    half = (sp.get('shoulders', 150) - 14) * (0.55 if view == 'side' else 0.8)
    hem = min(sp.get('bottom', V.JACKET), 470.0)
    out = []
    for sd in 'LR':
        de, dw = depth['el' + sd], depth['wr' + sd]
        sh, el, wr = j2['sh' + sd], j2['el' + sd], j2['wr' + sd]
        pts = [(el[0] + (wr[0] - el[0]) * u, el[1] + (wr[1] - el[1]) * u) for u in (0.0, 0.25, 0.5, 0.75, 1.0)]
        pts += [(sh[0] + (el[0] - sh[0]) * u, sh[1] + (el[1] - sh[1]) * u) for u in (0.5, 0.75)]
        over = sum(1 for x, y in pts if abs(x - cx) < half and 40 < y < hem)
        far_side = sd in behind and (wr[0] - cx) * (sh[0] - cx) < 0 and abs(wr[0] - cx) > half
        # a hand just peeking past the side his chest faces is a far arm reaching forward (arms folded from
        # three-quarter back); a long forearm out there with its shoulder hidden on the other side reads as an arm out
        # of his back (GTA v4 1.67 s, Sam's notes 3, 6, 7: wrist 80 px past his outline)
        far_side = far_side and not (face and (wr[0] - cx) * face > 0 and abs(wr[0] - cx) < half + 45)
        if over < 2 and not far_side:
            continue
        if sd not in behind and de < dc - 40 and dw < dc - 40:
            out.append(('order', f'{sd} arm drawn over the body though its elbow and hand are behind it (an arm out '
                                 f'of the {"back" if "back" in view else "side"})'))
        elif far_side:
            out.append(('order', f'{sd} arm hidden behind the body comes out on the far side, away from its own '
                                 f'shoulder (reads as an arm out of the {"back" if "back" in view else "body"})'))
        elif sd in behind and sd not in j.get('on_face', ()) and 'el' + sd in j:   # (on_face: redrawn over him)
            # hidden, but the elbow and hand are nearer us than the torso's own near surface where they cross it
            # (pose gallery, 20 Nov: a hanging near arm beside the body, nearer than its centre, is not in front)
            sel, swr = _surface(j, sd, vd, lean, sp, 'el'), _surface(j, sd, vd, lean, sp, 'wr')
            if sel and swr and de > sel[0] + 25 and dw > swr[0] + 25:
                out.append(('order', f'{sd} arm hidden behind the body though its elbow and hand are in front of it'))
    return out


def _joined(e):
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    import body as B
    import views as V
    s = e['s']
    if s * B.SS * 1150 < MIN_PX:
        return []
    j = dict(e['j'])
    j['props'], j['pre'], j['mid'] = [], [], []   # held things and set pieces (a desk, a chair) are not his body
    j['chair_draw'] = lambda *a, **k: None        # (Milburn: the PM's dispatch box read as a limb apart)
    W = int(1700 * s * B.SS) + 8
    H = int(1700 * s * B.SS) + 8
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    _BUSY[0] = True
    try:
        V.person(lay, B.Cam(1.0), 850 * s, 450 * s, s, e['sp'], e['t'], e['yaw'], j, e.get('head_yaw'),
                 e.get('tilt'))
    finally:
        _BUSY[0] = False
    al = np.asarray(lay.getchannel('A')) > 60
    lab, n = ndimage.label(al, structure=np.ones((3, 3)))
    if n < 2:
        return []
    areas = np.bincount(lab.ravel())[1:]
    big = areas.max()
    apart = [a for a in areas if a != big and a > max(0.02 * areas.sum(), 40)]
    if apart:
        return [('joined', f'{len(apart)} piece(s) drawn apart from the body ({int(max(apart))} px): a limb off its '
                           f'joint')]
    return []


def _lying(e):
    import lying as L
    out = []
    for f in L.body_faults(e['k'], e['sp'], cam=e.get('cam'), who=''):
        out.append(('skeleton', f.lstrip(': ')))
    return out


# ---------------------------------------------------------------------------------------------- per clip
class Writer:
    """Collects one clip's faults: one line per person and kind (first time, how many drawings)."""

    def __init__(self, label=''):
        self.label, self.found = label, {}
        frame_begin()

    def frame(self, t, faults):
        for t0, who, kind, text in faults:
            k = (who, kind, text.split(' (')[0])
            if k not in self.found:
                self.found[k] = [t0, 0, f'{who}: {text}']
            self.found[k][1] += 1

    def lines(self):
        return [f'BODY: {self.label} {t0:.2f} s: {text} ({n} drawing{"s" if n > 1 else ""})'
                for t0, n, text in sorted(self.found.values())]

    def finish(self, out, named=False):
        """Write OUT.bodycheck.txt; on an unnamed fault hold the video aside and stop."""
        lines = self.lines()
        rec = dict(video=os.path.basename(out), faults=lines, named=bool(named and lines), critique=None,
                   made=os.path.getmtime(out) if os.path.exists(out) else None)
        _save(out, rec)
        print('\n'.join(lines) or f'body check ({self.label}): clean, every person, every drawing', flush=True)
        if lines and not named:
            held = os.path.splitext(out)[0] + '.held.mp4'
            if os.path.exists(out):
                os.replace(out, held)
                _save(held, dict(rec, video=os.path.basename(held)))
            sys.exit(f'clip STOPPED (body check): {len(lines)} fault(s) above. The video is held as {held}. Fix them '
                     f'and render again, or name every one to Sam (python3 source/humancheck.py name VIDEO "why").')


def _side(video):
    return video + '.bodycheck.json'


def _save(video, rec):
    with open(_side(video), 'w') as fh:
        json.dump(rec, fh, indent=1)


def load(video):
    try:
        return json.load(open(_side(video)))
    except (OSError, ValueError):
        return None


def copy_record(src, dst):
    """finish.py: the finished video carries its clean render's record (faults, names, critique)."""
    rec = load(src)
    if rec is not None:
        _save(dst, dict(rec, video=os.path.basename(dst), made=os.path.getmtime(dst)))


def send_faults(video):
    """Why this video may not go to Sam yet ([] = it may)."""
    if not os.path.exists(video) or os.path.getmtime(video) < START:
        return []
    rec = load(video)
    if rec is None:
        return [f'{video}: no body check record. Render it with a writer that runs the body check (film_engine render, '
                f'gta_rehearse clip, or humancheck.Writer), or finish.py from such a render.']
    out = []
    if rec.get('faults') and not rec.get('named'):
        out.append(f'{video}: {len(rec["faults"])} body fault(s) not named to Sam: fix, or humancheck.py name VIDEO "why"'
                   f' and say each in the message ("Checks:" line).')
    if not rec.get('critique'):
        out.append(f'{video}: no fresh critique of this video (rule 89). Run critique.py pack on its frames, a NEW '
                   f'helper, then: python3 source/humancheck.py critiqued {video} PACKDIR')
    return out


def sendgate():
    """PreToolUse hook (SendUserFile): exit 2 with the reasons when a video may not go to Sam yet."""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    files = (data.get('tool_input') or {}).get('files') or []
    root = data.get('cwd') or os.getcwd()
    why = []
    for f in files:
        if os.path.splitext(f)[1].lower() in ('.mp4', '.mov', '.gif', '.webm'):
            why += send_faults(f if os.path.isabs(f) else os.path.join(root, f))
    if why:
        print('send REFUSED (body check / rule 89):\n' + '\n'.join(why), file=sys.stderr)
        return 2
    return 0


def main(a):
    if a and a[0] == 'sendgate':
        sys.exit(sendgate())
    if len(a) >= 3 and a[0] == 'critiqued':
        video, pack = a[1], a[2]
        res = os.path.join(pack, 'result.md')
        rec = load(video)
        if rec is None:
            sys.exit(f'humancheck: {video} has no body check record')
        if not os.path.exists(res) or os.path.getmtime(res) < os.path.getmtime(video):
            sys.exit(f'humancheck: {res} is missing or older than the video: the critique must look at THIS video')
        rec['critique'] = os.path.relpath(pack, os.path.dirname(HERE))
        _save(video, rec)
        print(f'humancheck: critique recorded for {video}')
        return
    if len(a) >= 3 and a[0] == 'name':
        rec = load(a[1])
        if rec is None:
            sys.exit(f'humancheck: {a[1]} has no body check record')
        rec['named'], rec['why_named'] = True, a[2]
        _save(a[1], rec)
        print(f'humancheck: {len(rec.get("faults") or [])} fault(s) named; each goes in the message to Sam')
        return
    if len(a) >= 2 and a[0] == 'show':
        print(json.dumps(load(a[1]), indent=1))
        return
    print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
