#!/usr/bin/env python3
"""Quick video: a short TikTok film from one brief file (two people, a background, captions, Sam's recordings).

A thin layer over the series' own parts, so it looks like ours: burnham.py people (flat shapes, black outlines, plain
circle hands), figure.py (arms solved and guarded), mouths.py (lip sync), mossad_audio.py (voices cleaned and levelled),
the standard title and captions, and preflight.py (the checks and the contact sheet). Nothing here needs reading:
fill in a brief (prompts/quick-example.json) and run the commands in guides/quick-video.md.

    python3 source/quick.py check BRIEF.json             seconds: the brief, captions, timing, safe area, recordings
    python3 source/quick.py sheet BRIEF.json OUT_DIR     about 2 minutes: every body check + ONE contact sheet to look at
    python3 source/quick.py final BRIEF.json OUT.mp4 [--scale 0.5] [--secs 3]    the film (1080 x 1920 by default)
"""
import json
import math
import os
import subprocess
import sys
import time
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import mossad as M           # noqa: E402  (brows, tilted heads, hair styles, limiter: patched into burnham on import)
import figure as F           # noqa: E402
import mouths                # noqa: E402
import mossad_audio as MA    # noqa: E402
from ed import INK           # noqa: E402

mouths.install(B)
FPS, SR = 12, MA.SR
SAFE = (60, 310, 900, 1500)
S = 0.8                        # the people's scale
FY = 1420                      # the floor line
NECK_Y = FY - F.SOLE_Y * S     # neck base height
XS = {'A': 340, 'B': 740}
SKINS = {'pale': B.PALE, 'pink': B.PINK, 'olive': B.OLIVE, 'brown': B.BROWN, 'deep': B.DEEP}
GESTURES = ('rest', 'talk', 'point', 'shrug', 'hips', 'wave', 'clasped')
FACES = ('neutral', 'angry', 'happy', 'shock')
HAIRS = ('crop', 'side', 'bald', 'bob', 'long', 'swept', 'wisps', 'blonde')
JAWS = ('round', 'square', 'soft', 'long')
OUTFITS = ('suit', 'jumper', 'dress', 'blouse')

BRIEF = {}
LINES, SHOT_LIST, SHOTS, TRACK, BLINKS = [], [], [], {}, {}
BG, TITLE, BLACK_AT, DUR = 'room', '', 0.0, 0.0


def col(v, default=(128, 128, 128)):
    if isinstance(v, (list, tuple)):
        return tuple(v)
    if isinstance(v, str) and v.startswith('#') and len(v) == 7:
        return tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    return SKINS.get(v, default)


# -------------------------------------------------------------------------------------------- the circle hand

def chand(p, x, y, skin, r=26):
    p.ell(x, y, r, r, skin, INK, 2.4)


def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    chand(p, wr[0] + d[0] / n * 12, wr[1] + d[1] / n * 12, skin)


B.gesture_hand = gesture_hand          # every hand is a plain circle (props are laid over it)


# ------------------------------------------------------------------------------------------------- the brief

def configure(path):
    """Read the brief and set up the module (timeline, mouth tracks, blinks). Everything else reads these."""
    global BRIEF, LINES, SHOT_LIST, SHOTS, TRACK, BLINKS, BG, TITLE, BLACK_AT, DUR
    BRIEF = json.load(open(path))
    BG, TITLE = BRIEF.get('background', 'room'), BRIEF.get('title', '')
    LINES = []
    for i, ln in enumerate(BRIEF['lines']):
        ln = dict(ln)
        ln['who'] = ln.get('who', 'A')
        if ln.get('audio'):
            ap = ln['audio'] if os.path.isabs(ln['audio']) else os.path.join(ROOT, ln['audio'])
            ln['_name'] = os.path.splitext(os.path.basename(ap))[0]
            ln['_path'] = ap
            if os.path.exists(ap) and os.path.dirname(ap) == os.path.join(HERE, 'audio'):
                a = MA.line(ln['_name'])
                ln['_len'] = len(a) / SR
                st = MA.pauses(a, 0.12) or [(0.0, ln['_len'])]
                hop = SR // 100
                env = np.array([np.sqrt(np.mean(a[k:k + hop] ** 2)) for k in range(0, len(a) - hop, hop)])
                env = env / (env.max() + 1e-9)
                ln['_speech'] = st[-1][1]
                ln['_track'] = mouths.track(ln['text'], st, env, 100)
            else:
                ln['_missing'] = True
        if '_track' not in ln:                       # no recording: the words at a natural pace
            words = ln['text'].split()
            d = max(1.0, len(words) / 3.3)
            ln['_len'] = ln['_speech'] = d
            ln['_track'] = mouths.track(ln['text'], [(0.0, d)])
        ln['end'] = ln['start'] + ln['_speech'] + 0.12
        ln['_track'] = [(a + ln['start'], b + ln['start'], s) for a, b, s in ln['_track']]
        LINES.append(ln)
    LINES.sort(key=lambda l: l['start'])
    last = max(l['end'] for l in LINES)
    BLACK_AT = float(BRIEF.get('end', round(last + 1.0, 2)))
    DUR = BLACK_AT + 0.35
    shots = BRIEF.get('shots') or [{'cam': 'two', 'start': 0, 'end': 'end'}]
    SHOT_LIST = []
    for s in shots:
        s = dict(s)
        s['end'] = BLACK_AT if s['end'] == 'end' else float(s['end'])
        SHOT_LIST.append(s)
    SHOTS = [(s['cam'], s['start'], s['end']) for s in SHOT_LIST]
    TRACK = {w: [x for ln in LINES if ln['who'] == w for x in ln['_track']] for w in 'AB'}
    BLINKS = {w: F.blinks(7 if w == 'A' else 11, 0.5, DUR, talking=True) for w in 'AB'}


