#!/usr/bin/env python3
"""The handover check (Job Q, Sam 13 Nov): nothing Sam says in a chat is dropped between chats.

Why: on Blessed, notes N8-N10 sat unread when chat 5 broke before writing them (chat 6 read only the notes file), and
note 47's second half ("his face still needs work") was marked done with the first half and fell out of two handovers.
Closest before it: CLAUDE.md "Fresh chats and the handover", rule 30, ledger.py; nothing checked a handover.

MAP
  log .............. UserPromptSubmit hook: each message Sam types is saved to notes/ledger/sam/CHAT.md (a background
                     step waits up to 20 s for the chat record to drop seeds and notices), committed
                     and pushed at once (in the background), so a chat that breaks mid-turn still leaves his words on
                     GitHub for the next chat. Costs nothing in the chat.
  end .............. before a chat hands over: reads this chat's own record (free, no list_events) and flags
                     (1) a message of Sam's with no reply after it, (2) an ask in his message that the film's notes do
                     not carry (asks(): each sentence of a message is one ask; carried(): a notes line holds most of
                     its words, and its note number when it has one: note 47's 'face' half), (3) "clip sent" with no
                     file sent, (4) an 'override' Sam never typed (chat 5 read "don't stop for any Y" as one)
  start ............ first thing in the next chat: `start PARENT_SESSION` reads the saved log from (1) and runs (2)
                     against the notes as they stand; a chat with no log falls back to `dump`
  open_notes() ..... in start (startup-fixes 3, 16 Nov): prints "Where things stand" and the unticked notes, which
                     the chat reads in place of the notes file
  branches ......... in end (startup-fixes 2, 16 Nov): every branch source/branches.py lists (work never on the main
                     line, last 7 days) must be merged or named in the notes
  finder ........... in end (finder-use, 17 Nov): this chat edited the film's code with no page.py show call
  model ............ in end and start: the Next line may not join Opus work with Sonnet work (render, finish.py,
                     sending, filing) nor give Sonnet a fix or build (Sam, 15 Nov: chat 30 rendered on Opus)
  watcher .......... in start: the watcher's standing BROKEN list and any system with no promise (source/watcher.py)
  dump ............. list_events results saved to files (kinds ["user"], only when there is no log; never page a
                     whole chat: the newest pages, back to the last handover commit's time)
  sam_messages() ... Sam's own typed messages from any of the three sources (no tool results, task or system
                     notices, seed prompts from a parent chat, Stop-hook feedback, image stubs)

    python3 source/handover.py end [--film blessed]                (prints faults only; exit 1 if any)
    python3 source/handover.py start session_01ABC... [--film blessed]
    python3 source/handover.py dump FILE1 [FILE2 ...] --film blessed [--notes notes/blessed.md]
"""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGDIR = os.path.join(ROOT, 'notes', 'ledger', 'sam')
NOT_SAM = ('<task-notification', '[SYSTEM NOTIFICATION', 'Stop hook feedback', '[Image:', '<system-reminder',
           '<command-', 'Caveat:', '<local-command', '[Request interrupted', '<agent-message', '[Subagent hand-back')
STOP = set('''about above after again also among apart because been before being below between both but can cant
could does doesnt dont down each even every explain from have having here hers into just keep like make more most much
must need needs only other over same seem shall should some still such than that thats their them then there these
they thing think this those though through thus very want wants were what when where which while whom whose why will
with within without would your youre yours the and for are was its his him her she has had not too now why how who
did get got going look looks really instead please also back away don't i'm it's there's'''.split())


# ------------------------------------------------------------------------------------------------ Sam's messages
def _text(content):
    if isinstance(content, str):
        return content
    if any(c.get('type') == 'tool_result' for c in content):
        return ''
    return '\n'.join(c.get('text', '') for c in content if c.get('type') == 'text')


def _is_sam(text):
    t = text.strip()
    return bool(t) and not t.startswith(NOT_SAM)


def sam_messages(path):
    """[(iso time, text)] of Sam's typed messages in one source: a chat record (.jsonl), a list_events result saved
    to a file, or a saved log (notes/ledger/sam/CHAT.md). Also [(time, 'claude', text, sent files)] for replies when
    the source has them (chat records only): see turns()."""
    return [(t, x) for t, who, x, _ in turns(path) if who == 'sam']


