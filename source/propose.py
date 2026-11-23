#!/usr/bin/env python3
"""propose: the proposal route (Sam, 15 Nov; notes/proposal-route.md). Any change to rules, tools, checks, kits or how
films are built (not animatics, renders, clips or film notes) is answered by fresh helpers and a judge BEFORE Sam sees
it, because Claude's own first idea was a plausible half-effort that only got better when Sam pushed (five times in
one chat, 15 Nov). Closest before it: rule 89's critic (critique.py) attacks pictures, not proposals; CLAUDE.md's
"Back-end proposals get a plain explanation" says how Sam is told, not how the idea is found.

MAP
  paths ............ PROPS (notes/proposals), PROMPTS (guides/proposal-route: helper.md, judge.md, sam-test.md, reader.md), LOCK
  new .............. step 1: notes/proposals/NAME.md with Problem / Facts / Record, NO solution; the chat's own idea
                     goes in NAME/chat.md, written before the helpers run (pack refuses without it)
  pack ............. step 2: refuses a solution-shaped line in the problem, changed prompts (LOCK) or a missing
                     chat.md; records the hashes; prints the two helper lines (A and B; Agent general-purpose, opus)
  judge ............ step 3: both helpers written after the pack; the three versions copied blind and shuffled to
                     NAME/judge/V1..V3.md (the key stays in state.json); prints the judge's line
  parse ............ the judge's file in the fixed shape of judge.md (every version scored 1-5 on quality, notes,
                     cost, risk, undo; Q1-Q8; one pick, or V0 = the judge's own when none passes; each fault
                     [fixed] or [named]; two options with Lost/Added)
  record ........... parse, then the verdict word for word into NAME.md with its hash (problem + versions + verdict)
  verdict_ok ....... the verdict exists and its hash still matches (an edit after the verdict makes it stale)
  show ............. step 5: what Sam sees: the two options, Lost/Added, "Critiqued: N found, N fixed, N named";
                     shape 2 (packed from 23 Nov): each option's fixed fields in order (Problem, steps, Why,
                     You'd notice, Other option, Lost, Added); parse refuses a missing field or a code name
  reader ........... plain-check Change 1 (Sam's 2): packs the blind reader (reader.md, a Sonnet helper) on `show`;
                     run again once it has written: prints its unexplained phrases for the writer. Never blocks
  plain ............ checker A on every lesson or option in a file (the end-of-film review's lessons)
  hook ............. step 4, the Stop hook: blocks a reply that asks Sam to approve a change while the proposal it
                     names (or wrote this turn) has no valid verdict, or lacks the Critiqued line; a change question
                     naming no proposal is blocked too. Routine Y/N (animatic, render, clip, budget) passes.
                     stop_hook_active: never blocks twice, logs the reply to notes/proposals/unrouted.md instead
                     (handover.py end flags this chat's entries). guard-film-questions (22 Nov): every block is logged
                     in full to notes/proposals/guard-blocks.jsonl; the block asks for ONE "Correction:" line (Sam has
                     read the reply); the retry is judged on the text after the block: a right correction = cleared
  blocks ........... the block log in numbers: blocks, retries cleared / let through, full repeated replies
  review ........... step 6, when Sam declares a film complete: every system change since the film began, beside its
                     results (notes, repeats, cost from the ledger) and the proposals later replaced
  mark ............. a proposal's fate: adopted / declined / replaced:NEW (the measure: how often one is replaced)
  lock ............. the prompts' hash; changed only by a proposal with a valid verdict (or the first lock)

    python3 source/propose.py new NAME "title"
    python3 source/propose.py pack NAME          (then two NEW helpers with the printed lines, one message)
    python3 source/propose.py judge NAME         (then one NEW judge with the printed line)
    python3 source/propose.py record NAME
    python3 source/propose.py show NAME
    python3 source/propose.py reader NAME        (pack; then one NEW Sonnet reader; then again: its phrases)
    python3 source/propose.py plain FILE         (checker A on each "### " item or numbered lesson)
    python3 source/propose.py status
    python3 source/propose.py blocks [--since 2026-11-23]
    python3 source/propose.py settle CHAT8 "routed: NAME" | "false block: why"   (a let-through; until then no handover)
    python3 source/propose.py mark NAME adopted|declined|replaced:OTHER
    python3 source/propose.py review FILM [--since 2026-11-12]
    python3 source/propose.py lock [--verdict NAME]
"""
import glob
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPS = os.path.join(ROOT, 'notes', 'proposals')
PROMPTS = os.path.join(ROOT, 'guides', 'proposal-route')
PROMPT_FILES = ('helper.md', 'judge.md', 'sam-test.md', 'reader.md')
SHAPE = 2                        # state shape 2 (plain-check Change 1, 23 Nov): For Sam in fixed fields
READER_MODEL = 'sonnet'          # the blind reader (reader.md): advice to the writer, never a gate (Sam's 2, 23 Nov)
LOCK = os.path.join(PROMPTS, 'LOCK')
UNROUTED = 'unrouted.md'
HELPER = 'general-purpose'      # critique.py's timing (11 Nov): no built-in kind is lighter AND can write its file
MODEL = 'opus'                  # the helpers must out-think the chat's first idea: the same model, fresh
CRITERIA = ('quality', 'notes', 'cost', 'risk', 'undo')
SECTIONS = ('Leak', 'Scores', 'Sam test', 'Pick', 'Why', 'Faults in the pick', 'Final version', 'For Sam')
VERDICT = '## Verdict (the judge, word for word)'
HASH_RE = re.compile(r'<!-- verdict-hash: ([0-9a-f]{16}) -->')
SOLUTION_RE = re.compile(r'^\s*(?:[-*]\s*)?(?:\*\*)?(proposal|proposed|solution|fix|the fix|my idea|suggestion|'
                         r'recommend(?:ation)?|plan)\s*(?:\*\*)?\s*:', re.I | re.M)


def _p(*a):
    return os.path.join(PROPS, *a)


def _sha(*texts):
    h = hashlib.sha256()
    for t in texts:
        h.update((t if isinstance(t, bytes) else t.encode()) + b'\0')
    return h.hexdigest()[:16]


def _read(path):
    try:
        return open(path, encoding='utf-8').read()
    except OSError:
        return ''


