#!/usr/bin/env python3
"""The Traitors, TikTok Story teaser (Sam, 17 Oct): Claudia says "Donald," under the cranberry lettering TOMORROW
(the film goes up Sunday 9am). The opening shot of the film, cut to her one word; nothing new is drawn.

    python3 source/traitors_story.py still OUT.jpg [T]     the frame at T seconds (default 1.0)
    python3 source/traitors_story.py final OUT.mp4 [--small]
Then: python3 source/finish.py OUT.mp4 animations/traitors-story.mp4      (adds the CranbriJoos sign-off)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import traitors as T             # noqa: E402
import burnham as B              # noqa: E402
import mossad_audio as MA        # noqa: E402
import film_engine as E          # noqa: E402

SR, FPS = T.SR, T.FPS
WORD_END = 0.94          # "Donald," ends here in the film's time; the next word starts at 1.62 s
CUT = 1.28               # the cut, in the silence between the two (never mid-sound)
DUR = BLACK_AT = 2.9     # a beat of Claudia, silent and still, under the lettering
TITLE = ('TOMORROW',)
TITLE_AT = dict(cap=116, top=330)          # one line sits highest; never above 310 (TikTok's buttons)

T.TRACK['claudia'] = [x for x in T.TRACK['claudia'] if x[1] <= WORD_END + 0.1]   # her mouth moves for one word only
T.CAPS[:] = [(T.CAPS[0][0], 1.75, 'Donald,')]


def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas((24, 16, 12))
    T.shot_claudia(img, t)
    return img


def overlay(img, t):
    if t < BLACK_AT:
        c = T.caption_at(t)
        if c:
            T.caption(img, c)
        B.title_lines(img, TITLE, **TITLE_AT)
    return img


def soundtrack():
    n = int((DUR + 0.3) * SR)
    voice = np.zeros(n)
    ln = T.LINES[0]
    seg = ln['_voice'][:int(CUT * SR)].copy()
    seg[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))        # a 30 ms fade inside the silence
    voice[:len(seg)] += seg
    mix, g = MA.master(voice, int(BLACK_AT * SR))
    mix[int(BLACK_AT * SR):] = 0
    return mix


def main():
    a = sys.argv[1:]
    if a[0] == 'still':
        B.SS = 1
        t = float(a[2]) if len(a) > 2 else 1.0
        overlay(picture(t), t).convert('RGB').save(a[1], quality=90)
    elif a[0] == 'final':
        small = '--small' in a
        E.render('traitors-story', a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS,
                 dur=DUR, picture=picture, overlay=overlay, shot_of=lambda t: 'claudia', sound=soundtrack,
                 write_wav=MA.write_wav, set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20)


if __name__ == '__main__':
    main()
