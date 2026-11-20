#!/usr/bin/env python3
"""MAP  People from a description (ranking item 4; overnight chat 4, 14 Nov). A person is a short block of plain lines
(about 10-15) in the film's people file, `story/FILM-people.txt`; this kit turns each block into the engine's person
(views.person: every view, circle hands) and hangs the tested drawing parts (people_parts.py, lifted out of the film
files) on it. A mouth, a neck, ears, brows and eye bags come by default; the cast sheet and the checks come free.
No film imports this until Sam approves the kit (overnight run, answer 2).

THE LANGUAGE (one fact per line, or several on a line split by ' | '; colours are 'R G B' or a word in COLOURS)
    # who: Their name                  starts a person (who: one word, used in the film's code)
    like: OTHER                        start from another person in the file, then change what follows
    body: 1.78 m, shoulders 156, head 66 x 96, neck 1.1, hem 500, legs 1.2   (only the height is needed)
    skin: olive                        hair: crop, 40 32 28    (crop bald side bob long curly bun pony receding none); 'streaks C': curly strands of a
                                       second colour through the first (the goth's blue in purple, Milburn note 1)
    face: jaw_wide +0.04, nose_long ++, size 0.86   (pushes on the average face; + is one step, ++ two: STEPS)
    eyes: 90 110 130 | lips: 190 122 112 | brows: 150 140 132, width 4.4, thick 0.06
    beard: stubble 0.82 | beard: boxed 46 40 38 | glasses: 40 36 34 | freckles | lashes | piercings: brow, lip, nose
    outfit: suit navy, shirt white, tie 120 30 40 (or 'no tie'), trousers 50 50 56, sleeves .., shoes .., dress ..
            (suit, jumper, dress, blouse); 'open collar': the shirt open at the neck (chat 15)
    extras: wig, robe, officer, open shirt, crucifix, scarf, zip, flowers, crest, skirt   (parts that sit on top: EXTRAS)
    (Milburn, 17 Nov: `hair: curly, C, big` | `beard: pencil C` | `glasses: C, thick` | extras flowers (a jumper's
    knitted flowers), crest (a football shirt's badge and white collar trim))
    (GTA, 20 Nov: `outfit: ..., sleeves short` | extras palms (a leaf-print shirt), biker (a leather biker jacket over a
    white vest, gold chain), unicorn (a jumper's unicorn being sick rainbows), scoop (a fitted top's scoop neck and
    gold chain), headphones (over-ear, round the neck) | chat 9: `hair: crop, C, buzz` (a buzz cut), `hair: bun, C,
    messy` (curly hair piled in a messy high bun, curls loose by the face), `bangles` (both wrists) | `soft`: a young face, no eye bags | `hair: pony, C, loose`)
    (GTA characters chat, 20 Nov: `body: ..., build man|woman, arms 36 muscle` (body.FIGS: a man's taper, a woman's
    waist and hips; thicker, muscled arms) | `outfit: ..., shorts knee|crop, camo, fray, trainers` | extras vest (wide
    straps, LEONIDA print, silver chain), tank (thin straps, gold chain): sleeveless, on a skin body, bare arms)
  One outfit in every view (face tool chat 15): each extra and the open collar is drawn turned too (TURNED below):
    its front drawing wrapped round the turned body (views.WrapPen), its own back where it shows from behind (the
    belt, the sash, the scarf round the neck, the top's collar), a bespoke view where Sam has seen one (the open
    collar at three-quarter); the wig turns with the head (people_turned's 'wig'). Kittest outfit_every_view.
    seed: 92                           (only to keep an old film's picture exactly; new people leave it out)
  A real person (chat 4c; people_famous.py: Brand's way, every colour from here):
    head: measured references/FILM/likeness/NAME-card.json, push 1.6     (the likeness card's measures)
    tune: jaw_wide 25.0, nose_long 5.0 | deep set                         (how far each measure is pushed)
    hair: curls, 80 62 48, light 112 90 72, grey 156 146 136 (or: knot)   (long loose curls; pulled into a topknot)
    beard: full, moustache C, cheeks C, chin C, grain C
    mood NAME: brow 0.03, frown -0.01, lid 0.14, squint 0.45, mouth grin  (adds to the house moods, people_famous)
    look of: OTHER                     the same person in another look (Brand's four); the film knows them by one name
    head: part walliams                a bespoke head too much its own for lines (HEAD_PARTS; test only)
  A crowd (chat 4d; Blessed's press pack, 31 people from 16 lines): its lines apply to every member, and
    crowd: press                       starts it (the film asks for member i; s is the shot's seed; job what they do)
    hair (i+2s): short; bob; pony      member i takes item (i + 2s) of the list (any fact: skin, jacket, face...)
    when hair bob; long: body: 1.64 m  facts for the members that fit (when hair ..., when job tv; boom: ...)
    taller (7i+s): 0; 0.05 | seed: 600 + i | hair seed: 500 | hair colour: C | jacket: C | brows: darker hair 0.8
    trousers: darker jacket 0.6
  Crowds varied by default (craft change 1, 16 Nov): what a crowd's lines leave unsaid comes per member from EPR's
    mix (skin, haircut, build, hair colour, face, tops, trousers, shoes, a hat on some: varied() below). Its own lines:
    mix: paris | hats: 0.3 | count: 40 | same: top because WHY   (MIXES; a hat share; the crowd's size; alike on purpose)
  Turned heads (chat 4d; people_turned.py): every invented face turns with its own face card, colours, haircut,
    beard and glasses (Blessed's press pack's way); before, the side and back were the engine's plain head.

    python3 source/people.py sheet FILM OUT.jpg          front, side, back of everyone in the file, true heights
    python3 source/people.py replicate FILM OUT_DIR [--film-keys]   the finished film's frames beside the same frames
                                                         with the kit's people swapped in (nothing in the film changes);
                                                         new turned heads scored apart (an improvement to look at)
    python3 source/people.py describe FILM               the film's people, as the page shows them

Map: colours 55 | steps 70 | parse 81 (a crowd's lines 129, member 166) | the engine's person 324 (a real person
     366; crowds 391) | install 401 (each look's head and torso 437; faults 454) | sheet 464 | replicate 510 |
     lines for the page 643 | main 655
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------------------------------------- colours
COLOURS = {   # the house's skin tones (burnham) and plain words for clothes and hair
    'pale': (246, 208, 188), 'pink': (240, 196, 178), 'olive': (226, 184, 150), 'brown': (176, 120, 86),
    'deep': (120, 78, 56), 'navy': (34, 40, 62), 'charcoal': (46, 46, 54), 'black': (22, 20, 22),
    'white': (246, 246, 246), 'grey': (134, 136, 140), 'red': (170, 26, 34), 'blonde': (214, 184, 120),
    'ginger': (150, 70, 40), 'dark brown': (62, 42, 32), 'light brown': (150, 108, 66), 'silver': (196, 192, 186)}
HAIR_STYLES = ('crop', 'bald', 'side', 'bob', 'long', 'curly', 'bun', 'pony', 'receding', 'none', 'curls', 'knot',
               'short', 'shag')
FAMOUS_HAIR = ('curls', 'knot')     # a measured head's hair (people_famous): long loose curls, or pulled into a topknot
BEHIND = {'crop': 'crop', 'bald': 'bald', 'side': 'side', 'bob': 'bob', 'long': 'long', 'curly': 'wavy', 'bun': 'crop',
          'pony': 'crop', 'receding': 'bald', 'none': 'bald', 'curls': 'wavy', 'knot': 'crop', 'short': 'crop',
          'shag': 'long'}   # the engine's hair for the side and back views
OUTFITS = ('suit', 'jumper', 'dress', 'blouse')
DEFAULTS = dict(hw=66, hh=96, head_dy=10, full=True, pose='custom', shoulders=150, height=1.75, shoe=(30, 26, 24),
                trousers=(50, 50, 56), shirt=(246, 246, 246), tie=None)

# ---------------------------------------------------------------------------------------------- steps
# One '+' on a face measure: about a sixth of how far real faces differ (likeness cards); slopes and tilts in degrees.
STEPS = {'brow_slope': 3.0, 'eye_tilt': 3.0, 'eye_size': 0.01, 'eye_open': 0.02, 'lip_top': 0.01, 'lip_low': 0.01,
         'philtrum': 0.01, 'brow_high': 0.05}
STEP = 0.04


class DescriptionError(ValueError):
    pass


# ---------------------------------------------------------------------------------------------- parse
def colour(s):
    s = s.strip().lower()
    if s in COLOURS:
        return COLOURS[s]
    n = re.findall(r'-?\d+', s)
    if len(n) != 3:
        raise DescriptionError(f'not a colour: {s!r} (three numbers or one of {", ".join(COLOURS)})')
    return tuple(int(v) for v in n)


def _num(s):
    s = s.strip()
    if re.fullmatch(r'[+-]+', s):
        return None, len(s) * (1 if s[0] == '+' else -1)
    return float(s), None


def parse(text):
    """The film's people file -> {who: description dict} in the order written."""
    people, cur = {}, None
    for n, raw in enumerate(text.split('\n'), 1):
        line = raw.split('  #')[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r'#\s*(\w+)\s*:\s*(.+)$', line)
        if m:
            cur = people[m.group(1)] = dict(who=m.group(1), name=m.group(2).strip(), _lines=[])
            continue
        if line.lstrip().startswith('#'):
            continue
        if cur is None:
            raise DescriptionError(f'line {n}: no person yet ("# who: Name" starts one)')
        cur['_lines'].append(line.strip())
        if cur.get('crowd') is not None and _crowd_line(cur, line.strip(), n):
            continue
        for fact in line.split(' | '):
            key, _, val = fact.partition(':')
            key = key.strip().lower()
            try:
                _fact(cur, key, val.strip(), people)
            except DescriptionError as e:
                raise DescriptionError(f'line {n} ({cur["who"]}): {e}')
            except (ValueError, IndexError) as e:
                raise DescriptionError(f'line {n} ({cur["who"]}): {fact.strip()!r}: {e}')
    return people


