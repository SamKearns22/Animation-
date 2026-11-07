#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (7 Nov): the rough composition sheet (rule 11) and the place-reference sheet (rule 3), drawn
BEFORE the sets are built. Flat blocked-in sets with the real cast standing in their places, sized from real metres
through one locked camera per shot (rough perspective: px per metre at each depth). Nothing here is final art.

    python3 source/ad_vanced_notice_comp.py comp OUT.jpg   the key shots side by side, the Hook Text band marked
    python3 source/ad_vanced_notice_comp.py refs OUT.jpg   each place: the photos and its 8-10 things (unticked)

Map: helpers 30 | study 60 | cliff 130 | close-up 230 | gas station 270 | sheets 380
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ad_vanced_notice_cast as AC   # noqa: E402
import midterminal_cast as MC        # noqa: E402
import moves                         # noqa: E402
import views as V                    # noqa: E402
from ed import INK                   # noqa: E402

FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
W, H = 1080, 1920
HOOK_BAND = (290, 440)               # where the Hook Text will sit on the opening shot (wording later, Sam 7 Nov)
REFS = os.path.join(ROOT, 'references', 'ad-vanced-notice')


# ---------------------------------------------------------------------------------------------- helpers
def font(n):
    return ImageFont.truetype(FONT, n)


def poly(d, pts, fill, w=3):
    d.polygon([tuple(p) for p in pts], fill=fill, outline=INK, width=w)


def rect(d, x0, y0, x1, y1, fill, w=3):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=INK, width=w)


def nts(sp):
    """Neck to soles in metres for someone of the cast."""
    return 928 * V.M_PER_UNIT * sp['height'] / 1.75


def person(im, sp, x, feet_y, ppm, yaw=0, j=None, **kw):
    """Someone of the cast at screen x, soles at feet_y, `ppm` pixels per metre at their depth."""
    s = nts(sp) * ppm / 928
    return V.person(im, AC.B.Cam(1.0, 540, 960), x, feet_y - 928 * s, s, dict(sp, **kw), 0.0, yaw, j)


def hand(d, x, y, r, skin):
    d.ellipse([x - r, y - r, x + r, y + r], fill=skin, outline=INK, width=3)


def setup():
    MC.CAST.clear()
    MC.CAST.update(AC.CAST)
    AC.B.SS = 1


# ---------------------------------------------------------------------------------------------- shot 1: the study
# Camera 1.45 m up (a standing eye looking a touch down), Vance 1.9 m away seated, the desk front 1.45 m, the back
# wall 3.6 m. Horizon y 760. px per metre: Vance 760, desk back 860, desk front 1000, back wall 400.
OAK, OAK_D, OAK_L = (122, 74, 38), (86, 50, 26), (156, 100, 56)


