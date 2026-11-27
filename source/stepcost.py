#!/usr/bin/env python3
"""stepcost: what each kind of step cost a chat (history-and-search Learn, Sam's 1 on 16 Nov; chat 6b).

MAP
  KINDS ........ film-file search, tool search, whole-file .py read, page.py, routine (modelguard.routine), renders, pictures, other (+ helpers,
                 the chat's critique and other agents, kept apart so they are not hidden in "other")
  kind_of() .... one tool call -> its kind. A search is Grep/Glob, a Read with offset/limit, or a shell grep/rg/
                 find/awk/sed -n/head/tail; it is a film-file search when it names the film's own files
                 (source/FILM*.py, story/FILM*), a tool search otherwise. page.py first, so `page.py show` is never
                 counted as a search
  measure() .... a transcript -> steps (API calls of the main chat), history at the end (tokens), and each kind's
                 share of the chat's cost (%). F4 checked 16 Nov: every assistant line carries its own usage, so
                 cost is read, not guessed. Each tool call is charged what it added (its result, written to the
                 cache once at the write price) plus re-reading it at every later step until a compaction, plus
                 the output that asked for it. What no call explains (the start-up reading, Claude's own words,
                 reminders) is "other"
  split() ...... cost-other change 1 (Sam's Y, 19 Nov): every dollar by block (start-up floor, carried history, new
                 writes, Claude's words, helpers) and by origin (which kind of tool result, Claude's own words or
                 edits, messages and reminders, cache re-write, the floor), exact: the parts add to the chat's bill;
                 'unexplained' (leftover) is only growth with nothing arriving. Number to beat: leftover under 5% on
                 every chat of the next film; three chats within 5% of the app's figure
  thing_of() / wrote_of()  cost audit (Sam, 21 Nov): every call's result and every piece of Claude's output gets a plain
                 name (reading notes, reading film code, writing code, thinking (exact, from the usage), messages to
                 Sam, critique helpers ...); split() returns them as 'named', adding up to the bill. source/dearest.py
                 ranks them per film and per week
  start() ...... cold-start change (Sam's Y, 19 Nov): four start figures per chat: step-1 context, steps and % of a
                 week to the first real work, the files read before it (with sizes and cost), base share. ledger.py
                 coldstart FILM turns them into the film-end line (start + re-learning as % of the film)
  test ......... `python3 source/stepcost.py test`: on tests/stepcost-transcript.jsonl (a real chat's transcript,
                 trimmed to usage and tool calls) and on this chat's own transcript when there is one

    python3 source/stepcost.py TRANSCRIPT.jsonl [--film FILM]     (prints the measure)
    python3 source/stepcost.py test

Called by ledger.py auto (the Stop hook) on every chat; the figures go into the chat's ledger row.
"""
import glob, json, os, re, shlex, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
import costwatch  # noqa: E402

KINDS = ['film-file search', 'tool search', 'whole-file .py read', 'page.py', 'routine', 'renders', 'pictures', 'other',
         'helpers']
import modelguard  # noqa: E402  (cost-fixes, model guard: 'routine' = what the guard stops on Opus; its share on an
#                    Opus row is the film's routine-on-Opus figure, number to beat under 0.5% of a week a film)
SEARCH_CMDS = {'grep', 'egrep', 'rg', 'ack', 'find', 'awk', 'head', 'tail'}   # ls is not a search (finder-use, 17 Nov)
IMG = re.compile(r'\.(png|jpe?g|gif|webp)$', re.I)
RENDER = re.compile(r'\b(final|animatic|render|clip|sheet|finish\.py|ffmpeg|blender)\b')
COMPACT = 0.6            # a step whose history is under 60% of the one before follows a compaction


def _film_paths(film):
    code = (film or '').replace('-', '_')
    if not code:
        return re.compile(r'(?!x)x')
    codes = [code]
    words = [w for w in code.split('_') if w]
    if len(words) >= 3:                       # cost audit (21 Nov): GTA's code is gta_*.py, its initials
        codes.append(''.join(w[0] for w in words))
    alt = '|'.join(re.escape(c) for c in codes)
    return re.compile(r'(?:source/(?:%s)[A-Za-z0-9_]*\.py|story/(?:%s|%s)[^\s\'"]*)' % (
        alt, alt, re.escape(code.replace('_', '-'))))


# cost audit (Sam, 21 Nov: "find the most expensive things"): every dollar named as a THING a person would
# recognise, not "other". Results are named by what was read or run; Claude's own output by what it wrote.
THINGS_START = 'start-up and handover tools'
START_RE = re.compile(r'\b(handover|branches|ledger|page|propose|watcher|status|plaincheck)\.py\b')


def _where(t):
    if re.search(r'(?:^|[\s\'"/])(?:notes|story)/', t):
        return 'notes'
    if 'guides/' in t or 'CLAUDE.md' in t:
        return 'guides'
    if re.search(r'(?:source|\.claude/hooks|tests)/|\.py\b', t):
        return 'code'
    return ''


def thing_of(name, inp, film_re):
    """What one tool call's RESULT was, in plain words (the thing it put into the chat)."""
    inp = inp or {}
    if name == 'Bash':
        cmd = inp.get('command', '')
        heads = [w[0].split('/')[-1] for w in _segments(cmd)]
        if START_RE.search(cmd):
            return THINGS_START
        if RENDER.search(cmd) and (re.search(r'source/\S+\.py', cmd) or 'ffmpeg' in cmd or 'blender' in cmd):
            return 'renders'
        if any(h in ('python3', 'python') for h in heads) and re.search(r'source/\S+\.py', cmd):
            return 'running checks and tools'
        if 'git' in heads and all(h in ('git', 'cd', 'for', 'do', 'done', 'sleep', 'echo', 'break', 'head', 'tail',
                                        'grep', '||', '&&') for h in heads):
            return 'git and saving'
        if re.search(r'\.jsonl\b|\.claude/projects', cmd):
            return 'reading chat records'
        w = _where(cmd)
        if any(h in SEARCH_CMDS or h in ('cat', 'sed', 'wc', 'ls', 'python3', 'python') for h in heads) and w:
            return 'reading ' + w if w != 'code' else ('reading film code' if film_re.search(cmd) else 'reading kit code')
        return 'small shell commands (listing, moving, copying)'
    if name in ('Read', 'Grep', 'Glob'):
        t = ' '.join(str(inp.get(k, '')) for k in ('file_path', 'path', 'glob', 'pattern'))
        if name == 'Read' and IMG.search(inp.get('file_path', '')):
            return 'looking at pictures'
        w = _where(t)
        if w == 'code':
            return 'reading film code' if film_re.search(t) else 'reading kit code'
        return 'reading ' + w if w else 'reading files outside the project (scratch, logs)'
    if name in EDIT_TOOLS:
        return 'edit results'
    if name in ('Agent', 'Task'):
        return 'helper results'
    if name == 'ToolSearch':
        return 'tool lookups'
    if re.search(r'list_events|list_sessions|get_session|get_event', name):
        return 'reading chat records'
    return 'app tools (chats, files sent)'


