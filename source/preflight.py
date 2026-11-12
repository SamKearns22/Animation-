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
Honest (system audit, 12 Nov): every check that does not run (left out by HAS, never set up, or switched off) is a
"NOT RUN" fault at the top of the list; HAS is checked against what the film gives and draws; --audit counts the
figure guard's stops; the summary never says "clean" while a check is off (only CHECKS_OFF with Sam's yes and a date
lets one stay off, and it is still listed first); checktests.py proves each check catches a broken film.
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

# --- the honest checker (system audit, 12 Nov; rule 59) -------------------------------------------------------------
# Every check pre-flight knows of, the kinds of film it is for (rule 58's HAS, any of them), and what the film must
# give for it to run. A check that does not run is never silent: it is a fault at the top of the list ("NOT RUN"),
# whether the film's HAS left it out, the film never set it up, or it was switched off; the summary never says
# "clean" while one is off. The only way past one is CHECKS_OFF = {key: 'Sam, DATE, note N: "his words"'} (Sam's yes, found in the notes,
# rule 59), and even those are listed at the top of every run. claim_faults() checks HAS itself: a film that says it
# has no people (or rooms, voices, props, effects) but gives them, or draws them, is a fault however it is set.
CHECKS = {   # key: (what it checks, the kinds it is for, what the film gives: names, any of them)
    'rooms': ('the plan, the rooms and the sets\' solids (rules 1, 2, 5, 12, 38)', ('rooms',), ('PLAN',)),
    'portals': ('every opening shows the space beyond (rule 2)', ('rooms',), ('cam_for',)),
    'collisions': ('collisions and pop-ins (rules 5, 6)', ('people', 'props'), ('scene', 'solids')),
    'clip': ('passes through, teleports, drawing order (rule 57)', ('people', 'props'),
             ('solids', 'layers', 'IN_SHOT', 'draw_order')),
    'set feet': ('people moving through the set against its solid things (rule 13)', ('people+rooms',),
                 ('SET_FEET',)),
    'shot cast': ('who is in each shot (rule 14)', ('people',), ('SHOT_CAST',)),
    'hands': ('hands, facing, poses, rests, copies and cut rests on the drawing pass (rules 13, 41, 72)', ('people',),
              ()),
    'body audit': ('each body alone: in pieces, popping, stretching, frozen (the general audit)', ('people',),
                   ('audits',)),
    'line work': ('every shape outlined, one weight', ('people',), ('LINE_SUBJECTS',)),
    'clothes': ('clothes against the body (skirts from the waist, jackets to the hips)', ('people',), ('OUTFIT',)),
    'famous faces': ('each famous face 240 px tall once (rule 50)', ('people',), ('FAMOUS',)),
    'script and mouths': ('script v recordings v subtitles, and the mouths drawn (rule 7)', ('voices',), ('LINES',)),
    'captions': ('subtitles readable: rows, width, reading speed (rule 62)', ('voices',), ('caption_at',)),
    'sizes': ('props and set pieces at their real size', ('props',), ('PROP_SIZES',)),
    'effect order': ('an effect never flips from in front to behind mid-shot (rule 57)', ('effects',),
                     ('draw_order', 'layers')),
    'shot lengths': ('shots over 8 s flagged; the shot named at every fault', ('*',), ('SHOTS',)),
}
_DATE = r'\b\d{1,2} (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b'


def _gives(film, name):
    v = getattr(film, name, None)
    if v is None:
        return False
    if name == 'LINES':                         # LINES = [] is "no lines": the script check has nothing to check
        return bool(v)
    return True


def _notes_text(film):
    """The film's notes and its archived notes, as one text (empty if it has none)."""
    path = notes_path(film, (getattr(film, '__name__', '') or '').split('.')[-1])
    old = os.path.join(os.path.dirname(path), 'archive', os.path.basename(path))
    return '\n'.join(open(p).read() for p in dict.fromkeys((path, old)) if os.path.exists(p))


