#!/usr/bin/env python3
"""waivers: rule 13's list of exceptions and its house look (tool chat, Sam Y 12 Nov; Blessed notes 45, 52: the
newsreader was skipped in a code comment and had no mouth; rule 80's knees-and-lap check never ran in the TV room).

MAP (rule 61):
  LIST_NAME 40       which film settings are exceptions to a check (HANDS_OK, LINE_OK, ALLOWED_POPS ... any *_OK)
  rows 55            the film's list of exceptions: the notes' "## Exceptions" table (check | who | why | looked at)
  waived 85          is (check, who) written in that table, with a reason and where it was looked at full size
  entries 100        every exception the film's settings make, as (check, who)
  gate_faults 120    pre-flight's gate: each one with no written reason (refuses), and the whole list printed
  install 145        the house look: logs, every front head drawn, whether the house head (burnham's own) drew it
  look_faults 180    everyone on the film's face system: no one on the house head while anyone has their own face
  lap_faults 205     rule 80: anyone seated front on (front or three-quarter) shows knees and lap
  unseen_faults 225  everyone in CAST is seen by the drawing checks (hands, facing, look, lap) at least once
  ANSWERS            named-lines change 2 (Sam's Y, 23 Nov; rule 59): each warning left has its own written answer
  answers            the notes' answered warnings: | `the warning's exact words` | - | why | looked at | kind | owner |
  is_blind           a warning whose check could not see the film: it can never be answered, only cured
  split              (answered, left): the render and pre-flight's stamp count only what is left
  release            a render held for its picture checks goes through once every line is answered (no second render)
  main 245           python3 source/waivers.py FILM: the film's exceptions and which have no written reason;
                     python3 source/waivers.py todo FILM: the rows to fill for every warning still unanswered

The list of exceptions lives in the film's notes (notes/NAME.md), never in code (a code comment, or a 'why' in an
allow-list, is never the reason). Rows: | check | who | why | looked at full size |, one per person or thing left out
of a check; `who` may be a pattern (Journalist*). The check is the setting's name (HANDS_OK) or the check's own name
('house look', 'lap', 'drawing checks', 'camera feel').
"""
import fnmatch
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# A film setting is an exception list when its name ends _OK, or it is one of these. Not exceptions: ALLOWED,
# ALLOWED_CONTACTS and TOUCHES (the touches the staging means, each checked for depth), LINE_OK_WHY (reasons).
LIST_NAME = re.compile(r'^[A-Z][A-Z0-9_]*_OK$|^(AUDIT_ALLOW|ALLOWED_POPS|[A-Z_]*SKIP[A-Z_]*|[A-Z_]*EXEMPT[A-Z_]*)$')
NOT_LISTS = {'ALLOWED', 'ALLOWED_CONTACTS', 'TOUCHES', 'LINE_OK_WHY'}


def _notes(film):
    import preflight
    path = preflight.notes_path(film, film.__name__)
    return open(path).read() if os.path.exists(path) else ''


def rows(text):
    """The notes' "## Exceptions" table: [(check, who, why, looked)]."""
    m = re.search(r'^##+ *(The )?(list of )?exceptions.*?$(.*?)(?=^## |\Z)', text, re.M | re.S | re.I)
    out = []
    for ln in (m.group(3).splitlines() if m else []):
        if not ln.strip().startswith('|') or re.match(r'^\s*\|[\s:|-]+\|\s*$', ln):
            continue
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) < 4 or c[0].lower() == 'check':
            continue
        out.append((c[0], c[1], c[2], c[3]))
    return out


def _who_matches(pattern, who):
    p, w = pattern.strip('`*_ ').lower() or '*', str(who).lower()
    return fnmatch.fnmatchcase(w, pattern.lower().strip('` ')) or fnmatch.fnmatchcase(w, p) or p == w


def waived(table, check, who):
    """The row that excuses `who` from `check`, if it has a reason and a full-size look; else None."""
    for c, w, why, looked in table:
        if c.strip('` ').lower() == check.lower() and _who_matches(w, who) and why and looked:
            return (c, w, why, looked)
    return None


def _who_of(entry):
    if isinstance(entry, (tuple, list)) and entry:
        return str(entry[0])
    return str(entry)


def entries(film):
    """[(setting, who, the entry)] for every exception the film's settings make."""
    out = []
    for k in sorted(vars(film)):
        if k in NOT_LISTS or not LIST_NAME.match(k):
            continue
        v = getattr(film, k)
        if isinstance(v, dict):
            out += [(k, str(w), (w, x)) for w, x in v.items()]
        elif isinstance(v, (list, tuple, set)):
            out += [(k, _who_of(e), e) for e in v]
    return out