def wrote_of(name, inp):
    """What one tool call's INPUT was, i.e. what Claude wrote to make it."""
    inp = inp or {}
    if name in EDIT_TOOLS:
        f = inp.get('file_path', '')
        return 'writing notes' if _where(f) in ('notes', 'guides') else 'writing code'
    if name == 'Bash':
        cmd = inp.get('command', '')
        if '<<' in cmd or 'python3 -c' in cmd:
            return 'writing notes' if re.search(r"open\(\s*['\"](?:notes|story|guides)/|p\s*=\s*['\"](?:notes|story)/", cmd) \
                else 'writing code'
        return 'commands'
    if name in ('Agent', 'Task') or name.endswith('create_session') or name.endswith('send_message'):
        return 'helper and chat prompts'
    return 'commands'


def _segments(cmd):
    """The commands in a shell line (split on && ; || | and newlines), each as its words."""
    out = []
    for part in re.split(r'&&|\|\||[;|\n]', cmd):
        try:
            w = shlex.split(part, comments=True)
        except ValueError:
            w = part.split()
        while w and ('=' in w[0] and not w[0].startswith('-')):
            w = w[1:]                              # VAR=x cmd
        if w:
            out.append(w)
    return out


def kind_of(name, inp, film_re):
    """One tool call -> its kind."""
    inp = inp or {}
    if name == 'Bash':
        cmd = inp.get('command', '')
        if 'page.py' in cmd:
            return 'page.py'
        if modelguard.routine(cmd):
            return 'routine'
        segs = _segments(cmd)
        heads = [w[0].split('/')[-1] for w in segs]
        search = any(h in SEARCH_CMDS or (h == 'sed' and '-n' in w) for h, w in zip(heads, segs))
        if search and not any(h in ('python3', 'python') for h in heads):
            return 'film-file search' if film_re.search(cmd) else 'tool search'
        if RENDER.search(cmd) and (re.search(r'source/\S+\.py', cmd) or 'ffmpeg' in cmd or 'blender' in cmd):
            return 'renders'
        if any(h == 'cat' and any(a.endswith('.py') for a in w) for h, w in zip(heads, segs)) and not search:
            return 'whole-file .py read'
        if search:
            return 'film-file search' if film_re.search(cmd) else 'tool search'
        return 'other'
    if name in ('Grep', 'Glob'):
        where = ' '.join(str(inp.get(k, '')) for k in ('path', 'glob', 'pattern'))
        return 'film-file search' if film_re.search(where) else 'tool search'
    if name == 'Read':
        p = inp.get('file_path', '')
        if IMG.search(p):
            return 'pictures'
        if p.endswith('.py'):
            if inp.get('offset') or inp.get('limit'):
                return 'film-file search' if film_re.search(p) else 'tool search'
            return 'whole-file .py read'
        return 'other'
    return 'other'


def _result_tokens(block):
    """Rough tokens a tool result adds: text at 4 characters a token, a picture ~1,600."""
    c = block.get('content')
    if isinstance(c, str):
        return len(c) / 4
    n = 0
    for x in c or []:
        if isinstance(x, dict) and x.get('type') == 'image':
            n += 1600
        elif isinstance(x, dict):
            n += len(x.get('text', '') or json.dumps(x)) / 4
    return n


def _has_image(block):
    c = block.get('content')
    return isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'image' for x in c)