def study():
    im = Image.new('RGBA', (W, H), (70, 44, 26, 255))
    d = ImageDraw.Draw(im)
    hz, pw = 760, 400
    floor_y = hz + 1.45 * pw                       # the back wall's foot
    ceil_y = hz - (2.9 - 1.45) * pw
    rect(d, -5, ceil_y, W + 5, floor_y, OAK)      # oak-lacquered panelling
    rect(d, -5, -5, W + 5, ceil_y, (230, 222, 204))   # ceiling, cornice
    rect(d, -5, ceil_y - 6, W + 5, ceil_y + 26, OAK_L)
    # bookcases: the whole back wall left of the fireplace, floor to cornice
    bx1 = 690
    books = [(128, 30, 30), (34, 58, 92), (40, 80, 50), (150, 120, 70), (90, 40, 60), (200, 180, 140), (60, 40, 30)]
    for c0 in range(0, bx1, 230):
        c1 = min(bx1, c0 + 230)
        rect(d, c0, ceil_y + 26, c1, floor_y, OAK_D)
        y = ceil_y + 40
        k = c0
        while y + 120 < floor_y - 60:
            x = c0 + 16
            while x < c1 - 30:
                k += 7
                bw = 14 + (k * 13) % 14
                bh = 86 + (k * 7) % 26
                d.rectangle([x, y + 110 - bh, x + bw, y + 110], fill=books[k % len(books)], outline=INK, width=2)
                x += bw + 2
            rect(d, c0 + 8, y + 110, c1 - 8, y + 122, OAK_L, 2)
            y += 132
    # fireplace on the right: stone surround, mantel at 1.2 m, firebox 0.8 m, fire
    fx0, fx1 = 720, 1120
    mant = hz - (1.25 - 1.45) * pw
    rect(d, fx0, mant - 14, fx1, mant + 12, OAK_L)
    rect(d, fx0 + 16, mant + 12, fx1 - 16, floor_y, (196, 186, 168))
    rect(d, fx0 + 70, floor_y - 0.8 * pw, fx1 - 60, floor_y, (24, 18, 16))
    for i, (dx, hh) in enumerate(((0, 120), (60, 160), (120, 110), (175, 140))):
        x = fx0 + 110 + dx
        poly(d, [(x - 34, floor_y - 30), (x, floor_y - 30 - hh), (x + 34, floor_y - 30)], (240, 140, 40), 2)
        poly(d, [(x - 16, floor_y - 30), (x, floor_y - 30 - hh * 0.55), (x + 16, floor_y - 30)], (255, 214, 90), 2)
    rect(d, fx0 + 84, floor_y - 34, fx1 - 74, floor_y - 18, (70, 40, 24), 2)   # logs
    rect(d, fx0 + 60, ceil_y + 70, fx1 - 50, mant - 40, (196, 160, 70))         # a portrait in a gilt frame
    rect(d, fx0 + 80, ceil_y + 90, fx1 - 70, mant - 60, (70, 60, 50), 2)
    # Vance seated behind the desk, hands folded on it
    ppm = 760
    j = moves.seated(AC.VANCE)
    j['seated'] = False
    vx, vfeet = 450, hz + 1.45 * ppm
    person(im, AC.VANCE, vx, vfeet, ppm, 0, j, mood='smile', mouth='rest')
    # the desk: top at 0.76 m, front edge 1.9 m away (760 px/m), back edge 1.3 m behind it
    top_f = hz + (1.45 - 0.76) * 1000
    top_b = hz + (1.45 - 0.76) * 860
    poly(d, [(-60, top_b), (1000, top_b), (1060, top_f), (-120, top_f)], OAK_L)
    rect(d, -120, top_f, 1060, H + 5, OAK)
    for x in (120, 520, 900):
        rect(d, x - 150, top_f + 70, x + 150, top_f + 300, OAK_D, 2)
    hand(d, vx - 50, top_b + 34, 44, AC.V_SKIN)
    hand(d, vx + 40, top_b + 38, 44, AC.V_SKIN)
    # the crystal glass of water, on his left (our right)
    gx = 790
    poly(d, [(gx - 34, top_b + 10), (gx + 34, top_b + 10), (gx + 28, top_b + 120), (gx - 28, top_b + 120)], (200, 228, 238))
    d.line([(gx - 30, top_b + 46), (gx + 30, top_b + 46)], fill=(140, 190, 210), width=3)
    # the flag draped over the left of the desk: canton and stripes hanging over the front
    fl0, fl1 = -20, 300
    poly(d, [(-20, top_b + 6), (250, top_b + 6), (fl1 + 20, top_f), (-20, top_f)], (30, 40, 100))
    for r in range(3):
        for c in range(6):
            x, y = 20 + c * 44, top_b + 22 + r * 26
            d.ellipse([x - 5, y - 4, x + 5, y + 4], fill=(250, 250, 250))
    for i in range(13):
        y0 = top_f - 40 + i * 34
        d.rectangle([fl0, y0, fl1 + i * 3, y0 + 34], fill=(190, 30, 40) if i % 2 == 0 else (245, 245, 245))
    d.rectangle([fl0, top_f - 40, 170, top_f - 40 + 7 * 34], fill=(30, 40, 100))
    for r in range(5):
        for c in range(5):
            x, y = 10 + c * 32, top_f - 22 + r * 44
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(250, 250, 250))
    d.rectangle([fl0, top_f - 40, fl1 + 36, top_f - 40 + 13 * 34], outline=INK, width=3)
    return im