def _yes_unfound(film, reason):
    """Audit item 2 (Sam, 12 Nov): a check is off only on Sam's yes, and the yes is traceable. The CHECKS_OFF reason
    quotes his words ("...", at least 3 words) and names the note or message they came in; those words must be found
    in the film's notes (a chat cannot write "Sam, 12 Nov: yes" into the code by itself). '' if found, else why not."""
    quotes = [q for q in re.findall(r'["\u201c]([^"\u201d]+)["\u201d]', reason) if len(q.split()) >= 3]
    if not quotes or not re.search(r'\b(note|message|notes)\b', reason, re.I):
        return 'it must quote Sam\'s words ("...") and name the note or message they came in'
    norm = lambda x: re.sub(r'\s+', ' ', re.sub(r'[*_`>|]', ' ', x)).strip().lower()
    text = norm(_notes_text(film))
    missing = [q for q in quotes if norm(q) not in text]
    return f'Sam\'s words "{missing[0]}" are not in the film\'s notes' if missing else ''


def coverage(film, has):
    """The checks that will not run on this film: [(key, how, why)], how = 'left out by HAS', 'not set up' or 'off
    with Sam's yes'. Read from the film alone (nothing drawn), so --text shows it too."""
    off = dict(getattr(film, 'CHECKS_OFF', {}) or {})
    out = []
    for key, (what, kinds, gives) in CHECKS.items():
        if kinds == ('*',):
            wanted = True
        elif kinds == ('people+rooms',):
            wanted = 'people' in has and 'rooms' in has
        else:
            wanted = any(k in has for k in kinds)
        if key == 'set feet' and wanted and getattr(film, 'SET_FEET', None) is None:
            how, why = 'not set up', 'the film has people in rooms but no SET_FEET, movers(t), SET_CAM and MOVE_SPAN'
        elif key == 'effect order' and not getattr(film, 'EFFECTS', None):
            continue                            # (no EFFECTS listed: nothing to order; claim_faults asks if it lists any)
        elif not wanted:
            need = ' and '.join(kinds[0].split('+')) if kinds == ('people+rooms',) else ' or '.join(kinds)
            how, why = 'left out by HAS', f'HAS says the film has no {need}'
        elif gives and not any(_gives(film, g) for g in gives):
            how, why = 'not set up', 'the film has no ' + ' or '.join(gives)
        else:
            continue
        if key in off:
            reason = str(off[key])
            if re.search(r'\bSam\b', reason) and re.search(_DATE, reason, re.I) and not _yes_unfound(film, reason):
                how, why = "off with Sam's yes", reason
        out.append((key, how, why))
    for key in off:
        if key not in CHECKS:
            out.append((key, 'not set up', f'CHECKS_OFF names {key!r}, which is not a check (keys: '
                                           + ', '.join(CHECKS) + ')'))
    return out


def coverage_lines(film, rows):
    """(faults, offs): one line per check that will not run. A check off without Sam's yes (a CHECKS_OFF entry with
    no 'Sam' and a date) is a fault like any other."""
    off = dict(getattr(film, 'CHECKS_OFF', {}) or {})
    faults, offs = [], []
    for key, how, why in rows:
        what = CHECKS[key][0] if key in CHECKS else key
        if how == "off with Sam's yes":
            offs.append(f'OFF (Sam\'s yes): {key}: {what}: {why}')
            continue
        tail = (f' (CHECKS_OFF[{key!r}] is not a yes Sam can be traced to: it needs Sam, the date, the note or '
                f'message, and his words in quotes, found in the film\'s notes; '
                f'{_yes_unfound(film, str(off[key])) or "no Sam or date"}: {off[key]!r})' if key in off else
                ': set it up, or ask Sam and record his yes in CHECKS_OFF (rule 59)')
        faults.append(f'NOT RUN: {key} ({how}): {what}: {why}{tail}')
    return faults, offs


