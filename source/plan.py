#!/usr/bin/env python3
"""plan: the film's world drawn once, in metres (guides/film-quality-rules.md, rule 1), checked and sketched.

Why: Power Crime Action built each room and shot on its own, so doors led nowhere, people stood in furniture and
shots disagreed about where things were. Prepper Minister's plan file (source/prepper_plan.py) fixed that for one film;
this is the same plan as a shared format, so every film has one and pre-flight checks it.

A film gives PLAN: a module or a dict with (plan view: x east, z north, y up; metres; facings in degrees, 0 = north,
90 = east):
  ROOMS     {name: (x0, z0, x1, z1)}                       every place (square, room, corridor)
  OPENINGS  {name: dict(wall=('x', value) or ('z', value), span=(a0, a1), sill=, head=
              [, hinge=, swings=room][, to=])}
              every door, window and gap; `to` names what an opening onto the outside shows (rule 2: never a flat
              colour), e.g. to='back garden'
  THINGS    {name: dict(at=(x, z), size=(along x, along z, height: as it stands), facing=deg[, y=height off the floor][, on=thing]
              [, solid=False, why=...])}                   furniture, fixtures, set dressing (rule 22)
  PEOPLE    {label: dict(at=(x, z), facing=deg, who=name[, on=thing])}   where each person stands, which way they face
  CAMS      {shot: dict(pos=(x, y, z), look=(x, y, z)) or dict(path=[...], look=) or dict(orbit=..., look_y=)}
  optional: CEIL (2.6), WALL_T, LOOKS {room: dict(floor=rgb, wall=rgb)} (the colours a portal shows, rule 2),
            GROUPS {group: dict(arriving=, stopped=, leaving=)} (rule 9), FRAMING {shot: dict(hook=, beats=)} (rule 10),
            SHOT_MARKS {shot: [people marks]} (rule 38: front on unless the film's THREE_QUARTER_OK says why)
A CAMS key matches a shot by name ('s6') or by its number (6).

    python3 source/plan.py FILM sketch OUT.jpg      the top-down sketch (rooms, doors, things, people, cameras)
    python3 source/plan.py FILM check               the plan's faults (pre-flight runs this too)
"""
import importlib
import math
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FONT = FONT_B = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')   # the one plain font kept in the repo
PASSAGE = 0.1                 # an opening whose sill is below this is walked through (a door or a gap)


class Plan:
    """The film's plan read the same way whether it is a module or a dict."""
    def __init__(self, src):
        get = (lambda k, d=None: src.get(k, d)) if isinstance(src, dict) else (lambda k, d=None: getattr(src, k, d))
        self.rooms = dict(get('ROOMS', {}) or {})
        self.openings = dict(get('OPENINGS', {}) or {})
        self.things = dict(get('THINGS', {}) or {})
        self.people = dict(get('PEOPLE', {}) or {})
        self.cams = dict(get('CAMS', {}) or {})
        self.ceil = get('CEIL', 2.6)
        self.wall_t = get('WALL_T', 0.1)
        self.looks = dict(get('LOOKS', {}) or {})
        self.groups = dict(get('GROUPS', {}) or {})
        self.framing = dict(get('FRAMING', {}) or {})
        self.src = src

    def room_of(self, x, z, pad=0.0):
        for name, (x0, z0, x1, z1) in self.rooms.items():
            if x0 - pad <= x <= x1 + pad and z0 - pad <= z <= z1 + pad:
                return name
        return None

    def sides(self, name):
        """The two spaces an opening joins: (room or None on the low side, room or None on the high side)."""
        o = self.openings[name]
        ax, v = o['wall']
        m = (o['span'][0] + o['span'][1]) / 2
        if ax == 'x':
            return self.room_of(v - 0.2, m), self.room_of(v + 0.2, m)
        return self.room_of(m, v - 0.2), self.room_of(m, v + 0.2)

    def cam_for_shot(self, shot):
        if shot in self.cams:
            return self.cams[shot]
        n = re.sub(r'\D', '', str(shot))
        for k, c in self.cams.items():
            if n and re.sub(r'\D', '', str(k)) == n:
                return c
        return None


def of(film):
    """The film's Plan, or None."""
    src = getattr(film, 'PLAN', None)
    if isinstance(src, str):
        src = importlib.import_module(src)
    return Plan(src) if src is not None else None