# ---------------------------------------------------------------------------------------------- shot 2: the cliff
# Camera 1.6 m up on the cliff-top plateau (the cliff 60 m above the sea), level, focal 1400 px. Horizon y 700. The
# plateau's edge 9 m out (y 950); beyond it only sea farther than about 340 m shows. The moving tanker 1.2 km out
# (330 m long: 385 px), the rest of the flotilla 2-9 km. Vance walks the path from the edge to his mark 2.6 m away.
SKY, SEA, SEA_D = (190, 214, 228), (58, 112, 150), (40, 88, 124)
ROCK, ROCK_D, SAND = (176, 150, 120), (128, 104, 82), (214, 196, 160)
HULL, DECK, HOUSE = (150, 40, 34), (118, 108, 98), (236, 232, 222)
TANKER_HIT = (720, 815)          # the moving tanker's middle when the missile lands (screen)


def tanker(d, x, wl, L, colour=HULL, wake=False):
    """A crude carrier side on, bow to the right: hull, deck pipework line, bridge house and funnel at the stern."""
    hgt = L * 0.075
    poly(d, [(x - L / 2, wl - hgt), (x + L / 2 - L * 0.04, wl - hgt), (x + L / 2, wl - hgt * 0.8),
             (x + L / 2 - L * 0.03, wl), (x - L / 2 + L * 0.02, wl)], colour, 2)
    d.line([(x - L / 2, wl - hgt * 0.35), (x + L / 2 - L * 0.02, wl - hgt * 0.35)], fill=(30, 30, 30), width=max(1, int(L / 120)))
    hx = x - L / 2 + L * 0.06
    rect(d, hx, wl - hgt * 2.3, hx + L * 0.09, wl - hgt, HOUSE, 2)
    rect(d, hx + L * 0.02, wl - hgt * 2.9, hx + L * 0.05, wl - hgt * 2.3, (40, 40, 44), 2)
    if wake:
        for k in range(3):
            d.line([(x - L / 2 - 10, wl + 2 + k * 5), (x - L / 2 - 160 - k * 90, wl + 6 + k * 10)], fill=(225, 235, 240), width=3)


