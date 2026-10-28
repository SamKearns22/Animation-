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
from ed import INK               # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR

# =============================================== STORY (change this) ===============================================
# BUILD STAGE (27 Oct): the room (patriots3_room), the acting (patriots3_act), the blast (patriots3_fx) and the coast
# (patriots3_coast) are drawn below through each shot's sets.Cam. Sam (27 Oct): no recordings yet, subtitles only.
import patriots3_cast as PC      # noqa: E402  the Patriot, the Gunner, the Loader, the MG42
import patriots3_plan as PL      # noqa: E402  the world in metres (rule 1)
import sets as SETS              # noqa: E402

NAME = 'patriots3'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'patriots-3.md')
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
    dict(n=3, who='patriot', text='Small boat problem?', start=6.4, end=7.5, audio='patriots3-patriot-1', off=True,
         chunks=['Small boat problem?']),
    dict(n=4, who='patriot', text='What can I say? Foreign invaders coming across the sea? Happens everywhere these '
         'days.', start=8.0, end=12.2, audio='patriots3-patriot-2',
         chunks=['What can I say? Foreign invaders', 'coming across the sea?', 'Happens everywhere these days.']),
    dict(n=5, who='loader', text='Who are you?', start=13.4, end=14.3, audio='patriots3-loader-1',
         chunks=['Who are you?']),   # Sam: the spotter
    dict(n=6, who='patriot', text='Just a concerned citizen. Just a regular man with regular problems.', start=14.5,
         end=18.4, audio='patriots3-patriot-3',
         chunks=['Just a concerned citizen.', 'Just a regular man', 'with regular problems.']),
    dict(n=7, who='loader', text='Ah, you are with the Führer?', start=19.0, end=20.4, audio='patriots3-loader-2',
         chunks=['Ah, you are', 'with the Führer?']),
    dict(n=8, who='gunner+loader', text='Heil!', start=20.75, end=21.2, audio='patriots3-heil', chunks=['Heil!']),
    dict(n=9, who='patriot', text='Jesus Christ, lads. The Free Speech Police are everywhere. Save that s*** for '
         'WhatsApp.', start=21.6, end=26.0, audio='patriots3-patriot-4', bleep='s***', bleep_at=(3.68, 3.95),
         chunks=['Jesus Christ, lads.', 'The Free Speech Police are everywhere.', 'Save that s*** for WhatsApp.']),
    dict(n=10, who='patriot', text='Anyway, got some problems with the Establishment? People trampling on your '
         'sovereignty? Let\'s just say I\'m here to assist.', start=27.9, end=33.2, audio='patriots3-patriot-5',
         chunks=['Anyway, got some problems', 'with the Establishment?', 'People trampling on your sovereignty?',
                 "Let's just say,", "I'm here to assist."]),
    dict(n=11, who='patriot', text='They ain\'t even wearing poppies.', start=34.4, end=36.2, audio='patriots3-patriot-6',
         chunks=["They ain't even", 'wearing poppies.']),
    dict(n=12, who='patriot', text='Traitors.', start=39.6, end=40.6, audio='patriots3-patriot-7',
         chunks=['Traitors.']),   # Sam, 27 Oct: after his last line, just before their eyes meet
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
                                    'FRAMING', 'SHOT_MARKS')}
REFS = 'references/patriots-3/'
BENCHMARK = [   # rule 3: what makes each place recognisable, and how ours has it
    dict(place='the coast from the air', refs=[REFS + r for r in ('air-1-fleet-low.jpg', 'air-2-fleet-and-coast.jpg',
                                               'air-4-beach-from-above.jpg', 'landers-3-from-above.jpg')], at=1.8,
         items=[('dark cliffs or bluffs along the shore, flashing with gunfire', 'black cliff band with gullies; '
                 'one-frame lumpy flashes and tracer streaks every frame'),
                ('a wide grey-brown beach with the tide out, wet sand darker near the sea', 'dry and wet sand bands, craters'),
                ('lines of white surf and spray', 'surf lines rolling in; white spray plumes on the water'),
                ('six landing craft in a ragged line, white wakes behind', 'six LCVPs, staggered, V wakes, bow waves'),
                ('each craft packed with helmets, shoulder to shoulder (landers-3)', '36 helmets in each, never a grid'),
                ('artillery bursts: sand and water thrown up in columns', '15 bursts over 3.6 s, lumpy plumes, stains stay'),
                ('smoke drifting along the shore', 'flat grey smoke drifting east along the beach'),
                ('ships far out on a grey sea, haze', 'two warships at the bottom corners (the fleet is behind us); haze'),
                ('beach obstacles (hedgehogs) in the shallows', 'small dark crosses along the waterline')]),
    dict(place='the casemate inside', refs=[REFS + r for r in ('room-1-inside-to-slit.jpg', 'room-2-inside-doorway.jpg',
                                            'bunker-3-casemate-gunner.jpg', 'bunker-4-embrasure-inside.jpg')], at=10.0,
         items=[('thick raw concrete, board marks from the formwork', 'vertical panel joints, board lines, damp stains'),
                ('the slit: bright beach in a dark wall', 'the slit wall darkest, the beach bright through it'),
                ('a low heavy ceiling', '2.4 m, ribbed with steel beams (room-1)'),
                ('a steel door frame in the back wall', 'angle-iron frame with rivets, a sill plate (room-2)'),
                ('the MG42 on the sill, belt and ammo box', 'the 3D MG42 on its bipod, belt into the box'),
                ('spent cases on the floor under the gun', '46 brass cases swept under the slit'),
                ('ammo crates, a range card, a field telephone', 'two crates, the card over the slit, phone on a shelf'),
                ('dim inside, lit from the slit', 'flat: back wall lit, slit wall in shadow, ceiling darkest'),
                ('cables and a caged lamp (room-2)', 'a cable run under the ceiling, a caged lamp over the door')]),
]
SHOT_CAST = {'s2': ['gunner', 'loader'], 's3': ['patriot', 'gunner', 'loader'], 's4': ['gunner', 'loader'],
             's5': ['patriot', 'gunner', 'loader'], 's6': ['gunner', 'loader'], 's7': ['patriot'],
             's8': ['patriot', 'gunner', 'loader'], 's9': ['patriot', 'gunner', 'loader']}