CYCLE = re.compile(r'^([a-z ]+?)\s*\(([0-9is+ ]+)\)\s*:\s*(.*)$')
WHEN = re.compile(r'^when\s+(\w+)\s+([^:]+):\s*(.+)$')


def _formula(f):
    """'3i+s' -> (3, 1): member i of a crowd takes item (3i + s) of a list (s: the shot's seed)."""
    a = b = 0
    for term in f.replace(' ', '').split('+'):
        m = re.fullmatch(r'(\d*)([is])', term)
        if not m:
            raise DescriptionError(f'({f}): a sum of i and s terms, like (3i+s)')
        k = int(m.group(1) or 1)
        a, b = (a + k, b) if m.group(2) == 'i' else (a, b + k)
    return a, b


def _crowd_line(cur, line, n):
    """A crowd's own lines, kept to apply per member: 'FACT (3i+s): item; item; ...' (member i takes one item) and
    'when hair bob; long: FACTS' / 'when job tv: FACTS' (applied to the members it fits). True if it was one."""
    m = WHEN.match(line)
    if m:
        facts = []
        for fact in m.group(3).split(' | '):
            c = CYCLE.match(fact.strip())
            facts.append((c.group(1).strip(), _formula(c.group(2)), [q.strip() for q in c.group(3).split(';')])
                         if c else (fact.partition(':')[0].strip() if ':' in fact else fact.split(' ')[0],
                                    None, [fact.partition(':')[2].strip() if ':' in fact
                                           else fact.strip().partition(' ')[2]]))
        cur['crowd']['when'].append((m.group(1), {q.strip() for q in m.group(2).split(';')}, facts))
        return True
    c = CYCLE.match(line)
    if c:
        cur['crowd']['cycle'].append((c.group(1).strip(), _formula(c.group(2)), [q.strip() for q in c.group(3).split(';')]))
        return True
    return False


# ------------------------------------------------------------------------------- crowds varied by default
# Craft change 1 (Sam's Y on the kit, 16 Nov; 11+ sameness notes, F15/F16 repeated, Blessed's bald heads): every crowd
# comes out varied unless its lines say otherwise. What a crowd's lines leave unsaid is filled per member from
# European Protests, Ranked's tested mix (protest_tiers_cast: SKINS, CITY_MIX, DRESS['t4'], T4_HATS, the marchers'
# faces and builds), the same member the same in every shot. Lines a crowd may add:
#     mix: paris        (or: light .5, olive .3, brown .2)   the place's skins (MIXES), else 'mixed'; the check tests it
#     hats: 0.3         the share in a beanie or cap (default .22; bald heads may go bare: Sam, 16 Nov); 'hats: 0' none
#     count: 40         how many the film draws (the check's crowd size; default 24)
#     same: hat, top because riot police wear one uniform    keys left alike on purpose (the check lets them be)
SKIN_TONES = {'light': [(236, 200, 176), (226, 186, 158)], 'olive': [(204, 160, 120), (190, 146, 106)],
              'tan': [(172, 124, 88)], 'brown': [(140, 96, 66)], 'dark': [(108, 72, 50), (86, 58, 42)],
              'sasian': [(160, 112, 78)]}
MIXES = {'barcelona': {'light': .72, 'olive': .16, 'tan': .07, 'brown': .03, 'dark': .02},
         'frankfurt': {'light': .46, 'olive': .24, 'tan': .12, 'brown': .06, 'dark': .07, 'sasian': .05},
         'paris': {'light': .55, 'olive': .17, 'tan': .07, 'brown': .07, 'dark': .12, 'sasian': .02},
         'tirana': {'light': .55, 'olive': .40, 'tan': .05},
         'london': {'light': .54, 'olive': .1, 'tan': .06, 'brown': .06, 'dark': .13, 'sasian': .11},
         'miami': {'light': .30, 'olive': .30, 'tan': .15, 'brown': .10, 'dark': .13, 'sasian': .02},   # GTA (Vice City), 20 Nov: Miami-Dade, mostly Hispanic
         'mixed': {'light': .55, 'olive': .15, 'tan': .08, 'brown': .07, 'dark': .1, 'sasian': .05}}
TOPS = [((26, 26, 30), .2), ((54, 56, 60), .12), ((34, 38, 56), .08), ((88, 90, 94), .08), ((168, 168, 164), .07),
        ((66, 68, 54), .07), ((156, 34, 38), .09), ((226, 224, 216), .06), ((62, 86, 128), .07), ((150, 118, 76), .06),
        ((96, 36, 48), .05), ((40, 92, 70), .05)]
LEGS = [((30, 30, 34), .3), ((58, 74, 110), .3), ((88, 88, 92), .18), ((156, 156, 154), .12), ((96, 84, 62), .1)]
SHOES = [((236, 236, 232), .45), ((22, 22, 24), .4), ((120, 120, 124), .08), ((150, 40, 40), .07)]
HATS = ((24, 24, 26), (80, 82, 86), (34, 40, 62), (156, 34, 38), (226, 224, 216), (110, 32, 40), (66, 68, 54),
        (186, 146, 52), (40, 92, 70), (150, 118, 76))      # the 10-colour round (A17): 3 steps round it per member
