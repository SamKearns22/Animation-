#!/usr/bin/env python3
"""critique: rule 89's fresh-eye critique (Job H, 10 Nov). A NEW helper (Agent tool, general-purpose, model opus) sees
only the pictures, the brief and the checklist, never the chat or the code, and answers in two steps (cold look first).

MAP
  paths ............ PACKS (source/data/critique/FILM/rR-pN, git-ignored), CHECKLIST (guides/critique-checklist.md)
  checklist_for .... the lines for the parts asked: A always, no "Came from", no header, no "Tool:"
  _panel / look .... render a panel (film.picture(t), clean) and the 1-look sheets (numbers only, 1080 px wide)
  check_sheet ...... each panel beside its references (same height), for step 2
  before / pairs ... a notes round: frames saved before any fix; beforeafter.jpg (marked, before, after, same box)
  pack ............. writes the pack and prints the one-line Agent prompt
  parse / record ... refuses a half answer or a look written after the result; saves into the ledger; tallies line ids
  false_alarm ...... Claude marks a FAULT that was not one (counted per line, so Job I sees which lines cry wolf)
  where ............ every named thing per shot from draw_order(t); flags any that start or stop mid-shot (rule 56, M1)
  status ........... the line pre-flight prints; ok only when the round's last pass is clean

    python3 source/critique.py pack FILM SPEC.json
    python3 source/critique.py record FILM PACKDIR
    python3 source/critique.py false FILM LINE "why it was not a fault"
    python3 source/critique.py where FILM [NAME...]
    python3 source/critique.py before FILM SPEC.json
    python3 source/critique.py status FILM

A round: `before` (notes round, before any fix) -> fix -> `pack` -> a NEW helper with the printed prompt -> `record`
-> fix every FAULT or name it to Sam; remake the sheet so each CAN'T TELL shows -> pack again (pass 2, a new helper);
a third pass only if pass 2 found something real; a fault surviving three goes to an options sheet (rule 87).
Calibration (10 Nov, two helpers on Elder Swindon stills plus two old faults put back): both caught the mirrored
label (O1) and the hand off its phone (P1), and neither flagged them on the clean panels. Limits: a person panel
with no face reference always gets CAN'T TELL P4; tiny props get named loosely in the cold look.

SPEC: {"round": R, "panels": [{"t": 12.3 or "img": PATH, "crop": [x0,y0,x1,y1] or null, "is": "...", "parts": "PO",
"refs": [PATH...], "beat": "...", "views": [...]}], "notes": [{"n": 61, "words": "...", "line": "O3", "marked": PATH
or null, "t": 20.1, "box": [x0,y0,x1,y1]}]}. A panel with a crop is a detail (540 px); without, a phone-size frame.
A panel showing something built new for the film adds "new": "NAME" (and "drawn": "file.function"): a clean pass
files it in guides/kit-catalogue.md, "Passed the critique" (library(); Job J).
"""
import glob
import importlib
import json
import os
import re
import sys
from datetime import date

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PACKS = os.path.join(HERE, 'data', 'critique')
CHECKLIST = os.path.join(ROOT, 'guides', 'critique-checklist.md')
PARTS = 'APCOSM'
OPENING = ('Someone else made these pictures for a director who has sent back faults in almost every first look. '
           'Assume there are some: find what he would flag. Don\'t reassure.')
LINE_RE = re.compile(r'^- ([APCOSM]\d+) \((\d+)\) (.*)$')


def _font(size):
    try:
        import burnham as B
        return ImageFont.truetype(B.SANS, size)
    except Exception:
        return ImageFont.load_default()


# ---- the checklist -------------------------------------------------------------------------------------------------
def lines(path=CHECKLIST):
    """{id: (section letter, text without Tool)} in file order."""
    out = {}
    for ln in open(path).read().split('## Came from')[0].splitlines():
        m = LINE_RE.match(ln)
        if m:
            out[m.group(1)] = (m.group(1)[0], re.sub(r'\s*Tool: .*$', '', m.group(3)))
    return out