def tilt(th):
    """How far a thing is turned off the plan's axes (degrees, -45 to 45): its size is given along x and z as it
    stands (prepper_plan.py's way), so a sink run facing 90 is not turned again; an armchair facing 250 is 20 off."""
    return ((th.get('facing', 0) + 45) % 90) - 45


def footprint(th):
    """A thing's plan footprint as an axis box (x0, z0, x1, z1)."""
    (cx, cz), (sx, sz, _) = th['at'], th['size']
    a = math.radians(tilt(th))
    w = abs(sx * math.cos(a)) + abs(sz * math.sin(a))
    d = abs(sx * math.sin(a)) + abs(sz * math.cos(a))
    return (cx - w / 2, cz - d / 2, cx + w / 2, cz + d / 2)


def corners(th):
    """A thing's four plan corners."""
    (cx, cz), (sx, sz, _) = th['at'], th['size']
    a = math.radians(tilt(th))
    out = []
    for u, v in ((-sx / 2, -sz / 2), (sx / 2, -sz / 2), (sx / 2, sz / 2), (-sx / 2, sz / 2)):
        out.append((cx + u * math.cos(a) + v * math.sin(a), cz - u * math.sin(a) + v * math.cos(a)))
    return out


def _in_poly(p, poly):
    inside = False
    for (x1, z1), (x2, z2) in zip(poly, poly[1:] + poly[:1]):
        if (z1 > p[1]) != (z2 > p[1]) and p[0] < x1 + (p[1] - z1) * (x2 - x1) / (z2 - z1):
            inside = not inside
    return inside


def _pt_seg(p, a, b):
    ax, az, bx, bz = a[0], a[1], b[0], b[1]
    dx, dz = bx - ax, bz - az
    L = dx * dx + dz * dz or 1e-12
    u = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - az) * dz) / L))
    return math.hypot(p[0] - ax - u * dx, p[1] - az - u * dz)


def _poly_dist(p, poly):
    """From a plan point to a polygon's outline; 0 inside it."""
    if _in_poly(p, poly):
        return 0.0
    return min(_pt_seg(p, a, b) for a, b in zip(poly, poly[1:] + poly[:1]))


def gap(A, B):
    """The true plan gap between two THINGS in metres (0 when they meet or overlap): turned boxes by their corners,
    round=True things (a round chair, a table) as circles of diameter size[0]."""
    ra, rb = A.get('round'), B.get('round')
    if ra and rb:
        return max(0.0, math.dist(A['at'], B['at']) - A['size'][0] / 2 - B['size'][0] / 2)
    if ra or rb:
        c, p = (A, B) if ra else (B, A)
        return max(0.0, _poly_dist(c['at'], corners(p)) - c['size'][0] / 2)
    pa, pb = corners(A), corners(B)
    if any(_in_poly(q, pb) for q in pa) or any(_in_poly(q, pa) for q in pb):
        return 0.0
    d = min(min(_pt_seg(q, a, b) for a, b in zip(pb, pb[1:] + pb[:1])) for q in pa)
    return min(d, min(min(_pt_seg(q, a, b) for a, b in zip(pa, pa[1:] + pa[:1])) for q in pb))


def heights(th):
    y = th.get('y', 0.0)
    return y, y + th['size'][2]


def _overlap(a, b, pad=0.0):
    return min(a[2], b[2]) - max(a[0], b[0]) > pad and min(a[3], b[3]) - max(a[1], b[1]) > pad


def _passage_box(o, depth=0.45):
    """The floor area just either side of a doorway that must be kept clear to walk through."""
    ax, v = o['wall']
    a0, a1 = o['span']
    return (v - depth, a0, v + depth, a1) if ax == 'x' else (a0, v - depth, a1, v + depth)