def measure(path, film=None, helpers=True):
    """steps, history at the end (tokens), total $ (main chat + helpers) and each kind's share (% of that total)."""
    film_re = _film_paths(film)
    steps, calls, results = [], {}, {}      # steps: [usage, model, [tool_use ids]]; results: id -> (step, tokens)
    byid = {}
    for raw in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get('isSidechain'):
            continue
        m = d.get('message')
        if not isinstance(m, dict):
            continue
        if d.get('type') == 'assistant' and m.get('usage'):
            mid = m.get('id')
            if mid not in byid:
                byid[mid] = len(steps)
                steps.append([m['usage'], m.get('model'), []])
            k = byid[mid]
            for b in m.get('content') or []:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    calls[b['id']] = (k, kind_of(b.get('name'), b.get('input'), film_re),
                                      thing_of(b.get('name'), b.get('input'), film_re))
                    steps[k][2].append(b['id'])
        elif d.get('type') == 'user' and isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('type') == 'tool_result':
                    results[b.get('tool_use_id')] = (len(steps), _result_tokens(b), _has_image(b))
    if not steps:
        return None
    ctx = [u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
           for u, _, _ in steps]
    seg, s = [], 0
    for i, c in enumerate(ctx):
        if i and c < COMPACT * ctx[i - 1]:
            s += 1
        seg.append(s)
    price = [costwatch.PRICE[costwatch.fam(mo)] for _, mo, _ in steps]
    cost = [(u.get('cache_read_input_tokens', 0) * p[0] + u.get('cache_creation_input_tokens', 0) * p[1]
             + u.get('input_tokens', 0) * p[2] + u.get('output_tokens', 0) * p[3]) / 1e6
            for (u, _, _), p in zip(steps, price)]
    main = sum(cost)
    by = dict.fromkeys(KINDS, 0.0)
    arrive = {}                                      # step a result is first read at -> [(id, tokens)]
    for tid, (k, tok, _) in results.items():
        if tid in calls and k < len(steps):
            arrive.setdefault(k, []).append((tid, tok))
    for k, rs in arrive.items():
        u = steps[k][0]
        avail = max(0.0, u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
                    - (steps[k - 1][0].get('output_tokens', 0) if k else 0))
        est = sum(t for _, t in rs) or 1.0
        scale = min(1.0, avail / est)
        later = sum(1 for j in range(k + 1, len(steps)) if seg[j] == seg[k])
        r, w = price[k][0], price[k][1]
        for tid, tok in rs:
            add = tok * scale
            kind = calls[tid][1]
            if results[tid][2] and kind == 'other':
                kind = 'pictures'
            if kind == 'other':                      # Sam, 28 Nov: nothing left as "other": its plain name
                kind = calls[tid][2]
            by[kind] = by.get(kind, 0.0) + add * (w + r * later) / 1e6
    for k, (u, _, ids) in enumerate(steps):          # the output that asked for each call, shared between them
        if ids:
            share = u.get('output_tokens', 0) * price[k][3] / 1e6 / len(ids)
            for tid in ids:
                kk = calls[tid][1] if calls[tid][1] != 'other' else calls[tid][2]
                by[kk] = by.get(kk, 0.0) + share
    named = sum(by.values())
    if named > main:                                 # estimates never claim more than the chat spent
        for kk in by:
            by[kk] *= main / named
        named = main
    rest = main - named                              # what no call explains: named from the exact split's origins
    try:
        sp = split(path, film) if helpers else None
    except Exception:
        sp = None
    og = {OTHER_NAMES[k]: v for k, v in ((sp or {}).get('origins') or {}).items() if k in OTHER_NAMES}
    tot = sum(og.values())
    for k, v in og.items():
        by[k] = by.get(k, 0.0) + rest * v / tot
    if not tot:
        by["Claude's words, start-up and messages"] = by.get("Claude's words, start-up and messages", 0.0) + rest
    by['other'] = 0.0
    if helpers:
        for h in costwatch.helper_files(path):
            hm = measure(h, film, helpers=False)
            if hm:
                by['helpers'] += hm['usd']
    total = sum(by.values())
    try:
        srch = search_record(path, film)
    except Exception:
        srch = None
    try:
        cs = start(path, film) if helpers else None
    except Exception:
        cs = None
    return {'steps': len(steps), 'hist': ctx[-1], 'usd': round(total, 4), 'search': srch, 'split': sp, 'start': cs,
            'kinds': {k: round(100 * v / total, 1) for k, v in by.items() if total and round(100 * v / total, 1)},
            'calls': {k: sum(1 for _, kk, _t in calls.values() if kk == k) for k in KINDS if k != 'helpers'}}


EDIT_TOOLS = {'Edit', 'Write', 'NotebookEdit', 'MultiEdit'}
# Sam, 28 Nov ("anything usually labelled 'other' gets an appropriate category"): the cost no tool call explains,
# named by the exact split's origins (split()); a step's own "other" kind takes thing_of()'s plain name
OTHER_NAMES = {"Claude's words": "Claude's words (thinking and writing)", 'start-up floor': 'start-up reading',
               'cache re-write': 'memory lapses (re-paying for the whole chat after a gap)',
               'messages and reminders': 'messages and reminders', 'unexplained': 'unexplained'}
BLOCKS = ['start-up floor', 'carried history', 'new writes', "Claude's words", 'helpers']


def _msg_tokens(d):
    """Rough tokens a non-tool line adds to the chat (Sam's message, a reminder, a hook's output): 4 characters each."""
    m = d.get('message')
    if isinstance(m, dict):
        c = m.get('content')
        if isinstance(c, str):
            return len(c) / 4
        return sum(len(b.get('text', '') or '') / 4 for b in c or [] if isinstance(b, dict) and b.get('type') == 'text')
    if d.get('type') in ('attachment', 'system'):
        return len(json.dumps(d.get('attachment') or d.get('content') or '')) / 4
    return 0


NAMED_COARSE = {'start-up floor': 'start-up reading (rules, tools, first files)', 'cache re-write': 'memory lapses (re-paying for the whole chat)',
                'messages and reminders': 'messages and reminders', 'unexplained': 'unexplained', 'helpers': 'helpers'}


def _words_parts(st, edits=True):
    """One step's output by what it was: thinking (exact, from the usage), then the visible output shared by the
    size of what was written (messages to Sam, code, notes, commands, prompts)."""
    u = st['u']
    th = (u.get('output_tokens_details') or {}).get('thinking_tokens', 0) or 0
    vis = max(0, u.get('output_tokens', 0) - th)
    out = {k: v for k, v in st['out'].items()}
    if not edits:
        for k, v in st['edit_thing'].items():
            out[k] = max(0, out.get(k, 0) - v)
    tot = sum(out.values())
    parts = {'thinking': th} if th else {}
    for k, v in out.items():
        if tot and v:
            parts[k] = parts.get(k, 0) + vis * v / tot
    if not tot and vis:
        parts['messages to Sam'] = vis
    return parts


def _shares(coarse, amount, parts, default='thinking'):
    """Spread an amount over named parts: {'coarse|part': amount x share}."""
    tot = sum(parts.values())
    if not amount:
        return {}
    if not tot:
        return {coarse + '|' + default: amount}
    return {coarse + '|' + k: amount * v / tot for k, v in parts.items() if v}


def _helper_name(path):
    """A helper's kind (critic, namer, general-purpose...) from the record beside it, else 'helpers'."""
    meta = os.path.splitext(path)[0] + '.meta.json'
    try:
        t = json.load(open(meta)).get('agentType') or ''
    except Exception:
        t = ''
    if not t:
        try:
            for raw in open(path, encoding='utf-8', errors='replace'):
                d = json.loads(raw)
                t = d.get('subagent_type') or d.get('agentType') or ''
                if t:
                    break
                if d.get('type') == 'user':
                    c = json.dumps(d.get('message', {}).get('content', ''))[:600]
                    t = ('critique' if 'critique' in c else 'proposal' if 'propos' in c else
                         'name test' if 'nametest' in c else '')
                    break
        except Exception:
            pass
    return {'critic': 'critique helpers', 'critique': 'critique helpers', 'namer': 'name-test helpers',
            'proposal': 'proposal helpers'}.get(t, 'other helpers' if t in ('', 'general-purpose') else t + ' helpers')


