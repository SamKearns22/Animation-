#!/usr/bin/env python3
"""ai_tells_lab: Job K's test bench (Sam, 10 Nov: "reduce the 'AI ick' factor without breaking the overall style").

It never changes a film, the kit or the rulebook. It draws the finished films' own frames twice, today and with one
proposed change swapped in while it draws, so each proposal can be judged before anything is adopted.
Pictures and clips go to review/job-k/ (off GitHub).

MAP
  cel()            proposal: shading as one hard-edged shadow shape (the kit's soft() and limbs' shading, unblurred)
  quiet_bg()       proposal: background lines drawn in a darker shade of their own colour, not black
  head_life        proposal: a talking head that tilts, settles and nods on the voice's stresses (pose to pose)
  sheet OUT.jpg    the before/after check sheet (three rows: shading, head, background lines)
  clip OUT.mp4     Islamocommunism 36-42 s (one unbroken close-up): today | with head acting, side by side, with the film's sound
  shading OUT.jpg  proposal 2's check (built, ed.HARD): the old airbrushed shading vs the hard-edged shapes, crops
  rigclip OUT.mp4  proposal 1's check (built, headlife.py + views.Rolled): Islamocommunism 36-42 s, today | the rig's
                   own head acting from the voice, side by side, with the film's sound
  shirt OUT.jpg    proposal 4's check (built, ad_vanced_notice_cast.BENT): the check shirt flat vs bent, four views
  driver OUT.jpg   proposal 5's sheet (built: patriots4_cast.lop, views.standing's weight_leg): the pump driver
                   with the options off | on, whole body, then the face full size

  python3 source/ai_tells_lab.py sheet review/job-k/before-after.jpg
  python3 source/ai_tells_lab.py clip review/job-k/talking-head.mp4
  python3 source/ai_tells_lab.py driver review/job-k/driver-lopsided.jpg
"""
import contextlib
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
OUT = os.path.join(ROOT, 'review', 'job-k')
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
SS = 2


# ------------------------------------------------------------------------------------------------ swaps
@contextlib.contextmanager
def swapped(pairs):
    """pairs: (module, name, new value), put back afterwards whatever happens."""
    old = [(m, n, getattr(m, n)) for m, n, _ in pairs]
    try:
        for m, n, v in pairs:
            setattr(m, n, v)
        yield
    finally:
        for m, n, v in old:
            setattr(m, n, v)


def cel():
    """Every module's soft() (and limbs' arm shading) drawn with a hard edge: the same shadow shape, no airbrush."""
    import ed
    import limbs
    orig, orig_shade = ed.soft, limbs._shade

    def hard(img, cam, pts, colr, alpha, blur=6):
        return orig(img, cam, pts, colr, alpha, 0)

    def hard_shade(lay, cam, pts, alpha, blur):
        return orig_shade(lay, cam, pts, alpha, 0.01)
    pairs = [(m, 'soft', hard) for m in list(sys.modules.values()) if getattr(m, 'soft', None) is orig]
    return swapped(pairs + [(limbs, '_shade', hard_shade)])


def quiet_bg(bg, people_mask):
    """Background ink lines turned into a darker shade of the colour they sit on (people keep their black line)."""
    import cv2
    a = np.asarray(bg.convert('RGB')).astype(np.float32)
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    ink = lum < 62
    fill = a.copy()
    fill[ink] = np.nan
    base = cv2.medianBlur(np.nan_to_num(fill, nan=0).astype(np.uint8), 11).astype(np.float32)
    k = np.clip((62 - lum) / 40, 0, 1)[..., None] * (~people_mask)[..., None]
    out = a * (1 - k) + base * 0.55 * k
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


# ------------------------------------------------------------------------------------------------ head acting
def accents(env, fps=12, gap=5):
    """Drawing numbers where the voice lands on a stress: the loudest drawing within +-3, well above the speech's
    usual loudness, at least `gap` drawings apart."""
    voiced = env[env > 0.01]
    if not len(voiced):
        return []
    bar = 1.25 * float(np.median(voiced))
    out, last = [], -99
    for i in range(len(env)):
        lo, hi = max(0, i - 3), min(len(env), i + 4)
        if env[i] >= bar and env[i] == env[lo:hi].max() and i - last >= gap:
            out.append(i)
            last = i
    return out


