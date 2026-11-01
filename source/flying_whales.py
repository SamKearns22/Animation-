#!/usr/bin/env python3
"""Flying Whales: the film file (copied from source/satire_template.py, 1 Nov; no cast: no people, rule 16 of the
brief). Two shots, hard cut between them:
  'under'  0-5.6 s   the opener under the sea (source/flying_whales_opener.py, its camera swings round the pod);
  'rig'    5.6-17.6  the rig scene, one locked camera (flying_whales_sea.CAM): sky and sea (flying_whales_sea), the rig
                     in 31 breakable pieces (flying_whales_rig), the whales' paths and the hits (built next).
Then finish.py adds the Hook Text ("Blue Planet III looks 🔥🔥🔥", --y 352, the whole video) and the sign-off.
24 fps, not the house 12: the opener's camera swings round the pod and the specks in the water strobe at 12 (each
drawing jumps several speck-widths), and the whales cross the rig scene fast; motion like this is shot on ones.
Guide: guides/satire.md; notes: notes/flying-whales.md.

    python3 source/flying_whales.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/flying_whales.py check                     the plan checks (also run by preflight.py)
    python3 source/flying_whales.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  canvas size, supersampling flag (no people in this film)
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list
import flying_whales_opener as O  # noqa: E402  the opener under the sea
import flying_whales_sea as SEA  # noqa: E402  the rig scene's sky and sea
import flying_whales_rig as R    # noqa: E402  the rig
import flying_whales_paths as PATHS  # noqa: E402  the whales' paths in the rig scene
import flying_whales_fx as FX    # noqa: E402  the effects (burst, splashes, fire, smoke, bits)
import flying_whales_wreck as WRECK  # noqa: E402  what breaks when, the pieces falling, the finale
import whale as W                # noqa: E402

FPS, SR = 24, MA.SR

# =============================================== STORY ==============================================================
NAME = 'flying-whales'
TITLE = ()                                        # no title (Sam, 15 Oct)
CAST = {}                                         # no people (brief 14)
LOOKS_AT = {}
# Attenborough (Sam records it; 'audio' then times the line to source/audio/flying-whales-1.m4a). Placeholder times
# until then: subtitles in chunks of two to five words, each on its first word (guides/satire.md, Subtitles).
LINES = [dict(who='narrator', text='This series, we will see animal behaviour we could scarcely have imagined.',
              start=O.LINE[0], end=O.LINE[1], audio='flying-whales-1')]
CHUNKS = [(0.3, 'This series,'), (1.3, 'we will see'), (2.2, 'animal behaviour'), (3.3, 'we could scarcely'),
          (4.2, 'have imagined.')]       # placeholder word times; re-pinned to the recording (PINS) when it arrives
CUT = O.CUT
RIG_LEN = 12.0                                    # "Let's do the 12 second shot" (brief 19)
SHOTS = [('under', 0.0, CUT), ('rig', CUT, CUT + RIG_LEN)]
DUR = CUT + RIG_LEN
# Rule 1: the plan in metres lives in the scene modules (opener: FORMATION, CAM_KEYS; rig: PARTS, sea: CAM); the notes
# file has it in words. No rooms or people: the template's PLAN is left empty.
PLAN = dict(ROOMS={}, OPENINGS={}, THINGS={}, PEOPLE={}, CAMS={}, GROUPS={})
BENCHMARK = []                                    # rule 3: done in the notes (B1-B10, Showstoppers) for both sets
SHOT_CAST = {}                                    # no people
HOOK = ('Blue Planet III looks 🔥🔥🔥', {'y': 352, 'until': 5.6})   # exactly as finish.py will be given it; off at the cut (Sam, 2 Nov: it blocked the rig scene)
KEEP_CLEAR = []
PROP_SIZES = []
OUTFIT, HEIGHTS = {}, {}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS, ALLOWED_POPS, SET_EXCLUDE = [], [], []
TOUCHES, FREE_MOVES, SOUND_SOURCES = [], [], {}
EFFECTS = [('water burst', 'burst', FX.test_draw(0.3)),          # rule 15: lumpy, never a star (viewchecks)
           ('water burst falling back', 'splash', FX.test_draw(1.1)),
           ('foam ring', 'foam', FX.test_draw(0.8, 'foam')),
           ('fireball bursting', 'burst', FX.test_draw(0.12, 'fireball')),
           ('fireball', 'burst', FX.test_draw(0.4, 'fireball')),
           ('fireball burning out', 'burst', FX.test_draw(0.85, 'fireball')),
           ('black smoke clumps', 'smoke', FX.test_draw(0.0, 'smoke')),
           ('steam', 'smoke', FX.test_draw(0.0, 'steam')),
           ('dust', 'smoke', FX.test_draw(0.0, 'dust')),
           ('deck fire', 'fire', FX.test_draw(1.0, 'fire')),
           ('splash (a falling piece)', 'burst', FX.test_draw(0.3, 'splash')),
           ('splash falling back', 'splash', FX.test_draw(0.9, 'splash')),
           ('crown splash (the finale)', 'burst', FX.test_draw(0.5, 'crown')),
           ('crown splash falling back', 'splash', FX.test_draw(1.4, 'crown')),
           ('flying bits', 'debris', FX.test_draw(0.0, 'bits'))]
JOKE_PROPS = []
# ====================================================================================================================

BLACK_AT = DUR
for ln in LINES:                                  # time the line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        v = MA.line(ln['audio'])
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


BLOW_AFTER = 0.9                                  # s after breaking the surface: each whale puffs spray (Showstopper 5)


def rig_whales(ts):
    """[(distance, sprite)] for every whale and its water burst at rig-scene time ts, for R.draw to sort among the
    rig's pieces; and the foam patches on the sea."""
    cam = SEA.CAM
    extra, foam = [], []
    for k in PATHS.KEYS:
        if not PATHS.on_screen(k, ts):
            continue
        ps = PATHS.pose(k, ts)
        sz = W.PATTERNS[k]['size']
        age = ts - PATHS.SURFACE[k]
        blow = ts - PATHS.SURFACE[k] - BLOW_AFTER
        spr = W.draw(cam, ps, pattern=k, t=ts + k * 0.37, flap=1.0, beat=1.0, tint=SEA.DUSK_TINT, phase=k * 0.9,
                     cut_z=0.0, blow=blow if 0 <= blow <= 1.6 else None)
        d = float(np.linalg.norm(ps.pos - cam.pos))
        if spr:
            extra.append((d, spr))
        if -0.4 <= age <= 2.4:                                   # the burst and its foam
            v = PATHS.vel(k, PATHS.SURFACE[k])
            head = v[:2] / (np.linalg.norm(v[:2]) + 1e-9)
            hole = PATHS.pos(k, PATHS.SURFACE[k]) * np.array([1, 1, 0])
            lumps = FX.burst_parts(cam, ps, sz, age, 11 + k * 7, head, hole)
            dist = lambda l: float(np.linalg.norm(np.asarray(l[0]) - cam.pos))
            for side, keep in ((d + 0.05, lambda l: dist(l) >= d), (d - 0.05, lambda l: dist(l) < d)):
                spr = FX.lumps_sprite(cam, [l for l in lumps if keep(l)], side)
                if spr:
                    extra.append((side, spr))
            foam += FX.foam_ring(cam, hole, age, 11 + k * 7, sz)
    return extra, foam


