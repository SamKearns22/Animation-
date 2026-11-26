#!/usr/bin/env python3
"""MAP  islamocommunism_model_body (was model_body_test; filed on the film side 26 Nov, freeze count 21->20): the investigation's moving test (model-body-all step 2, Sam's Y 25 Nov). Islamocommunism
(posted 5 Nov) shots 3-5 redrawn with model bodies (model_body.py) at the film's own cameras, times and poses; the
posted film beside it. This file holds only what is Islamocommunism's own (its flutes and handset as solids, the
desk's kneehole, the door leaf and the wall round the doorway); the drawing itself is model_body's.
'move to shared': the head-hook fix in _heads() (old films hook TC.HEADS, the kit now draws through body.HEADS).

  people(t) ......... the film's people code run with midterminal_set.put caught: [(sp, x, z, facing, j, lift)]
  solids(t, cam) .... the set's furniture (desk with its kneehole) and the door leaf, as solids that hide
  frame(t) .......... one 1080 x 1920 frame (and its faults: crossings, gaps between hand and arm)
  clip(t0, t1, out) . side by side at phone size: posted | model body

    python3 source/islamocommunism_model_body.py still T OUT.png
    python3 source/islamocommunism_model_body.py clip T0 T1 OUT.mp4
"""
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_body as MB          # noqa: E402
import bench_draw as BD          # noqa: E402

ROOT = os.path.dirname(HERE)
POSTED = os.path.join(ROOT, 'animations', 'islamocommunism-vertical.mp4')
_F = {}
FAULTS = []


def film():
    if _F:
        return _F
    import islamocommunism as I
    import midterminal_set as MS
    import midterminal_moves as MV
    import burnham as B
    import lying as LY
    _heads()
    _F.update(I=I, MS=MS, MV=MV, B=B, LY=LY)
    old = I.held_flute

    def held_flute(side, tilt=0.0):              # the film's own flute, tagged so the solid knows hand and tilt
        d = old(side, tilt)
        d.flute = (side, tilt)
        return d
    I.held_flute = held_flute
    oldk = I.handset_k

    def handset_k(side, k):
        d = oldk(side, k)
        d.handset = side
        return d
    I.handset_k = handset_k
    I.desk_arm_item = lambda t: (0.0, 99.0, lambda im, c: None)   # the solid desk hides the legs itself
    return _F


def _heads():
    """Old films hook their heads into traitors_cast's HEADS; the kit now draws heads through body.HEADS (found 25 Nov:
    Islamocommunism rebuilt today drew both bald, no beard). Hook both."""
    import body
    import midterminal_cast as MC
    import islamocommunism_cast as IC
    for k in ('elsayed', 'aoc'):
        body.HEADS[k] = MC.TC.HEADS[k]
        body.TORSOS[k] = MC.TC.TORSOS[k]
    body.HAIR_BEHIND['aoc'] = IC.aoc_hair_back


def _ss(n):
    """The drawing scale, in both people modules (burnham and body each keep their own SS)."""
    import body
    import burnham
    burnham.SS = body.SS = n


def people(t):
    F = film()
    I, MS = F['I'], F['MS']
    got = []
    old = MS.put

    def put(img, cm, sp, x, z, facing, j=None, t=0.0, head_yaw=None, lift=0.0):
        got.append(dict(sp=sp, x=x, z=z, facing=facing, j=j, lift=lift, head_yaw=head_yaw))
    MS.put = put
    try:
        items = I.people(t)
        bg = Image.new('RGBA', (1080 * 2, 1920 * 2), (0, 0, 0, 255))
        _ss(2)
        MS.render(bg, I.cam_for(t), items)
    finally:
        MS.put = old
    return got, bg


def _desk_swap(nm, i, part):
    """The Resolute desk is drawn as one block; under its top a seated man's knees need the kneehole: two pedestals
    and the front panel (from the front the solid looks the same as the block)."""
    if not nm.startswith('set@0.00,3.00') or i != 0:
        return None
    P = np.array([p for f in part for p in f.pts])
    lo, hi = P.min(0), P.max(0)
    out = []
    for a, b in ((lo[0], lo[0] + 0.5), (hi[0] - 0.5, hi[0])):
        out.append(MB.box((a, lo[1], lo[2]), (b, hi[1], hi[2])) + ('desk pedestal',))
    out.append(MB.box((lo[0], lo[1] + 0.05, lo[2]), (hi[0], hi[1], lo[2] + 0.04)) + ('desk front',))
    out.append(MB.box((lo[0], hi[1] - 0.08, lo[2]), (hi[0], hi[1], hi[2])) + ('desk drawer',))
    return out