def checklist_for(parts, path=CHECKLIST):
    """checklist.md for the helper: section A plus the parts asked, nothing for Claude."""
    want = 'A' + ''.join(p for p in PARTS if p in parts and p != 'A')
    text = open(path).read().split('## Came from')[0]
    out = ['# The checklist: answer every line that applies to each panel\n']
    for sec in re.split(r'\n(?=## )', text):
        m = re.match(r'## ([A-Z])\. ', sec)
        if not m or m.group(1) not in want:
            continue
        for ln in sec.strip().splitlines():
            if ln.startswith('Came from') or ln.startswith('**'):
                continue
            out.append(re.sub(r'^- ([A-Z]\d+) \(\d+\) ', r'- \1 ', re.sub(r'\s*Tool: .*$', '', ln))
                       if ln.startswith('- ') else ln)
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def applies(panel):
    """The line ids the helper must answer on this panel: A plus its parts."""
    want = 'A' + panel.get('parts', '')
    return [i for i, (sec, _) in lines().items() if sec in want and (i != 'A4' or panel.get('hook'))
            and (i != 'A2' or panel.get('refs'))]      # A2 needs a reference beside it; A4 the Hook Text frame


# ---- pictures ------------------------------------------------------------------------------------------------------
def _frame(film, t):
    im = (film.picture(t) if hasattr(film, 'picture') else film.frame_image(t)).convert('RGB')
    return im if im.size == (1080, 1920) else im.resize((1080, 1920))


def _panel(film, p):
    im = Image.open(p['img']).convert('RGB') if p.get('img') else _frame(film, p['t'])
    return im.crop(tuple(p['crop'])) if p.get('crop') else im


def _numbered(im, n, width, box=False):
    if box and im.height > im.width:          # a tall detail fits a width x width box, not a 1200 px column
        width = max(1, int(round(im.width * width / im.height)))
    h = max(1, int(round(im.height * width / im.width)))
    tile = Image.new('RGB', (width, h + 34), (18, 18, 22))
    tile.paste(im.resize((width, h)), (0, 34))
    ImageDraw.Draw(tile).text((8, 4), str(n), font=_font(26), fill=(255, 255, 255))
    return tile


def look_sheets(pics, specs, out_dir, per=12):
    """1-look.jpg (and 1-look-2.jpg...): numbers only, frames 270 px, details 540 px, rows at most 1080 px wide."""
    paths = []
    for k in range(0, len(pics), per):
        tiles = [_numbered(pics[i], i + 1, 540 if specs[i].get('crop') else 270, bool(specs[i].get('crop'))) for i in range(k, min(k + per, len(pics)))]
        rows, row, w = [], [], 0
        for tl in tiles:
            if row and w + tl.width > 1080:
                rows.append(row)
                row, w = [], 0
            row.append(tl)
            w += tl.width
        rows.append(row)
        sheet = Image.new('RGB', (1080, sum(max(t.height for t in r) for r in rows)), (8, 8, 10))
        y = 0
        for r in rows:
            x = 0
            for tl in r:
                sheet.paste(tl, (x, y))
                x += tl.width
            y += max(t.height for t in r)
        p = os.path.join(out_dir, '1-look.jpg' if k == 0 else f'1-look-{k // per + 1}.jpg')
        sheet.save(p, quality=85)
        paths.append(p)
    return paths


def _row(items, h):
    ims = [im.resize((max(1, int(im.width * h / im.height)), h)) for im in items]
    row = Image.new('RGB', (sum(i.width for i in ims) + 16 * (len(ims) - 1), h), (255, 255, 255))
    x = 0
    for i in ims:
        row.paste(i, (x, 0))
        x += i.width + 16
    return row


def check_sheet(pics, specs, out_dir, h=480, per=6):
    """check.jpg (check-2.jpg...): each panel (left, numbered) beside its references at the same height."""
    paths = []
    for k in range(0, len(pics), per):
        rows = []
        for i in range(k, min(k + per, len(pics))):
            refs = [Image.open(r).convert('RGB') for r in specs[i].get('refs', [])]
            r = _row([pics[i]] + refs, h)
            lab = Image.new('RGB', (r.width, h + 40), (255, 255, 255))
            lab.paste(r, (0, 40))
            ImageDraw.Draw(lab).text((6, 6), f'{i + 1}' + ('   ours | references' if refs else '   (no reference)'),
                                     font=_font(26), fill=(0, 0, 0))
            rows.append(lab)
        sheet = Image.new('RGB', (max(r.width for r in rows), sum(r.height + 12 for r in rows)), (200, 200, 200))
        y = 0
        for r in rows:
            sheet.paste(r, (0, y))
            y += r.height + 12
        if sheet.width > 2160:
            sheet = sheet.resize((2160, int(sheet.height * 2160 / sheet.width)))
        p = os.path.join(out_dir, 'check.jpg' if k == 0 else f'check-{k // per + 1}.jpg')
        sheet.save(p, quality=85)
        paths.append(p)
    return paths


