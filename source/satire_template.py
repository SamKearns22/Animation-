#!/usr/bin/env python3
"""Satire-style film TEMPLATE. Copy to source/NAME.py, change NAME and the STORY section; leave the rest.
Everything else is already wired in: the picture cache with captions and title on last, the cast sheet, the plan
checks (mouths move for every phrase, voice above everything else, subtitles printed to proofread), and the general
audit (each body drawn alone: in pieces, popping, stretching, frozen; every action tested on every frame; eyelines).
Guide: guides/satire.md.

    python3 source/NAME.py cast OUT.png              the cast on one sheet: approve it before any animation
    python3 source/NAME.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/NAME.py check                     every check and the audit (also run by preflight.py)
    python3 source/NAME.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1]   (--span: a clip of one moment)
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  people: flat shapes, black outlines
import mossad as M               # noqa: E402  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402  arms solved and guarded
import mouths                    # noqa: E402  lip sync
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
from satire_style import rough, install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR

# =============================================== STORY (change this) ===============================================
NAME = 'satire-template'
TITLE = ('THE TEMPLATE',)                         # Cranberry Title style, on for 2 s; one line sits highest
TITLE_AT = dict(cap=116, top=310)                 # its size and height: checked never to cover anyone
CAST = {   # look and build per person (skin, hair, clothes, face); the cast sheet shows them side by side
    'A': dict(skin=B.PALE, hair='side', hair_c=(70, 56, 44), jacket=(60, 70, 90), trousers=(40, 42, 50), outfit='suit',
              jaw='square', hw=70, hh=90),
    'B': dict(skin=B.OLIVE, hair='bob', hair_c=(150, 56, 40), jacket=(150, 60, 70), trousers=(50, 46, 50), outfit='blouse',
              jaw='soft', hw=64, hh=86, lashes=True),
}
LOOKS_AT = {'A': 'B', 'B': 'A'}                   # who each person looks at (checked)
LINES = [   # 'audio': 'NAME-1' uses source/audio/NAME-1.m4a and times the line to it
    dict(who='A', text='This is a template line.', start=0.3, end=2.4),
    dict(who='B', text='And this is the reply.', start=2.8, end=4.6),
]
SHOTS = [('two', 0.0, 3.0), ('B', 3.0, 5.6)]       # (camera: two-shot or one person's close-up, start, end)
# Rule 1 (plan.py): the world drawn once, in metres, before any shot: every place, every door and opening (and what
# each shows: rule 2), every thing, where each person stands and faces, every camera. Every shot reads from it (XS
# below comes from PEOPLE). `python3 source/plan.py NAME sketch OUT.jpg` draws it for Sam; pre-flight checks it.
PLAN = dict(   # this template's film is flat: its plan is the strip of room the frame shows (about 2 m across)
    CEIL=2.6,
    ROOMS={'room': (-1.6, -3.6, 1.6, 2.0)},
    OPENINGS={'window': dict(wall=('z', 2.0), span=(-0.82, -0.21), sill=1.07, head=1.8, to='the street')},
    THINGS={'table': dict(at=(0.0, 0.65), size=(0.61, 0.7, 0.82), facing=0)},
    PEOPLE={'A': dict(at=(-0.38, 0.0), facing=90, who='A'), 'B': dict(at=(0.38, 0.0), facing=270, who='B')},
    CAMS={'two': dict(pos=(0.0, 1.0, -3.0), look=(0.0, 1.0, 0.0)), 'B': dict(pos=(0.38, 1.5, -1.2), look=(0.38, 1.5, 0.0))},
    GROUPS={},                                      # rule 9: {group: dict(arriving=, stopped=, leaving=)}
)
# Rule 3 (benchmark.py): before building any place, the 8-10 things that make it recognisable, each with how ours has
# it ('' = not built: pre-flight fails); refs in references/NAME/. No references yet: stop and ask Sam.
BENCHMARK = [dict(place='room', refs=[], at=1.0, items=[('what makes it recognisable', '')])]
# Rule 14 (preflight.py): who the brief puts in each shot; pre-flight refuses while any of them is never on screen there
SHOT_CAST = {'two': ['A', 'B'], 'B': ['B']}
DUR = 5.6
# Any action as beats (set-up, action, contact, follow-through, settle); pace by ease: 'fast' into a hit, 'slow' out.
# The value is A's near hand target in A's own units (x right, y down from the neck). Every frame is tested.
THUMP = filmkit.Beats([(1.0, 'set-up', (150, 300)), (1.45, 'wind-up', (300, -40)),
                       (1.6, 'contact', (175, 335), 'fast'), (2.1, 'settle', (150, 310), 'slow')])
# What the shared checks need (preflight.py runs them all; guides/satire.md, 'Getting it right first time'):
HOOK = ('Hook Text here', {'y': 880})               # exactly as finish.py will be given it (--y, --x, --until)
KEEP_CLEAR = []                                     # [(name, box_at(t) -> (x0, y0, x1, y1) or None)]: signs, readouts
PROP_SIZES = []                                     # [(name, sizes.SIZES kind, w, h, px_per_m or None or 0)]
OUTFIT = {}                                         # {who: {'skirt top': y, 'jacket hem': y, ...}} person units
HEIGHTS = {}                                        # {who: real height in metres}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []   # clipcheck: deliberate contacts, hits, falls, knock-ons
# Rules 5 and 6 (guides/film-quality-rules.md; audit.py): scene(t) below gives everyone and everything solid; list
# here every contact that is meant (thing or thing.part, the other, from, to, why) and every meant pop-in.
ALLOWED_CONTACTS = [('A.hand*', 'TABLE', 1.5, 2.2, 'A thumps the table')]
ALLOWED_POPS = []                                   # [(name, from, to, why)], e.g. gone in through a door
# define layers(t) for drawing order (see clipcheck.py and shocking.py), and SPLICE = ((clip, start, end), ...) for a
# song joined from recordings (musiccheck.py)
# ====================================================================================================================

S, FY = 0.8, 1420                                 # people's scale, floor line
NECK_Y = FY - F.SOLE_Y * S
PX_M = 1.41 / (F.SOLE_Y * S)                       # metres per pixel (neck to soles: 1.41 m)
XS = {w: 540 + p['at'][0] / PX_M for w, p in PLAN['PEOPLE'].items()}   # where each stands, from the plan
BLACK_AT = DUR
for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        v = MA.line(ln['audio'])
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in 'AB'}
BLINKS = {w: F.blinks(7 if w == 'A' else 11, 0.5, DUR, talking=True) for w in 'AB'}


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def cam_for(t):
    s = shot_of(t)
    return B.Cam(1.0, 540, 960) if s == 'two' else B.Cam(2.0, XS[s], NECK_Y - 150 * S + 80)


def state(who, t):
    """Everything about one person at time t: look, arms, mouth, blink. Logs their eyeline for the check."""
    c = CAST[who]
    sp = dict(c, full=True, pose='custom', name=who)
    rig = F.Rig(sp)
    sp['arms'] = rig.pose('sides')
    if who == 'A' and THUMP.b[0][0] <= t <= THUMP.b[-1][0]:
        sp['arms']['R'] = rig.arm('R', THUMP.at(t), 'grip', 'out', strict=False)
    shape = mouths.at(TRACK[who], t)
    sp['mouth'] = 'set' if shape == 'rest' else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS[who])
    sp['look'] = F.look_at(XS[who], XS[LOOKS_AT[who]])
    sp['breath'] = F.breath(t, 4.0, 1.5, 0.0 if who == 'A' else 0.4)
    sp['tilt'] = filmkit.shifts(t, seed=1 if who == 'A' else 2)   # never frozen: held poses, small quick shifts (no sway)
    eye = (XS[who], NECK_Y - 150 * S)
    filmkit.eyeline(who, t, eye, (sp['look'], 0.0), (XS[LOOKS_AT[who]], eye[1]))
    return sp


def mouths_seen(t):
    """Every face on screen at t with its mouth as drawn, for the script and mouth audit (voices.py, rule 7):
    (name, mouth, view in degrees (0 facing us), head height in pixels). Add anyone else drawn with a face."""
    cam = cam_for(t)
    return [(who, state(who, t)['mouth'], 0.0, 2 * CAST[who].get('hh', 90) * S * cam.z)
            for who in 'AB' if visible(who, cam)]


def visible(who, cam):
    return abs(XS[who] - cam.cx) * cam.z <= 540 + 130 * S * cam.z


def background(img, cam):
    """The set, in Satire style: flat colour, one outline, hand-cut corners (never ruler-straight clip-art)."""
    p = B.Pen(img, cam)
    box = lambda x0, y0, x1, y1, f, sd: p.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 6, sd), f, (24, 20, 22), 3)
    box(-600, -600, 1700, FY - 40, (214, 200, 168), 1)
    box(110, 470, 430, 840, (150, 190, 214), 2)
    box(-600, FY - 40, 1700, 2600, (140, 104, 76), 3)
    box(380, NECK_Y + 390 * S, 700, FY - 30, (120, 84, 60), 4)          # the table A thumps


def picture(t):
    """The frame WITHOUT captions or title (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas()
    background(img, cam)
    for who in 'AB':
        if visible(who, cam):
            B.person(img, cam, XS[who], NECK_Y, S, state(who, t), t)
    return img


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.25, nxt):
            return ln['text']
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
        if t < 2.0:
            B.title_lines(img, TITLE, **TITLE_AT, alpha=1.0 if t < 1.75 else max(0.0, 1.0 - (t - 1.75) / 0.25))
    return img


