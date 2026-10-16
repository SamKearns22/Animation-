"""The New Press Secretary (working title): one slow push-in on the new White House press secretary's first
briefing. She reads near-gibberish from her notes, keeps looking down at them, flashes big strange smiles at the room,
and ends on a huge flat sigh and "...Venezuela." Silent for now (Sam records the voice later). Brief:
prompts/press-secretary.md. Satire style (flat colour, one outline, hand-cut shapes, circle hands).

    python3 source/press_secretary.py cast OUT.png           her, every view and expression, the reporters
    python3 source/press_secretary.py stills OUT.jpg T [T..] one contact sheet of stills at these times
    python3 source/press_secretary.py final OUT.mp4 [--small]
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  camera, pen, canvas
from ed import INK, curve, oval, smooth   # noqa: E402
from satire_style import rough   # noqa: E402
import filmkit                   # noqa: E402
import figure as F               # noqa: E402

NAME = 'press-secretary'
FPS = 12
SERIF = os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf')

# =============================================== STORY ===============================================================
# The draft script as beats. ('say', words, gaze) | ('look', 'up'/'down') | ('smile', level, secs) | ('hold', secs)
# | ('sigh', secs). Speaking time comes from the syllables; '...' leaves a long halting gap, '.' a short one.
# When Sam's recording arrives, these timings are replaced by the recording's.
# Sam's script and recording (15 Oct): source/audio/press-secretary.m4a. Tags place her acting between words:
# [down] / [up] she looks at her notes or the room (an instant glance), [double] a nervous check up and straight back
# down, [smile2] / [smile3] a big smile at the room in the pause, [sigh] the big sigh in the pause before the next word.
# '||' marks the five longest silences in the recording (paragraph ends, the silence, the sigh, before the last word),
# which anchor the words; inside each part the words are spread over the real stretches of speech by syllables.
SCRIPT = ("[down] So like uh it's really, [up] yes, it's really important that with the president we are, [down] "
          "we work tirelessly for America, [smile2] [down] and the people, they understand that, and I look forward to "
          "the president, [double] the president, with his helping, [up] with his [onsmile3] agenda. || "
          "My president and I, eh, [down] excuse me, [up] my [wide] master and I are very happy to be, [smile2] [down] "
          "and like, our kids are [delight] ^helicopters, [up] and I really think that with the biggest swell of "
          "support, the people are really, I just, [down] you know it's so. [up] [awkward] ^I'll get back to you "
          "on that. || [down] So, like. I think if we all just, you know, [up] [excited] cause it's booming, [smile3] and we've had "
          "a one day war, [down] and I just need, I just need. || I just want. || [sigh] Venezuela. || [dead] venezuela.")
# Sam's acting notes (15 Oct): looks down at "we work tirelessly"; big smile DURING "agenda"; eyes slightly wide at
# "master"; delighted at "helicopters"; slightly awkward through "I'll get back to you on that".
AUDIO_PARTS = [  # (recording, from, to, anchors inside it): Sam's second take of paragraphs 1-2 (15 Oct), then the
    ('press-secretary-p12', 0.0, None, 1),    # first take from "So, like." to the end
    ('press-secretary', 44.6, None, 3)]
JOIN_GAP = 1.2                   # the pause between the two takes (a paragraph break)
LEAD = 0.6                       # seconds of her at the podium before the first word
TAIL = 0.9                       # the hold on her face after the last word, then the hard cut


def syllables(w):
    w = w.lower().strip(".,!?-'")
    groups = sum(1 for i, c in enumerate(w) if c in 'aeiouy' and (i == 0 or w[i - 1] not in 'aeiouy'))
    return max(1, groups - (1 if w.endswith('e') and groups > 1 and not w.endswith('le') else 0))


def _voice():
    """The soundtrack's voice: the takes joined end to end, each cleaned and levelled alike; the stretches of
    speech; and which silences are the anchors between the script's parts."""
    import mossad_audio as MA
    pieces, runs, anchors, t0 = [], [], [], 0.0
    for k, (name, a_, b_, n_anch) in enumerate(AUDIO_PARTS):
        v = MA.line(name)
        v = v[int(a_ * MA.SR):(int(b_ * MA.SR) if b_ else None)]
        r = [(x, y) for x, y in MA.pauses(v, 0.12) if y - x > 0.05]
        lead = LEAD if k == 0 else JOIN_GAP
        cut = max(0.0, r[0][0] - (lead if k == 0 else 0.15))
        v = v[int(cut * MA.SR):int((r[-1][1] + 0.3) * MA.SR)]
        if k > 0:
            pieces.append(np.zeros(int((JOIN_GAP - 0.15) * MA.SR)))
            t0 += JOIN_GAP - 0.15
            anchors.append(len(runs) - 1)                       # the join is an anchor
        base = len(runs)
        rr = [(x - cut + t0, y - cut + t0) for x, y in r]
        gaps = sorted(range(len(rr) - 1), key=lambda i: rr[i + 1][0] - rr[i][1], reverse=True)[:n_anch]
        anchors += [base + g for g in gaps]
        runs += rr
        pieces.append(v)
        t0 += len(v) / MA.SR
    return MA, np.concatenate(pieces), runs, sorted(anchors)


def _syllable_beats(v, runs):
    """The moments each syllable peaks in the voice (loudness of the speech band), inside the stretches of speech."""
    from scipy.signal import butter, find_peaks, sosfilt
    import mossad_audio as MA
    x = sosfilt(butter(2, [300, 2500], 'band', fs=MA.SR, output='sos'), v)
    hop = MA.SR // 200
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    e = np.convolve(e, np.hanning(9) / np.hanning(9).sum(), 'same')
    pk, _ = find_peaks(e, distance=18, prominence=e.max() * 0.06)
    ts = pk / 200.0
    return [t for t in ts if any(a_ - 0.02 <= t <= b_ + 0.02 for a_, b_ in runs)]


START_WORD = 'I look forward'
CUT_AT = 18.02                   # the film's sound starts here in the full take: in the 40 ms gap between 'and' and 'I'
                                 # (Sam, 15 Oct: keep the 'I', never a scrap of the word before it); silence is laid before it   # the film opens on these words (None: from the very start)
PINS = {'I look forward': 18.04, 'helicopters,': 38.95, "I'll get back to": 50.39, 'I just need.': 63.29}   # an exact phrase -> where it starts, in the full take
FRESH = set()            # word indices whose subtitle starts fresh and exactly on the word (punchlines)


def build_timeline():
    """Words timed to the recording; her acting (glances, smiles, the sigh) placed by the tags."""
    MA, v, runs, cuts = _voice()
    parts_text = [x.strip() for x in SCRIPT.split('||')]
    assert len(cuts) == len(parts_text) - 1, (len(cuts), len(parts_text))
    groups, prev = [], 0
    for c in cuts + [len(runs) - 1]:
        groups.append(runs[prev:c + 1])
        prev = c + 1
    words, events = [], []                     # words: (start, end, text); events: (word index, tag)
    nuclei = _syllable_beats(v, runs)
    part_ranges = []
    global FRESH
    fresh = FRESH
    for text, grp in zip(parts_text, groups):
        toks = text.split()
        for i_, w_ in enumerate(toks):                 # '^word': its subtitle starts fresh, exactly on the word
            if w_.startswith('^'):
                fresh.add(len(words) + sum(1 for x in toks[:i_] if not x.startswith('[')))
                toks[i_] = w_[1:]
        plain = [w for w in toks if not w.startswith('[')]
        sy = [syllables(w) for w in plain]
        S = sum(sy)
        nuc = [x for x in nuclei if grp[0][0] - 0.05 <= x <= grp[-1][1] + 0.05]
        if len(nuc) < 2:
            nuc = [grp[0][0], grp[-1][1]]
        N = len(nuc)

        def T(f):                              # a (fractional) syllable beat -> its time in the recording
            f = min(max(f, 0.0), N - 1.0)
            i = int(f)
            return nuc[i] if i >= N - 1 else nuc[i] + (nuc[i + 1] - nuc[i]) * (f - i)
        # each script syllable is matched to the recording's syllable beats in order (Sam, 15 Oct: the
        # subtitles ran ahead); the beat counter misses about 1 in 6, so the matching is by proportion
        done, pending, start_idx = 0, [], len(words)
        for w in toks:
            if w.startswith('['):
                pending.append(w.strip('[]'))
                continue
            for tag in pending:
                events.append((len(words), tag))
            pending = []
            k = len(words) - start_idx
            i0, i1 = done * N / S, (done + sy[k]) * N / S
            words.append([T(i0) - 0.12, T(max(i0, i1 - 1.0)) + 0.16, w])
            done += sy[k]
        for tag in pending:
            events.append((len(words), tag))
        # a comma or full stop sits on the nearest real pause, if there is one close by
        part = words[start_idx:]
        pauses = [(grp[j][1], grp[j + 1][0]) for j in range(len(grp) - 1)]
        taken = set()
        for k in range(len(part) - 1):
            if part[k][2][-1] not in ',.':
                continue
            e = part[k][1]
            best = min((j for j in range(len(pauses)) if j not in taken), key=lambda j: abs(pauses[j][0] - e),
                       default=None)
            if best is not None and abs(pauses[best][0] - e) < 0.7:
                taken.add(best)
                part[k][1] = pauses[best][0] + 0.05
                part[k + 1][0] = pauses[best][1] - 0.05
        for k in range(len(part)):                       # keep every word inside its part, in order
            part[k][0] = max(part[k][0], grp[0][0] - 0.05, part[k - 1][1] - 0.02 if k else -1)
            part[k][1] = max(part[k][1], part[k][0] + 0.12)
        part_ranges.append((start_idx, len(words)))
    for (k0, k1) in part_ranges:                         # Sam's pins: a word starts exactly where he heard it
        pts = [(words[k0][0], words[k0][0])]
        for phrase, at_ in PINS.items():
            n_ = len(phrase.split())
            for k in range(k0, k1 - n_ + 1):
                if [w[2] for w in words[k:k + n_]] == phrase.split():
                    pts.append((words[k][0], at_))
        pts.append((words[k1 - 1][1], words[k1 - 1][1]))
        pts.sort()
        if len(pts) > 2:
            xs, ys = [p_[0] for p_ in pts], [p_[1] for p_ in pts]
            for k in range(k0, k1):
                words[k][0] = float(np.interp(words[k][0], xs, ys))
                words[k][1] = max(float(np.interp(words[k][1], xs, ys)), words[k][0] + 0.12)
    words = [tuple(w) for w in words]
    end = words[-1][1] + TAIL
    gaze, smiles, sigh, exprs = [(0.0, 'up')], [], (1e9, 1e9), []
    for wi, tag in events:
        before = words[wi - 1][1] if wi > 0 else 0.0
        after = words[wi][0] if wi < len(words) else end
        if tag in ('down', 'up'):
            gaze.append((max(before, after - 0.35) if wi > 0 else 0.0, tag))
        elif tag == 'double':
            g0 = max(before, after - 0.75)
            gaze += [(g0, 'up'), (g0 + 0.32, 'down')]
        elif tag.startswith('smile'):
            smiles.append((before + 0.05, max(after - 0.05, before + 0.45), int(tag[-1])))   # fills the pause, never talks over a line for long
            gaze.append((before + 0.05, 'up'))
        elif tag == 'sigh':
            sigh = (before + 0.25, after - 0.1)
        elif tag == 'dead':                                    # the last line: dead-eyed, straight down the lens
            exprs.append((words[wi][0] - 0.85, end + 1.0, 'dead'))
            gaze.append((words[wi][0] - 0.5, 'up'))
        elif tag == 'excited':                                 # through the phrase, to its comma: eyes wide, big
            j = wi                                             # talking smile, a little bounce (Sam, 15 Oct)
            while j < len(words) - 1 and words[j][2][-1] not in ',.':
                j += 1
            e1 = words[j][1] + 0.1
            exprs.append((words[wi][0] - 0.1, e1, 'excited'))
            smiles.append((words[wi][0] - 0.1, e1, 2))
            gaze.append((words[wi][0] - 0.15, 'up'))
        elif tag in ('onsmile2', 'onsmile3', 'delight', 'wide', 'awkward'):
            w0, w1 = words[wi][0], words[wi][1]
            nxt = words[wi + 1][0] if wi + 1 < len(words) else end
            gaze.append((w0 - 0.1, 'up'))
            if tag == 'wide':                                  # eyes slightly wide on the word
                exprs.append((w0 - 0.45, w1 + 0.3, 'wide'))   # kicks in just before the word (Sam, 15 Oct)
            elif tag == 'awkward':                             # through the sentence and the pause after it
                j = wi
                while j < len(words) - 1 and words[j][2][-1] != '.':
                    j += 1
                nx = words[j + 1][0] if j + 1 < len(words) else end
                exprs.append((w0 - 0.1, min(nx - 0.05, words[j][1] + 1.6), 'awkward'))
            else:                                              # a smile DURING the word, held into the pause
                b1 = max(w1 + 0.45, min(nxt - 0.05, w1 + 1.2))
                smiles.append((w0 - 0.08, b1, 2 if tag == 'delight' else int(tag[-1])))
                if tag == 'delight':
                    exprs.append((w0 - 0.08, b1, 'delight'))
    gaze.sort()
    return words, gaze, smiles, sigh, end, v, runs, exprs