# ---- before and after (a notes round) ------------------------------------------------------------------------------
def before_dir(film_name, rnd):
    return os.path.join(PACKS, film_name, f'r{rnd}-before')


def before(film_name, spec):
    """Save the frames each note touches, before any fix (step 5 of the design)."""
    film = importlib.import_module(film_name)
    d = before_dir(film_name, spec['round'])
    os.makedirs(d, exist_ok=True)
    for n in spec.get('notes', []):
        _frame(film, n['t']).save(os.path.join(d, f"note-{n['n']}.png"))
    print(d)
    return d


def pairs(film, film_name, spec, out_dir):
    """beforeafter.jpg: one row per note: Sam's marked picture (if sent), before, after: the same box, same scale."""
    rows = []
    for n in spec.get('notes', []):
        bpath = os.path.join(before_dir(film_name, spec['round']), f"note-{n['n']}.png")
        if not os.path.exists(bpath):
            sys.exit(f"critique: no before frame for note {n['n']}: run `critique.py before {film_name} SPEC` "
                     'before fixing anything')
        box = tuple(n.get('box') or (0, 0, 1080, 1920))
        ims = ([Image.open(n['marked']).convert('RGB')] if n.get('marked') else [])
        ims += [Image.open(bpath).convert('RGB').crop(box), _frame(film, n['t']).crop(box)]
        r = _row(ims, 480)
        lab = Image.new('RGB', (r.width, 520), (255, 255, 255))
        lab.paste(r, (0, 40))
        heads = (['marked', 'before', 'after'] if n.get('marked') else ['before', 'after'])
        ImageDraw.Draw(lab).text((6, 6), f"note {n['n']}: " + ' | '.join(heads), font=_font(26), fill=(0, 0, 0))
        rows.append(lab)
    if not rows:
        return None
    sheet = Image.new('RGB', (max(r.width for r in rows), sum(r.height + 12 for r in rows)), (200, 200, 200))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height + 12
    p = os.path.join(out_dir, 'beforeafter.jpg')
    sheet.save(p, quality=85)
    return p


# ---- the pack ------------------------------------------------------------------------------------------------------
def _next_pass(film_name, rnd):
    done = [int(m.group(1)) for p in glob.glob(os.path.join(PACKS, film_name, f'r{rnd}-p*'))
            if (m := re.search(r'-p(\d+)$', p))]
    return max(done, default=0) + 1


def brief_md(film, specs, notes):
    out = ['# What each panel should show (the director\'s intent)\n']
    for i, p in enumerate(specs, 1):
        shot = next((s[0] for s in getattr(film, 'SHOTS', []) if 't' in p and s[1] <= p['t'] < s[2]), '')
        when = f" ({p['t']:.2f} s{', shot ' + shot if shot else ''})" if 't' in p else ''
        out.append(f"{i}{when}: {p['is']}")
        if p.get('beat'):
            out.append(f"   acting beat: {p['beat']}")
        if p.get('views'):
            out.append(f"   views the film uses: {', '.join(p['views'])}")
        out.append(f"   lines to answer: {' '.join(applies(p))}")
    if notes:
        out.append('\n# The director\'s notes this round (each shown in beforeafter.jpg)\n')
        for n in notes:
            out.append(f"Note {n['n']}: \"{n['words']}\" (line {n.get('line', '?')})")
    return '\n'.join(out) + '\n'


STEP1 = '''# Step 1 of 2: the cold look

{opening}

Look ONLY at {looks}. Do not open any other file yet.
For every numbered panel write one line in look.md, 15 words at most: "N: " then the things, actions and feelings
you see, and every word exactly as written (spelled letter by letter as it appears). Never name a real person: say
what you see ("a bearded man in a suit").
Write look.md now ({n} lines, panels 1 to {n}). Only once it is written, open step2.md in this folder.
'''

STEP2 = '''# Step 2 of 2: the check

{opening}

Do not change look.md. Now read brief.md, {checks}, checklist.md{extra}.
Write result.md, under 400 words, no praise, in exactly this form:

## Panel N        (one section for every panel, 1 to {n})
ok: A1 A2 ...     (the line ids you confirmed on this panel)
FAULT P3: where in the panel - what is wrong
CAN'T TELL P5: what picture would show it

Every line id listed for the panel in brief.md must appear once in that panel's section: on "ok:", or as FAULT or
CAN'T TELL.

## Cold look
Your look.md against brief.md (line A1): what you named wrong or missed, and why.

## Same fault elsewhere
For each FAULT: the same fault looked for on every other panel (line A3); name each panel where it is.
{notes_part}
## Not on the list
Up to 5 things the director would flag that no line covers, each with "suggested line:".
'''

