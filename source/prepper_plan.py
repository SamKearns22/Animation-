#!/usr/bin/env python3
"""Prepper Minister: the house, drawn once, in metres (guides/film-quality-rules.md, rule 1).

Every shot reads its rooms, doors, windows, furniture, people and cameras from here; the 3D set and the film never
place anything on their own. Plan view: x runs east (screen right in shot 1 is east), z runs north (away from the
shot 1 camera), y is height. The living room's back (north) wall holds the hallway door; the kitchen lies to its west
through a wide opening; the hallway runs behind both rooms, with the front door at its east end.

    python3 source/prepper_plan.py sketch OUT.png      the top-down sketch for Sam (rooms, doors, cameras, who stands where)
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CEIL = 2.8
WALL_T = 0.12

ROOMS = {   # name: (x0, z0, x1, z1)
    'living room': (0.0, 0.0, 6.0, 5.4),
    'kitchen': (-5.6, 0.0, 0.0, 5.4),
    'hallway': (-5.6, 5.4, 6.0, 7.0),
}

# Openings in walls. wall: ('x', value) or ('z', value); span along the wall; sill and head heights.
OPENINGS = {
    'wide opening': dict(wall=('x', 0.0), span=(1.2, 4.0), sill=0.0, head=2.4),
    'living door': dict(wall=('z', 5.4), span=(2.13, 2.97), sill=0.0, head=2.04, hinge=2.13, swings='living room',
                        note='hinged on the left (west); booted open, it swings left and bangs the wall beside the drinks cabinet'),
    'kitchen door': dict(wall=('z', 5.4), span=(-1.62, -0.78), sill=0.0, head=2.04, hinge=-0.78, swings='kitchen'),
    'front door': dict(wall=('x', 6.0), span=(5.75, 6.65), sill=0.0, head=2.1),
    'living window': dict(wall=('x', 6.0), span=(0.9, 4.5), sill=0.3, head=2.5, note='grand window, floor to near ceiling'),
    'kitchen window': dict(wall=('x', -5.6), span=(1.5, 3.9), sill=0.95, head=2.4,
                           note='grand window over the sink run; the robots climb in over its sill'),
}

# Furniture and fixtures: centre (x, z), size along x, along z, height; facing (degrees, 0 = facing north/away).
THINGS = {
    # living room: forest green fitted carpet throughout
    'tv': dict(at=(3.0, 0.08), size=(1.45, 0.05, 0.84), y=0.72, facing=0, note='65-inch, on the media unit'),
    'media unit': dict(at=(3.0, 0.24), size=(2.0, 0.42, 0.5), facing=0),
    'sofa': dict(at=(3.0, 3.75), size=(2.4, 0.95, 0.85), facing=180, note='faces the TV; seat 0.45 m'),
    'coffee table': dict(at=(3.0, 2.2), size=(1.2, 0.6, 0.4), facing=0),
    'drinks cabinet': dict(at=(0.85, 5.17), size=(0.8, 0.45, 1.5), facing=180, note='left of the hallway door'),
    'watercolour': dict(at=(4.0, 5.39), size=(0.9, 0.02, 0.65), y=1.22, facing=180, note='Lake District fells, right of the door'),
    'armchair': dict(at=(5.15, 1.7), size=(0.85, 0.85, 0.95), facing=250, note='plush old-world, by the window'),
    'side table': dict(at=(4.55, 3.8), size=(0.45, 0.45, 0.55), facing=180),
    'floor lamp': dict(at=(5.6, 4.95), size=(0.35, 0.35, 1.6), facing=180),
    'plant': dict(at=(0.45, 0.45), size=(0.5, 0.5, 1.4), facing=0),
    # kitchen: large grey stone floor tiles, tiled splashback, slate-effect worktops
    'island': dict(at=(-2.8, 2.7), size=(2.4, 1.0, 0.92), facing=0, note='slate-effect top; the minigun, beans and water on it'),
    'north units': dict(at=(-3.7, 5.075), size=(3.8, 0.65, 0.92), facing=180, note='worktop, hob, wall cupboards above; the Alexa'),
    'sink run': dict(at=(-5.275, 2.7), size=(0.65, 4.1, 0.92), facing=90, note='under the kitchen window'),
    'tall units': dict(at=(-3.9, 0.325), size=(3.4, 0.65, 2.3), facing=0, note='fridge-freezer, two ovens, larder'),
    'stool 1': dict(at=(-3.6, 2.0), size=(0.4, 0.4, 0.75), facing=0),
    'stool 2': dict(at=(-1.3, 2.7), size=(0.4, 0.4, 0.75), facing=0),   # at the island's east end (25 Oct: south of
    #                                                          it, it stood where Andy kneels and robot 1 falls in shot 12)
    'alexa': dict(at=(-4.2, 5.05), size=(0.1, 0.1, 0.09), y=0.92, facing=180, note='Echo Dot, on the north worktop'),
    # hallway: well lit (pendant, fanlight over the front door), stairs along the north wall
    'stairs': dict(at=(-1.0, 6.55), size=(3.2, 0.9, 2.8), facing=90),
}

# Where people stand (plan, metres) and which way they face (degrees; 0 = north, 90 = east, 180 = south, 270 = west).
PEOPLE = {
    'andy sofa (1-4, 7, start of 8)': dict(at=(3.0, 3.6), facing=180, who='Andy'),
    'andy kitchen (6)': dict(at=(-1.3, 1.95), facing=300, who='Andy'),
    'andy aims (end of 8, 9)': dict(at=(2.95, 2.95), facing=355, who='Andy'),
    'wes enters (8)': dict(at=(2.55, 5.2), facing=180, who='Wes'),
    'wes at island (10)': dict(at=(-4.45, 2.7), facing=90, who='Wes'),
    'andy (11, 12)': dict(at=(-2.9, 1.85), facing=0, who='Andy'),
    'wes (12)': dict(at=(-2.7, 3.55), facing=180, who='Wes'),
}

ROBOTS = {   # robot: where it comes from and where it ends up. Every body stays where it falls.
    'robot A (8)': dict(at=(2.55, 5.95), arm='cannon', note='over Wes\'s shoulder in the hall; bolt to the head; falls back into the hall'),
    'robot B (9)': dict(at=(0.4, 2.4), arm='blade', note='lunges from the wide opening (screen left); shot; drops in the living room'),
    'robots C, D (10)': dict(at=(-6.0, 2.2), arm='cannon', note='at the kitchen window; shot through the glass; fall back outside'),
    # shot 12 (Sam's notes 3-8, 24 Oct). Every path stays clear of the camera's loop while the camera is near it.
    'robot 1 (12)': dict(at=(-2.05, 1.75), arm='blade', note='walks in from the lounge, comes at Andy, swipes over him as he '
                                                               'drops to his knees; he shoots its head off'),
    'robot 2 (12)': dict(at=(-0.7, 3.5), arm='blade', note='walks in from the lounge; Wes cuts it down'),
    'robot 3 (12)': dict(at=(-0.35, 2.7), arm='cannon', note='comes in from the lounge firing at Andy; he shoots it down'),
    'robot 4 (12)': dict(at=(-5.25, 2.3), arm='cannon', note='crawls in through the shot-out kitchen window; fires at Andy; '
                                                               'Wes riddles it'),
    'robot 5 (11, 12)': dict(at=(-1.3, 4.75), arm='cannon', note='the tin dents off it in the door (11); walks in firing at '
                                                                  'Wes, blown to pieces (12)'),
    'robot 6 (12)': dict(at=(0.15, 1.5), arm='cannon', note='Sam: under the wide opening, on the right; fires plasma, then '
                                                             'riddled by Wes'),
}

# Cameras: position (x, y, z) and the point looked at. A moving shot gives a path of positions.
CAMS = {
    1: dict(pos=(3.0, 1.15, 0.35), look=(3.0, 1.0, 3.7), note='mid shot, Andy on the sofa; door, cabinet, watercolour behind'),
    2: dict(pos=(3.0, 1.1, 1.5), look=(3.0, 1.0, 3.7), note='a bit closer'),
    3: dict(pos=(3.0, 1.1, 2.9), look=(3.0, 1.05, 3.75), note='extreme close-up'),
    4: dict(pos=(3.0, 1.15, 0.35), look=(3.0, 1.0, 3.7), note='as shot 1'),
    5: dict(pos=(-2.8, 1.45, 0.9), look=(-2.8, 0.95, 2.7), note='mid shot of the island, nobody in shot'),
    6: dict(path=[(-2.3, 1.42, 1.49), (-2.4, 1.3, 3.0), (-3.75, 1.12, 4.42)], look=(-4.2, 0.97, 5.05),
            note='Andy waist up from his left-front (24 Oct: the first start showed his back), then rides behind the '
                 'bolt to the Alexa (prepper.cam_for)'),
    7: dict(pos=(3.0, 1.1, 1.5), look=(3.0, 1.0, 3.7), note='as shot 2'),
    8: dict(path=[(3.0, 1.1, 1.5), (2.95, 1.4, 3.0), (2.75, 1.5, 3.75), (2.6, 1.55, 4.15)],
            look=(2.55, 1.4, 5.4), note='Sam, 24 Oct: the door is just behind Andy, slightly left; the camera passes over '
                                         'his (right) shoulder and arrives at the doorway; Andy, risen, just behind it'),
    9: dict(pos=(3.0, 1.15, 0.35), look=(3.0, 1.15, 5.4), note='wide (a wider lens), from the shot 1 spot'),
    10: dict(pos=(-0.6, 1.45, 2.7), look=(-4.5, 1.3, 2.7), note='mid shot: minigun on the island, window behind, units right'),
    11: dict(path=[(-1.9, 1.05, 1.7), (-1.5, 1.3, 3.2)], look=(-1.2, 1.4, 5.3), note='close on a tin, then follows it to the door'),
    12: dict(orbit=dict(centre=(-2.8, 2.7), rx=1.8, rz=1.85, y=1.6, turns=1.0, seconds=11.0, start_deg=-53.0), look_y=1.15,
             note='one full loop round Wes and Andy, slowed to 11 s (Sam, 24 Oct); it starts south-east of the island so '
                  'it sees Andy drop under the blade from the north-west, past Wes, not from behind Wes'),
}


def orbit_pos(t, o):
    """Camera on the shot 12 loop, t from 0 to o['seconds']: starts at `start_deg` (-90 = south of the island), goes
    round anticlockwise."""
    a = math.radians(o.get('start_deg', -90.0)) + 2 * math.pi * o['turns'] * t / o['seconds']
    return (o['centre'][0] + o['rx'] * math.cos(a), o['y'], o['centre'][1] + o['rz'] * math.sin(a))


def smooth(pts, n=16):
    """A Catmull-Rom curve through a camera path's points (the camera glides; it never turns a sharp corner)."""
    out = []
    ext = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            u = k / n
            out.append(tuple(0.5 * (2 * b + (-a + c) * u + (2 * a - 5 * b + 4 * c - e) * u * u
                                    + (-a + 3 * b - 3 * c + e) * u ** 3) for a, b, c, e in zip(p0, p1, p2, p3)))
    return out + [pts[-1]]


