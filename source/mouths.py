#!/usr/bin/env python3
"""Mouth shapes for talking (lip sync) in the flat cartoon films: the standard ten cartoon mouth shapes (Preston
Blair's set, the classic animation reference), chosen from the script's words and timed to Sam's recording.

There is no speech recognition here, so the words are placed on the recording by measurement: the script line is
split over the recording's own stretches of speech (by syllable count), each word's letters become mouth shapes
spread across the word's time, and wherever the recording is quiet the mouth closes. The shape arrives a frame
before the sound (it reads as in sync). Read guides/figure-rig.md, section 6.

    import mouths
    track = mouths.track("This is an urgent situation.", stretches, env)   # stretches: [(start, end)] seconds
    shape = mouths.at(track, t)                                             # 'AI', 'E', 'O', ... or 'rest'
    sp['mouth'] = 'v:' + shape                                              # burnham draws it (after mouths.install(B))

    python3 mouths.py sheet OUT.png        # every shape on a face, and one line's track as a strip
"""
import math
import re
import sys

SHAPES = ['rest', 'MBP', 'etc', 'E', 'AI', 'O', 'U', 'WQ', 'FV', 'L']
# what each shape is for (Preston Blair): A/I open; E wide; O round; U small round; W/Q pucker; M/B/P lips shut;
# F/V top teeth on the lower lip; L tongue up; etc = C D G K N R S T Y Z and most consonants: teeth nearly together.


def _letters_to_shapes(word):
    """A word's sounds as mouth shapes, from its spelling (rough English rules, good enough for a cartoon)."""
    w = re.sub(r"[^a-z]", '', word.lower())
    out, i = [], 0
    while i < len(w):
        two = w[i:i + 2]
        c = w[i]
        if two in ('oo', 'ou', 'ew', 'ue'):
            out.append('U'); i += 2; continue
        if two in ('th',):
            out.append('L'); i += 2; continue
        if two in ('ee', 'ea', 'ie', 'ey'):
            out.append('E'); i += 2; continue
        if two in ('ph',):
            out.append('FV'); i += 2; continue
        if two in ('wh', 'qu'):
            out.append('WQ'); i += 2; continue
        if two in ('ch', 'sh'):
            out.append('etc'); i += 2; continue
        if c in 'aiy' and not (c == 'y' and i == 0):
            out.append('AI')
        elif c == 'e':
            if i == len(w) - 1 and len(w) > 2:     # silent final e
                i += 1
                continue
            out.append('E')
        elif c == 'o':
            out.append('O')
        elif c == 'u':
            out.append('U')
        elif c in 'mbp':
            out.append('MBP')
        elif c in 'fv':
            out.append('FV')
        elif c == 'l':
            out.append('L')
        elif c in 'wq':
            out.append('WQ')
        else:
            out.append('etc')
        i += 1
    # merge repeats, keep consonant clusters short
    merged = []
    for s in out:
        if not merged or merged[-1] != s:
            merged.append(s)
    return merged or ['etc']


def _syllables(word):
    w = re.sub(r"[^a-z]", '', word.lower())
    k = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and k > 1 and not w.endswith(('le', 'ee')):
        k -= 1
    return max(1, k)