def _state(name, upd=None):
    f = _p(name, 'state.json')
    st = json.loads(_read(f) or '{}')
    if upd:
        st.update(upd)
        os.makedirs(_p(name), exist_ok=True)
        json.dump(st, open(f, 'w'), indent=1)
    return st


def problem_text(name):
    """The proposal file above its verdict: what the helpers saw (an edit to it after the verdict makes it stale)."""
    return _read(_p(name + '.md')).split(VERDICT)[0].rstrip() + '\n'


def hashable(name):
    """The problem as hashed: without its Status line, so `mark` never makes a verdict stale."""
    return re.sub(r'^Status: .*\n?', '', problem_text(name), flags=re.M)


def prompts_hash():
    return _sha(*[_read(os.path.join(PROMPTS, f)) for f in PROMPT_FILES])


def lock_state():
    """('ok'|'changed'|'none', note)."""
    have = _read(LOCK).strip()
    if not have:
        return 'none', 'the prompts are not locked yet (the route is not switched on)'
    return ('ok', '') if have == prompts_hash() else ('changed', 'the fixed prompts changed since `propose.py lock`')


# ------------------------------------------------------------------------------------------------ step 1
TEMPLATE = '''# Proposal: {title}

Status: open

## Problem
(what is wrong, in plain words; NO solution: the chat's own idea goes in {name}/chat.md)

## Facts
(the raw facts, each with its source: file, ledger, chat record; numbers as counted, "unchecked" where not)

## Record
(paths the helpers may search, one per line, e.g. notes/ledger/FILM.md)
'''


def new(name, title):
    f = _p(name + '.md')
    if os.path.exists(f):
        sys.exit(f'propose: {f} already exists')
    os.makedirs(_p(name), exist_ok=True)
    open(f, 'w').write(TEMPLATE.format(title=title, name=name))
    print(f'propose: wrote {os.path.relpath(f, ROOT)}; fill Problem, Facts, Record; write your own idea to '
          f'{os.path.relpath(_p(name, "chat.md"), ROOT)}; then `propose.py pack {name}`')