def turns(path):
    out = []
    raw = open(path, encoding='utf-8', errors='replace').read()
    if path.endswith('.md'):                                       # the saved log: '### TIME' then the text
        for m in re.finditer(r'^### (\S+)\n(.*?)(?=^### |\Z)', raw, re.S | re.M):
            if _is_sam(m.group(2)):                                # older logs kept helpers' reports
                out.append((m.group(1), 'sam', m.group(2).strip(), []))
        return out
    i = raw.find('{"ccr"')
    if i >= 0:                                                     # list_events result(s)
        for blob in re.finditer(r'\{"ccr".*?\}\}\s*(?=</other-session|\Z)', raw[i:], re.S):
            try:
                data = json.loads(blob.group(0))['ccr']['data']
            except ValueError:
                continue
            for e in data:
                kind = next((k for k in e if k not in ('created_at',)), None)
                c = (e.get(kind) or {}).get('internal_anthropic_catchall') or e.get(kind) or {}
                msg = c.get('message') or {}
                txt = _text(msg.get('content') or '')
                if kind == 'user':
                    seed = c.get('client_platform') in (None, 'claude_code_mcp_seed')
                    if not seed and not c.get('isSynthetic') and not c.get('isReplay') and _is_sam(txt):
                        out.append((e['created_at'][:19], 'sam', txt.strip(), []))
                elif kind == 'assistant' and txt.strip():
                    out.append((e['created_at'][:19], 'claude', txt, []))
        return sorted(out)
    failed = set()                     # status chat (21 Nov): chat 26's clip was refused by the permission check, yet
    for ln in raw.splitlines():        # counted as sent and Sam was told "I sent you a short clip"
        if '"tool_result"' in ln:
            try:
                for c in (json.loads(ln).get('message') or {}).get('content') or []:
                    if isinstance(c, dict) and c.get('type') == 'tool_result' and (
                            c.get('is_error') or re.search(r'denied|not sent|rejected', _text(c.get('content') or ''), re.I)):
                        failed.add(c.get('tool_use_id'))
            except (ValueError, AttributeError):
                pass
    for ln in raw.splitlines():                                    # a chat record
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        msg, t = d.get('message') or {}, (d.get('timestamp') or '')[:19]
        if d.get('type') == 'user' and not d.get('isMeta') and not d.get('isSidechain'):
            if (d.get('origin') or {}).get('kind') or d.get('promptSource') == 'system':
                continue                                           # seeds, task notices, peers
            txt = _text(msg.get('content') or '')
            if _is_sam(txt):
                out.append((t, 'sam', txt.strip(), []))
        elif d.get('type') == 'assistant' and not d.get('isSidechain'):
            for c in msg.get('content') or []:
                if c.get('type') == 'text' and c['text'].strip():
                    out.append((t, 'claude', c['text'], []))
                elif c.get('type') == 'tool_use' and c.get('name') == 'SendUserFile' and c.get('id') not in failed:
                    out.append((t, 'sent', '', [os.path.basename(f) for f in c['input'].get('files', [])]))
    return out


# ------------------------------------------------------------------------------------------------ asks and carrying
def _stem(w):
    for suf in ('ements', 'ement', 'ments', 'ment', 'ingly', 'ing', 'edly', 'ly', 'ed', 'es', 's', 'e'):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)]
    return w


def _num(tok):
    return re.sub(r'\.?0+$', '', tok) if '.' in tok else tok


def words(text):
    """Content words (stemmed) and number tokens (times, ranges: they count double, as anchors)."""
    t = text.lower().replace('’', "'")
    nums = {_num(n) for n in re.findall(r'\d+(?:[.-]\d+)?', t) if len(n) >= 3 or '-' in n}
    ws = {_stem(w) for w in re.findall(r"[a-z]+", t) if len(w) >= 4 and w not in STOP}
    return ws, nums


def asks(text):
    """Each sentence of Sam's message (and each half of a 'but') with 2+ content words is one ask; short answers
    (Y, N, numbers) are no asks. Returns [(note number or None, ask text)]."""
    m = re.match(r'\s*(?:note\s*)?N?(\d{1,3})\s*[:.)\-–]\s+', text, re.I)
    note = m.group(1) if m else None
    body = text[m.end():] if m else text
    out = []
    for s in re.split(r'(?<=[.?!;])\s+|\n+|\s+but\s+|--', body):
        ws, nums = words(s)
        if len(ws) + len(nums) >= 2 or (ws and nums):
            out.append((note, s.strip()))
    return out


DONE = re.compile(r'(?i)\b(done|fixed|answered|closed|removed|built)\b')


def _norm(s):
    return re.sub(r'\s+', ' ', s.lower()).strip(' .?!')


def carried(ask, lines, note=None, new=None):
    """The notes line that carries this ask, or None. It names the note's number (when it has one) and holds half the
    ask's weight: each content word weighs by how rare it is in the notes (head, shot, check weigh little; pool,
    table, journalists a lot), a time or range double. Unnumbered asks need 2+ words. A line that marks the note done
    must carry the ask in its own words, not by quoting Sam (note 47: 'answered' while his face was still open); a
    question is carried by 'answered' on its numbered line."""
    import math
    ws, nums = words(ask)
    if not ws and not nums:
        return 'no words'
    question = ask.rstrip().endswith('?') or re.match(r'(?i)\s*(why|how|explain)\b', ask)
    bags = [words(ln) for ln in lines]
    n = len(lines) + 1
    df = {w: sum(w in b[0] for b in bags) for w in ws}
    df.update({x: sum(x in b[1] for b in bags) for x in nums})
    wt = {k: (2 if k in nums else 1) * (math.log(n / (1 + v)) + 0.1) for k, v in df.items() if v}
    if not wt:                     # none of its words is anywhere in the notes
        return None
    total = sum(wt.values())       # (Sam's words the notes never use say nothing either way: left out)
    if new is not None:            # only what was written after Sam said it carries it (N8 repeated old note 43)
        lines = [ln for ln in lines if ln in new]
    if note:                       # a bullet listing many notes ('45 ... face; 46 ...; 47 ...'): only 47's part
        num = re.compile(rf'(?<![\d.]){note}(?![\d.])')
        lines = [seg for ln in lines for seg in (ln.split(';') if '|' not in ln else [ln]) if num.search(seg)]
    for ln in lines:
        if note and DONE.search(ln):
            if question and re.search(r'(?i)\banswered\b', ln):
                return ln
            ln = _norm(ln).replace(_norm(ask), ' ')
        lw, ln_nums = words(ln)
        got = [k for k in wt if k in lw or k in ln_nums]
        if (note and got) or (sum(wt[k] for k in got) >= 0.5 * total and len(got) >= min(2, len(wt))):
            return ln
    return None


