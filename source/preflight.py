#!/usr/bin/env python3
"""Pre-flight: catch problems before the animatic, not after the final render (lesson of The Patriots 2, which
took many renders because faults were found by eye, one round at a time).

Works on any film module that has frame_image(t) and SHOTS [(name, start, end)], plus optionally caption_at(t)
and BLACK_AT / DUR. It:
1. turns on the figure guard (every arm drawn is measured; see figure.py) and runs every module-level check,
   then the shared checks (housestyle: the template's style on; audit: collisions and pop-ins, from the film's
   scene(t), a FAULT if the film has none; clipcheck: solids, drawing order, teleports,
   contacts; hookcheck: the Hook Text clear of signs; musiccheck: song joins; linecheck: outlines; sizes: real
   sizes; landmarks: clothes against the body), each only if the film defines what it needs;
2. draws every 3rd frame small and quick, so any check inside the drawing code (overlaps, fingertips on the
   keyboard, feet on the floor, unreachable hands) fires now, with the time of the frame;
3. checks the captions: at most 700 px wide in at most 2 rows of 42 characters, on screen long enough to read
   (about 17 characters a second at most), never empty between pieces of one line;
4. checks shot lengths (over 8 s is flagged, so a long single shot is a choice, not an accident);
5. makes a contact sheet (one frame a second, safe-area guides drawn on) to look at once, instead of renders.
Before any of it, it REFUSES to run (rule 14) while the film's brief checklist (notes/NAME.md, "The brief as a
checklist") has a blank "done?" row, or before the composition sheet has been sent (a line "Composition sheet sent:
DATE, FILE" in the notes, rule 11); and it fails a film whose shot is missing anyone the brief puts in it (SHOT_CAST,
against the audit's roster). It prints a short summary; the full list goes to OUT_DIR/NAME-preflight.txt (rule 19).
The shared kit's checks (kitchecks.py, rule 13) run here on every film: facing on the drawing pass, marks, sounds,
and (inside the audit) hands on what they touch, props held, resting hands clear. handcheck.py (rule 41) probes
everyone drawn, on every frame: every arm ends in a visible hand. So do viewchecks.py's (rules S7, 16-18,
20): effect shapes, readability, direction across a cut, effects hidden behind figures, and on the drawing pass every
held prop turned through every view.

Usage:
    python3 preflight.py patriots2 OUT_DIR            before the animatic: stops at the first fault
    python3 preflight.py patriots2 OUT_DIR --audit    list every fault (for a finished film)
    ... --faults-named    the round's critique faults are named to Sam (rule 89): the animatic may go ahead
"""
import fnmatch
import hashlib
import importlib
import json
import os
import re
import sys
import traceback

from PIL import Image, ImageDraw, ImageFont

import burnham as B
import figure as F
import handcheck

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAFE = (60, 310, 900, 1500)
KINDS = ('people', 'rooms', 'voices', 'effects', 'props')   # rule 58: what a film can contain (the film's HAS)
SKIP_WHY = {   # check: (the kinds it needs, any of them)
    'plan and rooms (rules 1, 2, 12, 38)': ('rooms',),
    'collisions and pop-ins (rules 5, 6)': ('people', 'props'),
    'who is in each shot (rule 14)': ('people',),
    'script and mouths (rule 7)': ('voices',),
    'hands, facing, line work, clothes (rules 41, 13; the house style)': ('people',),
    'real sizes (props)': ('props',),
}
MAX_SHOT = 8.0


_FILM = None
_FPS = 12


_TURNED = set()                 # (per worker) the people and props already turned through every view


def _check_frame(i):
    import kitchecks
    import viewchecks
    film = _FILM
    t = i / _FPS
    shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')
    F.CONTEXT['where'] = f'{shot} {t:.2f}s'
    F.CONTEXT['t'] = t                              # the film's time, for kitchecks' cut and face checks (Job L)
    import turnhead
    n0, d0, p0 = len(F.LOG), len(kitchecks.DRAWN), len(kitchecks.POSES)
    s0, m0 = len(turnhead.SEEN), len(turnhead.MISSING)
    import waivers
    w0 = len(waivers.LOG)
    err = None
    handcheck.begin()
    try:
        film.frame_image(t)
    except Exception as e:
        err = (str(e), isinstance(e, ValueError), traceback.format_exc())
    hands = handcheck.end(t, F.CONTEXT['where'])    # rule 41: every arm ends in a visible hand
    turned = viewchecks.turn_faults(kitchecks.POSES[p0:], _TURNED)   # rule 20: every held prop through every view
    del kitchecks.POSES[p0:]
    heads = (sorted(set(turnhead.SEEN[s0:])), sorted(set(turnhead.MISSING[m0:])))   # Job I faces: turned heads drawn
    del turnhead.SEEN[s0:], turnhead.MISSING[m0:]
    looks = list(waivers.LOG[w0:])                  # rule 13's house look: who each front head was drawn on
    del waivers.LOG[w0:]
    return t, err, list(F.LOG[n0:]), list(kitchecks.DRAWN[d0:]), turned, hands, heads, looks