DUR = 42.6
THUMP = filmkit.Beats([(1.0, 'set-up', (150, 300)), (1.45, 'wind-up', (300, -40)),
                       (1.6, 'contact', (175, 335), 'fast'), (2.1, 'settle', (150, 310), 'slow')])   # template's
HOOK = ('Small Boats Crisis, June 1944', {'y': 300})   # Sam, 27 Oct; over the sky in shot 1
KEEP_CLEAR = []
PROP_SIZES = []                                     # the MG42, belt, box: patriots3_cast (real sizes)
OUTFIT = PC.OUTFIT
HEIGHTS = PC.HEIGHTS
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS = []
ALLOWED_MOUTHS = [('loader', 6.95, 7.45, 'startled: a gasp, mouth open'), ('gunner', 6.95, 7.45, 'startled: a gasp'),
                  ('loader', 26.8, 27.85, 'blasted: mouth open in shock'), ('gunner', 26.8, 27.3, 'blasted')]
PORTAL_OK = [('slit', 26.3, 33.5, 'shot 8 looks along the slit wall: we see the reveal side on, as you would'),
             ('door', 14.5, 18.7, 'shot 5 sees the doorway nearly edge on from the far corner: its reveal')]
ALLOWED_POPS = []
SET_EXCLUDE = []
TOUCHES = []
FREE_MOVES = []
SOUND_SOURCES = {}
EFFECTS = []                                      # filled in below the drawing code (each drawn alone, rule 15)
JOKE_PROPS = []                                   # the poppy is a line, not a prop (it is on him: 'ain't even wearing')
# Rule 38: front on by default; these views the shot demands (plan.py checks the rest face the lens)
THREE_QUARTER_OK = [
    ('s2', 'gunner at the gun', 'shot 2 is from behind the crew while they fire (the beach past them)'),
    ('s2', 'loader at the gun', 'shot 2 is from behind the crew while they fire'),
    ('s3', 'gunner turned', 'shot 3 is over their helmets at the Patriot in the doorway'),
    ('s3', 'loader turned', 'shot 3 is over their helmets at the Patriot in the doorway'),
    ('s5', 'patriot in the doorway', 'the wide: he walks across the room to them'),
    ('s5', 'patriot approached', 'the wide: he faces the crew'),
    ('s5', 'gunner facing him', 'the wide: they face the Patriot'),
    ('s5', 'loader facing him', 'the wide: they face the Patriot'),
    ('s8', 'patriot approached', 'Sam, 27 Oct: shot 8 side on from the west wall, the Patriot on the right'),
    ('s8', 'gunner facing him', 'Sam: shot 8 side on; they face the Patriot until the blast'),
    ('s8', 'loader facing him', 'Sam: shot 8 side on; they face the Patriot until the blast'),
    ('s8', 'patriot at the gun', 'Sam: shot 8 side on; he walks to the gun, the slit on the left'),
]
# ====================================================================================================================


import patriots3_room as ROOM    # noqa: E402  the casemate, drawn once from the plan
import patriots3_act as ACT      # noqa: E402  who stands where, in what pose, every moment
import patriots3_fx as PFX       # noqa: E402  the blast, dust, chips, muzzle light
import patriots3_coast as COAST  # noqa: E402  shot 1, painted in layers
import views as V                # noqa: E402
import sets as S3                # noqa: E402
from moves import lerp as MV_lerp   # noqa: E402