def note_lines(notes_path):
    """The notes file (a path, .gz too) as lines to search: each bullet or table row, continuation lines joined on."""
    import gzip
    out, cur = [], ''
    for ln in (gzip.open if notes_path.endswith('.gz') else open)(notes_path, 'rt', encoding='utf-8'):
        if re.match(r'\s*([-*|#]|\d+[.)])', ln) or not ln.strip():
            if cur:
                out.append(cur)
            cur = ln.strip()
        else:
            cur += ' ' + ln.strip()
    if cur:
        out.append(cur)
    return out


TICKED = re.compile(r'(?i)^\s*(fixed|done|ticked|built|answered|dropped|merged|kept off|n/?a|yes|y)\b|\[x\]|✓')


def open_notes(notes_path):
    """startup-fixes 3 (Sam, 16 Nov): what a chat reads of the notes at start, in place of the whole file (~3.6k
    tokens a chat): the "Where things stand" section word for word, then every unticked note: a '- [ ]' line, or a
    table row (under a 'done?' or 'status' column) whose last cell is blank or not done. carried() still checks the
    whole file."""
    out, cur, sec, stand, head, col = [], None, '', [], None, False
    lines = open(notes_path, encoding='utf-8').read().split('\n')
    for ln in lines:
        if ln.startswith('#'):
            sec, head, col = ln.lstrip('#').strip(), None, False
            cur = 'stand' if re.match(r'(?i)where things stand', sec) else None
            if cur:
                stand.append(ln)
            continue
        if cur == 'stand':
            stand.append(ln)
            continue
        row = None
        if re.match(r'\s*[-*] \[ \]', ln):
            row = ln.strip()
        elif ln.startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if head is None:
                head, col = cells, bool(re.match(r'(?i)(done\??|status)$', cells[-1]))
            elif col and not set(''.join(cells)) <= set('-: ') and any(cells[:-1]) and not TICKED.search(cells[-1]):
                row = '| ' + ' | '.join(cells) + ' |'
        elif not ln.strip():
            head, col = None, False
        if row:
            if not out or out[-1][0] != sec:
                out.append((sec, []))
            out[-1][1].append(row)
    text = '\n'.join(stand).rstrip()
    for s, rows in out:
        text += f'\n\n## Unticked: {s[:80]}\n' + '\n'.join(rows)
    return text + ('' if out else '\n\n## Unticked: none')


# ------------------------------------------------------------------------------------------------ the checks
def check(tr, lines, old=None):
    """Faults, one line each, for a chat's turns tr against the film's notes lines. old: the notes lines as they were
    when Sam said it (a list, or a function of the message's time): only lines written since carry his message."""
    def new_at(t):
        o = old(t) if callable(old) else old
        return None if o is None else set(lines) - set(o)
    faults = []
    sams = [x for x in tr if x[1] == 'sam']
    said = ' '.join(x[2] for x in sams).lower()
    last_reply = max((x[0] for x in tr if x[1] in ('claude', 'sent')), default='')
    for t, _, text, _ in sams:
        if any(x[1] == 'claude' for x in tr) and t > last_reply:
            faults.append(f'UNANSWERED {t[11:16]}: "{text[:90]}" (no reply after it: the chat broke)')
        for note, a in asks(text):
            if not carried(a, lines, note, new_at(t)):
                tag = f'note {note}' if note else t[11:16]
                faults.append(f'NOT CARRIED {tag}: "{a[:100]}" (no line in the notes holds it)')
    sent = {f for x in tr if x[1] == 'sent' for f in x[3]}
    for t, who, text, _ in tr:
        if who != 'claude':
            continue
        for m in re.finditer(r'(?i)(?:(?:clips?|sheet|animatic|picture)s?\b[^.\n]{0,30}?\s(?<!be )(?<!been )(?:is\s+|are\s+|was\s+)?(?<!be )sent\b|\b(?:sent|sending)\s+(?:you\s+)?(?:a\s+|the\s+|an\s+)?(?:short\s+|new\s+|quick\s+)?(?:clip|sheet|animatic|picture|video))[^.\n]*', text):
            files = re.findall(r'[\w.-]+\.(?:mp4|jpg|png|gif)', m.group(0))
            if any(x[1] == 'sent' for x in tr) is False or any(f not in sent for f in files):
                faults.append(f'NOT SENT {t[11:16]}: "{m.group(0)[:80]}" (no such file was sent in this chat)')
        if re.search(r'(?i)\boverride\b', text) and 'override' not in said and re.search(
                r"(?i)(as an? |treat\w* (it )?as |counts? as |Sam'?s? )override", text):
            faults.append(f'OVERRIDE {t[11:16]}: the chat treats something as an override, but Sam never typed '
                          f"'override' (rule 85)")
    return faults