def cliff(hit=False, vx=360, vfeet=1790, vppm=540, mood='sincere'):
    im = Image.new('RGBA', (W, H), SKY + (255,))
    d = ImageDraw.Draw(im)
    hz = 700
    for k in range(6):                                     # hazy sky bands, palest at the horizon
        c = tuple(int(a + (b - a) * k / 6) for a, b in zip((150, 186, 214), SKY))
        d.rectangle([0, k * hz / 6, W, (k + 1) * hz / 6], fill=c)
    # the far shore (Iran, about 40 km): a grey smudge of hills on the horizon
    d.polygon([(0, hz), (0, hz - 26), (160, hz - 44), (330, hz - 30), (520, hz - 58), (700, hz - 36), (880, hz - 50),
               (1080, hz - 28), (1080, hz)], fill=(170, 176, 186))
    d.rectangle([0, hz, W, 1000], fill=SEA)
    for k in range(10):
        y = hz + 8 + k * k * 3
        d.line([(30 + (k * 97) % 300, y), (200 + (k * 97) % 300, y)], fill=SEA_D, width=2)
    for x, dist in ((140, 9000), (300, 6000), (430, 7500), (930, 4200), (220, 3200), (980, 2600), (600, 5200)):
        tanker(d, x, hz + 60 * 1400 / dist, 330 * 1400 / dist, (90 + dist % 60, 60, 50) if dist % 2 else (40, 50, 60))
    if not hit:
        tanker(d, TANKER_HIT[0], TANKER_HIT[1], 385, HULL, wake=True)
    # the cliff top: the edge at y 950, a cliff face falling away at the right (m3), the stony plateau and the path
    poly(d, [(560, 1000), (1080, 880), (1080, 1060), (700, 1060)], ROCK_D)
    poly(d, [(-5, 940), (300, 930), (560, 960), (760, 1010), (1085, 1040), (1085, H + 5), (-5, H + 5)], ROCK)
    poly(d, [(380, 950), (470, 952), (720, H + 5), (100, H + 5)], SAND, 2)
    for i in range(40):
        x, y = (i * 263) % 1080, 980 + (i * 131) % 900
        r = 6 + (i * 7) % 18 * (y - 900) / 900
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=ROCK_D, outline=INK, width=2)
    if hit:
        fx, fy = TANKER_HIT
        tanker(d, fx, fy, 385, (60, 30, 26))
        d.polygon([(fx - 60, fy - 20), (fx - 120, fy - 300), (fx - 40, fy - 620), (fx + 80, fy - 900), (fx + 260, fy - 1000),
                   (fx + 360, fy - 640), (fx + 120, fy - 260), (fx + 70, fy - 20)], fill=(40, 36, 36), outline=INK)
        d.ellipse([fx - 170, fy - 330, fx + 170, fy + 10], fill=(200, 50, 20), outline=INK, width=3)
        d.ellipse([fx - 120, fy - 290, fx + 120, fy - 20], fill=(250, 150, 40))
        d.ellipse([fx - 60, fy - 230, fx + 60, fy - 70], fill=(255, 230, 120))
        for k, (px, py) in enumerate(((fx - 330, fy - 360), (fx + 300, fy - 420), (fx - 200, fy - 520), (fx + 380, fy - 200))):
            d.polygon([(px, py), (px + 30, py - 12), (px + 24, py + 22)], fill=(60, 50, 46), outline=INK)
            d.line([(px, py), (px - 30 * (1 if px < fx else -1), py + 40)], fill=(250, 150, 40), width=6)
        for sx in (fx - 300, fx + 340, fx - 420):
            d.ellipse([sx - 16, fy + 10, sx + 16, fy + 26], fill=(235, 240, 245), outline=INK, width=2)
            d.rectangle([sx - 6, fy - 40, sx + 6, fy + 16], fill=(235, 240, 245))
        d.polygon([(fx - 400, fy + 4), (fx + 400, fy + 4), (fx + 300, fy + 60), (fx - 300, fy + 60)], fill=(150, 100, 70))
        tanker(d, fx, fy, 385, (60, 30, 26))
        d.ellipse([fx - 170, fy - 330, fx + 170, fy + 10], fill=(200, 50, 20), outline=INK, width=3)
        d.ellipse([fx - 120, fy - 290, fx + 120, fy - 20], fill=(250, 150, 40))
        d.ellipse([fx - 60, fy - 230, fx + 60, fy - 70], fill=(255, 230, 120))
    person(im, AC.VANCE, vx, vfeet, vppm, 0, mood=mood)
    return im


# ---------------------------------------------------------------------------------------------- shot 3: close-up
def closeup():
    im = Image.new('RGBA', (W, H), SKY + (255,))
    d = ImageDraw.Draw(im)
    hz = 1010
    d.rectangle([0, 0, W, hz], fill=(176, 198, 214))
    d.polygon([(0, hz), (0, hz - 30), (300, hz - 50), (700, hz - 30), (1080, hz - 44), (1080, hz)], fill=(170, 176, 186))
    d.rectangle([0, hz, W, H], fill=SEA)
    # the burning wreck over his LEFT shoulder (screen right; Sam, 7 Nov: the screenplay said right by mistake), the
    # smoke leaning right as in the cliff shot
    wx, wl = 840, hz + 40
    d.polygon([(wx - 60, wl - 40), (wx - 220, wl - 500), (wx - 120, wl - 1000), (wx + 60, wl - 1300), (wx + 320, wl - 1250),
               (wx + 180, wl - 700), (wx + 80, wl - 40)], fill=(40, 36, 36), outline=INK)
    tanker(d, wx, wl, 420, (60, 30, 26))
    for dx in (-60, 0, 50):
        d.polygon([(wx + dx - 40, wl - 36), (wx + dx, wl - 190), (wx + dx + 40, wl - 36)], fill=(245, 140, 40), outline=INK)
    d.polygon([(wx - 300, wl + 4), (wx + 300, wl + 4), (wx + 200, wl + 90), (wx - 200, wl + 90)], fill=(170, 110, 70))
    person(im, AC.VANCE, 430, 1920 + 1500, 1500, 0, mood='sincere', mouth='rest')
    return im