def faults(film):
    """Rule 1: the plan exists, joins up, and every shot reads from it. Returns faults as lines."""
    P = of(film)
    if P is None:
        return ['plan (rule 1): the film has no PLAN (rooms, openings, things, people and cameras in metres; '
                'source/plan.py, the template)']
    out = []
    if not P.rooms:
        out.append('plan: no ROOMS')
    names = list(P.rooms)
    for i, a in enumerate(names):
        x0, z0, x1, z1 = P.rooms[a]
        if x1 <= x0 or z1 <= z0:
            out.append(f'plan: room {a} has no size')
        for b in names[i + 1:]:
            if _overlap(P.rooms[a], P.rooms[b], 0.01):
                out.append(f'plan: rooms {a} and {b} overlap')
    for n, o in P.openings.items():
        ax, v = o['wall']
        on_wall = any((ax == 'x' and (abs(x0 - v) < 0.02 or abs(x1 - v) < 0.02) and z0 - 0.02 <= o['span'][0] and
                       o['span'][1] <= z1 + 0.02) or
                      (ax == 'z' and (abs(z0 - v) < 0.02 or abs(z1 - v) < 0.02) and x0 - 0.02 <= o['span'][0] and
                       o['span'][1] <= x1 + 0.02) for x0, z0, x1, z1 in P.rooms.values())
        if not on_wall:
            out.append(f'plan: opening {n} is not in any room\'s wall')
        if not o.get('sill', 0.0) < o.get('head', 2.0) <= P.ceil + 0.01:
            out.append(f'plan: opening {n}: sill {o.get("sill")} and head {o.get("head")} (ceiling {P.ceil})')
        lo, hi = P.sides(n)
        if lo is None and hi is None:
            out.append(f'plan: opening {n} joins nothing on either side')
        elif (lo is None or hi is None) and not o.get('to'):
            out.append(f'plan: opening {n} looks outside but says nothing of what is seen there (give it to=..., '
                       f'rule 2: never a flat colour)')
    for n, th in P.things.items():
        cx, cz = th['at']
        if th.get('outside'):
            continue
        r = P.room_of(cx, cz)
        if r is None:
            out.append(f'plan: {n} at ({cx}, {cz}) is in no room')
            continue
        fx0, fz0, fx1, fz1 = footprint(th)
        x0, z0, x1, z1 = P.rooms[r]
        if fx0 < x0 - 0.03 or fz0 < z0 - 0.03 or fx1 > x1 + 0.03 or fz1 > z1 + 0.03:
            out.append(f'plan: {n} pokes through the walls of the {r}')
        if heights(th)[0] < 0.3 and th.get('solid', True):
            for on, o in P.openings.items():
                if o.get('sill', 0.0) < PASSAGE and _overlap(footprint(th), _passage_box(o), 0.02) and \
                        r in P.sides(on):
                    out.append(f'plan: {n} stands in the way of the {on}')
    tn = list(P.things)
    for i, a in enumerate(tn):
        A = P.things[a]
        for b in tn[i + 1:]:
            Bt = P.things[b]
            if A.get('on') == b or Bt.get('on') == a:
                continue
            if A.get('part_of') and A.get('part_of') == Bt.get('part_of'):   # pieces of one thing (a ring desk)
                continue
            ya, yb = heights(A), heights(Bt)
            if min(ya[1], yb[1]) - max(ya[0], yb[0]) <= 0.01:
                continue
            need = max(A.get('clear', 0.0), Bt.get('clear', 0.0))   # a minimum gap either asks for (metres)
            g = gap(A, Bt)
            if need > 0 and g < need - 1e-6:
                out.append(f'plan: {a} and {b} are {g:.2f} m apart; {need:.2f} m needed (clear=)')
            elif need <= 0 and g <= 0 and _overlap(footprint(A), footprint(Bt), 0.01):
                out.append(f'plan: {a} and {b} stand in each other')
    for n, p in P.people.items():
        x, z = p['at']
        if P.room_of(x, z, 0.05) is None and not p.get('outside'):
            out.append(f'plan: {n} stands in no room')
        if 'facing' not in p:
            out.append(f'plan: {n} has no facing (which way they face)')
        for tname, th in P.things.items():
            if p.get('on') == tname or not th.get('solid', True) or heights(th)[0] > 1.6:
                continue
            fx0, fz0, fx1, fz1 = footprint(th)
            if fx0 + 0.05 < x < fx1 - 0.05 and fz0 + 0.05 < z < fz1 - 0.05:
                out.append(f'plan: {n} stands inside the {tname} (sitting on it? give on="{tname}")')
    for k, c in P.cams.items():
        pts = [c['pos']] if 'pos' in c else list(c.get('path', []))
        if 'look' not in c and 'look_y' not in c:
            out.append(f'plan: camera {k} looks at nothing (give look=)')
        for q in pts:
            if P.room_of(q[0], q[2], 0.05) is None and not c.get('outside'):
                out.append(f'plan: camera {k} stands at ({q[0]}, {q[2]}), in no room')
                break
    out += front_faults(film, P)
    missing = [s[0] for s in getattr(film, 'SHOTS', []) if P.cam_for_shot(s[0]) is None]
    if missing:
        out.append(f'plan: no camera in the plan for shot(s) {", ".join(map(str, missing))}')
    for g, ph in P.groups.items():
        for phase in ('arriving', 'stopped', 'leaving'):
            if not ph.get(phase):
                out.append(f'plan (rule 9): group {g} has no plan for {phase}')
    return out


