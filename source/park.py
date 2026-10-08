"""The Park: a one-man, pigeon-gag short. Usage: python3 source/park.py OUT.mp4 [--scale 0.5] [--secs N] [--sheet OUT.jpg]
Voice: put Sam's recording at source/audio/park-1.m4a; the film is then timed to it."""
import math, os, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

W, H, FPS = 1080, 1920, 24
FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, "audio", "park-1.m4a")
LINE = "Nobody will believe you."

# ---- timing (seconds). Sam's recording: speech runs 1.49-3.57 s, so we use 1.45-3.75 s of it.
VOICE_FROM, VOICE_TO = 1.45, 3.75
VL = (VOICE_TO - VOICE_FROM) if os.path.exists(VOICE) else 2.1
SPEECH = VL - 0.2             # how long the beak moves
T1 = 5.0                      # shot 2 starts (looking down at the pigeon)
SAY = T1 + 1.1                # pigeon starts speaking (the birdsong has faded out by now)
T2 = SAY + VL + 0.7           # shot 3 starts (man shocked), birdsong back at full volume
FLY = T2 + 1.3                # pigeon takes off
END = FLY + 2.6

# ---- palette
OUT = (20, 16, 16)
SKIN = (110, 66, 40)
GREY_P = (138, 146, 160)
GREY_D = (96, 104, 120)
SHEEN = (110, 140, 130)
COAT = (214, 120, 40)
COAT_D = (170, 90, 30)

class Cam:
    def __init__(self, cx, cy, z, ss):
        self.cx, self.cy, self.z, self.ss = cx, cy, z, ss
    def p(self, x, y):
        return ((x - self.cx) * self.z + W / 2) * self.ss, ((y - self.cy) * self.z + H / 2) * self.ss
    def w(self, v):
        return max(1, v * self.z * self.ss)

class Ctx:
    def __init__(self, d, cam, ol=5):
        self.d, self.c, self.ol = d, cam, ol
    def ell(self, x, y, rx, ry, fill, line=True):
        a, b = self.c.p(x - rx, y - ry); c, e = self.c.p(x + rx, y + ry)
        self.d.ellipse([a, b, c, e], fill=fill, outline=OUT if line else None,
                       width=int(self.c.w(self.ol)) if line else 0)
    def poly(self, pts, fill, line=True):
        P = [self.c.p(*q) for q in pts]
        self.d.polygon(P, fill=fill)
        if line:
            self.d.line(P + [P[0]], fill=OUT, width=int(self.c.w(self.ol)), joint="curve")
    def rell(self, x, y, rx, ry, ang, fill, line=True, n=28):
        ca, sa = math.cos(ang), math.sin(ang)
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / n
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            pts.append((x + ex * ca - ey * sa, y + ex * sa + ey * ca))
        self.poly(pts, fill, line)
    def seg(self, a, b, wd, col=OUT):
        self.d.line([self.c.p(*a), self.c.p(*b)], fill=col, width=int(self.c.w(wd)))
    def rect(self, x0, y0, x1, y1, fill, r=0, line=True):
        a, b = self.c.p(x0, y0); c, e = self.c.p(x1, y1)
        self.d.rounded_rectangle([a, b, c, e], radius=self.c.w(r), fill=fill,
                                 outline=OUT if line else None, width=int(self.c.w(self.ol)) if line else 0)

# ---- background
HORIZON = 800
TREES = [(120, 560, 190, 4), (390, 600, 150, 3), (700, 520, 200, 5), (960, 600, 160, 4), (-30, 640, 150, 3)]