def envelope(film_mp4, t0, t1, fps=12):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', film_mp4, '-ac', '1',
                          '-ar', '12000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = 12000 // fps
    return np.array([np.sqrt(np.mean(x[i * n:(i + 1) * n] ** 2)) for i in range(len(x) // n)])


class HeadLife:
    """Pose-to-pose head acting for a talking head: a new tilt every phrase or so, reached in three drawings with a
    small overshoot and then HELD (never a sine wave, never perfectly still); a short nod on each stressed syllable;
    the shoulders follow the head a drawing later, at a third of the amount."""
    def __init__(self, env, fps=12, seed=3):
        rng = np.random.default_rng(seed)
        n = len(env)
        self.fps = fps
        self.roll = np.zeros(n)
        self.nod = np.zeros(n)
        keys, i, prev = [], 0, 0.0
        while i < n:
            tgt = prev
            while abs(tgt - prev) < 2.0:
                tgt = float(rng.choice([-4.0, -2.5, -1.0, 1.5, 3.0, 4.0]))
            keys.append((i, tgt))
            prev = tgt
            i += int(rng.integers(14, 30))            # 1.2-2.5 s held
        a = 0.0
        for k, (i0, tgt) in enumerate(keys):
            i1 = keys[k + 1][0] if k + 1 < len(keys) else n
            for j in range(i0, i1):
                u = j - i0
                if u < 3:
                    w = [0.35, 0.85, 1.08][u]          # three drawings in, a little past the mark
                else:
                    w = 1.0
                self.roll[j] = a + (tgt - a) * w
            a = tgt
        for i0 in accents(env):
            for u, d in enumerate([0.6, 1.0, 0.55, 0.2]):
                if i0 + u < n:
                    self.nod[i0 + u] = max(self.nod[i0 + u], d)

    def at(self, i):
        i = max(0, min(len(self.roll) - 1, i))
        return self.roll[i], self.nod[i], self.roll[max(0, i - 1)] / 3.0


def act_head(lay, pivot, head_w, roll, nod, body_roll):
    """The person's layer with the head turned by `roll` degrees about the neck and dipped by `nod`, the body by
    `body_roll` about the bottom of the frame."""
    W, H = lay.size
    px, py = pivot
    # head: above the neck, within the head's width, feathered so the collar does not tear
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle([px - head_w, 0, px + head_w, py], fill=255)   # hard cut across the neck
    head = lay.copy()
    head.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))))
    body = lay.copy()
    body.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), 255 - np.asarray(m))))
    dip = nod * head_w * 0.045
    head = head.rotate(roll, resample=Image.BICUBIC, center=(px, py), translate=(0, dip))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    out.alpha_composite(body)
    band = Image.new('L', (W, H), 0)                  # the top of the neck, unturned, under the turned head (no gap)
    ImageDraw.Draw(band).rectangle([px - head_w, py - head_w * 0.10, px + head_w, py], fill=255)
    neck = lay.copy()
    neck.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(band))))
    out.alpha_composite(neck)
    out.alpha_composite(head)
    sway = body_roll * W * 0.004
    return out.rotate(body_roll * 0.5, resample=Image.BICUBIC, center=(px, H * 1.4), translate=(sway, 0))


def ic_frame(t, life=None, i=0):
    """Islamocommunism's frame at t (captions on), El-Sayed's head acted when `life` is given."""
    import burnham as B
    import islamocommunism as IC
    import views as V
    B.SS = SS
    if life is None:
        return small(IC.frame_image(t).convert('RGB'), 1080)
    orig = IC.elsayed_item

    def item(tt):
        x, z, draw = orig(tt)
        sp = IC.elsayed_sp(tt)

        def acted(im, c):
            lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
            draw(lay, c)
            f = sp.get('height', 1.75) / 1.75
            (Xn, Yn), _ = c.project((x, 928 * V.M_PER_UNIT * f, z))
            Xn, Yn = float(np.ravel(Xn)[0]) * B.SS, float(np.ravel(Yn)[0]) * B.SS   # (the camera works at 1080 wide)
            a = np.asarray(lay.getchannel('A'))
            rows = np.nonzero(a[:int(Yn)].max(axis=1) > 0)[0]
            top = rows.min() if len(rows) else Yn - 400
            hw = float(Yn - top) * 0.55
            roll, nod, body = life.at(i)
            im.alpha_composite(act_head(lay, (Xn, Yn - (Yn - top) * 0.10), hw * 0.75, roll, nod, body))
        return (x, z, acted)
    IC.elsayed_item = item
    try:
        return small(IC.frame_image(t).convert('RGB'), 1080)
    finally:
        IC.elsayed_item = orig


def small(im, w):
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