def front_faults(film, P=None):
    """Rule 38: each person faces the lens within about 25 degrees, unless the film lists that shot and mark in
    THREE_QUARTER_OK with its reason. Reads the plan's SHOT_MARKS {shot: [people marks]} (said out loud if missing)."""
    P = P or of(film)
    marks = (P.src.get('SHOT_MARKS') if isinstance(P.src, dict) else getattr(P.src, 'SHOT_MARKS', None)) or {}
    if P.people and P.cams and not marks:
        return ['plan (rule 38): no SHOT_MARKS {shot: [people marks]}, so the front-on check cannot run']
    ok = {(str(a), b): why for a, b, *why in getattr(film, 'THREE_QUARTER_OK', ())}
    out = []
    for (a, b), why in ok.items():
        if not why or not str(why[0]).strip():
            out.append(f'plan (rule 38): THREE_QUARTER_OK {a} {b} gives no reason')
    for shot, labels in marks.items():
        c = P.cam_for_shot(shot)
        if c is None or 'pos' not in c:
            continue
        for lb in labels:
            p = P.people.get(lb)
            if p is None:
                out.append(f'plan (rule 38): SHOT_MARKS {shot}: no person mark {lb}')
                continue
            to_cam = math.degrees(math.atan2(c['pos'][0] - p['at'][0], c['pos'][2] - p['at'][1]))
            off = abs((to_cam - p['facing'] + 540) % 360 - 180)
            if off > 25 and (str(shot), lb) not in ok:
                kind = 'three-quarter' if off < 60 else 'side on' if off < 120 else 'from behind'
                out.append(f'plan (rule 38): shot {shot}: {lb} is seen {kind} ({off:.0f} degrees off the lens): '
                           f'turn them or the camera, or list it in THREE_QUARTER_OK with the reason')
    return out