def cast(who):
    c = BRIEF.get('characters', {}).get(who, {})
    d = dict(skin='pale', hair='crop', hair_c='#503c2c', jacket='#2e5c46' if who == 'A' else '#7a3a4a', trousers='#26262e',
             outfit='suit', jaw='round', glasses=False, hw=68, hh=88)
    d.update(c)
    return d


# ------------------------------------------------------------------------------------------ people and poses

def state(who, t):
    c = cast(who)
    other = 'B' if who == 'A' else 'A'
    toward = 1 if who == 'A' else -1
    near = 'R' if toward > 0 else 'L'
    sp = dict(skin=col(c['skin']), hw=c['hw'], hh=c['hh'], jaw=c['jaw'], hair=c['hair'], hair_c=col(c['hair_c']),
              jacket=col(c['jacket']), trousers=col(c['trousers']), outfit=c['outfit'], glasses=c['glasses'],
              dress=col(c['jacket']), full=True, pose='custom', name=who)
    for k in ('beard', 'beard_c', 'tie', 'nose', 'age', 'brow_c', 'shirt', 'earring'):
        if k in c:
            sp[k] = col(c[k]) if k.endswith('_c') or k in ('tie', 'shirt') else c[k]
    speaking = next((l for l in LINES if l['who'] == who and l['start'] - 0.1 <= t < l['end'] + 0.3), None)
    heard = next((l for l in LINES if l['who'] != who and l['start'] - 0.1 <= t < l['end'] + 0.3), None)
    face = (speaking.get('face', 'neutral') if speaking else (heard.get('react', 'neutral') if heard else 'neutral'))
    g = speaking.get('gesture', 'talk') if speaking else 'rest'
    rig = F.Rig(sp)
    w = math.sin(2 * math.pi * 1.1 * t + (0 if who == 'A' else 2))
    sh = rig.shoulder(near)
    if g == 'point':
        arms = rig.pose('point', side=near, target=(toward * 700, -60))
    elif g == 'talk':
        arms = dict(rig.pose('sides'), **{near: rig.arm(near, (sh[0] + toward * (46 + 12 * w), sh[1] + 330 - 12 * w), 'palm', 'depth')})
    elif g == 'wave':
        arms = dict(rig.pose('sides'), **{near: rig.arm(near, (sh[0] + toward * (40 + 25 * w), sh[1] - 110), 'palm', 'down')})
    elif g == 'shrug':
        sp['shoulder_dy'] = -10
        rig = F.Rig(sp)
        arms = {s: rig.arm(s, (rig.shoulder(s)[0] + (-1 if s == 'L' else 1) * 150, rig.shoulder(s)[1] + 120 + 8 * w), 'palm', 'down')
                for s in 'LR'}
    elif g == 'hips':
        arms = rig.pose('hips')
    elif g == 'clasped':
        arms = rig.pose('clasped')
    else:
        arms = rig.pose('sides')
    sp['arms'] = arms
    shape = mouths.at(TRACK[who], t)
    base = {'happy': 'smile', 'angry': 'set', 'shock': 'v:O'}.get(face, 'set')
    sp['mouth'] = base if shape == 'rest' else 'v:' + shape
    if face == 'angry':
        sp['brows'] = 'fierce'
    elif face == 'happy':
        sp['brows'] = 'joy'
    elif face == 'shock':
        sp['brow_raise'] = 6
    sp['blink'] = F.blinking(t, BLINKS[who])
    sp['look'] = F.look_at(XS[who], XS[other])
    sp['breath'] = F.breath(t, 4.0, 1.5, 0.0 if who == 'A' else 0.4)
    return sp