FACES = ['face_wide 0.04, jaw_wide 0.05', 'face_wide -0.04, chin_long 0.02', '', 'jaw_wide 0.07', 'face_wide 0.05',
         'face_wide -0.03', 'jaw_wide 0.03', 'face_wide -0.05, jaw_wide -0.05']
MEN_HAIR = [('short', .26), ('crop', .22), ('side', .16), ('curly', .1), ('receding', .1), ('bald', .08), ('long', .08)]
WOMEN_HAIR = [('bob', .3), ('long', .3), ('pony', .2), ('bun', .1), ('curly', .1)]
WOMEN = ('bob', 'pony', 'bun')          # cuts the kit gives women (long and curly: either)
SAID = {'skin': 'skin', 'hair': 'hair', 'hair colour': 'hair_c', 'face': 'face', 'body': 'body', 'taller': 'taller',
        'outfit': 'outfit', 'jacket': 'outfit', 'trousers': 'trousers', 'shoes': 'shoes', 'hair seed': 'hair_seed',
        'brows': 'brows', 'glasses': 'glasses', 'beard': 'beard', 'lashes': 'lashes', 'lips': 'lips'}
BEFORE_DEFAULTS = {'blessed': 'posted before the defaults (its press pack is redrawn pixel for pixel)',
                   'protest-tiers': 'in its final rounds when they came in (16 Nov): the film dresses its own crowds'}


def _said(d):
    """The facts a crowd's own lines give (plain, cycled or per 'when'): the defaults leave these alone."""
    out = set()
    for line in d.get('_lines', ()):
        w = WHEN.match(line)
        for fact in (w.group(3) if w else line).split(' | '):
            c = CYCLE.match(fact.strip())
            key = c.group(1).strip() if c else fact.partition(':')[0].strip().lower()
            out.add(SAID.get(key, key))
    return out | {k for keys, _ in d.get('crowd_same', ()) for k in keys}


def _pick(r, opts):
    return opts[int(r.choice(len(opts), p=[w for _, w in opts]))][0] if abs(sum(w for _, w in opts) - 1) < 1e-6 \
        else opts[int(r.choice(len(opts), p=[w / sum(q for _, q in opts) for _, w in opts]))][0]


def varied(d, m, i):
    """Member i's defaults for what the crowd's lines leave unsaid (EPR's mix; the same member in every shot)."""
    import zlib
    import numpy as np
    said = _said(d)
    r = np.random.default_rng(zlib.crc32(f"{d['crowd']['kind']}-{i}".encode()))
    mix = d.get('crowd_mix') or MIXES['mixed']
    g = list(mix)[int(r.choice(len(mix), p=np.array(list(mix.values())) / sum(mix.values())))]
    if 'skin' not in said:
        m['skin'] = SKIN_TONES[g][int(r.integers(len(SKIN_TONES[g])))]
    woman = r.random() < .45
    if 'hair' not in said:
        m['hair_style'] = _pick(r, WOMEN_HAIR if woman else MEN_HAIR)
    woman = m.get('hair_style') in WOMEN or (woman and m.get('hair_style') in ('long', 'curly'))
    if 'hair_c' not in said:
        darker = g != 'light' or m.get('skin', (0,))[0] < 215
        q = r.random()
        m['hair_c'] = ((22, 18, 16) if q < .6 else (40, 30, 24)) if darker else \
            (34, 28, 24) if q < .4 else (70, 50, 34) if q < .72 else (110, 80, 50) if q < .86 else \
            (196, 160, 96) if q < .94 else (150, 146, 140)
    if 'hair_seed' not in said and 'strand_seed' not in m:
        m['strand_seed'] = 500 + i % 40
    if 'brows' not in said:
        m['brows_dk'] = .8
    if 'face' not in said:
        f = FACES[(3 * i) % len(FACES)]
        if f:
            _fact(m, 'face', f, {})
        m.setdefault('face_m', {})['nose_long'] = round(float(r.uniform(-.04, .05)), 3)
    if 'body' not in said:
        if woman:
            m.update(height=round(float(r.uniform(1.56, 1.72)), 2), shoulders=int(r.integers(134, 146)), hw=62, hh=94)
        else:
            m.update(height=round(float(r.uniform(1.66, 1.88)), 2), shoulders=int(r.integers(146, 166)), hw=66, hh=94)
    if 'taller' not in said and 'body' in said:
        m['taller'] = float(r.choice([-.05, -.02, 0, .03, .06]))
    if woman and 'lashes' not in said:
        m['lashes'] = True
        if 'lips' not in said:
            m['lips'] = (178, 84, 86)
    if not woman and 'beard' not in said and r.random() < .2:
        m['stub'] = .84
    if 'glasses' not in said and r.random() < .08:
        m['glasses'] = (40, 36, 34)
    if 'outfit' not in said:
        top = _pick(r, TOPS)
        m.update(outfit='jumper', jacket=top, sleeve=top, shirt=top if r.random() < .5 else (236, 236, 232), tie=None)
    if 'trousers' not in said:
        m['trousers'] = _pick(r, LEGS)
    if 'shoes' not in said:
        m['shoe'] = _pick(r, SHOES)
    share = d.get('crowd_hats', .22)
    if 'hat' not in said and share and m.get('hair_style') not in ('bob', 'pony', 'bun', 'long') and r.random() < share:
        m['kit_hat'] = 'beanie' if r.random() < .55 else 'cap'
        c = HATS[(3 * i) % len(HATS)]
        m['hat_c'] = (c, tuple(int(v * .72) for v in c))
    return m


def member(d, i, s=0, job=None):
    """Crowd member i (s: the shot's seed; job: what the film has them doing) -> their own description."""
    cr = d['crowd']
    m = {k: (dict(v) if isinstance(v, dict) else v) for k, v in d.items() if k != 'crowd'}
    m["name"] = f"{d['name'].split('(')[0].strip()} {i + 1}"
    if d.get('crowd_defaults', True):
        varied(d, m, i)

    def apply(key, form, items):
        val = items[0] if form is None else items[(form[0] * i + form[1] * s) % len(items)]
        if val:
            _fact(m, key, val, {})
    for key, form, items in cr['cycle']:
        apply(key, form, items)
    for what, among, facts in cr['when']:
        if (m.get('hair_style') if what == 'hair' else job if what == 'job' else None) in among:
            for f in facts:
                apply(*f)
    m['height'] = m.get('height', DEFAULTS['height']) + m.pop('taller', 0.0)
    if 'seed_base' in m:
        m['seed'] = m.pop('seed_base') + i
    return m


