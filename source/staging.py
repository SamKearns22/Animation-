#!/usr/bin/env python3
"""MAP  staging: no shot moves before Sam has seen its framing (lesson staging-stills, Sam's option 1, 22 Nov; rule 11).

Why (notes/proposals/staging-stills/learn.md): over four films, 5 framings Sam had to note twice were all built and
sent as clips before he saw a picture of them; Milburn's Cabinet Room shot was built three times. The board check ran
only at the animatic. Now a clip, as well as the animatic, is refused for a shot whose framing Sam has not seen.

The record: story/FILM-staging.txt, one line per event, oldest first (times are epoch seconds):
    hold SHOT EPOCH note=N WORDS        a note about framing or staging: the shot's board is out of date
    options SHOT EPOCH FILE n=K         the sheet of K numbered framings reached Sam
    pick SHOT EPOCH N WORDS             Sam's number (0: none of them, his own framing in WORDS; go: build without a sheet)
    notframing NOTE EPOCH WORDS         a note the word finder flagged that is not about framing (why, in WORDS)

    python3 source/staging.py restage FILM SHOT[,SHOT] --note N "Sam's words"    the note marks the shots held
    python3 source/staging.py options FILM SHOT OUT.jpg A.jpg B.jpg [C.jpg] --script K "the screenplay's camera line"
                                     [--labels "one|two|three"]   the numbered sheet (K: the option that follows the
                                     script's camera line word for word); then SendUserFile it, then:
    python3 source/staging.py sent FILM OUT.jpg --delivered      the sheet recorded as seen
    python3 source/staging.py pick FILM SHOT N "Sam's words"     his number (or 0, or go); then build it, draw the
                                     shot on the board (rough.py board FILM OUT.jpg --shots SHOT), send, `sent --board`
    python3 source/staging.py notframing FILM NOTE "why"         a flagged note that is not about framing
    python3 source/staging.py check FILM [SHOT ...]              what is held and why (exit 1 if anything is)

The gate (gate(); film_engine.render calls it for a clip, rough.board_gate for the animatic), for each shot:
  1. never on a shot board that reached Sam: refused (rule 11; new shots included)
  2. held by a framing note: refused until Sam's number is recorded after the hold AND a board with the shot, drawn
     after his number, has reached him (the framing as built, before it moves); 'go' lifts it on his words alone
  3. a note in the film's notes whose words read as framing (FRAMING, on Sam's words only) on this shot, with no hold
     and no notframing mark for it: refused (so a framing note cannot be fixed straight into a clip)
Films begun before the shot board (rough._before_rule) are not gated. Not covered: a chat that changes a framing on its
own, with no note (the frames' digest changes with every pose, so it cannot tell a re-stage from a move); movement
code can still be written for a held shot, only not rendered or sent.

Map: record 50 | the note finder 95 | the gate 160 | options sheet 225 | main 270
"""
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


# ---------------------------------------------------------------------------------------------- record
def _name(film):
    return film.replace('_', '-')


def record_path(film, root=ROOT):
    return os.path.join(root, 'story', f'{_name(film)}-staging.txt')


def record(film, root=ROOT):
    """[(kind, key, epoch, fields)] oldest first; fields: note/file/n/pick/words as the kind has them."""
    out, p = [], record_path(film, root)
    if os.path.exists(p):
        for ln in open(p):
            f = ln.rstrip('\n').split(' ', 3)
            if len(f) < 3 or f[0] not in ('hold', 'options', 'pick', 'notframing'):
                continue
            rest = f[3] if len(f) > 3 else ''
            d = {}
            if f[0] == 'hold':
                m = re.match(r'note=(\S+)\s*(.*)', rest)
                d = dict(note=m.group(1), words=m.group(2)) if m else dict(note='', words=rest)
            elif f[0] == 'options':
                m = re.match(r'(\S+)\s+n=(\d+)', rest)
                d = dict(file=m.group(1), n=int(m.group(2))) if m else dict(file=rest, n=0)
            elif f[0] == 'pick':
                pk, _, w = rest.partition(' ')
                d = dict(pick=pk, words=w)
            else:
                d = dict(words=rest)
            out.append((f[0], f[1], int(f[2]), d))
    return out


def _write(film, line, root=ROOT):
    p = record_path(film, root)
    new = not os.path.exists(p)
    with open(p, 'a') as fh:
        if new:
            fh.write('# Framing holds (rule 11, lesson staging-stills; source/staging.py). '
                     'hold/options/pick SHOT EPOCH ...; notframing NOTE EPOCH why\n')
        fh.write(line.replace('\n', ' ') + '\n')


