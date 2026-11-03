#!/usr/bin/env python3
"""Subtitles for a film with recorded lines (film-quality-rules 62; Terfwarts, 3 Nov: three pre-flight rounds went on
subtitles that flashed by too fast to read, and Myrtle's were timed as equal shares of her talking time).

Short and quick: each line is split at sentence and comma breaks into pieces of at most four words. Each piece comes
up on the syllable it starts with, found in Sam's take (the script's syllables laid over the recording's syllable
peaks), snapped to a pause when one is right there. Then every piece is made readable at the moment it is cut: on
screen at least 0.8 s and no more than 220 words a minute (pre-flight's own limit). A piece that is nearly long enough
makes the next one wait a touch; one that is too quick is joined to its neighbour, as long as the two still fit two
rows (62 characters).

In a film (the template's caption_at does this):

    import subtitles as SUB
    def caption_at(t):
        for i, ln in enumerate(LINES):
            nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
            if ln['start'] - 0.05 <= t < min(ln['end'] + 0.45, nxt):
                return SUB.line_caption(ln, t - ln['start'])
        return None

A line is a dict with 'n', 'text', '_dur' (seconds), and for a recording '_voice' (samples) and '_stretches'
([(start, end)] of talk, seconds into the line).
"""
import math
import re

import mouths

_CACHE = {}


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
    key = (ln.get('n'), ln['text'], round(ln['_dur'], 3))
    if key in _CACHE:
        return _CACHE[key]
    ch = chunks(ln['text'])
    out = [(ch[0][0], 0.0)]
    if ln.get('_voice') is not None and len(ch) > 1:
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