M = V.M_PER_UNIT
BLACK_AT = DUR
for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    src = next((os.path.join(HERE, 'audio', ln['audio'] + x) for x in ('.m4a', '.wav') if ln.get('audio') and
                os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + x))), None)
    if src:                                       # the barks are .wav game clips: levelled like a line
        v = MA.line(ln['audio']) if src.endswith('.m4a') else MA.load(src)
        if src.endswith('.wav'):
            v = v * 10 ** ((MA.LINE_LUFS - MA.lufs(v)) / 20)
        if ln.get('bleep_at'):                    # the word gone, a 1 kHz tone in its place; the mouth still says it
            b0, b1 = (int(x * SR) for x in ln['bleep_at'])
            k = np.arange(b1 - b0)
            v = v.copy()
            v[b0:b1] = 0.18 * np.sin(2 * math.pi * 1000 * k / SR) * np.minimum(1, np.minimum(k, k[::-1]) / (0.006 * SR))
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)
WHO = ('patriot', 'gunner', 'loader')
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if w in ln['who'].split('+')
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in WHO}
BLINKS = {w: F.blinks(5 + i * 4, 3.6, DUR, talking=True) for i, w in enumerate(WHO)}
KEY_FACES = [(20.45, 21.9), (ACT.T_MEET - 0.3, DUR)]   # no blink on the salute or the glance (Sam, 15 Oct)
BLINKS = {w: [b for b in bl if not any(a - 0.3 <= b <= c for a, c in KEY_FACES)] for w, bl in BLINKS.items()}


def chunk_times(ln):
    """Each subtitle chunk comes up on its first word (Sam, 16 Oct). Until the recording is in, the words are spread
    over the line by their syllables (a placeholder: never shown as final)."""
    chunks = ln.get('chunks') or [ln['text']]
    syl = [sum(mouths._syllables(w) for w in c.split()) for c in chunks]
    tot = float(sum(syl)) or 1.0
    out, acc = [], 0
    for c, n in zip(chunks, syl):
        out.append((ln['start'] + 0.1 + (ln['end'] - ln['start']) * acc / tot, c))
        acc += n
    return out


CHUNKS = [(t, c, ln) for ln in LINES if ln.get('sub', True) for t, c in chunk_times(ln)]


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def cam_for(t):
    """The shot's camera from the plan (a sets.Cam); shot 9 holds still (no push-in, Sam 27 Oct); shot 8 is
    kicked by the blast."""
    s = shot_of(t)
    if s == 's9':                                  # no push-in at the end (Sam, 27 Oct): they just look at each other
        a = PL.CAMS['s9 start']
        return SETS.Cam(a['pos'], a['look'], focal=a['focal'])
    c = PL.CAMS[s]
    return SETS.Cam(c['pos'], c['look'], focal=c['focal'], shake=PFX.shake(t) if s == 's8' else (0.0, 0.0))


def _dir(deg):
    return (math.sin(math.radians(deg)), math.cos(math.radians(deg)))


def view_yaw(cam, x, z, facing):
    """Which way someone is seen (0 facing us, +90 facing screen right), from the line between them and the lens
    only: a camera turning on the spot (shot 9's push-in) never changes how a person is drawn (cam.yaw_of used the
    camera's own right, so the Patriot popped to three-quarter mid push-in)."""
    fx, fz = facing if isinstance(facing, tuple) else _dir(facing)
    tc = np.array((cam.pos[0] - x, cam.pos[2] - z))
    tc /= np.linalg.norm(tc) or 1.0
    right = (-tc[1], tc[0])
    return math.degrees(math.atan2(fx * right[0] + fz * right[1], fx * tc[0] + fz * tc[1]))


def _tilt(cam, x, z, sp):
    """Where someone stands on screen through a 3D camera at its real tilt (as lying.stand): the floor point, their
    drawing scale, and (e, c) for views.person."""
    (Xf, Yf), _ = cam.project((x, 0.0, z))
    (_, _), km = cam.project((x, 0.9, z))
    s = PC.scale_for(sp, km * M)
    h = PC.HEIGHTS.get(sp.get('name'), 1.75)
    (_, Yn), _ = cam.project((x, h * 1.41 / 1.75, z))
    c = max(0.15, min(1.0, (Yf - Yn) / (928 * s)))
    tc = np.array((cam.pos[0] - x, 0.0, cam.pos[2] - z))
    tc /= np.linalg.norm(tc) or 1.0
    (_, Ym), _ = cam.project((x, 1.2, z))             # measured at the arms' height, not the floor's: close up, a
    (_, Yq), _ = cam.project(tuple(np.array((x, 1.2, z)) + tc * 0.42))   # hand held out at chest height barely drops
    e = max(V.ELEV, (Yq - Ym) / s / (0.42 / (M * h / 1.75)))
    return Xf, Yf, s, e, c