# ------------------------------------------------------------------------------------------------ camera, set

def shot_at(t):
    for s in SHOT_LIST:
        if s['start'] <= t < s['end']:
            return s
    return SHOT_LIST[-1]


def cam_for(t):
    s = shot_at(t)
    k = (t - s['start']) / max(0.1, s['end'] - s['start'])
    push = 1 + s.get('push', 0.0) * k
    if s['cam'] == 'two':
        return B.Cam(1.0 * push, 540, 960 + 20 * (push - 1) * 0)
    z = s.get('zoom', 2.0) * push
    return B.Cam(z, XS[s['cam']], NECK_Y - 150 * S + 160 / z)


def head_box(who, cam):
    x, y = cam.P(XS[who], NECK_Y - 150 * S)
    r = cast(who)['hw'] * S * cam.z
    rh = cast(who)['hh'] * S * cam.z
    return x / B.SS - r, y / B.SS - rh, x / B.SS + r, y / B.SS + rh


def background(img, cam):
    p = B.Pen(img, cam)
    box = lambda x0, y0, x1, y1, f: p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], f, INK, 3)
    spec = BG
    if spec.startswith('#'):
        box(-600, -600, 1700, 2600, col(spec))
        box(-600, FY - 40, 1700, 2600, tuple(int(c * 0.8) for c in col(spec)))
    elif spec == 'street':
        box(-600, -600, 1700, 1000, (150, 200, 235))
        for x, w, h, c in [(-200, 380, 760, (178, 120, 98)), (180, 300, 900, (120, 140, 168)), (480, 340, 700, (200, 170, 120)),
                           (820, 380, 840, (150, 110, 130))]:
            box(x, 1100 - h, x + w, 1100, c)
            for wy in range(1100 - h + 60, 1060, 130):
                for wx in range(x + 40, x + w - 60, 100):
                    box(wx, wy, wx + 56, wy + 80, (240, 232, 170))
        box(-600, 1100, 1700, 1280, (170, 170, 176))
        box(-600, 1280, 1700, 2600, (84, 84, 92))
    elif spec == 'office':
        box(-600, -600, 1700, FY - 40, (210, 216, 222))
        box(60, 520, 460, 960, (170, 210, 235))
        for y in range(550, 960, 56):
            p.line([(60, y), (460, y)], INK, 2)
        box(620, 600, 1020, 740, (240, 240, 240))
        box(-600, FY - 40, 1700, 2600, (126, 104, 86))
    elif spec == 'cafe':
        box(-600, -600, 1700, FY - 40, (214, 190, 156))
        box(60, 480, 520, 800, (40, 56, 48))
        for i in range(4):
            p.line([(100, 540 + 60 * i), (260 + 60 * i, 540 + 60 * i)], (238, 238, 238), 3)
        box(-600, 1130, 1700, FY - 40, (120, 82, 56))
        box(-600, FY - 40, 1700, 2600, (90, 76, 70))
    else:  # room
        box(-600, -600, 1700, FY - 40, (232, 214, 170))
        box(120, 480, 460, 860, (170, 210, 235))
        p.line([(290, 480), (290, 860)], INK, 3)
        box(640, 540, 920, 760, (220, 150, 120))
        box(-600, FY - 40, 1700, 2600, (150, 110, 76))


# ------------------------------------------------------------------------------------------------ text layers