def _hands_frame(i):
    """Rule 41 on the frames the drawing pass skips: the hands are checked on every frame."""
    t = i / _FPS
    shot = next((s[0] for s in getattr(_FILM, 'SHOTS', []) if s[1] <= t < s[2]), '')
    F.CONTEXT['where'] = f'{shot} {t:.2f}s'
    n0 = len(F.LOG)
    handcheck.begin()
    try:
        _FILM.frame_image(t)
    except Exception:                               # the drawing pass reports drawing faults
        pass
    del F.LOG[n0:]
    return handcheck.end(t, F.CONTEXT['where'])


def _notes_file(name):
    return os.path.join(ROOT, 'notes', f'{name}.md')


def notes_path(film, name):
    """The film's notes; a finished film's are in notes/archive/ (2 Nov: every film before then is archived)."""
    path = getattr(film, 'NOTES', None) or _notes_file(getattr(film, 'NAME', name))
    old = os.path.join(os.path.dirname(path), 'archive', os.path.basename(path))
    return old if not os.path.exists(path) and os.path.exists(old) else path


def gates(film, name):
    """Rule 14: what stops pre-flight before it starts: a blank row in the brief checklist, no record of the
    composition sheet being sent; rule 75: no Hook Text plan (HOOK and KEEP_CLEAR). Returns the reasons (empty: go)."""
    path = notes_path(film, name)
    if not os.path.exists(path):
        return [f'no notes file ({os.path.relpath(path, ROOT)}): the brief checklist lives there (notes/_template.md)']
    text = open(path).read()
    out = []
    m = re.search(r'^## The brief as a checklist.*?$(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not m:
        out.append('the notes file has no "The brief as a checklist" section (notes/_template.md)')
    else:
        rows = [ln for ln in m.group(1).splitlines() if ln.strip().startswith('|')]
        blank, filled = [], 0
        for ln in rows[2:]:                                 # past the header and the |---| line
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) < 3 or not cells[1]:
                continue
            filled += 1
            if not cells[-1]:
                blank.append(f'{cells[0]} ({cells[1][:50]})')
        if not filled:
            out.append('the brief checklist is empty: copy every detail of the brief in, then tick each against the film')
        elif blank:
            out.append(f'the brief checklist has {len(blank)} blank "done?" row(s): ' + '; '.join(blank[:8]) +
                       (' ...' if len(blank) > 8 else '') + ' (tick each against the film, or say why not)')
    if not re.search(r'^\s*[-*]?\s*\**Composition sheet sent\**:\**[ \t]*[^\s(*]', text, re.M | re.I):   # not the (...)
        out.append('no record of the composition sheet being sent (rule 11): send Sam the 3-4 key shots, then add '
                   '"Composition sheet sent: DATE, FILE" to the notes file')
    import hookcheck
    out += hookcheck.plan_faults(film)                      # rule 75: the Hook Text planned at the first animatic
    return out