# ---------------------------------------------------------------------------------------------- the note finder
# Sam's words about where people are or how the shot is framed. Tested on four films' notes (kittest
# staging_stills_note_finder): it must find every staging note the look back listed, and leave face, hair and
# movement notes alone. A wrong flag costs one `notframing` line; a miss costs a round, so it leans to flagging.
FRAMING = re.compile(
    r"compos(e|ed|ition)|\bfram(ed|ing)\b|in (the )?(frame|shot)\b|re-?stag|\bstag(ed|ing)\b|camera|\blens\b|"
    r"\bwide(n|r)?\b|closer|further (out|back|away)|centr(e|al|ed|alise)\b|space around|from the side|"
    r"side[- ]on|\bzoom(?!s? by)|close-?up|two-?shot|look(ing)? across|"
    r"\b(at|from) \d{1,2}(:\d\d)?( o'clock)?\b(?![.,:\d%]| ?(s|sec|m|cm|px)\b)|"
    r"\bin front of\b|\bforeground|\bbackground(?! music)|speck|\bbunched|empty (space|paving|half|wall)|"
    r"close together|too (close|far)|far from|crammed|\b(distance|gap) between|open the gap|thicker|thinner|"
    r"\b(is|looks|too|very) (small|tiny)\b|(?-i:\b(FRONT|MIDDLE|BACK|LEFT|RIGHT)\b:)|"
    r"\b(sit|sits|stand|stands|seated|standing) (at|in|on|by|beside|behind|nearer|further)|position",
    re.I)


def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def notes_in(text):
    """[(id, shots text, Sam's words)] from a film's notes: table rows (the column headed 'note' is his words) and
    '- [ ] ID words' or '- **ID (shot, time ...):** words' lines."""
    out, col, shotcol = [], None, 1
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('|'):
            c = _cells(s)
            low = [x.lower() for x in c]
            if c and c[0] in ('#', 'n', 'no', 'note') and any('note' in x for x in low[1:] + [low[0]]):
                col = next((i for i, x in enumerate(low) if i > 0 and x.startswith('note')), 3)
                shotcol = next((i for i, x in enumerate(low) if x.startswith('shot')), 1)
                continue
            if col is not None and c and re.fullmatch(r'[A-Za-z]{0,3}\d+[a-z]?', c[0]) and len(c) > col:
                out.append((c[0], c[shotcol] if len(c) > shotcol else '', c[col]))
            continue
        col = None
        m = re.match(r'-\s*\[[ xX]\]\s*([A-Z]{1,3}\d+[a-z]?)\b\s*(?:\([^)]*\))?\s*(.*)', s)
        if m:
            out.append((m.group(1), '', re.split(r'\s+-\s+Plan\b|\s+-\s+[A-Z][a-z]+ the\b', m.group(2))[0]))
            continue
        m = re.match(r'-\s*\*\*([A-Z]{0,3}\d+[a-z]?)\s*\(([^)]*)\)[^*]*\*\*\s*(.*)', s)
        if m:
            out.append((m.group(1), m.group(2), m.group(3)))
    return out


def framing_notes(text):
    """The notes whose words read as framing or staging: [(id, shots text, words)]."""
    return [(i, sh, w) for i, sh, w in notes_in(text) if FRAMING.search(w)]


def shots_named(text, shots):
    """Which of the film's shots a notes cell names ('4a, 4c', '2-4', '9, 13', 'all'); [] when it names none."""
    low = (text or '').lower()
    if not low.strip() or re.search(r'\ball\b|whole film|every shot', low):
        return list(shots) if re.search(r'\ball\b|whole film|every shot', low) else []
    got = []
    for a, b in re.findall(r'\b([0-9]+[a-z]?)\s*[-–]\s*([0-9]+[a-z]?)\b', low):
        if a in shots and b in shots:
            got += shots[shots.index(a):shots.index(b) + 1]
    for tok in re.findall(r'[a-z0-9]+', low):
        if tok in shots and tok not in got:
            got.append(tok)
    return got


