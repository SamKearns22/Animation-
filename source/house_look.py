"""house_look: the house look (rule S7; Sam, 12 Nov): every drawing looks cut from paper and laid on paper.

MAP (rule 61):
  LOOK 25          the ONE setting: paper strength, light-edge strength, shadow strength and offset
  paper 45         the paper picture (fixed grain + soft blotches), made once per size, the same every frame
  shapes 75        the drawing split into its flat-colour shapes; each shape's height (smaller shapes lie on bigger)
  edges 125        per shape: a soft shadow down and right onto what lies beneath, and a thin light top edge
  apply 165        all of it, in order; film_engine.render calls it ONCE per drawing, before captions go on

Applied to the drawing only: captions, the Hook Text and the sign-off go on afterwards, clean. Shapes are found from the
picture's flat colours, not from its black outlines: an outline belongs to the shape it surrounds, and thin things
(outlines, wires, poles, ropes) cast no shadow.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd

# The one setting (brief: "a single setting so it can be changed"). Sizes are at 1080 wide and scale with the picture.
LOOK = dict(
    paper=0.70,          # soft light at 70% (as tested and chosen, 12 Nov)
    paper_depth=0.45,    # the paper's texture at 45%: the test's recipe alone came out 2.2x stronger than the test Sam
                         # chose (measured on the sky in his two screenshots, 12 Nov: grain 2.8x, blotches 1.9x)
    light=0.22,          # the light top edge: this much of the way to white
    light_px=2.0,        # its thickness
    shadow=0.26,         # the darkest a shadow gets (fraction darker)
    shadow_dx=4.0,       # down and right
    shadow_dy=6.0,
    shadow_soft=3.0,     # blur of the shadow's edge
    thin_px=4.0,         # a shape no thicker than twice this casts no shadow: wires, poles, ropes
    min_area=60,         # smaller patches (texture, sparks, specks) join the shape round them
    ramp=(0.5, 2.0),     # a shape lies fully on another only when that one is e^2 = 7 times bigger, not at all under
                         # e^0.5 = 1.6 times, fading between: near-equal shapes (a checked shirt's squares and bars)
                         # never flip which is on top from one drawing to the next (they flickered, 12 Nov)
)

_PAPER = {}


# ------------------------------------------------------------------------------------------------------------ paper
def paper(w, h):
    """The paper picture, w x h, grey around 0.5: fine grain averaged with soft blotches. Seeded, so every frame and
    every render get the same sheet (paper doesn't crawl)."""
    if (w, h) in _PAPER:
        return _PAPER[(w, h)]
    # made by exactly the steps of the test Sam chose (12 Nov). A first build copied the recipe by hand and came out
    # with twice the blotches and half the grain: "far more smudged" (Sam, 12 Nov). Never re-derive it.
    import subprocess
    import imageio_ffmpeg

    def make(size, chain):
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-f', 'lavfi', '-i',
                              f'color=gray:s={size},format=gray,{chain}', '-frames:v', '1', '-f', 'rawvideo',
                              '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.uint8).reshape(h, w).astype(np.float32) / 255
    grain = make(f'{w}x{h}', 'noise=alls=90,gblur=sigma=0.9,eq=contrast=2.2')
    blot = make(f'{max(8, w // 8)}x{max(8, h // 8)}', f'noise=alls=90,gblur=sigma=4,eq=contrast=4,scale={w}:{h}')
    p = (grain + blot) / 2
    p = p.mean() + LOOK['paper_depth'] * (p - p.mean())
    _PAPER[(w, h)] = p
    return p


def lay_on_paper(a, strength):
    """Soft light: where the paper is darker than mid-grey the drawing darkens a touch, lighter lightens it."""
    b = paper(a.shape[1], a.shape[0])[..., None]
    soft = (1 - 2 * b) * a * a + 2 * b * a
    return a + strength * (soft - a)


# ----------------------------------------------------------------------------------------------------------- shapes
def _disk(r):
    r = max(1, int(round(r)))
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def shapes(a):
    """(height map, ink mask, thin mask). Each flat-colour shape is one region; its height is -log(area), so a smaller
    shape lies on a bigger one (an eye on a face, a face on a body, a body on the sky). Black outlines (ink: dark and
    thin) take the height of the highest shape they touch, as an outline is part of the shape it goes round."""
    h, w = a.shape[:2]
    k = w / 1080
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    dark = lum < 0.2
    ink = dark & ~nd.binary_opening(dark, _disk(3 * k))           # dark and thin: an outline, not a black coat
    e = np.zeros((h, w), bool)
    d = np.abs(np.diff(a, axis=1)).max(2) > 0.07                   # a colour change between neighbours
    e[:, :-1] |= d
    e[:, 1:] |= d
    d = np.abs(np.diff(a, axis=0)).max(2) > 0.07
    e[:-1] |= d
    e[1:] |= d
    lab, n = nd.label(~(e | ink))
    area = np.bincount(lab.ravel(), minlength=n + 1)
    small = area < LOOK['min_area'] * k * k
    small[0] = True
    # every unlabelled pixel (a colour change, a speck) joins its nearest shape
    idx = nd.distance_transform_edt(small[lab], return_distances=False, return_indices=True)
    lab = lab[idx[0], idx[1]]
    # thickness: how far a shape's middle is from its edge; thin shapes cast no shadow
    inner = nd.distance_transform_edt(~(e | ink))
    thick = np.asarray(nd.maximum(inner, lab, index=np.arange(n + 1)))
    height = -np.log(np.maximum(area, 1)).astype(np.float32)
    H = height[lab]
    thin = (thick < LOOK['thin_px'] * k)[lab]
    r = int(round(3 * k)) * 2 + 1
    H = np.where(ink, nd.maximum_filter(np.where(ink, -1e9, H), size=r), H)
    thin = np.where(ink, nd.minimum_filter(np.where(ink, True, thin), size=r), thin)
    return H, ink, thin


# ------------------------------------------------------------------------------------------------------------ edges
def _shift(m, dx, dy, fill):
    """m moved right by dx and down by dy (whole pixels)."""
    out = np.full_like(m, fill)
    h, w = m.shape
    out[max(0, dy):h + min(0, dy), max(0, dx):w + min(0, dx)] = m[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
    return out


def _above(top, under):
    """How far a shape of height `top` lies on one of height `under`: 0 (not at all) to 1 (fully)."""
    lo, hi = LOOK['ramp']
    return np.clip((top - under - lo) / (hi - lo), 0, 1).astype(np.float32)


def edges(a):
    """The drawing with each shape's soft shadow down-right onto the shapes beneath, and its light top edge."""
    h, w = a.shape[:2]
    k = w / 1080
    H, ink, thin = shapes(a)
    # the shadow: where a thick shape, moved down and right, lies on what is there
    Hc = np.where(thin, -1e9, H).astype(np.float32)
    dx, dy = int(round(LOOK['shadow_dx'] * k)), int(round(LOOK['shadow_dy'] * k))
    moved = _shift(Hc, dx, dy, -1e9)
    s = nd.gaussian_filter(_above(moved, H), LOOK['shadow_soft'] * k)
    near = int(round(2 * LOOK['shadow_soft'] * k)) * 2 + 1
    s *= _above(nd.maximum_filter(moved, size=near), H) > 0           # never on the casting shape itself
    a = a * (1 - LOOK['shadow'] * s[..., None])
    # the light top edge: a shape's own pixels just below a lower shape (outlines are looked through: each outline
    # pixel takes the height of the first non-outline pixel above it)
    Hup = H.copy()
    for _ in range(int(round(4 * k)) + 1):
        Hup = np.where(ink, _shift(Hup, 0, 1, 1e9), Hup)
    lit = np.zeros((h, w), np.float32)
    for dd in range(1, max(1, int(round(LOOK['light_px'] * k))) + 1):
        lit = np.maximum(lit, _above(H, _shift(Hup, 0, dd, 1e9)))
    lit *= ~ink
    lit = nd.gaussian_filter(lit, 0.6 * k)
    return a + (1 - a) * (LOOK['light'] * lit[..., None])


# ------------------------------------------------------------------------------------------------------------ apply
def apply(img):
    """The house look on one drawing (PIL image, no captions yet) -> PIL RGB image."""
    a = np.asarray(img.convert('RGB'), np.float32) / 255
    a = lay_on_paper(edges(a), LOOK['paper'])
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))