# ---------------------------------------------------------------------------------------------- shot 4: gas station
# Camera 1.6 m up, level, horizon y 900. The two men 4.5 m away (480 px/m), the pickup 1.5 m behind them (360 px/m,
# side on, cab to the left), the pump island at the left edge, the price-board pylon 20 m away (108 px/m) at the
# forecourt's edge, flat land beyond.
def gas():
    im = Image.new('RGBA', (W, H), (176, 206, 232, 255))
    d = ImageDraw.Draw(im)
    hz = 900
    d.rectangle([0, hz, W, H], fill=(150, 146, 140))                     # forecourt concrete
    d.rectangle([0, hz - 6, W, hz + 14], fill=(200, 180, 110))           # flat fields to the horizon
    for x in (820, 900):                                                 # a grain elevator far off
        rect(d, x, hz - 120, x + 60, hz, (210, 206, 196), 2)
    for x in range(40, 1080, 160):                                       # power poles
        d.line([(x, hz - 60), (x, hz + 4)], fill=(70, 60, 50), width=3)
    # the price board on its pylon (6 m up, 20 m away), Diesel first (brief), Regular and Premium under (Sam, 7 Nov)
    px, ppm = 260, 108
    top = hz - (7.0 - 1.6) * ppm
    rect(d, px - 10, top + 260, px + 10, hz + 0.0, (90, 90, 96), 2)
    rect(d, px - 150, top, px + 150, top + 270, (245, 245, 240))
    rect(d, px - 150, top, px + 150, top + 50, (30, 60, 140))
    for i, (name, price) in enumerate((('DIESEL', '6.15'), ('REGULAR', '4.39'), ('PREMIUM', '5.25'))):   # peak war prices
        y = top + 62 + i * 68
        rect(d, px - 140, y, px + 140, y + 60, (20, 20, 22), 2)
        d.text((px - 128, y + 20), name, font=font(22), fill=(240, 240, 240))
        d.text((px + 20, y + 6), price, font=font(42), fill=(255, 70, 50) if i == 0 else (255, 200, 60))
        d.text((px + 126, y + 4), '9', font=font(16), fill=(255, 200, 60))
    # the canopy overhead (the men stand at its edge): its lit fascia across the top
    rect(d, -5, -5, 1085, 150, (236, 236, 236))
    rect(d, -5, 150, 1085, 215, (200, 40, 40))
    for x in range(80, 1080, 240):
        rect(d, x, 110, x + 120, 140, (255, 250, 220), 2)
    # the pickup, side on, rear half in frame: bed to the right, filler on the rear quarter
    tp = 360
    wl = hz + 1.6 * tp
    bot, top_bed, roof = wl - 0.35 * tp, wl - 1.25 * tp, wl - 1.95 * tp
    poly(d, [(-200, bot), (1040, bot), (1040, top_bed), (300, top_bed), (240, roof), (-200, roof)], (236, 236, 232))
    rect(d, 20, roof + 30, 220, top_bed - 10, (150, 170, 190))                # rear cab window
    for wx in (780,):
        d.ellipse([wx - 150, wl - 150 - 20, wx + 150, wl + 150 - 20], fill=(30, 30, 30), outline=INK, width=3)
        d.ellipse([wx - 70, wl - 90, wx + 70, wl + 50], fill=(170, 170, 176), outline=INK, width=3)
    # the pump island and pump at the left edge, the hose to the nozzle in the man's hand
    rect(d, -20, hz + 380, 180, hz + 770, (200, 200, 204))
    rect(d, -10, hz - 260, 150, hz + 400, (220, 60, 50))
    rect(d, 10, hz - 200, 130, hz - 60, (30, 30, 34), 2)
    ppm = 480
    mx, vx, feet = 470, 730, hz + 1.6 * ppm + 160
    rect(d, 300, hz + 330, 360, hz + 400, (40, 46, 54), 2)          # the filler flap
    d.line([(140, hz + 100), (200, hz + 640), (300, hz + 640), (346, hz + 600)], fill=(20, 20, 20), width=10)
    # Vance (arriving from the right, arm round him): drawn first so the man covers the arm, his hand laid on top
    j = V.standing(AC.VANCE)
    V.arm_to(j, 'L', (-360, 40, 40), 'out', 'palm')
    person(im, AC.VANCE, vx, feet + 30, ppm * 1.02, 0, j, mood='smile', mouth='rest')
    jm = V.standing(AC.MAN)
    V.arm_to(jm, 'L', (-250, 330, 60), 'down', 'fist')
    person(im, AC.MAN, mx, feet, ppm, 0, jm, head_yaw=-30, anger=4, gaze_dy=-1.0)
    d.line([(mx - 250 * nts(AC.MAN) * ppm / 928 * 1.0, feet - 900 * nts(AC.MAN) * ppm / 928 + 330 * nts(AC.MAN) * ppm / 928), (346, hz + 365)], fill=(30, 30, 30), width=14)
    s_m = nts(AC.MAN) * ppm / 928
    hand(d, mx - 150 * s_m * 1.1, feet - 928 * s_m + 20 * s_m, 34, AC.V_SKIN)
    return im