def chair_push(t):
    """His chair rolls back as he stands (standing where he sat, he stood inside it: the flat film's chair never
    moved). Pushed back 0.4 m over the rise, by the backs of his legs, then left there."""
    I = film()['I']
    if I.shot_of(t) not in ('office', 'two') or t < I.T['rise']:
        return 0.0
    u = min(1.0, (t - I.T['rise']) / (I.RISE * 0.8))
    return 0.4 * u * u * (3 - 2 * u)


def door_leaf(t):
    F = film()
    I, MS, MV = F['I'], F['MS'], F['MV']
    if I.shot_of(t) != 'door':
        return []
    t_open = MV.door_curve(t, I.T['open'], I.T['open'] + 0.4, 1e9)
    ang = 100.0 * max(0.0, t_open)
    c, h = MV.DOOR_A, MV.DOOR_H + MV.DOOR_W
    hinge = MS.wp(c - h, 0.0, 0.015)
    corners = ((c - h, 0.0), (c + h, 0.0), (c + h, 2.45), (c - h, 2.45))
    leaf = [MV._rot_out(MS.wp(a, y, 0.015), hinge, ang) for a, y in corners]
    back = [MV._rot_out(MS.wp(a, y, 0.015 + MV.DOOR_T), hinge, ang) for a, y in corners]
    P = np.array(leaf + back, float)
    T = np.array([(0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1), (1, 5, 6), (1, 6, 2),
                  (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0)])
    return [(P, T, 'door leaf')]


def props_of(person, k, f):
    """The film's held things as solids: flutes (upright, at the wrist the flat flute stood on) and the handset."""
    j = person['j']
    out = []
    M = F_M() * f
    up = np.array([0, 1.0, 0])
    for d in list(j.get('props', [])) + list(j.get('face_props', [])):
        if hasattr(d, 'flute'):
            sd, tilt = d.flute
            w = np.asarray(k['wr' + sd], float)
            el = np.asarray(k['el' + sd], float)
            fw = MB._u(w - el)
            ax = MB._u(np.cross(np.asarray(k['fwd'], float), up))
            a = math.radians(tilt)
            upv = MB._u(up * math.cos(a) - ax * math.sin(a))
            out += MB.flute_mesh(w, upv, np.asarray(k['fwd'], float), M)
            _ = fw
        if hasattr(d, 'handset'):
            w = np.asarray(k['wr' + d.handset], float)
            ax = MB._u(np.cross(np.asarray(k['fwd'], float), up))
            fw = MB._u(np.asarray(k['fwd'], float))
            c = w + up * 6 * M + fw * 30 * M
            P, T = MB.box(c - ax * 50 * M - up * 12 * M - fw * 10 * M, c + ax * 50 * M + up * 12 * M + fw * 10 * M)
            out.append((P, T, 'handset'))
    return out


def F_M():
    import views as V
    return V.M_PER_UNIT


def skeleton(person):
    """lying.Body from the flat pose, at the person's real height (the flat drawing is scaled by height / 1.75)."""
    LY = film()['LY']
    f = person['sp'].get('height', 1.75) / 1.75
    a = math.radians(person['facing'])
    k = LY.from_views(person['j'], person['sp'], person['x'], person['z'], (math.sin(a), math.cos(a)),
                      ground=person['lift'])
    base = np.array([person['x'], person['lift'], person['z']])
    for n, p in list(k.items()):
        if n in ('fwd', 'hup', 'hfwd') or n.startswith(('toe', 'sup')):
            continue
        if isinstance(p, np.ndarray) and p.shape == (3,):
            k[n] = base + (p - base) * f
    return k, f