def claim_faults(film, has, drawn_names=()):
    """What the film says it contains (HAS) against what it gives and draws (system audit, 12 Nov: Remakes said 'no
    people, no rooms' with a cast and painted sets, and five checks never ran). A fault for each kind it leaves out
    but has; a yes in CHECKS_OFF does not excuse it (Sam's yes was for a film without them)."""
    out = []
    plan = getattr(film, 'PLAN', None) or {}
    rooms_in_plan = plan.get('ROOMS') if isinstance(plan, dict) else getattr(plan, 'rooms', None)
    people_in_plan = plan.get('PEOPLE') if isinstance(plan, dict) else getattr(plan, 'people', None)
    base = (getattr(film, '__name__', '') or '').split('.')[-1]
    set_mods = sorted(n for n in sys.modules if n.startswith(base + '_') and
                      re.search(r'_(sets?|rooms?|office|interior|house|studio)$', n)) if base else []
    cast = sorted({n for names in (getattr(film, 'SHOT_CAST', None) or {}).values() for n in names})
    famous = list(getattr(film, 'FAMOUS', None) or [])
    drawn_names = sorted(set(drawn_names))
    evidence = {
        'people': ([f'SHOT_CAST puts {", ".join(cast[:4])} on screen'] if cast else []) +
                  ([f'FAMOUS lists {", ".join(famous[:3])}'] if famous else []) +
                  (['the plan has PEOPLE'] if people_in_plan else []) +
                  ([f'the drawing pass drew {", ".join(drawn_names[:4])}'] if drawn_names else []),
        'rooms': (['the plan has ROOMS'] if rooms_in_plan else []) +
                 ([f'it draws sets from {", ".join(m + ".py" for m in set_mods)}'] if set_mods else []),
        'voices': ['LINES has the script\'s lines'] if getattr(film, 'LINES', None) else [],
        'props': ['PROP_SIZES lists props'] if getattr(film, 'PROP_SIZES', None) else [],
        'effects': ['EFFECTS lists effects'] if getattr(film, 'EFFECTS', None) else [],
    }
    for kind, why in evidence.items():
        if kind not in has and why:
            out.append(f'HAS: the film says it has no {kind}, but ' + '; '.join(why) + f': add {kind!r} to HAS and '
                       'set up its checks (rule 58), or, if HAS is right, take them out')
    return out


ALLOW_LISTS = re.compile(r'^(ALLOWED_\w+|\w+_OK|SET_EXCLUDE|SET_MEANT|ORDER_SWAPS|TOUCHES|FREE_MOVES|AUDIT_ALLOW)$')


def _whole(t0, t1, end):
    return t0 <= 0.1 and t1 >= end - 0.1


def allow_faults(film):
    """Rule 5 (audit item 5, Sam 12 Nov): every "allowed" entry, in every allow-list a film keeps (ALLOWED_CONTACTS,
    ALLOWED_POPS, SET_EXCLUDE, ORDER_SWAPS, SET_MEANT, TOUCHES, FREE_MOVES, and every NAME_OK list: HANDS_OK,
    PORTAL_OK, STILL_OK...), gives its reason (the last words in the entry, at least two of them, after the names it
    matches) and never spans the whole film (a time span from the start to the end lets the check off in silence).
    One line per list."""
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0)) or 1e9
    out = []
    for k in sorted(dir(film)):
        v = getattr(film, k, None)
        if not ALLOW_LISTS.match(k) or not isinstance(v, (list, tuple)) or k == 'CHECKS_OFF':
            continue
        bare, whole = [], []
        for e in v:
            e = tuple(e) if isinstance(e, (list, tuple)) else (e,)
            idx = [i for i, x in enumerate(e) if isinstance(x, str)]
            last = idx[-1] if idx else -1
            after = len(e) - 1 - last                 # what follows the reason: nothing, or one cap (ALLOWED_CONTACTS)
            if last < min(2, len(e) - 1) or after > 1 or len(e[last].split()) < 2:   # names and kinds come first
                bare.append(e)
            nums = [(i, x) for i, x in enumerate(e) if isinstance(x, (int, float)) and not isinstance(x, bool)]
            if any(i2 == i1 + 1 and _whole(a, b, end) for (i1, a), (i2, b) in zip(nums, nums[1:])):
                whole.append(e)
        if bare:
            out.append(f'ALLOWED with no reason: {k}: {len(bare)} of {len(v)} entr{"y" if len(v) == 1 else "ies"} '
                       f'give no reason (first: {bare[0]!r:.90}): end each entry with why, in words (rule 5)')
        if whole:
            out.append(f'ALLOWED for the whole film: {k}: {len(whole)} entr{"y spans" if len(whole) == 1 else "ies span"}'
                       f' 0 to {end:g} s (first: {whole[0]!r:.90}): give the seconds it is meant for (rule 5)')
    return out