def _section(text, head):
    m = re.search(rf'^## {re.escape(head)}\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''


def record_paths(name):
    return [ln.strip(' -*`') for ln in _section(problem_text(name), 'Record').splitlines()
            if ln.strip(' -*`') and not ln.strip().startswith('(')]


# ------------------------------------------------------------------------------------------------ step 2
def pack_faults(name):
    t = problem_text(name)
    faults = []
    for head in ('Problem', 'Facts', 'Record'):
        body = _section(t, head)
        if not body or body.startswith('('):
            faults.append(f'the {head} section is empty')
    for ln in SOLUTION_RE.findall(t):
        faults.append(f'the problem file states a solution ("{ln}:" line): it would anchor the helpers; move it to chat.md')
    for p in record_paths(name):
        if not glob.glob(os.path.join(ROOT, p)) and not os.path.exists(p):
            faults.append(f'record path not found: {p}')
    if not _read(_p(name, 'chat.md')).strip():
        faults.append(f'no {name}/chat.md: write your own version first, so it is fixed before the helpers run')
    ls, why = lock_state()
    if ls == 'changed':
        faults.append(why + ' (a prompt change goes through the route: `propose.py lock --verdict NAME`)')
    return faults


def helper_line(name, who):
    out = os.path.relpath(_p(name, f'helper-{who.lower()}.md'), ROOT)
    return (f'Agent ({HELPER}, model {MODEL}, a NEW one): "Read guides/proposal-route/helper.md and follow it exactly. '
            f'The repository root is {ROOT}. The problem file is notes/proposals/{name}.md. Write only {out}."')


def pack(name):
    faults = pack_faults(name)
    if faults:
        sys.exit('propose: pack refused:\n' + '\n'.join('  ' + f for f in faults))
    _state(name, {'packed': datetime.now(timezone.utc).timestamp(), 'problem': _sha(hashable(name)),
                  'chat': _sha(_read(_p(name, 'chat.md'))), 'prompts': prompts_hash(), 'shape': SHAPE})
    ls, why = lock_state()
    if ls == 'none':
        print(f'propose: note: {why}')
    print('propose: start BOTH helpers in one message, each NEW, nothing added to the lines:')
    for who in 'AB':
        print('  ' + helper_line(name, who))


# ------------------------------------------------------------------------------------------------ step 3
def judge(name, seed=None):
    st = _state(name)
    if not st.get('packed'):
        sys.exit(f'propose: run `propose.py pack {name}` first')
    if _sha(hashable(name)) != st['problem']:
        sys.exit('propose: the problem file changed after the pack: pack again (the helpers answered the old one)')
    if _sha(_read(_p(name, 'chat.md'))) != st['chat']:
        sys.exit('propose: chat.md changed after the helpers started: the chat may not borrow from them')
    vers = {'chat': _p(name, 'chat.md')}
    for who in 'ab':
        f = _p(name, f'helper-{who}.md')
        if not _read(f).strip():
            sys.exit(f'propose: helper {who.upper()} has not written {os.path.relpath(f, ROOT)}')
        if os.path.getmtime(f) < st['packed'] - 1:
            sys.exit(f'propose: helper-{who}.md is older than the pack: start a NEW helper')
        vers[f'helper {who.upper()}'] = f
    order = list(vers)
    random.Random(seed).shuffle(order)
    os.makedirs(_p(name, 'judge'), exist_ok=True)
    key = {}
    for i, who in enumerate(order, 1):
        open(_p(name, 'judge', f'V{i}.md'), 'w').write(_read(vers[who]))
        key[f'V{i}'] = who
    _state(name, {'key': key, 'judged': datetime.now(timezone.utc).timestamp()})
    out = os.path.relpath(_p(name, 'judge', 'verdict-raw.md'), ROOT)
    vs = ', '.join(os.path.relpath(_p(name, 'judge', f'V{i}.md'), ROOT) for i in range(1, len(order) + 1))
    print('propose: start ONE NEW judge, nothing added to the line:')
    print(f'  Agent ({HELPER}, model {MODEL}, a NEW one): "Read guides/proposal-route/judge.md and follow it exactly. '
          f'The repository root is {ROOT}. The problem file is notes/proposals/{name}.md; the versions are {vs}. '
          f'Write only {out}."')


def parse(text, versions, shape=1):
    """The judge's file -> dict, or ValueError naming what is missing (a half verdict is never recorded). shape 2
    (proposals packed from 23 Nov): every For Sam option must pass checker A (the fixed fields, no code names);
    shape 1 (older proposals) parses as before, so no old verdict goes stale."""
    bad = [s for s in SECTIONS if not re.search(rf'^## {re.escape(s)}\s*$', text, re.M)]
    if bad:
        raise ValueError('missing sections: ' + ', '.join(bad))
    sec = {s: _section(text, s) for s in SECTIONS}
    scores = {}
    for ln in sec['Scores'].splitlines():
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if cells and re.fullmatch(r'V\d+', cells[0]):
            nums = [int(c) for c in cells[1:6] if c.isdigit()]
            if len(nums) != 5 or not all(1 <= n <= 5 for n in nums):
                raise ValueError(f'scores for {cells[0]} are not five numbers from 1 to 5')
            scores[cells[0]] = dict(zip(CRITERIA, nums))
    if sorted(k for k in scores if k != 'V0') != sorted(versions):     # a V0 row is the judge's own (judge.md 5)
        raise ValueError(f'scores cover {sorted(scores)}, not every version {sorted(versions)}')
    qs = set(re.findall(r'^\s*\**Q([1-8])\**\s*[:.]', sec['Sam test'], re.M))
    if len(qs) < 8:
        raise ValueError('the Sam test does not answer Q' + ', Q'.join(str(i) for i in range(1, 9) if str(i) not in qs))
    pick = re.findall(r'\bV\d+\b', sec['Pick'])
    if not pick or pick[0] not in list(versions) + ['V0']:     # V0: the judge's own better-still version (judge.md 5)
        raise ValueError(f'no valid pick (got {sec["Pick"][:40]!r})')
    faults = []
    for ln in sec['Faults in the pick'].splitlines():
        ln = ln.strip()
        if not ln.startswith('-') or ln.strip('- ').lower() in ('none', 'none.'):
            continue
        m = re.search(r'\[(fixed|named)\]', ln, re.I)
        if not m:
            raise ValueError(f'fault not tagged [fixed] or [named]: {ln[:60]}')
        faults.append((m.group(1).lower(), ln))
    opts = re.split(r'^### ', sec['For Sam'], flags=re.M)[1:]
    if len(opts) < 2:
        raise ValueError('For Sam needs two options (### Option 1 / ### Option 2)')
    for o in opts[:2]:
        if not re.search(r'^Lost:', o, re.M) or not re.search(r'^Added:', o, re.M):
            raise ValueError(f'option "{o.splitlines()[0]}" lacks a Lost: or an Added: line')
        if shape >= 2 and shape_faults(o):
            raise ValueError(f'option "{o.splitlines()[0]}" is not in the fixed fields: ' + '; '.join(shape_faults(o)))
    if not sec['Final version'].strip():
        raise ValueError('the final version is empty')
    return {'scores': scores, 'pick': pick[0], 'faults': faults, 'leak': sec['Leak'], 'options': opts[:2]}


# ------------------------------------------------------------------------------------------------ plain words (Sam's Y, 23 Nov)
# CLAUDE.md "Back-end proposals are explained plainly": the problem in 1-2 sentences, numbered steps, why, what he'd
# notice, the other option, one Lost and one Added line, no code names. Checker A (fixed) tests the shape and the names;
# checker C (the blind reader, reader.md) tests whether a stranger understands it. Step 0: notes/proposals/plain-check/step0.
FIELDS = ('Problem', 'Steps', 'Why', "You'd notice", 'Other option', 'Lost', 'Added')
FIELD_RE = {'Problem': r'Problem', 'Why': r'Why', "You'd notice": r"You(?:'|’)d notice", 'Other option': r'Other option',
            'Lost': r'Lost', 'Added': r'Added'}
PLAIN_OK = {'CranbriJoos', 'TikTok', 'YouTube', 'iPhone', 'GitHub', 'BoJack', 'McFadden', 'MacBook'}  # names, not code
CODE_RE = re.compile(r'`[^`\n]+`'                                             # anything in code marks
                     r'|\b[\w-]+\.(?:py|md|json|jsonl|tsv|txt|sh|html|jpg|png|mp4|mov|yaml|toml|lock)\b'  # file names
                     r'|\b(?:source|notes|guides|animations|\.claude)/[\w./-]*'          # paths
                     r'|\b[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+\b'                    # joined_with_underscores
                     r'|\b[a-z]+[A-Z][A-Za-z0-9]*\b|\b[A-Z][a-z]+[A-Z][A-Za-z0-9]*\b'  # joinedCapitals
                     r'|--[a-z][\w-]+')                                        # command switches


def code_names(text):
    return sorted({m.group(0) for m in CODE_RE.finditer(text) if m.group(0) not in PLAIN_OK})


def shape_faults(option):
    """Checker A on one option (or one message): [] when it has every field of the rule, in plain shape."""
    body = '\n'.join(option.splitlines()[1:]) if option.lstrip().startswith(('### ', 'Option')) else option
    faults = []
    for f, pat in FIELD_RE.items():
        hits = re.findall(rf'^\s*(?:\*\*)?{pat}(?:\*\*)?\s*:\s*(\S.*)$', body, re.M | re.I)
        if not hits:
            faults.append(f'no "{f}:" line')
        elif len(hits) > 1:
            faults.append(f'"{f}:" twice')
    prob = re.search(r'^\s*(?:\*\*)?Problem(?:\*\*)?\s*:\s*(.*)$', body, re.M | re.I)
    if prob and len(re.findall(r'[.!?](?:\s|$)', prob.group(1).strip() + ' ')) > 2:
        faults.append('the problem is more than two sentences')
    if len(re.findall(r'^\s*\d+[.)]\s+\S', body, re.M)) < 1:
        faults.append('no numbered step lines ("1. ...")')
    names = code_names(body)
    if names:
        faults.append('code or file names: ' + ', '.join(names[:6]))
    return faults


SAM_DIR = os.path.join(ROOT, 'notes', 'ledger', 'sam')      # Sam's own typed messages (handover.py log)
SAM_KNOWS = os.path.join(PROPS, 'plain-check', 'step0', 'sam-before-19nov.md')   # the C3 reader's 'what Sam knows'
STOP = set('the a an of to in on at for and or but is are was be it its this that with by as from not no his her '
           'their our your my we you i he she they them what which who how why when where one two all any each per '
           'than then so if do does did has have had can could would should will just only also very more most '
           'used sense unclear never explained said meaning means mean exactly'.split())


def _words(text):
    return {w.rstrip('s') for w in re.findall(r"[a-z][a-z0-9'’-]*", text.lower()) if len(w) > 2}


def sam_words():
    """Every word Sam has typed himself (his saved messages): a word he uses is a word he knows."""
    txt = ''
    for f in glob.glob(os.path.join(SAM_DIR, '*.md')):
        t = re.sub(r'<cross-session-message.*?</cross-session-message>', '', _read(f), flags=re.S)
        txt += '\n'.join(ln for ln in t.splitlines() if not ln.startswith(('(handover log', '# Sam', '### ')))
    return _words(txt)


def reader_verdict(look, result, known=None):
    """The blind reader's two files -> {'words', 'unknown', 'wrong', 'pass', 'pass_sam'}. pass = the reader's own
    strict result (no word it can't explain, every mark RIGHT); pass_sam (C2, Step 0's winner) = no word Sam has never
    used himself, and no step retold WRONG. Raises ValueError on a half answer."""
    if not re.search(r'^## Words I can.t explain', look, re.M) or not re.search(r'^## Retelling', look, re.M):
        raise ValueError('look.md lacks its "Words I can\'t explain" or "Retelling" section')
    if not re.search(r'^## Result', result, re.M) or not re.search(r'^## Marks', result, re.M):
        raise ValueError('result.md lacks its "Marks" or "Result" section')
    sec = look.split('## Retelling')[0]
    words = []
    for ln in sec.splitlines():
        m = re.match(r'\s*-\s*(.+?)(?::\s|$)', ln)
        if m and m.group(1).strip().lower().strip('."') != 'none':
            words.append(m.group(1).strip().strip('"“”*'))
    known = sam_words() if known is None else known
    unknown = [w for w in words if {x for x in _words(w) if x not in STOP} - known]
    marks = P_MARK_RE.findall(result.split('## Result')[0])
    wrong = sum(1 for m in marks if m.upper() == 'WRONG')
    strict = re.search(r'^## Result\s*\n\s*PASS\b', result, re.M) is not None
    return {'words': words, 'unknown': unknown, 'wrong': wrong, 'pass': strict and not words,
            'pass_sam': not unknown and not wrong}


P_MARK_RE = re.compile(r':\s*\**(RIGHT|WRONG|PARTLY)\b', re.I)


def who_wrote(key, pick):
    return key.get(pick, 'the judge (V0: no version passed, so it wrote a better one)')


def critiqued(faults):
    fixed = sum(1 for k, _ in faults if k == 'fixed')
    return f'Critiqued: {len(faults)} found, {fixed} fixed, {len(faults) - fixed} named'


def _verdict_hash(name, raw):
    st = _state(name)
    vers = [_read(_p(name, 'judge', f'{v}.md')) for v in sorted(st.get('key', {}))]
    return _sha(hashable(name), *vers, raw)


def record(name):
    st = _state(name)
    raw = _read(_p(name, 'judge', 'verdict-raw.md'))
    if not raw.strip():
        sys.exit(f'propose: the judge has not written notes/proposals/{name}/judge/verdict-raw.md')
    if os.path.getmtime(_p(name, 'judge', 'verdict-raw.md')) < st.get('judged', 0) - 1:
        sys.exit('propose: verdict-raw.md is older than `judge`: start a NEW judge')
    try:
        v = parse(raw, list(st['key']), st.get('shape', 1))
    except ValueError as e:
        sys.exit(f'propose: the verdict is refused ({e}); send the judge back to judge.md\'s shape')
    key = ', '.join(f'{k} = {w}' for k, w in sorted(st['key'].items()))
    block = (f'{VERDICT}\n<!-- verdict-hash: {_verdict_hash(name, raw)} -->\n'
             f'Who wrote which (hidden from the judge): {key}. Picked: {v["pick"]} ({who_wrote(st["key"], v["pick"])}). '
             f'{critiqued(v["faults"])}.\n\n{raw.strip()}\n')
    f = _p(name + '.md')
    text = problem_text(name) + '\n' + block    # read BEFORE open(f, 'w') truncates it (15 Nov: wiped the problem)
    open(f, 'w').write(text)
    _state(name, {'recorded': datetime.now(timezone.utc).timestamp(), 'pick': who_wrote(st['key'], v['pick'])})
    show(name)


def verdict_ok(name):
    """(True, parsed) or (False, why)."""
    text = _read(_p(name + '.md'))
    if not text:
        return False, f'notes/proposals/{name}.md does not exist'
    if VERDICT not in text:
        return False, f'notes/proposals/{name}.md has no judge\'s verdict (run the route: pack, two helpers, judge, record)'
    m = HASH_RE.search(text.split(VERDICT)[1])
    raw = _read(_p(name, 'judge', 'verdict-raw.md'))
    if not m or m.group(1) != _verdict_hash(name, raw):
        return False, f'notes/proposals/{name}.md changed after its verdict (stale): pack and judge it again'
    if not text.split(VERDICT)[1].rstrip().endswith(raw.strip()):    # the copy in NAME.md must stay word for word
        return False, f'notes/proposals/{name}.md: its verdict was edited after `record` (stale): record it again'
    try:
        st = _state(name)
        return True, parse(raw, list(st.get('key', {})), st.get('shape', 1))
    except ValueError as e:
        return False, f'its verdict does not parse ({e})'


# ------------------------------------------------------------------------------------------------ step 5
def show(name):
    ok, v = verdict_ok(name)
    if not ok:
        sys.exit('propose: ' + v)
    who = who_wrote(_state(name)['key'], v['pick'])
    print(f'Proposal {name}: the judge picked {who}\'s version (judged blind).')
    shape = _state(name).get('shape', 1)
    for o in v['options']:
        print('### ' + (field_text(o) if shape >= 2 else o.strip()))
    print(critiqued(v['faults']) + '.')


def fields(option):
    """One option in the fixed fields -> {'head', 'Problem', 'Steps': [...], 'Why', ..., 'Added'} (missing ones '')."""
    lines = option.strip().splitlines()
    out = {'head': lines[0].lstrip('# ').strip() if lines else '', 'Steps': []}
    for ln in lines[1:]:
        st = re.match(r'^\s*(\d+)[.)]\s+(\S.*)$', ln)
        if st:
            out['Steps'].append(st.group(2).strip())
            continue
        for f, pat in FIELD_RE.items():
            m = re.match(rf'^\s*(?:\*\*)?{pat}(?:\*\*)?\s*:\s*(\S.*)$', ln, re.I)
            if m:
                out[f] = m.group(1).strip()
    return out


def field_text(option):
    """An option printed with its fields in the rule's order, whatever order the judge wrote them in."""
    f = fields(option)
    out = [f['head'], 'Problem: ' + f.get('Problem', '')]
    out += [f'{i}. {s}' for i, s in enumerate(f['Steps'], 1)]
    out += [f'{k}: {f.get(k, "")}' for k in FIELDS if k not in ('Problem', 'Steps')]
    return '\n'.join(out)


# ------------------------------------------------------------------------------------------------ the blind reader (advice)
def reader(name):
    """plain-check Change 1 (Sam's answer 2, 23 Nov): the blind reader is ADVICE to the writer, never a gate. First
    run: packs NAME/reader/ (message.md = what `show` prints, truth.md = the final version, sam-knows.md = Sam's own
    earlier messages) and prints the one Sonnet helper line. Once look.md and result.md are written: prints every
    phrase it could not explain, for the writer to explain where it appears (or leave, saying why). Returns 0 always."""
    import contextlib
    import io
    d = _p(name, 'reader')
    look, res = _read(os.path.join(d, 'look.md')), _read(os.path.join(d, 'result.md'))
    msg = io.StringIO()
    with contextlib.redirect_stdout(msg):
        show(name)
    if look and res and _read(os.path.join(d, 'message.md')) == msg.getvalue():
        try:
            v = reader_verdict(look, res)
        except ValueError as e:
            print(f'propose: the reader\'s answer is half written ({e}); advice only, nothing refused')
            return 0
        print(f'propose: the blind reader (advice, never a gate): {len(v["words"])} phrase(s) it could not explain, '
              f'{v["wrong"]} step(s) retold WRONG.')
        for w in v['words']:
            print(f'  - {w}')               # every one: Step 0 showed known words still make unknown phrases
        print('  Explain each where it first appears (a few plain words), or say in the notes why it stays.')
        return 0
    os.makedirs(d, exist_ok=True)
    for f in ('look.md', 'result.md'):
        if os.path.exists(os.path.join(d, f)):
            os.remove(os.path.join(d, f))
    open(os.path.join(d, 'message.md'), 'w').write(msg.getvalue())
    open(os.path.join(d, 'truth.md'), 'w').write(_section(_read(_p(name + '.md')).split(VERDICT)[-1], 'Final version') + '\n')
    open(os.path.join(d, 'sam-knows.md'), 'w').write(_read(SAM_KNOWS))
    rel = os.path.relpath(d, ROOT)
    print('propose: start ONE NEW reader, nothing added to the line (advice only: it never holds the ask):')
    print(f'  Agent ({HELPER}, model {READER_MODEL}, a NEW one): "Read guides/proposal-route/reader.md and follow it '
          f'exactly. The repository root is {ROOT}. Your folder is {rel}."')
    print(f'  then: python3 source/propose.py reader {name}')
    return 0


def plain_items(text):
    """A file's items for checker A: each '### ' block, or else each top-level bold numbered lesson ('1. **...')."""
    if re.search(r'^### ', text, re.M):
        return ['### ' + b for b in re.split(r'^### ', text, flags=re.M)[1:]]
    return [b for b in re.split(r'^(?=\d+\.\s+\*\*)', text, flags=re.M) if re.match(r'\d+\.\s+\*\*', b)]


def plain(path):
    """Checker A on every item of a file (the end-of-film review's lessons, or any ask): 0 when all pass."""
    items = plain_items(_read(path))
    if not items:
        print(f'propose: plain: no "### " items or numbered lessons in {path}')
        return 1
    bad = 0
    for it in items:
        head = it.strip().splitlines()[0].lstrip('# ')[:70]
        f = shape_faults(it)
        bad += bool(f)
        print(f'  {"FAIL" if f else "ok  "} {head}' + (': ' + '; '.join(f) if f else ''))
    print(f'propose: plain: {len(items) - bad} of {len(items)} in the fixed fields')
    return 1 if bad else 0


def status():
    for f in sorted(glob.glob(_p('*.md'))):
        name = os.path.basename(f)[:-3]
        if name == UNROUTED[:-3]:
            continue
        st = re.search(r'^Status: (.*)$', _read(f), re.M)
        ok, v = verdict_ok(name)
        print(f'{name}: {st.group(1) if st else "?"}; ' + (f'verdict ok, picked {who_wrote(_state(name)["key"], v["pick"])}' if ok
                                                           else v))


def mark(name, fate):
    if not re.fullmatch(r'adopted|declined|replaced:[\w.-]+', fate):
        sys.exit('propose: fate is adopted, declined or replaced:OTHER')
    f = _p(name + '.md')
    text = _read(f)
    if not text:
        sys.exit(f'propose: no {f}')
    # the Status line sits above the verdict, so it is kept out of the hash: rewrite without touching it
    text = re.sub(r'^Status: .*$', f'Status: {fate} ({datetime.now():%Y-%m-%d})', text, count=1, flags=re.M)
    open(f, 'w').write(text)


# ------------------------------------------------------------------------------------------------ step 4, the hook
ASK_RE = re.compile(r'\bY or N\b|\bY/N\b|\bN or Y\b|\b\d or \d\b|\(I.d say [YN\d]|\(my pick|\bapprove\b|'
                    r'\bgo ahead\b|\bshall I\b|\bok(?:ay)? to\b|\bAnswer Q\d', re.I)
CHANGE_RE = re.compile(r'\brules?\b|\brulebook\b|\btools?\b|\bchecks?\b(?! sheet)|\bkits?\b|\bkit piece|\bhooks?\b|'
                       r'CLAUDE\.md|\bjob packs?\b|\bpacks?\b|\bguides?\b|\.py\b|\bhelpers?\b|\bpipeline\b|'
                       r'\bworkflow\b|\bprocess\b|how (?:the )?films are (?:built|made)|\bthe system\b|\baudit\b|'
                       r'\bhandover check\b|\bpre-?flight\b', re.I)
ROUTINE_RE = re.compile(r'\banimatic\b|\bfinal render\b|\brender\b|\bclips?\b|\bpost(?:ed|ing)?\b|\bbudget\b|'
                        r'\bcheck sheet\b|\bsheet\b|\bnotes on\b|\bvoice|\brecording\b', re.I)
PROP_RE = re.compile(r'notes/proposals/([A-Za-z0-9][\w-]*)')


def questions(reply):
    """Lines that ask Sam to approve something: a question or a Need line carrying a Y/N or choice marker."""
    out = []
    lines = reply.splitlines()
    for i, ln in enumerate(lines):
        if ('?' in ln or re.match(r'\s*\**Need', ln)) and ASK_RE.search(ln):
            ctx = [x for x in lines[max(0, i - 6):i] if not x.lstrip().startswith(('Checks:', '- Checks'))]
            out.append((ln.strip(), '\n'.join(ctx)))
    return out


def is_change(q, ctx):
    """A question asking Sam to approve a change to the system (not a routine film Y/N)."""
    if ROUTINE_RE.search(q):
        return False
    return bool(CHANGE_RE.search(q) or (CHANGE_RE.search(ctx) and re.search(
        r'\b(change|build|write|add|edit|remove|take .* out|switch|wire|widen|run|make)\b', q, re.I)))


def reply_faults(reply, touched=(), lookup=None):
    """Why this reply may not go to Sam yet ([] when it may). lookup(name) -> (ok, verdict) stands in for verdict_ok
    when the labelled list (guard-film-questions Learn) is replayed with each proposal as it was then."""
    lookup = lookup or verdict_ok
    asks = questions(reply)
    if not asks:
        return []
    names = sorted(n for n in set(touched) | set(PROP_RE.findall(reply))
                   if n != UNROUTED[:-3] and not n.startswith('review-')
                   and (n in PROP_RE.findall(reply) or os.path.exists(_p(n + '.md'))))   # cost audit, 21 Nov: a proposal
    #                deleted this turn (or a glob like dearest-week-*.md in a command) is not one the reply asks about
    faults = []
    for name in names:
        ok, v = lookup(name)
        if not ok:
            faults.append(v)
        elif critiqued(v['faults']) not in reply:
            faults.append(f'proposal {name}: the reply must carry "{critiqued(v["faults"])}" (counted from its file; '
                          f'`propose.py show {name}` prints what Sam sees)')
    if not names:
        for q, ctx in asks:
            if is_change(q, ctx):
                faults.append(f'this asks Sam to approve a change to the system with no proposal behind it: "{q[:120]}". '
                              'Put it through the route first (`propose.py new NAME`, pack, judge, record) and name '
                              'notes/proposals/NAME.md in the reply. If it is not a change to rules, tools, checks, '
                              'kits or how films are built, reword the question to say what it is.')
                break
    return faults


def locked_line(reply):
    """Sam, 23 Nov: "Please remove the 'locked by Sam' section of communication as it doesn't help me." The line stays
    in the notes (it guards shots for later chats); a reply to Sam never carries it."""
    if re.search(r'(?im)^[\W_]*locked by sam\b', reply or ''):
        return ['the reply carries a "Locked by Sam" line: Sam asked (23 Nov) for it to stay in the notes only; take it '
                'out of the message']
    return []


def _real_user(entry):
    if entry.get('type') != 'user' or entry.get('isMeta'):
        return False
    c = entry.get('message', {}).get('content')
    if isinstance(c, list):
        return not any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c)
    return isinstance(c, str)