def frame(t, scale=2):
    """One frame at 1080 x 1920: the set with nobody in it, the model bodies, their solids and house heads."""
    F = film()
    I, MS, MV, B = F['I'], F['MS'], F['MV'], F['B']
    cam = I.cam_for(t)
    MS.DESK_CHAIR = (0.0, 3.75 + chair_push(t))
    global SEAT
    SEAT = SEAT0[:3] + (SEAT0[3] + chair_push(t), SEAT0[4] + chair_push(t))
    who, bg = people(t)
    _ss(1)
    objs, attrs, owner = [], {}, {}
    solid_ix = set()
    bodies = []
    for pi, person in enumerate(who):
        sp = person['sp']
        k0, f = skeleton(person)
        import views as V
        kit_hip = (928 - V.standing(sp)['hipL'][1]) * F_M() * f
        k = MB.real_skeleton(k0, sp, kit_hip, seat=SEAT, surfaces=SURFACES,
                             held=set(person['j'].get('grip') or ()) | {d.handset for d in person['j'].get('props', []) if hasattr(d, 'handset')})
        person['gaps'] = (round(float(k['_reach']), 3), round(float(k['_foot']), 3))
        P, R = MB.pose(k, sp)
        oi = len(objs)
        objs.append((P, R['T'], np.zeros(len(R['T']), np.int64), sp['who']))
        attrs[oi] = np.concatenate([R['v'], R['grp']], 1)
        owner[oi] = (pi, 'body')
        bodies.append((person, k, f, P, R, oi))
        for sd in 'LR':                          # the house circle hand: a ball 12 units past the wrist, radius 26
            el, wr = np.asarray(k['el' + sd]), np.asarray(k['wr' + sd])
            d = MB._u(wr - el)
            Pb, Tb = MB.ball(wr + d * 12 * F_M() * f, 26 * F_M() * f)
            owner[len(objs)] = (pi, 'hand')
            objs.append((Pb, Tb, np.full(len(Tb), MB.PIX['hand']), sp['who'] + ' hand' + sd))
        for Pp, Tp, part in props_of(person, k, f):
            owner[len(objs)] = (pi, part)
            objs.append((Pp, Tp, np.full(len(Tp), MB.PIX[part]), sp['who'] + ' ' + part))
    solids = MB.set_solids(MS, _desk_swap) + door_leaf(t)
    for Ps, Ts, nm in solids:
        solid_ix.add(len(objs))
        objs.append((Ps, Ts, np.full(len(Ts), MB.PIX['solid']), nm))
    zb, pb, ob, ab = MB.raster(cam, objs, scale, attrs)
    solid = np.isin(ob, list(solid_ix))
    # each body's dots painted from its rest point
    for person, k, f, P, R, oi in bodies:
        m = ob == oi
        if m.any():
            pb[m] = MB.suit_parts(ab[m][:, :3], ab[m][:, 3:], R, person['sp'])
    # the wall round the doorway: a body dot behind the wall shows only through the opening
    hidden = solid.copy()
    if I.shot_of(t) == 'door':
        wpt = MB.world_of(cam, zb, scale)
        r = (wpt[..., 0] / MS.A) ** 2 + (wpt[..., 2] / MS.BZ) ** 2
        op = np.asarray(MV.opening_mask((W_ * scale, H_ * scale), _ScaledCam(cam, scale)))
        behind = (ob >= 0) & ~solid & (r > 1.0) & (op < 128)
        hidden |= behind
    drawn = (ob >= 0) & ~hidden
    edge = MB.ink(np.where(hidden, np.inf, zb), np.where(hidden, -1, pb), np.where(hidden, -1, ob), hidden,
                  3 * scale) & drawn | (MB.ink(zb, pb, ob, solid, 3 * scale) & drawn)
    lay = np.zeros(zb.shape + (4,), np.uint8)
    for oi, (pi, kind) in owner.items():
        cols = MB.colours(who[pi]['sp'])
        m = (ob == oi) & drawn
        for n, ix in MB.PIX.items():
            mm = m & (pb == ix)
            if mm.any():
                lay[mm, :3] = cols[n]
    lay[drawn, 3] = 255
    lay[edge, :3] = MB.INK
    lay[edge, 3] = 255
    img = bg.resize((W_, H_), Image.LANCZOS)
    L = Image.fromarray(lay, 'RGBA').resize((W_, H_), Image.LANCZOS)
    img.alpha_composite(L)
    # the house heads at the heads' depth (a solid nearer than the head hides it: the door leaf, the desk)
    zfull = np.where(hidden & ~solid, np.inf, zb)
    for person, k, f, P, R, oi in bodies:
        head, _ = BD.house_head(cam, k, person['sp'], neck=False)
        own = (ob == oi) | np.isin(ob, [o for o, (pi, kd) in owner.items() if who[pi] is person])
        BD.lay_head(img, head, np.where(own, np.inf, zfull), cam.depth(tuple(k['head'])), scale)
    used = np.unique(np.concatenate([R['T'].ravel() for _, _, _, _, R, _ in bodies])) if bodies else []
    faults = {}
    for person, k, f, P, R, oi in bodies:
        hit = MB.crossings(P, [s for s in solids], np.unique(R['T']))
        if hit:
            faults[person['sp']['who']] = hit
    for person in who:
        g = person.get('gaps', (0, 0))
        if g[0] > 0.02 or g[1] > 0.03:
            faults.setdefault(person['sp']['who'], {})['reach (hand m, foot m)'] = g
    out = I.overlay(img, t)
    _ = used
    return out.convert('RGB'), faults


