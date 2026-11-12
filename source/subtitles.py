#!/usr/bin/env python3
"""Subtitles for a film with recorded lines (film-quality-rules 62; Terfwarts, 3 Nov: three pre-flight rounds went on
subtitles that flashed by too fast to read, and Myrtle's were timed as equal shares of her talking time).

Short and quick: each line is split at sentence and comma breaks into pieces of at most four words. Each piece comes
up on the syllable it starts with, found in Sam's take (the script's syllables laid over the recording's syllable
peaks), snapped to a pause when one is right there. Then every piece is made readable at the moment it is cut: on
screen at least 0.8 s and no more than 220 words a minute (pre-flight's own limit). A piece that is nearly long enough
makes the next one wait a touch; one that is too quick is joined to its neighbour, as long as the two still fit two
rows (62 characters).

The kit's style for every film (rule 62, tool job 11 Nov; set on Remakes): pieces of 3-5 words, each up on the
syllable it starts with, never joined into longer rows (`pieces`), drawn large in the lower third in Montserrat Black,
white with a black outline and shadow (`draw`). finish.py burns them in from the film's caption_at and refuses a film
without one. `line_caption` / `chunk_times` (joined pieces, the old white caption) stay only for films finished before.

MAP
  chunks ........... the words cut into pieces at sentence and comma breaks
  pieces ........... the kit's timing: each piece on its syllable, never joined (fix: {piece index: seconds})
  caption_at ....... the piece on screen at t, from the film's LINES (what a film's caption_at returns)
  draw ............. the kit's caption look, on an RGBA layer or picture
  readable_faults .. rule 62's check at the delivered speed (SPEED, rule 70): rows, width, time on screen
  readable / chunk_times / line_caption ... the old joined style (finished films only)

In a film (the template does this):

    import subtitles as SUB
    PIECE_FIX = {}                                   # {line n: {piece index: seconds}} only where a take needs it
    def caption_at(t):
        return SUB.caption_at(LINES, t, PIECE_FIX)

A line is a dict with 'n', 'text', '_dur' (seconds), and for a recording '_voice' (samples) and '_stretches'
([(start, end)] of talk, seconds into the line).
"""
import math
import os
import re

import mouths

_CACHE = {}
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'Montserrat-Black.ttf')   # Gotham Black's free stand-in (Sam, 11 Nov)
SPEED = 1.1                    # rule 70: every animatic and final is delivered at 1.1x (finish.py)
SIZE, WIDE, BASE, ROW = 64, 900, 1450, 84   # the look on the 1080 x 1920 frame: px size, row width, last row's y, row gap


def chunks(text, most=4):
    """[(words, share of the line)]: sentence and comma breaks, then even groups of at most `most` words; a lone last
    word joins the words before it; one or two words alone are joined to the next piece."""
    parts = [p.strip().split() for p in re.split(r'(?<=[.,?!])\s+', text) if p.strip()]
    out = []
    for w in parts:
        k = math.ceil(len(w) / most)
        cuts = [round(i * len(w) / k) for i in range(k + 1)]
        for g in [w[cuts[i]:cuts[i + 1]] for i in range(k)]:
            if len(g) == 1 and out and out[-1][-1][-1] not in '.?!' and len(out[-1]) < 5:
                out[-1] = out[-1] + g
            else:
                out.append(g)
    i = 0
    while i < len(out) - 1:
        if len(out[i]) < 3 and len(out[i]) + len(out[i + 1]) <= 5 and len(' '.join(out[i] + out[i + 1])) <= 34:
            out[i:i + 2] = [out[i] + out[i + 1]]
        else:
            i += 1
    n = sum(len(c) for c in out)
    return [(' '.join(c), len(c) / n) for c in out]