def last_turn(path):
    """(the reply's text this turn, proposal names written this turn) from the chat's own record."""
    try:
        raw = open(path, 'rb').read()[-3_000_000:].decode('utf-8', 'replace').splitlines()
    except (OSError, TypeError):
        return '', set()
    ents = []
    for ln in raw:
        try:
            ents.append(json.loads(ln))
        except ValueError:
            pass
    start = max([i for i, e in enumerate(ents) if _real_user(e)] or [-1]) + 1
    texts, touched = [], set()
    for e in ents[start:]:
        if e.get('type') != 'assistant':
            continue
        for c in e.get('message', {}).get('content') or []:
            if not isinstance(c, dict):
                continue
            if c.get('type') == 'text':
                texts.append(c.get('text', ''))
            elif c.get('type') == 'tool_use':
                inp = c.get('input') or {}
                if c.get('name') in ('Write', 'Edit', 'MultiEdit'):
                    touched |= set(PROP_RE.findall(str(inp.get('file_path', '')) + ' '))
                elif c.get('name') == 'Bash':
                    cmd = str(inp.get('command', ''))
                    if re.search(r'propose\.py (?:new|pack|judge|record)|>\s*\S*notes/proposals/', cmd):
                        touched |= set(re.findall(r'propose\.py (?:new|pack|judge|record) ([\w.-]+)', cmd))
                        touched |= set(PROP_RE.findall(cmd))
    return '\n'.join(texts), touched


