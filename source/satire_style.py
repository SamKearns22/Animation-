"""filmcow: the shared Satire-style drawing kit (flat colour, one thick black outline, lumpy shapes, circle hands).
Use it from the first frame of any new film so the look never needs a rescue (The Park's first version had no style
and had to be redrawn). Pure Pillow, no other files.
Rules of the look (guides/filmcow-style.md): flat colour (no gradients, glows or highlight blobs); ONE outline weight
round every shape; lumpy, lopsided shapes (blob), never perfect ovals; every copy different (palettes, sizes, facing);
circle hands with props laid over them; deadpan faces (heavy lids, one brow up, flat mouth); hard cuts; a close-up
for every reaction that matters.
"""
import math
import random

from PIL import ImageDraw

W, H = 1080, 1920
OUT = (20, 16, 16)


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

def blob(X, lumps, fill, ol=5):
    """Overlapping lumps drawn as one shape with a single outline round the outside (no seams inside)."""
    X.ol = ol * 2
    for x, y, rx, ry, a in lumps:
        X.rell(x, y, rx, ry, a, OUT, line=True)
    X.ol = ol
    for x, y, rx, ry, a in lumps:
        X.rell(x, y, rx, ry, a, fill, line=False)


def limb(X, a, b, w, col):
    """A sleeve from a to b with round ends and an outline all the way round."""
    r = w / 2
    for p in (a, b):
        X.ell(p[0], p[1], r + 6, r + 6, OUT, line=False)
    X.seg(a, b, w + 12, OUT)
    for p in (a, b):
        X.ell(p[0], p[1], r, r, col, line=False)
    X.seg(a, b, w, col)