def bg(X, t):
    # sky
    for i in range(0, HORIZON + 40, 40):
        k = i / HORIZON
        col = (int(110 + 90 * k), int(180 + 50 * k), int(235 + 10 * k))
        X.rect(-600, i, 1700, i + 41, col, line=False)
    # sun + glow
    X.ell(880, 300, 130, 130, (255, 244, 190), line=False)
    X.ell(880, 300, 80, 80, (255, 226, 110), line=False)
    # clouds (drift slowly)
    for cx, cy, s in [(250, 330, 1.0), (640, 470, 0.7)]:
        ox = cx + 14 * math.sin(t * 0.25 + cx)
        for dx, dy, r in [(-70, 10, 55), (0, -15, 75), (80, 8, 60), (20, 25, 55)]:
            X.ell(ox + dx * s, cy + dy * s, r * s, r * s * 0.8, (252, 252, 255), line=False)
    # far hedge + trees
    X.rect(-600, 730, 1700, HORIZON + 10, (74, 140, 70), line=False)
    for x, y, r, _ in TREES:
        X.rect(x - 14, y, x + 14, HORIZON + 20, (96, 66, 40))
        sway = 4 * math.sin(t * 0.9 + x)
        X.ell(x + sway, y - 30, r, r * 0.85, (52, 128, 62))
        X.ell(x - r * 0.4 + sway, y - r * 0.25, r * 0.55, r * 0.5, (70, 150, 76), line=False)
    # lawn
    X.rect(-600, HORIZON, 1700, 2800, (110, 182, 80), line=False)
    for i, y in enumerate(range(HORIZON + 20, 1200, 110)):
        if i % 2 == 0:
            X.rect(-600, y, 1700, y + 55, (122, 194, 90), line=False)
    # gravel path in the foreground
    X.poly([(-600, 1200), (1700, 1200), (1700, 2800), (-600, 2800)], (212, 190, 150), line=False)
    X.poly([(-600, 1200), (1700, 1200), (1700, 1215), (-600, 1215)], (176, 156, 120), line=False)
    rnd = random.Random(3)
    for _ in range(90):
        gx, gy = rnd.uniform(-500, 1600), rnd.uniform(1230, 1690)
        X.ell(gx, gy, 6, 3, (186, 166, 128), line=False)
    # flowers
    rnd = random.Random(8)
    for _ in range(26):
        fx, fy = rnd.uniform(-400, 1500), rnd.uniform(HORIZON + 40, 1180)
        X.ell(fx, fy, 6, 6, rnd.choice([(250, 240, 90), (255, 255, 255), (240, 120, 150)]), line=False)

def bench(X):
    wood, dark = (150, 96, 54), (110, 70, 40)
    for y in (820, 880, 940):
        X.rect(220, y, 900, y + 44, wood, r=8)
    X.rect(220, 800, 252, 1130, dark, r=6); X.rect(868, 800, 900, 1130, dark, r=6)
    X.rect(210, 1020, 910, 1066, wood, r=10)          # seat
    X.rect(240, 1066, 270, 1300, (70, 70, 80), r=6); X.rect(850, 1066, 880, 1300, (70, 70, 80), r=6)
    X.ell(560, 1315, 340, 18, (150, 132, 100), line=False)