def log_unrouted(chat, faults, reply):
    os.makedirs(PROPS, exist_ok=True)
    q = next((q for q, _ in questions(reply)), '')
    with open(_p(UNROUTED), 'a') as f:
        f.write(f'- {datetime.now():%Y-%m-%d %H:%M} chat {chat}: sent after one block: {faults[0][:160]} | '
                f'"{q[:120]}"\n')


# guard-film-questions (adopted 22 Nov, Sam's option 1). Learn step 1: EVERY block is logged, first time included, with
# the whole reply and the retry's length (before, only a second stop was logged, cut at 120 characters). Change 1 (the
# check for Sam's own rule, CLAUDE.md "One message, never twice", 22 Nov): the block tells the chat Sam has already read
# the reply and asks for ONE "Correction:" line; on the retry only the text written after the block is judged, and a
# correction that answers every fault is logged as cleared, not as a let-through.
BLOCKS = 'guard-blocks.jsonl'
CORRECTION_RE = re.compile(r'(?im)^[\W_]*correction\s*:')


def _blocks():
    out = []
    for ln in _read(_p(BLOCKS)).splitlines():
        try:
            out.append(json.loads(ln))
        except ValueError:
            pass
    return out


def _log_block(rec):
    os.makedirs(PROPS, exist_ok=True)
    rec = dict({'t': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}, **rec)
    with open(_p(BLOCKS), 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def correction_needs(faults):
    """What a one-line correction must carry for each fault: (fault, the words it needs or '' for any Correction line)."""
    out = []
    for f in faults:
        m = re.search(r'must carry "(Critiqued: [^"]+)"', f)
        out.append((f, m.group(1) if m else '' if 'Locked by Sam' in f else 'withdrawn'))
    return out


def block_reason(faults, reply):
    """The block's message (Change 1): Sam has read the reply already, so only a one-line correction is sent."""
    asks = [q for q, _ in questions(reply)]
    num = next((m.group(1) for q in asks for m in [re.match(r'\W*(\d+)[.)]', q)] if m), '')
    lines = []
    for f, need in correction_needs(faults):
        if need.startswith('Critiqued'):
            lines.append(f'"Correction: {need}" (the line the proposal\'s ask was missing)')
        elif need == 'withdrawn':
            lines.append(f'"Correction: ignore {"question " + num if num else "my last question"}, it is withdrawn" '
                         '(it goes through the proposal route before Sam is asked again)')
        else:
            lines.append('"Correction: none needed" (the line stays in the notes from now on)')
    return ('Sam has ALREADY READ this reply: this check runs after it is on his screen (CLAUDE.md "One message, never '
            'twice", Sam 22 Nov). Do NOT send the reply again, not even reworded. Send only: '
            + ' and '.join(dict.fromkeys(lines)) + '. Nothing else in that answer. Why it stopped (the proposal route, '
            'Sam 15 Nov): ' + ' | '.join(faults))


def correction_ok(retry, faults):
    """The retry clears the block: a short answer (at most 3 lines) with a Correction line carrying what each fault
    needs. Returns (ok, why)."""
    body = [ln for ln in (retry or '').splitlines() if ln.strip()]
    if not CORRECTION_RE.search(retry or ''):
        return False, 'no "Correction:" line'
    if len(body) > 3:
        return False, f'{len(body)} lines (a correction is one line)'
    miss = [need for _, need in correction_needs(faults) if need and need.lower() not in retry.lower()]
    return (not miss), ('missing ' + ', '.join(f'"{m}"' for m in miss)) if miss else 'cleared'


def _resent_share(blocked, retry):
    """How much of the blocked reply came back in the retry (share of its lines of 16+ characters)."""
    lines = [ln.strip() for ln in blocked.splitlines() if len(ln.strip()) >= 16]
    if not lines:
        return 0.0
    return sum(1 for ln in lines if ln in retry) / len(lines)


def _retry_text(reply, blocked, last_msg):
    b = (blocked or '').strip()
    i = reply.find(b) if b else -1
    if i >= 0:
        return reply[i + len(b):].strip()
    return (last_msg or '').strip()


def hook(stdin=None):
    try:
        data = json.loads(stdin if stdin is not None else sys.stdin.read() or '{}')
    except ValueError:
        return 0
    reply, touched = last_turn(data.get('transcript_path'))
    if data.get('last_assistant_message') and data['last_assistant_message'] not in reply:
        reply += '\n' + data['last_assistant_message']
    chat = os.path.basename(data.get('transcript_path') or 'unknown')[:8]
    pending = None
    if data.get('stop_hook_active'):
        pending = next((b for b in reversed(_blocks()) if b.get('chat') == chat and b.get('event') == 'block'
                        and not b.get('answered')), None)
    if pending:                               # the retry after this guard's own block: judge only what came after it
        retry = _retry_text(reply, pending.get('reply', ''), data.get('last_assistant_message'))
        ok, why = correction_ok(retry, pending.get('faults', []))
        share = _resent_share(pending.get('reply', ''), retry)
        _log_block({'chat': chat, 'event': 'retry', 'of': pending.get('t'), 'retry_chars': len(retry),
                    'shape': 'full' if share >= 0.5 else 'short' if len(retry) <= 400 else 'long',
                    'resent_share': round(share, 2), 'result': 'cleared' if ok else 'let-through', 'why': why,
                    'retry': retry[:4000]})
        _mark_answered(pending)
        if not ok:
            log_unrouted(chat, pending.get('faults') or ['(faults not kept)'], pending.get('reply', reply))
        return 0
    faults = reply_faults(reply, touched) + locked_line(reply)
    if not faults:
        return 0
    if __import__('override').skip('proposal route stop: ' + ' | '.join(faults), data.get('transcript_path'), sys.stderr):
        return 0
    if data.get('stop_hook_active'):          # another hook blocked first: never loop; leave a trace for the handover
        log_unrouted(chat, faults, reply)
        return 0
    _log_block({'chat': chat, 'event': 'block', 'faults': faults, 'asks': [q for q, _ in questions(reply)],
                'reply_chars': len(reply), 'reply': reply})
    print(json.dumps({'decision': 'block', 'reason': block_reason(faults, reply)}))
    return 0


def _mark_answered(rec):
    """A block whose retry has been judged is not judged again (rewrites its line with answered: true)."""
    rows = _blocks()
    for r in rows:
        if r.get('chat') == rec.get('chat') and r.get('t') == rec.get('t') and r.get('event') == 'block':
            r['answered'] = True
    with open(_p(BLOCKS), 'w', encoding='utf-8') as f:
        f.write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))