# ---------------------------------------------------------------------------------------------- the gate
def gate(film, want, shots, root=ROOT, now=None, notes_text=None):
    """Plain-words refusals for rendering `want` (shot names) of `film`, whose shots are `shots` (in order). now: the
    moment to judge at (a replay of an old film); notes_text: the film's notes (default notes/FILM.md)."""
    import rough
    now = now or time.time()
    boards = [b for b in rough.board_record(_name(film), root) if b['delivered'] <= now]
    rec = [r for r in record(film, root) if r[2] <= now]
    if notes_text is None:
        p = os.path.join(root, 'notes', f'{_name(film)}.md')
        notes_text = open(p).read() if os.path.exists(p) else ''
    held_notes = {r[3].get('note') for r in rec if r[0] == 'hold'}
    cleared = {r[1] for r in rec if r[0] == 'notframing'}
    flagged = [(i, shots_named(sh, shots) or list(shots), w) for i, sh, w in framing_notes(notes_text)
               if i not in held_notes and i not in cleared]
    out = []
    for n in want:
        seen = [b['delivered'] for b in boards if n in b['shots']]
        if not seen:
            out.append(f'shot {n} has never been on a shot board that reached Sam (rule 11: he sees every framing '
                       f'before it moves): python3 source/rough.py board {_name(film)} OUT.jpg --shots {n}, send it, '
                       f'then rough.py sent {_name(film)} OUT.jpg --delivered --board')
        holds = [r for r in rec if r[0] == 'hold' and r[1] == n]
        if holds:
            h = holds[-1]
            picks = [r for r in rec if r[0] == 'pick' and r[1] == n and r[2] >= h[2]]
            sheets = [r for r in rec if r[0] == 'options' and r[1] == n and r[2] >= h[2]]
            if not picks:
                out.append(f'shot {n} is held by note {h[3]["note"]} ("{h[3]["words"][:60]}"): '
                           + ('waiting for Sam\'s number on the framings sheet sent '
                              f'{time.strftime("%d %b %H:%M", time.localtime(sheets[-1][2]))}; then python3 '
                              f'source/staging.py pick {_name(film)} {n} N "his words"' if sheets else
                              f'send him 2-3 numbered framings first (python3 source/staging.py options '
                              f'{_name(film)} {n} OUT.jpg A.jpg B.jpg --script K "the camera line")'))
            elif picks[-1][3]['pick'] != 'go' and not [t for t in seen if t >= picks[-1][2]]:
                out.append(f'shot {n}: Sam picked {picks[-1][3]["pick"]}; draw it as built on the board before it '
                           f'moves (python3 source/rough.py board {_name(film)} OUT.jpg --shots {n}, send it, '
                           f'`sent --delivered --board`)')
        for i, on, w in flagged:
            if n in on:
                out.append(f'note {i} on shot {n} reads as framing ("{w[:60]}"): python3 source/staging.py restage '
                           f'{_name(film)} {",".join(on) if len(on) < 6 else n} --note {i} "{w[:40]}..." '
                           f'(or, if it is not about framing: staging.py notframing {_name(film)} {i} "why")')
    return out


def render_gate(film_mod, film, want):
    """film_engine.render's call for a clip: [] for films begun before the board, else gate()."""
    import rough
    if rough._before_rule(film_mod, _name(film), ROOT):
        return []
    shots = [n for n, a, b in getattr(film_mod, 'SHOTS', []) if float(b) > float(a)]
    return gate(film, [n for n in want if n in shots], shots)