def gate_warnings(film, name, has):
    """Job J: by-hand rules turned into checks, printed (not yet refusing: Sam's numbers decide): rule 74 (an acting
    list row per line), rule 8 (risky moves rehearsed: a "Rehearsal clips sent:" line, or "none: why"), rule 61 (the
    film's code opens with its MAP and stays under about 1,000 lines a file)."""
    out = []
    path = notes_path(film, name)
    text = open(path).read() if os.path.exists(path) else ''
    if 'voices' in has:
        m = re.search(r'^##+ *(The )?acting list.*?$(.*?)(?=^## |\Z)', text, re.M | re.S | re.I)
        rows = [ln for ln in (m.group(2).splitlines() if m else []) if ln.strip().startswith('|')][2:]
        if not rows:
            out.append('no acting list in the notes (rule 74: one row per line; guides/satire.md "The acting list")')
    out += head_life_faults(film)
    if not re.search(r'^\s*[-*]?\s*\**Rehearsal clips sent\**:\**[ \t]*[^\s(*]', text, re.M | re.I):
        out.append('no "Rehearsal clips sent: DATE, FILE" (or "none: why") line in the notes (rule 8: the 3-4 riskiest '
                   'moves as 2-3 s clips before the rest)')
    src = getattr(film, '__file__', '') or ''
    if src.endswith('.py') and os.path.exists(src):
        lines = open(src).read().splitlines()
        if not any('MAP' in ln for ln in lines[:40]):
            out.append(f'{os.path.basename(src)} has no MAP in its first lines (rule 61; python3 source/codemap.py)')
        if len(lines) > 1000:
            out.append(f'{os.path.basename(src)} is {len(lines)} lines: split it, one file per group of shots (rule 61)')
    return out


def head_life_faults(film):
    """Rule 74 (Sam, 11 Nov: Remakes' KG and Link talked with still heads although Job K's head acting was in the
    guide): every speaker in LINES has head acting from the voice, HEAD_LIFE = {who: headlife.HeadLife} (or
    CAST[who]['head_life']), and it really moves (its tilt changes at least once inside every line of theirs)."""
    out = []
    hl = dict(getattr(film, 'HEAD_LIFE', {}) or {})
    for who, sp in (getattr(film, 'CAST', {}) or {}).items():
        if isinstance(sp, dict) and sp.get('head_life') is not None:
            hl.setdefault(who, sp['head_life'])
    for ln in getattr(film, 'LINES', []) or []:
        who = ln.get('who') if isinstance(ln, dict) else None
        if who is None:
            continue
        life = hl.get(who)
        if life is None:
            out.append(f'HEAD LIFE: {who} speaks (line {ln.get("n", "?")}) with no head acting (rule 74: '
                       f'HEAD_LIFE[{who!r}] = headlife.HeadLife from the voice, used in the drawing)')
            hl[who] = False
            continue
        if life is False:
            continue
        ts = [ln['start'] + k / 12 for k in range(max(1, int((ln['end'] - ln['start']) * 12)))]
        if len({round(life.at_time(t)[0], 1) for t in ts}) < 2 and max(life.at_time(t)[1] for t in ts) == 0:
            out.append(f'HEAD LIFE: {who}\'s head is still all through line {ln.get("n", "?")} (rule 74)')
    return out


def cast_faults(film, roster):
    """Rule 14 / CLAUDE.md (25 Oct): every shot has everyone the brief puts in it, on screen at some point (SHOT_CAST:
    {shot: [name or pattern]}, against the audit's roster of who is on screen)."""
    want = getattr(film, 'SHOT_CAST', None)
    if want is None:
        return ['SHOT CAST: SHOT_CAST missing: list who the brief puts in each shot ({shot: [names]}); pre-flight '
                'checks each is on screen there (CLAUDE.md: no animatic while a shot is missing anyone)']
    out = []
    for shot, names in want.items():
        seen = roster.get(shot, set())
        for n in names:
            if not any(fnmatch.fnmatchcase(x, n) for x in seen):
                out.append(f'SHOT CAST: shot {shot}: {n} is never on screen (the brief puts them in it; SHOT_CAST)')
    return out


def _sheet_tile(k):
    t = k + 0.5
    try:
        im = _FILM.frame_image(t).convert('RGB').resize((B.W, B.H))
    except Exception:                           # a drawing the figure guard stopped: a grey tile (the pass reports it)
        im = Image.new('RGB', (B.W, B.H), (90, 90, 90))
    d = ImageDraw.Draw(im, 'RGBA')
    for box in ((0, 0, 1080, SAFE[1]), (0, SAFE[3], 1080, 1920), (SAFE[2], 864, 1080, SAFE[3])):
        d.rectangle(box, fill=(255, 0, 0, 60))
    d.rectangle(SAFE, outline=(0, 255, 0, 255), width=5)
    d.text((20, 1840), f'{t:.1f} s', font=ImageFont.truetype(B.SANS, 60), fill=(255, 255, 255))
    return im.resize((216, 384))