NOTES_PART = '''
## Notes
For each of the director's notes: "Note N: fixed / not fixed; worse anywhere: ...; same fault elsewhere: ...",
judged on beforeafter.jpg (marked, before, after) and the panels.
'''


def pack(film_name, spec_path):
    spec = json.load(open(spec_path))
    film = importlib.import_module(film_name)
    specs, notes, rnd = spec['panels'], spec.get('notes', []), spec['round']
    for p in specs:
        bad = [p_ for p_ in p.get('parts', '') if p_ not in PARTS]
        if bad or ('t' not in p and 'img' not in p) or not p.get('is'):
            sys.exit(f'critique: panel {p} needs "t" or "img", "is", and parts from {PARTS}')
    for i, p in enumerate(specs, 1):
        if 'P' in p.get('parts', '') and not p.get('refs'):
            print(f'critique: panel {i} shows a person with no reference: P4 (the face) will come back CAN\'T TELL')
    out = os.path.join(PACKS, film_name, f'r{rnd}-p{_next_pass(film_name, rnd)}')
    os.makedirs(out)
    pics = [_panel(film, p) for p in specs]
    looks = look_sheets(pics, specs, out)
    checks = check_sheet(pics, specs, out)
    ba = pairs(film, film_name, spec, out) if notes else None
    parts = ''.join(sorted(set(''.join(p.get('parts', '') for p in specs)), key=PARTS.index))
    open(os.path.join(out, 'checklist.md'), 'w').write(checklist_for(parts))
    open(os.path.join(out, 'brief.md'), 'w').write(brief_md(film, specs, notes))
    if notes:
        open(os.path.join(out, 'notes.md'), 'w').write(
            ''.join(f"Note {n['n']}: \"{n['words']}\"\n" for n in notes))
    names = lambda ps: ' and '.join(os.path.basename(p) for p in ps)
    open(os.path.join(out, 'step1.md'), 'w').write(STEP1.format(opening=OPENING, looks=names(looks), n=len(specs)))
    open(os.path.join(out, 'step2.md'), 'w').write(STEP2.format(
        opening=OPENING, checks=names(checks), n=len(specs),
        extra=(', notes.md and beforeafter.jpg' if ba else ''), notes_part=(NOTES_PART if notes else '')))
    json.dump(spec, open(out + '.spec.json', 'w'), indent=1)   # beside the pack: the helper never sees it
    print(out)
    print(f'Agent (general-purpose, model opus, a NEW one): "Read {out}/step1.md and follow it exactly; '
          f'write only into {out}."')
    return out


# ---- the record ----------------------------------------------------------------------------------------------------
def parse(text):
    """result.md -> {'panels': {n: {id: ('ok'|'FAULT'|"CAN'T TELL", words)}}, 'sections': set of headings}."""
    panels, cur, sections = {}, None, set()
    for ln in text.splitlines():
        m = re.match(r'^##\s+(.*?)\s*$', ln)
        if m:
            h = m.group(1)
            pm = re.match(r'Panel\s+(\d+)', h, re.I)
            cur = int(pm.group(1)) if pm else None
            if cur is not None:
                panels.setdefault(cur, {})
            else:
                sections.add(h.lower())
            continue
        if cur is None:
            continue
        s = ln.strip().lstrip('-* ').strip()
        if s.lower().startswith('ok:'):
            for i in re.findall(r'\b([APCOSM]\d+)\b', s):
                panels[cur].setdefault(i, ('ok', ''))
            continue
        m = re.match(r"^(FAULT|CAN'?T TELL|CAN’T TELL)\s+((?:[APCOSM]\d+[\s,/&]*)+)\s*:?\s*(.*)$", s, re.I)
        if m:                                    # one fault may name several lines: "FAULT A1 O3: ..."
            kind = 'FAULT' if m.group(1).upper() == 'FAULT' else "CAN'T TELL"
            for lid in re.findall(r'[APCOSM]\d+', m.group(2)):
                if panels[cur].get(lid, ('ok',))[0] != 'FAULT':
                    panels[cur][lid] = (kind, m.group(3))
    return {'panels': panels, 'sections': sections}