# ---------------------------------------------------------------------------------------------- options sheet
def options_sheet(film, shot, out, images, script_k, script_line, labels=None):
    """2-3 framings side by side, each with a big number; option K carries the screenplay's camera line; the foot says
    what 0 means. Leaves OUT.jpg.json for `sent`."""
    from PIL import Image, ImageDraw, ImageFont
    if not 2 <= len(images) <= 3:
        raise SystemExit('NOT drawn: 2 or 3 framings (lesson staging-stills: 2-3 numbered framings)')
    if not 1 <= script_k <= len(images) or not script_line.strip():
        raise SystemExit('NOT drawn: --script K "line": one framing must follow the screenplay\'s camera line')
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)      # noqa: E731
    tw, th, gap = 432, 768, 24
    W = gap + len(images) * (tw + gap)
    sheet = Image.new('RGB', (W, th + 330), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    d.text((gap, 14), f'Shot {shot}: which framing? Reply with a number.', font=font(34), fill=(20, 20, 20))
    labels = labels or [''] * len(images)
    for i, f in enumerate(images):
        x = gap + i * (tw + gap)
        im = Image.open(f).convert('RGB')
        im.thumbnail((tw, th))
        sheet.paste(im, (x, 70))
        d.ellipse((x + 10, 80, x + 90, 160), fill=(255, 255, 255), outline=(20, 20, 20), width=4)
        d.text((x + 36, 92), str(i + 1), font=font(48), fill=(20, 20, 20))
        lab = (labels[i] if i < len(labels) else '') or ''
        if i + 1 == script_k:
            lab = (lab + '  ' if lab else '') + f'(the script: "{script_line}")'
        y = 70 + th + 10
        for k in range(0, min(len(lab), 4 * 34), 34):
            d.text((x, y), lab[k:k + 34], font=font(20), fill=(20, 20, 20))
            y += 26
    d.text((gap, th + 290), '0: none of these (say what instead)', font=font(24), fill=(90, 90, 90))
    sheet.save(out, quality=86)
    json.dump(dict(film=_name(film), shot=shot, n=len(images), script=script_k), open(out + '.json', 'w'))
    return out


# ---------------------------------------------------------------------------------------------- main
def _film_shots(film):
    import importlib
    try:
        m = importlib.import_module(film.replace('-', '_'))
        return m, [n for n, a, b in getattr(m, 'SHOTS', []) if float(b) > float(a)]
    except Exception:
        return None, []


def main(argv):
    if len(argv) < 2 or argv[0] not in ('restage', 'options', 'sent', 'pick', 'notframing', 'check'):
        print(__doc__.split('The gate')[0])
        return 2
    cmd, film, now = argv[0], argv[1], int(time.time())
    if cmd == 'restage':
        if '--note' not in argv or len(argv) < 6:
            print('NOT recorded: staging.py restage FILM SHOT[,SHOT] --note N "Sam\'s words"')
            return 1
        note = argv[argv.index('--note') + 1]
        words = ' '.join(a for i, a in enumerate(argv[3:], 3) if a != '--note' and argv[i - 1] != '--note')
        _, shots = _film_shots(film)
        named = argv[2].split(',')
        if shots and [s for s in named if s not in shots]:
            print(f'NOT recorded: no shot {[s for s in named if s not in shots]} in {film} ({", ".join(shots)})')
            return 1
        for s in named:
            _write(film, f'hold {s} {now} note={note} {words}')
        print(f'{film}: {", ".join(named)} held by note {note}: next, 2-3 numbered framings (staging.py options)')
        return 0
    if cmd == 'options':
        args, k, line, labels, i = [], None, '', None, 2
        while i < len(argv):                              # flags and their values taken out by place, not by value
            if argv[i] == '--script' and i + 2 < len(argv):
                k, line, i = int(argv[i + 1]), argv[i + 2], i + 3
            elif argv[i] == '--labels' and i + 1 < len(argv):
                labels, i = argv[i + 1].split('|'), i + 2
            else:
                args.append(argv[i])
                i += 1
        if k is None:
            print('NOT drawn: --script K "the screenplay\'s camera line" (one framing follows it word for word)')
            return 1
        shot, out, imgs = args[0], args[1], args[2:]
        options_sheet(film, shot, out, imgs, k, line, labels)
        print(f'{out}: {len(imgs)} framings of shot {shot}; after SendUserFile: python3 source/staging.py sent {film} '
              f'{out} --delivered')
        return 0
    if cmd == 'sent':
        if '--delivered' not in argv:
            print('NOT recorded: add --delivered once SendUserFile has delivered the sheet')
            return 1
        out = argv[2]
        if not os.path.exists(out + '.json'):
            print(f'NOT recorded: {out} has no note beside it: draw it with staging.py options')
            return 1
        b = json.load(open(out + '.json'))
        _write(film, f'options {b["shot"]} {now} {os.path.basename(out)} n={b["n"]}')
        print(f'{film}: framings sheet for shot {b["shot"]} recorded; ask Sam for a number, then staging.py pick')
        return 0
    if cmd == 'pick':
        shot, n, words = argv[2], argv[3], ' '.join(argv[4:])
        if not words.strip():
            print('NOT recorded: Sam\'s own words are needed with his number')
            return 1
        sheets = [r for r in record(film) if r[0] == 'options' and r[1] == shot]
        if n != 'go' and (not n.isdigit() or not sheets or int(n) > sheets[-1][3]['n']):
            print(f'NOT recorded: {n} is not a framing on the last sheet sent for shot {shot}'
                  + ('' if sheets else ' (no sheet sent: staging.py options, then sent)'))
            return 1
        _write(film, f'pick {shot} {now} {n} {words}')
        print(f'{film}: shot {shot}, Sam picked {n}. Build it, then draw it on the board: python3 source/rough.py '
              f'board {film} OUT.jpg --shots {shot}; send it; rough.py sent {film} OUT.jpg --delivered --board'
              if n != 'go' else f'{film}: shot {shot} released on Sam\'s words')
        return 0
    if cmd == 'notframing':
        if len(argv) < 4:
            print('NOT recorded: staging.py notframing FILM NOTE "why it is not about framing"')
            return 1
        _write(film, f'notframing {argv[2]} {now} {" ".join(argv[3:])}')
        print(f'{film}: note {argv[2]} marked as not about framing')
        return 0
    mod, shots = _film_shots(film)
    want = argv[2:] or shots
    faults = render_gate(mod, film, want) if mod else gate(film, want, shots)
    print('\n'.join(faults) if faults else f'{film}: no shot held (every framing seen by Sam)')
    return 1 if faults else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
