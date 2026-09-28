"""Clothes made over a bent body (rig.py), for any character: a top (jumper, T-shirt, pyjama top) and
trousers. The cloth is the body's surface swollen by the cloth's thickness; loose cloth bridges hollows and
hides small bumps, hangs straight down from where it hangs, and is cut off at the hem, cuffs and collar.
"""
import functools

import numpy as np

import rig
from rig import unit

TORSO = {'hips', 'chest', 'head', 'thigh.L', 'thigh.R'}


def top(b, pose, J, spec):
    """A top made over the bent body b (rig.Body) in pose, J its joints (rig.Pose.joints). spec keys:
      thick     cloth thickness over the skin
      bridge    loose cloth spans hollows narrower than this (0: follows the body closely)
      smooth    and hides bumps smaller than this
      drape     how steeply it tucks back in under an overhang (the bust); None: no drape
      hem       how far below the hips' joint it ends; cuff: how far past the wrist the sleeves end
      collar    ('roll', [(height, ring radius, tube radius), ...]) or ('crew', opening radius, band radius)
      voxel
    Returns (lo, d, voxel, part) with part 0 body, 1 right sleeve, 2 left sleeve."""
    Vw = b.skin(pose)
    vox = spec['voxel']
    hem = J['spine05'][1] - spec['hem']
    names = TORSO | {'upperarm.R', 'forearm.R', 'upperarm.L', 'forearm.L'}
    sel = np.isin(b.label, [b.piece_names.index(n) for n in names if n in b.piece_names])
    sel[:] &= np.isin(np.arange(len(Vw)), b.skin_idx) & (Vw[:, 1] > hem - 0.02) & (Vw[:, 1] < J['neck02'][1] + 0.04)
    lo = Vw[sel].min(0) - 0.05
    hi = Vw[sel].max(0) + 0.05
    for s in ('R', 'L'):  # the cuffs reach a little past the wrists
        lo = np.minimum(lo, J['wrist.' + s] - 0.06)
        hi = np.maximum(hi, J['wrist.' + s] + 0.06)
    n = np.round((hi - lo) / vox).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * vox, vox)
    part = b.part_map(Vw, lo, d.shape, vox, [TORSO, {'upperarm.R', 'forearm.R'}, {'upperarm.L', 'forearm.L'},
                                                  {'hand.R'}, {'hand.L'}, {'head'}])

    @functools.lru_cache(maxsize=None)
    def region_cached(ids):
        return region(list(ids))

    def region(ids):
        """Smooth signed distance to where the body is made of these parts (negative inside); measured at
        half resolution, which is plenty for cutting cloth."""
        from scipy import ndimage
        m = np.isin(part[::2, ::2, ::2], ids)
        r = (ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)) * 2 * vox
        return ndimage.zoom(r.astype(np.float32), np.array(part.shape) / np.array(m.shape), order=1)[
            :part.shape[0], :part.shape[1], :part.shape[2]]
    f = d - spec['thick']
    del d
    # the body of the jumper is loose: it bridges hollows (between the breasts, the small of the back) rather
    # than following the skin into them (the shape closed up by a 3 cm ball), hides small bumps (thick knit
    # over a bra: rounded off by a 1.5 cm ball), and hangs straight down from the bust and shoulder blades.
    # The sleeves keep closer to the arm (and don't drape into bat wings).
    # (these broad shapes are worked out at half resolution, then brought back to the full grid)
    from scipy import ndimage
    reg = region_cached((0,))
    torso = np.maximum(f, reg)[::2, ::2, ::2]   # the body of the jumper alone (a smooth cut, no jumps)
    v2 = 2 * vox
    r = spec['bridge']
    torso = rig.robust_distance(rig.robust_distance(torso - r, v2) + r, v2)
    r = spec['smooth']
    torso = rig.robust_distance(rig.robust_distance(torso + r, v2) - r, v2)
    torso = rig.drape(torso, v2, spec['drape'])
    torso = ndimage.zoom(torso, np.array(f.shape) / np.array(torso.shape), order=1)[
        :f.shape[0], :f.shape[1], :f.shape[2]]
    w = np.clip(-reg / 0.02, 0, 1)
    f = w * torso + (1 - w) * np.minimum(f, torso)
    del torso, w
    axes = [lo[q] + np.arange(n[q]) * vox for q in range(3)]

    def window(c, r):
        """The part of the grid within r of c: its slices and coordinates (broadcastable)."""
        i0 = [max(int((c[q] - r - lo[q]) / vox), 0) for q in range(3)]
        i1 = [min(int((c[q] + r - lo[q]) / vox) + 1, n[q]) for q in range(3)]
        sl = tuple(slice(i0[q], i1[q]) for q in range(3))
        return sl, (axes[0][sl[0]][:, None, None], axes[1][sl[1]][None, :, None], axes[2][sl[2]][None, None, :])

    # cuffs: the sleeve ends just past the wrist, over the heel of the hand (cut only where the body is hand)
    for s, hid in (('R', 3), ('L', 4)):
        wr, el = J['wrist.' + s], J['elbow.' + s]
        fd = unit(wr - el)
        c = wr + fd * spec['cuff']
        sl, (X, Y, Z) = window(wr, 0.25)
        beyond = -((X - c[0]) * fd[0] + (Y - c[1]) * fd[1] + (Z - c[2]) * fd[2])
        f[sl] = rig.smax(f[sl], -np.maximum(beyond, region_cached((hid,))[sl] - 0.03), 0.004)
    sl, _ = window(J['head'], 0.25)
    f[sl] = rig.smax(f[sl], -(region_cached((5,))[sl] - 0.02), 0.004)            # nothing on her head
    # the hem, round her hips
    j1 = min(int((hem + 0.02 - lo[1]) / vox) + 1, n[1])
    # (only the body of the top: arms hanging down past the hips keep their sleeves)
    f[:, :j1] = np.where(part[:, :j1] == 0, rig.smax(f[:, :j1], hem - axes[1][:j1][None, :, None], 0.006), f[:, :j1])
    # the collar: take the cloth off her neck and head, then the collar itself
    # (the collar follows the upper body, not the neck: looking down tips the neck forward, and the cut would
    # then take away arms folded in front)
    nb, na = J['neck01'], unit(J['neck01'] - J['spine02'])
    sl, (X, Y, Z) = window(nb, 0.30)
    g = f[sl]
    ax = (X - nb[0]) * na[0] + (Y - nb[1]) * na[1] + (Z - nb[2]) * na[2]
    rad = np.sqrt(np.maximum((X - nb[0]) ** 2 + (Y - nb[1]) ** 2 + (Z - nb[2]) ** 2 - ax ** 2, 0))
    kind = spec['collar'][0]
    if kind == 'roll':      # a roll neck: rolls of knit round the neck, the neck coming out of the middle
        g = rig.smax(g, -np.maximum(-(ax + 0.005), rad - 0.11), 0.006)
        for h, R0, r in spec['collar'][1]:
            g = rig.smin(g, np.sqrt((rad - R0) ** 2 + (ax - h) ** 2) - r, 0.012)
        g = rig.smax(g, -np.maximum(rad - 0.052, -ax), 0.004)
    else:                   # a crew neck: a round opening at the base of the neck, edged with a soft band
        _, R0, r = spec['collar']
        g = rig.smax(g, -np.maximum(-(ax + 0.012), rad - 0.11), 0.004)
        g = rig.smax(g, -np.maximum(rad - (R0 - 0.004), -(ax + 0.03)), 0.003)   # the opening itself
        ring = np.sqrt((rad - R0) ** 2 + (ax + 0.012) ** 2) - r
        g = rig.smin(g, ring, 0.004)
    f[sl] = g
    f = f.astype(np.float32)
    knit_part = np.array([0, 1, 2, 1, 2, 0], np.float32)[np.maximum(part, 0)]  # hands count as their sleeves
    return lo, f, vox, knit_part



def bottoms(b, pose, J, spec, lowest=0.55):
    """Slim trousers (or tights) from under the top's hem down to `lowest` (metres above the floor)."""
    Vw = b.skin(pose)
    vox = 0.004
    top_y = J['spine05'][1] - spec['hem'] + 0.04
    sel = np.isin(np.arange(len(Vw)), b.skin_idx) & (Vw[:, 1] < top_y + 0.02) & (Vw[:, 1] > 0.55)
    sel &= np.isin(b.label, [b.piece_names.index(n) for n in ('hips', 'thigh.L', 'thigh.R', 'shin.L', 'shin.R')])
    lo, hi = Vw[sel].min(0) - 0.03, Vw[sel].max(0) + 0.03
    n = np.round((hi - lo) / vox).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * vox, vox) - 0.004
    Y = (lo[1] + np.arange(n[1]) * vox)[None, :, None]
    d = rig.smax(d, Y - top_y, 0.004)
    return lo, rig.robust_distance(d.astype(np.float32), vox), vox


