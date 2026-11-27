"""MAP: stand_band(p, view, ...) - a jacket's stand collar drawn as a band wrapped round the foot of the neck.

Shared for any jacket (Sam's Y, 27 Nov, Patriots 5 note 4): the collar is a band in the jacket's OWN colour, never a
flat lighter box beside the neck; its top and bottom edges curve round the neck (the front of a ring seen from a
little above), its ends turn away darker, and the opening (zip or front edge) shows where the jacket fastens. Alike in
every view: front, three, side, three_back, back. Body units, y down; the neck's centre cx, the neck's half width nk.
"""
import body as B

INK = (20, 20, 24)


def _arc(x0, x1, y_end, y_mid, n=9):
    """A shallow curve from (x0, y_end) to (x1, y_end) through (mid, y_mid): a ring's near edge."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append((x0 + (x1 - x0) * t, y_end + (y_mid - y_end) * (1 - (2 * t - 1) ** 2)))
    return out


def stand_band(p, view, cx, nk, colour, top=-24, bot=30, opening=None, zip_c=(96, 96, 104)):
    """Draw the band. opening: x of the fastening on the near side (None: centre front; back views have none)."""
    dark = B.dk(colour, 0.78)
    back = view in ('back', 'three_back')
    if view == 'side':
        tx = cx + nk + 22                                        # the top hugs the neck's front
        fx = max(tx, tx if opening is None else opening + 2)       # the foot meets the zip on the chest
        bx = cx - nk - 10                                         # the back of the band, round the nape
        pts = [(bx, top - 6), (tx - 8, top), (tx, top + 6), (fx + 2, bot - 4),   # the front slopes to the chest
               (fx + 4, bot + 4), (bx - 6, bot - 2)]
        p.poly(pts, colour, INK, 2.4)
        p.poly([(bx, top - 6), (bx + 10, top - 4), (bx + 6, bot - 2), (bx - 6, bot - 2)], dark, None)   # turning away
        p.line([(bx + 4, top), (fx - 10, top + 8)], dark, 1.6)                                # the rim's thickness
        p.line([(tx - 1, top + 12), (fx, bot)], zip_c, 2.0)                                   # the front edge, the zip
        p.line(pts + pts[:1], INK, 2.4)
        return
    ht, hb = nk + 12, nk + 24                        # wider at the foot: it sits on the shoulders
    sag_t, sag_b = (5, 8) if back else (9, 10)       # the near edge of a ring seen from a little above
    up = _arc(cx - ht, cx + ht, top, top + sag_t)
    lo = _arc(cx + hb, cx - hb, bot - 6, bot + sag_b)
    p.poly(up + lo, colour, INK, 2.4)
    for sg in (-1, 1):                               # the ends turning away round the neck: darker
        e = [(cx + sg * ht, top), (cx + sg * (ht - 6), top + 3), (cx + sg * (hb - 7), bot - 3), (cx + sg * hb, bot - 6)]
        p.poly(e, dark, None)
    p.line([(x, y + 6) for x, y in up[1:-1]], dark, 1.6)                              # the rim's thickness
    if not back:
        ox = cx if opening is None else max(cx - ht + 10, min(cx + ht - 10, opening))
        k = (ox - cx) / max(ht, 1)
        y0 = top + sag_t * (1 - k * k)
        p.poly([(ox - 7, y0 - 1), (ox + 7, y0 - 1), (ox + 1, y0 + 12)], dark, None)  # the small V where it fastens
        p.line([(ox, y0 + 2), (ox + 1, bot + sag_b * (1 - k * k) - 2)], zip_c, 2.0)
    p.line(up + lo + up[:1], INK, 2.4)