# ---- the man
def man(X, t, shock, arm_t, glance=0.0, pv=(1.0, 0.0)):
    x0 = 470
    # shadow
    X.ell(x0, 1296, 140, 14, (150, 132, 100), line=False)
    # legs
    for dx in (-45, 45):
        X.rect(x0 + dx - 32, 1030, x0 + dx + 32, 1260, (60, 66, 90), r=20)
        X.ell(x0 + dx + (10 if dx > 0 else -10), 1268, 50, 26, (40, 32, 30))
    # body (puffy coat)
    X.rect(x0 - 130, 760, x0 + 130, 1090, COAT, r=70)
    for yy in (850, 940, 1020):
        X.seg((x0 - 124, yy), (x0 + 124, yy), 5, COAT_D)
    X.rect(x0 - 12, 770, x0 + 12, 1080, COAT_D, r=6, line=False)
    X.ell(x0, 770, 70, 38, COAT_D)      # collar
    # left arm (viewer's left): rests on knee
    X.seg((x0 - 105, 830), (x0 - 100, 1035), 78, OUT)
    X.seg((x0 - 105, 830), (x0 - 100, 1035), 66, COAT)
    X.ell(x0 - 100, 1040, 32, 32, SKIN)
    # right arm scatters seed
    if shock:
        hx, hy = x0 + 130, 1110 + 6 * math.sin(t * 3)    # limp, hand drops
    else:
        sw = math.sin(arm_t * 2 * math.pi / 1.4)
        hx, hy = x0 + 175 + 20 * sw, 960 - 40 * max(0, sw) + 20
    X.seg((x0 + 105, 830), (hx, hy), 78, OUT)
    X.seg((x0 + 105, 830), (hx, hy), 66, COAT)
    X.ell(hx, hy, 32, 32, SKIN)
    if not shock:
        ph = (arm_t % 1.4) / 1.4
        if 0.25 < ph < 0.9:
            for k in range(5):
                f = (ph - 0.25) / 0.65
                X.ell(hx + 60 * f + k * 18, hy + 20 + 330 * f * f + k * 12 * f, 5, 5, (232, 200, 90), line=False)
    # head
    hy0 = 650 + (math.sin(t * 2.0) * 4 if not shock else -8)
    turn = 1.0 if shock else 0.0         # shot 3: head turned toward the pigeon
    fx = x0 + 12 * turn
    fe = x0 + 28 * turn
    X.rect(x0 - 24, hy0 + 60, x0 + 24, 780, SKIN, line=False)
    X.ell(fx, hy0, 96, 108, SKIN)
    X.ell(fx - 96, hy0 + 8, 18, 28, SKIN); X.ell(fx + 96, hy0 + 8, 18, 28, SKIN)   # ears
    # grey hair at the sides, bald top
    X.ell(fx - 88, hy0 - 22, 14, 38, (170, 170, 172), line=False)
    X.ell(fx + 88, hy0 - 22, 14, 38, (170, 170, 172), line=False)
    # eyes
    blink = (t % 3.4) < 0.12 and not shock
    for ex in (-36, 36):
        if shock:
            X.ell(fe + ex, hy0 - 18, 24, 28, (255, 255, 255))
            X.ell(fe + ex + 12 * pv[0], hy0 - 18 + 12 * pv[1], 7, 7, OUT, line=False)
            X.seg((fe + ex - 26, hy0 - 62), (fe + ex + 26, hy0 - 66), 7)
        elif blink:
            X.seg((fe + ex - 15, hy0 - 16), (fe + ex + 15, hy0 - 16), 6)
        else:
            X.ell(fe + ex, hy0 - 16, 14, 16, (255, 255, 255))
            X.ell(fe + ex - 4 + 11 * glance, hy0 - 14 + 2 * glance, 6, 6, OUT, line=False)
            X.seg((fe + ex - 22, hy0 - 44), (fe + ex + 20, hy0 - 40), 6)
    # nose + moustache
    X.ell(fe, hy0 + 14, 22, 18, (96, 56, 34))
    X.ell(fe - 20, hy0 + 40, 26, 11, (182, 182, 186))
    X.ell(fe + 20, hy0 + 40, 26, 11, (182, 182, 186))
    # mouth
    if shock:
        X.ell(fe, hy0 + 78, 28, 36, (60, 18, 22))
    else:
        X.poly([(fe - 34, hy0 + 66), (fe, hy0 + 86), (fe + 34, hy0 + 66), (fe, hy0 + 76)], (60, 18, 22))

# ---- pigeons (side view; face = -1 faces left, +1 faces right)
def pigeon(X, x, y, s, face, head_dy=0.0, tilt=0.0, beak=0.0, wing=0.0, legs=True, ol=5):
    X.ol = ol
    f = face
    X_ = lambda dx: x + f * dx * s
    Y_ = lambda dy: y + dy * s
    if legs:
        for lx in (-10, 10):
            X.seg((X_(lx), Y_(48)), (X_(lx + 2), Y_(88)), 7 * s)
            X.seg((X_(lx + 2), Y_(88)), (X_(lx + 22), Y_(90)), 7 * s)
    # tail
    X.poly([(X_(-60), Y_(-4)), (X_(-122), Y_(6)), (X_(-116), Y_(34)), (X_(-56), Y_(38))], GREY_D)
    # body
    X.ell(X_(0), Y_(14), 72 * s, 46 * s, GREY_P)
    X.ell(X_(34), Y_(24), 34 * s, 26 * s, SHEEN, line=False)
    # head
    hx, hy = X_(66), Y_(-26 + head_dy)
    X.seg((X_(46), Y_(0)), (hx, hy + 6 * s), 34 * s, OUT)
    X.seg((X_(46), Y_(0)), (hx, hy + 6 * s), 26 * s, GREY_P)
    X.ell(hx, hy, 29 * s, 27 * s, GREY_P)
    # beak
    ty = tilt * 6 * s
    bo = beak * 12 * s
    X.poly([(hx + f * 22 * s, hy - 6 * s - bo * 0.5), (hx + f * 58 * s, hy + 4 * s + ty - bo * 0.3), (hx + f * 22 * s, hy + 6 * s)], (240, 200, 150))
    if beak > 0:
        X.poly([(hx + f * 22 * s, hy + 6 * s), (hx + f * 54 * s, hy + 10 * s + ty + bo), (hx + f * 22 * s, hy + 14 * s)], (240, 200, 150))
        X.poly([(hx + f * 22 * s, hy + 6 * s), (hx + f * 48 * s, hy + 10 * s + bo), (hx + f * 22 * s, hy + 12 * s + bo)], (150, 40, 50), line=False)
    # eye
    X.ell(hx + f * 8 * s, hy - 6 * s, 11 * s, 11 * s, (240, 150, 40))
    X.ell(hx + f * 10 * s, hy - 6 * s, 5 * s, 5 * s, OUT, line=False)
    # wing
    X.rell(X_(-6), Y_(10), 52 * s, 28 * s, f * (-0.15 + wing), GREY_D)
    X.ol = 5