def split(path, film=None, helpers=True):
    """cost-other change 1 (Sam's Y, 19 Nov): every dollar of the main chat by block AND by origin, exactly.

    Each step's bill is read x read price + write x write price + input x input price + output x output price.
    Blocks: start-up floor (the step-1 context, written once, then re-read at every later step until a compaction;
    after one, the summary is that part's floor), carried history (the rest of each re-read), new writes (what each
    step adds, and history written again after a cache miss), Claude's words (output). Origins: what put the tokens
    there: a tool call's result (by kind), Claude's own words or edits (its earlier output, carried), messages and
    reminders, cache re-write, the floor. A step's new tokens are its context minus the step before's, so each
    origin's share is scaled to what really arrived; 'unexplained' is only growth with nothing arriving (leftover).
    Returns usd (main chat), floor_k (step-1 context), blocks and origins in $ and %, leftover %."""
    film_re = _film_paths(film)
    steps, byid = [], {}                  # step: dict(u, price, arr={origin: est tokens}, edits=tokens of edit input)
    pend = {}
    for raw in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get('isSidechain'):
            continue
        m = d.get('message')
        if d.get('type') == 'assistant' and isinstance(m, dict) and m.get('usage'):
            mid = m.get('id')
            if mid not in byid:
                byid[mid] = len(steps)
                steps.append({'u': m['usage'], 'price': costwatch.PRICE[costwatch.fam(m.get('model'))],
                              'arr': pend, 'edits': 0.0, 'kind': {}, 'out': {}, 'edit_thing': {}})
                pend = {}
            st = steps[byid[mid]]
            for b in m.get('content') or []:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    st['kind'][b['id']] = (kind_of(b.get('name'), b.get('input'), film_re) + '|'
                                           + thing_of(b.get('name'), b.get('input'), film_re))
                    n = len(json.dumps(b.get('input') or {})) / 4
                    w = wrote_of(b.get('name'), b.get('input'))
                    st['out'][w] = st['out'].get(w, 0) + n
                    if b.get('name') in EDIT_TOOLS:
                        st['edits'] += n
                        st['edit_thing'][w] = st['edit_thing'].get(w, 0) + n
                elif isinstance(b, dict) and b.get('type') == 'text':
                    st['out']['messages to Sam'] = st['out'].get('messages to Sam', 0) + len(b.get('text', '')) / 4
            continue
        if d.get('type') == 'user' and isinstance(m, dict) and isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('type') == 'tool_result':
                    k = next((s['kind'][b.get('tool_use_id')] for s in reversed(steps[-3:])
                              if b.get('tool_use_id') in s['kind']), 'other|other tool results')
                    if _has_image(b) and k.startswith('other|'):
                        k = 'pictures|looking at pictures'
                    o = 'result: ' + k
                    pend[o] = pend.get(o, 0) + _result_tokens(b)
        t = _msg_tokens(d)
        if t:
            pend['messages and reminders'] = pend.get('messages and reminders', 0) + t
    if not steps:
        return None
    blocks = dict.fromkeys(BLOCKS, 0.0)
    origins = {}
    add = lambda o, v: origins.__setitem__(o, origins.get(o, 0.0) + v)
    floor = carried = 0.0
    held = {}                                          # origin -> tokens carried in this part of the chat
    prev_ctx = 0
    for k, st in enumerate(steps):
        u, (pr, pw, pi, po) = st['u'], st['price']
        R, W, I, O = (u.get('cache_read_input_tokens', 0), u.get('cache_creation_input_tokens', 0),
                      u.get('input_tokens', 0), u.get('output_tokens', 0))
        ctx = R + W + I
        wprice = (W * pw + I * pi) / max(1, W + I)     # $ a token for this step's new writes
        if k == 0 or ctx < COMPACT * prev_ctx:         # a new part: everything in it is its floor
            floor, held = ctx, {}
            v = (R * pr + W * pw + I * pi) / 1e6
            blocks['start-up floor'] += v
            add('start-up floor', v)
        else:
            fr = min(R, floor)
            v = fr * pr / 1e6
            blocks['start-up floor'] += v
            add('start-up floor', v)
            hist = R - fr                              # carried history, shared by what put it there
            tot = sum(held.values())
            if hist:
                if tot:
                    for o, n in held.items():
                        vv = hist * n / tot * pr / 1e6
                        blocks['carried history'] += vv
                        add(o, vv)
                else:
                    vv = hist * pr / 1e6
                    blocks['carried history'] += vv
                    add('start-up floor', vv)
            grow = max(0, ctx - prev_ctx)              # what really arrived since the step before
            new = min(W + I, grow)
            rew = (W + I) - new                        # written again: the cache missed or expired
            if rew:
                v = rew * wprice / 1e6
                blocks['new writes'] += v
                add('cache re-write', v)
            po_prev = steps[k - 1]['u'].get('output_tokens', 0)
            mine = min(new, po_prev)
            ed = min(mine, steps[k - 1]['edits'])
            got = {}
            for o, n in _shares("Claude's edits", ed, steps[k - 1]['edit_thing'], 'writing code').items():
                got[o] = got.get(o, 0) + n
            for o, n in _shares("Claude's words", mine - ed, _words_parts(steps[k - 1], edits=False)).items():
                got[o] = got.get(o, 0) + n
            rest = new - mine
            est = sum(st['arr'].values())
            if rest and est:
                for o, n in st['arr'].items():
                    got[o] = got.get(o, 0) + rest * n / est
            elif rest:
                got['unexplained'] = rest
            for o, n in got.items():
                if n:
                    v = n * wprice / 1e6
                    blocks['new writes'] += v
                    add(o, v)
                    held[o] = held.get(o, 0) + n
        v = O * po / 1e6
        blocks["Claude's words"] += v
        for o, n in _shares("Claude's words", v, _words_parts(st)).items():
            add(o, n)
        prev_ctx = ctx
    usd = sum(blocks.values())
    hu = 0.0
    helper_names = {}
    for h in (costwatch.helper_files(path) if helpers else []):
        hm = split(h, film, helpers=False)
        if hm:
            hu += hm['usd']
            nm = _helper_name(h)
            helper_names[nm] = helper_names.get(nm, 0.0) + hm['usd']
    blocks['helpers'] = hu
    for name, v in helper_names.items():
        add('helpers|' + name, v)
    total = usd + hu
    named = {}
    for o, v in origins.items():
        coarse, _, fine = o.partition('|')
        t = fine or NAMED_COARSE.get(coarse, coarse)
        named[t] = named.get(t, 0.0) + v
    coarse_o = {}
    for o, v in origins.items():
        c = o.partition('|')[0]
        coarse_o[c] = coarse_o.get(c, 0.0) + v
    origins = coarse_o
    pc = lambda dct: {k: round(100 * v / total, 1) for k, v in sorted(dct.items(), key=lambda kv: -kv[1])
                      if total and round(100 * v / total, 1)}
    return {'usd': round(usd, 4), 'total': round(total, 4), 'floor_k': round(steps[0]['u'].get('cache_read_input_tokens', 0)
            + steps[0]['u'].get('cache_creation_input_tokens', 0) + steps[0]['u'].get('input_tokens', 0)) // 1000,
            'blocks': pc(blocks), 'origins': pc(origins), 'named': pc(named),
            'leftover': round(100 * origins.get('unexplained', 0) / total, 1) if total else 0.0}