# ---------------------------------------------------------------------------------------------- the places (rule 3)
# Each place: the photos (references/ad-vanced-notice/, sources.txt) and the 8-10 things that make it recognisable,
# written from the photos before drawing. These become the film's BENCHMARK (benchmark.py) once the sets are built.
PLACES = [
    ('The study', ['study-abbotsford.jpg', 'study-canons-ashby.jpg', 'study-oak-fireplace.jpg'], [
        'floor-to-ceiling dark oak bookcases, packed with old books',
        'books in leather browns, dark reds and greens, gold spine bands',
        'shelves in tall bays between flat oak uprights; a cornice on top',
        'oak with a lacquer shine: pale highlight streaks on the wood',
        'the fireplace set into the book wall (right): stone surround',
        'a black firebox, iron grate, logs, a low fire',
        'a mantel shelf with a clock and two candlesticks',
        'a portrait in a gilt frame over the mantel',
        'a big pedestal desk: drawers in front, leather top',
        'warm, low light; the fire glows on the nearby wood']),
    ('The cliff and the strait', ['cliff-musandam-plateau.jpg', 'cliff-musandam-road.jpg', 'cliff-musandam-fjord.jpg'], [
        'bare limestone mountains, grey-brown, in level layers',
        'a stony plateau: pale sand, scattered dark rocks, a dirt track',
        'sheer cliff faces dropping straight into the sea',
        'calm deep blue-teal sea, fine ripples, no waves',
        'haze: the farther, the paler and bluer',
        'the far shore: flat grey hill shapes on the horizon',
        'a pale washed-out blue sky, a few thin wisps',
        'no plants but the odd thorn tree',
        'high sun: short, hard shadows']),
    ('The tankers', ['tanker-side-wake.jpg', 'tanker-side-dark.jpg', 'tankers-at-anchor-haze.jpg'], [
        'very long and low: 330 m long, about 10 m above the water',
        'hull dark above, a red band below; laden ships sit low',
        'a white bridge block at the stern, 5-6 storeys',
        'a funnel on the bridge block with a coloured band',
        'a flat deck: a pipe run and catwalk down the middle',
        'cranes and a manifold amidships; a raised bow and mast',
        'no names or logos (decision: no brands)',
        'at anchor: still, all pointing the same way',
        'under way: a white bow wave and a spreading V wake',
        'far ones: grey shapes in the haze, the bridge the tallest bump']),
    ('The gas station', ['gas-iowa-canopy.jpg', 'gas-price-pylon.jpg', 'gas-price-board.jpg'], [
        'a flat canopy on square columns, lit underneath, a coloured band',
        'pumps on raised concrete islands, a post at each end',
        'pumps: tall boxes with a screen, black hoses and nozzles',
        'a pylon price board by the road: a tall pole, a blank top panel',
        'prices in lit numbers, each ending in a small 9 (9/10 of a cent)',
        'rows: DIESEL 6.15, REGULAR 4.39, PREMIUM 5.25 (peak war prices)',
        'a pale concrete forecourt with oil stains',
        'flat land to the horizon under a huge sky; power poles',
        'a grain elevator in the distance',
        'a low shop with a glass front behind']),
    ('The pickup', ['pickup-side.jpg', 'pickup-rear.jpg', 'gas-nozzle-filler.jpg'], [
        'a full-size 4x4 crew cab: 4 doors, 5.9 m long, 1.9 m tall',
        'a big square grille and a high, flat bonnet',
        'an open bed behind the cab with a tailgate',
        'big wheels, chunky tyres, high off the ground',
        'flared wheel arches; a running board under the doors',
        'big side mirrors; dark tinted glass',
        'the fuel flap on the driver side, ahead of the rear wheel',
        'seen side on facing left: the driver side, as in the photo',
        'plain white paint (my pick: both men stand out against it)']),
]