def flying_wing(X, x, y, s, face, ph):
    # far-side wing raised/lowered behind and near wing in front
    a = 0.9 * math.sin(ph)
    pts = []
    for sg in (1,):
        pts = [(x - face * 10 * s, y), (x - face * 70 * s, y - 120 * s * math.cos(ph) - 40 * s),
               (x - face * 20 * s, y - 140 * s * math.cos(ph) - 60 * s), (x + face * 40 * s, y - 20 * s)]
    X.poly(pts, GREY_D)

# ---- scene
def font(sz):
    return ImageFont.truetype(os.path.join(HERE, "fonts", "Anton-Regular.ttf"), sz)

def pecks(t, seed, rate=1.3):
    """head_dy for a pecking pigeon: sharp dips."""
    ph = (t * rate + seed) % 1.0
    return 46 * (1 - abs(ph * 2 - 1)) ** 2 if ph < 0.5 else 0

def floor_pigeons(X, t):
    spec = [(190, 1320, 0.9, +1, 0.1), (430, 1370, 1.0, -1, 0.5), (680, 1320, 0.95, +1, 0.8),
            (850, 1400, 1.0, -1, 0.3), (300, 1450, 1.0, +1, 0.65), (600, 1455, 1.0, -1, 0.2)]
    for i, (x, y, s, f, sd) in enumerate(spec):
        X.ell(x, y + 90 * s, 70 * s, 12 * s, (176, 156, 120), line=False)
        pigeon(X, x + 8 * math.sin(t * 0.8 + i), y, s, f, head_dy=pecks(t, sd, 1.1 + 0.2 * (i % 3)), wing=0)

def bench_pigeon_state(t, talking_t=None):
    """curious head turns: sharp 'snap' poses held a moment."""
    k = int(t * 1.7)
    r = random.Random(k)
    tilt = r.choice([-1.6, 0, 1.6, 0.6, -0.8])
    dy = r.choice([-8, 0, 6, -4])
    return tilt, dy

def ppos(t):
    """Where the bench pigeon is in the wide shot."""
    u = t - FLY
    if u < 0:
        return 790, 959
    return 790 + 360 * u - 60 * u * u, 959 - 300 * u

def eyedir(t):
    px, py = ppos(t)
    dx, dy = px - 500, py - 632
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n

def glance(t):
    g = (t - (T1 - 1.4)) / 0.3          # eyes swing round during the last 1.4 s of shot 1
    return max(0.0, min(1.0, g)) if t < T1 else 0.0