def check_answer(pack_dir):
    """The reasons record refuses (empty: whole). look.md before result.md; every panel looked at; every line that
    applies answered; the notes answered in a notes round."""
    spec = json.load(open(pack_dir.rstrip('/') + '.spec.json'))
    look, res = os.path.join(pack_dir, 'look.md'), os.path.join(pack_dir, 'result.md')
    why = []
    if not os.path.exists(look) or not os.path.exists(res):
        return ['look.md and result.md must both be written'], None
    if os.path.getmtime(look) > os.path.getmtime(res):
        why.append('look.md was written (or changed) after result.md: the cold look must come first')
    seen = {int(m.group(1)) for m in re.finditer(r'^\s*(\d+)\s*[:.)-]', open(look).read(), re.M)}
    n = len(spec['panels'])
    miss = sorted(set(range(1, n + 1)) - seen)
    if miss:
        why.append(f'look.md has no line for panel(s) {miss}')
    r = parse(open(res).read())
    for i, p in enumerate(spec['panels'], 1):
        got = r['panels'].get(i)
        if got is None:
            why.append(f'result.md has no section for panel {i}')
            continue
        left = [x for x in applies(p) if x not in got]
        if left:
            why.append(f'panel {i}: lines not answered: {" ".join(left)}')
    if spec.get('notes'):
        body = open(res).read()
        for nt in spec['notes']:
            if not re.search(rf"Note\s+{nt['n']}\b", body):
                why.append(f"note {nt['n']} not answered")
    return why, r


def record(film_name, pack_dir):
    import ledger
    why, r = check_answer(pack_dir)
    if why:
        print('critique: NOT recorded (a half answer):')
        for w in why:
            print(' -', w)
        sys.exit(1)
    spec = json.load(open(pack_dir.rstrip('/') + '.spec.json'))
    faults = [(i, lid, w) for i, got in sorted(r['panels'].items()) for lid, (k, w) in got.items() if k == 'FAULT']
    asked = {i: set(applies(p)) for i, p in enumerate(spec['panels'], 1)}
    cant = [(i, lid, w) for i, got in sorted(r['panels'].items()) for lid, (k, w) in got.items() if k != 'ok'
            and k != 'FAULT' and lid in asked.get(i, ())]      # a CAN'T TELL on a line not asked is dropped
    rnd, pas = spec['round'], int(re.search(r'-p(\d+)$', pack_dir.rstrip('/')).group(1))
    body = (f'== critique, round {rnd} pass {pas} ({date.today()}): {len(faults)} fault(s), {len(cant)} can\'t tell\n'
            + '-- look.md --\n' + open(os.path.join(pack_dir, 'look.md')).read().rstrip()
            + '\n-- result.md --\n' + open(os.path.join(pack_dir, 'result.md')).read().rstrip())
    ledger.append(film_name, rnd, body)
    d = ledger.load(film_name)
    c = d.setdefault('critique', {'passes': [], 'lines': {}})
    c['passes'] = [p for p in c['passes'] if not (p['round'] == rnd and p['pass'] == pas)]
    c['passes'].append({'round': rnd, 'pass': pas, 'date': str(date.today()), 'faults': len(faults),
                        'cant_tell': len(cant), 'open': [f'{i} {lid}: {w}'[:160] for i, lid, w in faults + cant]})
    for _, lid, _ in faults:
        c['lines'].setdefault(lid, {'faults': 0, 'false': 0})['faults'] += 1
    ledger.store(d)
    if not faults and not cant:
        library(film_name, spec, rnd, pas)
    print(f'critique: round {rnd} pass {pas} recorded: {len(faults)} fault(s), {len(cant)} can\'t tell')
    for i, lid, w in faults + cant:
        print(f'  panel {i} {lid}: {w}')
    return faults, cant


LIBRARY = os.path.join(ROOT, 'guides', 'kit-catalogue.md')
LIB_HEAD = '## Passed the critique'


def library(film_name, spec, rnd, pas, path=LIBRARY):
    """Job J: a clean pass files each panel marked "new": NAME (a person, prop, set or move built for this film) in
    the catalogue's "Passed the critique" table, so the next film's plan counts it as KNOWN (guides/job-packs.md)."""
    new = [p for p in spec['panels'] if p.get('new')]
    if not new or not os.path.exists(path):
        return []
    text = open(path).read()
    if LIB_HEAD not in text:
        text = text.rstrip('\n') + f'\n\n{LIB_HEAD} (filed by `critique.py record` on a clean pass: reuse as KNOWN)\n' \
                                   '| thing | what it is | film, round, pass, date | where it is drawn |\n|---|---|---|---|\n'
    head = text.index(LIB_HEAD)
    added = []
    for p in new:
        if f'| {p["new"]} |' in text[head:]:
            continue
        row = (f'| {p["new"]} | {p.get("is", "")[:80]} | {film_name}, r{rnd} p{pas}, {date.today()} | '
               f'{p.get("drawn", p.get("img", "t=%s" % p.get("t")))} |\n')
        text = text.rstrip('\n') + '\n' + row
        added.append(p['new'])
    open(path, 'w').write(text)
    if added:
        print('critique: filed in the catalogue (Passed the critique):', ', '.join(added))
    return added


