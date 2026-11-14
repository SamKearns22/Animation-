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
    skin: olive                        hair: crop, 40 32 28    (crop bald side bob long curly bun pony receding none)
    face: jaw_wide +0.04, nose_long ++, size 0.86   (pushes on the average face; + is one step, ++ two: STEPS)
    eyes: 90 110 130 | lips: 190 122 112 | brows: 150 140 132, width 4.4, thick 0.06
    beard: stubble 0.82 | beard: boxed 46 40 38 | glasses: 40 36 34 | freckles | lashes
    outfit: suit navy, shirt white, tie 120 30 40 (or 'no tie'), trousers 50 50 56, sleeves .., shoes .., dress ..
            (suit, jumper, dress, blouse)
    extras: wig, robe, officer, open shirt, crucifix, scarf, zip   (parts that sit on top: EXTRAS)
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
               'short')
FAMOUS_HAIR = ('curls', 'knot')     # a measured head's hair (people_famous): long loose curls, or pulled into a topknot
BEHIND = {'crop': 'crop', 'bald': 'bald', 'side': 'side', 'bob': 'bob', 'long': 'long', 'curly': 'wavy', 'bun': 'crop',
          'pony': 'crop', 'receding': 'bald', 'none': 'bald', 'curls': 'wavy', 'knot': 'crop', 'short': 'crop'}   # the engine's hair for the side and back views
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


def member(d, i, s=0, job=None):
    """Crowd member i (s: the shot's seed; job: what the film has them doing) -> their own description."""
    cr = d['crowd']
    m = {k: (dict(v) if isinstance(v, dict) else v) for k, v in d.items() if k != 'crowd'}
    m["name"] = f"{d['name'].split('(')[0].strip()} {i + 1}"

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
        elif kind == 'part':
            if rest.strip() not in HEAD_PARTS:
                raise DescriptionError(f'head part {rest.strip()!r}: one of {", ".join(HEAD_PARTS)}')
            d['head_part'] = rest.strip()
        else:
            raise DescriptionError(f'head {kind!r}: measured CARD or part NAME')
    elif key == 'tune':
        d.setdefault('tune', {}).update({w: float(v) for w, v in (q.rsplit(' ', 1) for q in parts)})
    elif key.startswith('mood '):
        m = {}
        for q in parts:
            w, _, v = q.partition(' ')
            m[w] = True if not v else (v if w == 'mouth' else float(v))
        d.setdefault('moods', {})[key[5:].strip()] = m
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
        elif kind == 'full':                       # people_famous: moustache, cheeks, chin, grain colours
            d['full_beard'] = {w: colour(c) for w, _, c in (q.partition(' ') for q in parts[1:])}
            if set(d['full_beard']) != {'moustache', 'cheeks', 'chin', 'grain'}:
                raise DescriptionError('beard full: moustache C, cheeks C, chin C, grain C')
        else:
            raise DescriptionError(f'beard {kind!r}: stubble, boxed or full')
    elif key == 'glasses':
        d['glasses'] = colour(val or 'black')
    elif key in ('freckles', 'lashes'):
        d[key] = True
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
    sp = dict(DEFAULTS)
    style = d.get('hair_style', 'crop')
    for k in ('who', 'name', 'skin', 'hw', 'hh', 'height', 'shoulders', 'neck_w', 'bottom', 'leg_k', 'hair_c',
              'outfit', 'jacket', 'sleeve', 'trousers', 'shirt', 'tie', 'shoe', 'dress', 'seed'):
        if k in d:
            sp[k] = d[k]
    if 'skin' not in sp:
        raise DescriptionError(f"{d['who']}: no skin line")
    sp.setdefault('hair_c', (40, 32, 28))
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
                  ('glasses', 'glasses'), ('brow_thick', 'brow_thick'), ('lashes', 'lashes')):
        if k in d:
            fc[fk] = d[k]
    sp['kit_face'] = fc
    sp['kit_extras'] = list(d.get('extras', ()))
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
    """The film's crowds -> {who: description}; crowd_person(d, i, s, job) draws member i."""
    return {w: d for w, d in parse(open(people_file(film)).read()).items() if 'crowd' in d}


def crowd_person(d, i, s=0, job=None):
    """Crowd member i as the engine's person (their own look; the film adds what they are doing)."""
    return person(dict(member(d, i, s, job), crowd_member=True))


# ---------------------------------------------------------------------------------------------- install
def _extras():
    import people_parts as PP
    import people_famous as PF
    return {'wig': ('head', PP.wig_head), 'robe': ('torso', PP.robe_torso), 'officer': ('torso', PP.officer_torso),
            'open shirt': ('torso', PF.open_shirt), 'crucifix': ('torso', PF.crucifix), 'scarf': ('torso', PF.scarf),
            'zip': ('torso', PF.zip_top)}


def _head_parts():
    import people_famous as PF
    import people_walliams as PW
    return {'famous': PF.famous_head, 'walliams': PW.walliams_head}





EXTRAS = ('wig', 'robe', 'officer', 'open shirt', 'crucifix', 'scarf', 'zip')
HEAD_PARTS = ('walliams',)        # a bespoke head too much its own for lines (TEST ONLY: never in a film)


def install(cast):
    """Hang each person's head and torso parts on the engine (traitors_cast's hooks, read by views.person)."""
    import people_parts as PP
    TC = PP.AV.MC.TC
    import people_famous as PF
    import people_turned as PT
    PF.install()
    PT.install()
    for sp in cast.values():                     # one person may have several looks (Brand's four): the head and
        TC.HEADS[sp['who']] = kit_head           # torso are chosen from the look being drawn, not from the name
        TC.TORSOS[sp['who']] = kit_torso
    return cast


def kit_head(img, p, sp, t, hx, hy):
    """The look's own head: a head extra (the wig), a measured or named part, or the invented front face."""
    import people_parts as PP
    ex = _extras()
    fn = next((ex[e][1] for e in sp.get('kit_extras', ()) if ex[e][0] == 'head'), None)
    fn = fn or (_head_parts()[sp['kit_head']] if sp.get('kit_head') else PP.front_head)
    return fn(img, p, sp, t, hx, hy)


def kit_torso(img, p, sp, t):
    """The look's torso extras, in the order written (open shirt, crucifix, scarf...); none: the plain torso."""
    ex = _extras()
    for e in sp.get('kit_extras', ()):
        if ex[e][0] == 'torso':
            ex[e][1](img, p, sp, t)


def faults(cast):
    """Blessed's notes 5, 13, 15, 45 (a repeated note): a face on the house head draws no mouth at rest. Everyone the
    kit builds must be drawn by the kit's own face (or a part over it)."""
    import people_parts as PP
    TC = PP.AV.MC.TC
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
    B, V = PP.B, PP.AV.MC.V
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
    frames = frames or FRAMES[film]
    old = [BL.frame_image(t) for t, _ in frames]
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
        new.append(BL.frame_image(t))
        drawn[-1] |= {w.split(':')[1] + ' (turned)' for w, _ in TH.SEEN[n0:] if w.startswith(('kit:', 'kitfilm:'))}
        turned_new = {w for w, _ in TH.SEEN[n0:] if w.startswith(('kit:', 'kitfilm:')) and w.split(':')[1] in PT_WHO(kit, film)}
        if turned_new:
            PT.ON = False                         # the same frame with the invented people's turned heads off
            plain.append(BL.frame_image(t))
            PT.ON = True
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