def pov(X, t):
    """Shot 2: looking straight down at the bench pigeon, through the man's eyes."""
    # bench seat planks seen from above
    X.rect(-100, -100, 1200, 2100, (150, 96, 54), line=False)
    for y in range(-60, 2000, 330):
        X.rect(-100, y, 1200, y + 18, (80, 50, 30), line=False)
        X.rect(-100, y + 18, 1200, y + 26, (176, 120, 72), line=False)
    for y in range(120, 2000, 330):
        X.seg((60, y), (500, y + 14), 3, (124, 78, 44)); X.seg((600, y + 90), (1000, y + 80), 3, (124, 78, 44))
    sw = 6 * math.sin(t * 1.3)
    cx = 540 + sw
    X.ell(cx, 830, 250, 330, (110, 70, 40), line=False)                 # shadow
    # feet
    for fx in (-70, 70):
        X.seg((cx + fx, 1000), (cx + fx * 1.2, 1060), 9)
        for tx in (-22, 0, 22):
            X.seg((cx + fx * 1.2, 1060), (cx + fx * 1.2 + tx, 1090), 7)
    # tail + body + wings
    X.poly([(cx - 70, 560), (cx - 120, 330), (cx, 300), (cx + 120, 330), (cx + 70, 560)], GREY_D)
    X.ell(cx, 740, 195, 270, GREY_P)
    X.ell(cx, 930, 120, 70, SHEEN, line=False)
    X.rell(cx - 120, 700, 80, 235, 0.14, GREY_D)
    X.rell(cx + 120, 700, 80, 235, -0.14, GREY_D)
    for k in range(4):
        X.seg((cx - 150 + k * 6, 620 + k * 60), (cx - 100 + k * 6, 640 + k * 60), 4, (70, 76, 90))
        X.seg((cx + 150 - k * 6, 620 + k * 60), (cx + 100 - k * 6, 640 + k * 60), 4, (70, 76, 90))
    # head tipped back, looking up at the camera
    up = max(0.0, min(1.0, (t - (T1 + 0.15)) / 0.3))     # head snaps up to stare into the lens
    hx, hy = cx, 1010 + 60 * (1 - up)
    X.ell(hx, hy, 118, 110, GREY_P)
    lt = t - SAY
    talk = 0 < lt < SPEECH
    beak = (0.5 + 0.5 * math.sin(lt * 17)) if talk else 0
    blink = (t % 2.6) < 0.1 and not (up >= 1 and t < T2)
    for ex in (-66, 66):
        X.ell(hx + ex, hy - 14, 30, 30, (240, 150, 40))
        if blink:
            X.seg((hx + ex - 26, hy - 14), (hx + ex + 26, hy - 14), 7)
        else:
            r = 13 + 4 * up
            X.ell(hx + ex, hy - 14 + 8 * (1 - up), r, r + 1, OUT, line=False)   # staring dead at the camera
            X.ell(hx + ex - 5, hy - 20 + 8 * (1 - up), 4, 4, (255, 255, 255), line=False)
    # beak points down at us, foreshortened; opens while speaking
    X.poly([(hx - 38, hy + 36), (hx + 38, hy + 36), (hx + 20, hy + 88 + 14 * beak), (hx - 20, hy + 88 + 14 * beak)], (240, 200, 150))
    if beak > 0:
        X.ell(hx, hy + 70 + 10 * beak, 22, 8 + 14 * beak, (150, 40, 50))
    X.seg((hx, hy + 38), (hx, hy + 68), 4)
    # the man's own lap and hand at the edge of the picture
    X.rect(-200, 1560, 330, 2100, COAT, r=80)
    X.rect(760, 1600, 1300, 2100, (60, 66, 90), r=60)

def render(t, cam_mode, ss):
    # camera
    if cam_mode == "wide":
        cam = Cam(500, 1000, 1.0, ss)
    elif cam_mode == "close":
        push = min(1, (t - T1) / 3.0) * 0.25
        cam = Cam(540, 900, 1.35, ss)
    img = Image.new("RGB", (int(W * ss), int(H * ss)), (255, 255, 255))
    X = Ctx(ImageDraw.Draw(img), cam)
    if cam_mode == "close":
        pov(X, t)
        out = img.resize((W, H), Image.LANCZOS) if ss != 1 else img
        return finish(out, t)
    bg(X, t)
    bench(X)
    man(X, t, shock=(t >= T2), arm_t=t, glance=glance(t), pv=eyedir(t))
    floor_pigeons(X, t)
    # the bench pigeon
    bx, by, bs = 790, 1005, 1.0
    gone = False
    if t < T2:
        if cam_mode == "close":
            lt = t - SAY
            talk = 0 < lt < SPEECH
            beak = (0.5 + 0.5 * math.sin(lt * 17)) if talk else 0
            pigeon(X, bx, by - 46, bs, -1, head_dy=-26, tilt=-1.2, beak=beak)
        else:
            tilt, dy = bench_pigeon_state(t)
            pigeon(X, bx, by - 46, bs, -1, head_dy=dy, tilt=tilt)
    else:
        lt = t - FLY
        if lt < 0:
            pigeon(X, bx, by - 46, bs, -1, head_dy=-8)
        elif lt < 1.9:
            u = lt
            px = bx + 360 * u + (-60 * u * u)
            py = by - 46 - 300 * u - 120 * u * u * 0
            ph = lt * 26
            flying_wing(X, px, py, 1.0, -1, ph)
            pigeon(X, px, py, 1.0 - 0.1 * u, +1 if True else -1, head_dy=-10, wing=0.6 * math.sin(ph), legs=False)
    out = img.resize((W, H), Image.LANCZOS) if ss != 1 else img
    return finish(out, t)