def false_alarm(film_name, lid, why):
    import ledger
    d = ledger.load(film_name)
    c = d.setdefault('critique', {'passes': [], 'lines': {}})
    c['lines'].setdefault(lid, {'faults': 0, 'false': 0})['false'] += 1
    ledger.store(d)
    film, rnd = ledger.current()
    if film == film_name:
        ledger.append(film_name, rnd, f'critique false alarm, {lid}: {why}')
    print(f'critique: {lid} false alarm noted')


def status(film_name):
    """(ok, line) for pre-flight: the round's last pass clean (no FAULT, no CAN'T TELL), else what is open."""
    import ledger
    passes = ledger.load(film_name).get('critique', {}).get('passes', [])
    film, cur = ledger.current()
    rnd = cur if film == film_name else max((p['round'] for p in passes), default=None)
    mine = sorted((p for p in passes if p['round'] == rnd), key=lambda p: p['pass'])
    if not mine:
        return False, f'critique: round {rnd if rnd is not None else "?"}: none recorded'
    last = mine[-1]
    if last['faults'] + last['cant_tell'] == 0:
        return True, f'critique: round {rnd}, pass {last["pass"]} clean'
    return False, (f'critique: round {rnd}, pass {last["pass"]}: {last["faults"]} fault(s), '
                   f'{last["cant_tell"]} can\'t tell open')


# ---- where (rule 56, line M1) --------------------------------------------------------------------------------------
def where(film_name, names=(), film=None, step=None):
    """Every named thing per shot, from the film's draw_order(t), sampled every frame; flags a thing that starts or
    stops mid-shot (unless the film lists it in ENTRANCES {name: why}). Returns (lines, flags)."""
    film = film or importlib.import_module(film_name)
    if not hasattr(film, 'draw_order'):
        sys.exit(f'critique where: {film_name} has no draw_order(t) (rule 57)')
    planned = getattr(film, 'ENTRANCES', {})
    step = step or 1.0 / getattr(film, 'FPS', 12)
    out, flags = [], []
    for shot, a, b in film.SHOTS:
        ts = [a + k * step for k in range(max(1, int((b - a) / step)))]
        seen = {}
        for t in ts:
            for nm in dict.fromkeys(film.draw_order(t)):
                if names and nm not in names:
                    continue
                seen.setdefault(nm, []).append(t)
        parts = []
        for nm, at in seen.items():
            gaps = [(x, y) for x, y in zip(at, at[1:]) if y - x > step * 1.5]
            first, last = at[0], at[-1]
            late, early = first > ts[0] + step / 2, last < ts[-1] - step / 2
            note = nm
            if late or early or gaps:
                bits = ([f'in at {first:.2f}'] if late else []) + ([f'out at {last:.2f}'] if early else [])
                bits += [f'gone {x:.2f}-{y:.2f}' for x, y in gaps]
                note += ' (' + ', '.join(bits) + ')'
                if nm in planned:
                    note += f' planned: {planned[nm]}'
                else:
                    flags.append(f'{shot}: {nm} ' + ', '.join(bits) + ' mid-shot: pops in or vanishes?')
            parts.append(note)
        out.append(f'{shot} ({a:.2f}-{b:.2f} s): ' + ', '.join(parts))
    return out, flags


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, film = a[0], a[1]
    if cmd == 'pack' and len(a) == 3:
        pack(film, a[2])
    elif cmd == 'record' and len(a) == 3:
        record(film, a[2])
    elif cmd == 'false' and len(a) == 4:
        false_alarm(film, a[2], a[3])
    elif cmd == 'before' and len(a) == 3:
        before(film, json.load(open(a[2])))
    elif cmd == 'status':
        print(status(film)[1])
    elif cmd == 'where':
        out, flags = where(film, a[2:])
        print('\n'.join(out))
        print(f'{len(flags)} flag(s)' + ''.join(f'\n  FLAG {f}' for f in flags))
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