TALK, GAZE, SMILES, SIGH, END, VOICE, RUNS, EXPRS = build_timeline()


def _trim(start_word):
    """Start the film at a later word (Sam, 15 Oct: 'starts with I look forward to the President'): everything
    before it is cut, everything after slides earlier, her pose carries over."""
    global TALK, GAZE, SMILES, SIGH, END, VOICE, RUNS, EXPRS, FRESH
    import mossad_audio as MA
    k = next(i for i in range(len(TALK) - 3) if [w for _, _, w in TALK[i:i + 3]] == start_word.split()[:3])
    t0 = CUT_AT - LEAD                           # the cut sits in the silence just before the first word
    TALK = [(a - t0, b - t0, w) for a, b, w in TALK[k:]]
    g0 = [g for t_, g in GAZE if t_ <= t0][-1:] or ['up']
    GAZE = [(0.0, g0[0])] + [(t_ - t0, g) for t_, g in GAZE if t_ > t0]
    SMILES = [(a - t0, b - t0, l) for a, b, l in SMILES if b > t0]
    EXPRS = [(a - t0, b - t0, x) for a, b, x in EXPRS if b > t0]
    SIGH = (SIGH[0] - t0, SIGH[1] - t0)
    END -= t0
    rest = VOICE[int(CUT_AT * MA.SR):].copy()
    nf = int(0.01 * MA.SR)
    rest[:nf] *= np.linspace(0, 1, nf)          # a 10 ms fade-in at the cut, inside the silence (no click)
    VOICE = np.concatenate([np.zeros(int(LEAD * MA.SR)), rest])
    RUNS = [(max(a, CUT_AT) - t0, b - t0) for a, b in RUNS if b > CUT_AT]
    FRESH = {i - k for i in FRESH if i >= k}


if START_WORD:
    _trim(START_WORD)
DUR = round(END + 0.25, 2)
BLACK_AT = END
SHOTS = [('push', 0.0, DUR)]            # one continuous shot (the pre-flight reads this)
BLINKS = F.blinks(17, 0.4, END, talking=True)


