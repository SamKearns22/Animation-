"""Netan-Yahoo! rough composition sheet (rule 11): the plan from above and the key shots, on the built studio."""
import sys, math
sys.path.insert(0, 'source')
from PIL import Image, ImageDraw, ImageFont
import burnham as B
B.SS = 1
import sets as S, newsdesk_set as NS, newsdesk_props as NP, newsdesk_cast as NC, netanyahu_cast as NN, maul_cast as MC
import views as V

CAPTION = 'עימות לראשות הממשלה 2026'
_orig = NS.heb_text
NS.heb_text = lambda text, px, col, pad=8: _orig(CAPTION if text == 'משדר מיוחד' else text, px, col, pad)

# ---- the plan (metres; x east = screen right, z north = away from the cameras; facing in plan degrees, 180 = south)
P = (-1.6, 0.55, 105)      # presenter (inside the floor disc: Sam, 26 Oct)
M = (0.0, 0.75, 210)       # Maul
N = (1.6, 0.5, 205)        # Netanyahu
CHAIR_BACK = 0.7
def chair_of(p):
    return (p[0], p[1] + CHAIR_BACK, 180)

CAMS = {
    's1 start': S.Cam((P[0], 1.65, P[1] - 4.6), (P[0] - 0.3, 0.95, P[1]), focal=2500),   # straight in front: the
    's1 end':   S.Cam((P[0], 1.65, P[1] - 4.6), (P[0], 1.3, P[1]), focal=5200),         # candidates stay out (Sam)
    's2 / s5':  S.Cam((N[0], 1.62, N[1] - 2.1), (N[0], 1.45, N[1]), focal=2700),
    's3':       S.Cam((M[0], 1.62, M[1] - 2.1), (M[0], 1.47, M[1]), focal=2700),
    's4':       S.Cam((-3.0, 1.6, -3.25), (-0.3, 1.1, 0.6), focal=1420),   # all three: front-left, presenter nearest
    's4 push':  S.Cam((-3.0, 1.6, -3.25), (-1.15, 1.05, 1.0), focal=2050),  # pushes in as Maul ignites (Sam: closer)
}