def _fact(d, key, val, people):
    parts = [p.strip() for p in val.split(',') if p.strip()]
    if key == 'crowd':
        d['crowd'] = dict(kind=val, cycle=[], when=[])
    elif key in ('mix', 'hats', 'count', 'same') and d.get('crowd') is None:
        raise DescriptionError(f'{key}: a crowd\'s line (after "crowd: ...")')
    elif key == 'mix':
        if val.strip().lower() in MIXES:
            d['crowd_mix'] = dict(MIXES[val.strip().lower()])
        else:
            mx = {w: float(v) for w, v in (q.rsplit(' ', 1) for q in parts)}
            if set(mx) - set(SKIN_TONES):
                raise DescriptionError(f'mix: a place ({", ".join(MIXES)}) or shares of {", ".join(SKIN_TONES)}')
            d['crowd_mix'] = mx
    elif key == 'hats':
        d['crowd_hats'] = float(val)
    elif key == 'count':
        d['crowd_n'] = int(val)
    elif key == 'same':
        keys, _, why = val.partition(' because ')
        keys = [k.strip() for k in keys.split(',') if k.strip()]
        if not why.strip() or set(keys) - {'hat', 'hair', 'top', 'skin', 'look', 'step', 'outfit'}:
            raise DescriptionError('same: hat, top because WHY (keys: hat hair top skin look step outfit)')
        d.setdefault('crowd_same', []).append(({'outfit' if k == 'top' else k for k in keys} | set(keys), why.strip()))
    elif key == 'hair colour':
        d['hair_c'] = colour(val)
    elif key == 'hair seed':
        d['strand_seed'] = int(val)
    elif key == 'taller':
        d['taller'] = float(val)
    elif key in ('jacket', 'trousers', 'shirt', 'shoes', 'sleeves'):
        _fact(d, 'outfit', d.get('outfit', 'suit') + ', ' + key + ' ' + val, people)
    elif key in ('like', 'look of'):
        if val not in people:
            raise DescriptionError(f'{key} {val}: no such person above')
        for k, v in people[val].items():
            if k not in ('who', 'name', '_lines'):
                d[k] = dict(v) if isinstance(v, dict) else v
        if key == 'look of':                       # the same person in another look: the film knows them by one name
            d['person'] = people[val].get('person', val)
    elif key == 'head':
        kind, _, rest = parts[0].partition(' ')
        if kind == 'measured':
            d['measured'] = dict(card=rest.strip(), push=1.0)
            for q in parts[1:]:
                w, v = q.split(' ')
                d['measured'][w] = float(v)
        elif kind == 'house':                      # a face tool pick on the house head (facehouse; face chat 11)
            d['house'] = dict(name=rest.strip())
            for q in parts[1:]:
                w, _, v = q.partition(' ')
                if w not in ('hair', 'look'):
                    raise DescriptionError(f'head: house NAME, hair PIECE, look LOOK (not {w!r})')
                d['house'][w] = v.strip()
        elif kind == 'part':
            if rest.strip() not in HEAD_PARTS:
                raise DescriptionError(f'head part {rest.strip()!r}: one of {", ".join(HEAD_PARTS)}')
            d['head_part'] = rest.strip()
        else:
            raise DescriptionError(f'head {kind!r}: measured CARD, house NAME or part NAME')
    elif key == 'house':                           # the house head's own lines (facehouse: brow_thick 0.05, lid 0.24,
        h = d.setdefault('house_kw', {})          # iris_c 56 36 26, shape, ears)
        for q in parts:
            w, _, v = q.partition(' ')
            n = re.findall(r'-?\d*\.?\d+', v)
            h[w] = True if not v.strip() else (float(n[0]) if len(n) == 1 else tuple(int(float(x)) for x in n))
    elif key == 'tune':
        d.setdefault('tune', {}).update({w: float(v) for w, v in (q.rsplit(' ', 1) for q in parts)})
    elif key.startswith('mood '):
        m = {}
        for q in parts:
            w, _, v = q.partition(' ')
            m[w] = True if not v else (v if w == 'mouth' else float(v))
        d.setdefault('moods', {})[key[5:].strip()] = m
    elif key == 'rest smile':                      # GTA (20 Nov): the mouth at rest (house -0.4, a little down)
        d['smile'] = float(val)
    elif key == 'stud':                            # GTA: the nose stud's size (1 = the kit's)
        d['stud_k'] = float(val)
    elif key == 'hoops':                           # GTA (20 Nov): small gold hoop earrings
        d['hoops'] = True
    elif key == 'bangles':                         # GTA (chat 9): bangles and bracelets on both wrists
        d['bangles'] = True
    elif key == 'soft':                            # GTA (20 Nov): a young, pretty face (no eye bags, faint folds)
        d['soft'] = True
    elif key == 'deep set':
        d['deep_set'] = True
    elif key == 'body':
        for p in parts:
            if p.endswith(' m'):
                d['height'] = float(p[:-2])
            else:
                w, _, v = p.partition(' ')
                if w == 'head':
                    a, b = re.findall(r'\d+', v)
                    d['hw'], d['hh'] = int(a), int(b)
                elif w == 'build':                 # GTA (20 Nov): 'build man' (a broad chest's taper) or 'build woman'
                    if v not in ('man', 'woman'):  # (a waist and hips): body.FIGS
                        raise DescriptionError(f'build {v!r}: man or woman')
                    d['figure'] = v
                elif w == 'arms':                  # 'arms 35' (the house arm is 30); 'arms 35 muscle' swells them
                    a = v.split()
                    d['arm_w'] = float(a[0])
                    if a[1:] == ['muscle']:
                        d['arm_bulge'] = 0.28
                else:
                    d[{'shoulders': 'shoulders', 'neck': 'neck_w', 'hem': 'bottom', 'legs': 'leg_k'}[w]] = \
                        float(v) if '.' in v else int(v)
    elif key == 'skin':
        d['skin'] = colour(val)
    elif key == 'hair':
        if parts[0] not in HAIR_STYLES:
            raise DescriptionError(f'hair {parts[0]!r}: one of {", ".join(HAIR_STYLES)}')
        d['hair_style'] = parts[0]
        for q in parts[1:]:
            w, _, c = q.partition(' ')
            if q.strip() == 'big':                     # Milburn (17 Nov): a big mass of curls, half as big again
                d['hair_big'] = 1.5
                continue
            if q.strip() == 'high':                    # GTA (20 Nov): a high ponytail, its top seen over the crown
                d['pony_high'] = True
                continue
            if q.strip() in ('buzz', 'messy'):         # GTA (chat 9): a buzz cut (crop); a messy curly bun (bun)
                d['hair_' + q.strip()] = True
                continue
            if q.strip() == 'loose':                   # GTA (20 Nov): a middle parting and loose strands by the face
                d['hair_loose'] = True
                continue
            if w == 'streaks':                         # Milburn note (Sam, 17 Nov): strands of a second colour
                d['hair_streak'] = colour(c)
                continue
            if w in ('light', 'grey') and q.strip().lower() not in COLOURS:     # 'light 112 90 72'; 'light brown' is a colour
                d['hair_' + w] = colour(c)
            else:
                d['hair_c'] = colour(q)
    elif key == 'face':
        m = d.setdefault('face_m', {})
        for p in parts:
            w, v = p.rsplit(' ', 1)
            if w == 'size':
                d['face_k'] = float(v)
                continue
            num, steps = _num(v)
            m[w] = num if steps is None else steps * STEPS.get(w, STEP)
    elif key in ('eyes', 'lips'):
        d[key] = colour(val)
    elif key == 'brows':
        if parts[0].startswith('darker hair'):         # the hair's colour, darker (settled when the person is built)
            d['brows_dk'] = float(parts[0].split()[-1])
            return
        d['brows'] = colour(parts[0])
        for p in parts[1:]:
            w, v = p.split(' ')
            d['brow_' + {'width': 'w', 'thick': 'thick'}[w]] = float(v)
    elif key == 'beard':
        kind, _, rest = parts[0].partition(' ')
        if kind == 'stubble':
            d['stub'] = float(rest or 0.84)
        elif kind == 'boxed':
            d['beard'] = colour(rest)
        elif kind == 'pencil':                     # Milburn (17 Nov): a thin pencil moustache, nothing else
            d['pencil'] = colour(rest or 'black')
        elif kind == 'full':                       # people_famous: moustache, cheeks, chin, grain colours
            d['full_beard'] = {w: colour(c) for w, _, c in (q.partition(' ') for q in parts[1:])}
            if set(d['full_beard']) != {'moustache', 'cheeks', 'chin', 'grain'}:
                raise DescriptionError('beard full: moustache C, cheeks C, chin C, grain C')
        else:
            raise DescriptionError(f'beard {kind!r}: stubble, boxed, pencil or full')
    elif key == 'glasses':
        d['glasses'] = colour(parts[0] if parts and parts[0] else 'black')
        if 'thick' in parts[1:]:                   # Milburn (17 Nov): thick rectangular frames, the first thing seen
            d['glasses_thick'] = True
    elif key in ('freckles', 'lashes'):
        d[key] = True
    elif key == 'piercings':                       # Milburn note 2 (17 Nov): silver, front head
        got = [w for w in parts if w] or ['brow', 'lip', 'nose']
        bad = [w for w in got if w not in ('brow', 'lip', 'nose')]
        if bad:
            raise DescriptionError(f'piercings {bad[0]!r}: brow, lip or nose')
        d['piercings'] = tuple(got)
    elif key == 'outfit':
        kind, _, c = parts[0].partition(' ')
        if kind not in OUTFITS:
            raise DescriptionError(f'outfit {kind!r}: one of {", ".join(OUTFITS)}')
        d['outfit'] = kind
        if c:
            d['jacket'] = d['sleeve'] = colour(c)
        for p in parts[1:]:
            if p == 'no tie':
                d['tie'] = None
                continue
            if p == 'open collar':                     # the shirt open at the neck (chat 15: an outfit choice)
                d['collar'] = 'open'
                continue
            if p.startswith('shorts'):                 # GTA (20 Nov): 'shorts knee', 'shorts crop' (to mid calf)
                w_ = p.split()[1] if len(p.split()) > 1 else 'knee'
                d['leg_cover'] = {'knee': 0.56, 'crop': 0.8}.get(w_) or float(w_)
                continue
            if p in ('camo', 'cargo', 'fray'):          # the shorts' print and pocket; a frayed hem
                if p == 'fray':
                    d['fray'] = True
                else:
                    d['shorts_print'] = p
                continue
            if p.startswith('trainers'):               # 'trainers' or 'trainers SOLE COLOUR': round-toed, a pale sole
                d['shoe_style'] = 'trainer'
                if p[8:].strip():
                    d['sole_c'] = colour(p[8:].strip())
                continue
            if p == 'sleeves short':                   # a short-sleeved shirt (GTA, 20 Nov: midterminal's sleeve)
                d['short_sleeve'] = True
                d['sleeve_up'], d['sleeve_w'], d['sleeve_taper'] = 0.27, 39, 0.88    # over the shoulder's top (no skin corner shows)
                continue
            w, _, c = p.partition(' ')
            if c.startswith('darker '):                # 'trousers darker jacket 0.6': the jacket's colour, darker
                src, k = c.split()[1:]
                d['trousers' if w == 'trousers' else w] = tuple(int(v * float(k)) for v in d[src])
                continue
            d[{'shirt': 'shirt', 'tie': 'tie', 'trousers': 'trousers', 'sleeves': 'sleeve', 'shoes': 'shoe',
               'dress': 'dress', 'jacket': 'jacket'}[w]] = colour(c)
            if w == 'jacket':
                d['sleeve'] = d['jacket']
    elif key == 'extras':
        for p in parts:
            if p not in EXTRAS:
                raise DescriptionError(f'extra {p!r}: one of {", ".join(EXTRAS)}')
        d['extras'] = parts
    elif key == 'seed':
        if val.replace(' ', '').endswith('+i'):          # a crowd: member i's seed
            d['seed_base'] = int(val.split('+')[0])
        else:
            d['seed'] = int(val)
    else:
        raise DescriptionError(f'unknown line {key!r}')