def _envelope():
    """How loud her voice is on each picture (for the mouth): 0 silent .. 1 her loudest."""
    import mossad_audio as MA
    hop = MA.SR // FPS
    n = len(VOICE) // hop + 1
    e = np.array([np.sqrt(np.mean(VOICE[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(VOICE) else 0.0 for i in range(n)])
    return e / (np.percentile(e[e > 0], 97) + 1e-9)


ENV = _envelope()


# ------------------------------------------------------------------------------------------------ the camera
# One slow push-in: the zoom grows at a steady rate (log-linear, so it never seems to speed up), easing in at the
# start. Depth: each layer sits f closer to the camera than her (negative = behind her), so the reporters in front
# swell and slide away under the lens while the back wall barely moves.
Z0, Z1 = 0.5, 3.3
A0, A1 = (560.0, 1400.0), (540.0, 880.0)       # the point the camera looks at: the room, then her face
D0 = Z1 / Z0                                    # her distance at the start (1 at the end)
PUSH_END = END - 0.9                            # arrives on the close-up just before "Venezuela"


def push(t):
    u = max(0.0, min(1.0, t / PUSH_END))
    u = u * u * (3 - 2 * u) * 0.35 + u * 0.65   # a gentle ease in and out over a steady glide
    return u


def cam_at(t, f=0.0):
    u = push(t)
    z = Z0 * (Z1 / Z0) ** (u ** 1.25)               # stays wide a little longer, then closes in
    d = D0 * Z0 / z
    if f:
        if d - f <= 0.08:
            return None
        z *= (d / (d - f)) / (D0 / (D0 - f))
    ax = A0[0] + (A1[0] - A0[0]) * u
    ay = A0[1] + (A1[1] - A0[1]) * (u ** 0.9)
    return B.Cam(z, ax, ay)


# ------------------------------------------------------------------------------------------------ her look
NECK = (540.0, 1000.0)               # her neck base in the world; podium top is 280 below it
SKIN = (236, 190, 160)
SKIN_D = (214, 160, 130)
HAIR = (226, 186, 118)
HAIR_D = (184, 138, 76)
HAIR_L = (246, 220, 162)
BROW = (138, 98, 60)
LIP = (204, 128, 124)
LIP_D = (166, 86, 88)
NAVYJ = (30, 38, 66)
NAVYJ_D = (20, 26, 46)
BLOUSE = (248, 246, 240)
BLOUSE_D = (214, 210, 204)
GOLDB = (222, 176, 72)
IRIS = (96, 120, 112)
PODIUM_TOP = 280


def gaze_at(t):
    g = 'up'
    for gt, gv in GAZE:
        if gt <= t:
            g = gv
    return g


def state(t):
    """Everything about her at time t: where she looks, lids, brows, mouth, head and shoulders."""
    s = dict(gaze=gaze_at(t), lid=0.0, brow=0.0, mouth='rest', smile=0, head_dy=0.0, head_tilt=0.0, sh_dy=0.0,
             closed=False, look_x=0.0, squint=0.0)
    i = int(round(t * FPS))
    lv = ENV[i] if i < len(ENV) else 0.0
    if lv > 0.08:                                         # the mouth follows the loudness of her voice
        s['mouth'] = 'small' if lv < 0.3 else ('mid' if lv < 0.62 else ['open', 'mid'][i % 2])
    for a, b, level in SMILES:
        on = smooth((t - a) / 0.12)                        # the smile switches ON almost at once
        off = 1.0 - smooth((t - (b - 0.1)) / 0.1)          # and OFF, just as suddenly (that is the strangeness)
        if on * off > 0.5:
            # talking: she keeps speaking THROUGH the smile (the jaw opens with her voice); the moment she stops,
            # it flashes into the crazed one (Sam, 15 Oct)
            level = 2 if lv > 0.08 else 3
            s['smile_open'] = 0.0 if lv <= 0.08 else min(1.0, lv)
            s['smile'] = level
            s['brow'] = 5 + 3 * level
            s['squint'] = 0.2 * level
            s['head_tilt'] = 0.04 * (1 if level == 3 else -1) * smooth((t - a) / max(0.2, (b - a) / 4))
            s['gaze'] = 'up'
    if s['gaze'] == 'up':                                  # looking round the journalists while she talks: the eyes
        rnd = random.Random(31)                            # jump to a new face and hold, the head follows a little
        tt, k = 0.0, 0
        spots = [-0.48, -0.22, 0.05, 0.28, 0.5, -0.1, 0.4, -0.35]   # half as wide, half as often (Sam, 15 Oct)
        while tt <= t:
            tt += rnd.uniform(1.4, 3.2)
            k += 1
        s['look_x'] = spots[(k * 3) % len(spots)]
        s['look_dy'] = 2.0                                 # the press sit below her
    if s['gaze'] == 'down' and s['smile'] == 0:            # head right down, eyes on the paper (note 13)
        s['lid'] = 0.86
        s['head_dy'] = 24.0
        s['feat_dy'] = 9.0
        s['brow'] = -3.0
    for a, b, kind in EXPRS:
        if a <= t < b:
            if kind == 'wide':                                 # eyes slightly wide, brows up
                s['wide'] = 1.0
                s['lid'] = 0.0
                s['brow'] = max(s['brow'], 8.0)
            elif kind == 'delight':                            # delighted: brows high, eyes crinkled, head tipped
                s['brow'] = 14.0
                s['squint'] = 0.5
                s['head_tilt'] = -0.06
            elif kind == 'excited':                            # excited: wide eyes, brows high, a bounce
                s['wide'] = 1.0
                s['lid'] = 0.0
                s['squint'] = 0.0
                s['brow'] = 16.0
                s['head_dy'] = -7.0 * abs(math.sin((t - a) * 7.0))
                s['sh_dy'] = -4.0 * abs(math.sin((t - a) * 7.0))
            elif kind == 'awkward':                            # sheepish, looking dead at the crowd (Sam, 15 Oct):
                s['wince'] = 1.0                               # 'yeaaah... sorry' (Sam, 15 Oct): a wince, never happy
                s['worry'] = 1.6                               # worried brows, chin dipped, a tight grimace, and
                s['brow'] = 2.0                                # more uncomfortable (Sam, 15 Oct): a bead of sweat,
                s['look_x'] = 0.0                              # a nervous flick of the eyes down and back, a swallow
                s['look_dy'] = 2.5
                s['gaze'] = 'up'
                s['lid'] = 0.22
                s['head_dy'] = 7.0
                s['head_tilt'] = 0.1                           # the apologetic head tilt
                s['squint'] = 0.25                             # wincing
                if s['mouth'] == 'open':                        # talking small and tight, never a big open mouth
                    s['mouth'] = 'mid'
                if s['mouth'] == 'grimace':
                    s['mouth'] = 'eek'
                u = t - a
                if 1.9 < u < 2.25 or 3.4 < u < 3.7:            # eyes flick down to the notes and straight back
                    s['look_dy'] = 6.0
                    s['lid'] = 0.5
                if 2.8 < u < 3.1:                              # a swallow: the chin dips and comes back
                    s['head_dy'] = 11.0
                if s['mouth'] == 'rest' and s['smile'] == 0:
                    s['mouth'] = 'eek'                         # the 'yeaaah... sorry' wince in the pause
    a, b = SIGH
    if a <= t < b:
        u = (t - a) / (b - a)
        rise = smooth(u / 0.45) - smooth((u - 0.5) / 0.4) * 1.25
        s['sh_dy'] = -16.0 * rise
        s['head_dy'] = 24.0 - 12 * rise
        s['feat_dy'] = 9.0 * (1 - max(0.0, rise))
        s['closed'] = 0.25 < u < 0.8
        s['mouth'] = 'blow' if 0.5 < u < 0.92 else 'rest'
        s['brow'] = 3.0 * rise
    if t >= b:                                            # after the sigh: heavier lids, flatter, deader
        s['lid'] = max(s['lid'], 0.7)
        s['brow'] = -3.0
    dead = any(a_ <= t < b_ and k_ == 'dead' for a_, b_, k_ in EXPRS)
    if dead:                                              # dead-eyed and despondent, staring straight into the camera
        a_dead = next(a_ for a_, b_, k_ in EXPRS if k_ == 'dead')
        u = smooth((t - a_dead) / 0.7)                    # the head lifts into it over 0.7 s, eased like the sigh
        base = dict(lid=0.86, worry=0.0, brow=-3.0, head_dy=24.0, feat_dy=9.0, look_dy=5.0, look_x=0.0)   # her reading pose
        target = dict(lid=0.42, worry=0.55, brow=-2.0, head_dy=5.0, feat_dy=0.0, look_dy=0.0, look_x=0.0)
        for key in target:
            s[key] = base[key] + (target[key] - base[key]) * u
        s.update(gaze='up', smile=0, squint=0.0)
        if s['mouth'] == 'rest':
            s['mouth'] = 'rest'
    keyface = any(a_ - 0.3 <= t < b_ + 0.2 for a_, b_, k_ in EXPRS)   # no blink may land on a key face (Sam, 15 Oct)
    if any(bt <= t < bt + 0.14 for bt in BLINKS) and s['smile'] == 0 and not dead and not keyface:
        s['closed'] = True
    if dead:                                              # utterly still: no shifts, no turn
        s['head_dx'] = 0.0
        return s
    s['head_tilt'] += filmkit.shifts(t, seed=4, amount=0.025)
    s['head_dx'] = 40 * filmkit.shifts(t, seed=9, amount=0.06) + 6 * s['look_x'] * (s['gaze'] == 'up')
    return s


# ------------------------------------------------------------------------------------------------ drawing her
def head_shape(hx, hy, hw, hh):
    """A slim oval face: wide at the cheekbones, tapering to a narrow, slightly pointed chin."""
    top = oval(hx, hy - 4, hw, hh * 0.98, 24, math.pi, 2 * math.pi)
    return top + [(hx + hw, hy + 8), (hx + hw * 0.96, hy + hh * 0.46), (hx + hw * 0.7, hy + hh * 0.86),
                  (hx + hw * 0.32, hy + hh * 1.1), (hx, hy + hh * 1.16), (hx - hw * 0.32, hy + hh * 1.1),
                  (hx - hw * 0.7, hy + hh * 0.86), (hx - hw * 0.96, hy + hh * 0.46), (hx - hw, hy + 8)]


def wave_edge(x_of, y0, y1, n, amp, phase=0.0):
    """Points down a wavy edge: x_of(u) the base line, plus a soft S-wave (the blow-dried waves)."""
    return [(x_of(k / n) + amp * math.sin(phase + k / n * math.pi * 3.2), y0 + (y1 - y0) * k / n) for k in range(n + 1)]


def hair_mass(p, hx, hy, hw, hh, shrug):
    """The back of the hair, seen only in the gap behind her neck: kept inside the front locks' outline so no
    second edge ever shows round them (Sam, 15 Oct: 'a second haircut hiding just behind')."""
    pts = [(hx - hw - 4, hy - hh * 0.3), (hx + hw + 4, hy - hh * 0.3), (hx + hw + 4, hy + 290 + shrug),
           (hx - hw - 4, hy + 290 + shrug)]
    p.poly(pts, HAIR_D, None)


def _locks(hx, hy, hw, hh, sh_dy):
    """The two long waves falling in front of the shoulders, as outlines (starting up inside the crown, so they
    join it with no seam)."""
    out = []
    for sgn in (-1, 1):
        outer = wave_edge(lambda u: hx + sgn * (hw + 24 + 28 * math.sin(u * math.pi * 0.9)), hy - hh * 0.55,
                          hy + 300 + sh_dy, 12, 10 * sgn, 0.0)
        inner = wave_edge(lambda u: hx + sgn * (hw * 0.86 - 4 * u + 6 * math.sin(u * math.pi)), hy + 20,
                          hy + 290 + sh_dy, 10, 7 * sgn, 0.9)
        tip = (hx + sgn * (hw + 18), hy + 330 + sh_dy)
        out.append(curve([(hx + sgn * hw * 0.6, hy - hh * 0.7)] + inner + [tip] + outer[::-1], 3))
    return out


def _crown(hx, hy, hw, hh, fx):
    """The crown: full and rounded, its lower edge the hairline across the forehead (side parting, our left)."""
    part = fx - hw * 0.25
    outer = oval(hx, hy - 8, hw + 24, hh + 28, 20, math.pi * 0.97, math.pi * 2.03)
    line = [(hx + hw + 18, hy + 30), (hx + hw * 0.92, hy - hh * 0.3), (hx + hw * 0.62, hy - hh * 0.7),
            (part + hw * 0.25, hy - hh * 0.86), (part, hy - hh * 0.98), (part - hw * 0.2, hy - hh * 0.84),
            (hx - hw * 0.7, hy - hh * 0.62), (hx - hw * 0.94, hy - hh * 0.2), (hx - hw - 18, hy + 30)]
    return curve(outer + line, 3), curve(line, 3)[7:-7], part


def hair_front(p, hx, hy, hw, hh, sh_dy):
    """Locks and crown as ONE shape with ONE outline: every piece outlined first, then every fill laid on top,
    so the seams between pieces vanish. Drawn before the face; the hairline goes over the face after."""
    pieces = _locks(hx, hy, hw, hh, sh_dy) + [_crown(hx, hy, hw, hh, hx)[0]]
    for pts in pieces:
        p.poly(pts, HAIR, INK, 5.2)
    for pts in pieces:
        p.poly(pts, HAIR, None)
    for sgn in (-1, 1):                                   # two soft strands inside each lock, never past its edge
        for k in range(2):
            line = wave_edge(lambda u: hx + sgn * (hw + 20 + 10 * k + 22 * math.sin(u * math.pi * 0.9)),
                             hy + 40 + 30 * k, hy + 250 - 30 * k + sh_dy, 8, 7 * sgn, 0.3)
            p.line(line, HAIR_D, 1.6)


def hair_top(p, hx, hy, hw, hh, fx):
    """The crown again, over the face: fill, the hairline, the parting and a few combed strands."""
    shape, line, part = _crown(hx, hy, hw, hh, fx)
    p.poly(shape, HAIR, None)
    p.line(line, INK, 2.6)
    p.line([(part, hy - hh * 1.2), (part + 3, hy - hh * 0.98)], HAIR_D, 2.0)
    for k in range(2):
        p.line(curve([(part + 14 + 16 * k, hy - hh * 1.14 + 8 * k), (hx + hw * 0.7 + 6 * k, hy - hh * 0.88 + 12 * k),
                      (hx + hw + 4, hy - hh * 0.3 + 10 * k)], 3)[:-3], HAIR_D, 1.6)
        p.line(curve([(part - 12 - 12 * k, hy - hh * 1.12 + 8 * k), (hx - hw * 0.7 - 6 * k, hy - hh * 0.84 + 12 * k),
                      (hx - hw - 4, hy - hh * 0.3 + 10 * k)], 3)[:-3], HAIR_D, 1.6)


def _clip_convex(subject, window):
    """The part of a shape inside a convex window (Sutherland-Hodgman): the iris kept inside the eye."""
    def inside(p_, a_, b_):
        return (b_[0] - a_[0]) * (p_[1] - a_[1]) - (b_[1] - a_[1]) * (p_[0] - a_[0]) >= 0

    def cross(p1, p2, a_, b_):
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
        x3, y3, x4, y4 = a_[0], a_[1], b_[0], b_[1]
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(d) < 1e-9:
            return p2
        u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        return (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    out = list(subject)
    for i in range(len(window)):
        a_, b_ = window[i], window[(i + 1) % len(window)]
        inp, out = out, []
        if not inp:
            break
        s_ = inp[-1]
        for e_ in inp:
            if inside(e_, a_, b_):
                if not inside(s_, a_, b_):
                    out.append(cross(s_, e_, a_, b_))
                out.append(e_)
            elif inside(s_, a_, b_):
                out.append(cross(s_, e_, a_, b_))
            s_ = e_
    return out


def eye(p, ex, ey, sgn, st):
    """A large almond eye: heavy liner along the upper lid, lashes flicked out at the corner, a hazel iris. The eye
    is ONE opening between the two lids; the iris is cut to it, so no line ever crosses the white (Sam, 15 Oct)."""
    lid, squint = st['lid'], st['squint']
    w, h = 21, 10 + 3.5 * st.get('wide', 0.0)             # slightly wide: more white above and below the iris
    us = np.linspace(-1, 1, 15)
    if st['closed']:
        p.line([(ex + w * u, ey + 1 + 5 * (1 - u * u)) for u in us], INK, 3.4)
        for k in range(3):
            lx = ex + sgn * (8 + 6 * k)
            p.line([(lx, ey + 5), (lx + sgn * 5, ey + 12)], INK, 1.8)
        return
    low = (h + 1.5 * st.get('wide', 0.0)) * (1 - squint)  # a big smile pushes the lower lid up
    upper_open = [(ex + w * u, ey - h * (1 - u * u)) for u in us]
    upper = [(ex + w * u, ey - h * (1 - u * u) * (1 - lid * 1.08)) for u in us]
    lower = [(ex + w * u, ey + low * (1 - u * u) - 0.8 * h * squint * (1 - u * u) * 0.0) for u in us]
    opening = upper + lower[::-1][1:-1]
    p.poly(opening, (252, 252, 250), None)
    dx = st['look_x'] * 7
    dy = 5 if st['gaze'] == 'down' else st.get('look_dy', 0.0)
    cx, cy = ex + dx, ey + dy
    circ = lambda r: [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
    iris = _clip_convex(opening[::-1], circ(9))
    if len(iris) >= 3:
        p.poly(iris, IRIS, None)
    pupil = _clip_convex(opening[::-1], circ(4.2))
    if len(pupil) >= 3:
        p.poly(pupil, INK, None)
    hl = (cx + 3, cy - 3)
    if lid < 0.4 and squint < 0.5:
        p.ell(hl[0], hl[1], 1.8, 1.8, (255, 255, 255), None)
    if lid > 0:                                           # the lowered lid, made up, above the lid's edge
        p.poly(upper_open + upper[::-1], (214, 174, 160), None)
    p.line(lower, INK, 1.6)                               # the lower lid, corner to corner
    p.line(upper, INK, 3.4)                               # the liner, along the upper lid's edge, corner to corner
    tip = upper[-1] if sgn > 0 else upper[0]
    p.line([tip, (tip[0] + sgn * 8, tip[1] - 6)], INK, 2.6)        # the winged flick
    for k in range(3):                                    # lashes at the outer corner, from the lid's edge
        x0, y0 = upper[7 + sgn * (3 + k)]
        p.line([(x0, y0), (x0 + sgn * 4, y0 - 6 - k + (9 if lid > 0.3 else 0))], INK, 1.6)
    crease = [(ex + w * 0.7 * u, ey - h - 7 - 3 * (1 - u * u)) for u in np.linspace(-1, 1, 7)]
    p.line(crease, (198, 156, 140), 1.4)                  # the crease, made up


def mouth(p, fx, my, st):
    m, sm = st['mouth'], st['smile']
    if sm >= 2:                                           # the big strange smile: wide, all top teeth (3: both rows)
        w = 36 if sm == 2 else 42
        up = 9 if sm == 2 else 12
        drop = 16 if sm == 2 else 21
        drop += 12 * st.get('smile_open', 0.0)            # talking through it: the jaw drops with her voice
        w -= 4 * st.get('smile_open', 0.0)
        outer = curve([(fx - w, my - up), (fx - w * 0.5, my - 4), (fx, my - 3), (fx + w * 0.5, my - 4), (fx + w, my - up),
                       (fx + w * 0.62, my + drop * 0.7), (fx, my + drop), (fx - w * 0.62, my + drop * 0.7)], 4)
        p.poly(outer, LIP, INK, 2.2)
        inner = curve([(fx - w + 7, my - up + 3), (fx, my + 1), (fx + w - 7, my - up + 3), (fx + w * 0.5, my + drop * 0.6),
                       (fx, my + drop - 6), (fx - w * 0.5, my + drop * 0.6)], 4)
        p.poly(inner, (96, 34, 42), None)
        teeth = [(fx - w + 8, my - up + 3), (fx - w * 0.5, my + 1), (fx, my + 2), (fx + w * 0.5, my + 1),
                 (fx + w - 8, my - up + 3), (fx + w * 0.55, my + 10), (fx, my + 12), (fx - w * 0.55, my + 10)]
        p.poly(curve(teeth, 3), (255, 255, 252), None)
        if sm == 3:
            p.poly(curve([(fx - w * 0.5, my + drop * 0.62), (fx, my + drop - 10), (fx + w * 0.5, my + drop * 0.62),
                          (fx, my + drop - 3)], 3), (250, 250, 246), None)
        for k in range(-3, 4):                            # the gaps between teeth, faint
            p.line([(fx + k * w * 0.22, my + 1 + abs(k)), (fx + k * w * 0.22, my + 10 - abs(k))], (226, 222, 216), 1.0)
        p.poly(outer, None, INK, 2.2)
        for sgn in (-1, 1):                               # cheeks bunched up by it
            p.line([(fx + sgn * (w + 4), my - up - 12), (fx + sgn * (w + 10), my - up), (fx + sgn * (w + 4), my - up + 10)],
                   SKIN_D, 1.8)
        return
    if m == 'eek':                                        # 'yeaaah... sorry': lips pulled wide and flat over clenched teeth
        outer = [(fx - 30, my + 5), (fx - 14, my - 3), (fx + 14, my - 3), (fx + 30, my + 5), (fx + 16, my + 13),
                 (fx - 16, my + 13)]
        p.poly(curve(outer, 3), LIP, INK, 1.8)
        teeth = [(fx - 24, my + 3), (fx - 12, my), (fx + 12, my), (fx + 24, my + 3), (fx + 14, my + 9), (fx - 14, my + 9)]
        p.poly(curve(teeth, 2), (252, 252, 248), None)
        p.line([(fx - 24, my + 5), (fx, my + 4.5), (fx + 24, my + 5)], (200, 196, 190), 1.2)
        for k in range(-2, 3):
            p.line([(fx + k * 8, my + 1), (fx + k * 8, my + 8)], (214, 210, 204), 1.0)
        p.poly(curve(outer, 3), None, INK, 1.8)
        for sgn in (-1, 1):
            p.line([(fx + sgn * 30, my + 5), (fx + sgn * 35, my + 10)], SKIN_D, 1.6)
        return
    if m == 'grimace':                                    # slightly awkward: lips pressed tight, wide, one corner up
        top = [(fx - 28, my + 4), (fx - 10, my - 1), (fx + 10, my - 1), (fx + 28, my + 1)]
        bot = [(fx + 28, my + 1), (fx + 12, my + 6), (fx - 12, my + 7), (fx - 28, my + 4)]
        p.poly(curve(top + bot, 3), LIP, INK, 1.8)
        p.line([(fx - 28, my + 4), (fx, my + 2), (fx + 28, my + 1)], INK, 2.2)
        p.line([(fx + 28, my + 1), (fx + 32, my + 5)], SKIN_D, 1.6)
        p.line([(fx - 28, my + 4), (fx - 32, my + 8)], SKIN_D, 1.6)
        return
    if m == 'blow':                                       # the sigh: a small rounded breath out
        p.poly(curve(oval(fx, my + 4, 11, 9, 12)), LIP, INK, 2.0)
        p.ell(fx, my + 4, 5, 4, (96, 34, 42), None)
        return
    if m in ('small', 'mid', 'open'):
        h = {'small': 7, 'mid': 13, 'open': 19}[m]
        w = {'small': 20, 'mid': 22, 'open': 19}[m]
        outer = curve([(fx - w - 3, my), (fx - 8, my - 6), (fx, my - 4), (fx + 8, my - 6), (fx + w + 3, my),
                       (fx + w * 0.6, my + h + 6), (fx, my + h + 8), (fx - w * 0.6, my + h + 6)], 4)
        p.poly(outer, LIP, INK, 2.0)
        p.poly(curve([(fx - w + 2, my), (fx, my - 1), (fx + w - 2, my), (fx + w * 0.5, my + h), (fx, my + h + 1),
                      (fx - w * 0.5, my + h)], 3), (96, 34, 42), None)
        if m != 'small':
            p.poly([(fx - w * 0.7, my), (fx + w * 0.7, my), (fx + w * 0.55, my + 5), (fx - w * 0.55, my + 5)],
                   (255, 255, 252), None)
        p.poly(outer, None, INK, 2.0)
        return
    # resting: full lips, closed (sm == 1: a small closed smile)
    c = 6 if sm == 1 else 0
    top = curve([(fx - 25, my + 1 - c), (fx - 10, my - 8), (fx, my - 5), (fx + 10, my - 8), (fx + 25, my + 1 - c),
                 (fx, my + 2)], 3)
    bot = curve([(fx - 25, my + 1 - c), (fx, my + 2), (fx + 25, my + 1 - c), (fx + 12, my + 13), (fx, my + 15),
                 (fx - 12, my + 13)], 3)
    p.poly(top, LIP_D, INK, 1.8)
    p.poly(bot, LIP, INK, 1.8)
    p.line([(fx - 25, my + 1 - c), (fx - 10, my + 3), (fx + 10, my + 3), (fx + 25, my + 1 - c)], INK, 2.0)


def face(p, hx, hy, hw, hh, st):
    fx = hx
    hy = hy + st.get('feat_dy', 0.0)                       # looking down: the features drop, more forehead shows
    brow = st['brow']
    for sgn in (-1, 1):                                   # arched, filled-in brows, darker than the hair
        ex = fx + sgn * 29
        by = hy - 30 - brow
        wy = 7 * st.get('worry', 0.0)                       # worried: inner ends lifted, outer ends dropped
        p.poly([(ex - sgn * 18, by + 6 - wy), (ex - sgn * 4, by - 3 - wy * 0.6), (ex + sgn * 10, by - 7), (ex + sgn * 24, by + 2 + wy * 0.5),
                (ex + sgn * 10, by - 2), (ex - sgn * 4, by + 2 - wy * 0.6)], BROW, BROW, 1.6)
    for sgn in (-1, 1):
        eye(p, fx + sgn * 29, hy - 6 + st.get('eye_dy', 0), sgn, st)
    p.line([(fx - 3, hy - 4), (fx - 6, hy + 26), (fx - 2, hy + 33), (fx + 7, hy + 31)], INK, 1.8)   # a slim nose
    p.line([(fx - 11, hy + 30), (fx - 7, hy + 33)], INK, 1.4)
    for sgn in (-1, 1):                                   # cheekbones: a flat blush, high
        p.ell(fx + sgn * 38, hy + 22, 12, 6, (240, 176, 156), None, rot=-sgn * 0.3)
    mouth(p, fx, hy + 56, st)


def torso(p, sh_dy):
    """Navy double-breasted blazer with gold buttons; a white tie-neck blouse with a keyhole."""
    sw = 150
    body = [(-40, -4), (-sw * 0.82, 10 + sh_dy), (-sw - 6, 44 + sh_dy), (-sw - 2, 200), (-sw + 4, 460), (sw - 4, 460),
            (sw + 2, 200), (sw + 6, 44 + sh_dy), (sw * 0.82, 10 + sh_dy), (40, -4)]
    p.poly(rough(body, 3, 11), NAVYJ, INK, 2.6)
    p.poly([(-30, -78), (30, -78), (34, 8), (-34, 8)], SKIN, INK, 2.4)                       # neck
    # the blouse in the V, the tie at the neck, the keyhole under it
    p.poly([(-46, -6), (46, -6), (24, 170), (0, 200), (-24, 170)], BLOUSE, INK, 2.2)
    p.poly(curve([(-36, -30), (0, -22), (36, -30), (38, 0), (0, 8), (-38, 0)], 3), BLOUSE, INK, 2.0)  # the collar band
    p.poly(curve([(-8, 66), (0, 20), (8, 66), (0, 84)], 3), SKIN, INK, 1.8)                 # the keyhole
    p.poly(curve([(-22, 4), (0, -6), (22, 4), (12, 22), (0, 26), (-12, 22)], 3), BLOUSE, INK, 2.0)   # the knot
    for sgn in (-1, 1):                                   # the tie's short tails, draped
        p.poly(curve([(sgn * 6, 20), (sgn * 26, 26), (sgn * 34, 70), (sgn * 22, 96), (sgn * 12, 60)], 3), BLOUSE, INK, 1.8)
        p.line([(sgn * 14, 30), (sgn * 24, 80)], BLOUSE_D, 1.4)
    for sgn in (-1, 1):                                   # peaked lapels
        lap = [(sgn * 46, -4), (sgn * 76, 24 + sh_dy * 0.5), (sgn * 60, 86), (sgn * 92, 100), (sgn * 70, 130),
               (sgn * 24, 176), (sgn * 30, 120)]
        p.poly(lap, NAVYJ, INK, 2.2)
    p.line([(-24, 176), (22, 236), (22, 460)], NAVYJ_D, 2.2)    # the front edge, crossing over (double-breasted)
    for bx in (-46, 46):                                  # gold buttons, two rows of two
        for by in (196, 264):
            p.ell(bx, by, 9, 9, GOLDB, INK, 1.6)
            p.ell(bx, by, 4.5, 4.5, (176, 130, 40), None)
    return sw


def arms(p, sh_dy):
    """Upper arms down the sides, forearms forward onto the podium; circle hands either side of her notes."""
    for sgn in (-1, 1):
        sh = (sgn * 140, 40 + sh_dy)
        el = (sgn * 172, 232)
        wr = (sgn * 112, PODIUM_TOP - 24)
        p.poly(curve([(sh[0] + sgn * 14, sh[1]), (el[0] + sgn * 14, el[1]), (wr[0] + sgn * 4, wr[1] + 14),
                      (wr[0] - sgn * 12, wr[1] - 16), (el[0] - sgn * 22, el[1] - 26), (sh[0] - sgn * 26, sh[1] + 40)], 3),
               NAVYJ, INK, 2.4)
        p.ell(wr[0] - sgn * 14, wr[1] + 2, 20, 17, SKIN, INK, 2.2)


def her(img, cam, t, st=None, notes=True):
    st = st or state(t)
    L = B.Local(cam, NECK[0], NECK[1], 1.0)
    p = B.Pen(img, L)
    hw, hh = 60, 84
    hx, hy = st['head_dx'], -138 + st['head_dy']
    sh = st['sh_dy']
    tilt = st['head_tilt']
    hair_mass(p, hx * 0.6, hy, hw, hh, sh)
    torso(p, sh)
    arms(p, sh)
    # the head (tilt by shearing the face sideways a little: flat, never a 3D turn)
    T = B.Local(cam, NECK[0] + 0, NECK[1] + 0, 1.0)

    class Tilted:
        def __init__(self, base):
            self.base, self.s = base, base.s

        def P(self, x, y):
            dx, dy = x - hx, y - (hy + 60)
            c, s_ = math.cos(tilt), math.sin(tilt)
            return self.base.P(hx + dx * c - dy * s_, hy + 60 + dx * s_ + dy * c)

        def S(self, v):
            return self.base.S(v)

    q = B.Pen(img, Tilted(T))
    for sgn in (-1, 1):                                   # ears hidden under the hair; a gold stud shows
        q.ell(hx + sgn * (hw + 1), hy + 14, 9, 17, SKIN, INK, 2.0)
    hair_front(q, hx, hy, hw, hh, sh)
    q.poly(head_shape(hx, hy, hw, hh), SKIN, INK, 2.6)
    face(q, hx, hy, hw, hh, st)
    if st.get('sweat', 0) > 0:                            # a single bead of sweat at her temple, flat, outlined
        sx, sy = hx + hw * 0.72, hy - hh * 0.42 + 10 * st['sweat']
        q.poly(curve([(sx, sy - 13), (sx + 7, sy + 1), (sx + 5, sy + 8), (sx - 5, sy + 8), (sx - 7, sy + 1)], 3),
               (214, 236, 250), INK, 1.6)
        q.line([(sx - 2, sy - 2), (sx - 3, sy + 3)], (255, 255, 255), 1.6)
    q.poly(head_shape(hx, hy, hw, hh), None, INK, 2.6)
    hair_top(q, hx, hy, hw, hh, hx)


# ------------------------------------------------------------------------------------------------ the set
SET_BLUE = (120, 178, 214)
SET_BLUE_L = (160, 206, 232)
SET_BLUE_D = (64, 108, 156)
DRAPE = (28, 58, 128)
DRAPE_D = (18, 40, 96)
WALL = (240, 238, 232)
WALL_D = (214, 212, 206)
WOOD = (132, 76, 42)
WOOD_D = (96, 52, 28)
PODIUM_C = (30, 36, 56)
CARPET = (34, 44, 86)
STAR = (176, 182, 196)
FLOOR = (62, 70, 96)
CREAM = WALL
# The room, from Sam's photos (15 Oct): a low stage between two white columns, recessed into the wall; the blue
# backdrop with the seal in the middle, dark blue drapes either side; a white beam above the columns and a low
# ceiling of light boxes; the stage carpet navy with grey stars and a white edge; rows of wooden-backed seats.
# World units at her distance: 1 m is about 830. Her neck is at y 1000; her feet (the stage) at 2200.
STAGE_Y = 2200          # the stage surface at the front
STAGE_EDGE = 2240       # the white trim along its front
FLOOR_Y = 2370          # the room's floor: the stage is only a shallow step up
BEAM_Y = -300           # the underside of the beam over the columns
COL_X = (-410, 1490)    # the two white columns at the stage's front corners


# ------------------------------------------------------------------------------------------------ steady lettering
_GLYPHS = {}


def stamp_text(img, cam, s, cx, cy, width, colr, font=SERIF, weight=700):
    """Lettering drawn once at high resolution, then scaled to an exact width in world units with sub-pixel
    placement, so it never jumps in size from frame to frame and always fits inside its plaque or seal."""
    key = (s, colr, font, weight)
    if key not in _GLYPHS:
        f = ImageFont.truetype(font, 240)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        l, t_, r, b = f.getbbox(s)
        lay = Image.new('RGBA', (r - l + 20, b - t_ + 20), colr + (0,))
        ImageDraw.Draw(lay).text((10 - l, 10 - t_), s, font=f, fill=colr + (255,))
        _GLYPHS[key] = lay
    src = _GLYPHS[key]
    W = cam.S(width)
    if W < 3:
        return
    k = W / src.width
    if k < 0.5:                                   # shrink in one good step first (no shimmering), then place exactly
        src = src.resize((max(1, int(src.width * k * 2)), max(1, int(src.height * k * 2))), Image.LANCZOS)
        k = W / src.width
    H = src.height * k
    X, Y = cam.P(cx, cy)
    ox, oy = X - W / 2, Y - H / 2
    x0, y0 = int(math.floor(ox)), int(math.floor(oy))
    tile = src.transform((int(math.ceil(W)) + 2, int(math.ceil(H)) + 2), Image.AFFINE,
                         (1 / k, 0, (x0 - ox) / k, 0, 1 / k, (y0 - oy) / k), resample=Image.BICUBIC)
    l0, t0 = max(0, -x0), max(0, -y0)
    r0, b0 = min(tile.width, img.width - x0), min(tile.height, img.height - y0)
    if r0 > l0 and b0 > t0:
        img.alpha_composite(tile.crop((l0, t0, r0, b0)), (x0 + l0, y0 + t0))


def white_house(p, cx, cy, w):
    """The White House, as on the seal: portico, columns, wings, a flag on the roof."""
    h = w * 0.42
    pal, pal_d = (234, 244, 250), (178, 206, 224)
    p.poly([(cx - w, cy), (cx + w, cy), (cx + w, cy - h * 0.62), (cx - w, cy - h * 0.62)], pal, INK, 1.6)
    p.poly([(cx - w * 0.32, cy), (cx + w * 0.32, cy), (cx + w * 0.32, cy - h * 0.86), (cx - w * 0.32, cy - h * 0.86)],
           pal, INK, 1.6)
    p.poly([(cx - w * 0.36, cy - h * 0.86), (cx + w * 0.36, cy - h * 0.86), (cx, cy - h * 1.16)], pal, INK, 1.6)
    for k in range(6):
        x = cx - w * 0.26 + k * w * 0.104
        p.line([(x, cy - 2), (x, cy - h * 0.8)], pal_d, 2.0)
    for side in (-1, 1):
        for k in range(4):
            x = cx + side * (w * 0.44 + k * w * 0.14)
            p.poly([(x - w * 0.03, cy - h * 0.18), (x + w * 0.03, cy - h * 0.18), (x + w * 0.03, cy - h * 0.42),
                    (x - w * 0.03, cy - h * 0.42)], pal_d, None)
    p.line([(cx, cy - h * 1.16), (cx, cy - h * 1.5)], INK, 1.4)
    p.poly([(cx, cy - h * 1.5), (cx + w * 0.12, cy - h * 1.44), (cx, cy - h * 1.38)], (190, 50, 60), None)


def seal(img, cam, cx, cy, rx, ry, words=True):
    """The oval White House seal: a pale rim, deep blue, the house, the words inside the oval."""
    p = B.Pen(img, cam)
    p.ell(cx, cy, rx * 1.06, ry * 1.08, (150, 196, 224), INK, 2.4)
    p.ell(cx, cy, rx, ry, (46, 98, 150), (214, 234, 246), 3.0)
    white_house(p, cx, cy - ry * 0.02, rx * 0.5)
    if words:
        stamp_text(img, cam, 'THE WHITE HOUSE', cx, cy + ry * 0.4, rx * 1.1, (232, 242, 250))
        stamp_text(img, cam, 'WASHINGTON', cx, cy + ry * 0.66, rx * 0.5, (232, 242, 250))


def _clip(img, lay, cam, *outlines):
    """Composite a layer onto the picture, kept inside every outline given (their overlap)."""
    a = np.asarray(lay.getchannel('A'))
    for pts in outlines:
        m = Image.new('L', img.size, 0)
        ImageDraw.Draw(m).polygon([cam.P(*pt) for pt in pts], fill=255)
        a = np.minimum(a, np.asarray(m))
    lay.putalpha(Image.fromarray(a))
    img.alpha_composite(lay)


def _star(p, cx, cy, r, colr):
    pts = [(cx + (r if k % 2 == 0 else r * 0.42) * math.cos(-math.pi / 2 + k * math.pi / 5),
            cy + (r if k % 2 == 0 else r * 0.42) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    p.poly(pts, colr, None)


def flag(img, cam, x, top, bottom, t):
    """The US flag on its pole, as in the briefing-room photos: the cloth hangs straight down beside the pole in
    soft vertical folds, the free edge scalloped where the folds turn, a gathered tail near the bottom; the blue
    canton at the top by the pole with its stars kept inside it; the stripes falling at a slant along the drape.
    A brass pole with a gold spear tip. (Sam, 15 Oct: no dots off the flag, no sock shape.)"""
    p = B.Pen(img, cam)
    w = 170
    # the pole and its gold spear tip
    p.poly(rough([(x - 6, top - 40), (x + 6, top - 40), (x + 7, STAGE_Y - 40), (x - 7, STAGE_Y - 40)], 1, 3),
           (200, 170, 90), INK, 2)
    p.ell(x, top - 52, 14, 14, (222, 184, 80), INK, 2)
    p.poly([(x - 12, top - 62), (x, top - 120), (x + 12, top - 62), (x, top - 70)], (222, 184, 80), INK, 2)
    # the cloth: attached down the pole, scalloped free edge, a gathered tail
    cloth = curve([(x + 5, top), (x + w * 0.55, top + 6), (x + w, top + 26), (x + w + 16, top + 170),
                   (x + w - 8, top + 260), (x + w + 12, top + 390), (x + w - 14, top + 520), (x + w, top + 660),
                   (x + w * 0.76, top + 840), (x + w * 0.52, top + 990), (x + w * 0.4, bottom),
                   (x + w * 0.22, bottom - 110), (x + 18, bottom - 300), (x + 5, top + 700)], 4)
    p.poly(cloth, (246, 246, 244), None)
    slope, sh = 0.42, 62.0
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = B.Pen(lay, cam)
    for k in range(0, 22, 2):                             # red stripes, falling at a slant along the drape
        y0 = top + 20 + k * sh
        q.poly([(x - 20, y0 - 20 * slope), (x + w + 40, y0 + (w + 40) * slope),
                (x + w + 40, y0 + sh + (w + 40) * slope), (x - 20, y0 + sh - 20 * slope)], (190, 40, 54), None)
    cw = w * 0.6                                           # the canton: down seven stripes, by the pole
    c_bot = top + 20 + 7 * sh
    canton = [(x - 20, top - 20), (x + cw, top - 20), (x + cw, c_bot + cw * slope), (x - 20, c_bot - 20 * slope)]
    q.poly(canton, (34, 48, 110), None)
    _clip(img, lay, cam, cloth)
    st = Image.new('RGBA', img.size, (0, 0, 0, 0))         # the stars, only ever inside the canton
    sp = B.Pen(st, cam)
    for row in range(9):
        for col in range(4):
            sx = x + 18 + col * 26 + (13 if row % 2 else 0)
            sy = top + 30 + row * 40 + (sx - x) * slope
            _star(sp, sx, sy, 7, (246, 246, 244))
    _clip(img, st, cam, cloth, canton)
    sd = Image.new('RGBA', img.size, (0, 0, 0, 0))         # the folds: flat darker bands where the cloth turns away
    fp = B.Pen(sd, cam)
    for fx0, fx1 in ((w * 0.28, w * 0.42), (w * 0.7, w * 0.86)):
        fp.poly([(x + fx0, top), (x + fx1, top), (x + fx1 - 10, bottom), (x + fx0 - 20, bottom)], (0, 0, 0, 46), None)
    _clip(img, sd, cam, cloth)
    for fx0 in (w * 0.28, w * 0.7):
        p.line([(x + fx0, top + 30), (x + fx0 - 4, top + 400), (x + fx0 - 16, bottom - 160)], (60, 24, 36), 1.6)
    p.poly(cloth, None, INK, 2.4)


def stars(p, x0, x1, y0, y1, gap, size, seed):
    """Small grey five-point stars in a staggered grid, as on the briefing-room stage carpet."""
    rng = np.random.default_rng(seed)
    row = 0
    y = y0 + gap * 0.4
    while y < y1:
        x = x0 + (gap * 0.5 if row % 2 else 0) + gap * 0.25
        while x < x1:
            r = size * (0.92 + 0.16 * rng.random())
            pts = [(x + (r if k % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + k * math.pi / 5),
                    y + (r if k % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + k * math.pi / 5) * 0.6) for k in range(10)]
            p.poly(pts, STAR, None)
            x += gap
        y += gap * 0.45
        row += 1


def column(p, x, top, bottom, w=70):
    """A round white column: fluting, a moulded base and a simple capital."""
    p.poly(rough([(x - w, top + 60), (x + w, top + 60), (x + w, bottom - 60), (x - w, bottom - 60)], 2, int(x)), WALL, INK, 2.6)
    for k in range(-3, 4):
        p.line([(x + k * w * 0.26, top + 80), (x + k * w * 0.26, bottom - 80)], WALL_D, 2.0)
    p.line([(x + w * 0.62, top + 70), (x + w * 0.62, bottom - 70)], (200, 198, 192), 6)        # the shaded side
    for y0, h, ww in ((top, 30, 1.35), (top + 30, 30, 1.15), (bottom - 60, 30, 1.2), (bottom - 30, 30, 1.4)):
        p.poly(rough([(x - w * ww, y0), (x + w * ww, y0), (x + w * ww, y0 + h), (x - w * ww, y0 + h)], 2, int(y0)),
               WALL, INK, 2.2)


def back_wall(img, cam, t):
    """Behind her (a little further back than she is): the backdrop, the seal, the drapes, the flag."""
    p = B.Pen(img, cam)
    p.poly([(-2600, BEAM_Y - 200), (3700, BEAM_Y - 200), (3700, STAGE_Y), (-2600, STAGE_Y)], DRAPE_D, INK, 3)
    # dark blue drapes either side of the backdrop, in folds
    for x0, x1, sd in ((-420, 40, 1), (1040, 1500, 2)):
        p.poly(rough([(x0, BEAM_Y), (x1, BEAM_Y), (x1, STAGE_Y), (x0, STAGE_Y)], 3, sd), DRAPE, INK, 3)
        for k in range(int((x1 - x0) / 46)):
            x = x0 + 24 + k * 46
            p.line([(x, BEAM_Y + 10), (x + 6, STAGE_Y - 10)], DRAPE_D, 3)
    # the pale blue backdrop: glass bands, little seals down the right, the big seal above her
    p.poly(rough([(40, BEAM_Y), (1040, BEAM_Y), (1040, STAGE_Y), (40, STAGE_Y)], 2, 3), SET_BLUE, INK, 3)
    for x in (50, 70, 90, 990, 1010, 1030):
        p.line([(x, BEAM_Y + 10), (x, STAGE_Y - 10)], SET_BLUE_L, 3)
    for j in range(7):
        cy = BEAM_Y + 160 + j * 300
        p.ell(950, cy, 50, 33, SET_BLUE_L, SET_BLUE_D, 2)
        white_house(p, 950, cy + 8, 22)
    seal(img, cam, 545, 420, 260, 172)
    flag(img, cam, 170, 520, 1700, t)
    p.poly(rough([(130, STAGE_Y - 40), (210, STAGE_Y - 40), (220, STAGE_Y), (120, STAGE_Y)], 1, 5), (196, 164, 84), INK, 2)


def room(img, cam):
    """The room around the stage (level with her): side walls, the beam, the low ceiling of light boxes, the
    stage itself, the floor."""
    p = B.Pen(img, cam)
    # side walls: blue panels beside the columns, then white walls; a round seal on the left, an arch on the right
    p.poly([(-2600, -1400), (3700, -1400), (3700, FLOOR_Y), (-2600, FLOOR_Y)], WALL, INK, 3)
    for x0, x1 in ((-820, -410), (1490, 1900)):
        p.poly(rough([(x0, BEAM_Y), (x1, BEAM_Y), (x1, FLOOR_Y), (x0, FLOOR_Y)], 3, x0), (52, 92, 160), INK, 3)
        p.poly(rough([(x0 + 60, 900), (x1 - 60, 900), (x1 - 60, FLOOR_Y), (x0 + 60, FLOOR_Y)], 3, x0 + 1), (44, 80, 146), INK, 2.4)
    p.ell(-1150, 600, 120, 120, (60, 104, 156), INK, 2.6)
    p.ell(-1150, 600, 100, 100, (46, 98, 150), (214, 234, 246), 2.4)
    white_house(p, -1150, 610, 52)
    p.poly(curve([(2050, FLOOR_Y), (2050, 700), (2150, 520), (2350, 470), (2550, 520), (2650, 700), (2650, FLOOR_Y)], 4)[:-2],
           (226, 224, 218), INK, 2.6)
    p.ell(-1400, 1000, 18, 26, (220, 200, 60), INK, 1.6)                                         # a fire alarm
    # the beam over the columns, and the ceiling: a grid of bright light boxes
    p.poly(rough([(-960, BEAM_Y - 140), (2040, BEAM_Y - 140), (2040, BEAM_Y), (-960, BEAM_Y)], 2, 61), WALL, INK, 3)
    p.line([(-960, BEAM_Y - 40), (2040, BEAM_Y - 40)], WALL_D, 3)
    p.poly([(-2600, -1400), (3700, -1400), (3700, BEAM_Y - 140), (-2600, BEAM_Y - 140)], (226, 226, 224), INK, 3)
    for j, (y, h, n, x0, x1) in enumerate(((-560, 90, 7, -900, 1980), (-820, 120, 6, -1300, 2380), (-1180, 160, 5, -1900, 2980))):
        p.poly([(x0 - 200, y - 30), (x1 + 200, y - 30), (x1 + 200, y + h + 30), (x0 - 200, y + h + 30)], (196, 198, 200), INK, 2)
        for k in range(n):
            x = x0 + (x1 - x0) * k / (n - 1)
            w = (x1 - x0) / (n - 1) * 0.36
            p.poly(rough([(x - w, y), (x + w, y), (x + w, y + h), (x - w, y + h)], 2, j * 10 + k), (252, 252, 248), (150, 150, 154), 2.4)
    # the stage: navy carpet with grey stars, a white edge, the riser, the room's floor
    p.poly([(-820, STAGE_Y - 150), (1900, STAGE_Y - 150), (1900, STAGE_EDGE), (-820, STAGE_EDGE)], CARPET, INK, 3)
    stars(p, -800, 1880, STAGE_Y - 140, STAGE_EDGE - 6, 130, 18, 7)
    p.poly(rough([(-860, STAGE_EDGE), (1940, STAGE_EDGE), (1940, STAGE_EDGE + 34), (-860, STAGE_EDGE + 34)], 2, 62),
           (244, 242, 236), INK, 2.6)
    p.poly([(-860, STAGE_EDGE + 34), (1940, STAGE_EDGE + 34), (1940, FLOOR_Y), (-860, FLOOR_Y)], (40, 50, 96), INK, 2.6)
    p.poly([(-2600, FLOOR_Y), (3700, FLOOR_Y), (3700, 6000), (-2600, 6000)], FLOOR, INK, 3)


def columns(img, cam):
    p = B.Pen(img, cam)
    for x in COL_X:
        column(p, x, BEAM_Y, STAGE_EDGE + 10)


def podium(img, cam):
    """The briefing-room podium: a dark top with the plaque, on a wooden pedestal that narrows and flares to a
    wide base on the stage; two thin microphones."""
    p = B.Pen(img, cam)
    x0, y0 = NECK[0], NECK[1] + PODIUM_TOP
    base_y = STAGE_Y - 20
    # the pedestal: wood, edged in navy
    ped = [(x0 - 170, y0 + 280), (x0 + 170, y0 + 280), (x0 + 95, base_y - 190), (x0 + 290, base_y - 20),
           (x0 - 290, base_y - 20), (x0 - 95, base_y - 190)]
    p.poly(rough(ped, 2, 44), PODIUM_C, INK, 3)
    p.poly([(x0 - 105, y0 + 290), (x0 + 105, y0 + 290), (x0 + 55, base_y - 200), (x0 + 210, base_y - 40),
            (x0 - 210, base_y - 40), (x0 - 55, base_y - 200)], WOOD, None)
    p.line([(x0, y0 + 250), (x0, base_y - 60)], WOOD_D, 3)
    p.poly(rough([(x0 - 310, base_y - 24), (x0 + 310, base_y - 24), (x0 + 322, base_y + 12), (x0 - 322, base_y + 12)], 2, 45),
           WOOD, INK, 2.6)
    # the top: slanted lid, a deep dark front with the plaque
    body = [(x0 - 316, y0 + 20), (x0 + 316, y0 + 20), (x0 + 290, y0 + 290), (x0 - 290, y0 + 290)]
    p.poly(rough(body, 2, 41), PODIUM_C, INK, 3)
    p.poly(rough([(x0 - 304, y0 - 6), (x0 + 304, y0 - 6), (x0 + 326, y0 + 22), (x0 - 326, y0 + 22)], 2, 42),
           (44, 50, 72), INK, 2.6)
    px0, py0, px1, py1 = x0 - 200, y0 + 70, x0 + 200, y0 + 230
    p.poly(rough([(px0, py0), (px1, py0), (px1, py1), (px0, py1)], 2, 43), (16, 18, 24), (96, 98, 110), 2.4)
    p.line([(px0 + 24, py0 + 96), (px1 - 24, py0 + 96)], (196, 36, 46), 5)
    stamp_text(img, cam, 'THE WHITE HOUSE', x0, py0 + 56, 320, (242, 240, 236))
    stamp_text(img, cam, 'WASHINGTON', x0, py0 + 126, 150, (242, 240, 236))
    for sgn in (-1, 1):                                   # the two thin microphones, leaning in towards her
        base = (x0 + sgn * 170, y0 - 2)
        tip = (x0 + sgn * 96, y0 - 150)
        p.line([base, (x0 + sgn * 140, y0 - 80), tip], (20, 20, 24), 3)
        p.ell(tip[0], tip[1], 7, 12, (20, 20, 24), INK, 1.4, rot=-sgn * 0.5)


def notes(img, cam):
    """Her notes on the podium top: the edge of the paper, poking out between her hands."""
    p = B.Pen(img, cam)
    x0, y0 = NECK[0], NECK[1] + PODIUM_TOP
    p.poly(rough([(x0 - 90, y0 - 10), (x0 + 84, y0 - 12), (x0 + 92, y0 + 4), (x0 - 96, y0 + 6)], 2, 51),
           (250, 250, 246), INK, 2)


# ------------------------------------------------------------------------------------------------ the reporters
# Rows of seated reporters seen from behind, each in a wooden-backed seat, filling the room wall to wall. Each row
# sits f nearer the camera than her; `sy` is where its heads land on screen in the opening frame.
REPORTER_ROWS = [(0.9, 1440), (1.9, 1540), (2.8, 1660), (3.6, 1800), (4.3, 1960), (4.8, 2150)]


def _reporters():
    rng = np.random.default_rng(12)
    rows = []
    hairs = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (210, 178, 120), (170, 166, 162), (110, 70, 46), (80, 40, 30),
             (196, 196, 192)]
    jackets = [B.NAVY, B.CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (60, 60, 70), (40, 110, 90),
               (150, 120, 90), (120, 160, 196), (222, 110, 50), (200, 60, 70), (236, 210, 214)]
    skins = [B.PALE, B.PINK, B.OLIVE, B.BROWN, B.DEEP]
    styles = ['short', 'bob', 'pony', 'long', 'bald', 'short', 'bun', 'curly', 'short', 'long']
    for f, sy in REPORTER_ROWS:
        k0 = D0 / (D0 - f)
        s = 1.05 * k0
        wy = A0[1] + (sy - 960) / Z0                     # world position that lands at screen y sy at the start
        pitch = 330 * s
        half = 1080 / (Z0 * k0) * 0.5 + pitch            # wall to wall, with a seat spare at each end
        n = int(2 * half / pitch) + 2
        xs = A0[0] - half + pitch * (np.arange(n) + (0.5 if len(rows) % 2 else 0.0))
        seats = []
        for x in xs:
            empty = False
            hand = False                                  # no hands up (Sam, 15 Oct)
            seats.append(dict(f=f, x=float(x + rng.uniform(-0.06, 0.06) * pitch), y=float(wy + rng.uniform(-10, 10) * s),
                              s=s, hair=hairs[rng.integers(len(hairs))], jacket=jackets[rng.integers(len(jackets))],
                              skin=skins[rng.integers(5)], style=styles[rng.integers(len(styles))], hand=hand,
                              side=1 if rng.random() < 0.5 else -1, up_at=float(rng.uniform(0, 9)),
                              seed=int(rng.integers(1e6)), empty=empty,
                              phone=False, pad=rng.random() < 0.15, typing=rng.random() < 0.45,
                              lean=float(rng.uniform(-0.06, 0.06))))
        rows.append((f, seats, pitch, wy, s))
    for ri, target in ((1, A0[0] - 330), (2, A0[0] + 360)):   # exactly two empty seats, both in view at the start
        min(rows[ri][1], key=lambda r: abs(r['x'] - target))['empty'] = True
    return rows


ROWS = _reporters()
REPORTERS = [r for _, seats, _, _, _ in ROWS for r in seats if not r['empty']]


def seat_backs(img, cam, row):
    """The row's wooden seat backs, in front of the people sitting in them: rounded tops, a grey striped
    cushion showing in each gap, carried down out of sight (nobody sinks into the floor)."""
    f, seats, pitch, wy, s = row
    p = B.Pen(img, cam)
    for r in seats:
        L = B.Pen(img, B.Local(cam, r['x'], wy, s))
        w = 150
        L.poly(rough([(-w, 170), (-w + 12, 140), (w - 12, 140), (w, 170), (w, 900), (-w, 900)], 2, r['seed'] % 97),
               WOOD, INK, 2.8)
        L.line([(-w + 14, 160), (w - 14, 160)], (160, 100, 60), 3)
        L.poly([(-48, 186), (48, 186), (48, 900), (-48, 900)], (118, 122, 132), INK, 2.2)   # the striped panel
        for k in range(5):
            L.line([(-36 + k * 18, 196), (-36 + k * 18, 890)], (196, 198, 204), 5)
        L.line([(-w + 20, 200), (-w + 20, 880)], WOOD_D, 2.4)
        if r['empty']:                                    # an empty seat: the striped cushion shows above the back
            L.poly([(-w + 16, 40), (w - 16, 40), (w - 16, 140), (-w + 16, 140)], (120, 124, 132), INK, 2.4)
            for k in range(7):
                L.line([(-w + 30 + k * 40, 46), (-w + 30 + k * 40, 136)], (170, 172, 178), 3)


def _look(r):
    """Each reporter's own build and clothes, worked out once from their seed: shoulder width and slope, a
    higher shoulder, head size, the garment and its pattern (Sam, 15 Oct: no identical blocky backs)."""
    if 'look' in r:
        return r['look']
    g = np.random.default_rng(r['seed'])
    garment = ['suit', 'suit', 'suit', 'blazer', 'sweater', 'blouse', 'cardigan', 'shirt'][g.integers(8)]
    if r['style'] in ('long', 'pony', 'bun', 'bob') and garment == 'suit' and g.random() < 0.6:
        garment = 'blazer'
    pattern = None
    if garment in ('suit', 'blazer') and g.random() < 0.4:
        pattern = ['pinstripe', 'check', 'tweed'][g.integers(3)]
    L = dict(sw=float(g.uniform(118, 158)), slope=float(g.uniform(24, 52)), hi=float(g.uniform(-12, 12)),
             nw=float(g.uniform(21, 29)), hrx=float(g.uniform(56, 70)), hry=float(g.uniform(70, 84)),
             garment=garment, pattern=pattern, lumps=[float(v) for v in g.uniform(-1, 1, 14)],
             shade_side=1 if g.random() < 0.5 else -1, folds=int(g.integers(2, 5)),
             tufts=[float(v) for v in g.uniform(0.7, 1.3, 9)])
    r['look'] = L
    return L


def _torso_outline(L, bottom=600):
    """Neck, the trapezius sloping to each shoulder, the round of the shoulder, the arms hanging down."""
    sw, sl, hi, nw = L['sw'], L['slope'], L['hi'], L['nw']
    pts = [(-sw + 6, bottom), (-sw - 6, sl + 150), (-sw - 4, sl + 60 - hi), (-sw + 18, sl + 12 - hi),
           (-sw * 0.55, sl * 0.45 - hi * 0.6), (-nw - 10, 6), (-nw, -2), (nw, -2), (nw + 10, 6),
           (sw * 0.55, sl * 0.45 + hi * 0.6), (sw - 18, sl + 12 + hi), (sw + 4, sl + 60 + hi), (sw + 6, sl + 150),
           (sw - 6, bottom)]
    return curve(pts, 4)


def _head_outline(L, cx, cy):
    """A hand-cut, slightly lumpy head (never a perfect oval)."""
    n = len(L['lumps'])
    return curve([(cx + L['hrx'] * (1 + 0.035 * L['lumps'][k]) * math.cos(2 * math.pi * k / n),
                   cy + L['hry'] * (1 + 0.035 * L['lumps'][(k + 3) % n]) * math.sin(2 * math.pi * k / n)) for k in range(n)], 3)


def _clothes(p, L, jc, sd, t):
    """Seams, collar, folds and pattern on the back of the garment; a flat shadow down one side."""
    sw, sl, hi, nw = L['sw'], L['slope'], L['hi'], L['nw']
    jd, jl = B.dk(jc, 0.8), B.lt(jc, 1.18)
    side = L['shade_side']
    p.poly(curve([(side * sw * 0.45, sl * 0.4 + 20), (side * (sw - 10), sl + 30 + hi * side), (side * (sw + 2), sl + 160),
                  (side * (sw - 4), 600), (side * sw * 0.55, 600), (side * sw * 0.6, 260)], 3), jd, None)   # flat shadow
    pat = L['pattern']
    if pat:                                               # the cloth's pattern, kept inside the back
        x0, x1, y0 = -sw + 26, sw - 26, sl + 46
        if pat == 'pinstripe':
            for k in range(int((x1 - x0) / 16)):
                p.line([(x0 + k * 16, y0), (x0 + k * 16, 600)], jl, 1.2)
        elif pat == 'check':
            for k in range(int((x1 - x0) / 34)):
                p.line([(x0 + k * 34, y0), (x0 + k * 34, 600)], jl, 1.6)
            for k in range(int((600 - y0) / 34)):
                p.line([(x0, y0 + k * 34), (x1, y0 + k * 34)], jl, 1.6)
        else:
            g = np.random.default_rng(sd)
            for _ in range(70):
                x, y = g.uniform(x0, x1), g.uniform(y0, 560)
                p.line([(x, y), (x + 5, y + 2)], jl if g.random() < 0.5 else jd, 1.4)
    gm = L['garment']
    if gm in ('suit', 'blazer'):
        p.line([(0, 30), (0, 600)], jd, 2.0)                                       # the centre back seam
        for sgn in (-1, 1):
            p.line([(sgn * (nw + 12), 10), (sgn * (sw - 16), sl + 10 + hi * sgn)], jd, 1.6)   # shoulder seams
            p.line(curve([(sgn * (sw - 16), sl + 12 + hi * sgn), (sgn * (sw - 30), sl + 90), (sgn * (sw - 26), sl + 170),
                          (sgn * (sw - 22), sl + 175)], 3)[:-4], jd, 1.6)        # the armhole
        for k in range(L['folds']):                                                # creases across the back
            y = 120 + 40 * k
            sg = 1 if (k + sd) % 2 else -1
            p.line(curve([(sg * 20, y), (sg * 60, y - 10), (sg * (sw - 40), y + 12), (sg * (sw - 30), y + 20)], 3)[:-4], jd, 1.4)
        p.poly(curve([(-nw - 22, 12), (-nw - 14, -10), (0, -14), (nw + 14, -10), (nw + 22, 12), (0, 22)], 3), jc, INK, 2.2)  # collar
        if gm == 'suit':
            p.poly(curve([(-nw - 6, -6), (0, -12), (nw + 6, -6), (nw + 4, -18), (0, -24), (-nw - 4, -18)], 3), (242, 240, 236), INK, 1.8)
    elif gm in ('sweater', 'cardigan'):
        p.poly(curve([(-nw - 18, 14), (-nw - 12, -8), (0, -12), (nw + 12, -8), (nw + 18, 14), (0, 18)], 3), jd, INK, 2.2)
        for k in range(-6, 7):                                                     # the ribbed neck
            p.line([(k * (nw + 14) / 6, -8 + abs(k) * 0.6), (k * (nw + 16) / 6, 14)], B.dk(jc, 0.65), 1.2)
        for row in range(5):                                                       # knit texture
            y = sl + 60 + row * 90
            for k in range(-4, 5):
                x = k * sw / 5 + (row % 2) * 12
                p.line([(x - 5, y), (x, y + 6), (x + 5, y)], jl, 1.2)
        for sgn in (-1, 1):
            p.line(curve([(sgn * (nw + 16), 10), (sgn * (sw * 0.6), sl + 40), (sgn * (sw - 20), sl + 150)], 3)[:-3], jd, 1.4)
    else:                                                 # blouse or shirt: soft drapes, a yoke seam
        p.line(curve([(-sw + 22, sl + 40), (0, sl + 30), (sw - 22, sl + 40)], 3)[1:-1], jd, 1.4)
        for k in range(3):
            x = -sw * 0.5 + k * sw * 0.5
            p.line(curve([(x, sl + 60), (x + 10, 260), (x - 6, 420), (x + 4, 590)], 3)[:-3], jd, 1.4)
        p.poly(curve([(-nw - 10, 8), (-nw - 4, -14), (0, -18), (nw + 4, -14), (nw + 10, 8), (0, 12)], 3),
               (246, 244, 240) if gm == 'shirt' else jc, INK, 1.8)


def _hair(p, L, st, hc, skin, cx, cy, sd):
    """Hair from behind, with its own nape, tufts and strands; a bald crown keeps its fringe."""
    rx, ry = L['hrx'], L['hry']
    hd, hl = B.dk(hc, 0.75), B.lt(hc, 1.2)
    tf = L['tufts']
    head = _head_outline(L, cx, cy)
    if st == 'bald':
        p.poly(head, skin, INK, 2.8)
        band = [(cx - rx - 3, cy - 6), (cx - rx * 0.9, cy + ry * 0.55)] + \
               [(cx - rx * 0.6 + k * rx * 0.3, cy + ry * (0.86 + 0.06 * tf[k])) for k in range(5)] + \
               [(cx + rx * 0.9, cy + ry * 0.55), (cx + rx + 3, cy - 6), (cx + rx * 0.7, cy + ry * 0.25), (cx, cy + ry * 0.36),
                (cx - rx * 0.7, cy + ry * 0.25)]
        p.poly(curve(band, 3), hc, INK, 2.2)
        p.line(curve([(cx - rx * 0.3, cy - ry * 0.6), (cx, cy - ry * 0.7), (cx + rx * 0.2, cy - ry * 0.62)], 3)[1:-1],
               B.lt(skin, 1.08), 3)
        return
    if st == 'long':
        p.poly(curve([(cx - rx - 6, cy - 20), (cx - rx - 14, cy + 120), (cx - rx * 0.4, cy + 250 * tf[0]),
                      (cx, cy + 240 * tf[1]), (cx + rx * 0.5, cy + 255 * tf[2]), (cx + rx + 14, cy + 120),
                      (cx + rx + 6, cy - 20), (cx, cy - ry - 8)], 4), hc, INK, 2.8)
        for k in range(5):
            x = cx - rx * 0.7 + k * rx * 0.35
            p.line(curve([(x, cy - ry * 0.6), (x - 6, cy + 60), (x + 4, cy + 200 * tf[k])], 3)[:-3], hd, 1.6)
        part = cx + rx * 0.15 * L['lumps'][0]
        p.line([(part, cy - ry - 6), (part + 2, cy - ry * 0.5)], hd, 2.0)          # the parting
        for sgn in (-1, 1):                                                        # the waves at the sides
            p.line(curve([(cx + sgn * (rx + 2), cy - 10), (cx + sgn * (rx + 12), cy + 60), (cx + sgn * (rx + 4), cy + 130),
                          (cx + sgn * (rx + 14), cy + 200)], 3)[1:-2], hd, 1.6)
        return
    p.poly(head, hc, INK, 2.8)
    if st in ('short', 'curly'):
        nape = [(cx - rx * 0.62, cy + ry * 0.8)] + [(cx - rx * 0.4 + k * rx * 0.2, cy + ry * (0.86 + 0.05 * tf[k]))
                                                    for k in range(5)] + [(cx + rx * 0.62, cy + ry * 0.8)]
        p.poly(nape + [(cx + rx * 0.5, cy + ry * 0.98), (cx, cy + ry * 1.04), (cx - rx * 0.5, cy + ry * 0.98)], skin, None)
        p.line(nape, INK, 1.8)                                                     # the nape's hairline, low
        if st == 'curly':
            for k in range(14):
                a = math.pi * (0.95 + k / 12.0)
                p.ell(cx + rx * 0.98 * math.cos(a), cy + ry * 0.95 * math.sin(a), 15 * tf[k % 9], 13, hc, INK, 2.0)
            for k in range(8):
                p.line(oval(cx - rx * 0.5 + (k % 4) * rx * 0.33, cy - ry * 0.4 + (k // 4) * 40, 7, 6, 8, 0, 4), hd, 1.4)
        else:
            whorl = (cx + rx * 0.2, cy - ry * 0.55)
            for k in range(7):                                                     # combed from the crown
                a = -0.9 + k * 0.42
                p.line(curve([whorl, (whorl[0] + rx * 0.5 * math.sin(a), whorl[1] + ry * 0.6 * math.cos(a) * 0.8),
                              (whorl[0] + rx * 0.8 * math.sin(a), whorl[1] + ry * 1.0 * math.cos(a))], 3)[1:-3], hd, 1.4)
    elif st == 'bob':
        p.poly(curve([(cx - rx - 8, cy - 30), (cx - rx - 12, cy + 70), (cx - rx * 0.4, cy + 96 * tf[0]), (cx, cy + 90),
                      (cx + rx * 0.4, cy + 98 * tf[1]), (cx + rx + 12, cy + 70), (cx + rx + 8, cy - 30), (cx, cy - ry - 6)], 4),
               hc, INK, 2.8)
        for k in range(5):
            x = cx - rx * 0.6 + k * rx * 0.3
            p.line(curve([(x, cy - ry * 0.7), (x - 4, cy + 20), (x + 2, cy + 84)], 3)[:-2], hd, 1.5)
    elif st in ('pony', 'bun'):
        for k in range(6):
            a = -0.8 + k * 0.32
            p.line(curve([(cx + rx * math.sin(a) * 0.95, cy - ry * 0.6), (cx + rx * math.sin(a) * 0.5, cy - ry * 0.1),
                          (cx, cy + 6)], 3)[1:-2], hd, 1.4)
        if st == 'pony':
            p.poly(curve([(cx - 14, cy), (cx + 14, cy), (cx + 24 * tf[0], cy + 90), (cx + 6, cy + 150 * tf[1]),
                          (cx - 14, cy + 100)], 3), hc, INK, 2.4)
            p.line(curve([(cx, cy + 20), (cx + 8, cy + 90), (cx + 2, cy + 130)], 3)[:-2], hd, 1.4)
            p.poly(curve([(cx - 15, cy - 8), (cx + 15, cy - 8), (cx + 14, cy + 8), (cx - 14, cy + 8)], 2),
                   (190, 50, 70), INK, 1.8)
        else:
            p.poly(curve(oval(cx + 4, cy - ry * 0.2, 34 * tf[0], 28, 10), 3), hc, INK, 2.4)
            p.line(oval(cx + 4, cy - ry * 0.2, 18, 12, 10, 0.4, 4.6), hd, 1.4)
    p.line(curve([(cx - rx * 0.5, cy - ry * 0.75), (cx - rx * 0.2, cy - ry * 0.88), (cx + rx * 0.1, cy - ry * 0.86)], 3)[1:-1],
           hl, 2.4)                                                                # a flat sheen on top


def reporter(img, cam, r, t):
    """A seated reporter from behind, each one their own build, clothes and haircut. Quiet life only (Sam,
    15 Oct): shifting in the seat now and then, a glance aside or down, typing (elbows going), scribbling notes."""
    if r.get('empty'):
        return
    sd = r['seed']
    L = _look(r)
    dx = 9 * filmkit.shifts(t, seed=sd, amount=1.0, hold=(2.0, 4.5))           # shuffling in the seat
    hdx = 10 * filmkit.shifts(t, seed=sd + 1, amount=1.0, hold=(1.6, 3.6))     # a glance aside
    hdy = 8 * max(0.0, filmkit.shifts(t, seed=sd + 2, amount=1.0, hold=(1.8, 4.0)))   # a glance down at the notes
    p = B.Pen(img, B.Local(cam, r['x'] + dx * r['s'], r['y'], r['s']))
    ph = B.Pen(img, B.Local(cam, r['x'] + (dx + hdx) * r['s'], r['y'] + hdy * r['s'], r['s']))
    hc, jc, skin, st = r['hair'], r['jacket'], r['skin'], r['style']
    sw, sl = L['sw'], L['slope']
    if r.get('typing'):                                   # elbows out at the sides, bobbing while they type
        on = (t * 0.9 + sd % 13) % 4.0 < 2.8
        for sgn in (-1, 1):
            bob = 4 * math.sin(t * 22 + sgn * 1.7 + sd % 5) if on else 0.0
            p.poly(curve(oval(sgn * (sw + 4), sl + 190 + bob * sgn, 30, 44, 10), 3), jc, INK, 2.6)
    # the neck first (behind the collar), then the back, then the head
    nw = L['nw']
    ph.poly(curve([(-nw, 10 - hdy), (-nw + 2, -40), (0, -46), (nw - 2, -40), (nw, 10 - hdy)], 3), skin, INK, 2.4)
    ph.line([(-nw * 0.4, -10), (nw * 0.3, -12)], B.dk(skin, 0.86), 1.4)
    p.poly(_torso_outline(L), jc, INK, 2.8)
    _clothes(p, L, jc, sd, t)
    p.poly(_torso_outline(L), None, INK, 2.8)
    cx, cy = 0, -84
    for sgn in (-1, 1):                                   # ears, with an inner fold
        ph.poly(curve(oval(cx + sgn * (L['hrx'] - 2), cy + 14, 11, 19, 10), 3), skin, INK, 2.4)
        ph.line([(cx + sgn * (L['hrx'] + 1), cy + 4), (cx + sgn * (L['hrx'] + 4), cy + 22)], B.dk(skin, 0.8), 1.4)
    _hair(ph, L, st, hc, skin, cx, cy, sd)
    if r['pad'] and not r.get('typing'):                  # a notebook held up by the shoulder, scribbled in
        tilt = 4 * math.sin(t * 9 + sd) if (t + sd % 7) % 3.0 < 1.6 else 0.0
        q = p
        q.poly(rough([(sw - 60, 60 + tilt), (sw + 16, 50 - tilt), (sw + 22, 150 - tilt), (sw - 54, 160 + tilt)], 3, sd),
               (250, 248, 236), INK, 2.4)
        for k in range(3):
            q.line([(sw - 44, 80 + 20 * k), (sw + 4, 74 + 20 * k)], (150, 160, 190), 2)


def crowd(img, t):
    """Rows drawn back to front, each with its own depth (nearer rows swell and slide away as we push in);
    each row's people, then the backs of the seats they sit in."""
    for row in sorted(ROWS, key=lambda r: r[0]):
        f, seats = row[0], row[1]
        cam = cam_at(t, f)
        if cam is None:
            continue
        X, Y = cam.P(A0[0], row[3])
        if Y - cam.S(400 * row[4]) > B.H * B.SS:
            continue
        for r in seats:
            reporter(img, cam, r, t)
        seat_backs(img, cam, row)


TV_RISER = 1.6        # the camera riser on the right sits this much nearer than her


def tv_crew(img, cam, t):
    """A camera riser on the right: two TV cameras on tripods and an operator, side on."""
    p = B.Pen(img, cam)
    p.poly(rough([(1500, 2500), (2700, 2500), (2700, 3400), (1500, 3400)], 3, 71), (70, 74, 86), INK, 3)
    for k, x in enumerate((1700, 2150)):
        for dx in (-90, 0, 90):
            p.line([(x, 2160), (x + dx, 2500)], (40, 40, 44), 5)
        p.poly(rough([(x - 150, 2040), (x + 120, 2040), (x + 120, 2160), (x - 150, 2160)], 2, 72 + k), (36, 36, 40), INK, 2.6)
        p.poly(rough([(x - 260, 2060), (x - 150, 2050), (x - 150, 2150), (x - 260, 2140)], 2, 74 + k), (24, 24, 28), INK, 2.4)
        p.ell(x - 262, 2100, 16, 40, (90, 110, 140), INK, 2)
    op = dict(x=2380, y=1900, s=0.9, hair=(40, 30, 26), jacket=(40, 44, 54), skin=B.PINK, style='short', hand=False,
              side=1, up_at=0.0, seed=5, empty=False, phone=False, pad=False)
    reporter(img, cam, op, t)


# ------------------------------------------------------------------------------------------------ the frame
def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas(WALL)
    room(img, cam_at(t, -0.3))
    back_wall(img, cam_at(t, -0.3), t)
    cam = cam_at(t)
    her(img, cam, t)
    notes(img, cam)
    podium(img, cam_at(t, 0.04))
    columns(img, cam_at(t, 0.25))
    crowd(img, t)
    return img


def _caption_chunks():
    """Subtitles (Sam, 15 Oct): the script in pieces at its commas and full stops, each at most 42 characters
    (two rows), timed to her words; tiny pieces join their neighbour; each stays up until just before the next."""
    pieces, cur = [], []
    for wi, (st_, en_, w) in enumerate(TALK):
        if wi in FRESH and cur:
            pieces.append(cur)
            cur = []
        cur.append((st_, en_, w, wi))
        if w[-1] in ',.':
            pieces.append(cur)
            cur = []
    if cur:
        pieces.append(cur)
    split = []
    for pc in pieces:                                  # anything over 42 characters splits at its middle word
        while len(' '.join(x[2] for x in pc)) > 42:
            total = len(' '.join(x[2] for x in pc))
            k = min(range(1, len(pc)), key=lambda i: abs(len(' '.join(x[2] for x in pc[:i])) - total / 2))
            split.append(pc[:k])
            pc = pc[k:]
        split.append(pc)
    pieces = split
    merged = []
    for pc in pieces:
        text = ' '.join(x[2] for x in pc)
        if merged:
            prev = merged[-1]
            ptext = ' '.join(x[2] for x in prev)
            gap = pc[0][0] - prev[-1][1]
            fresh_here = pc[0][3] in FRESH or any(x[3] in FRESH for x in prev)
            if not fresh_here and (len(text) < 14 or len(ptext) < 10) and len(ptext) + 1 + len(text) <= 40 and gap < 0.5:
                merged[-1] = prev + pc
                continue
        merged.append(pc)
    out = []
    for i, pc in enumerate(merged):
        start = pc[0][0] + (0.0 if pc[0][3] in FRESH else 0.1)   # with the word, never ahead of it (Sam, 15 Oct)
        nn = merged[i + 1] if i + 1 < len(merged) else None
        nxt = (nn[0][0] + (0.0 if nn[0][3] in FRESH else 0.1)) if nn else BLACK_AT
        text = ' '.join(x[2] for x in pc)
        end = min(nxt, max(pc[-1][1] + 0.4, start + len(text) / 15.0))
        out.append([start, end, text])
    for i in range(len(out) - 1):                      # a quick piece borrows a moment from the next (readable)
        need = len(out[i][2].split()) / 3.5 + 0.1
        if out[i][1] - out[i][0] < need and out[i + 1][2].split()[0] not in FRESH_TEXT:
            out[i][1] = out[i][0] + need
            out[i + 1][0] = max(out[i + 1][0], out[i][1])
    return [tuple(c) for c in out]


FRESH_TEXT = {TALK[i][2] for i in FRESH}
CAPTIONS = _caption_chunks()


def caption_at(t):
    return next((c for a, b, c in CAPTIONS if a <= t < b), None)


def overlay(img, t):
    """Subtitles go on last (a wording change never re-renders a picture). The Hook Text is stamped later by
    hook_text.py / finish.py, at y 1180 so it clears both her face and the subtitles."""
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            import peepee as PP
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ the sheets
def label(img, x, y, s, size=30, colr=(30, 30, 30)):
    f = ImageFont.truetype(B.SANS, size)
    ImageDraw.Draw(img).text((x, y), s, font=f, fill=colr, anchor='mm')


def cast_sheet(out):
    """Her in every expression the film uses (talking, reading her notes, the smile levels, the sigh, the dead
    'Venezuela'), the strength sheet of her smile, and a row of the reporters."""
    B.SS = 1
    W, H = 2160, 2400
    sheet = Image.new('RGB', (W, H), (232, 228, 222))
    base = dict(gaze='up', lid=0.0, brow=0.0, mouth='rest', smile=0, head_dy=0.0, head_tilt=0.0, sh_dy=0.0,
                closed=False, look_x=0.0, squint=0.0, head_dx=0.0)
    looks = [
        ('1  calm, looking at the room', {}),
        ('2  talking', dict(mouth='mid')),
        ('3  reading her notes', dict(gaze='down', lid=0.62, head_dy=10, brow=-2, mouth='small')),
        ('4  smile 1: small, closed', dict(smile=1, brow=4)),
        ('5  smile 2: the big toothy one', dict(smile=2, brow=11, squint=0.4, head_tilt=-0.04)),
        ('6  smile 3: the huge strange one', dict(smile=3, brow=14, squint=0.6, head_tilt=0.04)),
        ('7  the sigh', dict(gaze='down', closed=True, mouth='blow', sh_dy=-14, head_dy=10, brow=3)),
        ('8  "...Venezuela" (flat, dead)', dict(gaze='down', lid=0.72, head_dy=12, brow=-3, mouth='small')),
    ]
    for i, (name, ch) in enumerate(looks):
        col, row = i % 4, i // 4
        tile = Image.new('RGBA', (540, 760), (232, 228, 222, 255))
        bg = B.Pen(tile, B.Cam(1.0, 540, 960))
        cam = B.Cam(1.55, NECK[0], NECK[1] - 140)
        cam.cx, cam.cy = NECK[0], NECK[1] - 140
        st = dict(base, **ch)
        layer = B.canvas(SET_BLUE)
        tc = B.Cam(1.3, NECK[0], NECK[1] + 60)
        her(layer, tc, 0.0, st)
        notes(layer, tc)
        podium(layer, tc)
        crop = layer.convert('RGB').crop((190, 380, 890, 1365)).resize((540, 760))
        sheet.paste(crop, (col * 540, 70 + row * 830))
        label(sheet, col * 540 + 270, 40 + row * 830, name, 26)
    # the whole room, the opening frame, small, and a row of reporters
    wide = picture(0.0).convert('RGB').resize((540, 960))
    sheet.paste(wide.crop((0, 120, 540, 840)), (0, 1700))
    label(sheet, 270, 1675, '9  the room (opening frame)', 26)
    end = picture(PUSH_END + 0.1).convert('RGB').resize((540, 960)).crop((0, 120, 540, 840))
    sheet.paste(end, (540, 1700))
    label(sheet, 810, 1675, '10  the close-up (end of the push)', 26)
    tile = B.canvas((232, 228, 222)).convert('RGBA')
    for i, r in enumerate(REPORTERS[:20:2][:6]):
        rr = dict(r, x=150 + i * 170, y=1300, s=0.55, hand=(i % 2 == 0), up_at=0.0)
        reporter(tile, B.Cam(1.0, 540, 960), rr, 0.0)
    rep = tile.convert('RGB').crop((40, 1000, 1080, 1460)).resize((1040, 460))
    sheet.paste(rep, (1100, 1720))
    label(sheet, 1620, 1675, '11  reporters from behind (all different)', 26)
    sheet.save(out, quality=90)


def stills(out, times):
    B.SS = 1
    n = len(times)
    cols = min(6, n)
    rows = (n + cols - 1) // cols
    tw, th = 360, 640
    sheet = Image.new('RGB', (cols * tw, rows * (th + 44)), (20, 20, 20))
    for i, t in enumerate(times):
        im = frame_image(t).convert('RGB').resize((tw, th))
        sheet.paste(im, ((i % cols) * tw, (i // cols) * (th + 44) + 44))
        label(sheet, (i % cols) * tw + tw // 2, (i // cols) * (th + 44) + 22, f'{t:.1f}s  {beat_name(t)}', 22,
              (240, 240, 240))
    sheet.save(out, quality=88)


def beat_name(t):
    if t >= BLACK_AT:
        return 'black'
    if SIGH[0] <= t < SIGH[1]:
        return 'SIGH'
    sm = next((lv for a, b, lv in SMILES if a <= t < b), None)
    if sm:
        return f'smile {sm}'
    w = next((w for a, b, w in TALK if a - 0.05 <= t < b + 0.05), None)
    return f'"{w}" ({gaze_at(t)})' if w else f'(pause, {gaze_at(t)})'


def soundtrack():
    """Her voice only (no effects), from the first word's lead-in, mastered to -16 LUFS; silent after the cut."""
    import mossad_audio as MA
    n = int((DUR + 0.3) * MA.SR)
    mix = np.zeros(n)
    seg = VOICE[:n]
    mix[:len(seg)] = seg
    end = int(BLACK_AT * MA.SR)
    mix[end:] = 0
    mix, _ = MA.master(mix, end)
    mix[end:] = 0
    return mix


def _write_wav(path, mix):
    import mossad_audio as MA
    MA.write_wav(path, mix)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        stills(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'timeline':
        print(f'length {END:.1f} s, push ends {PUSH_END:.1f} s')
        for st_, en_, w in TALK:
            print(f'{st_:5.1f}-{en_:5.1f}  {w}  ({gaze_at(st_ + 0.01)})')
        print('smiles', [(round(x, 1), round(y, 1), l) for x, y, l in SMILES], 'sigh', [round(x, 1) for x in SIGH])
    elif a[0] == 'final':
        import film_engine as E
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=lambda t: 'push', sound=soundtrack,
                 write_wav=_write_wav, set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 22,
                 reuse='--reuse' in a, redo=())


if __name__ == '__main__':
    main()