def _drop_dupes(lines, rows):
    """The lines the shared checks print for an input the film lacks ('the film has no OUTFIT', 'SHOT_CAST missing')
    that a NOT RUN line already says, so each missing check is told once, at the top."""
    names = {g for key, how, _ in rows if how == 'not set up' and key in CHECKS for g in CHECKS[key][2]}
    pats = [re.compile(rf'(\bno {re.escape(n)}\b|\b{re.escape(n)} missing\b|has no {re.escape(n)}\(t\))') for n in names]
    return [x for x in lines if not any(p.search(x) for p in pats)]


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
    return t, err, list(F.LOG[n0:]), list(kitchecks.DRAWN[d0:]), turned, hands, heads


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
    if os.sep + 'archive' + os.sep not in path:             # a posted film's notes are history
        out += seen_before_faults(text)
    return out


NOT_FAILED = re.compile(r'seen before\W{0,3}(no\b|new kind)|new kind|not a failed fix|changed decision', re.I)


def proven_checks():
    """The names a "seen before" note can give for its check: checktests.py's cases (c_...) and kittests.py's tests."""
    names = set()
    for f in ('checktests.py', 'kittests.py'):
        p = os.path.join(ROOT, 'source', f)
        if os.path.exists(p):
            names |= set(re.findall(r'^def ([a-z]\w*_\w+)\(', open(p).read(), re.M))
    return names - {'proven_checks'}


def seen_before_faults(text, known=None):
    """Rule 30 (audit item 8, Sam 12 Nov): a "seen before" note means the first fix failed and a check was missing;
    the check is built in the same round, before the fix is sent. Each such row in the notes' tables names it
    ("check: c_resting_arm" or a kittests.py test) and the name must be a case that exists. A seen-before that was a
    changed decision ("not a failed fix", "new kind") needs none."""
    known = proven_checks() if known is None else known
    out = []
    for ln in text.splitlines():
        if not ln.strip().startswith('|') or not re.search(r'seen before', ln, re.I) or NOT_FAILED.search(ln):
            continue
        n = ln.strip().strip('|').split('|')[0].strip()
        named = [x for x in re.findall(r'\b([a-z]\w*_\w+)\b', ln) if x in known]
        if not re.search(r'\bcheck\b', ln, re.I) or not named:
            out.append(f'note {n[:30]} is "seen before" (the first fix failed) but names no built check: build it in '
                       f'this round, with its broken example in checktests.py or kittests.py, and write "check: NAME" '
                       f'in the note\'s status before the fix is sent (rule 30)')
    return out


def gate_warnings(film, name, has):
    """Job J: by-hand rules turned into checks, printed (not yet refusing: Sam's numbers decide): rule 74 (an acting
    list row per line), rule 8 (risky moves rehearsed: a "Rehearsal clips sent:" line, or "none: why"), rule 61 (the
    film's code opens with its MAP and stays under about 1,000 lines a file)."""
    out = []
    path = notes_path(film, name)
    text = open(path).read() if os.path.exists(path) else ''
    old = os.path.join(os.path.dirname(path), 'archive', os.path.basename(path))   # a posted film's notes (audit,
    if old != path and os.path.exists(old):                                        # 12 Nov: they were never read)
        text += '\n' + open(old).read()
    if 'voices' in has:
        # "## The acting list", "## Acting (rule 74 ...)", "## Acting, line 9": every table row under any of them
        # (audit, 12 Nov: Ad-Vanced Notice's and Islamocommunism's lists were under "## Acting" and read as missing)
        rows = []
        for m in re.finditer(r'^##+ *(The )?acting\b(?! questions)[^\n]*$(.*?)(?=^##+ |\Z)', text, re.M | re.S | re.I):
            rows += [ln for ln in m.group(2).splitlines() if ln.strip().startswith('|')][2:]
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


def _clean_word(offs):
    """Never the bare word 'clean' while a check is off (audit, 12 Nov)."""
    return 'clean' if not offs else f'no faults found, but {len(offs)} check(s) did not run (Sam\'s yes, listed above)'