def frame_image(t):
    return overlay(picture(t), t)


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # no room tone: white noise under a film comes up as a hiss (Sam, 19 Oct)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    # Sound effects go in by the moment they really start, not the start of their file, e.g.
    #   filmkit.place(rest, load('source/audio/NAME-slam.mp3'), at=1.6, sr=SR)   (lands the slam on the contact frame)
    # Outdoor recordings and ambience: cut wind rumble (sound_questions asks about it).
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:                              # -16 LUFS, levelled gently, never squashed by more
        mix, g = MA.master(mix, end)                             # than 3 dB (hard limiting crackles on a phone)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in 'AB' for x in TRACK[w]), windows)
    if any(ln['_voice'] is not None for ln in LINES):
        _, voice, rest = soundtrack(stems=True)
        faults += filmkit.voice_balance(voice, rest, SR, windows)
        n = int((DUR + 0.3) * SR)
        raw = np.zeros(n)
        for ln in LINES:
            if ln['_voice'] is not None:
                s = int(ln['start'] * SR)
                raw[s:s + len(ln['_voice'])] += ln['_voice'][:n - s]
        faults += MA.limit_check(raw, int(BLACK_AT * SR))     # more than 3 dB of limiting crackles on a phone
    faults += title_check()
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT)               # no steady hiss (Sam, 19 Oct)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)        # may be meant: ask, never change it without him
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# ------------------------------------------------------------------------------------------------ the audit
# audit.py: rule 5 (nothing passes through anything) and rule 6 (nothing pops in or out). This template's film is flat
# (everyone at one distance, on the floor line), so its world is the frame in metres. scene(t) gives the people and
# props; the set (every wall, door frame, door and THING in PLAN) joins the audit by itself (sets.solids, rule 12):
# list only what to leave out, SET_EXCLUDE = [(name, why)]. A film with a 3D set and a
# camera (Cam3) instead runs its own picture(t) with the drawing switched off and records where everyone is put:
# copy power_crime.scene(), which gets every person and prop exactly as drawn (props too: a card with .quad, a
# long thing with .along).