def _film_notes(film, notes=None):
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    if not os.path.exists(p):
        sys.exit(f'handover: no notes file {p}; pass --film or --notes')
    return note_lines(p)


def notes_before(film, when):
    """The film's notes lines as they stood just before `when` (ISO time), from git; None if git has no copy."""
    rel = f'notes/{film}.md'
    c = subprocess.run(['git', '-C', ROOT, 'log', '--all', '-1', '--format=%H', f'--before={when}', '--', rel],
                       capture_output=True, text=True).stdout.strip()
    if not c:
        return None
    import tempfile
    p = os.path.join(tempfile.mkdtemp(), 'old.md')
    open(p, 'w').write(subprocess.run(['git', '-C', ROOT, 'show', f'{c}:{rel}'], capture_output=True, text=True).stdout)
    return note_lines(p)


def _run(tr, film, notes=None):
    seen = {}
    old = None if notes or not film else (lambda t: seen.setdefault(t, notes_before(film, t)))
    return check(tr, _film_notes(film, notes), old)


ROUTINE = re.compile(r'finish\.py|`final (?![^`]*--span)[^`]*`|final render|\banimatic\b[^.;]{0,12}\brender|\brender[^.;]{0,20}'
                     r'\banimatic|send(ing)? the (animatic|final)|\bfiling\b', re.I)
BUILDING = re.compile(r'\bfix(es|ing)?\b|\bbuild|\bplan(ning)?\b|\bnotes? round', re.I)


def model_faults(film, notes=None):
    """Each job on its own model (Sam, 15 Nov: chat 30 ran a fix AND the animatic render on Opus; the 10 Nov rule
    guarded only the step up to a stronger model, and nothing checked it). The handover's Next line must not join
    Opus work with Sonnet work (render, finish.py, sending, filing) or give Sonnet a fix or a build."""
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    if not film and not notes or not os.path.exists(p):
        return []
    nxt = next((ln for ln in open(p, encoding='utf-8') if ln.lstrip('- *').lower().startswith('next')), '')
    out = []
    if re.search(r'\bopus\b', nxt, re.I) and not re.search(r'\bsonnet\b', nxt, re.I) and ROUTINE.search(nxt):
        out.append('MODEL: the Next line gives Opus routine work ("' + ROUTINE.search(nxt).group(0) + '"): split it, '
                   'Opus for the fix, then a Sonnet chat (opened by the Opus one) for the render, finish.py and sending '
                   '(CLAUDE.md, Models by stage)')
    if re.search(r'\bsonnet\b', nxt, re.I) and not re.search(r'\bopus\b', nxt, re.I) and BUILDING.search(nxt):
        out.append('MODEL: the Next line gives Sonnet a fix or a build ("' + BUILDING.search(nxt).group(0) + '"): '
                   'Opus (medium for a fix from a clear plan) does that, then opens the Sonnet chat')
    return out


def draft_faults(film, notes=None):
    """Rule P16 (Sam, 15 Nov: animatic 2 was lost with its chat, so a 3-second fix meant a 30-minute redraw): once a film's
    notes say an animatic was sent, its latest animatic and clean render are in animations/drafts/ and pushed."""
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    if not film or not os.path.exists(p) or not re.search(r'animatic \d+ sent', open(p, encoding='utf-8').read(), re.I):
        return []
    d = os.path.join(ROOT, 'animations', 'drafts')
    slug = film.replace('_', '-')
    if all(os.path.exists(os.path.join(d, f'{slug}-{k}.mp4')) for k in ('animatic',)):
        return []
    return ['DRAFT: the notes say an animatic was sent, but animations/drafts/' + slug + '-animatic.mp4 is '
            'not on file (rule P16): save them (finish.py does it for the next one) and push']


def changed_films():
    """Film modules (source/NAME.py with SHOTS) whose code this chat changed: uncommitted, or committed on this branch
    and not yet on the main line (so `end` runs before the main-line push, as the handover order says)."""
    main = 'origin/claude/create-claude-md-oe8z4g'
    out = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', f'{main}...HEAD'], capture_output=True, text=True).stdout
    out += subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout
    films = set()
    for m in re.finditer(r'source/([a-z][a-z0-9]*(?:_[a-z0-9]+)*)\.py', out):
        parts = m.group(1).split('_')
        for k in range(len(parts), 0, -1):          # protest_tiers_sets -> protest_tiers (the film's main module)
            base = '_'.join(parts[:k])
            f = os.path.join(ROOT, 'source', base + '.py')
            if os.path.exists(f) and re.search(r'^SHOTS\b', open(f, encoding='utf-8').read(), re.M):
                films.add(base); break
    return sorted(films)