# ---------------------------------------------------------------------------------------------- the engine's person
def person(d):
    """One description -> the engine's person dict (views.person), with its face card in 'kit_face'."""
    if d.get('house'):
        return _house(d)
    sp = dict(DEFAULTS)
    style = d.get('hair_style', 'crop')
    for k in ('who', 'name', 'skin', 'hw', 'hh', 'height', 'shoulders', 'neck_w', 'bottom', 'leg_k', 'hair_c',
              'outfit', 'jacket', 'sleeve', 'trousers', 'shirt', 'tie', 'shoe', 'dress', 'seed', 'collar', 'kit_hat',
              'hat_c', 'short_sleeve', 'sleeve_up', 'sleeve_w', 'sleeve_taper', 'smile', 'figure', 'arm_w',
              'arm_bulge', 'leg_cover', 'shorts_print', 'fray', 'shoe_style', 'sole_c', 'bangles'):
        if k in d:
            sp[k] = d[k]
    if 'skin' not in sp:
        raise DescriptionError(f"{d['who']}: no skin line")
    sp.setdefault('hair_c', (40, 32, 28))
    if d.get('hair_buzz'):                         # a buzz cut: the skin shows through, so the hair reads lighter
        sp['hair_c'] = tuple(int(h * 0.8 + k * 0.2) for h, k in zip(sp['hair_c'], sp['skin']))
    sp['hair'] = BEHIND[style]
    if 'brows_dk' in d:
        d = dict(d, brows=tuple(int(v * d['brows_dk']) for v in sp['hair_c']))
    sp['brow_c'] = d.get('brows', (40, 32, 28))
    if 'brow_w' in d:
        sp['brow_w'] = d['brow_w']
    if d.get('glasses'):
        sp['glasses'] = True
    if d.get('lashes'):
        sp['lashes'] = True
    fc = dict(m=dict(d.get('face_m', {})), iris=d.get('eyes', (70, 60, 50)), lip=d.get('lips', (190, 120, 110)),
              brow=sp['brow_c'], hair='crop' if style == 'short' else style, turned=style)
    for k, fk in (('face_k', 'k'), ('stub', 'stub'), ('beard', 'beard'), ('freckles', 'freckles'),
                  ('glasses', 'glasses'), ('brow_thick', 'brow_thick'), ('lashes', 'lashes'), ('pencil', 'pencil'),
                  ('glasses_thick', 'glasses_thick'), ('hair_big', 'hair_big'), ('hair_streak', 'hair_streak'), ('hair_loose', 'hair_loose'), ('soft', 'soft'), ('hoops', 'hoops'), ('pony_high', 'pony_high'), ('stud_k', 'stud_k'),
                  ('hair_buzz', 'hair_buzz'), ('hair_messy', 'hair_messy'),
                  ('piercings', 'piercings')):
        if k in d:
            fc[fk] = d[k]
    sp['kit_face'] = fc
    sp['kit_extras'] = list(d.get('extras', ()))
    if {'vest', 'tank'} & set(sp['kit_extras']):   # a sleeveless top (GTA, 20 Nov): bare shoulders and arms; the body
        sp['vest_c'] = sp.get('jacket', (236, 232, 220))   # is skin, the top drawn on it (people_parts.vest_torso)
        sp['jacket'] = sp['sleeve'] = sp['skin']
        sp.pop('short_sleeve', None)
    if 'strand_seed' in d:
        sp['strand_seed'] = d['strand_seed']
    if d.get('crowd_member'):                       # a crowd member: the head draws all their hair (the film's press)
        sp.update(hair='bald', kit_crowd=True)
    sp['who'] = d.get('person', d['who'])
    if d.get('head_part'):
        sp.update(kit_head=d['head_part'], neck_shade=True)
    elif d.get('measured'):
        _famous(d, sp)
    return sp