def caption(img, s, shout=False, bottom=1480):
    SS = B.SS
    d = ImageDraw.Draw(img)
    if shout:
        size = 120
        while size > 40:
            f = ImageFont.truetype(B.ANTON, size * SS)
            rows = B.wrap(s.upper(), f, 700 * SS)
            if len(rows) <= 2:
                break
            size -= 4
        for i, row in enumerate(rows):
            y = (bottom - 0.6 * size - size * 1.1 * (len(rows) - 1 - i)) * SS
            d.text((540 * SS, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=int(size * 0.07) * SS, stroke_fill=(0, 0, 0))
        return
    f = ImageFont.truetype(B.SANS, 50 * SS)
    rows = B.wrap(s, f, 700 * SS)
    for i, row in enumerate(rows):
        y = (bottom - 34 - 64 * (len(rows) - 1 - i)) * SS
        d.text((540 * SS, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5 * SS, stroke_fill=(0, 0, 0))


def caption_at(t):
    """(text) of the caption on screen at t, or None (also used by preflight.py)."""
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.25, nxt):
            return ln['text']
    return None


def frame_image(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas()
    background(img, cam)
    for who in 'AB':
        if abs(XS[who] - cam.cx) * cam.z > 540 + 130 * S * cam.z:
            continue                                      # out of the picture: not drawn
        B.person(img, cam, XS[who], NECK_Y, S, state(who, t), t)
    c = caption_at(t)
    if c:
        caption(img, c, next(l.get('shout', False) for l in LINES if l['text'] == c))
    if TITLE and t < 1.0:
        B.title(img, TITLE, alpha=1.0 if t < 0.7 else 1.0 - (t - 0.7) / 0.3, maxw=720)
    return img


# ------------------------------------------------------------------------------------------------------ sound

def sfx(kind, rng):
    if kind == 'thud':
        tt = np.arange(int(0.5 * SR)) / SR
        return np.sin(2 * np.pi * (140 * np.exp(-tt * 7) + 40) * tt) * np.exp(-tt * 9) + 0.25 * np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 30)
    if kind == 'ding':
        tt = np.arange(int(1.2 * SR)) / SR
        return sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((1320, 1), (2640, 0.4), (3960, 0.15))) * np.exp(-tt * 4) * 0.5
    if kind == 'whoosh':
        tt = np.arange(int(0.5 * SR)) / SR
        return np.convolve(rng.standard_normal(len(tt)), np.ones(40) / 40, mode='same') * np.sin(np.pi * tt / 0.5) ** 2 * 3
    if kind == 'bang':
        tt = np.arange(SR) / SR
        return (rng.standard_normal(len(tt)) * np.exp(-tt * 6) + np.sin(2 * np.pi * (90 * np.exp(-tt * 3) + 30) * tt) * np.exp(-tt * 5)) * 0.7
    return np.zeros(10)


def soundtrack(total=None):
    n = int((total or DUR) * SR)
    mix = np.zeros(n)
    rng = np.random.default_rng(5)
    for ln in LINES:
        if ln.get('_name') and not ln.get('_missing'):
            a = MA.line(ln['_name'])
            s = int(ln['start'] * SR)
            seg = a[:max(0, n - s)]
            mix[s:s + len(seg)] += seg
    for e in BRIEF.get('sfx', []):
        s = int(e['at'] * SR)
        seg = sfx(e['type'], rng)[:max(0, n - s)] * e.get('gain', 0.35)
        mix[s:s + len(seg)] += seg
    end = min(n, int(BLACK_AT * SR))
    if np.abs(mix[:end]).max() > 1e-6:
        for _ in range(3):                                # master: about -14 LUFS, peaks under -1 dBTP
            mix *= 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
            mix = M.limiter(mix, -2.6)
    k = int(0.005 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)             # hard cut to black: picture and sound together
    mix[end:] = 0
    return mix


# ------------------------------------------------------------------------------------------------------ checks