# --- incremental frame passes (rule 59 as amended 3 Nov, Sam: a small fix should not re-check the whole film) --------
# Every frame is fingerprinted (its picture at the check size). A later run redraws and re-checks only the frames
# whose fingerprint changed (and a few round them), and only the bodies whose shots they fall in. It falls back to the
# full pass whenever it cannot be sure: no earlier run, an earlier run that found a frame-level fault, any change to the
# check code, any change to the film's allow-lists and settings, or a change in length. The text and sound checks
# (script, mouths, subtitles, plan, shared checks) always run in full: they take seconds. `--full` forces the full pass.
CHECK_FILES = ('preflight.py', 'handcheck.py', 'posecheck.py', 'lying.py', 'audit.py', 'clipcheck.py', 'kitchecks.py',
               'filmkit.py', 'figure.py', 'viewchecks.py', 'housestyle.py', 'plan.py', 'benchmark.py', 'sets.py', 'linecheck.py', 'landmarks.py',
               'hookcheck.py', 'musiccheck.py', 'sizes.py', 'voices.py', 'report.py', 'mounts.py', 'collisions.py',
               'waivers.py', 'camfeel.py', 'views.py')


def _checks_hash():
    h = hashlib.sha1()
    for f in CHECK_FILES:
        path = os.path.join(ROOT, 'source', f)
        if os.path.exists(path):
            h.update(f.encode())
            with open(path, 'rb') as fh:
                h.update(fh.read())
    return h.hexdigest()


def _plain(v):
    if isinstance(v, (set, frozenset)):
        return sorted(map(repr, v))
    if isinstance(v, dict):
        return {repr(k): _plain(x) for k, x in sorted(v.items(), key=lambda kv: repr(kv[0]))}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    return v


def _config_hash(film):
    """The film's own settings and allow-lists (HANDS_OK, ALLOWED, TOUCHES, SHOTS...): a change in any of them can
    change what a check says about a frame that did not itself change. (Pictures cover the rest; one-letter names and
    the heavy line, mouth and blink tables are left out: pictures and the text checks cover them.)"""
    h = hashlib.sha1()
    for k in sorted(dir(film)):
        if k.isupper() and len(k) > 1 and not k.startswith('_') and k not in ('LINES', 'TRACK', 'BLINKS'):
            v = getattr(film, k)
            if isinstance(v, (list, tuple, dict, set, frozenset, str, int, float, bool, type(None))):
                h.update(k.encode())
                h.update(re.sub(r' at 0x[0-9a-fA-F]+', '', repr(_plain(v))).encode()[:400000])   # (no memory addresses)
    return h.hexdigest()


def _frame_hash(i):
    B.SS = 1
    t = i / _FPS
    try:
        pic = _FILM.picture(t) if hasattr(_FILM, 'picture') else _FILM.frame_image(t)
    except Exception as e:                      # the figure guard stops a bad drawing: that frame is "changed" for good,
        return 'ERROR ' + str(e)[:60]           # and the normal pass below draws it again and reports the fault
    return hashlib.md5(pic.tobytes()).hexdigest()[:16]


def _fault_frame(text, fps):
    """The frame a fault names ('4.83s', '  4.83 s:'), or None when it names no time."""
    import re
    m = re.search(r'(\d+(?:\.\d+)?) ?s\b', text)
    return int(round(float(m.group(1)) * fps)) if m else None


def _frames_path(name):
    import film_engine
    return os.path.join(film_engine.PASSES, f'{name}-frames.json')


def _in_child(fn, *args):
    """Run fn(*args) in a forked child and return its result (a list of fault strings): whatever libraries it loads
    (GNU OpenMP) stay out of this process, which later forks the drawing workers. Forked, not pickled: the film is a
    module."""
    import pickle
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        code = 0
        try:
            os.close(r)
            out = ('ok', fn(*args))
        except BaseException:
            out = ('err', traceback.format_exc())
            code = 1
        with os.fdopen(w, 'wb') as fh:
            pickle.dump(out, fh)
        os._exit(code)
    os.close(w)
    with os.fdopen(r, 'rb') as fh:
        data = fh.read()
    os.waitpid(pid, 0)
    kind, val = pickle.loads(data) if data else ('err', 'the child produced nothing')
    if kind == 'err':
        raise RuntimeError('check failed in its child process:\n' + str(val))
    return val


