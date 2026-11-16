#!/usr/bin/env python3
"""The frozen code-finder replay (code-finder Learn step, Sam's 1, 16 Nov; notes/proposals/code-finder.md).
26 Blessed notes with a named fix (notes/archive/blessed-notes-animatics-1-2.md): each note's words, shot and time go to
`page.py blessed show` as a round chat would pass them; a hit = the ~40 lines hold the fix's target word.
Loose: any code word the fix names. Strict: only distinctive names (14 notes). Note 18's code (cot_top) was new, so it
is scored on showing the nearest like shot ('cot'). Targets are fixed: never tune them to the finder.
    python3 notes/proposals/learn/replay-show.py [--words-only] [-v]
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'source'))
LOOSE = {1: ['HEAD_K'], 2: ['chin_long'], 8: ['gaze', 'turn'], 9: ['ears_hidden'], 11: ['camera', 'zoom'],
         12: ['press_spots'], 13: ['mouth', 'front'], 14: ['neck', 'bald'], 16: ['seat'], 18: ["'cot'"], 19: ['LINES'],
         20: ['phone'], 22: ['chair'], 23: ['zoom', 'neck'], 24: ['flash', 'photograph'], 27: ['music'], 30: ['gates2'],
         31: ['gates2', 'zoom'], 32: ['G2_PART', 'gates2'], 35: ['LINES', 'shall'], 37: ['dock', 'cy'], 38: ['music'],
         43: ['pool', 'chair'], 44: ['tvroom', 'voice'], 45: ['checks', 'mouth'], 46: ['gates2', 'gates']}
STRICT = {1: ['HEAD_K'], 2: ['chin_long'], 9: ['ears_hidden'], 12: ['press_spots'], 18: ["'cot'"], 19: ['LINES'],
          27: ['music'], 30: ['gates2'], 31: ['gates2'], 32: ['G2_PART', 'gates2'], 35: ['LINES'], 37: ['dock'],
          38: ['music'], 45: ['checks']}


def rows():
    out = {}
    for l in open(os.path.join(ROOT, 'notes/archive/blessed-notes-animatics-1-2.md'), encoding='utf-8'):
        p = [x.strip() for x in l.split('|')]
        if len(p) > 6 and p[1].isdigit():
            out[int(p[1])] = (p[2], p[3], p[4])          # shot, time, note
    return out


def run(words_only=False, verbose=False):
    import page
    R, res = rows(), {}
    for n in sorted(LOOSE):
        shot, time, note = R[n]
        note = re.sub(r"[^A-Za-z0-9' ]", ' ', note)[:160]
        out = page.show('blessed', note, 40, None if words_only else shot, None if words_only else page._at(time))
        txt = '\n'.join([h for h, _ in out] + [t for _, rs in out for _, t in rs])
        n_lines = sum(len(rs) + 1 for _, rs in out)
        hit = lambda toks: [t for t in toks if re.search(re.escape(t), txt, re.I)]
        res[n] = (hit(LOOSE[n]), hit(STRICT.get(n, [])), n_lines)
        if verbose:
            print(n, shot, '|', 'HIT' if res[n][0] else 'MISS', res[n][0], 'strict', res[n][1] if n in STRICT else '-', n_lines, 'lines')
    loose = sum(1 for n in LOOSE if res[n][0])
    strict = sum(1 for n in STRICT if res[n][1])
    return loose, strict, max(r[2] for r in res.values()), res


if __name__ == '__main__':
    lo, st, mx, _ = run('--words-only' in sys.argv, '-v' in sys.argv)
    print(f'loose {lo}/{len(LOOSE)}  strict {st}/{len(STRICT)}  longest {mx} lines')