def blocks_report(since=''):
    """The full block log in numbers (the measure for guard-film-questions: full repeated replies per chat to 0)."""
    rows = [r for r in _blocks() if r.get('t', '') >= since]
    blocks = [r for r in rows if r.get('event') == 'block']
    retries = [r for r in rows if r.get('event') == 'retry']
    out = [f'guard blocks since {since or "the start"}: {len(blocks)}; retries judged {len(retries)}: '
           f'{sum(r["result"] == "cleared" for r in retries)} cleared, '
           f'{sum(r["result"] == "let-through" for r in retries)} let through; '
           f'full repeated replies {sum(r.get("shape") == "full" for r in retries)}']
    for r in retries:
        if r.get('shape') == 'full' or r.get('result') != 'cleared':
            out.append(f'  {r["t"]} chat {r["chat"]}: {r.get("shape")} ({r.get("retry_chars")} chars), '
                       f'{r["result"]}: {r.get("why")}')
    return '\n'.join(out)


# ------------------------------------------------------------------------------------------------ step 6
SCOPE = ('CLAUDE.md', 'guides/', '.claude/', 'source/')


def review(film, since=None):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ledger
    d = ledger.load(film)
    since = since or min([c['date'] for c in d['chats']] or ['2026-01-01'])
    spent, rounds, notes, reps = ledger.totals(d)
    films = {os.path.basename(f)[:-5].replace('-', '_') for f in glob.glob(os.path.join(ledger.DIR, '*.json'))}
    log = subprocess.run(['git', '-C', ROOT, 'log', f'--since={since}', '--name-only', '--format=@@%h %ad %s',
                          '--date=short', '--no-merges'], capture_output=True, text=True).stdout
    changes = []
    for block in log.split('@@')[1:]:
        head, *files = [x for x in block.splitlines() if x.strip()]
        sys_files = [f for f in files if f.startswith(SCOPE) and not any(
            os.path.basename(f).startswith(fm) for fm in films) and not f.startswith('source/data/')]
        if sys_files:
            changes.append((head, sys_files))
    replaced = [os.path.basename(f)[:-3] for f in glob.glob(_p('*.md')) if re.search(r'^Status: replaced', _read(f), re.M)]
    out = [f'# End-of-film review: {film} (the proposal route, step 6)', '',
           f'Results: spent {spent}% of a week against an estimate of {d.get("estimate")}%; {rounds} rounds, {notes} '
           f'notes, {len(reps)} repeated notes. Proposals later replaced: {len(replaced)} {replaced or ""}.', '',
           'Starting chats (cold-start, for Sam in one line): ' + (ledger.coldstart(d) or 'no start figures recorded'),
           '',
           f'## Every change to the system since {since} ({len(changes)} commits)',
           'For each: did it help THIS film (its notes, faults Sam caught, cost)? keep / needs changing (-> '
           '`propose.py new`, the route). Nothing temporary: a change is kept or properly replaced.', '']
    for head, files in changes:
        out.append(f'- {head} ({", ".join(files[:6])}{" ..." if len(files) > 6 else ""}): ')
    import dearest                                 # cost audit (Sam, 21 Nov): the five dearest things, each a proposal
    text, _, _ = dearest.report(film)               # Sam, 21 Nov: suggested to him first; the route only on his picks
    named, _ = dearest.suggestions(film)
    out += ['', '## The five dearest things (source/dearest.py): suggest them to Sam, numbered', '', text, '']
    out += [f'{i}. {k} ({v:g}% of a week)' for i, (k, v, _) in enumerate(named, 1)]
    out += ['', f'Open only the ones Sam picks: python3 source/dearest.py {film} --open N,N (then the route on each)']
    out += ['', '## Lessons, each in the fixed fields (CLAUDE.md "Back-end proposals are explained plainly"; '
            f'checked by `propose.py plain notes/proposals/review-{film}.md`)', '',
            '### Lesson 1: short plain name', 'Problem: one or two plain sentences.', '1. first step',
            '2. second step', 'Why: ...', "You'd notice: ...", 'Other option: ...', 'Lost: ...', 'Added: ...']
    f = _p(f'review-{film}.md')
    os.makedirs(PROPS, exist_ok=True)
    open(f, 'w').write('\n'.join(out) + '\n')
    print(f'propose: review written to {os.path.relpath(f, ROOT)}: {len(changes)} changes to judge against the '
          f'film\'s results ({notes} notes, {spent}% spent)')