def gate_faults(film, text=None):
    """Rule 13 at pre-flight's gate: (faults, listing). Each exception in the film's settings needs a row in the notes'
    exceptions table with a reason and where it was looked at full size; the listing names every one."""
    table = rows(_notes(film) if text is None else text)
    faults, listing, missing, count = [], [], [], {}
    for k, who, e in entries(film):
        count[(k, who)] = count.get((k, who), 0) + 1
    for (k, who), n in count.items():
        ok = waived(table, k, who)
        listing.append(f'{k}: {who}' + (f' ({n} entries)' if n > 1 else '') + ': ' +
                       (f'{ok[2][:70]} (looked: {ok[3][:40]})' if ok else 'NO WRITTEN REASON'))
        if not ok:
            missing.append((k, who))
    if missing:
        faults.append(f'EXCEPTIONS: {len(missing)} exception(s) with no written reason in the notes (rule 13: a row '
                      'in "## Exceptions": | check | who | why | looked at full size |; a code comment is never a '
                      'reason). Rows to fill: ' + ' '.join(f'| {k} | {w} | | |' for k, w in missing))
    return faults, listing


# ------------------------------------------------------------------------------------------------- the house look
LOG = []          # (name, who, house head?, where): every front head drawn on this worker since install()
_HOUSE = []


def install():
    """Log every front head drawn and whether burnham's own head (the house head: no lips at rest) drew it. Wraps the
    top of the head hooks (B.head) and every module's reference to the original."""
    import body as B
    import figure as F
    if getattr(B.head, '_waivers', False):
        return
    orig = None
    for m in list(sys.modules.values()):
        for v in list(getattr(m, '__dict__', {}).values()):
            if callable(v) and getattr(v, '__module__', '') == 'burnham' and getattr(v, '__qualname__', '') == 'head':
                orig = v
                break
        if orig:
            break
    if orig is None:
        return
    top = B.head

    def house_head(img, p, sp, t, hx, hy):
        _HOUSE.append(1)
        return orig(img, p, sp, t, hx, hy)

    def head(img, p, sp, t, hx, hy):
        n0 = len(_HOUSE)
        r = (house_head if top is orig else top)(img, p, sp, t, hx, hy)
        LOG.append((sp.get('name', sp.get('who', 'someone')), sp.get('who'), len(_HOUSE) > n0,
                    F.CONTEXT.get('where', '')))
        del _HOUSE[n0:]
        return r
    head._waivers = True
    for m in list(sys.modules.values()):
        if getattr(m, '__name__', '') == 'burnham':
            continue
        try:
            for k, v in list(vars(m).items()):
                if v is orig:
                    setattr(m, k, house_head)
        except TypeError:
            continue
    B.head = head


def look_faults(log, table=()):
    """Rule 13 (the house look): when anyone in the film has their own face, nobody's front head is the house head
    (Blessed's newsreader, notes 45, 52). The film's own heads are its face system; the house head draws no lips at
    rest. A film where everyone is on the house head is in one look, and passes."""
    own = {n for n, w, house, _ in log if not house}
    if not own:
        return []
    out, seen = [], set()
    for n, w, house, where in log:
        if house and n not in seen and n not in own:
            seen.add(n)
            if not (waived(table, 'house look', n) or (w and waived(table, 'house look', w))):
                out.append(f'HOUSE LOOK: {n} is drawn on the house head (no lips at rest) at {where}, while '
                           f'{", ".join(sorted(own)[:3])} have the film\'s own faces (rule 13: everyone in the '
                           'film\'s house look; or a row in the exceptions)')
    return out


def lap_faults(drawn, table=()):
    """Rule 80 (Sam, 7 Nov): anyone seated front on (the front or three-quarter view) shows knees and lap (views.py
    draws them when the pose sets j['lap']: sitting.py's poses do; the old moves.seated does not). A lap below the
    picture's bottom edge is not looked for; one hidden behind a desk or a box front needs a row in the exceptions."""
    out, seen = [], set()
    for where, name, d in drawn:
        key = (name, (where or ' ').split(' ')[0])          # once per person per shot
        if (d.get('seated') and not d.get('lap') and d.get('view') in ('front', 'three') and d.get('lap_in', True)
                and key not in seen):
            seen.add(key)
            if not waived(table, 'lap', name):
                out.append(f'LAP: {name} sits {d.get("view")} on with no knees or lap at {where} (rule 80: a '
                           'sitting.py pose sets them; old films\' moves.seated does not)')
    return out


def unseen_faults(film, drawn, table=()):
    """Everyone in the film's CAST is drawn through views.person at least once, so the drawing checks (hands, facing,
    the house look, the lap) see them; someone drawn another way is left out of them all, silently."""
    names = {n for _, n, _ in drawn} | {d.get('_who') for _, _, d in drawn}
    out = []
    for key, sp in (getattr(film, 'CAST', {}) or {}).items():
        if not isinstance(sp, dict):
            continue
        n = sp.get('name', key)
        if n not in names and sp.get('who', key) not in names and not waived(table, 'drawing checks', n):
            out.append(f'UNSEEN: {n} is never drawn through views.person, so the hand, facing, look and lap checks '
                       'never see them (rule 13: a row in the exceptions saying why and how they were checked)')
    return out