def split_line(sp):
    """One line: blocks, then the three biggest origins, then the leftover."""
    if not sp:
        return ''
    b = ', '.join(f'{k} {v:g}%' for k, v in sp['blocks'].items())
    o = ', '.join(f'{k} {v:g}%' for k, v in list(sp['origins'].items())[:3])
    return f"{b}. Biggest origins: {o}. Leftover {sp['leftover']:g}%"


FILE_RE = re.compile(r'[\w./-]*(?:source|guides|notes|story|research|tests|\.claude)/[\w./-]+|[\w./-]*CLAUDE\.md')
CHECK_RE = re.compile(r'\b(preflight|check|checks|critique|sheet)\b')


def _real_work(name, inp, film_re):
    """cold-start, figure 2: the chat's first real work: an edit or write outside notes/ (and outside the scratchpad),
    or a render or check on the film's own files. A rule of thumb (F6): some chats start differently."""
    inp = inp or {}
    if name in EDIT_TOOLS:
        f = inp.get('file_path', '')
        return bool(f) and '/notes/' not in f and not f.startswith('notes/') and not re.search(r'^/tmp/|scratchpad', f)
    if name != 'Bash':
        return False
    cmd = inp.get('command', '')
    if film_re.search(cmd) and (RENDER.search(cmd) or CHECK_RE.search(cmd)):
        return True
    if re.search(r"(?:sed -i[^|;&]*|open\(\s*['\"]|>\s*)(?:\S*/)?(?:source|story|guides|animations|\.claude)/", cmd):
        return True
    return bool(re.search(r",\s*['\"][wa]['\"]\s*\)", cmd) and re.search(r"['\"](?:\S*/)?(?:source|story|guides|\.claude)/", cmd))


def _read_files(name, inp):
    """The files one call reads in (a Read, or a shell cat / sed -n / head / tail): repo paths, short."""
    inp = inp or {}
    if name == 'Read':
        f = inp.get('file_path', '')
        return [re.sub(r'^.*?/(?=(?:source|guides|notes|story|research|tests|\.claude)/|CLAUDE\.md)', '', f)] if f else []
    if name != 'Bash':
        return []
    cmd = inp.get('command', '')
    out = []
    for w in _segments(cmd):
        h = w[0].split('/')[-1]
        if h in ('cat', 'head', 'tail') or (h == 'sed' and '-n' in w) or (h.startswith('python') and 'show' in w):
            out += [x for x in w[1:] if FILE_RE.fullmatch(x)]
    return list(dict.fromkeys(out))


def start(path, film=None):
    """cold-start change (Sam's Y, 19 Nov): what it cost this chat to get going.

    1 floor_k: the context at step 1 (k tokens).
    2 work_step / work_pct: steps, and % of a week, up to the first real work (None if there was none).
    3 reads: the files read before the first real work, [file, k tokens, $ to read and carry them]; re-learning is
      worked out at the film level (ledger.coldstart) against the previous chat's list.
    4 base_pct: step-1 context x steps x re-read price, as % of the chat's own cost."""
    film_re = _film_paths(film)
    steps, byid, calls, res = [], {}, {}, {}
    work = None
    for raw in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get('isSidechain'):
            continue
        m = d.get('message')
        if not isinstance(m, dict):
            continue
        if d.get('type') == 'assistant' and m.get('usage'):
            if m.get('id') not in byid:
                byid[m.get('id')] = len(steps)
                steps.append((m['usage'], costwatch.PRICE[costwatch.fam(m.get('model'))]))
            k = byid[m.get('id')]
            for b in m.get('content') or []:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    if work is None and _real_work(b.get('name'), b.get('input'), film_re):
                        work = k
                    if work is None:
                        fs = _read_files(b.get('name'), b.get('input'))
                        if fs:
                            calls[b['id']] = (k, fs)
        elif d.get('type') == 'user' and isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('type') == 'tool_result' and b.get('tool_use_id') in calls:
                    res[b['tool_use_id']] = (len(steps), _result_tokens(b))
    if not steps:
        return None
    ctx = [u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
           for u, _ in steps]
    cost = [(u.get('cache_read_input_tokens', 0) * p[0] + u.get('cache_creation_input_tokens', 0) * p[1]
             + u.get('input_tokens', 0) * p[2] + u.get('output_tokens', 0) * p[3]) / 1e6 for u, p in steps]
    end = len(steps)                                   # carried until the first compaction
    for i in range(1, len(steps)):
        if ctx[i] < COMPACT * ctx[i - 1]:
            end = i
            break
    reads = {}
    for tid, (k, fs) in calls.items():
        if tid not in res:
            continue
        at, tok = res[tid]
        if at >= len(steps):
            continue
        r, w = steps[at][1][0], steps[at][1][1]
        usd = tok * (w + r * max(0, end - at - 1)) / 1e6
        for f in fs:
            a = reads.setdefault(f, [f, 0.0, 0.0])
            a[1] += tok / len(fs) / 1000
            a[2] += usd / len(fs)
    total = sum(cost)
    base = ctx[0] * steps[0][1][0] * (len(steps) - 1) / 1e6
    return {'floor_k': ctx[0] // 1000,
            'work_step': None if work is None else work + 1,
            'work_pct': None if work is None else round(100 * sum(cost[:work + 1]) / costwatch.WEEK_USD, 2),
            'reads': [[f, round(t, 1), round(u, 4)] for f, t, u in sorted(reads.values(), key=lambda x: -x[2])][:40],
            'base_pct': round(100 * base / total, 1) if total else 0.0}