def track(text, stretches, env=None, env_rate=100, lead=1 / 12):
    """[(t0, t1, shape)] for one line: text spread over the speech stretches (seconds from the line's start, as the
    voice is placed). env: the recording's loudness 0-1 (env_rate a second); quiet moments close the mouth."""
    words = text.split()
    if not words or not stretches:
        return []
    syl = [_syllables(w) for w in words]
    total_speech = sum(b - a for a, b in stretches)
    per_syl = total_speech / max(1, sum(syl))
    # walk the words through the stretches, never splitting a word across a pause
    out, k = [], 0
    for a, b in stretches:
        t = a
        budget = b - a
        need = 0
        start_k = k
        while k < len(words) and (need + syl[k] * per_syl <= budget * 1.25 or k == start_k):
            need += syl[k] * per_syl
            k += 1
        chunk = list(range(start_k, k))
        if not chunk:
            continue
        scale = budget / max(need, 1e-6)
        for j in chunk:
            d = syl[j] * per_syl * scale
            shapes = _letters_to_shapes(words[j])
            step = d / len(shapes)
            for n, s in enumerate(shapes):
                out.append((t + n * step - lead, t + (n + 1) * step - lead, s))
            if words[j][-1] in ',.?!':
                out.append((t + d - lead - 0.04, t + d - lead, 'rest'))
            t += d
    if k < len(words):                       # anything left goes on the end of the last stretch
        a, b = stretches[-1]
        out.append((b - lead, b + 0.2 - lead, 'etc'))
    if env is not None:                      # silence closes the mouth, whatever the text says
        quiet = []
        for t0, t1, s in out:
            m = (t0 + t1) / 2 + lead
            i = int(m * env_rate)
            lv = env[min(max(i, 0), len(env) - 1)] if len(env) else 1
            quiet.append((t0, t1, s if lv > 0.08 else 'rest'))
        out = quiet
    return out


def at(trk, t):
    for t0, t1, s in trk:
        if t0 <= t < t1:
            return s
    return 'rest'


# ------------------------------------------------------------------------------------------- drawing
def draw(p, sp, fx, my, shape, ink=(24, 20, 22)):
    """One mouth shape in the series' flat style, centred at (fx, my) in the person's units (burnham.mouth's place)."""
    from ed import curve
    lip = sp.get('lip_c', (198, 96, 104)) if sp.get('lips') else (150, 80, 84)
    dark, teeth, tongue = (70, 26, 30), (248, 248, 242), (196, 90, 96)
    if shape == 'rest':
        p.line([(fx - 16, my + 2), (fx, my), (fx + 16, my + 3)], ink, 2.4)
    elif shape == 'MBP':      # lips pressed together, a little fuller
        p.line([(fx - 18, my + 2), (fx - 6, my + 3), (fx + 6, my + 3), (fx + 18, my + 2)], ink, 3.2)
        p.line([(fx - 10, my + 7), (fx + 10, my + 7)], lip, 2.0)
    elif shape == 'etc':      # slightly open, teeth nearly together
        p.poly([(fx - 15, my - 1), (fx + 15, my - 2), (fx + 12, my + 7), (fx - 12, my + 7)], dark, ink, 2.0)
        p.poly([(fx - 12, my), (fx + 12, my - 1), (fx + 11, my + 3), (fx - 11, my + 4)], teeth, None)
    elif shape == 'E':        # wide, a little open, teeth showing
        p.poly(curve([(fx - 22, my - 1), (fx, my - 4), (fx + 22, my - 1), (fx + 14, my + 9), (fx - 14, my + 9)], 3), dark, ink, 2.2)
        p.poly([(fx - 17, my - 1), (fx + 17, my - 1), (fx + 14, my + 3), (fx - 14, my + 3)], teeth, None)
    elif shape == 'AI':       # wide open, top teeth, tongue
        p.poly(curve([(fx - 19, my - 3), (fx, my - 5), (fx + 19, my - 3), (fx + 12, my + 19), (fx, my + 23), (fx - 12, my + 19)], 3),
               dark, ink, 2.4)
        p.poly([(fx - 15, my - 2), (fx + 15, my - 2), (fx + 13, my + 3), (fx - 13, my + 3)], teeth, None)
        p.ell(fx, my + 17, 9, 4, tongue, None)
    elif shape == 'O':        # round and open
        p.ell(fx, my + 7, 11, 13, dark, ink, 2.4)
        p.ell(fx, my + 14, 6, 3, tongue, None)
    elif shape == 'U':        # small, round, lips forward
        p.ell(fx, my + 5, 7, 8, dark, ink, 2.4)
        p.line([(fx - 9, my + 5), (fx - 12, my + 5)], ink, 1.6)
        p.line([(fx + 9, my + 5), (fx + 12, my + 5)], ink, 1.6)
    elif shape == 'WQ':       # a tight pucker
        p.ell(fx, my + 4, 5, 6, dark, ink, 2.4)
        for k in (-1, 1):
            p.line([(fx + k * 8, my - 2), (fx + k * 10, my + 10)], ink, 1.4)
    elif shape == 'FV':       # top teeth on the lower lip
        p.poly([(fx - 15, my - 1), (fx + 15, my - 2), (fx + 12, my + 6), (fx - 12, my + 6)], dark, ink, 2.0)
        p.poly([(fx - 12, my - 1), (fx + 12, my - 2), (fx + 11, my + 4), (fx - 11, my + 4)], teeth, None)
        p.line([(fx - 13, my + 7), (fx, my + 9), (fx + 13, my + 7)], lip, 2.4)
    elif shape == 'L':        # open, tongue up behind the top teeth
        p.poly(curve([(fx - 15, my - 2), (fx + 15, my - 3), (fx + 10, my + 15), (fx - 10, my + 15)], 3), dark, ink, 2.2)
        p.poly([(fx - 12, my - 1), (fx + 12, my - 2), (fx + 11, my + 2), (fx - 11, my + 2)], teeth, None)
        p.ell(fx, my + 5, 6, 5, tongue, None)