def look_of(a, t, cam):
    """The pupils' sideways offset (-1..1) towards what this person is looking at, from where both are on screen."""
    target = gaze(a, t)
    if target is None:
        return 0.0, None
    (X, _), k = cam.project((a.x, 1.6, a.z))
    (TX, TY), _ = cam.project(target)
    v = (TX - X) / (0.45 * k)
    if abs(TX - X) > 10:                               # a look that is meant always reads: never a dead-centre stare
        v = math.copysign(max(0.3, abs(v)), v)
    return max(-1.0, min(1.0, v)), (TX, TY)


def gaze(a, t):
    """What each person looks at (rule 25): a 3D point, or None (straight ahead: firing, spotting)."""
    P = lambda who: next(b for b in ACT.everyone(t) if b.who == who)
    if a.who == 'patriot':
        if t >= ACT.T_TO_GUN + 2.0:
            return None if t >= 34.4 else (0.0, 1.2, 1.6)             # at the gun: out at the beach
        g, l = P('gunner'), P('loader')
        return ((g.x + l.x) / 2, 1.55, (g.z + l.z) / 2)
    if t < ACT.T_TURN:
        return None
    other = 'loader' if a.who == 'gunner' else 'gunner'
    if ACT.T_GLANCE <= t < ACT.T_BACK or t >= ACT.T_MEET:
        o = P(other)
        return (o.x, 1.5, o.z)
    p = P('patriot')
    return (p.x, 1.6, p.z)


def face(a, t, cam):
    sp = {}
    shape = mouths.at(TRACK[a.who], t)
    sp['mouth'] = ('set' if a.who == 'gunner' else 'line') if shape == 'rest' else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS[a.who])
    look, scr = look_of(a, t, cam)
    sp['look'] = look
    sp.update(a.sp)
    return sp, scr


def draw_actor(img, cam, a, t, log=True):
    base = CAST[a.who]
    sp, scr = face(a, t, cam)
    sp = dict(base, **sp)
    Xf, Yf, s, e, c = _tilt(cam, a.x, a.z, base)
    if scr is not None and abs(scr[0] - Xf) > 10:      # the eyes point the way the target really is from the face
        sp['look'] = math.copysign(max(0.3, abs(sp['look'])), scr[0] - Xf)
    seen = sp['look']                                  # the way the eyes point on screen
    yaw = view_yaw(cam, a.x, a.z, a.facing)
    hy = view_yaw(cam, a.x, a.z, a.head_facing) if a.head_facing is not None else None
    if hy is not None and abs(yaw) < 22.5 and (hy < 0) != (yaw < 0) and a.who != 'patriot':
        yaw = math.copysign(max(abs(yaw), 0.5), hy)    # views.py mirrors the head with the body: a front-on soldier
                                                       # (symmetric) is drawn mirrored so his head can turn that way
    if a.who == 'patriot' and abs(yaw) < 22.5:         # facing us he is never mirrored: the poppy (left breast)
        yaw = abs(yaw)                                 # and his badges stay on the same sides in every shot (note 8)
        if hy is not None and abs(hy) < 22.5:
            hy = abs(hy)
    if V.snap(yaw)[1]:                                 # a mirrored drawing mirrors the pupils too
        sp['look'] = -sp['look']
    if not a.j.get('_dressed'):
        PC.outfit(a.j, base)
        a.j['_dressed'] = True
    ring = [(a.x + 0.3 * math.cos(u), 0.004, a.z + 0.22 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 18)]
    if all(cam.depth(q) > 0.2 for q in ring):         # the contact shadow on the floor
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        B.Pen(lay, S3.FLAT).poly([cam.project(q)[0] for q in ring], (0, 0, 0, 55), None)
        img.alpha_composite(lay)
    target = img
    if a.roll:
        target = Image.new('RGBA', img.size, (0, 0, 0, 0))
    PC.FROM_BEHIND[0] = abs(yaw) > 112.5
    j2 = V.person(target, S3.FLAT, Xf, Yf - 928 * s, s, sp, t, yaw, a.j, hy, tilt=(e, c))
    if a.roll:                                         # tipped onto the door post: west on screen, at this camera
        (wx, _), _ = cam.project((a.x - 0.3, 1.4, a.z))
        (ox, _), _ = cam.project((a.x, 1.4, a.z))
        (_, wy), _ = cam.project((a.x, 1.4 + 0.3, a.z))
        side = max(-1.0, min(1.0, (wx - ox) / (abs(ox - wx) + 0.3 * abs(Yf - wy) + 1e-6)))
        target = target.rotate(-a.roll * side, resample=Image.BICUBIC, center=(Xf * B.SS, Yf * B.SS))
        img.alpha_composite(target)
    if log:
        eye = (Xf, Yf - (928 + 150) * s * c)            # (the face's x is the feet's: people stand upright)
        if scr is not None:                             # rule 43: measured from the drawing, at this camera
            tx, _, tz = gaze(a, t)
            aim = view_yaw(cam, a.x, a.z, (tx - a.x, tz - a.z))
            at = next((b.who for b in ACT.everyone(t) if b.who != a.who and math.hypot(b.x - tx, b.z - tz) < 0.05), None)
            filmkit.eyeline(a.who, t, eye, (seen, 0.0), scr, aim=aim, drawn=j2, at=at)
    return j2