def project(cam, P):
    X = P[:, 0] / PX_M + 540
    Y = FY - P[:, 1] / PX_M
    return (X - cam.cx) * cam.z + 540, (Y - cam.cy) * cam.z + 960, np.full(len(P), 5.0)


def scene(t):
    import audit
    import clipcheck as CC
    cam = cam_for(t)
    out = []
    for who in 'AB':
        if visible(who, cam):
            x = (XS[who] - 540) * PX_M
            sol = audit.simple(who, x, 0.0)
            if who == 'A':                                # his thumping hand (its target is in his own units)
                hx, hy = THUMP.at(t)
                sol.append(CC.sphere('A', 'handR', (x + hx * S * PX_M, (FY - NECK_Y - hy * S) * PX_M, 0.35), 0.05))
            out.append(audit.Thing(who, sol))
    return out                                            # the walls, the table and every THING: from PLAN (rule 12)


def title_check():
    """The title must not cover anyone: the title and each person alone, on a frame where the title shows."""
    t = 1.0
    title = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
    B.title_lines(title, TITLE, **TITLE_AT)
    people = {}
    for who in 'AB':
        if visible(who, cam_for(t)):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            B.person(lay, cam_for(t), XS[who], NECK_Y, S, state(who, t), t)
            people[who] = lay
    return filmkit.title_clear(title, people)


