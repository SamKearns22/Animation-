#!/usr/bin/env python3
"""Patriots 3 (D-Day: the Patriot turns up in a German MG42 bunker). Started from source/satire_template.py.
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
# PLANNING STAGE (27 Oct): the story, the shots and the plan are in; everything below the STORY section is still the
# template's flat two-person drawing. The build stage replaces picture/state/scene with the bunker set
# (patriots3_bunker), the cast (patriots3_cast) and a sets.Cam per shot from the plan (cam_for, already done).
import patriots3_cast as PC      # noqa: E402  the Patriot, the Gunner, the Loader, the MG42
import patriots3_plan as PL      # noqa: E402  the world in metres (rule 1)
import sets as SETS              # noqa: E402

NAME = 'patriots3'
TITLE = ()                                        # no title by default (Sam, 15 Oct)
TITLE_AT = dict(cap=116, top=310)
CAST = {'patriot': PC.PATRIOT, 'gunner': PC.GUNNER, 'loader': PC.LOADER}
LOOKS_AT = {'patriot': 'gunner', 'gunner': 'patriot', 'loader': 'patriot'}
# Lines by number (never by position). Times are the plan's guesses until Sam's recordings arrive ('audio' keys).
# The German barks are Sam's game clips (source/audio/patriots3-sfx/, kept off GitHub); no subtitles on them.
LINES = [
    dict(n=1, who='loader', text='Feind gesichtet!', start=4.0, end=5.1, audio='patriots3-sfx/german-see-enemy',
         sub=False),
    dict(n=2, who='loader', text='Feuer auf Ziel!', start=5.4, end=6.2, audio='patriots3-sfx/german-fire-at-target',
         sub=False),
    dict(n=3, who='patriot', text='Small boat problem?', start=6.4, end=7.5, audio='patriots3-patriot-1', off=True),
    dict(n=4, who='patriot', text='What can I say? Foreign invaders coming across the sea? Happens everywhere these '
         'days.', start=8.0, end=12.2, audio='patriots3-patriot-2'),
    dict(n=5, who='gunner', text='Who are you?', start=13.4, end=14.3, audio='patriots3-gunner-1'),
    dict(n=6, who='patriot', text='Just a concerned citizen. Just a regular man with regular concerns.', start=14.8,
         end=18.4, audio='patriots3-patriot-3'),
    dict(n=7, who='loader', text='Ah, you are with the Führer?', start=18.9, end=20.4, audio='patriots3-loader-1'),
    dict(n=8, who='gunner+loader', text='Heil!', start=20.6, end=21.2, audio='patriots3-heil'),
    dict(n=9, who='patriot', text='Jesus Christ, lads. The Free Speech Police are everywhere. Save that s*** for '
         'WhatsApp.', start=21.6, end=26.0, audio='patriots3-patriot-4', bleep='s***'),
    dict(n=10, who='patriot', text='Anyway, got problems with the Establishment? People trampling on your '
         'sovereignty? Let\'s just say I\'m here to assist.', start=27.9, end=33.2, audio='patriots3-patriot-5'),
    dict(n=11, who='patriot', text='They ain\'t even wearing poppies.', start=34.4, end=36.2, audio='patriots3-patriot-6'),
]
SHOTS = [   # (shot, start, end): one camera each from PL.CAMS
    ('s1', 0.0, 3.6),     # high above the coast: cliffs flashing, artillery into sand and spray, six craft creeping in
    ('s2', 3.6, 7.6),     # inside, behind the crew: firing, the Loader spotting; "Small boat problem?" (off); they turn
    ('s3', 7.6, 12.4),    # the Patriot leaning in the doorway (their eyeline)
    ('s4', 12.4, 14.5),   # the crew from in front: a look at each other, back to him; "Who are you?"
    ('s5', 14.5, 18.7),   # the wide: he walks up to them; "Just a concerned citizen..."
    ('s6', 18.7, 21.5),   # the crew from in front: "Ah, you are with the Führer?"; the salute; "Heil!"
    ('s7', 21.5, 26.3),   # the Patriot, upset, arms darting: "Jesus Christ, lads..."
    ('s8', 26.3, 33.5),   # the wide: the blast on the slit's lip, they stumble back; "Anyway..." he walks to the gun
    ('s9', 33.5, 42.6),   # in the slit facing in: head shake, "poppies", he fires (room lit), push-in on their glance
]
PLAN = {k: getattr(PL, k) for k in ('CEIL', 'ROOMS', 'OPENINGS', 'LOOKS', 'THINGS', 'PEOPLE', 'CAMS', 'GROUPS',
                                    'FRAMING')}
BENCHMARK = [   # rule 3: filled in when each place is built ('' = not built yet: pre-flight fails)
    dict(place='the coast from the air', refs=['air-1-fleet-low.jpg', 'air-2-fleet-and-coast.jpg',
                                               'landers-3-from-above.jpg', 'landers-4-in-convoy.jpg'], at=1.8,
         items=[('dark cliffs or bluffs along the shore, flashing with gunfire', ''),
                ('a wide grey-brown beach with the tide out, wet sand darker near the sea', ''),
                ('lines of white surf and spray', ''), ('six landing craft in a ragged line, white wakes behind', ''),
                ('each craft packed with helmets, shoulder to shoulder (landers-3)', ''),
                ('artillery bursts: sand and water thrown up in columns', ''), ('smoke drifting along the shore', ''),
                ('ships far out on a grey sea, haze', ''), ('beach obstacles (hedgehogs) in the shallows', '')]),
    dict(place='the casemate inside', refs=['bunker-1-cutaway-wn65.jpg', 'bunker-3-casemate-gunner.jpg',
                                            'bunker-4-embrasure-inside.jpg'], at=10.0,
         items=[('thick raw concrete, board marks from the formwork', ''), ('the slit: bright beach in a dark wall', ''),
                ('a low heavy ceiling', ''), ('a steel door frame in the back wall (reference still missing)', ''),
                ('the MG42 on the sill, belt and ammo box', 'built (patriots3_bunker)'),
                ('spent cases on the floor under the gun', ''), ('ammo crates, a range card, a field telephone', ''),
                ('dim inside, lit from the slit', '')]),
]
SHOT_CAST = {'s2': ['gunner', 'loader'], 's3': ['patriot'], 's4': ['gunner', 'loader'],
             's5': ['patriot', 'gunner', 'loader'], 's6': ['gunner', 'loader'], 's7': ['patriot'],
             's8': ['patriot', 'gunner', 'loader'], 's9': ['patriot', 'gunner', 'loader']}
DUR = 42.6
THUMP = filmkit.Beats([(1.0, 'set-up', (150, 300)), (1.45, 'wind-up', (300, -40)),
                       (1.6, 'contact', (175, 335), 'fast'), (2.1, 'settle', (150, 310), 'slow')])   # template's
HOOK = ('Small boats crisis, June 1944', {'y': 300})   # to settle with Sam: over the sky in shot 1
KEEP_CLEAR = []
PROP_SIZES = []                                     # the MG42, belt, box: patriots3_cast (real sizes)
OUTFIT = PC.OUTFIT
HEIGHTS = PC.HEIGHTS
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS = []
ALLOWED_POPS = []
SET_EXCLUDE = []
TOUCHES = []
FREE_MOVES = []
SOUND_SOURCES = {}
EFFECTS = []
JOKE_PROPS = []
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
    """The shot's camera from the plan (a sets.Cam); shot 9 pushes in on the soldiers over its last 3.4 s."""
    s = shot_of(t)
    if s == 's9':
        a, b = PL.CAMS['s9 start'], PL.CAMS['s9 end']
        t0 = next(x for n, _, x in SHOTS if n == 's9') - 3.4
        k = min(1.0, max(0.0, (t - t0) / 1.6))
        k = k * k * (3 - 2 * k)
        mix = lambda p, q: tuple(u + (v - u) * k for u, v in zip(p, q))
        return SETS.Cam(a['pos'], mix(a['look'], b['look']), focal=a['focal'] + (b['focal'] - a['focal']) * k)
    c = PL.CAMS[s]
    return SETS.Cam(c['pos'], c['look'], focal=c['focal'])


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
    box(110, 470, 430, 840, (150, 190, 214), 2)                          # the window (PLAN: to 'the street'):
    box(110, 600, 430, 840, (168, 108, 84), 5)                           # the street seen through it, never a flat
    for wx in (150, 290):                                                # fill (rule 2): the building opposite,
        box(wx, 640, wx + 90, 720, (96, 112, 128), 6 + wx)               # its windows, the pavement
    box(110, 800, 430, 840, (176, 174, 168), 7)
    box(262, 470, 278, 840, (236, 232, 222), 8)                          # the window's middle bar
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