def lock(verdict=None):
    if _read(LOCK).strip() and not verdict:
        sys.exit('propose: the prompts are locked; a change to them needs a proposal with a valid verdict '
                 '(`propose.py lock --verdict NAME`)')
    if verdict:
        ok, why = verdict_ok(verdict)
        if not ok:
            sys.exit('propose: ' + why)
    open(LOCK, 'w').write(prompts_hash() + '\n')
    print(f'propose: prompts locked at {prompts_hash()}')


def unrouted_for(chat):
    """handover.py end: this chat's replies that went to Sam after a block and are not yet settled (lesson 7 step 3,
    fail closed: the handover is refused until each is settled; naming it in the notes no longer clears it)."""
    return [ln.strip() for ln in _read(_p(UNROUTED)).splitlines() if f' chat {chat}:' in ln and SETTLED not in ln]


SETTLED = ' || settled: '
CLOSED_FROM = '2026-11-23'                         # lesson 7 step 3 began; older let-throughs are history (rule table)


def open_letthroughs(since=CLOSED_FROM):
    """Every unsettled let-through since step 3 began, from any chat: finish.py refuses an animatic while one stands."""
    return [ln.strip() for ln in _read(_p(UNROUTED)).splitlines()
            if ln.startswith('- ') and ln[2:12] >= since and SETTLED not in ln]