# ------------------------------------------------------------------------------------------------ the sheet
def sheet(out):
    import burnham as B
    import ad_vanced_notice as AV
    import islamocommunism as IC
    B.SS = SS
    rows = []
    # 1. shading: Vance walking in (soft airbrush bands today; one hard shadow shape proposed)
    t = 10.5
    a = AV.picture(t).convert('RGB')
    with cel():
        b = AV.picture(t).convert('RGB')
    box = (250, 800, 610, 1440)
    rows.append(('1. Shading: soft airbrushed bands (today) vs one hard-edged shadow shape', a, b, box))
    # 2. head: dead-still, mirror-front head vs a tilted, settled head (the clip shows it moving)
    t = 31.0
    a = ic_frame(t)
    life = HeadLife(np.zeros(12))
    life.roll[:] = 4.0
    b = ic_frame(t, life, 5)
    rows.append(('2. Talking head: dead upright and centred (today) vs tilted and settled', a, b, (300, 500, 780, 1353)))
    # 3. background lines: black everywhere (today) vs a darker shade of their own colour behind the people
    t = 15.0
    a = small(IC.picture(t).convert('RGB'), 1080)
    keep = IC.people
    IC.people = lambda tt: []
    try:
        bg = small(IC.picture(t).convert('RGB'), 1080)
    finally:
        IC.people = keep
    diff = np.abs(np.asarray(a).astype(int) - np.asarray(bg).astype(int)).sum(axis=2) > 18
    import cv2
    mask = cv2.dilate(diff.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    q = quiet_bg(bg, mask)
    b = Image.fromarray(np.where(mask[..., None], np.asarray(a), np.asarray(q)))
    rows.append(('3. Background lines: black like the people (today) vs a darker shade of their own colour', a, b,
                 (600, 300, 960, 940)))
    tw, gap, lab = 264, 6, 26
    S = Image.new('RGB', (4 * tw + 5 * gap, len(rows) * (int(tw * 1920 / 1080) + lab + 2 * gap) + 40),
                  (245, 242, 236))
    d = ImageDraw.Draw(S)
    d.text((gap, 8), 'Job K: before / after (left pair today, right pair proposed; crops at the same place)',
           font=ImageFont.truetype(SANS, 17), fill=(0, 0, 0))
    f = ImageFont.truetype(SANS, 14)
    y = 40
    th = int(tw * 1920 / 1080)
    for title, a, b, box in rows:
        d.text((gap, y), title, font=f, fill=(0, 0, 0))
        y += lab
        ca, cb = a.crop(box), b.crop(box)
        for k, im in enumerate([small(a, tw), small(ca, tw), small(b, tw), small(cb, tw)]):
            x = gap + k * (tw + gap)
            S.paste(im.crop((0, 0, tw, th)), (x, y))
            d.rectangle([x, y, x + 74, y + 18], fill=(20, 20, 20) if k < 2 else (190, 30, 30))
            d.text((x + 4, y + 2), 'TODAY' if k < 2 else 'PROPOSED', font=f, fill=(255, 255, 255))
        y += th + 2 * gap
        a.save(os.path.join(OUT, f'{title[:1]}-today.png'))
        b.save(os.path.join(OUT, f'{title[:1]}-proposed.png'))
    S.save(out, quality=88)
    print(out, S.size)


# ------------------------------------------------------------------------------------------------ the clip
def clip(out, t0=36.0, t1=42.0, fps=12):
    film = os.path.join(ROOT, 'animations', 'islamocommunism-vertical.mp4')
    env = envelope(film, t0, t1, fps)
    life = HeadLife(env)
    tmp = os.path.join(OUT, 'clipframes')
    os.makedirs(tmp, exist_ok=True)
    f = ImageFont.truetype(SANS, 34)
    from multiprocessing import Pool
    n = len(env)
    with Pool(os.cpu_count()) as pool:
        pool.starmap(_clip_frame, [(i, t0 + i / fps, life, tmp, f.path) for i in range(n)])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                    '-ss', str(t0), '-t', str(t1 - t0), '-i', film, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                    '-crf', '26', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k',
                    '-shortest', out], check=True)
    print(out, os.path.getsize(out) // 1024, 'KB', 'accents at drawings', accents(env))


def _clip_frame(i, t, life, tmp, font):
    a = small(ic_frame(t), 540)
    b = small(ic_frame(t, life, i), 540)
    S = Image.new('RGB', (1080, 840), (245, 242, 236))
    S.paste(a.crop((0, 140, 540, 940)), (0, 40))       # (each side 540 x 960: the head and chest)
    S.paste(b.crop((0, 140, 540, 940)), (540, 40))
    d = ImageDraw.Draw(S)
    f = ImageFont.truetype(font, 30)
    d.text((270, 20), 'TODAY', font=f, fill=(20, 20, 20), anchor='mm')
    d.text((810, 20), 'PROPOSED: head acting', font=f, fill=(190, 30, 30), anchor='mm')
    S.save(os.path.join(tmp, f'{i + 1:04d}.png'))


# ------------------------------------------------------------------------------------------------ proposal 5 (built)
def driver(out):
    """Proposal 5's sheet: the pump driver with the kit's options off and on, whole body, then his face full size."""
    import burnham as B
    import views as V
    import ad_vanced_notice_cast as AC
    B.SS = 1
    sp = dict(AC.MAN)
    bg = (238, 234, 228, 255)

    plain = dict(sp, lopsided=None, weight_leg=None)      # today: the kit's options off

    def body(prop):
        im = Image.new('RGBA', (1080, 1920), bg)
        cam = B.Cam(1.0, 540, 960)
        s = 0.62 * sp['height'] / 1.75
        V.person(im, cam, 540, 1560 - 928 * s, s, dict(sp if prop else plain), 0.0, 0)
        return im.convert('RGB').crop((240, 820, 840, 1620))

    def face(prop):
        im = Image.new('RGBA', (1080, 1920), bg)
        cam = B.Cam(1.0, 540, 960)
        V.person(im, cam, 540, 1150, 2.2, dict(sp if prop else plain), 0.0, 0)
        return im.convert('RGB').crop((190, 420, 890, 1180))

    tiles = [body(False), body(True), face(False), face(True)]
    W = 2 * 700 + 30
    S = Image.new('RGB', (W, 60 + 800 + 50 + 760 + 20), (245, 242, 236))
    d = ImageDraw.Draw(S)
    f = ImageFont.truetype(SANS, 30)
    d.text((10, 14), 'Proposal 5, built: the pump driver, before (left) vs now (right)', font=f, fill=(0, 0, 0))
    for k, im in enumerate(tiles[:2]):
        S.paste(im, (10 + k * 720 + 50, 60))
    for k, im in enumerate(tiles[2:]):
        S.paste(im, (10 + k * 720, 910))
    for k in range(2):
        x = 10 + k * 720
        d.rectangle([x, 60, x + 200, 96], fill=(20, 20, 20) if k == 0 else (190, 30, 30))
        d.text((x + 8, 64), 'BEFORE' if k == 0 else 'NOW', font=f, fill=(255, 255, 255))
    d.text((10, 870), 'The face at full size', font=f, fill=(0, 0, 0))
    S.save(out, quality=90)
    print(out, S.size)


# ------------------------------------------------------------------------------------------------ proposal 2 (built)
SHADE_ROWS = [  # (label, film, time, crop box on the 1080 x 1920 frame)
    ('Vance walking in (navy suit)', 'av', 10.5, (250, 800, 610, 1440)),
    ('El-Sayed close-up (jacket, neck)', 'ic', 31.0, (300, 600, 780, 1453)),
    ('The driver at the pump (check shirt, jeans)', 'av', 22.0, (420, 640, 960, 1600)),
]


def _film_frame(film, t):
    import burnham as B
    B.SS = SS
    if film == 'av':
        import ad_vanced_notice as AV
        return small(AV.picture(t).convert('RGB'), 1080)
    return ic_frame(t)


def shading(out, rows=None):
    """Today's airbrushed shading (ed.HARD off) beside the hard-edged shapes, each a crop at the same place."""
    import ed
    rows = rows or SHADE_ROWS
    cw = 528
    pics = []
    for label, film, t, box in rows:
        ed.HARD = False
        a = _film_frame(film, t)
        ed.HARD = True
        b = _film_frame(film, t)
        a.save(os.path.join(OUT, f'shade-{film}-{t}-today.png'))
        b.save(os.path.join(OUT, f'shade-{film}-{t}-hard.png'))
        ca, cb = a.crop(box), b.crop(box)
        h = int(ca.height * cw / ca.width)
        pics.append((label, ca.resize((cw, h), Image.LANCZOS), cb.resize((cw, h), Image.LANCZOS)))
    f = ImageFont.truetype(SANS, 22)
    H = 50 + sum(p[1].height + 40 for p in pics)
    S = Image.new('RGB', (2 * cw + 24, H), (245, 242, 236))
    d = ImageDraw.Draw(S)
    d.text((8, 12), 'Proposal 2: shading, airbrushed (left, before) vs hard-edged (right, now)', font=f, fill=(0, 0, 0))
    y = 50
    for label, a, b in pics:
        d.text((8, y + 4), label, font=f, fill=(0, 0, 0))
        y += 34
        for k, im in enumerate((a, b)):
            x = 8 + k * (cw + 8)
            S.paste(im, (x, y))
            d.rectangle([x, y, x + 110, y + 28], fill=(20, 20, 20) if k == 0 else (190, 30, 30))
            d.text((x + 6, y + 2), 'BEFORE' if k == 0 else 'NOW', font=f, fill=(255, 255, 255))
        y += a.height + 6
    S.save(out, quality=90)
    print(out, S.size)


# ------------------------------------------------------------------------------------------------ proposal 1 (built)
def rigclip(out, t0=36.0, t1=42.0, fps=12):
    import headlife
    film = os.path.join(ROOT, 'animations', 'islamocommunism-vertical.mp4')
    life = headlife.from_voice(film, t0, t1)
    tmp = os.path.join(OUT, 'rigframes')
    os.makedirs(tmp, exist_ok=True)
    n = int(round((t1 - t0) * fps))
    from multiprocessing import Pool
    with Pool(os.cpu_count()) as pool:
        pool.starmap(_rig_frame, [(i, t0 + i / fps, life, tmp) for i in range(n)])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                    '-ss', str(t0), '-t', str(t1 - t0), '-i', film, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                    '-crf', '26', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k',
                    '-shortest', out], check=True)
    print(out, os.path.getsize(out) // 1024, 'KB', 'accents at drawings', headlife.accents(headlife.envelope(film, t0, t1)))


def _rig_frame(i, t, life, tmp):
    import islamocommunism as IC
    a = small(ic_frame(t), 540)
    orig = IC.elsayed_sp
    IC.elsayed_sp = lambda tt: dict(orig(tt), head_life=life)
    try:
        b = small(ic_frame(t), 540)
    finally:
        IC.elsayed_sp = orig
    S = Image.new('RGB', (1080, 840), (245, 242, 236))
    S.paste(a.crop((0, 140, 540, 940)), (0, 40))
    S.paste(b.crop((0, 140, 540, 940)), (540, 40))
    d = ImageDraw.Draw(S)
    f = ImageFont.truetype(SANS, 30)
    d.text((270, 20), 'BEFORE', font=f, fill=(20, 20, 20), anchor='mm')
    d.text((810, 20), 'NOW: head acting', font=f, fill=(190, 30, 30), anchor='mm')
    S.save(os.path.join(tmp, f'{i + 1:04d}.png'))


def shirt(out):
    """Proposal 4's check (built, ad_vanced_notice_cast.BENT): the driver's shirt from four views, the flat grid as
    filmed (top) vs the check bent round his body (bottom)."""
    import burnham as B
    import views as V
    import ad_vanced_notice_cast as AC
    B.SS = 1
    sp = dict(AC.MAN)
    views = [(0, 'front'), (45, 'three-quarter'), (90, 'side'), (180, 'back')]
    f = ImageFont.truetype(SANS, 30)
    tw, th = 420, 650
    S = Image.new('RGB', (len(views) * tw + 20, 2 * (th + 50) + 70), (245, 242, 236))
    d = ImageDraw.Draw(S)
    d.text((10, 14), 'The driver\'s check shirt: as filmed (top) vs bent round his body (bottom)', font=f, fill=(0, 0, 0))
    s_ = 0.62 * sp['height'] / 1.75 * 1.6
    for r, bent in enumerate((False, True)):
        y = 70 + r * (th + 50)
        d.rectangle([10, y, 230, y + 36], fill=(20, 20, 20) if not bent else (190, 30, 30))
        d.text((18, y + 3), 'AS FILMED' if not bent else 'BENT', font=f, fill=(255, 255, 255))
        for c, (deg, name) in enumerate(views):
            im = Image.new('RGBA', (1080, 1920), (238, 234, 228, 255))
            with swapped([(AC, 'BENT', bent)]):
                V.person(im, B.Cam(1.0, 540, 960), 540, 1500 - 928 * s_, s_, dict(sp), 0.0, float(deg))
            top = 1500 - 928 * s_
            box = (540 - int(300 * s_), int(top - 280 * s_), 540 + int(300 * s_), int(top + 640 * s_))
            t = im.convert('RGB').crop(box).resize((tw - 10, th - 10))
            S.paste(t, (10 + c * tw, y + 46))
            if r == 0:
                d.text((20 + c * tw, y + 46), name, font=f, fill=(0, 0, 0))
    S.save(out, quality=90)
    print(out, S.size)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cmd = sys.argv[1]
    {'sheet': sheet, 'clip': clip, 'driver': driver, 'shading': shading, 'rigclip': rigclip, 'shirt': shirt}[cmd](sys.argv[2])