_installed = {}


def install(B):
    """Teach burnham's mouth to draw 'v:SHAPE' (e.g. sp['mouth'] = 'v:AI'); every other mouth is left as it was."""
    if 'mouth' in _installed:
        return
    inner = B.mouth
    _installed['mouth'] = inner

    def mouth(p, sp, t, fx, my):
        m = sp.get('mouth', 'line')
        if isinstance(m, str) and m.startswith('v:'):
            return draw(p, sp, fx, my, m[2:])
        return inner(p, sp, t, fx, my)
    B.mouth = mouth


def sheet(out):
    """Every shape on a face, labelled, and one line's track as a strip under it."""
    import burnham as B
    from PIL import Image, ImageDraw, ImageFont
    install(B)
    B.SS = 1
    base = dict(skin=B.PALE, hw=68, hh=90, jaw='square', hair='crop', hair_c=(80, 60, 44), outfit='jumper',
                jacket=(52, 78, 132), shoulders=146, bottom=600, pose='side')
    tw, th = 220, 260
    img = Image.new('RGB', (tw * 5, th * 2 + 120), (240, 238, 232))
    f = ImageFont.truetype(B.SANS, 20)
    for i, s in enumerate(SHAPES):
        c = B.canvas((246, 244, 240))
        B.person(c, B.Cam(2.2, 540, 820), 540, 960, 1.0, dict(base, mouth='v:' + s), 0.0)
        tile = c.convert('RGB').crop((240, 380, 840, 1090)).resize((tw, th))
        img.paste(tile, ((i % 5) * tw, (i // 5) * th))
        ImageDraw.Draw(img).text(((i % 5) * tw + 8, (i // 5) * th + 6), s, font=f, fill=(20, 20, 20))
    trk = track("This is an urgent situation.", [(0.0, 1.6)])
    d = ImageDraw.Draw(img)
    for t0, t1, s in trk:
        x0, x1 = 10 + t0 * 650, 10 + t1 * 650
        d.rectangle([x0, th * 2 + 20, x1, th * 2 + 70], outline=(60, 60, 60))
        d.text((x0 + 2, th * 2 + 30), s, font=ImageFont.truetype(B.SANS, 13), fill=(20, 20, 20))
    d.text((10, th * 2 + 80), '"This is an urgent situation." over 1.6 s', font=f, fill=(20, 20, 20))
    img.save(out)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