def settle(chat, why):
    """Settle this chat's let-throughs: 'routed: NAME' (put through the route since) or 'false block: why' (the guard
    was wrong; counted for the end-of-film review). Returns how many lines were settled."""
    if not re.match(r'(routed: [\w.-]+|false block: .{8,})', why):
        sys.exit('propose: settle needs "routed: PROPOSAL" or "false block: why (8+ characters)"')
    if why.startswith('routed: ') and not os.path.exists(_p(why[8:].strip() + '.md')):
        sys.exit(f'propose: no proposal {why[8:].strip()} in notes/proposals/')
    lines, n = _read(_p(UNROUTED)).splitlines(True), 0
    for i, ln in enumerate(lines):
        if f' chat {chat}:' in ln and SETTLED not in ln:
            lines[i], n = ln.rstrip('\n') + SETTLED + why + '\n', n + 1
    open(_p(UNROUTED), 'w').write(''.join(lines))
    return n


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    opt = lambda k: rest[rest.index(k) + 1] if k in rest else None
    if cmd == 'hook':
        __import__('hookran').ran('propose.py hook')
        return hook()
    if cmd == 'new':
        new(rest[0], ' '.join(rest[1:]) or rest[0])
    elif cmd == 'pack':
        pack(rest[0])
    elif cmd == 'judge':
        judge(rest[0])
    elif cmd == 'record':
        record(rest[0])
    elif cmd == 'settle':                        # lesson 7 step 3: propose.py settle CHAT8 "routed: NAME" | "false block: why"
        print(f'propose: {settle(rest[0][-8:], " ".join(rest[1:]))} let-through(s) settled')
    elif cmd == 'show':
        show(rest[0])
    elif cmd == 'reader':
        return reader(rest[0])
    elif cmd == 'plain':
        return plain(rest[0])
    elif cmd == 'blocks':
        print(blocks_report(opt('--since') or ''))
    elif cmd == 'status':
        status()
    elif cmd == 'mark':
        mark(rest[0], rest[1])
    elif cmd == 'review':
        review(rest[0], opt('--since'))
    elif cmd == 'lock':
        lock(opt('--verdict'))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
