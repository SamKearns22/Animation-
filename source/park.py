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

# ---- timing (seconds). Voice length is read from the recording when it exists.
def voice_len():
    if not os.path.exists(VOICE):
        return 1.5
    r = subprocess.run([FF, "-i", VOICE], capture_output=True, text=True).stderr
    for l in r.splitlines():
        if "Duration" in l:
            h, m, s = l.split("Duration:")[1].split(",")[0].split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 1.5
VL = voice_len()
T1 = 5.0                      # shot 2 starts (close-up)
SAY = T1 + 0.5                # pigeon starts speaking
T2 = SAY + VL + 0.7           # shot 3 starts (man shocked)
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
        X.rect(230, y, 760, y + 44, wood, r=8)
    X.rect(230, 800, 262, 1130, dark, r=6); X.rect(728, 800, 760, 1130, dark, r=6)
    X.rect(220, 1020, 770, 1066, wood, r=10)          # seat
    X.rect(250, 1066, 280, 1300, (70, 70, 80), r=6); X.rect(710, 1066, 740, 1300, (70, 70, 80), r=6)
    X.ell(500, 1315, 280, 18, (150, 132, 100), line=False)

# ---- the man
def man(X, t, shock, arm_t):
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
    X.rell(x0 - 125, 880, 40, 92, 0.15, COAT)
    X.ell(x0 - 100, 1040, 32, 32, SKIN)
    # right arm scatters seed
    if shock:
        hx, hy = x0 + 130, 1110 + 6 * math.sin(t * 3)    # limp, hand drops
    else:
        sw = math.sin(arm_t * 2 * math.pi / 1.4)
        hx, hy = x0 + 205 + 20 * sw, 960 - 40 * max(0, sw) + 20
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
    X.rect(x0 - 24, hy0 + 60, x0 + 24, 780, SKIN, line=False)
    X.ell(x0, hy0, 96, 108, SKIN)
    X.ell(x0 - 96, hy0 + 8, 18, 28, SKIN); X.ell(x0 + 96, hy0 + 8, 18, 28, SKIN)   # ears
    # grey hair at the sides, bald top
    X.ell(x0 - 88, hy0 - 22, 14, 38, (170, 170, 172), line=False)
    X.ell(x0 + 88, hy0 - 22, 14, 38, (170, 170, 172), line=False)
    # eyes
    blink = (t % 3.4) < 0.12 and not shock
    for ex in (-36, 36):
        if shock:
            X.ell(x0 + ex, hy0 - 18, 24, 28, (255, 255, 255))
            X.ell(x0 + ex, hy0 - 18, 6, 6, OUT, line=False)
            X.seg((x0 + ex - 26, hy0 - 62), (x0 + ex + 26, hy0 - 66), 7)
        elif blink:
            X.seg((x0 + ex - 15, hy0 - 16), (x0 + ex + 15, hy0 - 16), 6)
        else:
            X.ell(x0 + ex, hy0 - 16, 14, 16, (255, 255, 255))
            X.ell(x0 + ex - 4, hy0 - 14, 6, 6, OUT, line=False)
            X.seg((x0 + ex - 22, hy0 - 44), (x0 + ex + 20, hy0 - 40), 6)
    # nose + moustache
    X.ell(x0, hy0 + 14, 22, 18, (96, 56, 34))
    X.ell(x0 - 20, hy0 + 40, 26, 11, (182, 182, 186))
    X.ell(x0 + 20, hy0 + 40, 26, 11, (182, 182, 186))
    # mouth
    if shock:
        X.ell(x0, hy0 + 78, 28, 36, (60, 18, 22))
    else:
        X.poly([(x0 - 34, hy0 + 66), (x0, hy0 + 86), (x0 + 34, hy0 + 66), (x0, hy0 + 76)], (60, 18, 22))

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
    spec = [(250, 1330, 0.9, +1, 0.1), (360, 1400, 1.0, -1, 0.5), (600, 1360, 0.95, +1, 0.8),
            (700, 1420, 1.05, -1, 0.3), (520, 1470, 1.05, +1, 0.65), (160, 1440, 1.0, +1, 0.2)]
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

def render(t, cam_mode, ss):
    # camera
    if cam_mode == "wide":
        cam = Cam(500, 1000, 1.0, ss)
    elif cam_mode == "close":
        push = min(1, (t - T1) / 3.0) * 0.25
        cam = Cam(615, 960, 3.0 + push, ss)
    img = Image.new("RGB", (int(W * ss), int(H * ss)), (255, 255, 255))
    X = Ctx(ImageDraw.Draw(img), cam)
    bg(X, t)
    bench(X)
    man(X, t, shock=(t >= T2), arm_t=(1.05 if cam_mode == "close" else t))
    floor_pigeons(X, t)
    # the bench pigeon
    bx, by, bs = 640, 1005, 1.0
    gone = False
    if t < T2:
        if cam_mode == "close":
            lt = t - SAY
            talk = 0 < lt < VL
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
def make_audio(path):
    sr = 44100
    n = int(END * sr)
    rnd = np.random.RandomState(1)
    a = np.zeros(n)
    wind = np.convolve(rnd.randn(n), np.ones(900) / 900, "same") * 0.9
    a += wind * (0.5 + 0.5 * np.sin(np.arange(n) / sr * 0.5))
    for k in range(14):                       # little bird chirps
        s0 = int(rnd.uniform(0, END - 0.4) * sr)
        base = rnd.uniform(2600, 4200)
        for j in range(3):
            tt = np.arange(int(0.07 * sr)) / sr
            env = np.sin(np.pi * tt / 0.07) ** 2
            seg = np.sin(2 * np.pi * (base + 500 * j + 900 * tt / 0.07) * tt) * env * 0.05
            o = s0 + int(j * 0.1 * sr)
            a[o:o + len(seg)] += seg[: n - o]
    for k in range(12):                       # wing flaps at take-off
        o = int((FLY + k * 0.085) * sr)
        ln = int(0.06 * sr)
        if o + ln < n:
            nz = rnd.randn(ln) * np.exp(-np.arange(ln) / (0.02 * sr)) * 0.35
            a[o:o + ln] += nz
    a = a / max(1e-6, np.abs(a).max()) * 0.5
    pcm = (a * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

def main():
    args = sys.argv[1:]
    outp = args[0]
    scale = float(args[args.index("--scale") + 1]) if "--scale" in args else 1.0
    secs = float(args[args.index("--secs") + 1]) if "--secs" in args else END
    ss = 1.5
    if "--sheet" in args:
        times = [1.0, 3.0, T1 + 1.0, SAY + 0.5, T2 + 0.3, FLY + 0.6]
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
    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ow}x{oh}", "-r", str(FPS), "-i", "-", "-i", tmpa]
    if os.path.exists(VOICE):
        cmd += ["-i", VOICE,
                "-filter_complex", f"[2:a]adelay={int(SAY*1000)}|{int(SAY*1000)},volume=1.6[v];[1:a][v]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
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