def quick_faults(films=None):
    """Late-faults change 1 (Sam's 1, 16 Nov; notes/proposals/late-faults.md): a chat that changed a film's code runs its
    quick check (preflight --text) before it hands over; each fault is fixed, or waived in the notes' "## Exceptions"
    with a reason (pre-flight then drops it). COULD NOT TEST (an undeclared list) counts as a fault. At red the
    handover still goes, these listed first."""
    out = []
    for film in (changed_films() if films is None else films):
        tmp = os.path.join('/tmp', f'handover-quick-{film}')
        try:
            r = subprocess.run([sys.executable, os.path.join(ROOT, 'source', 'preflight.py'), film, tmp, '--text'],
                               cwd=os.path.join(ROOT, 'source'), capture_output=True, text=True, timeout=600)
            txt = r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            out.append(f'QUICK CHECK: {film}: did not finish in 10 minutes (run preflight.py {film} OUT --text by hand)')
            continue
        lines = [ln.strip()[2:] for ln in txt.splitlines() if ln.startswith(' - ')]
        lines += [ln.strip() for ln in txt.splitlines() if 'COULD NOT TEST' in ln.upper() and not ln.startswith(' - ')]
        if r.returncode not in (0, 1) and not lines:
            lines = ['the quick check stopped: ' + (txt.strip().splitlines() or ['no output'])[-1][:160]]
        out += [f'QUICK CHECK {film}: {x[:220]}' for x in lines]
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import ledger
            d = ledger.load(film)
            d.setdefault('quick_checks', []).append({'at': datetime.now(timezone.utc).isoformat(timespec='minutes'),
                                                     'faults': len(lines)})
            ledger.store(d)
        except Exception:
            pass
    return out


def end_stamp(rec):
    """`end` ran in this chat: one line in notes/logs/handover-end.log, so the next chat's `start` can tell."""
    os.makedirs(os.path.join(ROOT, 'notes', 'logs'), exist_ok=True)
    with open(os.path.join(ROOT, 'notes', 'logs', 'handover-end.log'), 'a', encoding='utf-8') as f:
        sid = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '').split('_')[-1] or os.path.basename(rec or '-')[:8]
        f.write(f'{datetime.now(timezone.utc).isoformat(timespec="minutes")}\t{sid}\n')


def finder_faults(film, rec=None):
    """finder-use change 1 (Sam's 1, 17 Nov), replacing the per-day flag (one show call anywhere that day silenced it
    for every chat; it never fired on 16 Nov): THIS chat edited the film's code with no `page.py show` call: say so,
    with its count of hand searches of the film's code (stepcost.search_record, from the chat's own record)."""
    if not film or not rec:
        return []
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import stepcost
    try:
        r = stepcost.search_record(rec, film)
    except Exception:
        return []
    if not r['edited film code'] or r['show']:
        return []
    return [f'FINDER: this chat edited the film\'s code with no `page.py {film} show` call ({r["film"].get("no show", 0)} '
            'hand searches of its code): each note looks first with show --shot --at --who (or say in the notes why not)']