# ------------------------------------------------------------------------------------------------ the sketch
def sketch(film, out):
    """The plan from above, to show Sam: rooms (floor colours from LOOKS), walls with their openings, doors and their
    swing, windows, every thing, every person (a dot with a facing arrow) and every camera (a numbered cone)."""
    P = of(film)
    xs = [v for r in P.rooms.values() for v in (r[0], r[2])]
    zs = [v for r in P.rooms.values() for v in (r[1], r[3])]
    for c in P.cams.values():
        for q in ([c['pos']] if 'pos' in c else c.get('path', [])):
            xs.append(q[0])
            zs.append(q[2])
    X0, X1, Z0, Z1 = min(xs) - 1.6, max(xs) + 1.6, min(zs) - 0.8, max(zs) + 0.8
    S = min(140, 1900 / max(X1 - X0, Z1 - Z0))
    W, H = int((X1 - X0) * S), int((Z1 - Z0) * S) + 60
    im = Image.new('RGB', (W, H), (250, 248, 242))
    d = ImageDraw.Draw(im)
    pt = lambda x, z: (round((x - X0) * S), round((Z1 - z) * S))
    f, fb = ImageFont.truetype(FONT, max(12, int(S * 0.13))), ImageFont.truetype(FONT_B, max(14, int(S * 0.16)))
    ink = (30, 30, 34)
    palette = [(214, 200, 168), (196, 196, 190), (226, 214, 190), (190, 210, 196), (210, 196, 214)]
    for i, (n, (x0, z0, x1, z1)) in enumerate(P.rooms.items()):
        col = P.looks.get(n, {}).get('floor', palette[i % len(palette)])
        d.rectangle([pt(x0, z1), pt(x1, z0)], fill=tuple(col))
        d.text(pt((x0 + x1) / 2, z1 - 0.25), n.upper(), font=fb, fill=ink, anchor='mm')
    for n, (x0, z0, x1, z1) in P.rooms.items():
        for wall, a0, a1 in ((('z', z0), x0, x1), (('z', z1), x0, x1), (('x', x0), z0, z1), (('x', x1), z0, z1)):
            cuts = sorted(o['span'] for o in P.openings.values()
                          if tuple(o['wall']) == wall and o.get('sill', 0) < PASSAGE)
            pos = a0
            for c0, c1 in cuts + [(a1, a1)]:
                c0, c1 = max(c0, a0), min(c1, a1)
                if c0 > pos:
                    seg = [(pos, wall[1]), (c0, wall[1])] if wall[0] == 'z' else [(wall[1], pos), (wall[1], c0)]
                    d.line([pt(*seg[0]), pt(*seg[1])], fill=ink, width=max(3, int(S * 0.07)))
                pos = max(pos, c1)
    for n, o in P.openings.items():
        ax, v = o['wall']
        a0, a1 = o['span']
        if o.get('sill', 0) >= PASSAGE:
            box = [pt(v - 0.07, a1), pt(v + 0.07, a0)] if ax == 'x' else [pt(a0, v + 0.07), pt(a1, v - 0.07)]
            d.rectangle(box, fill=(150, 200, 235), outline=ink, width=2)
        if 'hinge' in o:
            h = o['hinge']
            other = a1 if abs(h - a0) < 1e-6 else a0
            leaf = abs(other - h)
            room = o.get('swings')
            sgn = 1
            if room and room in P.rooms:
                rx0, rz0, rx1, rz1 = P.rooms[room]
                sgn = 1 if ((rz0 + rz1) / 2 if ax == 'z' else (rx0 + rx1) / 2) > v else -1
            tip = (h, v + sgn * leaf) if ax == 'z' else (v + sgn * leaf, h)
            hp = (h, v) if ax == 'z' else (v, h)
            d.line([pt(*hp), pt(*tip)], fill=(120, 72, 40), width=4)
        mid = (a0 + a1) / 2
        lab = pt(mid, v) if ax == 'z' else pt(v, mid)
        d.text((lab[0], lab[1] + 4), n + (f' (to {o["to"]})' if o.get('to') else ''), font=f, fill=(90, 60, 30),
               anchor='mt')
    for n, th in P.things.items():
        c = [pt(*q) for q in corners(th)]
        d.polygon(c, fill=(170, 140, 110) if th.get('solid', True) else (200, 190, 175), outline=ink)
        d.text(pt(*th['at']), n, font=f, fill=ink, anchor='mm')
    for n, p in P.people.items():
        x, z = p['at']
        a = math.radians(p.get('facing', 0))
        c = pt(x, z)
        r = max(5, int(S * 0.12))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(200, 60, 60), outline=ink)
        d.line([c, pt(x + 0.4 * math.sin(a), z + 0.4 * math.cos(a))], fill=(200, 60, 60), width=3)
        d.text((c[0], c[1] + r + 2), n, font=f, fill=(140, 30, 30), anchor='mt')
    for k, cm in P.cams.items():
        pts = [cm['pos']] if 'pos' in cm else list(cm.get('path', []))
        if 'orbit' in cm:                                     # a camera going round: its loop
            o = cm['orbit']
            (ox, oz), rx, rz = o['centre'], o['rx'], o['rz']
            d.ellipse([pt(ox - rx, oz + rz), pt(ox + rx, oz - rz)], outline=(40, 90, 200), width=2)
            d.text(pt(ox + rx * 0.7, oz - rz * 0.7), f'{k} (loop)', font=fb, fill=(20, 50, 140), anchor='mm')
        if not pts:
            continue
        if len(pts) > 1:
            d.line([pt(q[0], q[2]) for q in pts], fill=(40, 90, 200), width=2)
        q = pts[0]
        look = cm.get('look', (q[0], 0, q[2] + 1))
        a = math.atan2(look[0] - q[0], look[2] - q[2])
        cone = [pt(q[0], q[2])] + [pt(q[0] + 0.7 * math.sin(a + s), q[2] + 0.7 * math.cos(a + s)) for s in (-0.35, 0.35)]
        d.polygon(cone, fill=(120, 160, 230), outline=(40, 90, 200))
        d.text(pt(q[0], q[2]), str(k), font=fb, fill=(20, 50, 140), anchor='mm')
    d.text((10, H - 50), f'{getattr(film, "NAME", "")}: the plan (1 square = 1 m)', font=fb, fill=ink)
    for x in range(math.ceil(X0), math.floor(X1) + 1):
        d.line([pt(x, Z1), pt(x, Z1 - 0.1)], fill=ink)
    im.save(out, quality=88)
    return out


def main():
    a = sys.argv[1:]
    film = importlib.import_module(a[0])
    if a[1] == 'sketch':
        print('sketch:', sketch(film, a[2]))
    else:
        fs = faults(film)
        print('\n'.join(fs) or 'plan: clean')


if __name__ == '__main__':
    main()