def _audit_guard_faults():
    """--audit (audit, 12 Nov): the figure guard's stops that --audit let through to keep going, as faults, each kind
    once with how often (they used to go only into the file's small print, so a finished film's audit undercounted).
    The film's own named breaks (F.allow('a gag')) stay small print: they were meant."""
    seen = {}
    for m in F.LOG:
        if not m.endswith('(allowed: audit of a finished film)'):
            continue
        where, _, what = m.partition(': ')
        what = what.rsplit(' (allowed', 1)[0]
        key = (where.split(' ')[0], what.split(':')[-1].strip()[:60])
        seen.setdefault(key, [0, m.rsplit(' (allowed', 1)[0]])[0] += 1
    return [f'figure guard: {first} ({n} frame(s); a normal pre-flight stops here)' for n, first in seen.values()]


def _off_banner(sheet, offs):
    """The check sheet with a band on top listing every check that is off with Sam's yes, and his words."""
    font = ImageFont.truetype(os.path.join(ROOT, 'source', 'fonts', 'DejaVuSans-Bold.ttf'), 18)
    import textwrap
    rows = ['CHECKS OFF WITH SAM\'S YES (each one, before this animatic):']
    for x in offs:
        rows += textwrap.wrap('- ' + x.split(': ', 1)[-1], 95)
    band = Image.new('RGB', (sheet.width, 16 + 26 * len(rows)), (120, 20, 20))
    d = ImageDraw.Draw(band)
    for i, r in enumerate(rows):
        d.text((12, 8 + 26 * i), r, font=font, fill=(255, 255, 255))
    both = Image.new('RGB', (sheet.width, band.height + sheet.height))
    both.paste(band, (0, 0))
    both.paste(sheet, (0, band.height))
    return both


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
               'hookcheck.py', 'musiccheck.py', 'sizes.py', 'voices.py', 'report.py', 'mounts.py', 'collisions.py')


def _checks_hash():
    h = hashlib.sha1()
    for f in CHECK_FILES:
        path = os.path.join(ROOT, 'source', f)
        if os.path.exists(path):
            h.update(f.encode())
            with open(path, 'rb') as fh:
                h.update(fh.read())
    return h.hexdigest()


def _sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha1(fh.read()).hexdigest()


def _check_files(name):
    """The check code an incremental run trusts, {file: sha1} (audit, 12 Nov, question 5): CHECK_FILES, and every
    other module from source/ loaded now, so a check module missing from CHECK_FILES (turnhead.py, setcheck.py,
    posegallery.py, grips.py...) cannot change while an old clean run is trusted. The film's own drawing code is left
    out (its pictures are compared instead); its own check modules (NAME_checks.py) are kept."""
    import turnhead  # noqa: F401  (the drawing workers load it; its file counts)
    here = os.path.join(ROOT, 'source')
    out = {}
    for mod in list(sys.modules.values()):
        path = os.path.abspath(getattr(mod, '__file__', None) or '')
        if not path.endswith('.py') or os.path.dirname(path) != here:
            continue
        stem = os.path.basename(path)[:-3]
        if (stem == name or stem.startswith(name + '_')) and not re.search(r'check|audit', stem):
            continue
        out[os.path.basename(path)] = _sha(path)
    for f in CHECK_FILES:
        if os.path.exists(os.path.join(here, f)):
            out[f] = _sha(os.path.join(here, f))
    return out


def _files_changed(files):
    """The first check file that changed since the stamp (None: none did)."""
    here = os.path.join(ROOT, 'source')
    for f, h in sorted((files or {}).items()):
        path = os.path.join(here, f)
        if not os.path.exists(path) or _sha(path) != h:
            return f
    return None


def _recheck(film, changed, n_frames, fps):
    """The frames an incremental run redraws: each changed frame and 3 either side, and (audit, 12 Nov, question 5)
    the last CUT_TAIL + 0.8 s of every shot that holds a changed frame, which is all kitchecks.cut_rests looks at: a fix
    that makes an arm drop to rest just before a cut changes only the last frames, and the pose before them was not
    redrawn, so the drop went unseen."""
    import kitchecks
    todo = {j for i in changed for j in range(max(0, i - 3), min(n_frames, i + 4))}
    tail = kitchecks.CUT_TAIL + 0.8 + 3 / fps
    for _n, a, b in [s[:3] for s in getattr(film, 'SHOTS', [])]:
        if any(a * fps <= i < b * fps for i in changed):
            todo |= set(range(max(0, int((b - tail) * fps)), min(n_frames, int(round(b * fps)) + 1)))
    return todo


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