# --- the sketch ---------------------------------------------------------------------------------------------------
S = 118                     # pixels per metre
X0, Z1 = -6.3, 7.4          # the sketch's left edge (x) and top edge (z)
Z0 = -0.3                   # and bottom edge
W, H = int(13.2 * S), int((Z1 - Z0) * S) + 300


def P(x, z):
    return (round((x - X0) * S), round((Z1 - z) * S))


def font(px, bold=False):
    path = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else '')
    return ImageFont.truetype(path, px)


def sketch(out):
    im = Image.new('RGB', (W, H), (250, 248, 242))
    d = ImageDraw.Draw(im)
    floors = {'living room': (64, 104, 72), 'kitchen': (196, 196, 190), 'hallway': (226, 214, 190)}
    for name, (x0, z0, x1, z1) in ROOMS.items():
        d.rectangle([P(x0, z1), P(x1, z0)], fill=floors[name])
    ink = (30, 30, 34)
    # walls, with gaps at the openings
    for name, (x0, z0, x1, z1) in ROOMS.items():
        for wall, a0, a1 in ((('z', z0), x0, x1), (('z', z1), x0, x1), (('x', x0), z0, z1), (('x', x1), z0, z1)):
            cuts = sorted(o['span'] for o in OPENINGS.values() if o['wall'] == wall and o['sill'] < 0.5)
            pos = a0
            for c0, c1 in cuts + [(a1, a1)]:
                c0, c1 = max(c0, a0), min(c1, a1)
                if c0 > pos:
                    p0 = P(pos, wall[1]) if wall[0] == 'z' else P(wall[1], pos)
                    p1 = P(c0, wall[1]) if wall[0] == 'z' else P(wall[1], c0)
                    d.line([p0, p1], fill=ink, width=9)
                pos = max(pos, c1)
    # windows: pale blue glass bars on the wall
    for name, o in OPENINGS.items():
        if 'window' in name:
            a0, a1 = o['span']
            v = o['wall'][1]
            box = [P(v - 0.08, a1), P(v + 0.08, a0)]
            d.rectangle(box, fill=(150, 200, 235), outline=ink, width=3)
    # doors: leaf and swing arc
    for name in ('living door', 'kitchen door'):
        o = OPENINGS[name]
        h = o['hinge']
        other = o['span'][1] if h == o['span'][0] else o['span'][0]
        leaf = abs(other - h)
        zw = o['wall'][1]
        d.line([P(h, zw), P(h, zw - leaf)], fill=(120, 72, 40), width=6)
        bb = [P(h - leaf, zw + leaf), P(h + leaf, zw - leaf)]
        start = 90 if other > h else 0
        d.arc(bb, start, start + 90, fill=(120, 72, 40), width=2)
    o = OPENINGS['front door']
    d.line([P(6.0, o['span'][0]), P(6.0, o['span'][1])], fill=(120, 72, 40), width=10)
    # furniture
    cols = {'sofa': (232, 226, 214), 'armchair': (122, 40, 44), 'island': (60, 64, 70), 'north units': (150, 150, 146),
            'sink run': (150, 150, 146), 'tall units': (120, 120, 118), 'drinks cabinet': (110, 70, 42),
            'tv': (20, 20, 22), 'media unit': (122, 84, 52), 'coffee table': (130, 92, 58), 'watercolour': (120, 160, 200),
            'alexa': (40, 40, 44), 'stairs': (200, 180, 150), 'plant': (70, 130, 60), 'floor lamp': (60, 60, 60)}
    for name, th in THINGS.items():
        (cx, cz), (sx, sz, _) = th['at'], th['size']
        c = cols.get(name, (170, 140, 110))
        if name.startswith('stool') or name in ('plant', 'floor lamp'):
            r = sx / 2
            d.ellipse([P(cx - r, cz + r), P(cx + r, cz - r)], fill=c, outline=ink, width=2)
        else:
            d.rectangle([P(cx - sx / 2, cz + sz / 2), P(cx + sx / 2, cz - sz / 2)], fill=c, outline=ink, width=2)
    if True:   # the stairs' treads
        (cx, cz), (sx, sz, _) = THINGS['stairs']['at'], THINGS['stairs']['size']
        for i in range(1, 12):
            x = cx - sx / 2 + i * sx / 12
            d.line([P(x, cz - sz / 2), P(x, cz + sz / 2)], fill=ink, width=1)
    f_small, f_mid, f_big = font(19), font(23), font(30, True)

    def label(text, x, z, f=f_small, fill=ink, anchor='mm', box=True):
        px = P(x, z)
        if box:
            bb = d.textbbox(px, text, font=f, anchor=anchor)
            d.rectangle([bb[0] - 4, bb[1] - 3, bb[2] + 4, bb[3] + 3], fill=(255, 255, 255))
        d.text(px, text, font=f, fill=fill, anchor=anchor)

    for name, (xt, zt) in {'living room': (1.75, 1.15), 'kitchen': (-1.0, 1.15), 'hallway': (4.3, 6.68)}.items():
        label(name.upper(), xt, zt, f_big, box=True)
    label('forest green carpet', 1.75, 0.7, f_small)
    label('grey stone tiles', -1.0, 0.7, f_small)
    names = {'tv': 'TV', 'media unit': '', 'sofa': 'sofa', 'coffee table': 'coffee table', 'drinks cabinet': 'drinks\ncabinet',
             'watercolour': 'Lake District\nwatercolour', 'armchair': 'armchair', 'island': 'island', 'north units': 'worktop + hob',
             'sink run': 'sink\nrun', 'tall units': 'fridge, ovens, larder', 'alexa': 'Alexa', 'stairs': 'stairs',
             'side table': '', 'floor lamp': '', 'plant': '', 'stool 1': '', 'stool 2': ''}
    offs = {'tv': (1.05, 0.12), 'drinks cabinet': (0, -0.55), 'watercolour': (0, -0.42), 'alexa': (0.1, -0.35),
            'island': (0, 0), 'armchair': (0, -0.7), 'sofa': (-0.75, 0.0), 'north units': (-0.4, 0.0)}
    for name, th in THINGS.items():
        t = names.get(name, name)
        if t:
            dx, dz = offs.get(name, (0, 0))
            fill = (255, 255, 255) if name == 'island' else ink
            label(t, th['at'][0] + dx, th['at'][1] + dz, f_small, fill=fill, box=name != 'island')
    for name, o in OPENINGS.items():
        a = sum(o['span']) / 2
        v = o['wall'][1]
        txt = {'wide opening': 'wide\nopening', 'living door': 'door', 'kitchen door': 'door', 'front door': 'front\ndoor',
               'living window': 'grand\nwindow', 'kitchen window': 'grand\nwindow'}[name]
        x, z = (v, a) if o['wall'][0] == 'x' else (a, v)
        dx = {'living window': 0.55, 'kitchen window': -0.45, 'front door': 0.0, 'wide opening': 0.0}.get(name, 0)
        dz = {'living door': 0.3, 'kitchen door': 0.3, 'front door': 0.0}.get(name, 0)
        dx = {'living door': -0.8, 'kitchen door': 0.75}.get(name, dx)
        if name == 'front door':
            dx = -0.55
        label(txt, x + dx, z + dz, f_small)
    # the shot 12 loop and the shot 8 move
    o = CAMS[12]['orbit']
    pts = [P(*(lambda p: (p[0], p[2]))(orbit_pos(o['seconds'] * i / 120, o))) for i in range(121)]
    d.line(pts, fill=(200, 40, 40), width=3)
    path8 = [P(p[0], p[2]) for p in smooth(CAMS[8]['path'])]
    d.line(path8, fill=(200, 40, 40), width=3, joint='curve')
    path6 = [P(p[0], p[2]) for p in CAMS[6]['path']]
    d.line(path6, fill=(200, 40, 40), width=3)
    path11 = [P(p[0], p[2]) for p in CAMS[11]['path']]
    d.line(path11, fill=(200, 40, 40), width=3)

    def cam_icon(x, z, lx, lz, num, dxy=(0, 0)):
        a = math.atan2(-(lz - z), lx - x)          # screen angle of the look direction
        cx, cy = P(x, z)
        cx += dxy[0]
        cy += dxy[1]
        tri = [(cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
               (cx + 22 * math.cos(a + 2.5), cy + 22 * math.sin(a + 2.5)),
               (cx + 22 * math.cos(a - 2.5), cy + 22 * math.sin(a - 2.5))]
        d.polygon(tri, fill=(200, 40, 40), outline=ink)
        d.text((cx - 22 * math.cos(a), cy - 22 * math.sin(a)), str(num), font=font(20, True), fill=(200, 40, 40),
               anchor='mm', stroke_width=3, stroke_fill=(255, 255, 255))

    seen = {}
    for n, c in CAMS.items():
        if 'pos' in c:
            key = (c['pos'][0], c['pos'][2])
            seen.setdefault(key, []).append(n)
    for (x, z), ns in seen.items():
        look = CAMS[ns[0]]['look']
        cam_icon(x, z, look[0], look[2], ','.join(map(str, ns)))
    p6 = CAMS[6]['path']
    cam_icon(p6[0][0], p6[0][2], CAMS[6]['look'][0], CAMS[6]['look'][2], 6)
    p8 = CAMS[8]['path']
    cam_icon(p8[-1][0], p8[-1][2], CAMS[8]['look'][0], CAMS[8]['look'][2], 8)
    p11 = CAMS[11]['path']
    cam_icon(p11[0][0], p11[0][2], CAMS[11]['look'][0], CAMS[11]['look'][2], 11)
    s0 = orbit_pos(0, o)
    cam_icon(s0[0], s0[2], o['centre'][0], o['centre'][1], '12 loop')
    # people and robots
    for name, pp in PEOPLE.items():
        x, z = pp['at']
        c = (240, 240, 240) if pp['who'] == 'Andy' else (40, 50, 90)
        r = 0.2
        d.ellipse([P(x - r, z + r), P(x + r, z - r)], fill=c, outline=ink, width=3)
        a = math.radians(pp['facing'])
        tip = P(x + 0.34 * math.sin(a), z + 0.34 * math.cos(a))
        d.line([P(x, z), tip], fill=ink, width=4)
        d.text(P(x, z), pp['who'][0], font=font(18, True), fill=ink if pp['who'] == 'Andy' else (255, 255, 255), anchor='mm')
    for name, rb in ROBOTS.items():
        x, z = rb['at']
        r = 0.2
        d.regular_polygon((P(x, z), r * S), 6, fill=(205, 210, 220), outline=(30, 60, 160), width=3)
        tag = name.split(' (')[0].replace('robot ', '').replace('robots ', '')
        d.text(P(x, z), tag, font=font(15, True), fill=(30, 60, 160), anchor='mm')
    # key
    y = int((Z1 - Z0) * S) + 6
    d.line([(20, y), (W - 20, y)], fill=ink, width=2)
    lines = [
        ('PREPPER MINISTER: the house from above (1 square of the grid = 1 m)', f_big),
        ('Red triangles: cameras, numbered by shot, pointing where they look. Red lines: moving cameras (6, 8, 11) and the shot 12 loop.', f_mid),
        ('A = Andy, W = Wes (the stick shows which way they face). Hexagons = robots: A at the hall door (8), B from the opening (9),', f_mid),
        ('C and D at the kitchen window (10), 1 to 5 in shot 12 (5 is the one in the kitchen door in shot 11).', f_mid),
        ('Living room 6 x 5.4 m, kitchen 5.6 x 5.4 m, hallway 1.6 m wide, ceilings 2.8 m. Doors 0.84 m, the wide opening 2.8 m.', f_mid),
        ('Hallway door just behind Andy, slightly left. Hinged on its left: kicked open, it bangs the wall by the drinks cabinet.', f_mid),
    ]
    yy = y + 16
    for text, f in lines:
        d.text((24, yy), text, font=f, fill=ink)
        yy += 46 if f is f_big else 36
    # a faint metre grid over the plan
    grid = Image.new('RGBA', im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gx in range(-6, 7):
        gd.line([P(gx, Z1), P(gx, Z0)], fill=(0, 0, 0, 22), width=1)
    for gz in range(0, 8):
        gd.line([P(X0, gz), P(6.9, gz)], fill=(0, 0, 0, 22), width=1)
    im = Image.alpha_composite(im.convert('RGBA'), grid).convert('RGB')
    im.save(out, quality=92)
    print('saved', out, im.size)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'sketch':
        sketch(sys.argv[2])
    else:
        print(__doc__)