def unrouted_faults(rec):
    """The proposal route (Sam, 15 Nov): a change put to Sam that the Stop hook blocked once and then let through
    (stop_hook_active) is logged by propose.py; the handover names each one so it is routed, not forgotten."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import propose
    return ['UNROUTED: ' + ln + ' (put it through propose.py new/pack/judge/record, or tell Sam it went unjudged)'
            for ln in propose.unrouted_for(os.path.basename(rec or '')[:8])] if rec else []


def branch_faults(film, notes=None):
    """startup-fixes 2 (Sam's Y, 16 Nov): CLAUDE.md "merge or name every branch the start lists". A fresh scan
    (source/branches.py: work from the last 7 days whose newest version never reached the main line or this copy);
    each branch still listed must be named in the film's notes (with what was decided), else it is a fault."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import branches
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    text = open(p, encoding='utf-8').read() if film and os.path.exists(p) else ''
    try:
        left = branches.unsettled(text)
    except Exception as e:
        return [f'BRANCH: the branch scan failed ({e}); run python3 source/branches.py scan']
    return [f'BRANCH not merged or named in the notes: {branches.line(b).strip()}' for b in left]



TAG = re.compile(r'(?i)should\s+have\s+caught')


def note_tags(notes_path):
    """check-catches change 2 (Sam's Y, 20 Nov): Sam's numbered notes (the "## Notes" table) as {number: tag}, the
    tag being the "should have caught" cell (a check's name, or "none"); None when the table has no such column.
    Only rows with words in their note cell count (the template's empty row 1 does not)."""
    if not notes_path or not os.path.exists(notes_path):
        return {}
    tags, head, on = {}, None, False
    for ln in open(notes_path, encoding='utf-8'):
        if ln.startswith('#'):
            on, head = bool(re.match(r'#+\s*Notes\b', ln)), None
            continue
        if not on or not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if head is None:
            head = [c.lower() for c in cells]
            continue
        if set(''.join(cells)) <= set('-: ') or not re.match(r'^\d+[a-z]?$', cells[0]):
            continue
        ni = next((i for i, h in enumerate(head) if h.startswith('note')), 3)
        if ni >= len(cells) or not cells[ni]:
            continue
        ti = next((i for i, h in enumerate(head) if TAG.search(h)), None)
        tags[cells[0]] = cells[ti] if ti is not None and ti < len(cells) else None
    return tags


def tag_faults(film, notes=None):
    """change 2: the handover refuses while any of Sam's notes lacks "should have caught: CHECK / none"; the tags and
    the count go into the film's record (ledger notes_tags), so misses are counted without guessing."""
    p = notes or (film and os.path.join(ROOT, 'notes', f'{film}.md'))
    tags = note_tags(p)
    if not tags:
        return []
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import ledger
        d = ledger.load(film)
        if d.get('notes_tags') != tags:
            d['notes_tags'] = tags
            ledger.store(d)
    except Exception as e:
        return [f'TAG: the notes\' tags could not be saved to the record ({e})']
    return [f'TAG: note {n} has no "should have caught" (a check\'s name, or none): add it to the notes table'
            for n, t in tags.items() if not t]


def record_faults(rec):
    """check-catches change 1 (Sam's Y, 20 Nov): this chat ran pre-flight but the check record holds nothing from it."""
    if not rec or not os.path.exists(rec):
        return []
    films, start = set(), None
    for ln in open(rec, encoding='utf-8'):
        try:
            x = json.loads(ln)
        except ValueError:
            continue
        start = start or x.get('timestamp')
        for c in (x.get('message') or {}).get('content') or []:
            if isinstance(c, dict) and c.get('type') == 'tool_use':
                films |= set(re.findall(r'preflight\.py\s+([\w-]+)\s', str((c.get('input') or {}).get('command', ''))))
    if not films or not start:
        return []
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ledger
    return [f'RECORD: pre-flight ran on {f} in this chat but the check record (notes/ledger/{f.replace("_", "-")}/'
            'checks.jsonl) holds nothing from it: find why it did not save before handing over'
            for f in sorted(films) if not (ledger.record_since(f, start) or ledger.record_since(f.replace('_', '-'), start))]


def cost_faults(film, notes=None):
    """Job 2 (Sam, 19 Nov): the cost line is recorded at every handover and shown only on a problem (costline.py)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import costline
    try:
        return costline.faults(film, notes)
    except Exception as e:
        return [f'COST: the cost line could not be recorded ({e})']


def size_faults(film, notes=None):
    """Status check (Sam, 21 Nov: "everything needs checking"): CLAUDE.md "Reading little" keeps a film's notes under
    4,000 words, and "The handover" keeps ONE "Where things stand" of 15 lines at most. Nothing checked either: by
    chat 26 Grand Theft Autism's notes were 11,031 words and the handover 22 lines."""
    p = notes or (film and os.path.join(ROOT, 'notes', f'{film}.md'))
    if not p or not os.path.exists(p):
        return []
    text = open(p, encoding='utf-8').read()
    out, words = [], len(text.split())
    if words > 4000:
        out.append(f'NOTES: {os.path.relpath(p, ROOT)} is {words:,} words (CLAUDE.md "Reading little": under 4,000). '
                   f'Move ticked notes and finished sections to notes/archive/{os.path.basename(p)[:-3]}-notes.md, '
                   'keeping the brief checklist, the estimate, open notes and Where things stand')
    lines = text.splitlines()
    heads = [i for i, ln in enumerate(lines) if ln.startswith('#') and 'where things stand' in ln.lower()]
    if len(heads) > 1:
        out.append(f'HANDOVER: {len(heads)} "Where things stand" sections; keep ONE, move the old ones to '
                   f'notes/archive/{os.path.basename(p)[:-3]}-handovers.md')
    if heads:
        i, n = heads[-1] + 1, 0
        while i < len(lines) and not lines[i].startswith('#'):
            n += bool(lines[i].strip())
            i += 1
        block = '\n'.join(lines[heads[-1]:i]).lower()
        if 'rule request' not in block:
            out.append('HANDOVER: no "Open rule requests" line (CLAUDE.md: search the notes for rule requests not yet '
                       'written and list them, "none" if none)')
        if n > 15:
            out.append(f'HANDOVER: "Where things stand" is {n} lines (CLAUDE.md: 15 at most); move detail to the notes '
                       'or the "For Claude" line')
    return out


def push_faults(rec):
    """Status check (Sam, 21 Nov): CLAUDE.md "Models and chats": push notifications when a render or long job
    finishes, fails or needs Sam, and at every stage end. Chat 26 handed over (a stage end) with none; nothing checked.
    A call the app skips because Sam is watching still counts: the chat tried."""
    if not rec or not os.path.exists(rec):
        return []
    for ln in open(rec, encoding='utf-8', errors='replace'):
        if 'PushNotification' not in ln:
            continue
        try:
            m = json.loads(ln).get('message') or {}
        except ValueError:
            continue
        if m.get('role') == 'assistant' and any(isinstance(b, dict) and b.get('type') == 'tool_use'
                                                and b.get('name') == 'PushNotification' for b in m.get('content') or []):
            return []
    return ['PUSH: no push notification in this chat; send one at the handover (what is done, what Sam is needed for), '
            'and when a render or long job finishes or fails (CLAUDE.md, Models and chats)']


def ledger_faults(film, rec=None):
    """Status check (Sam, 21 Nov): the budget tracker's record of notes, repeated notes and finished stages. On Grand
    Theft Autism every chat's row read 'auto, 0 notes, 0 repeats' (nobody ran `ledger.py log`), and none of the 11
    stages was marked done, so the forecast assumed the whole plan was still ahead and the stage stop could not mean
    anything. This chat must log its row; a stage long past its planned end must be marked."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ledger
    try:
        d = ledger.load(film)
    except Exception:
        return []
    if not d.get('chats'):
        return []
    out, sid = [], ledger.this_sid()
    chat = os.path.basename(rec)[:8] if rec else None
    row = next((c for c in d['chats'] if (sid and c.get('sid') == sid) or (chat and c['chat'] == chat)), None)
    if row and row.get('stage') in ('auto', '', None):
        out.append(f'LEDGER: this chat never logged its stage and Sam\'s notes: run python3 source/ledger.py log {film} '
                   '--stage STAGE --notes N [--repeat "the note | what would have caught it"] (0 notes is fine if none came)')
    o = ledger.open_stage(d)
    if o:
        i, s, share, spent = o
        planned_end = sum(x['pct'] for x in d['stages'][:i + 1])
        if spent > 1.5 * planned_end and spent - planned_end > 2:
            out.append(f"STAGES: the first unfinished stage is '{s['name']}' (planned to end by {planned_end:g}% of a "
                       f"week) but the film has spent {spent:g}%: mark each finished stage with python3 source/ledger.py "
                       f"stage {film} NAME, or the forecast is guesswork")
    return out


def freeze_faults():
    """One route to the kit (Sam's Y, 20 Nov): old-film files loaded, steps swapped and the like may never rise;
    every finished film keeps its bookmark (source/freeze.py)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import freeze
    try:
        return freeze.count_faults() + freeze.bookmark_faults()
    except Exception as e:
        return [f'FREEZE: the count could not be made ({e}); run python3 source/freeze.py count']


def sentence_faults():
    """startup fixes 4 (Sam's Y, 16 Nov): no CLAUDE.md sentence lost; text leaves only word for word (sentences.py)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sentences
    try:
        return sentences.faults()
    except Exception as e:
        return [f'SENTENCE: the check failed ({e}); run python3 source/sentences.py check']

def report(faults, where):
    for f in faults:
        print(f)
    print(f'Checks: handover check {where}: ' + (f'{len(faults)} to settle before handing over (each: fix, '
                                               f'write it in the notes, or answer it)' if faults else 'clean'))
    return 1 if faults else 0


def this_record():
    recs = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
    return max(recs, key=os.path.getmtime) if recs else None


# ------------------------------------------------------------------------------------------------ the hook
def _not_typed(text, transcript):
    """True when the chat record shows this prompt came from a parent chat's seed, a task notice or a peer."""
    try:
        tail = open(transcript, 'rb').read()[-400_000:].decode('utf-8', 'replace').splitlines()
    except (OSError, TypeError):
        return False
    for ln in reversed(tail):
        if '"type":"user"' not in ln.replace(' ', ''):
            continue
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if _text((d.get('message') or {}).get('content') or '').strip() == text:
            kind = (d.get('origin') or {}).get('kind')
            if kind in TYPED:
                return False
            return bool(kind in ROBOT or d.get('promptSource') == 'system')
    return None


# cost-fixes chat D (17 Nov): nothing Sam typed was saved after 16 Nov 19:02. The app (2.1.x) now stamps a typed
# message with an origin too ("human", "person", "remote" ...), and any origin at all read as "not typed". Only these
# kinds are robots; an unknown kind with no promptSource "system" counts as Sam (the watcher compares saved vs record).
TYPED = {'human', 'person', 'remote', 'composer', 'voice-call', 'suggestion', 'channel'}
ROBOT = {'task-notification', 'peer', 'coordinator', 'auto-continuation', 'plugin', 'observer-activity'}


def log_hook():
    """UserPromptSubmit: hand Sam's message to a background step that saves it to notes/ledger/sam/CHAT.md and
    commits and pushes it. The hook runs before the chat record holds the prompt, so a parent chat's seed or a task
    notice can only be told apart a moment later: the background step waits for the record (up to 20 s)."""
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return
    text = (inp.get('prompt') or '').strip()
    if not _is_sam(text):
        return
    inp['sid'] = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '') or inp.get('session_id', 'local')
    inp['at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    subprocess.Popen([sys.executable, os.path.abspath(__file__), '_late', json.dumps(inp)],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def _late(inp, wait=20):
    import time
    text = inp['prompt'].strip()
    for _ in range(wait * 2):
        seen = _not_typed(text, inp.get('transcript_path'))
        if seen is not None:
            break
        time.sleep(0.5)
    if seen:
        return
    if seen is None:                           # never found in the record: saved anyway, marked (watcher counts it)
        text += '\n(handover log: not found in the chat record after 20 s; saved as Sam\'s)'
    sid = inp['sid']
    tail = sid.split('_')[-1][-8:].lower()
    os.makedirs(LOGDIR, exist_ok=True)
    p = os.path.join(LOGDIR, f'{tail}.md')
    new = not os.path.exists(p)
    with open(p, 'a', encoding='utf-8') as f:
        if new:
            f.write(f'# Sam\'s messages, chat {sid} (handover.py log)\n\n')
        f.write(f'### {inp["at"]}\n{text}\n\n')
    if any(os.path.exists(os.path.join(ROOT, '.git', x)) for x in ('MERGE_HEAD', 'rebase-merge', 'rebase-apply')):
        return
    rel = os.path.relpath(p, ROOT)
    block = f'### {inp["at"]}\n{text}\n\n'
    import mainline                              # startup-fixes 1 (16 Nov): straight onto the main line, never via
    add = lambda old: None if old and block in old else (old + block if old else open(p, encoding='utf-8').read())
    mainline.to_main({rel: add}, "Sam's message saved (handover log)", root=ROOT)   # a claude/chat-XXXX branch
    # (5t3vj4eb and phxjozvs never reached the main line that way)
    subprocess.run(['git', '-C', ROOT, 'add', rel], capture_output=True)
    subprocess.run(['git', '-C', ROOT, 'commit', '-q', '-m', "Sam's message saved (handover log)", '--', rel],
                   capture_output=True)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    opt = lambda k: rest[rest.index(k) + 1] if k in rest else None
    pos = [a for i, a in enumerate(rest) if not a.startswith('--') and (i == 0 or not rest[i - 1].startswith('--'))]
    if cmd == 'log':
        log_hook()
        return 0
    if cmd == '_late':
        _late(json.loads(rest[0]))
        return 0
    if cmd == 'end':
        rec = this_record()
        film = opt('--film')
        if not film:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import ledger
            film = ledger.film_of(rec)
        return report(quick_faults() + _run(turns(rec), film, opt('--notes')) + model_faults(film, opt('--notes')) + draft_faults(film, opt('--notes'))
                      + finder_faults(film, rec) + unrouted_faults(rec) + branch_faults(film, opt('--notes'))
                      + sentence_faults() + freeze_faults() + cost_faults(film, opt('--notes'))
                      + size_faults(film, opt('--notes')) + ledger_faults(film, rec) + push_faults(rec)
                      + tag_faults(film, opt('--notes')) + record_faults(rec)
                      + (end_stamp(rec) or []),
                      f'(end of chat, {film})')
    if cmd == 'start':
        tail = pos[0].split('_')[-1][-8:].lower()
        p = os.path.join(LOGDIR, f'{tail}.md')
        for f in model_faults(opt('--film'), opt('--notes')):    # a mixed job is split before any work starts
            print(f)
        try:                                                     # early-warning (Sam's 1, 17 Nov): broken first
            import watcher
            for ln in watcher.start_lines():
                print(ln)
        except Exception as e:
            print(f'BROKEN (watcher): the watcher could not run at start ({e})')
        nf = opt('--notes') or (opt('--film') and os.path.join(ROOT, 'notes', f"{opt('--film')}.md"))
        if nf and os.path.exists(nf):                            # startup-fixes 3: read this, not the whole file
            print(f'handover: the notes to read ({os.path.relpath(nf, ROOT)}; nothing else of it unless a note names it):')
            print(open_notes(nf))
        if opt('--film'):                                        # Sam's Y, 15 Nov: chats 29/31 grepped instead
            print(f'handover: for each note, look at the code with ONE step: python3 source/page.py {opt("--film")} '
                  'show "the note\'s words" --shot SHOT --at SECONDS --who WHO (shot, time and who from the notes table; ~40 lines, '
                  'the functions it touches); never grep or sed a film file first')
        ends = os.path.join(ROOT, 'notes', 'logs', 'handover-end.log')
        parent = pos[0].split('_')[-1]
        if not (os.path.exists(ends) and any(ln.split('\t')[-1].strip() == parent for ln in open(ends, encoding='utf-8'))):
            print(f'handover: the last chat ({pos[0][-8:]}) has no `handover.py end` on record: run '
                  '`python3 source/handover.py end --film FILM` now and settle what it lists before new work')
        if not os.path.exists(p):
            print(f'handover: no saved log for {pos[0]}; list_events kinds ["user"], newest pages only, then `dump`')
            for f in freeze_faults():
                print(f)
            return 2
        return report(_run(turns(p), opt('--film'), opt('--notes')) + freeze_faults(), f'(start, {pos[0][-8:]})')
    if cmd == 'dump':
        tr = sorted(x for f in pos for x in turns(f))
        return report(_run(tr, opt('--film'), opt('--notes')), '(from list_events)')
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