def _text_only(film, problems, end, fps, offs=()):
    """`preflight.py NAME OUT --text` (film-quality-rules 67): after the shared checks, only the subtitles (rows, reading
    speed) and shot lengths; no frame is drawn. Fix text faults here until it is clean, then run the full pre-flight once."""
    if hasattr(film, 'caption_at'):             # rule 62 at the delivered speed (rule 70: 1.1x), in the kit's style
        import subtitles as SUB
        problems += SUB.readable_faults(film.caption_at, end, fps)
    for s in getattr(film, 'SHOTS', []):
        if s[2] - s[1] > MAX_SHOT:
            problems.append(f'shot {s[0]} ({s[1]:.1f}-{s[2]:.1f} s) is {s[2] - s[1]:.1f} s long (over {MAX_SHOT:.0f} s)')
    print('quick check (--text):', _clean_word(offs) if not problems else f'{len(problems)} fault(s)')
    for x in list(offs) + problems:
        print(' -', x)
    print('(no pass stamp: the render still needs the full pre-flight)')


def main():
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    audit = '--audit' in sys.argv              # list every fault instead of stopping at the first
    if audit:
        F._ALLOW.append('audit of a finished film')
    film = importlib.import_module(name)        # module-level checks (set plans, overlaps) run on import
    has = set(getattr(film, 'HAS', KINDS))      # rule 58: only the checks for what the film contains
    unknown = has - set(KINDS)
    if unknown:
        sys.exit(f'preflight: HAS has {sorted(unknown)}; use only {KINDS}')
    runs = {c: any(k in has for k in need) for c, need in SKIP_WHY.items()}
    cover = coverage(film, has)                 # the honest checker (audit, 12 Nov): every check that will not run
    not_run, offs = coverage_lines(film, cover)
    not_run += claim_faults(film, has)          # HAS against what the film gives
    if not_run or offs:
        print(f'CHECKS NOT RUN: {len(not_run)} fault(s)' + (f', {len(offs)} off with Sam\'s yes' if offs else '') +
              ' (each listed first below)')
    stop = gates(film, name)   # rule 14: refuse while the brief or the sheet is not done
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
    if hasattr(film, 'checks'):                 # the film's own plan checks (overlaps, outfits...)
        film.checks()
    shared = ['gate: ' + x for x in stop]       # the shared checks every film gets (Sam, 18 Oct: catch it before I do)
    head = list(not_run)                        # the checks that did not run: always at the top of the list
    B.SS = 1
    import audit as collisions, clipcheck, hookcheck, linecheck, musiccheck, sizes, landmarks, housestyle
    import plan, benchmark, sets
    people, rooms = 'people' in has, 'rooms' in has
    shared += housestyle.faults(film, B, has)   # the template's house style is on, and each check has its inputs
    shared += allow_faults(film)                # rule 5: every allowed entry has a reason, none spans the whole film
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
    if people:                                  # (in a throwaway child: linecheck loads GNU OpenMP, and forking the
        shared += _in_child(linecheck.faults, film)   # drawing workers from a process that has used it freezes them
        shared += _in_child(landmarks.faults, film)   # after about 330 frames: the Elder Swindon hang, 8 Nov)
    if 'props' in has:
        shared += _in_child(sizes.faults, film)  # props and set pieces at their real size
    shared = head + _drop_dupes(shared, cover)  # each missing check told once, at the top
    print('shared checks:', _clean_word(offs) if not shared else f'{len(shared)} fault(s)')
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    if not end:                                 # a film without an end time would pass having checked nothing
        sys.exit('preflight: the film module needs BLACK_AT or DUR (its length in seconds)')
    fps = getattr(film, 'FPS', 12)
    problems = list(shared)
    B.SS = 1
    if '--text' in sys.argv:                    # rule 67: the quick check, in seconds: the plan, script, mouths, subtitles
        _text_only(film, problems, end, fps, offs)   # and shot lengths; no picture passes, no sheet, never a pass stamp
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
            moved = _files_changed(prev.get('files')) if prev and prev.get('files') else 'no list of check files'
            incremental = bool(prev and prev.get('clean') and prev.get('checks') == chk and prev.get('config') == cfg
                               and prev.get('n') == n_frames and prev.get('fps') == fps and moved is None)
            if incremental:
                changed = [i for i in range(n_frames) if hashes[i] != prev['hashes'][i]]
                near = _recheck(film, changed, n_frames, fps)
                print(f'incremental pre-flight: {len(changed)} of {n_frames} frames changed since the last clean run; '
                      f're-checking {len(near)} (the rest were clean then and are unchanged). --full re-checks all.')
            elif prev:
                why = ('the last run found a frame-level fault' if not prev.get('clean') else
                       'the check code changed' if prev.get('checks') != chk else
                       f'the check code changed ({moved})' if moved else
                       'the film\'s settings or allow-lists changed' if prev.get('config') != cfg else
                       'the length changed')
                print(f'full pre-flight (not incremental: {why})')
            else:
                print('full pre-flight (no earlier clean run to compare with)')
        todo = _recheck(film, changed, n_frames, fps) if incremental else None
        hands = []
        first = [i for i in range(0, n_frames, 3) if todo is None or i in todo]
        heads_seen, heads_missing = set(), {}
        for t, err, log, dr, turned, hs, (seen, miss) in pool.imap(_check_frame, first, chunksize=4):
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
        if not incremental:                     # (an incremental pass draws only some frames: no runs to measure)
            problems += kitchecks.still(film, drawn)   # audit item 9: anyone on screen 3 s with nothing moving
        problems += kitchecks.rests(film, drawn)   # rule 78: resting forearms and elbows never below their surface
        problems += kitchecks.cut_rests(film, drawn)   # rule 72: no pose drops back to rest just before a cut
        problems += kitchecks.faces(film, drawn, ask=new_template)   # rule 50: each famous person's face 240 px tall once
    if hasattr(film, 'audits'):               # the film's general body / movement / marks audit (filmkit.py)
        import filmkit
        if incremental:                         # only the bodies in shots that hold a changed frame (a second round)
            filmkit.ONLY_FRAMES = {j for i in changed for j in range(max(0, i - 12), min(n_frames, i + 13))}
        try:
            problems += film.audits()
        finally:
            filmkit.ONLY_FRAMES = None
    if 'people' not in has:                     # HAS against what the drawing pass really drew (views.py people)
        drawn_names = sorted({str(r[1]) for r in drawn if len(r) > 1})
        late = [x for x in claim_faults(film, has, drawn_names) if 'drawing pass' in x and x not in problems]
        problems[:0] = late
        not_run += late
        n_text += len(late)
    if audit:                                   # --audit lets a bad drawing go on (so every fault is listed): the
        problems += _audit_guard_faults()       # figure guard's stops still count, they are not small print
    if stamp_ok and hashes is not None:         # the fingerprints for the next run; "clean" = no frame-level fault
        os.makedirs(os.path.dirname(_frames_path(name)), exist_ok=True)
        with open(_frames_path(name), 'w') as fh:
            json.dump({'checks': _checks_hash(), 'config': _config_hash(film), 'n': n_frames, 'fps': fps,
                       'hashes': hashes, 'clean': len(problems) == n_text, 'files': _check_files(name)}, fh)
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
    if offs:                                    # audit item 2: every check off with Sam's yes is on the check sheet,
        sheet = _off_banner(sheet, offs)        # at the top, before each animatic (he sees what he said yes to)
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
    report.summarise(f'pre-flight ({name})', problems, os.path.join(out, f'{name}-preflight.txt'),
                     notes=(['The figure guard (allowed drawings, how often):'] + log) if log else (), off=offs)
    print('contact sheet:', os.path.join(out, f'{name}-preflight.jpg'))
    if not audit:
        import film_engine                      # rule 59: the render checks this stamp before an animatic or final
        film_engine.write_pass(name, len(problems), not_run=len(not_run))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