def refs(out):
    """Each place: up to three photos and its list (none ticked yet: the sets are not built)."""
    th, rows = 300, []
    f, fs = font(26), font(19)
    for name, photos, items in PLACES:
        tiles = []
        for p in photos:
            im = Image.open(os.path.join(REFS, p)).convert('RGB')
            im.thumbnail((420, th))
            tiles.append(im)
        x0 = sum(im.width + 12 for im in tiles) + 12
        row = Image.new('RGB', (x0 + 760, max(th, 40 + 27 * len(items)) + 24), (246, 243, 236))
        d = ImageDraw.Draw(row)
        x = 12
        for im in tiles:
            row.paste(im, (x, 12))
            x += im.width + 12
        d.text((x0, 8), name.upper(), font=f, fill=(30, 30, 34))
        for i, it in enumerate(items):
            d.text((x0, 44 + i * 27), f'{i + 1}. {it}', font=fs, fill=(40, 40, 44))
        rows.append(row)
    Wd = max(r.width for r in rows)
    sheet = Image.new('RGB', (Wd, sum(r.height + 6 for r in rows)), (210, 206, 198))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height + 6
    sheet.save(out, quality=86)
    return out


# ---------------------------------------------------------------------------------------------- sheets
SHOTS = [
    ('1  Study, front on: Vance seated, hands folded; bookcases behind, fire on the right, glass, flag over the left '
     'of the desk. Hook Text band over the books', lambda: study(), True),
    ('2a  Cliff: Vance walks the path at the lens; the flotilla still, the near tanker sailing right (wake). He stops '
     'at his mark, screen left, clear of the tanker', lambda: cliff(False, 400, 1500, 300), False),
    ('2b  Same shot, the hit: the missile drops top left onto the tanker behind him; fireball, flying pieces, smoke; '
     'he never looks round', lambda: cliff(True), False),
    ('3  Close-up: the burning wreck and its smoke over his LEFT shoulder (screen right; Sam, 7 Nov), the glow on his face. "None '
     'of this is my fault."', lambda: closeup(), False),
    ('4  Gas station: the driver at his pickup, pump in hand, glaring up at the board (DIESEL 6.15); Vance in from '
     'the right, arm round him', lambda: gas(), False),
]


def wrap(d, text, f, width):
    rows, row = [], ''
    for wd in text.split():
        if d.textlength(row + ' ' + wd, font=f) > width and row:
            rows.append(row)
            row = wd
        else:
            row = (row + ' ' + wd).strip()
    return rows + [row]


def comp(out):
    setup()
    tw, th, pad, head = 360, 640, 14, 150
    sheet = Image.new('RGB', (pad + len(SHOTS) * (tw + pad), head + th + pad), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = font(15)
    for i, (label, fn, hook) in enumerate(SHOTS):
        im = fn().convert('RGB')
        dd = ImageDraw.Draw(im)
        dd.rectangle([60, 310, 900, 1500], outline=(255, 255, 255), width=4)        # TikTok's safe area
        if hook:
            dd.rectangle([120, HOOK_BAND[0], 960, HOOK_BAND[1]], fill=(255, 255, 255), outline=INK, width=4)
            dd.text((540, sum(HOOK_BAND) / 2), 'Hook Text (wording later)', font=font(44), fill=INK, anchor='mm')
        x = pad + i * (tw + pad)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, head))
        d.multiline_text((x, 8), '\n'.join(wrap(d, label, f, tw)[:8]), font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    print({'comp': comp, 'refs': refs}[sys.argv[1]](sys.argv[2]))