# ------------------------------------------------------------------------------- answered warnings (named-lines)
# named-lines change 2 (Sam's Y, 23 Nov; rule 59). Before: one switch (--faults-named) waved a film's whole warning list
# through, so Milburn's same 61 lines went past every round and the name-card fault hid among them. Now each warning
# left needs its own row in the notes' "## Exceptions": | `the warning's exact words` | - | why | where it was looked
# at full size | chosen or real | who fixes it |. The words must match exactly, so a warning whose numbers change comes
# back. A warning from a check that could not see the film (blind) cannot be answered: hand the check what it needs.
ANSWER_KINDS = ('chosen', 'real')
BLIND = re.compile(r"COULD NOT TEST|could not (test|run|see)|did not run|cannot run|can't run|not checked|"
                   r"\bskipped\b|the film (has|gives|defines) no |has no facing|no camera in the plan|looks at nothing|"
                   r"so the [a-z' -]+ (check|test)s? cannot run", re.I)


def _norm(line):
    return re.sub(r'\s+', ' ', str(line).replace('|', '/').strip().lstrip('-').strip().strip('`')).strip()


def is_blind(line, film=None):
    """A warning whose check could not see the film. SHOT CAST's 'never on screen' is blind when the film has no
    scene(t) for it to read (Milburn: 21 such lines)."""
    if BLIND.search(str(line)):
        return True
    return (film is not None and str(line).startswith('SHOT CAST') and 'never on screen' in str(line)
            and not hasattr(film, 'scene'))


def answers(text):
    """{exact words: (why, looked, kind, owner)} for the answered-warning rows, and the faults of rows that are not
    complete (no reason, no look, a kind other than chosen or real, no owner)."""
    m = re.search(r'^##+ *(The )?(list of )?exceptions.*?$(.*?)(?=^## |\Z)', text or '', re.M | re.S | re.I)
    out, bad = {}, []
    for ln in (m.group(3).splitlines() if m else []):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if not ln.strip().startswith('|') or not c or not c[0].startswith('`'):
            continue
        c += [''] * (6 - len(c))
        words, why, looked, kind, owner = _norm(c[0]), c[2], c[3], c[4].lower().strip('* '), c[5]
        miss = [n for n, v in (('why', why), ('looked at', looked), ('owner', owner)) if not v]
        if kind not in ANSWER_KINDS:
            miss.append('kind (chosen or real)')
        if miss:
            bad.append(f'ANSWER incomplete for "{words[:80]}": no {", no ".join(miss)}')
            continue
        out[words] = (why, looked, kind, owner)
    return out, bad


def split(lines, text, film=None):
    """(answered [(line, row)], left [line]). Blind lines are always left, marked, even when a row answers them."""
    table, bad = answers(text)
    done, left = [], list(bad)
    for x in lines:
        row = table.get(_norm(x))
        if is_blind(x, film):
            left.append(x if not row else f'{x} [BLIND: a check that could not see the film cannot be answered; '
                                          'hand it what it needs]')
        elif row:
            done.append((x, row))
        else:
            left.append(x)
    return done, left


def answered_note(done):
    return ([f'Answered warnings ({len(done)}; rule 59, named-lines):'] +
            [f'{x[:110]} -> {r[2]}, {r[0][:60]} (looked: {r[1][:30]}; owner {r[3]})' for x, r in done]) if done else []


def todo_rows(left):
    """The rows to paste into "## Exceptions" and fill (blind ones are not offered: they are cured, not answered)."""
    return [f'| `{_norm(x)}` | - | WHY | WHERE LOOKED AT FULL SIZE | chosen or real | WHO FIXES IT |'
            for x in left if not is_blind(x) and not x.startswith('ANSWER incomplete')]


def release(film_name, held, text):
    """A render held for its picture checks (film_engine) goes under its own name once every line saved beside it
    is answered: no second render. Returns why not, or None (released)."""
    import json
    side = held + '.faults.json'
    if not os.path.exists(side):
        return f'no saved picture-check list beside {held}'
    rec = json.load(open(side))
    done, left = split(rec['faults'], text)
    if left:
        return f'{len(left)} picture-check line(s) still unanswered: ' + ' | '.join(left[:3])
    os.replace(held, rec['out'])
    os.remove(side)
    import film_engine
    stamp0 = film_engine.read_pass(film_name) or {}
    film_engine.write_pass(film_name, stamp0.get('faults', 0), pictures=True)
    return None


def main():
    import importlib
    if sys.argv[1:2] == ['todo']:                 # named-lines: the rows to fill for every unanswered warning
        import film_engine
        stamp = film_engine.read_pass(sys.argv[2]) or {}
        rows_ = todo_rows(stamp.get('left', []))
        print('\n'.join(rows_) or 'nothing unanswered in the last pre-flight')
        return
    if sys.argv[1:2] == ['release']:              # python3 source/waivers.py release FILM HELD.mp4
        film = importlib.import_module(sys.argv[2])
        why = release(sys.argv[2], sys.argv[3], _notes(film))
        print(why or 'released: every picture-check line has its own answer')
        sys.exit(1 if why else 0)
    film = importlib.import_module(sys.argv[1])
    faults, listing = gate_faults(film)
    print(f'exceptions ({sys.argv[1]}): {len(listing)}' + (f'; {faults[0][:90]}...' if faults else ', all with reasons'))
    for x in listing:
        print(' -', x)


if __name__ == '__main__':
    main()