def _text_only(film, problems, end, fps):
    """`preflight.py NAME OUT --text` (film-quality-rules 67): after the shared checks, only the subtitles (rows, reading
    speed) and shot lengths; no frame is drawn. Fix text faults here until it is clean, then run the full pre-flight once."""
    if hasattr(film, 'caption_at'):             # rule 62 at the delivered speed (rule 70: 1.1x), in the kit's style
        import subtitles as SUB
        problems += SUB.readable_faults(film.caption_at, end, fps)
    for s in getattr(film, 'SHOTS', []):
        if s[2] - s[1] > MAX_SHOT:
            problems.append(f'shot {s[0]} ({s[1]:.1f}-{s[2]:.1f} s) is {s[2] - s[1]:.1f} s long (over {MAX_SHOT:.0f} s)')
    print('quick check (--text):', 'clean' if not problems else f'{len(problems)} fault(s)')
    for x in problems:
        print(' -', x)
    print('(no pass stamp: the render still needs the full pre-flight)')


def main():
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    named_file = os.path.join(out, f'{name}-named.txt')   # Job C 1: faults named not fixed (ARM_FOLD_NAMED), from
    open(named_file, 'w').close()                         # every forked child too
    os.environ['NAMED_FAULTS_FILE'] = named_file
    audit = '--audit' in sys.argv              # list every fault instead of stopping at the first
    if audit:
        F._ALLOW.append('audit of a finished film')
    film = importlib.import_module(name)        # module-level checks (set plans, overlaps) run on import
    has = set(getattr(film, 'HAS', KINDS))      # rule 58: only the checks for what the film contains
    unknown = has - set(KINDS)
    if unknown:
        sys.exit(f'preflight: HAS has {sorted(unknown)}; use only {KINDS}')
    runs = {c: any(k in has for k in need) for c, need in SKIP_WHY.items()}
    skipped = [c for c, on in runs.items() if not on]
    if skipped:
        print('skipped (the film has no ' + ', '.join(k for k in KINDS if k not in has) + '; HAS): ' + '; '.join(skipped))
    stop = gates(film, name)   # rule 14: refuse while the brief or the sheet is not done
    import waivers                              # rule 13: every exception has a written reason in the notes
    wf, wlist = waivers.gate_faults(film)
    print(f'exceptions: {len(wlist)}' + (' (every one in the report file)' if wlist else ''))
    stop += wf
    warn = gate_warnings(film, name, has)      # Job J: rules 8, 61, 74
    path = notes_path(film, name)
    new_template = os.path.exists(path) and 'KNOWN (where) or NEW' in open(path).read()   # started from 10 Nov's template
    for x in warn:
        if new_template and ('rule 74' in x or 'rule 8:' in x):
            stop.append(x)                                           # Sam, 10 Nov (Job J Q4): refuse on new films
        else:
            print('WARNING:', x)
    if stop and not audit:
        print('pre-flight REFUSES to run (guides/film-quality-rules.md, rule 14):')
        for x in stop:
            print(' -', x)
        sys.exit(2)
    F.guard(B)
    import kitchecks
    kitchecks.install()                         # every views.py person drawn is logged for the facing check
    import posecheck
    posecheck.install()                         # rule 42: named poses against the gallery's avoid views; lying bodies
    handcheck.install()                         # rule 41: every views.py person drawn is probed for hands
    waivers.install()                           # rule 13: the house look (who each front head is drawn on)
    if hasattr(film, 'checks'):                 # the film's own plan checks (overlaps, outfits...)
        film.checks()
    shared = ['gate: ' + x for x in stop]       # the shared checks every film gets (Sam, 18 Oct: catch it before I do)
    B.SS = 1
    import audit as collisions, clipcheck, hookcheck, linecheck, musiccheck, sizes, landmarks, housestyle
    import plan, benchmark, sets
    people, rooms = 'people' in has, 'rooms' in has
    shared += housestyle.faults(film, B, has)   # the template's house style is on, and each check has its inputs
    if rooms:
        shared += plan.faults(film)         # rule 1: one plan of the world in metres, joined up, a camera per shot
    shared += benchmark.faults(film)        # rule 3: each place benchmarked against its references, all decided
    if rooms:
        shared += sets.solids_faults(film)      # rule 5: what the set's solids need (door angles, reasons)
        if getattr(film, 'PLAN', None) is not None and hasattr(film, 'cam_for'):
            shared += sets.portal_faults(film)  # rule 2: every opening shows the space beyond, never a flat colour
    roster = None
    if hasattr(film, 'scene'):
        shared += collisions.check(film)        # rules 5, 6, 12, 13: nothing passes through anything; nothing pops in;
        roster = collisions.LAST_ROSTER         # hands on what they touch, props held, resting hands clear
    if any(hasattr(film, a) for a in ('solids', 'layers', 'IN_SHOT', 'draw_order')):
        shared += clipcheck.run(film)           # passes through, teleports, drawing order, flips (rule 57)
    if runs['collisions and pop-ins (rules 5, 6)'] and not any(hasattr(film, a) for a in ('scene', 'solids')):
        shared.append('the collision and pop-in tests did not run: the film has no scene(t) (audit.py; '   # never
                      'rules 5 and 6; a film with no people or props says so in HAS)')               # in silence
    if 'effects' in has and getattr(film, 'EFFECTS', None) and not any(hasattr(film, a) for a in ('draw_order', 'layers')):
        shared.append('rule 57: the film has effects but no draw_order(t) (names back to front), so nothing checks '
                      'that a thing never flips from in front to behind mid-shot')
    if people:
        shared += cast_faults(film, roster or {})   # rule 14: no shot missing anyone the brief puts in it
    if hasattr(film, 'LINES') and 'voices' in has:   # rule 7: script v recordings v subtitles, and the mouths drawn
        import voices
        shared += voices.check(film)
    import viewchecks                       # rules S7, 16-18: effect shapes, readability, direction across a cut,
    shared += viewchecks.faults(film)       # effects hidden behind figures (rule 20 runs on the drawing pass)
    import film_engine
    shared += film_engine.look_faults(film)   # house look (S7): the engine's alone, so once; drawings 12 a second
    if 'mounts' in sys.modules:                 # riding (Sam, 25 Oct): a film with a mount gets the mount checks
        import mounts
        shared += mounts.check()
    shared += kitchecks.marks(film)             # rule 13: marks on real surfaces
    shared += kitchecks.sounds(film)            # rule 13: a sound tied to a thing only with it in frame, once a hit
    shared += hookcheck.faults(film)            # the Hook Text clear of the signs and readouts listed
    import setcheck
    shared += setcheck.film_faults(film)        # rule 13: figures moving through the set, against its solid things
    shared += musiccheck.faults(film)           # no beat skipped or doubled where pieces of a song are joined
    import camfeel                              # rule 72: a fast or sudden camera move the acting list doesn't mark
    shared += camfeel.faults(film)              # sharp (a row in the exceptions excuses a shot: 'camera feel')
    if people:                                  # (in a throwaway child: linecheck loads GNU OpenMP, and forking the
        shared += _in_child(linecheck.faults, film)   # drawing workers from a process that has used it freezes them
        shared += _in_child(landmarks.faults, film)   # after about 330 frames: the Elder Swindon hang, 8 Nov)
    if 'props' in has:
        shared += _in_child(sizes.faults, film)  # props and set pieces at their real size
    print('shared checks:', 'clean' if not shared else f'{len(shared)} fault(s)')
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    if not end:                                 # a film without an end time would pass having checked nothing
        sys.exit('preflight: the film module needs BLACK_AT or DUR (its length in seconds)')
    fps = getattr(film, 'FPS', 12)
    problems = list(shared)
    B.SS = 1
    if '--text' in sys.argv:                    # rule 67: the quick check, in seconds: the plan, script, mouths, subtitles
        _text_only(film, problems, end, fps)    # and shot lengths; no picture passes, no sheet, and never a pass stamp
        sys.exit(1 if problems else 0)
    # 2. every 3rd frame, small: the checks inside the drawing code (all processor cores)
    global _FILM, _FPS
    _FILM, _FPS = film, fps
    drawn = []
    from multiprocessing import Pool
    n_frames = int(end * fps)
    n_text = len(problems)                      # faults after this are the frame-level ones (the stamp's "clean")
    prev, incremental, changed = None, False, list(range(n_frames))
    stamp_ok = not audit and '--full' not in sys.argv
    with Pool(os.cpu_count()) as pool:
        hashes = None
        if stamp_ok:                            # fingerprint every frame: a plain picture, a quarter of a probed one
            hashes = pool.map(_frame_hash, range(n_frames), chunksize=4)
            try:
                with open(_frames_path(name)) as fh:
                    prev = json.load(fh)
            except (OSError, ValueError):
                prev = None
            chk, cfg = _checks_hash(), _config_hash(film)
            # A run that found frame-level faults is still a base to compare with (Sam, 12 Nov: a one-fault fix
            # must not mean a full re-run): its faults are kept, each with its time, and carried forward unless
            # their frame is re-checked. A fault with no time in it cannot be carried, so that case runs in full.
            carry = prev.get('faults') if prev and not prev.get('clean') else []
            carry_ok = carry is not None and all(_fault_frame(x, fps) is not None for x in carry)
            incremental = bool(prev and (prev.get('clean') or carry_ok) and prev.get('checks') == chk
                               and prev.get('config') == cfg and prev.get('n') == n_frames and prev.get('fps') == fps)
            if incremental:
                changed = [i for i in range(n_frames) if hashes[i] != prev['hashes'][i]]
                near = {j for i in changed for j in range(max(0, i - 3), min(n_frames, i + 4))}
                for x in (carry or []):             # faults from the last run whose frame was not re-checked
                    if _fault_frame(x, fps) not in near and x not in problems:
                        problems.append(x)
                print(f'incremental pre-flight: {len(changed)} of {n_frames} frames changed since the last clean run; '
                      f're-checking {len(near)} (the rest were clean then and are unchanged). --full re-checks all.')
            elif prev:
                why = ('the last run found a fault with no time in it' if not prev.get('clean') and not carry_ok else
                       'the check code changed' if prev.get('checks') != chk else
                       'the film\'s settings or allow-lists changed' if prev.get('config') != cfg else
                       'the length changed')
                print(f'full pre-flight (not incremental: {why})')
            else:
                print('full pre-flight (no earlier clean run to compare with)')
        todo = {j for i in changed for j in range(max(0, i - 3), min(n_frames, i + 4))} if incremental else None
        hands, looks = [], []
        first = [i for i in range(0, n_frames, 3) if todo is None or i in todo]
        heads_seen, heads_missing = set(), {}
        for t, err, log, dr, turned, hs, (seen, miss), lk in pool.imap(_check_frame, first, chunksize=4):
            looks += lk
            heads_seen.update(seen)
            for who, view in miss:
                heads_missing.setdefault((who, view), t)
            F.LOG.extend(log)
            drawn += dr
            hands += hs
            problems += [x for x in turned if x not in problems]
            if err:
                problems.append(f'{t:6.2f} s: {err[0]}')
                if not err[1]:
                    print(err[2])
        rest = [i for i in range(n_frames) if i % 3 and (todo is None or i in todo)]
        for hs in pool.imap(_hands_frame, rest, chunksize=4):   # the hands on every frame (rule 41)
            hands += hs
    if people:
        problems += [row[1] for row in handcheck.summary(film, hands, fps)]
    heads_seen = locals().get('heads_seen', set())
    heads_missing = locals().get('heads_missing', {})
    for (who, view), t in sorted(heads_missing.items()):   # Job I faces: built only when a shot needs it
        problems.append(f'{t:6.2f} s: {who} is drawn turned ({view}) with the old generic head: their front design is '
                        'measured, so give them a turned head (turnhead.register, as the Ad-Vanced Notice cast does)')
    if heads_seen or heads_missing:
        print('turned heads the shots need:', ', '.join(f'{w} {v}' for w, v in sorted(heads_seen | set(heads_missing))))
    F.CONTEXT['where'] = ''
    if people:
        problems += kitchecks.facing(drawn)     # rule 13: heads never turned past the body; nothing held over a back
        problems += kitchecks.copies(film, drawn)   # Job K: no group drawn from one copy
        problems += kitchecks.rests(film, drawn)   # rule 78: resting forearms and elbows never below their surface
        problems += kitchecks.cut_rests(film, drawn)   # rule 72: no pose drops back to rest just before a cut
        table = waivers.rows(open(path).read() if os.path.exists(path) else '')
        problems += waivers.look_faults(locals().get('looks', []), table)   # rule 13: everyone in the house look
        problems += waivers.lap_faults(drawn, table)   # rule 80: seated front on shows knees and lap
        if not incremental:                     # (a re-check that redrew only some frames can't say who is unseen)
            problems += waivers.unseen_faults(film, drawn, table)   # rule 13: no one silently outside the checks
        _faces = kitchecks.faces(film, drawn, ask=new_template)   # rule 50: each famous person's face 240 px tall once
        if incremental:                         # a re-check that did not redraw them cannot say they were "never drawn"
            _faces = [x for x in _faces if 'never found drawn' not in x]
        problems += _faces
    if hasattr(film, 'audits'):               # the film's general body / movement / marks audit (filmkit.py)
        import filmkit
        if incremental:                         # only the bodies in shots that hold a changed frame (a second round)
            filmkit.ONLY_FRAMES = {j for i in changed for j in range(max(0, i - 12), min(n_frames, i + 13))}
        try:
            problems += film.audits()
        finally:
            filmkit.ONLY_FRAMES = None
    if stamp_ok and hashes is not None:         # the fingerprints for the next run; "clean" = no frame-level fault
        os.makedirs(os.path.dirname(_frames_path(name)), exist_ok=True)
        with open(_frames_path(name), 'w') as fh:
            json.dump({'checks': _checks_hash(), 'config': _config_hash(film), 'n': n_frames, 'fps': fps,
                       'hashes': hashes, 'clean': len(problems) == n_text,
                       'faults': problems[n_text:]}, fh)
    # 3. captions
    if hasattr(film, 'caption_at'):             # rule 62 at the delivered speed (rule 70: 1.1x), in the kit's style
        import subtitles as SUB
        problems += SUB.readable_faults(film.caption_at, end, fps)
    # 4. shot lengths
    for s in getattr(film, 'SHOTS', []):
        if s[2] - s[1] > MAX_SHOT:
            problems.append(f'shot {s[0]} ({s[1]:.1f}-{s[2]:.1f} s) is {s[2] - s[1]:.1f} s long (over {MAX_SHOT:.0f} s: '
                            f'fine only if chosen, e.g. an unbroken speech)')
    # 5. contact sheet with the safe area drawn on
    logged = len(F.LOG)                         # the sheet's frames repeat ones already checked
    with Pool(os.cpu_count()) as pool:
        tiles = pool.map(_sheet_tile, range(int(end)))
    cols = 5                                    # 1080 px wide: one look, not a wall of pixels
    sheet = Image.new('RGB', (cols * 216, ((len(tiles) + cols - 1) // cols) * 384), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
    import turnhead                             # Job I faces: the turnaround of each (person, view) the shots need
    try:
        turn = turnhead.turnaround(sorted(heads_seen | set(heads_missing)))
    except KeyError as e:                       # 11 Nov (Blessed): a person with no turnaround entry crashed the run
        turn = None                             # before it wrote its stamp; the sheet is only a picture, the checks stand
        problems.append(f'turnaround sheet skipped: a person it draws has no {e} (film has no PEOPLE entry)')
    if turn is not None:
        turn.thumbnail((sheet.width, 10 ** 5))
        both = Image.new('RGB', (sheet.width, sheet.height + turn.height), (20, 20, 20))
        both.paste(sheet, (0, 0))
        both.paste(turn, (0, sheet.height))
        sheet = both
    sheet.save(os.path.join(out, f'{name}-preflight.jpg'), quality=85)
    del F.LOG[logged:]
    import contextlib
    import io
    import report                               # rule 19: a short summary; every fault in the file
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):       # the figure guard's log (what it allowed, how often): the file only
        F.report()
    log = buf.getvalue().splitlines()
    if not audit:                                # rule 89: the fresh-eye critique of this round, from the ledger
        import critique
        ok, line = critique.status(name)
        print(line)
        if not ok and '--faults-named' not in sys.argv:
            problems.append(f'{line}: pre-flight refuses the animatic (rule 89) until the round\'s last critique pass '
                            'is clean, or its faults are named to Sam (then add --faults-named)')
    checks = []                                  # Job C 1: a fault caught is fixed or told, never waved through
    named = list(dict.fromkeys(x.strip() for x in open(named_file) if x.strip()))
    if named:
        checks.append(f'{len(named)} fault(s) named, not fixed: ' + '; '.join(named[:3])
                      + (f' (+{len(named) - 3} more in {named_file})' if len(named) > 3 else ''))
    if not audit:
        cl = critique.checks_line(name)
        if cl and ('--faults-named' in sys.argv or ok):
            checks.append(cl[len('Checks: '):])
    if checks:
        print('Checks: ' + ' | '.join(checks) + '   <- put this line in Sam\'s message')
    notes = (['The figure guard (allowed drawings, how often):'] + log) if log else []
    notes += (['The film\'s exceptions (rule 13; reasons in the notes\' "## Exceptions"):'] + wlist) if wlist else []
    report.summarise(f'pre-flight ({name})', problems, os.path.join(out, f'{name}-preflight.txt'), notes=notes)
    print('contact sheet:', os.path.join(out, f'{name}-preflight.jpg'))
    if not audit:
        import film_engine                      # rule 59: the render checks this stamp before an animatic or final
        film_engine.write_pass(name, len(problems))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