def rig_scene(t, ss=1):
    """The rig scene at film time t: sea and sky (lit orange under the fires), foam on the sea, then the rig (pieces
    moved, holed or gone: flying_whales_wreck) with the whales, their bursts and every effect sorted in among its
    pieces by distance; then the camera's jolt. The story clock stands still for two frames at each main hit."""
    real = t - CUT
    ts = WRECK.story(real)
    extra, foam = rig_whales(ts)
    fx, fx_foam, glows = WRECK.effects(ts)
    xf, gone, swap = WRECK.rig_state(ts)
    sea = SEA.paint(ts, glows=glows, ss=ss).convert('RGBA')
    FX.draw_foam(sea, SEA.CAM, foam + fx_foam)
    img = R.draw(sea, ts, xf=xf, gone=gone, extra=extra + fx, swap=swap).convert('RGB')
    return WRECK.shift(img, *WRECK.shake(real))


def picture(t):
    """The frame WITHOUT captions (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return Image.new('RGB', O.SIZE, (0, 0, 0))
    if shot_of(t) == 'under':
        return O.frame(t, ss=B.SS)[0]
    return rig_scene(t, ss=max(1, B.SS))


def caption_at(t):
    for i, (a, txt) in enumerate(CHUNKS):
        nxt = CHUNKS[i + 1][0] if i + 1 < len(CHUNKS) else LINES[-1]['end'] + 0.25
        if a + 0.1 <= t < nxt + (0.1 if i + 1 < len(CHUNKS) else 0.0):
            return txt
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            img = img.convert('RGBA')
            keep, B.SS = B.SS, 1              # the scenes hand back 1080 x 1920 whatever the supersampling
            PP.caption(img, c)
            B.SS = keep
    return img


def frame_image(t):
    return overlay(picture(t), t)


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # voices only (no sound effects until Sam asks)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    if any(ln['_voice'] is None for ln in LINES):
        print('NOTE: no recording yet for the Attenborough line (placeholder times)')
    mix, voice, rest = soundtrack(stems=True)
    if np.abs(mix).max() > 1e-6:
        faults += filmkit.hiss_check(mix, SR, BLACK_AT)
        for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                         cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
            print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def main():
    a = sys.argv[1:]
    if a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        print('checks: clean')
    elif a[0] == 'final':
        small = '--small' in a
        # the scenes paint at 1080 x 1920 themselves; ss 2 (supersampled lines) only for the full-size final
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


if __name__ == '__main__':
    main()