def _project_patch(cam):
    """views.project swapped for the real camera while the MG42 kit draws (its parts are 3D solids in world metres):
    the gun is drawn in true perspective in every shot (end on in shot 9), never through a person's flat frame."""
    return lambda p3, yaw: (cam.project(p3)[0], -cam.depth(p3))


def draw_gun3d(img, cam, fire_t, t):
    """The MG42 on its bipod on the sill, the belt into its box: each part a solid (the hull of its two sections),
    far parts first; parts at or behind the lens are left out (shot 9: the muzzle is beside the camera)."""
    g = ACT.gun_at(fire_t)
    firing = fire_t is not None and fire_t >= 0
    flash = 1.0 if (firing and int(round(fire_t * 12)) % 3 != 2) else 0.0
    p = B.Pen(img, S3.FLAT)
    real = V.project
    V.project = _project_patch(cam)
    try:
        path = PC.belt_path(ACT.REST.belt_points(), 48)
        if all(cam.depth(tuple(q)) > 0.3 for q in path):
            PC.draw_box(p, lambda w: w, 0, ACT.REST.box_at)
            PC.draw_belt(p, lambda w: w, 0, path, g.a, -(fire_t or 0.0) * 20 * 0.032 if firing else 0.0)
        P = lambda w: V.project(w, 0)
        parts = []
        for name, col, ring, centre, kind in PC.mg42_solids(g):
            if min(cam.depth(tuple(q)) for q in ring) < 0.2:
                continue
            pts, deps = zip(*(P(tuple(q)) for q in ring))
            parts.append((sum(deps) / len(deps), name, col, list(pts)))
        for hinge, foot in PC._bipod(g):
            d = PC._unit(foot - hinge)
            ring = PC._section(g, hinge, d, 0.008, 0.008, 'cyl') + PC._section(g, foot, d, 0.008, 0.008, 'cyl')
            if min(cam.depth(tuple(q)) for q in ring) < 0.2:
                continue
            pts, deps = zip(*(P(tuple(q)) for q in ring))
            parts.append((sum(deps) / len(deps), 'bipod', PC.GUN_D, list(pts)))
        parts.sort(key=lambda q: q[0])
        for _, name, col, pts in parts:
            hull = V._hull(pts)
            if len(hull) >= 3:
                p.poly(hull, col, INK, 2.0)
            if name == 'jacket':
                PC._vents(p, P, g)
        if firing:
            PC.cases(p, lambda w: w, 0, g, fire_t)
        if flash:
            tip = g(1.225)
            if cam.depth(tip) > 0.3:
                (X, Y), k = cam.project(tip)
                (bx, by), _ = cam.project(g(0.9))
                dx, dy = X - bx, Y - by
                n = math.hypot(dx, dy) or 1.0
                PC.PC.muzzle_flash(p, (X, Y), (dx / n, dy / n), 0.2 * k, n < 0.1 * k, int(fire_t * 12))
            else:                                     # beside the lens (shot 9): the flash floods in at the frame edge
                q = g(1.0)
                if cam.depth(q) > 0.15:
                    (X, Y), _ = cam.project(q)
                    X = min(max(X, -60), 1140)
                    _edge_flash(img, X, Y, int(fire_t * 12))
    finally:
        V.project = real


def _edge_flash(img, X, Y, seed):
    """A big lumpy muzzle flash at a screen point (house style: no star, no glow)."""
    rng = np.random.default_rng(seed)
    p = B.Pen(img, S3.FLAT)
    r = 300
    pts = [(X + r * rng.uniform(0.6, 1.0) * math.cos(a), Y + r * 0.8 * rng.uniform(0.6, 1.0) * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, 13, endpoint=False)]
    p.poly(pts, (255, 176, 60), INK, 2.0)
    p.poly([(X + (x - X) * 0.6, Y + (y - Y) * 0.6) for x, y in pts], (255, 232, 120), None)
    p.poly([(X + (x - X) * 0.3, Y + (y - Y) * 0.3) for x, y in pts], (255, 255, 244), None)