def finish(out, t):
    d = ImageDraw.Draw(out)
    # title: first second only, full size, in the empty sky
    if t < 1.0:
        f = font(200)
        for i, wd in enumerate(("THE", "PARK")):
            tw = d.textlength(wd, font=f)
            cx = 540 - tw / 2
            for ox in range(-8, 9, 4):
                for oy in range(-8, 9, 4):
                    d.text((cx + ox, 360 + i * 230 + oy), wd, font=f, fill=(0, 0, 0))
            d.text((cx, 360 + i * 230), wd, font=f, fill=(178, 24, 52))
    # caption while the pigeon speaks
    if SAY <= t < T2 - 0.2:
        f = font(86)
        tw = d.textlength(LINE.upper(), font=f)
        cx, cy = 540 - tw / 2, 1290
        for ox in range(-6, 7, 3):
            for oy in range(-6, 7, 3):
                d.text((cx + ox, cy + oy), LINE.upper(), font=f, fill=(0, 0, 0))
        d.text((cx, cy), LINE.upper(), font=f, fill=(255, 255, 255))
    return out

def mode(t):
    return "close" if T1 <= t < T2 else "wide"

# ---- sound: park ambience + birds + wing flaps + the voice
AMB = os.path.join(HERE, "audio", "park-ambient-clip.mp3")

def make_audio(path):
    """Wing flaps only (the park birdsong is Sam's own file, mixed in by ffmpeg)."""
    sr = 44100
    n = int(END * sr)
    rnd = np.random.RandomState(1)
    a = np.zeros(n)
    for k in range(0):  # wing flaps removed
        o = int((FLY + k * 0.085) * sr)
        ln = int(0.06 * sr)
        if o + ln < n:
            a[o:o + ln] += rnd.randn(ln) * np.exp(-np.arange(ln) / (0.02 * sr)) * 0.35
    a = a * 0.0
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((a * 32767).astype("<i2").tobytes())

def main():
    args = sys.argv[1:]
    outp = args[0]
    scale = float(args[args.index("--scale") + 1]) if "--scale" in args else 1.0
    secs = float(args[args.index("--secs") + 1]) if "--secs" in args else END
    ss = 1.5
    if "--sheet" in args:
        times = [T1 - 0.3, T2 + 0.3, FLY + 0.4, FLY + 0.9, FLY + 1.2, FLY + 2.0]
        ims = [render(t, mode(t), 1.0).resize((360, 640)) for t in times]
        sheet = Image.new("RGB", (360 * 3, 640 * 2))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 3) * 360, (i // 3) * 640))
        sheet.save(args[args.index("--sheet") + 1], quality=88)
        return
    wd = os.path.dirname(os.path.abspath(outp)) or "."
    tmpa = outp + ".amb.wav"
    make_audio(tmpa)
    ow, oh = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}", "-r", str(FPS), "-i", "-",
           "-i", tmpa, "-stream_loop", "-1", "-i", AMB]
    A, B = T1, T1 + 1.0       # birdsong fades out over the first second of shot 2, silent for the line
    fade = f"volume='if(lt(t,{A}),1,if(lt(t,{B}),({B}-t)/({B}-{A}),if(lt(t,{T2}),0,1)))':eval=frame"
    fc = f"[2:a]aformat=channel_layouts=mono,volume=1.0,{fade}[amb];[1:a][amb]amix=inputs=2:duration=first:normalize=0[m]"
    if os.path.exists(VOICE):
        cmd += ["-i", VOICE]
        fc = (f"[3:a]atrim={VOICE_FROM}:{VOICE_TO},asetpts=PTS-STARTPTS,adelay={int(SAY*1000)}|{int(SAY*1000)},volume=1.6[v];"
              + fc + ";[m][v]amix=inputs=2:duration=first:normalize=0[a]")
    else:
        fc += ";[m]anull[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]"]
    cmd += ["-t", f"{secs:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", outp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    nf = int(secs * FPS)
    for i in range(nf):
        t = i / FPS
        im = render(t, mode(t), ss)
        if (ow, oh) != (W, H):
            im = im.resize((ow, oh), Image.LANCZOS)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    os.remove(tmpa)

if __name__ == "__main__":
    main()