def _house(d):
    """A face tool pick on the house head (facehouse.person): the pick's face, colours and age lines; the hair piece,
    look and the house lines from the people file, else facehouse.CAST's for that face; the body and clothes here."""
    import facehouse as FH
    h = d['house']
    kw = dict(FH.CAST.get(h['name'], {}))
    kw.update(d.get('house_kw', {}))
    hair = h.get('hair') or kw.pop('hair', None)
    kw.pop('hair', None)
    if hair not in FH.HAIR:
        raise DescriptionError(f"{d['who']}: head: house {h['name']} needs 'hair' one of {', '.join(FH.HAIR)}")
    out = kw.pop('outfit', ('suit', (31, 34, 58)))
    out = (d.get('outfit', out[0]), d.get('jacket', out[1]))
    for k in ('shirt', 'tie', 'height', 'collar'):
        if k in d:
            kw[k] = d[k]
    if 'neck_w' in d:
        kw['neck_w'] = d['neck_w']
    sp = FH.person(h['name'], h.get('look', 'detail'), hair, outfit=out, **kw)
    sp.update(who=d.get('person', d['who']), name=d['name'], kit_extras=list(d.get('extras', ())))
    return sp


def _famous(d, sp):
    """A measured head (people_famous): the likeness card, the beard, the curls, the moods, from the lines."""
    ms = d['measured']
    hc = sp['hair_c']
    fm = dict(key='kit:' + sp['who'], card=ms['card'], push=ms.get('push', 1.0), tune=d.get('tune', {}),
              hair='knot' if d.get('hair_style') == 'knot' else 'curls', iris=d.get('eyes', (70, 60, 50)),
              lip=d.get('lips', (190, 120, 110)), brow_thick=d.get('brow_thick', 0.05),
              deep_set=d.get('deep_set', False), moods=d.get('moods', {}),
              c=dict(hair=hc, light=d.get('hair_light', hc), grey=d.get('hair_grey', hc)))
    if d.get('full_beard'):
        b = d['full_beard']
        fm['beard'] = dict(moust=b['moustache'], mid=b['cheeks'], low=b['chin'], grain=b['grain'])
        sp.update(beard='full', beard_c=b['cheeks'])
    sp.update(kit_head='famous', kit_famous=fm, neck_shade=True, hair='kit_' + fm['hair'])


def people_file(film):
    return os.path.join(ROOT, 'story', f'{film}-people.txt')


def load(film):
    """The film's people file -> {who: engine person} (crowds apart: crowds())."""
    return {w: person(d) for w, d in parse(open(people_file(film)).read()).items() if 'crowd' not in d}


def crowds(film):
    """The film's crowds -> {who: description}; crowd_person(d, i, s, job) draws member i. A film built before the
    crowd defaults (BEFORE_DEFAULTS) keeps its crowds exactly as drawn."""
    out = {w: d for w, d in parse(open(people_file(film)).read()).items() if 'crowd' in d}
    for d in out.values():
        d['crowd_defaults'] = film not in BEFORE_DEFAULTS
    return out


def crowd_person(d, i, s=0, job=None):
    """Crowd member i as the engine's person (their own look; the film adds what they are doing)."""
    sp = person(dict(member(d, i, s, job), crowd_member=True))
    if d.get('crowd_defaults', True):               # GTA shot 4 (Sam's notes 5, 10, 14, 20 Nov): a member made on the fly
        import people_parts as PP                   # was never hung on the engine, so its body's 'bald' stand-in drew
        if PP.B.HEADS and sp['who'] not in PP.B.HEADS:   # (every walker and cop a bald man); hang its own head and torso
            PP.B.HEADS[sp['who']] = kit_head        # once the kit is installed
            PP.B.TORSOS[sp['who']] = kit_torso
    return sp


# ---------------------------------------------------------------------------------------------- install
def _extras():
    import people_parts as PP
    import people_famous as PF
    return {'wig': ('head', PP.wig_head), 'robe': ('torso', PP.robe_torso), 'officer': ('torso', PP.officer_torso),
            'open shirt': ('torso', PF.open_shirt), 'crucifix': ('torso', PF.crucifix), 'scarf': ('torso', PF.scarf),
            'zip': ('torso', PF.zip_top), 'open collar': ('torso', PP.collar_torso),
            'flowers': ('torso', PP.flowers_torso), 'crest': ('torso', PP.crest_torso),
            'skirt': ('torso', PP.skirt_torso), 'palms': ('torso', PP.palms_torso),
            'biker': ('torso', PP.biker_torso), 'unicorn': ('torso', PP.unicorn_torso),
            'scoop': ('torso', PP.scoop_torso), 'headphones': ('torso', PP.headphones_torso),
            'vest': ('torso', PP.vest_torso), 'tank': ('torso', PP.vest_torso)}


def turned():
    """Each torso piece in the turned views (chat 15: one outfit in every view): 'back', its drawing seen from behind
    (None: nothing of it shows from behind); 'own', a bespoke drawing for a view, in place of the front's wrapped."""
    import people_parts as PP
    import people_famous as PF
    return {'robe': dict(back=PP.robe_back), 'officer': dict(back=PP.officer_back), 'open shirt': dict(back=None),
            'crucifix': dict(back=None), 'scarf': dict(back=PF.scarf_back), 'zip': dict(back=PF.zip_back),
            'open collar': dict(back=None, own={'three': PP.collar_three}), 'flowers': dict(back=PP.flowers_torso),
            'crest': dict(back=None), 'skirt': dict(back=PP.skirt_torso), 'palms': dict(back=PP.palms_torso),
            'biker': dict(back=PP.biker_back), 'unicorn': dict(back=None),
            'scoop': dict(back=None), 'headphones': dict(back=PP.headphones_back, own={v: PP.headphones_view(v) for v in PP.PHONES_YAW}),
            'vest': dict(back=PP.vest_back, own={'side': PP.vest_side}),
            'tank': dict(back=PP.vest_back, own={'side': PP.vest_side})}


def pieces(sp):
    """The torso pieces this look wears, in the order drawn: the open collar (the outfit's), then the extras."""
    ex = _extras()
    got = [e for e in sp.get('kit_extras', ()) if ex[e][0] == 'torso']
    got.sort(key=lambda e: e in WORN_OVER)       # a prop worn on top always after the clothes' prints (GTA chat 10)
    return (['open collar'] if sp.get('collar') == 'open' else []) + got


WORN_OVER = ('headphones',)   # props that sit on the clothes (her unicorn print was drawn over her headphones)


TURNED_ON = True     # replicate turns the new turned pieces off to score a frame against the film (as PT.ON)
FILM_TURNED = set()  # pieces the film being replicated draws turned itself (its own body props): left to it
DREW = []            # the turned pieces drawn (replicate: a frame with any is scored again without them)


def kit_torso_view(img, p, sp, view, seated=False):
    """views.TORSO_EXTRAS: this look's torso pieces in a turned view."""
    import views as V
    tv = turned()
    for e in pieces(sp):
        if e in FILM_TURNED or not TURNED_ON:
            continue
        DREW.append(e)
        own = tv[e].get('own', {}).get(view)
        if own:
            own(img, p, sp, 0.0)
            continue
        if view in ('three', 'side'):
            _extras()[e][1](img, V.WrapPen(img, p, sp, view, seated), sp, 0.0)
        if tv[e]['back'] and view in ('three_back', 'back', 'side'):
            tv[e]['back'](img, V.WrapPen(img, p, sp, view, seated, face='back'), sp, 0.0)