def check():
    bad, note = [], []
    for k in ('lines',):
        if k not in BRIEF:
            sys.exit(f'FAIL: the brief has no "{k}"')
    if BLACK_AT > 30:
        bad.append(f'the film is {BLACK_AT:.1f} s: keep it to 30 s or less (TikTok: first payoff by 8-10 s)')
    first = min(l['start'] for l in LINES)
    if first > 0.5:
        bad.append(f'the first line starts at {first:.2f} s: start it by 0.5 s')
    if not TITLE or len(TITLE) > 22:
        note.append('title missing or over 22 characters (it shrinks to fit)')
    f = ImageFont.truetype(B.SANS, 50)
    for i, ln in enumerate(LINES):
        n = f'line {i + 1} ({ln["who"]} "{ln["text"][:22]}", {ln["start"]:.2f}-{ln["end"]:.2f} s)'
        print(n)
        if ln['who'] not in ('A', 'B'):
            bad.append(f'{n}: who must be A or B')
        if ln.get('gesture', 'talk') not in GESTURES:
            bad.append(f'{n}: gesture must be one of {GESTURES}')
        for k in ('face', 'react'):
            if ln.get(k, 'neutral') not in FACES:
                bad.append(f'{n}: {k} must be one of {FACES}')
        if ln.get('audio') and ln.get('_missing'):
            bad.append(f'{n}: recording not found in source/audio/ ({ln["audio"]})')
        if not ln.get('audio'):
            note.append(f'{n}: no recording, so the film is silent there')
        rows = B.wrap(ln['text'], f, 700)
        wide = max(f.getbbox(r)[2] for r in rows)
        if not ln.get('shout') and (len(rows) > 2 or wide > 700 or max(len(r) for r in rows) > 42):
            bad.append(f'{n}: caption has {len(rows)} rows, {wide} px wide (max 2 rows, 700 px, 42 characters a row): shorten it')
        dur = ln['end'] - ln['start']
        if dur < 0.8 or len(ln['text'].split()) / dur * 60 > 220:
            note.append(f'{n}: too fast to read')
        if i and ln['start'] < LINES[i - 1]['end'] - 0.05:
            bad.append(f'{n}: starts before line {i} ends ({LINES[i - 1]["end"]:.2f} s): move it later')
    t = 0.0
    for s in SHOT_LIST:
        if abs(s['start'] - t) > 0.01:
            bad.append(f'the shots have a gap or overlap at {t:.2f} s')
        if s['cam'] not in ('two', 'A', 'B'):
            bad.append(f'shot cam must be two, A or B, not {s["cam"]}')
        if s['end'] - s['start'] > 8:
            note.append(f'shot at {s["start"]} s lasts {s["end"] - s["start"]:.1f} s: cut away within 6-8 s')
        t = s['end']
        B.SS = 1
        cam = cam_for(s['start'])
        for who in 'AB':
            if s['cam'] in ('two', who):
                x0, y0, x1, y1 = head_box(who, cam)
                if x0 < SAFE[0] or x1 > SAFE[2] or y0 < SAFE[1] or y1 > SAFE[3]:
                    bad.append(f'shot at {s["start"]} s: {who}\'s head leaves the safe area (lower the zoom)')
    if abs(t - BLACK_AT) > 0.01:
        bad.append(f'the shots end at {t:.2f} s but the film ends at {BLACK_AT:.2f} s (give the last shot "end": "end")')
    files = [l['_path'] for l in LINES if l.get('_path') and not l.get('_missing')]
    if len(files) > 1:
        import voices
        ms = [voices.measure(p) for p in files]
        for i, a in enumerate(ms):
            for b in ms[i + 1:]:
                if a['hash'] == b['hash'] or voices.similar(a, b) > 0.97:
                    bad.append(f'{os.path.basename(a["path"])} and {os.path.basename(b["path"])} are the same take')
    print('\n'.join('FAIL: ' + m for m in bad + []), flush=True)
    print('\n'.join('note: ' + m for m in note))
    print('CHECKS PASSED' if not bad else f'{len(bad)} FAIL(S): fix them and run check again')
    return not bad


def sheet(out_dir):
    """preflight.py on this film: the body checks on every third frame and one contact sheet with the safe area."""
    os.makedirs(out_dir, exist_ok=True)
    env = dict(os.environ, QUICK_BRIEF=os.path.abspath(sys.argv[2]))
    r = subprocess.run([sys.executable, os.path.join(HERE, 'preflight.py'), 'quick', out_dir, '--audit'], cwd=HERE, env=env,
                       capture_output=True, text=True)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    print('\n'.join(lines[-25:]))


# -------------------------------------------------------------------------------------------- render

def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, scale=1.0, secs=None):
    import imageio_ffmpeg
    from multiprocessing import Pool
    size = (int(1080 * scale) // 2 * 2, int(1920 * scale) // 2 * 2)
    ss = 2 if scale > 0.6 else 1
    total = secs or DUR
    n = int(round(total * FPS))
    wav = out + '.wav'
    MA.write_wav(wav, soundtrack(total))
    t0 = time.time()
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 60 == 0:
                print(f'frame {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.2f} MB, {n} frames, {time.time() - t0:.0f} s)')


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ('check', 'sheet', 'final'):
        print(__doc__)
        return
    configure(a[1])
    if a[0] == 'check':
        sys.exit(0 if check() else 1)
    elif a[0] == 'sheet':
        sheet(a[2])
    else:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        secs = float(a[a.index('--secs') + 1]) if '--secs' in a else None
        render(a[2], scale, secs)


if os.environ.get('QUICK_BRIEF'):                 # imported by preflight.py (a separate process)
    configure(os.environ['QUICK_BRIEF'])

if __name__ == '__main__':
    main()