SHOW = re.compile(r'(?:^|[;&|\n(]\s*)(?:cd \S+ && )?python3?\s+\S*page\.py\s+[\w-]+\s+show\b')    # a finder call (page.py FILM show ...)
WHY = 120                                           # characters Claude wrote just before a search: its reason
MISS = 10                                            # film searches within 10 calls after a show: the show missed
NOTES_RE = re.compile(r'notes/[\w./-]*\.md')


def _target(name, inp):
    """Where a search that is not on the film's code looks: 'shared:FILE.py', 'film notes', 'guides', 'other'."""
    t = ' '.join(str((inp or {}).get(k, '')) for k in ('command', 'path', 'glob', 'pattern', 'file_path'))
    m = re.search(r'(?:source|\.claude/hooks)/([A-Za-z0-9_]+\.py)', t)
    if m:
        return 'shared:' + m.group(1)
    if NOTES_RE.search(t) or 'story/' in t:
        return 'film notes'
    if 'guides/' in t or 'CLAUDE.md' in t:
        return 'guides'
    return 'other'


def _what(name, inp):
    """finder-first Learn, step 4 (Sam's Option 1, 18 Nov): the file and the pattern one search asked about, short
    enough to keep on the ledger row. A shell line gives its first quoted pattern and the files it names."""
    inp = inp or {}
    if name in ('Grep', 'Glob'):
        return (str(inp.get('path') or inp.get('glob') or '')[:80], str(inp.get('pattern', ''))[:80])
    if name == 'Read':
        return (str(inp.get('file_path', ''))[:80], 'lines %s+%s' % (inp.get('offset', 0), inp.get('limit', '')))
    cmd = inp.get('command', '')
    files = re.findall(r'[\w./-]*(?:source|guides|notes|story|research|\.claude)/[\w./*-]+', cmd)
    q = re.search(r"""(?:grep|rg|ack)\b[^|;&]*?(?:-\w+\s+)*(?:'([^']+)'|"([^"]+)")""", cmd)
    pat = (q.group(1) or q.group(2)) if q else re.sub(r'\s+', ' ', cmd)[:80]
    return (' '.join(dict.fromkeys(files))[:80], pat[:80])


def _edits_film(name, inp, film_re):
    inp = inp or {}
    if name in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit'):
        return bool(film_re.search(inp.get('file_path', '')))
    cmd = inp.get('command', '') if name == 'Bash' else ''
    return bool(film_re.search(cmd) and re.search(r"sed -i|open\([^)]*['\"]w['\"]|>\s*source/", cmd))


def _ticked(name, inp):
    """'[x]' lines a call adds to a notes file (approximate: Edit new vs old text; a shell line naming notes/)."""
    inp = inp or {}
    if name in ('Edit', 'Write') and NOTES_RE.search(inp.get('file_path', '')):
        return max(0, (inp.get('new_string') or inp.get('content') or '').count('[x]')
                   - (inp.get('old_string') or '').count('[x]'))
    if name == 'Bash' and NOTES_RE.search(inp.get('command', '')):
        return max(0, inp['command'].count('[x]') - inp['command'].count('[ ]'))
    return 0


def search_record(path, film=None):
    """finder-use Learn (Sam's 1, 17 Nov): per chat, in call order: show calls; film-code searches split into before
    the first show / a miss (within MISS calls after a show) / later after a show / in a chat with no show; other
    searches by target (shared tools named per file); notes ticked; whether the chat edited the film's code."""
    film_re = _film_paths(film)
    seq, whys, ids, sizes = [], [], [], {}
    for raw in open(path, encoding='utf-8', errors='replace'):
        if '"tool_result"' in raw:                  # printout size per call (Sam's Y, 26 Nov): characters of each result
            try:
                u = json.loads(raw)
            except ValueError:
                u = {}
            for b in ((u.get('message') or {}).get('content') or []) if isinstance(u.get('message'), dict) else []:
                if isinstance(b, dict) and b.get('type') == 'tool_result':
                    c = b.get('content')
                    sizes[b.get('tool_use_id')] = len(c) if isinstance(c, str) else sum(
                        len(x.get('text', '')) for x in c or [] if isinstance(x, dict))
        if '"tool_use"' not in raw:
            continue
        try:
            d = json.loads(raw)
        except ValueError:
            continue
        if d.get('isSidechain') or d.get('type') != 'assistant':
            continue
        said = ''
        for b in (d.get('message') or {}).get('content') or []:
            if isinstance(b, dict) and b.get('type') == 'text':
                said = (b.get('text') or '').strip()[-WHY:] or said
            if isinstance(b, dict) and b.get('type') == 'tool_use':
                seq.append((b.get('name'), b.get('input') or {}))
                ids.append(b.get('id'))
                whys.append(said)
                said = ''
    out = {'show': 0, 'film': {'before show': 0, 'miss': 0, 'after show': 0}, 'other': {}, 'ticked': 0,
           'edited film code': False, 'list': []}     # list: [call number, kind, target, file, pattern, reason, printout chars] per search
    last_show = None
    for i, (name, inp) in enumerate(seq):
        cmd = inp.get('command', '') if name == 'Bash' else ''
        if SHOW.search(cmd):
            out['show'] += 1
            last_show = i
            continue
        k = kind_of(name, inp, film_re)
        if k == 'film-file search':
            key = 'before show' if last_show is None else 'miss' if i - last_show <= MISS else 'after show'
            out['film'][key] += 1
            out['list'].append([i, 'film', key] + list(_what(name, inp)) + [whys[i], sizes.get(ids[i], 0)])
        elif k == 'tool search':
            t = _target(name, inp)
            out['other'][t] = out['other'].get(t, 0) + 1
            out['list'].append([i, 'other', t] + list(_what(name, inp)) + [whys[i], sizes.get(ids[i], 0)])
        out['ticked'] += _ticked(name, inp)
        out['edited film code'] |= _edits_film(name, inp, film_re)
    if not out['show']:
        out['film'] = {'no show': out['film']['before show']}
    return out