def readable(out, end):
    """[(text, start)] made readable (see the top). `end`: when the last piece goes off, seconds into the line."""
    out = list(out)
    i = 0
    while i < len(out):
        a = out[i][1]
        b = out[i + 1][1] if i + 1 < len(out) else end
        need = max(0.82, len(out[i][0].split()) * 0.275)
        deficit = need - (b - a)
        if 0 < deficit <= 0.3 and i + 1 < len(out):      # nearly long enough: the next piece comes up a touch later
            nb = out[i + 2][1] if i + 2 < len(out) else end
            nneed = max(0.82, len(out[i + 1][0].split()) * 0.275)
            if nb - (out[i + 1][1] + deficit) >= nneed:
                out[i + 1] = (out[i + 1][0], out[i + 1][1] + deficit)
                i += 1
                continue
        if b - a < need and len(out) > 1:
            j = i + 1 if i + 1 < len(out) else i - 1
            lo, hi = sorted((i, j))
            text = out[lo][0] + ' ' + out[hi][0]
            if len(text) <= 62:
                out[lo:hi + 1] = [(text, out[lo][1])]
                i = lo                             # the joined piece is looked at again (up to two rows)
                continue
        i += 1
    return out


def chunk_times(ln, tail=0.45):
    """[(text, start)] for one line, seconds into the line, timed from its recording and made readable."""
    text = ln.get('sub') or ln['text']           # 'sub': the subtitle's own wording, when Sam wants it different
    key = (ln.get('n'), text, round(ln['_dur'], 3))
    if key in _CACHE:
        return _CACHE[key]
    ch = chunks(text)
    out = [(ch[0][0], 0.0)]
    parts = [p.split() for p in re.split(r'(?<=[.,?!])\s+', text) if p.strip()]
    st = ln.get('_stretches') or []
    if ln.get('_voice') is not None and len(ch) > 1 and len(parts) == len(st) > 1:
        # one stretch of talk per phrase (Ad-Vanced Notice line 9, 8 Nov: counted syllables put "Between you and
        # me," two seconds early): each piece is timed inside its own phrase's stretch, by its share of the words
        bounds = [0]
        for p in parts:
            bounds.append(bounds[-1] + len(p))
        w = len(ch[0][0].split())
        for c, _ in ch[1:]:
            k = max(i for i in range(len(parts)) if bounds[i] <= w)
            a0, a1 = st[k]
            at = a0 + (w - bounds[k]) / len(parts[k]) * (a1 - a0) - (0.05 if w == bounds[k] else 0.0)
            out.append((c, max(out[-1][1] + 0.5, at)))
            w += len(c.split())
    elif ln.get('_voice') is not None and len(ch) > 1:
        import press_secretary as PS
        beats = PS._syllable_beats(ln['_voice'], ln['_stretches'])
        syl = [sum(mouths._syllables(w) for w in c.split()) for c, _ in ch]
        tot = sum(syl)
        acc = 0
        for (c, _), n in zip(ch[1:], syl[:-1]):
            acc += n
            k = min(len(beats) - 1, int(round(acc / tot * len(beats))))
            at = beats[k] - 0.1 if len(beats) else out[-1][1] + 1.0
            starts = [a for a, _ in ln['_stretches'][1:] if abs(a - at) < 0.35]   # a pause right there: change on it
            if starts:
                at = min(starts, key=lambda a: abs(a - at)) - 0.05
            out.append((c, max(out[-1][1] + 0.5, at)))
    else:
        a = 0.0
        for c, share in ch[1:]:
            a += share * ln['_dur']
            out.append((c, a))
    out = readable(out, ln['_dur'] + tail)
    _CACHE[key] = out
    return out


def line_caption(ln, u):
    """The subtitle on screen `u` seconds into the line."""
    text = None
    for c, t0 in chunk_times(ln):
        if text is None or u >= t0:
            text = c
    return text


# ------------------------------------------------------------------------------- the kit's style (rule 62, 11 Nov)