def hold_gun(a, cam, t):
    """Whoever is at the gun: both hands put on its grips where the camera really sees them (each grip's screen point
    turned back into a hand target in their own frame), and the gun drawn with them, their hands over it."""
    g = ACT.gun_at(a.fire_t)
    base = CAST[a.who]
    j = a.j
    Xf, Yf, s, e, c = _tilt(cam, a.x, a.z, base)
    yw = view_yaw(cam, a.x, a.z, a.facing)
    if a.who == 'patriot' and abs(yw) < 22.5:          # as draw_actor: facing us he is never mirrored
        yw = abs(yw)
    deg, mirror = V.snap(yw)
    flip = -1 if mirror else 1
    ang = math.radians(deg)
    Yn = Yf - 928 * s + j.get('bob', 0.0) * s
    unit = M * PC.HEIGHTS.get(base['name'], 1.75) / 1.75
    tc = np.array((cam.pos[0] - a.x, cam.pos[2] - a.z))
    tc /= np.linalg.norm(tc) or 1.0

    def target(W):
        (X, Y), _ = cam.project(W)
        d = float(np.dot((W[0] - a.x, W[2] - a.z), tc)) / unit
        px = (X - Xf) / (s * flip)
        py = 928.0 + ((Y - Yn) / s - 928.0) / c
        x, z, y = px * math.cos(ang) - d * math.sin(ang), px * math.sin(ang) + d * math.cos(ang), py - e * d
        return V.leaned((x, y, z), -j.get('lean', 0.0))
    grips = [target(g(0.40, -0.04)), target(g(0.24, 0.02))]          # on the receiver, where the camera sees them (Sam)
    near = lambda side, q: math.dist(j['sh' + side], q)
    sides = ('R', 'L') if near('R', grips[0]) + near('L', grips[1]) <= near('L', grips[0]) + near('R', grips[1]) \
        else ('L', 'R')
    pairs = list(zip(sides, grips))
    if a.one_hand:                                     # resting one hand on the stock, the other at his side
        side = min('LR', key=lambda sd: near(sd, grips[1]))
        pairs = [(side, grips[1])]
    for side, q in pairs:
        if a.reach < 1.0:                              # still reaching for it: part way from where the hand was
            q = MV_lerp(j['wr' + side], q, a.reach)
        V.arm_to(j, side, q, 'down', 'fist')

    def gun(p, j2):
        draw_gun3d(img_ref[0], cam, a.fire_t, t)
    gun.held = True
    j['props'] = [gun]
    j['grip'] = {sd for sd, _ in pairs}
    W = g(0.32, 0.0)                                   # the gun nearer the lens than his shoulders (shot 9, from the
    if math.dist(cam.pos, W) < math.dist(cam.pos, (a.x, 1.35, a.z)) - 0.15:   # slit): arms behind it, hands over (Sam)
        j['wrap'] = set(j['grip'])


img_ref = [None]


def on_screen(cam, a):
    return any(cam.visible((a.x, y, a.z), margin=60) for y in (0.2, 0.9, 1.6))


def picture(t):
    """The frame WITHOUT captions or title (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    if shot_of(t) == 's1':
        return COAST.picture(t)
    cam = cam_for(t)
    img = B.canvas((0, 0, 0))
    ROOM.draw(img, cam, t)
    PFX.lintel_bite(img, cam, t)
    landed = [pc for pc in PFX.pieces() if t >= pc.t0 and PFX.FX.landed_at(pc) is not None and t >= PFX.FX.landed_at(pc)]
    for pc in landed:                                   # settled on the floor: drawn as the floor, before people
        PFX.FX.draw_piece(img, cam, pc, t)
    people = [a for a in ACT.everyone(t) if on_screen(cam, a)]
    items = [(cam.depth((a.x, 0.9, a.z)), 'p', a) for a in people]
    items += [(cam.depth(pc.at(t)[0]), 'c', pc) for pc in PFX.pieces() if t >= pc.t0 and pc not in landed]
    items += [(cam.depth(pf[0]), 'd', pf) for pf in PFX.puffs(t)]     # dust: behind whoever is nearer than it
    img_ref[0] = img
    if not any(a.fire_t is not None or a.holds for a in ACT.everyone(t)):
        items.append((cam.depth(ACT.GUN(0.6)), 'g', None))
    for _, kind, a in sorted(items, key=lambda q: -q[0]):
        if kind == 'p':
            if a.holds:
                hold_gun(a, cam, t)
            draw_actor(img, cam, a, t)
        elif kind == 'c':
            PFX.FX.draw_piece(img, cam, a, t)
        elif kind == 'd':
            PFX.draw_puff(img, cam, a)
        else:
            draw_gun3d(img, cam, None, t)
    PFX.blast_flash(img, cam, t)
    PFX.dust(img, cam, t)
    ROOM.foreground(img, cam)
    PFX.muzzle_light(img, t)
    return img


def caption_at(t):
    for i, (a, c, ln) in enumerate(CHUNKS):
        nxt = CHUNKS[i + 1][0] if i + 1 < len(CHUNKS) else 1e9
        if a <= t < min(nxt, ln['end'] + 0.35):
            return c
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


SFX = os.path.join(HERE, 'audio', 'patriots3-sfx')


def sfx(name, t0=0.0, t1=None):
    """One of Sam's effect files (patriots3-sfx), optionally a stretch of it, cached."""
    key = (name, t0, t1)
    if key not in _SFX:
        x = MA.load(os.path.join(SFX, name))
        _SFX[key] = x[int(t0 * SR):None if t1 is None else int(t1 * SR)]
    return _SFX[key]