def line(m):
    """One line for the ledger page."""
    if not m:
        return ''
    ks = ', '.join(f'{k} {v:g}%' for k, v in sorted(m['kinds'].items(), key=lambda kv: -kv[1]))
    return f"{m['steps']} steps, history {m['hist'] // 1000}k at the end; {ks}"


def test():
    """Checks on a real transcript (trimmed) and on this chat's own, when there is one."""
    ok = True

    def check(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(('PASS ' if cond else 'FAIL ') + name)
    fr = _film_paths('blessed')
    check('page.py show is page.py, not a search',
          kind_of('Bash', {'command': 'python3 source/page.py blessed show "arm clips the mic"'}, fr) == 'page.py')
    check('grep on the film file is a film-file search',
          kind_of('Bash', {'command': 'grep -n "def arm" source/blessed_cast.py | head'}, fr) == 'film-file search')
    check('sed -n on a shared tool is a tool search',
          kind_of('Bash', {'command': 'cd x && sed -n 10,60p source/ledger.py'}, fr) == 'tool search')
    check('Read of a .py with no range is a whole-file read',
          kind_of('Read', {'file_path': '/r/source/moves.py'}, fr) == 'whole-file .py read')
    check('Read of a film .py with a range is a film-file search',
          kind_of('Read', {'file_path': '/r/source/blessed.py', 'offset': 40, 'limit': 40}, fr) == 'film-file search')
    check('a render is a render',
          kind_of('Bash', {'command': 'python3 source/blessed.py final /tmp/a.mp4 --small --span 3 6'}, fr) == 'renders')
    check('Read of a .png is a picture', kind_of('Read', {'file_path': '/tmp/sheet.png'}, fr) == 'pictures')
    check('cat of a whole .py is a whole-file read',
          kind_of('Bash', {'command': 'cat source/blessed.py'}, fr) == 'whole-file .py read')
    fx = os.path.join(ROOT, 'tests', 'stepcost-transcript.jsonl')
    m = measure(fx, 'proposal-route')
    print('  real transcript (trimmed):', line(m))
    check('steps counted once per reply (one reply is several lines)', m and m['steps'] == FIXTURE_STEPS)
    check('history at the end is the last step\'s', m and m['hist'] == FIXTURE_HIST)
    sr = (m or {}).get('search') or {}
    check('every search is listed with its file and pattern',
          sr.get('list') and len(sr['list']) == sum(sr['film'].values()) + sum(sr['other'].values())
          and all(len(x) == 7 and isinstance(x[6], int) for x in sr["list"]))
    import tempfile
    tj = os.path.join(tempfile.mkdtemp(), 't.jsonl')       # change 2 (19 Nov): the words before a search are its reason
    with open(tj, 'w') as f:
        f.write(json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'text', 'text': 'Looking for where the arm is drawn'},
            {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'grep -n "def arm" source/blessed_cast.py'}}]}}) + '\n')
    rr = search_record(tj, 'blessed')['list']
    check('a search carries the reason Claude gave just before it', len(rr) == 1 and 'arm is drawn' in rr[0][5])
    check('the file and pattern of a shell grep are read',
          _what('Bash', {'command': 'grep -n "def arm" source/blessed_cast.py | head'}) == ('source/blessed_cast.py', 'def arm'))
    check('the kinds add to 100%', m and abs(sum(m['kinds'].values()) - 100) < 1)
    check('nothing is left as "other" (Sam, 28 Nov)', m and not any('other' in k for k in m['kinds']))
    check('the total matches the cost watch', m and abs(m['usd'] - _watch_usd(fx)) < 0.01)
    check('this fixture\'s searches are tool searches (no film files in a tool job)',
          m and m['kinds'].get('tool search', 0) > 0 and 'film-file search' not in m['kinds'])
    sp = (m or {}).get('split') or {}                # cost-other change 1: the exact split
    print('  split:', split_line(sp))
    check('split: the main chat\'s parts add to its real cost within 1%',
          sp and abs(sp['usd'] - _watch_usd(fx)) <= 0.01 * _watch_usd(fx))
    check('split: blocks and origins each add to 100%', sp and abs(sum(sp['blocks'].values()) - 100) < 1
          and abs(sum(sp['origins'].values()) - 100) < 1)
    check('split: leftover under 5%', sp and sp['leftover'] < 5)
    check('split: the step-1 context is stored', sp and sp['floor_k'] > 0)
    tk = os.path.join(tempfile.mkdtemp(), 'k.jsonl')  # a made-up chat: floor 1000, a tool result, an edit, a cache miss
    U = lambda r, w, o: {'cache_read_input_tokens': r, 'cache_creation_input_tokens': w, 'input_tokens': 0, 'output_tokens': o}
    with open(tk, 'w') as f:
        for ln in [{'type': 'assistant', 'message': {'id': 'a', 'model': 'opus', 'usage': U(0, 1000, 100), 'content': [
                       {'type': 'tool_use', 'id': 't1', 'name': 'Bash', 'input': {'command': 'grep -n x source/ledger.py'}}]}},
                   {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': 't1', 'content': 'x' * 1600}]}},
                   {'type': 'assistant', 'message': {'id': 'b', 'model': 'opus', 'usage': U(1000, 500, 0), 'content': []}},
                   {'type': 'assistant', 'message': {'id': 'c', 'model': 'opus', 'usage': U(0, 1500, 0), 'content': []}}]:
            f.write(json.dumps(ln) + '\n')
    sk = split(tk, helpers=False)
    check('split: a made-up chat lands where it should (floor, tool result, Claude\'s words, cache re-write)',
          sk and sk['leftover'] == 0 and sk['floor_k'] == 1 and set(sk['origins']) ==
          {'start-up floor', 'result: tool search', "Claude's words", 'cache re-write'})
    cs = (m or {}).get('start') or {}                # cold-start change: the four start figures
    print('  start:', {k: v for k, v in cs.items() if k != 'reads'}, 'read first:', [r[0] for r in cs.get('reads', [])][:4])
    check('start: step-1 context, first real work, files read before it, base share all recorded',
          cs and cs['floor_k'] == sp.get('floor_k') and cs['work_step'] and cs['work_pct'] > 0 and cs['reads']
          and 0 < cs['base_pct'] < 100 and all(len(r) == 3 for r in cs['reads']))
    check('start: the first real work is the first edit outside notes, never before it',
          all(not _real_work('Read', {'file_path': f}, fr) for f in ('source/ledger.py',)) and
          _real_work('Edit', {'file_path': '/r/source/blessed.py'}, fr) and
          not _real_work('Edit', {'file_path': '/r/notes/blessed.md'}, fr) and
          _real_work('Bash', {'command': 'python3 source/blessed.py final /tmp/a.mp4 --small'}, fr) and
          _real_work('Bash', {'command': "python3 - <<'X'\np='source/ledger.py'; open(p,'w').write(s)\nX"}, fr) and
          not _real_work('Bash', {'command': 'cat >> notes/blessed.md <<X'}, fr))
    check('start: shell reads name their files', _read_files('Bash', {'command': 'sed -n 1,40p source/ledger.py | head'})
          == ['source/ledger.py'])
    own = sorted(glob.glob(os.path.expanduser('~/.claude/projects/**/*.jsonl'), recursive=True),
                 key=os.path.getmtime)
    if own:
        mo = measure(own[-1], 'proposal-route')
        print('  this chat:', line(mo))
        check('this chat measures', mo and mo['steps'] > 0 and abs(sum(mo['kinds'].values()) - 100) < 1)
        so = mo.get('split') or {}
        check('this chat splits exactly, leftover under 5%', so and abs(so['usd'] - _watch_usd(own[-1])) < 0.01
              and so['leftover'] < 5)
    import tempfile                                  # the ledger keeps the measure, and keeps it when the app's
    import ledger                                    # real figure replaces the estimate row
    tmp = tempfile.mkdtemp()
    ledger.DIR, ledger.CURRENT = tmp, os.path.join(tmp, '.current')
    d = ledger.load('testfilm')
    row = {'date': '2026-11-16', 'chat': 'abcd1234', 'stage': 'auto', 'round': None, 'notes': 0, 'repeats': [],
           'model': 'opus', 'cost': 1.0, 'src': 'estimate', 'sid': 'session_XYZ'}
    ledger._put_measure(row, m)
    d['chats'].append(row)
    ledger.store(d)
    page = open(os.path.join(tmp, 'testfilm.md')).read()
    check('the ledger page shows the chat\'s cost by kind', 'Cost by kind of step' in page)
    check('the ledger page shows where each chat\'s money went (split)', 'Where the money went' in page)
    tsv = os.path.join(tmp, 'app.tsv')
    open(tsv, 'w').write('\t'.join(['testfilm', 'XYZ', '2026-11-16T09:00', 'chat title', '2.45'] + [''] * 4
                                    + ['opus']) + '\n')
    ledger.app_import(tsv)
    rows = ledger.load('testfilm')['chats']
    check('the app row replaces the estimate and keeps its measure',
          len(rows) == 1 and rows[0]['src'] == 'app' and rows[0].get('steps') == m['steps'])
    check('the app row keeps the split and start figures', rows and rows[0].get('split') and rows[0].get('start'))
    d2 = ledger.load('testfilm')                     # a second chat re-reads the first one's files: re-learning
    r2 = dict(rows[0], chat='efgh5678', sid='session_ABC', src='estimate')
    d2['chats'].append(r2)
    cl = ledger.coldstart(d2) or ''
    print('  film-end line:', cl)
    check('the film-end line gives start and re-learning as % of the film, checked against the app',
          "A new chat's start and re-learning cost" in cl and 're-learning 0.00' not in cl and 'checked against the app' in cl)
    ledger.store(d2)
    check('the ledger page shows starting each chat', 'Starting each chat' in open(os.path.join(tmp, 'testfilm.md')).read())
    print('ALL PASS' if ok else 'SOME FAILED')
    return ok


FIXTURE_STEPS, FIXTURE_HIST = None, None   # set from the fixture's own record (tests/stepcost-transcript.json)


def _watch_usd(path):
    tot, seen = 0.0, set()
    for raw in open(path):
        d = json.loads(raw)
        m = d.get('message')
        if d.get('type') != 'assistant' or not isinstance(m, dict) or not m.get('usage') or m.get('id') in seen:
            continue
        seen.add(m['id'])
        u, p = m['usage'], costwatch.PRICE[costwatch.fam(m.get('model'))]
        tot += (u.get('cache_read_input_tokens', 0) * p[0] + u.get('cache_creation_input_tokens', 0) * p[1]
                + u.get('input_tokens', 0) * p[2] + u.get('output_tokens', 0) * p[3]) / 1e6
    return tot


def _load_fixture_facts():
    global FIXTURE_STEPS, FIXTURE_HIST
    try:
        f = json.load(open(os.path.join(ROOT, 'tests', 'stepcost-transcript.json')))
        FIXTURE_STEPS, FIXTURE_HIST = f['steps'], f['hist']
    except Exception:
        pass


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'test':
        _load_fixture_facts()
        sys.exit(0 if test() else 1)
    if not a:
        print(__doc__)
        sys.exit(1)
    film = a[a.index('--film') + 1] if '--film' in a else None
    m = measure(a[0], film)
    print(line(m))
    print(json.dumps(m, indent=1))
