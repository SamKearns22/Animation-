"""Kemi's build MEASURED from Sam's three photos (Open Wounds chat 6, 24 Nov; Sam's note 7).

Every reading below was taken off a pixel grid laid over the photo (grid.py) and, where the clothes stand out from the
background, checked by a row scan of the white top's runs. Widths are over each photo's own OUTER SHOULDER (the arm
tops, as the drawing's: 2 (sw + 20.5) body units), depths below the collar base over the same width, so a photo and
a drawing compare at any size. Heights as shares of her height use her head (crown to chin) and a stature of 7.4
heads (her knee height in photo 2, 2.07 heads with heels, is 0.28 of stature on the standard tables).

    python3 notes/learn/kemi-build/measure.py OUT.jpg     the sheet: each photo with its lines, beside the drawings
    python3 notes/learn/kemi-build/measure.py --json      the numbers (written to measures.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
REF = os.path.join(ROOT, 'references', 'brexit-is-done')

# photo: collar base y, head (crown, chin), outer shoulder row and x span; then each measure: (name, y, x0, x1, note)
PHOTOS = {
    'kemi-full-1-portrait-sam.jpg': dict(collar=175, head=(65, 157), shoulder=(200, 73, 236), what='front, blazer', m=[
        ('hip', 420, 93, 232, 'the dress below the jacket, at its widest (hands clasped in front, not at the sides)'),
        ('thigh', 470, 97, 230, 'the dress over the thighs'),
        ('jacket hem', 395, None, None, 'her blazer ends here, above the hip')]),
    'kemi-full-3-walking-sam.jpg': dict(collar=125, head=(15, 117), shoulder=(140, 242, 403), what='front, a little '
                                        'turned, wrap top', m=[
        ('bust', 225, 263, 385, 'row scan: the top 263-385, the left sleeve apart at 213-257'),
        ('waist', 262, 258, 377, 'row scan of the white top, rows 254 and 270 (the wrap band): 116 and 123 wide, '
         '0.72-0.76 of the shoulders; the rows between break on the folds\' shadows'),
        ('upper waist', 222, 263, 386, 'row 222, just under the bust: 0.76 (v1 drew 0.67 here: the hourglass pinch)')]),
    'kemi-full-2-seated-sam.jpg': dict(collar=108, head=(42, 100), shoulder=(115, 58, 158), what='seated', m=[
        ('knee to sole', None, None, None, 'the standing leg: knee at 275, the heel on the floor at 395 (120 high, '
         '2.07 heads; her heels add about 0.3 head)')]),
}
STATURE_HEADS = 7.4

# the drawing's measures for the same names, in body units below the collar (views.py: hip joint 450, elbow 266)
DRAWN_Y = {'bust': 200, 'waist': 275, 'hip': 470}   # (upper waist: body y 193, checked by hand)


def numbers():
    out = {}
    for f, ph in PHOTOS.items():
        sy, sx0, sx1 = ph['shoulder']
        W = sx1 - sx0
        head = ph['head'][1] - ph['head'][0]
        H = head * STATURE_HEADS
        rec = dict(what=ph['what'], outer_shoulder_px=W, head_px=head, outer_shoulder_of_height=round(W / H, 3),
                   measures={})
        for name, y, x0, x1, note in ph['m']:
            r = dict(note=note)
            if y is not None:
                r['depth_over_shoulder'] = round((y - ph['collar']) / W, 2)
                r['depth_of_height'] = round((y - ph['collar']) / H, 3)
            if x0 is not None:
                r['width_px'] = x1 - x0
                r['width_over_shoulder'] = round((x1 - x0) / W, 2)
                r['width_of_height'] = round((x1 - x0) / H, 3)
            if name == 'knee to sole':
                r['of_height'] = round(120 / H, 3)
            rec['measures'][name] = r
        out[f] = rec
    return out


def build_from(nums, sw=140.0):
    """The body.FIGS 'straight' numbers: each width over the outer shoulder, turned into half width over sw."""
    W = 2 * (sw + 20.5)
    get = {n: m for rec in nums.values() for n, m in rec['measures'].items()}
    return {n: dict(y=DRAWN_Y[n], k=round(get[n]['width_over_shoulder'] * W / 2 / sw, 2),
                    photo_depth_y=round(get[n]['depth_over_shoulder'] * W)) for n in DRAWN_Y}


def drawn_widths(fig, sw=140.0, bottom=505.0):
    sys.path.insert(0, os.path.join(ROOT, 'source'))
    import body as B
    W = 2 * (sw + 20.5)
    return {n: round(2 * B.fig_half(fig, y, sw, bottom) / W, 2) for n, y in DRAWN_Y.items()}


def sheet(out):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, os.path.join(ROOT, 'source'))
    import castsheet as CS
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 21)
    COL = {'bust': (40, 120, 230), 'waist': (230, 60, 40), 'hip': (30, 160, 60), 'thigh': (150, 150, 150)}
    Hh = 900
    panels = []
    for f, ph in PHOTOS.items():
        if not ph['m'] or ph['m'][0][1] is None:
            continue
        im = Image.open(os.path.join(REF, f)).convert('RGB')
        k = Hh / im.height
        im = im.resize((int(im.width * k), Hh), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        sy, sx0, sx1 = ph['shoulder']
        d.line([(sx0 * k, sy * k), (sx1 * k, sy * k)], fill=(250, 200, 0), width=4)
        for name, y, x0, x1, _ in ph['m']:
            if x0 is None or name not in COL:
                continue
            d.line([(x0 * k, y * k), (x1 * k, y * k)], fill=COL[name], width=5)
            d.text((x1 * k + 6, y * k - 14), name, fill=COL[name], font=small)
        panels.append(('photo', im))
    cast, PP = CS._setup('brexit-is-done', ['may', 'kemi'])
    for label, who, fig in (('Kemi, new (measured)', 'kemi', 'straight'), ('Kemi, v1 (May\'s)', 'kemi', 'female'),
                            ('May (kept)', 'may', 'female')):
        sp = dict(cast[who])
        sp['figure'] = fig
        a, b = CS.draw(sp, 0, PP)
        s = 0.5 * sp['height'] / 1.75
        y0 = 840 - 928 * s
        sw = sp.get('shoulders', 150)
        W = 2 * (sw + 20.5)
        im = Image.fromarray(a).crop((b[0] - 60, b[1] - 10, b[2] + 160, b[3] + 10))
        ox, oy = b[0] - 60, b[1] - 10
        d = ImageDraw.Draw(im)
        scr = lambda u: (y0 + u * s - 470) * 2 + 960 - oy
        sxu = lambda u: 540 + 2 * s * u - ox
        import body as B
        d.line([(sxu(-(sw + 20.5)), scr(30)), (sxu(sw + 20.5), scr(30))], fill=(250, 200, 0), width=4)
        for name, y in DRAWN_Y.items():
            hw = B.fig_half(fig, y, sw, sp.get('bottom', 505))
            d.line([(sxu(-hw), scr(y)), (sxu(hw), scr(y))], fill=COL[name], width=5)
            d.text((sxu(hw) + 50, scr(y) - 14), f'{name} {2 * hw / W:.2f}', fill=COL[name], font=small)
        k = Hh / im.height
        im = im.resize((int(im.width * k), Hh), Image.LANCZOS)
        panels.append((label, im))
    # the outlines (as Sam's note 7 picture, notes/learn/womans-build/outline-female-v1.jpg): headless, black
    outl = []
    for label, who, fig in (('Kemi new', 'kemi', 'straight'), ('Kemi v1', 'kemi', 'female'), ('May', 'may', 'female')):
        for yaw in (0, 45):
            sp = dict(cast[who])
            sp['figure'] = fig
            sp['hair_style'] = 'back'
            for kk in ('hat', 'hat_c', 'specs'):
                sp.pop(kk, None)
            a, b = CS.draw(sp, yaw, PP)
            s = 0.5 * sp['height'] / 1.75
            neck = int((840 - 928 * s - 470) * 2.0 + 960) + 6
            m = (np.abs(a.astype(int) - 255).sum(2) > 30)
            m[:neck] = False
            o = np.where(m[..., None], 20, 255).astype(np.uint8).repeat(3, 2)
            im = Image.fromarray(o).crop((b[0] - 20, neck - 10, b[2] + 20, b[3] + 10))
            k = 560 / im.height
            outl.append((f'{label} {"front" if yaw == 0 else "3/4"}', im.resize((int(im.width * k), 560))))
    W1 = sum(p.width for _, p in panels) + 30 * (len(panels) + 1)
    W2 = sum(p.width for _, p in outl) + 40 * (len(outl) + 1)
    Wt = max(W1, W2)
    page = Image.new('RGB', (Wt, Hh + 150 + 640), (236, 233, 226))
    d0 = ImageDraw.Draw(page)
    x = 40
    for label, p in outl:
        page.paste(p, (x, Hh + 210))
        d0.text((x, Hh + 160), label, fill=(30, 30, 30), font=small)
        x += p.width + 40
    d = ImageDraw.Draw(page)
    x = 30
    for label, p in panels:
        page.paste(p, (x, 70))
        d.text((x, 20), 'Sam\'s photo' if label == 'photo' else label, fill=(30, 30, 30), font=font)
        x += p.width + 30
    d.text((30, Hh + 85), 'Yellow: the shoulders (arm tops). Widths as a share of the yellow line. Photos: bust 0.76, '
           'waist 0.72-0.76, hip 0.85. Below: the outlines, as in note 7.', fill=(30, 30, 30), font=small)
    page.save(out, quality=88)
    return out


if __name__ == '__main__':
    nums = numbers()
    res = dict(photos=nums, build_straight=build_from(nums),
               drawn={f: drawn_widths(f) for f in ('straight', 'female', 'man', None) if True})
    res['drawn'] = {str(k): v for k, v in res['drawn'].items()}
    json.dump(res, open(os.path.join(HERE, 'measures.json'), 'w'), indent=1)
    if sys.argv[1:] and sys.argv[1] != '--json':
        print(sheet(sys.argv[1]))
    print(json.dumps(dict(build=res['build_straight'], drawn=res['drawn']), indent=0))