def audits():
    """The general audit: each person alone over every frame they are on screen, the actions on every frame,
    the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            B.person(lay, cam_for(t), XS[who], NECK_Y, S, state(who, t), t)
            return lay
        return draw
    actors = {}
    for who in 'AB':
        for shot, a, b in SHOTS:
            ts = [i / FPS for i in range(int(a * FPS), int(b * FPS)) if visible(who, cam_for(i / FPS))]
            if ts:
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=())
    faults += filmkit.check_eyelines()
    rig = F.Rig(dict(CAST['A'], full=True, pose='custom'))

    def arm_rule(target):
        el, wr = rig.arm('R', target, 'grip', 'out', strict=False)[:2]
        return filmkit.check_joints({'sh': rig.shoulder('R'), 'el': el, 'wr': wr, 'head': (0, -150)},
                                    [('angle', 'sh', 'el', 'wr', 25, 180), ('apart', 'wr', 'head', 90),
                                     ('side', 'el', 'sh', 0)])
    faults += THUMP.audit(arm_rule, label='A thumps the table')
    faults += moves.audit()                                  # the movement library's own checks (gaits, poses)
    return faults


def cast_sheet(out):
    """Everyone side by side, with the body landmarks (waist, hips, knee) drawn across to check the clothes against,
    and a 1.75 m person and a 1 m ruler for scale (sizes.scale_ref). Add every OTHER view each character appears in
    (from above, a close-up, mid-action), any new prop beside the scale person, and for the film's key reaction a
    numbered strength sheet (1 = slight, 6 = huge) for Sam to pick from."""
    import landmarks
    import sizes
    from PIL import ImageDraw
    img = Image.new('RGBA', (1080, 1080), (230, 226, 220, 255))
    for i, who in enumerate('AB'):
        sp = dict(CAST[who], full=True, pose='custom')
        sp['arms'] = F.Rig(sp).pose('sides')
        B.person(img, B.Cam(1.0, 540, 960), 300 + 480 * i, 260, 0.62, sp, 0.0)
    d = ImageDraw.Draw(img)
    landmarks.draw(d, 540, 260, 0.62, 1000)
    sizes.scale_ref(d, 520, 260 + 928 * 0.62, 0.62 / landmarks.V.M_PER_UNIT)
    img.convert('RGB').save(out)


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    def one(who):
        def d(im):
            sp = dict(CAST[who], full=True, pose='custom')
            sp['arms'] = F.Rig(sp).pose('sides')
            B.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, sp, 0.0)
        return d
    return [(who, one(who)) for who in CAST]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        B.SS = 1
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = audits()
        import audit
        f += [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]   # collisions, pop-ins (preflight too)
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)                 # natural arms and legs: one outline at the shoulder, smooth shaped legs (Cry Minister)
# Movement (guides/movement-system-plan.md, guides/reference-pack.md), built to order: use only what the script needs.
#   views.person(img, cam, x, y, s, sp, t, yaw, pose)   anyone from any angle (front, three-quarter, side, back)
#   moves.gait / travel / pace, moves.pose(sp, 'arms_folded'), moves.sit_down / stand_up, moves.punch / kick / sword /
#   hit_react / fall, moves.driving / car_in / car_out; stage.Stage(series.Room(...)) for people on a perspective floor.
#   Turns: the straight 180 (one drawing to the other). No sound effects unless the script asks.
import views                     # noqa: E402,F401
import moves                     # noqa: E402,F401
import stage                     # noqa: E402,F401
import perform                   # noqa: E402,F401  natural performance: follow-through, beat bounce, varied faces

if __name__ == '__main__':
    main()