def pieces(ln, fix=None, most=4):
    """[(text, start)] seconds into the line: 3-5 words at a time, each up on the syllable it starts with (the take's
    syllable beats), never joined into longer rows; a piece shorter than 0.45 s pushes the next a touch later.
    fix: {line n: {piece index: seconds}} where a take's pause fools the syllable count. A line with no recording is
    timed by each piece's share of the words."""
    if '_pieces' in ln:
        return ln['_pieces']
    ch = chunks(ln.get('sub') or ln['text'], most=most)
    out = [[ch[0][0], 0.0]]
    if len(ch) > 1 and ln.get('_voice') is not None:
        import press_secretary as PS
        beats = PS._syllable_beats(ln['_voice'], ln['_stretches'])
        syl = [sum(mouths._syllables(w) for w in c.split()) for c, _ in ch]
        acc = 0
        for (c, _), n in zip(ch[1:], syl[:-1]):
            acc += n
            k = min(len(beats) - 1, int(round(acc / sum(syl) * len(beats))))
            out.append([c, max(out[-1][1] + 0.45, beats[k] - 0.06 if len(beats) else out[-1][1] + 0.8)])
    elif len(ch) > 1:
        a = 0.0
        for (c, _), (_, share) in zip(ch[1:], ch[:-1]):
            a += share * ln.get('_dur', ln.get('end', 0) - ln.get('start', 0))
            out.append([c, max(out[-1][1] + 0.45, a)])
    for i, at in ((fix or {}).get(ln.get('n'), {}) or {}).items():
        out[i][1] = at
    ln['_pieces'] = [tuple(p) for p in out]
    return ln['_pieces']


def caption_at(lines, t, fix=None, lead=0.05, tail=0.45):
    """The piece on screen at t (or None): each line's pieces from just before it starts to `tail` after it ends,
    never running into the next line."""
    for i, ln in enumerate(lines):
        nxt = lines[i + 1]['start'] - lead if i + 1 < len(lines) else 1e9
        if ln['start'] - lead <= t < min(ln['end'] + tail, nxt):
            u = t - ln['start']
            return [c for c, a in pieces(ln, fix) if a <= u or a == 0.0][-1]
    return None


def _font(ss=1):
    from PIL import ImageFont
    return ImageFont.truetype(FONT, int(SIZE * ss))


def rows(text, ss=1):
    import burnham as B
    return B.wrap(text, _font(ss), WIDE * ss)


def draw(img, text, ss=None, base=None):
    """The kit's caption on an RGBA picture or layer: large, lower third, at most two rows, Montserrat Black, white
    with a black outline and a shadow down and right. ss: the picture's supersampling (burnham.SS when not given)."""
    from PIL import Image, ImageDraw
    if ss is None:
        import sys
        B = sys.modules.get('burnham')
        ss = B.SS if B else 1
    f = _font(ss)
    rs = rows(text, ss)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, row in enumerate(rs):
        y = ((base or BASE) - ROW * (len(rs) - 1 - i)) * ss   # base: a shot's own height (Blessed note 37)
        d.text((540 * ss + 6 * ss, y + 7 * ss), row, font=f, fill=(0, 0, 0, 150), anchor='mm',
               stroke_width=int(7 * ss), stroke_fill=(0, 0, 0, 150))                 # the shadow, down and right
        d.text((540 * ss, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=int(7 * ss),
               stroke_fill=(0, 0, 0))
    if img.mode == 'RGBA':
        img.alpha_composite(lay)
    else:
        img.paste(lay, (0, 0), lay)


def readable_faults(caption_at, end, fps, speed=SPEED):
    """Rule 62 on the delivered file (rule 70: played at `speed`): each piece at most 5 words and two rows that fit
    the width, on screen at least 0.8 s and at most 220 words a minute AT THAT SPEED. Returns faults."""
    seen = {}
    for i in range(int(end * fps)):
        c = caption_at(i / fps)
        if c:
            seen.setdefault(c, []).append(i / fps)
    f = _font()
    out = []
    for c, ts in seen.items():
        rs = rows(c)
        wide = max(f.getbbox(r)[2] for r in rs)
        if len(rs) > 2 or wide > WIDE or len(c.split()) > 5:
            out.append(f'caption "{c}": {len(c.split())} words, {len(rs)} rows, {wide} px wide (max 5 words, 2 rows, '
                       f'{WIDE} px)')
        dur, words = len(ts) / fps / speed, len(c.split())
        if dur < 0.8 or words / max(dur, 0.01) * 60 > 220:
            out.append(f'caption "{c}": {dur:.2f} s on screen at {speed:g}x for {words} words (too fast to read)')
    return out