W_, H_ = 1080, 1920
SURFACES = [(0.83, 0.33, 0.57, 3.09, 3.27), (0.76, -0.95, 0.95, 2.51, 3.49)]   # the phone base, the desk top
SEAT0 = SEAT = (0.55, -0.31, 0.31, 3.75 - 0.29, 3.75 + 0.29)    # the leather chair's cushion top and extent (midterminal_set)


class _ScaledCam:
    """A camera that projects onto a frame `scale` times bigger (opening_mask multiplies by B.SS, which is 1 here)."""
    def __init__(self, cam, scale):
        self.cam, self.scale = cam, scale

    def project(self, p):
        (x, y), k = self.cam.project(p)
        return (x * self.scale, y * self.scale), k


def posted_frame(t):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', POSTED, '-frames:v', '1', '-f', 'rawvideo',
                        '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return Image.frombytes('RGB', (1080, 1920), p)


def _frame_job(t):
    import humancheck as HC
    HC.frame_begin()
    im, faults = frame(t)
    body = list(HC.frame_end(t))                  # the house body check on what was drawn (the house heads)
    for who, hit in faults.items():               # and the model body's own: points inside a solid
        for nm, n in hit.items():
            if not nm.startswith('reach'):
                thing = 'the desk chair' if nm.startswith('set@0.00,3.8') or nm.startswith('set@0.00,3.9') or \
                    nm.startswith('set@0.00,4.') else nm
                body.append((t, who, 'solid', f'body points inside {thing} ({n} points)'))
    return t, im.resize((540, 960), Image.LANCZOS), faults, body


def clip(t0, t1, out, fps=12):
    """Side by side at phone size (each half 540 x 960): the posted film | the model bodies; 12 frames a second."""
    tmp = out + '.frames'
    os.makedirs(tmp, exist_ok=True)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.4f}', '-t', f'{t1 - t0:.4f}', '-i', POSTED,
                        '-vf', 'fps=12,scale=540:960', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True, check=True).stdout
    n_post = len(p) // (540 * 960 * 3)
    n = int(round((t1 - t0) * fps))
    t_start = time.time()
    log = []
    film()
    import multiprocessing as mp
    ts = [t0 + (i + 0.5) / fps for i in range(n)]
    with mp.get_context('fork').Pool(int(os.environ.get('MB_PROCS', '3'))) as pool:
        done = pool.imap(_frame_job, ts)
        rows = list(done)
    import humancheck as HC
    hc = HC.Writer(os.path.basename(out))
    for i, (t, im, faults, body) in enumerate(rows):
        hc.frame(t, body)
        left = Image.frombytes('RGB', (540, 960), p[min(i, n_post - 1) * 540 * 960 * 3:(min(i, n_post - 1) + 1) * 540 * 960 * 3])
        s = Image.new('RGB', (1080, 960))
        s.paste(left, (0, 0))
        s.paste(im, (540, 0))
        s.save(os.path.join(tmp, f'{i:04d}.png'))
        if faults:
            log.append((round(t, 2), faults))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                    '-ss', f'{t0:.4f}', '-t', f'{t1 - t0:.4f}', '-i', POSTED,
                    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23',
                    '-c:a', 'aac', '-shortest', out], check=True)
    print('frames', n, 'seconds', round(time.time() - t_start), 'faults', log[:20], 'fault frames', len(log))
    notes = os.path.join(ROOT, 'notes', 'proposals', 'model-body-all.md')
    hc.finish(out, notes=open(notes).read())
    return log


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'still':
        t0 = time.time()
        im, faults = frame(float(a[1]))
        im.save(a[2])
        print('seconds', round(time.time() - t0, 1), 'crossings', faults or 0)
    elif a[0] == 'clip':
        clip(float(a[1]), float(a[2]), a[3])