def _head_parts():
    import people_famous as PF
    import people_walliams as PW
    import facehouse as FH
    return {'famous': PF.famous_head, 'walliams': PW.walliams_head, 'house': FH.house_head}





EXTRAS = ('wig', 'robe', 'officer', 'open shirt', 'crucifix', 'scarf', 'zip', 'flowers', 'crest', 'skirt', 'palms',
          'biker', 'unicorn', 'scoop', 'headphones', 'vest', 'tank')
HEAD_PARTS = ('walliams',)        # a bespoke head too much its own for lines (TEST ONLY: never in a film)


def install(cast):
    """Hang each person's head and torso parts on the engine (traitors_cast's hooks, read by views.person)."""
    import people_parts as PP
    TC = PP.B                                    # the engine holds each look's head and torso (HEADS, TORSOS)
    import people_famous as PF
    import people_turned as PT
    import facehouse as FH
    import turnhead as TH
    TH.install(PP.V)                             # turned heads, first in line (people_turned, famous, house: before it)
    PF.install()
    PT.install()
    FH.install_turned()
    V = PP.V
    if kit_torso_view not in V.TORSO_EXTRAS:
        V.TORSO_EXTRAS.append(kit_torso_view)
    import people_hats as PH                     # craft change 1: a crowd member's beanie or cap, every view
    if PH.draw not in V.HEAD_WEAR:
        V.HEAD_WEAR.append(PH.draw)
    if PP.headphones_over_neck not in V.HEAD_WEAR:   # GTA chat 10: from behind the neck is drawn after the torso's
        V.HEAD_WEAR.append(PP.headphones_over_neck)  # props, so the band round its back is drawn again over it
    for sp in cast.values():                     # one person may have several looks (Brand's four): the head and
        TC.HEADS[sp['who']] = kit_head           # torso are chosen from the look being drawn, not from the name
        TC.TORSOS[sp['who']] = kit_torso
        if sp.get('kit_famous'):                 # a famous look's curls behind the head
            TC.HAIR_BEHIND[sp['who']] = PF.hair_back
    return cast


def kit_head(img, p, sp, t, hx, hy):
    """The look's own head: a head extra (the wig), a measured or named part, or the invented front face."""
    import people_parts as PP
    ex = _extras()
    fn = next((ex[e][1] for e in sp.get('kit_extras', ()) if ex[e][0] == 'head'), None)
    fn = fn or (_head_parts()[sp['kit_head']] if sp.get('kit_head') else PP.front_head)
    return fn(img, p, sp, t, hx, hy)


def kit_torso(img, p, sp, t):
    """The look's torso pieces, in the order written (open collar, open shirt, crucifix, scarf...); none: the plain
    torso. A head that repaints the neck (braids) lays the collar again itself (neck_redrawn)."""
    ex = _extras()
    for e in pieces(sp):
        if e == 'open collar' and sp.get('neck_redrawn'):
            continue
        ex[e][1](img, p, sp, t)


def faults(cast):
    """Blessed's notes 5, 13, 15, 45 (a repeated note): a face on the house head draws no mouth at rest. Everyone the
    kit builds must be drawn by the kit's own face (or a part over it)."""
    import people_parts as PP
    TC = PP.B                                    # the engine holds each look's head and torso (HEADS, TORSOS)
    ok = {kit_head}
    return [f"{sp['name']}: not on the kit's face (no mouth at rest; Blessed notes 5, 13, 15, 45)"
            for w, sp in cast.items() if TC.HEADS.get(sp['who']) not in ok]


# ---------------------------------------------------------------------------------------------- sheet
YAWS = (0, 45, 90, 135, 180)      # the sheet's turns (chat 4d: every view, the rule that a person turns as drawn)


def sheet(film, out, cast=None, yaws=YAWS, crowd=8):
    """Every person in the people file at five turns (front, three-quarter, side, three-quarter behind, behind) at
    true heights, a 1.75 m person's scale; each crowd's first `crowd` members after them."""
    import people_parts as PP
    from PIL import Image, ImageDraw, ImageFont
    B, V = PP.B, PP.V
    from satire_style import install_circle_hands
    install_circle_hands(B)
    cast = dict(cast or load(film))
    for w, cd in crowds(film).items():
        for i in range(crowd):
            cast[f'{w}{i}'] = crowd_person(cd, i)
    cast = install(cast)
    B.SS = 1
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)   # noqa: E731
    tw, th, per = 200, 360, len(yaws)
    cols = 2
    rows = (len(cast) + cols - 1) // cols
    img = Image.new('RGB', (40 + cols * per * tw, 80 + rows * th), (232, 228, 222))
    d = ImageDraw.Draw(img)
    d.text((20, 20), f'{film}: people from the description (turned {", ".join(map(str, yaws))})', font=font(34),
           fill=(30, 30, 30))
    cam = B.Cam(1.0, 540, 960)
    for i, (w, sp) in enumerate(cast.items()):
        s = 0.5 * sp['height'] / 1.75
        x0, y0 = 20 + (i % cols) * per * tw, 70 + (i // cols) * th
        d.text((x0 + 4, y0), f"{sp['name']} ({sp['height']:.2f} m)", font=font(20), fill=(30, 30, 30))
        for k, yaw in enumerate(yaws):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw)
            tile = tile.crop((290, 60, 790, 880))
            tile.thumbnail((tw, th - 34))
            img.paste(tile.convert('RGB'), (x0 + k * tw, y0 + 28))
    img.save(out, quality=88)
    return out


def cast_sheet(out):
    """The catalogue's tile: the kit's test cast (Blessed's invented people)."""
    return sheet('blessed', out)


# ---------------------------------------------------------------------------------------------- replicate
# The pass mark (Sam, 13 Nov): the kit redraws the film's people from their descriptions and matches the finished
# film's pictures. The film is imported as it is; each of its people's dicts is emptied and refilled IN PLACE from
# the kit (every reference to them sees the kit's person), its old face cards are taken away (so any old drawing path
# left would crash, not pass quietly), and the kit's parts are hung on the engine. Nothing is written to the film.
FRAMES = {'blessed': [(2.0, 'arrive'), (5.6, 'oath'), (8.6, 'jury'), (16.0, 'dock'), (24.0, 'escort'),
                      (28.6, 'cot'), (33.0, 'phone'), (38.0, 'tvroom'), (41.0, 'tv'), (50.0, 'gates'), (59.5, 'walliams'),
                      (20.5, 'van'), (60.5, 'gates2')]}   # van, gates2: Brand turned (turnhead)
KEEP = ('look_', 'mood')     # the film's own staging on a person (which scarf move, a default mood), not their look


def _film_people(film):
    """The film's own dicts for each person in its people file, found by name (film-specific: a small table)."""
    if film == 'blessed':
        import blessed as BL
        import blessed_cast as BC
        import blessed_jury as JY
        import blessed_walliams as BW
        found = {'judge': BC.JUDGE, 'officer': BC.OFFICER, 'newsreader': BC.NEWSREADER, 'guard2': BL.GUARDS['guard2'],
                 'brand': BC.BRAND, 'brand_stand': BC.BRAND_STAND, 'brand_dock': BC.BRAND_DOCK,
                 'brand_prison': BC.BRAND_PRISON, 'walliams': BW.WALLIAMS}
        found.update({w: BL.CAST[w] for w in ('inmate1', 'inmate2', 'inmate3')})
        found.update(JY.JURORS)

        def unhook():
            for w in found:
                BC.FRONT_FACES.pop(w, None)

        def press(d):                              # the film asks for journalist i: the kit's look, the film's job
            film_sp = BL.press_sp

            def kit_sp(i, seed):
                staging = film_sp(i, seed)
                sp = crowd_person(d, i, seed, staging['kit'])
                sp.update(kit=staging['kit'], yaw=staging['yaw'])
                return sp
            BL.press_sp = kit_sp
        return BL, found, unhook, {'press': press}
    raise SystemExit(f'replicate: no table for {film}')