_SFX = {}


def _fit(x, dur, fade=0.03):
    """A clip looped or cut to `dur` seconds, a short fade at the end."""
    n = int(dur * SR)
    y = np.tile(x, n // len(x) + 1)[:n].copy()
    f = min(n, int(fade * SR))
    y[n - f:] *= np.linspace(1, 0, f)
    return y


def _muffle(x, hz=900):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, hz, 'low', fs=SR, output='sos'), x)


def sound_events():
    """Sam's effects (27 Oct: 'where are the sound effects?'), as the notes' sound list (rule 26)."""
    s2 = next(x for n, x, _ in SHOTS if n == 's2')
    ev = [('amb', 0.0, DUR, 0.55), ('artillery', 0.0, s2, 0.8), ('shots', 0.0, s2, 0.5)]
    ev += [('mg42', a, b, 0.45) for a, b in ACT.G_BURSTS] + [('mg42', a, b, 0.6) for a, b in ACT.P_BURSTS]
    ev += [('explosion', ACT.T_BLAST, None, 1.0), ('rubble', ACT.T_BLAST + 0.45, None, 0.55)]
    return ev


def soundtrack(stems=False):
    """Sam's voices, the barks, and his effects: the battle loud in shot 1; inside the bunker muffled under the
    dialogue, opening up only while the MG42 fires (Sam, 27 Oct)."""
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    s2 = int(next(x for n_, x, _ in SHOTS if n_ == 's2') * SR)
    for name, at, until, g in sound_events():
        if name == 'amb':                             # the battle all along: open air in shot 1, through concrete after
            x = _fit(sfx('battlefield-ambience.mp3', 10.0), DUR + 0.3)[:n]
            open_ = np.zeros(len(x))                 # 1 = open air: shot 1, and inside only while the MG42 fires
            open_[:s2] = 1.0
            for a, b in ACT.G_BURSTS + ACT.P_BURSTS:
                open_[int(a * SR):int(b * SR)] = 1.0
            k = np.hanning(int(0.3 * SR))
            open_ = np.clip(np.convolve(open_, k / k.sum(), 'same'), 0, 1)   # a quick swell in and out
            open_[:s2] = 1.0                         # the cut to inside is a hard cut
            x = open_ * x + (1 - open_) * 0.3 * _muffle(x)   # muffled and low under the dialogue (Sam, 27 Oct)
            rest[:len(x)] += x * g
        elif name in ('artillery', 'shots'):
            x = _fit(sfx('field-artillery.mp3' if name == 'artillery' else 'distant-shots.mp3'), until - at, 0.08)
            filmkit.place(rest, x, at=at, sr=SR, gain=g)
        elif name == 'mg42':                         # the rapid burst in Sam's file (2.8-5.0 s), cut to each burst
            filmkit.place(rest, _fit(sfx('mg42.mp3', 2.8, 5.0), until - at), at=at, sr=SR, gain=g)
        elif name == 'explosion':
            filmkit.place(rest, sfx('explosion.mp3'), at=at, sr=SR, gain=g)
        elif name == 'rubble':
            filmkit.place(rest, sfx('rubble-slide.mp3'), at=at, sr=SR, gain=g)
    rest *= 10 ** ((MA.LINE_LUFS - 4 - MA.lufs(rest[:int(DUR * SR)])) / 20)   # effects a little under the voices
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults += E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# ------------------------------------------------------------------------------------------------ the audit
def scene(t, faces=None):
    """Everyone and everything solid at time t, as picture(t) places them (audit.py, rules 5 and 6); the set's walls
    and things join by themselves (sets.solids, rule 12). `faces` collects each face drawn for voices.py."""
    import audit
    cam = cam_for(t) if shot_of(t) != 's1' else None
    out = []
    if cam is None:
        return out
    for a in ACT.everyone(t):
        if not on_screen(cam, a):
            continue
        h = PC.HEIGHTS.get(CAST[a.who]['name'], 1.75)
        out.append(audit.Thing(a.who, audit.placed(a.who, a.j, a.x, a.z, _dir(a.facing), h, sp=CAST[a.who])))
        if faces is not None and a.who != 'patriot':  # the Patriot's mouth is under the balaclava
            sp, _ = face(a, t, cam)
            yaw = view_yaw(cam, a.x, a.z, a.head_facing if a.head_facing is not None else a.facing)
            Xf, Yf, s, e, c = _tilt(cam, a.x, a.z, CAST[a.who])
            faces.append((a.who, sp['mouth'], yaw, 2 * s * CAST[a.who].get('hh', 90)))
    return out