def put(img, cm, sp, x, z, facing, j, lift=0.0):
    Mu = V.M_PER_UNIT
    f = sp.get('height', 1.75) / 1.75
    (_, Yn), _ = cm.project((x, lift + 928 * Mu * f, z))
    (Xf, Yf), _ = cm.project((x, lift, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cm.yaw_of((x, 0, z), fd)
    return V.person(img, NS.FLAT, Xf, Yf - 928 * s, s, dict(sp, full=True, pose='custom'), 0.0, yaw, j)


def chunk_pile(img, cm, x, z):
    """Stand-in blocks for the pile of pieces (rough sheet only)."""
    d = ImageDraw.Draw(img)
    pieces = [(-0.25, 0.1, 0.55, 0.22, (24, 34, 74)), (0.2, -0.05, 0.5, 0.2, (24, 34, 74)),
              (0.05, 0.25, 0.35, 0.18, (30, 40, 86)), (-0.05, -0.2, 0.3, 0.16, (224, 180, 150))]
    for dx, dz, w, h, col in pieces:
        cx, cz = x + dx, z + dz
        quad = [(cx - w / 2, h, cz), (cx + w / 2, h, cz), (cx + w / 2, 0.0, cz), (cx - w / 2, 0.0, cz)]
        d.polygon([cm.project(q)[0] for q in quad], fill=col, outline=(10, 10, 12))
        top = [cm.project((cx - w / 2, h, cz))[0], cm.project((cx + w / 2, h, cz))[0]]
        d.line(top, fill=(232, 110, 40), width=4)


def frame(cm, phase):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
    extra = []
    for p in (P, M, N):
        cx, cz, cf = chair_of(p)
        extra.append((cx, cz + 0.35, lambda im, c, cx=cx, cz=cz, cf=cf: (NP.pool(im, c, cx, cz), NP.shadow(im, c, cx, cz, cf))))
        extra.append((cx, cz, lambda im, c, cx=cx, cz=cz, cf=cf: NP.round_chair(im, c, cx, cz, cf)))
    if phase in ('start', 'to camera'):
        pp = P
        people = [(NC.PRESENTER, V.standing(NC.PRESENTER), pp, 0.0),
                  (MC.MAUL_HOOD, MC.pose('stand', MC.MAUL_HOOD), M, 0.0),
                  (NN.NETANYAHU_RED, V.standing(NN.NETANYAHU_RED), N, 0.0)]
    else:   # the end of shot 4: Maul crouched on the presenter's chair, the pile where the presenter stood
        cx, cz, _ = chair_of(P)
        people = [(MC.MAUL, MC.pose('attack', MC.MAUL), (cx, cz, 160), 0.46),
                  (NN.NETANYAHU_RED, V.standing(NN.NETANYAHU_RED), N, 0.0)]
        extra.append((P[0], P[1], lambda im, c: chunk_pile(im, c, P[0], P[1])))
    for sp, j, (x, z, f), lift in people:
        f = math.degrees(math.atan2(cm.pos[0] - x, cm.pos[2] - z))      # everyone faces the camera (Sam, 26 Oct)
        if sp is NC.PRESENTER and phase != 'to camera':
            sp = dict(sp, look=0.8)                                      # his eyes to the candidates (screen right)
        extra.append((x, z - 0.01, lambda im, c, sp=sp, j=j, x=x, z=z, f=f, lift=lift: put(im, c, sp, x, z, f, j, lift)))
    # sheet-only: draw everything standing inside the ring after the desk (the building stage splits the desk into
    # pieces, rule: nearer is always on top; the whole-desk sort point put it in front of Netanyahu)
    def nearer(x, z, k=1.2):
        dx, dz = cm.pos[0] - x, cm.pos[2] - z
        n = math.hypot(dx, dz) or 1.0
        return x + dx / n * k, z + dz / n * k
    extra = [(*nearer(x, z), fn) for x, z, fn in extra]
    NS.render(img, cm, extra)
    return img.convert('RGB')


def plan_tile(W=540, H=960):
    """The plan from above (north up = away from the cameras)."""
    im = Image.new('RGB', (W, H), (246, 244, 238))
    d = ImageDraw.Draw(im)
    sc, ox, oz = 62.0, W / 2, 330   # pixels per metre; origin
    def P2(x, z):
        return (ox + x * sc, oz - z * sc)
    d.rectangle([P2(-4.2, 4.2), P2(4.2, -7.6)], outline=(160, 160, 160))
    r0, r1 = NS.DESK_R0, NS.DESK_R1
    for a0 in range(int(NS.DESK_A0), int(NS.DESK_A1), 4):
        pts = [(NS.DISC[0] + r * math.cos(math.radians(a)), NS.DISC[1] + r * math.sin(math.radians(a)))
               for r, a in ((r0, a0), (r1, a0), (r1, a0 + 4), (r0, a0 + 4))]
        d.polygon([P2(*q) for q in pts], fill=(70, 120, 210))
    cx, cz = P2(*NS.DISC)
    rr = NS.DISC_R * sc
    d.ellipse([cx - rr, cz - rr, cx + rr, cz + rr], outline=(214, 40, 48), width=3)
    f = ImageFont.truetype('source/fonts/DejaVuSans-Bold.ttf', 18)
    for name, p, col in (('presenter', P, (40, 40, 40)), ('Maul', M, (200, 30, 40)), ('Netanyahu', N, (30, 60, 160))):
        hx, hz, hf = chair_of(p)
        a, b = P2(hx - 0.3, hz + 0.3), P2(hx + 0.3, hz - 0.3)
        d.rectangle([a, b], fill=(186, 130, 70), outline=(40, 30, 20))
        x, y = P2(p[0], p[1])
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col)
        ex = x + 30 * math.sin(math.radians(p[2])); ey = y - 30 * math.cos(math.radians(p[2]))
        d.line([(x, y), (ex, ey)], fill=col, width=4)
        d.text((x - 40, y + 16), name, font=f, fill=col)
    for name, cm in CAMS.items():
        x, y = P2(cm.pos[0], cm.pos[2])
        lx, ly = P2(cm.at[0], cm.at[2]) if hasattr(cm, 'at') else (x, y - 40)
        d.line([(x, y), (x + (lx - x) * 0.35, y + (ly - y) * 0.35)], fill=(120, 120, 120), width=2)
        d.rectangle([x - 6, y - 6, x + 6, y + 6], fill=(20, 20, 20))
        d.text((x + 8, y - 6), name, font=f, fill=(20, 20, 20))
    # Maul's leap path
    d.line([P2(M[0], M[1]), P2(P[0] + 0.85, P[1] - 0.05)], fill=(200, 30, 40), width=3)
    d.text((P2(-1.2, -1.25)[0], P2(-1.2, -1.25)[1]), 'leap-flip ~1 m', font=f, fill=(200, 30, 40))
    d.text((12, 12), 'From above (1 square = studio)', font=f, fill=(20, 20, 20))
    d.text((12, 36), 'desk ring (blue), floor disc (red)', font=f, fill=(20, 20, 20))
    return im


if __name__ == '__main__':
    out = sys.argv[1]
    tiles = [('plan from above', plan_tile()),
             ('shot 1 start (zoom in)', frame(CAMS['s1 start'], 'to camera')),
             ('shot 1 end', frame(CAMS['s1 end'], 'to camera')),
             ('shots 2 and 5', frame(CAMS['s2 / s5'], 'start')),
             ('shot 3', frame(CAMS['s3'], 'start')),
             ('shot 4 start', frame(CAMS['s4'], 'start')),
             ('shot 4 end, pushed in (stand-ins)', frame(CAMS['s4 push'], 'end'))]
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 560 + 20, rows * 1030 + 20), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype('source/fonts/DejaVuSans-Bold.ttf', 30)
    for i, (k, im) in enumerate(tiles):
        x, y = 20 + (i % cols) * 560, 20 + (i // cols) * 1030
        sheet.paste(im.resize((540, 960), Image.LANCZOS), (x, y + 50))
        d.text((x, y + 6), k, font=f, fill=(30, 30, 30))
    sheet.save(out, quality=86)
    print(out)