def _differ(a, b):
    import numpy as np
    A, Bm = np.asarray(a.convert('RGB'), np.int16), np.asarray(b.convert('RGB'), np.int16)
    return float((np.abs(A - Bm).max(axis=2) > 24).mean() * 100)


FROZEN_DRIFT = {}                 # frame label -> % of pixels where the live film code differs from its saved copy
FROZEN_FILMS = ('blessed',)       # films whose reference pictures are drawn from their bookmark (source/freeze.py)


def replicate(film, out_dir, frames=None, film_keys=False):
    """Render the finished frames, swap the kit's people in, render the same frames again; one labelled sheet of
    pairs and a score per frame (the share of pixels that differ by more than a hair's colour).
    Turned invented people (chat 4d) are new: the film drew them on the engine's plain head. So each frame is drawn
    a third time with their turned heads off: that score is the pass mark (0.05%); the change the turned heads make
    is reported beside it (an improvement to look at, not a fail). film_keys: crowd heads keyed the film's way (one
    head per haircut, the first member's colours), to show the lifted turned heads match the film exactly."""
    from PIL import Image, ImageDraw, ImageFont
    import people_turned as PT
    os.makedirs(out_dir, exist_ok=True)
    BL, found, unhook, crowd_hooks = _film_people(film)
    FILM_TURNED.update({'blessed': ('scarf', 'officer')}.get(film, ()))   # its own turned scarf and officer kit
    frames = frames or FRAMES[film]
    old = [BL.frame_image(t) for t, _ in frames]
    FROZEN_DRIFT.clear()
    if film in FROZEN_FILMS:                        # one route to the kit: how far the live code is from the POSTED film
        import freeze
        for (t, lab), live in zip(frames, old):
            FROZEN_DRIFT[lab] = _differ(freeze.film_frame(film, t), live)
    kit = load(film)
    for w, d in crowds(film).items():
        crowd_hooks[w](d)
        if film_keys:
            PT.KEYED[w] = lambda sp, _w=w: f"kitfilm:{_w}:{sp['kit_face']['turned']}:{sorted(sp['kit_face']['m'].items())}"
    missing = [w for w in kit if w not in found]
    if missing:
        raise SystemExit(f'replicate: the film has no {missing}')
    for w, sp in kit.items():
        tgt = found[w]
        keep = {k: tgt[k] for k in KEEP if k in tgt}
        tgt.clear()
        tgt.update(sp, **keep)
    unhook()
    install(kit)
    import people_parts as PP
    import people_famous as PF
    import people_walliams as PW
    import turnhead as TH
    drawn, real = [], {}

    def spying(mod, name):                           # proof the kit drew them: who went through the kit's faces
        fn = real[(mod, name)] = getattr(mod, name)

        def spy(img, p, sp, t, hx, hy):
            drawn[-1].add(sp['who'])
            return fn(img, p, sp, t, hx, hy)
        setattr(mod, name, spy)
    for mod, name in ((PP, '_front_head'), (PF, '_famous_head'), (PW, '_head')):
        spying(mod, name)
    new, plain = [], []
    for t, _ in frames:
        drawn.append(set())
        n0 = len(TH.SEEN)
        del DREW[:]
        new.append(BL.frame_image(t))
        drawn[-1] |= {w.split(':')[1] + ' (turned)' for w, _ in TH.SEEN[n0:] if w.startswith(('kit:', 'kitfilm:'))}
        turned_new = {w for w, _ in TH.SEEN[n0:] if w.startswith(('kit:', 'kitfilm:')) and w.split(':')[1] in PT_WHO(kit, film)}
        if turned_new or DREW:
            PT.ON = False                         # the same frame with the invented people's turned heads off
            global TURNED_ON                      # (and the kit's new turned pieces: chat 15)
            TURNED_ON = False
            plain.append(BL.frame_image(t))
            PT.ON = TURNED_ON = True
        else:
            plain.append(None)
    for (mod, name), fn in real.items():
        setattr(mod, name, fn)
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 28)
    tw, th = 405, 720
    sheet_ = Image.new('RGB', (tw * 4 + 30, (th + 50) * ((len(frames) + 1) // 2) + 10), (232, 228, 222))
    d = ImageDraw.Draw(sheet_)
    scores, turned = [], {}
    for i, ((t, label), a, b, c) in enumerate(zip(frames, old, new, plain)):
        diff = _differ(a, b if c is None else c)
        if c is not None:
            turned[label] = _differ(a, b)
        scores.append((t, label, diff, sorted(drawn[i])))
        x, y = 10 + (i % 2) * (2 * tw + 10), 10 + (i // 2) * (th + 50)
        for k, im in enumerate((a, b)):
            sheet_.paste(im.convert('RGB').resize((tw, th)), (x + k * tw, y + 40))
        extra = f'; turned heads {turned[label]:.2f}%' if label in turned else ''
        d.text((x + 4, y + 4), f'{label} {t:.1f}s: finished | kit ({diff:.2f}%{extra})', font=font, fill=(30, 30, 30))
        b.convert('RGB').save(os.path.join(out_dir, f'kit-{label}.png'))
    out = os.path.join(out_dir, f'{film}-people-replicate.jpg')
    sheet_.save(out, quality=86)
    PT.KEYED.clear()
    FILM_TURNED.clear()
    replicate.turned = turned
    return out, scores


def PT_WHO(kit, film):
    """Who the new turned-head route draws that the film drew plain (invented faces; crowds were already turned)."""
    return {sp['who'] for sp in kit.values() if not sp.get('kit_head')}


# ---------------------------------------------------------------------------------------------- lines for the page
def lines(film):
    """Each person's description, one page line each, for page.py (a note on a person changes these lines, not
    code): [(line number of the person's block, 'who (Name): their facts')]."""
    path = people_file(film)
    if not os.path.exists(path):
        return []
    text = open(path).read()
    starts = {m.group(1): text[:m.start()].count('\n') + 1 for m in re.finditer(r'^#\s*(\w+)\s*:', text, re.M)}
    return [(starts[w], f"{w} ({d['name']}): " + '; '.join(d['_lines'])) for w, d in parse(text).items()]


# ---------------------------------------------------------------------------------------------- main
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'sheet':
        print(sheet(sys.argv[2], sys.argv[3]))
    elif cmd == 'replicate':
        out, scores = replicate(sys.argv[2], sys.argv[3], film_keys='--film-keys' in sys.argv)
        for t, label, diff, who in scores:
            tn = replicate.turned.get(label)
            print(f'{label:8s} {t:5.1f}s  {diff:6.2f}% of pixels differ'
                  + (f' (turned invented heads on: {tn:.2f}%)' if tn is not None else '')
                  + f'; drawn by the kit: {", ".join(who) or "nobody"}')
        print(out)
    elif cmd == 'describe':
        for w, d in parse(open(people_file(sys.argv[2])).read()).items():
            print(f"# {w}: {d['name']}\n" + '\n'.join('    ' + ln for ln in d['_lines']), flush=True)