def mouths_seen(t):
    faces = []
    scene(t, faces)
    return faces


def audits():
    """The general audit: each person alone over every frame they are on screen; the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            a = next(x for x in ACT.everyone(t) if x.who == who)
            draw_actor(lay, cam_for(t), a, t)
            return lay
        return draw
    actors = {}
    for who in WHO:
        for shot, a, b in SHOTS[1:]:
            ts = [i / FPS for i in range(int(a * FPS), int(b * FPS)) if shot_of(i / FPS) == shot
                  and on_screen(cam_for(i / FPS), next(x for x in ACT.everyone(i / FPS) if x.who == who))]
            if ts:
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=STILL_OK, allow=AUDIT_ALLOW)
    faults += filmkit.check_eyelines(allow=LOOKS_OK)
    faults += moves.audit()
    return faults


STILL_OK = ()
LOOKS_OK = [('patriot', 22.9, 24.3, 'he looks round: "the Free Speech Police are everywhere" (ACT.LOOKS_ROUND)')]
AUDIT_ALLOW = [   # (name [shot], from, to, why): on purpose
    ('gunner [s8]', ACT.T_BLAST, ACT.T_BLAST + ACT.G_FLIGHT + 0.1, 'thrown across the room by the blast (Sam, 27 Oct)'),
    ('loader [s8]', ACT.T_BLAST, ACT.T_BLAST + ACT.L_FLIGHT + 0.1, 'knocked back by the blast, staggering'),
    ('loader [s8]', 31.9, 32.1, 'a straight turn to face the gun (house standard: one drawing to the other)'),
    ('gunner [s8]', 31.9, 32.1, 'a straight turn to face the gun (house standard: one drawing to the other)'),
    ('gunner [s9]', 39.2, 40.9, 'the push-in: the camera turns and zooms, so every shape moves'),
    ('loader [s9]', 39.2, 40.9, 'the push-in: the camera turns and zooms, so every shape moves'),
    ('patriot [s9]', 39.2, 40.9, 'the push-in: the camera turns and zooms, so every shape moves'),
]


def _fx_cam():
    return SETS.Cam((0.0, 1.5, -3.0), (0.0, 1.5, 0.0), focal=1000)


EFFECTS[:] = [
    ('muzzle flash', 'burst', lambda im: PC.PC.muzzle_flash(B.Pen(im, S3.FLAT), (540, 960), (1.0, 0.0), 120, False, 3)),
    ('muzzle flash beside the lens (shot 9)', 'burst', lambda im: _edge_flash(im, 540, 960, 5)),
    ('the blast at the slit', 'burst', lambda im: PFX.FX.flash(im, _fx_cam(), (0.0, 1.5, 0.0), 1.6, seed=3)),
    ('a dust puff', 'smoke', lambda im: PFX.draw_puff(im, _fx_cam(), ((0.0, 1.5, 0.0), 0.4, 200, 7))),
    ('a shell burst on the beach', 'burst', lambda im: COAST.burst(im, COAST.cam(1.0), S3.pen(im), 1.05, 1.0, -20, 60,
                                                                    'sand')),
]


def cast_sheet(out):
    PC.sheet(out)


def LINE_SUBJECTS():
    return PC.LINE_SUBJECTS()


_BLACK = "his black balaclava and jacket count as ink, so the check's 'house' weight is the jacket (22 px): his real outlines read as thin"
LINE_OK = [('patriot', 'line weight', x, y) for x, y in ((485, 182), (583, 183), (495, 210), (574, 210), (321, 616),
                                                         (743, 615), (767, 615))] + \
          [('gunner', 'line weight', 584, 181)]
LINE_OK_WHY = {'patriot': _BLACK, 'gunner': 'the helmet rim on the approved cast drawing (cast stage, 27 Oct)'}


def stills_sheet(out, times):
    from PIL import ImageDraw, ImageFont
    tiles = []
    for t in times:
        im = frame_image(t).convert('RGB').resize((360, 640))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 150, 30), fill=(0, 0, 0))
        d.text((6, 4), f'{shot_of(t)}  {t:.1f}s', fill=(255, 255, 255),
               font=ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 18))
        tiles.append(im)
    cols = min(5, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 364 + 4, rows * 644 + 4), (255, 255, 255))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, (4 + (i % cols) * 364, 4 + (i // cols) * 644))
    sheet.save(out, quality=86)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        B.SS = 1
        stills_sheet(a[1], [float(x) for x in a[2:]] or [(s[1] + s[2]) / 2 for s in SHOTS])
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = audits()
        import audit
        f += [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)   # --nostamp: a clip to splice into a final has no overlay


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)                 # natural arms and legs: one outline at the shoulder, smooth shaped legs (Cry Minister)
import moves                     # noqa: E402,F401
import perform                   # noqa: E402,F401

if __name__ == '__main__':
    main()
