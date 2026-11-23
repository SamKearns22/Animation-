#!/usr/bin/env python3
"""watcher: the early-warning system (early-warning Option 1, Sam's 1 on 17 Nov, PLUS Sam: "it needs to adapt to new
systems we build too"). Every automatic system has a PROMISE (the real result it must reach) and a PROOF read from
the real record, never from the system's own report.

Why: chat switching, the people kit and the code finder all failed silently last week, and Sam found each one days
later; the message saver stopped on 16 Nov 19:02 and nobody saw. Checks read notes, background steps hid errors,
and a seen fault had no owner.

MAP
  PROMISES ........ one entry per system: id, promise (plain words), proof: a live check below, 'kittest NAME', or
                    'named: why there is no live check'. A NEW hook, handover check or pack tool must add its entry
                    here (and a kittest) or the watcher flags it as UNLISTED at every chat start and Stop.
  systems() ....... what exists now, found by reading: every hook command in .claude/settings.json, every
                    *_faults check in source/handover.py, every source tool the job packs name (guides/job-packs.md)
  live checks ..... saver (Sam's typed messages in this chat's record vs his saved log), guard (routine work that ran
                    on Opus), finder (film code edited with no show and no reminder), kits (kit list vs Sam's
                    recorded Y's), kittests (the last background run's FAILs), hooks (every hook file runs)
  BROKEN .......... notes/logs/broken.md on the main line: a standing list; a fault stays until its check passes
                    again or a chat names it (`watcher.py name ID "why"`); `handover.py start` lists it first
  stop ............ Stop hook: runs the live checks (a few seconds); a NEW fault blocks once with the line for Sam
                    ("Broken: ...; fixing it first") and a push; once a day it asks for the "Watcher: N checks ran,
                    all held" line, so a silent watcher is itself a sign
  start ........... in handover.py start: the BROKEN list, UNLISTED systems, the last kittest run's FAILs
  rules ........... ruleproofs.py (lesson 7): every rule's proof; a broken one or a new rule with no example is a
                    fault here and a STOP at handover end; one RULES line at start
  replay .......... the number to beat: last week's four failures, each caught from its own record (kittest
                    watcher_catches_last_weeks_four)

    python3 source/watcher.py check            (all live checks on this chat; prints faults)
    python3 source/watcher.py unlisted         (systems with no promise)
    python3 source/watcher.py name ID "why"    (a chat owns a fault: named, off the standing list)
    python3 source/watcher.py kittests-bg      (setup.sh: the kit tests in the background, result to notes/logs)
"""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'source'))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
LOGS = os.path.join(ROOT, 'notes', 'logs')
BROKEN = 'notes/logs/broken.md'
DAYS = 'notes/logs/watcher-days.log'           # the days the alive line was asked for (main line)
KITLOG = os.path.join(LOGS, 'kittests-last.log')     # local to the chat's machine: the background run's result
STATE = os.path.expanduser('~/.claude/watcher')

PROMISES = {
    # hooks (.claude/settings.json)
    'setup.sh': ('the tools are installed and the newest main line is fetched before Sam\'s first message',
                 'live hooks'),
    'costwatch.py': ('every step of every chat is priced; amber and red are said at 250k / 370k', 'kittest cost_watch_lines'),
    'handover.py log': ('every message Sam types is saved to notes/ledger/sam/ and pushed to the main line', 'live saver'),
    'ledger.py auto': ('every chat has a cost row with its steps, kinds and search record', 'kittest cost_rows_reach_the_main_line'),
    'propose.py hook': ('no change is put to Sam without the proposal route', 'named: its block is the proof; a let-through is logged to notes/proposals/unrouted.md and listed by handover end'),
    'modelguard.py': ('no routine work (finish.py, a whole-film render, a splice) runs on Opus or Fable', 'live guard'),
    'humancheck.py sendgate': ('no clip reaches Sam without a body check record, clean or each line answered in the notes (named-lines)', 'kittest body_send_gate'),
    'finderwarn.py': ('a chat that hand-searches a film\'s code before using the finder is told so at once', 'live finder'),
    'watcher.py stop': ('every promise here is checked at the end of every reply; a daily line shows it is alive', 'live hooks'),
    # handover checks (source/handover.py)
    'model_faults': ('a Next line never joins Opus work with Sonnet work', 'named: the old word check; replaced by modelguard.py once it has caught everything this caught'),
    'draft_faults': ('the latest animatic and its clean render are on GitHub', 'named: its own fault line in handover end is the proof'),
    'quick_faults': ('handover end runs the quick film checks', 'named: its own fault line in handover end is the proof'),
    'finder_faults': ('a chat that edited a film\'s code without the finder is named at handover', 'kittest finder_reminder_per_chat'),
    'rule_faults': ('no rule without a working check: every rule has its saved bad example and a kittest that catches it; a new rule with none stops the handover (lesson 7)', 'kittest rule_proofs_gate'),
    'unrouted_faults': ('a change that slipped the proposal route is named at handover', 'named: reads propose.py\'s log'),
    'branch_faults': ('every branch with work off the main line is merged or named', 'named: branches.py scan at every start'),
    'cost_faults': ('the film\'s cost line is recorded at every handover and shown only on a problem', 'kittest quiet_cost_line'),
    'sentence_faults': ('no CLAUDE.md sentence is lost', 'kittest claude_md_sentences_never_lost'),
    'freeze.py': ('the count of old-film loads and the bookmarks of finished films', 'kittest finished_films_keep_their_bookmark'),
    'freeze_faults': ('old-film loads never rise and every finished film keeps its bookmark', 'kittest finished_films_keep_their_bookmark'),
    'tag_faults': ('each of Sam\'s notes is tagged with the check that should have caught it', 'named: its own fault line in handover end is the proof'),
    'record_faults': ('a pre-flight run leaves its check record', 'named: its own fault line in handover end is the proof'),
    'size_faults': ('a film\'s notes stay under 4,000 words and its handover under 15 lines, with its rule-requests line', 'kittest handover_status_checks'),
    'ledger_faults': ('every chat logs its stage and Sam\'s notes; finished stages are marked', 'kittest handover_status_checks'),
    'push_faults': ('every chat sends Sam a push notification at its handover', 'kittest handover_status_checks'),
    'dearest_faults': ('the week\'s five dearest things are re-ranked at least every 7 days and suggested to Sam', 'kittest dearest_things_named'),
    # pack tools (guides/job-packs.md)
    'catalogue.py': ('the kit list is current', 'live kits'),
    'codemap.py': ('every film file opens with a MAP', 'named: used by hand'),
    'compare.py': ('two renders compared side by side', 'named: used by hand'),
    'critique.py': ('fresh-eye critique packs', 'named: the critique gate (rule 89) in preflight'),
    'finish.py': ('Hook Text and sign-off on every animatic and final', 'named: rule 75 checks in preflight'),
    'handover.py': ('nothing Sam says is dropped between chats', 'live saver'),
    'kittests.py': ('every kit check passes against the fault that taught it', 'live kittests'),
    'ledger.py': ('every film\'s cost is recorded', 'kittest cost_rows_reach_the_main_line'),
    'page.py': ('a note finds its code in one step', 'live finder'),
    'plan.py': ('the plan stage', 'named: used by hand'),
    'posegallery.py': ('pose sheets', 'named: used by hand'),
    'preflight.py': ('no animatic or final with an open fault (rule 59)', 'named: film_engine refuses a render without its pass'),
    'rough.py': ('the rough sheet', 'named: used by hand'),
    'waivers.py': ('no warning waves through in a bunch: each one left on a film has its own written answer, and a check that could not see the film is cured, never answered (rule 59, lesson named-lines)', 'kittest named_lines_each_answered'),
    'staging.py': ('no shot reaches Sam as a clip or animatic before he has seen its framing (rule 11, lesson staging-stills)', 'kittest staging_stills_milburn_replay'),
    'satire_template.py': ('a new satire film starts from the house template', 'named: used by hand'),
}


# ------------------------------------------------------------------------------------------------ what exists
def systems():
    """Every system that exists now, found by reading (so a new one is seen without anyone listing it)."""
    found = set()
    try:
        hooks = json.load(open(os.path.join(ROOT, '.claude', 'settings.json')))['hooks']
    except (OSError, ValueError, KeyError):
        hooks = {}
    for groups in hooks.values():
        for g in groups:
            for h in g.get('hooks', []):
                m = re.search(r'([\w.-]+\.(?:py|sh))"?\s*(\w+)?', h.get('command', ''))
                if m:
                    found.add(m.group(1) + (' ' + m.group(2) if m.group(2) else ''))
    try:
        found |= set(re.findall(r'^def (\w+_faults)\(', open(os.path.join(ROOT, 'source', 'handover.py')).read(), re.M))
    except OSError:
        pass
    try:
        packs = open(os.path.join(ROOT, 'guides', 'job-packs.md'), encoding='utf-8').read()
        found |= {m for m in re.findall(r'(?:source/|`)([a-z_]+\.py)', packs)
                  if os.path.exists(os.path.join(ROOT, 'source', m))}
    except OSError:
        pass
    return found


def unlisted():
    """Systems with no promise, and promises whose proof names a kittest that does not exist."""
    out = sorted(s for s in systems() if s not in PROMISES)
    try:
        tests = set(re.findall(r'^@test\ndef (\w+)', open(os.path.join(ROOT, 'source', 'kittests.py')).read(), re.M))
    except OSError:
        tests = set()
    if tests:
        out += [f'{s} (its proof names kittest {p.split()[1]}, which does not exist)' for s, (_, p) in PROMISES.items()
                if p.startswith('kittest ') and p.split()[1] not in tests]
    return out


# ------------------------------------------------------------------------------------------------ live checks
def _records_lines(path):
    try:
        for raw in open(path, encoding='utf-8', errors='replace'):
            try:
                yield json.loads(raw)
            except ValueError:
                continue
    except (OSError, TypeError):
        return


def typed_messages(path):
    """[(timestamp, text)] Sam typed in this chat, by the record's own marks (handover.py TYPED/ROBOT)."""
    import handover as H
    out = []
    for d in _records_lines(path):
        if d.get('type') != 'user' or d.get('isSidechain') or d.get('isMeta'):
            continue
        c = (d.get('message') or {}).get('content')
        if isinstance(c, list):
            if any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in c):
                continue
            c = ' '.join(b.get('text', '') for b in c if isinstance(b, dict) and b.get('type') == 'text')
        text = (c or '').strip()
        kind = (d.get('origin') or {}).get('kind')
        robot = kind not in H.TYPED and (kind in H.ROBOT or d.get('promptSource') == 'system')
        if text and H._is_sam(text) and not robot:
            out.append((d.get('timestamp') or '', text))
    return out


def saver_faults(path, sid=None, logdir=None, now=None):
    """Each message Sam typed in this chat is in his saved log (the saver writes it there within ~20 s)."""
    sid = sid or os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '')
    if not sid:
        return []
    logdir = logdir or os.path.join(ROOT, 'notes', 'ledger', 'sam')
    p = os.path.join(logdir, sid.split('_')[-1][-8:].lower() + '.md')
    saved = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    now = now or datetime.now(timezone.utc)
    missed = 0
    for ts, text in typed_messages(path):
        try:
            age = (now - datetime.fromisoformat(ts.replace('Z', '+00:00'))).total_seconds()
        except ValueError:
            age = 999
        if age > 60 and ' '.join(text.split())[:60] not in ' '.join(saved.split()):
            missed += 1
    return [f'saver|the message saver missed {missed} of Sam\'s messages in this chat (handover.py log); his words '
            'are not on GitHub'] if missed else []


def guard_faults(path):
    """No routine command ran on Opus/Fable without the guard stopping it (or a logged GUARD_OK escape)."""
    import modelguard as G
    pending, ran = {}, []
    for d in _records_lines(path):
        m = d.get('message') or {}
        if d.get('isSidechain'):
            continue
        if d.get('type') == 'assistant':
            for b in m.get('content') or []:
                if isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') == 'Bash':
                    cmd = (b.get('input') or {}).get('command', '')
                    if G.routine(cmd) and G.DEAR.search(m.get('model') or '') and not re.search(r'(^|[;&|\n]\s*)GUARD_OK=', cmd):
                        pending[b.get('id')] = G.routine(cmd)
        elif d.get('type') == 'user' and isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('tool_use_id') in pending:
                    res = json.dumps(b.get('content'))
                    if 'MODEL GUARD' not in res:
                        ran.append(pending[b['tool_use_id']])
    return [f'guard|the model guard let routine work run on Opus ({", ".join(sorted(set(ran)))})'] if ran else []


def finder_faults(path, film=None):
    """A chat that edited a film's code with no show call was reminded at its first hand search."""
    import stepcost
    if not film:
        try:
            import ledger
            film = ledger.film_of(path)
        except Exception:
            return []
    try:
        r = stepcost.search_record(path, film)
    except Exception:
        return []
    if not r['edited film code'] or r['show'] or not r['film'].get('no show'):
        return []
    told = any('FINDER: this is a hand search' in json.dumps(d) for d in _records_lines(path)
               if d.get('type') in ('attachment', 'user', 'system'))
    return [] if told else [f'finder|this chat hand-searched {film}\'s code {r["film"]["no show"]} times with no show '
                            'call and the finder reminder never fired']


def kit_faults(root=ROOT, text=None):
    """The kit list (guides/kit-catalogue.md) carries no "NOT for films until Sam approves" on a kit Sam said Y to."""
    cat = text if text is not None else open(os.path.join(root, 'guides', 'kit-catalogue.md'), encoding='utf-8').read()
    said = ''
    for p in [os.path.join(root, 'notes', 'morning-report.md')] + glob.glob(os.path.join(root, 'notes', 'ledger', 'sam', '*.md')):
        try:
            said += open(p, encoding='utf-8').read().lower() + '\n'
        except OSError:
            pass
    out = []
    for line in cat.splitlines():
        m = re.search(r'\(the ([\w ]+? kit);[^)]*NOT for films until Sam approves', line)
        if m and re.search(re.escape(m.group(1).lower()) + r' approved \(y\)', said):
            out.append(f'kits|the kit list still says the {m.group(1)} is NOT for films, but Sam approved it (Y)')
    return out


def kittest_faults():
    """The last background kit-test run (setup.sh at chat start) passed."""
    if not os.path.exists(KITLOG):
        return []
    txt = open(KITLOG, encoding='utf-8', errors='replace').read()
    if 'kittests:' not in txt:
        return []                                  # still running
    fails = re.findall(r'^FAIL (\w+)', txt, re.M)
    return [f'kittests|kit tests failing: {", ".join(fails)}'] if fails else []


def hook_faults():
    """Every hook command in settings.json points at a file that exists; the watcher itself is wired in."""
    out = []
    try:
        hooks = json.load(open(os.path.join(ROOT, '.claude', 'settings.json')))['hooks']
    except (OSError, ValueError, KeyError) as e:
        return [f'hooks|.claude/settings.json cannot be read ({e}): no automatic system runs']
    cmds = [h.get('command', '') for gs in hooks.values() for g in gs for h in g.get('hooks', [])]
    for c in cmds:
        m = re.search(r'"?\$CLAUDE_PROJECT_DIR"?/([\w./-]+)', c)
        if m and not os.path.exists(os.path.join(ROOT, m.group(1))):
            out.append(f'hooks|a hook points at a missing file: {m.group(1)}')
    if not any('watcher.py' in c for c in cmds):
        out.append('hooks|the watcher is not wired into the Stop hook')
    # status chat (Sam, 21 Nov): modelguard.py was built and promised on 17 Nov but never wired into settings.json, so
    # it never ran for four days and nothing said so. Every promised hook file must be in a hook command.
    for f in sorted(glob.glob(os.path.join(ROOT, '.claude', 'hooks', '*.py'))):
        name = os.path.basename(f)
        if name in PROMISES and not any(name in c for c in cmds):
            out.append(f'hooks|{name} has a promise but is not wired into .claude/settings.json: it never runs')
    return out


# Sam, 21 Nov: "Why are tools built then not enabled? Keeps happening. Please ensure that doesn't happen again."
# Why it kept happening: systems() found tools only from the wiring, so a tool never wired was invisible; each tool's
# kittest called it directly (it works when called, never that anything calls it); and a job was ticked when its file
# and test existed. So the watcher now also finds tools from the FILES (every hook file, every source tool an adopted
# proposal names), flags any that nothing switches on (unwired), and flags a switched-on step never seen running
# (ran_faults, from the marks source/hookran.py leaves).
OFF = {                    # a tool deliberately not switched on, and why (a chat names it here, Sam sees it in notes)
    'bench_move.py': 'the test-space tool for learning solid-body moves (Sam, chat 32): run by hand by each bench chat '
                     '(named in the film handover and notes/bench/learn-step.md); joins a job pack when the skill passes',
}
SWITCHES = ('.claude/settings.json', '.claude/hooks/setup.sh', 'source/handover.py', 'guides/job-packs.md', 'CLAUDE.md')


def _read(rel, text=None):
    if text is not None:
        return text
    try:
        return open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
    except OSError:
        return ''


def built_tools():
    """Every tool that exists, found from the files: each file in .claude/hooks, and each source or hook tool an
    adopted proposal names. -> {file name: where it was found}"""
    out = {}
    for f in glob.glob(os.path.join(ROOT, '.claude', 'hooks', '*.py')) + glob.glob(os.path.join(ROOT, '.claude', 'hooks', '*.sh')):
        out[os.path.basename(f)] = 'a hook file'
    for f in glob.glob(os.path.join(ROOT, 'notes', 'proposals', '*.md')):
        txt = _read(os.path.relpath(f, ROOT))
        if not re.search(r'^Status: adopted', txt, re.M):
            continue
        import freeze                              # a film's own files are not tools
        for m in set(re.findall(r'(?:source/|\.claude/hooks/)([a-z_]+\.(?:py|sh))', txt)):
            if freeze.FILM.match(m[:-3]):
                continue
            if os.path.exists(os.path.join(ROOT, 'source', m)) or os.path.exists(os.path.join(ROOT, '.claude', 'hooks', m)):
                out.setdefault(m, 'named by adopted proposal ' + os.path.basename(f)[:-3])
    return out


def unwired(settings_text=None):
    """Tools that exist but nothing switches on: not in a hook command, the start-up script, the handover check, the
    job packs or CLAUDE.md, and (for a source tool) not imported or run by any other source file. settings_text: test
    a different settings.json (the kittest replays 17 Nov's)."""
    hooks_txt = _read('.claude/settings.json', settings_text)
    others = ''.join(_read(r) for r in SWITCHES[1:])
    out = []
    for name, why in sorted(built_tools().items()):
        if name in OFF:
            continue
        stem = name.rsplit('.', 1)[0]
        on = name in hooks_txt or (why != 'a hook file' and name in others)
        if not on and why != 'a hook file':
            for f in glob.glob(os.path.join(ROOT, 'source', '*.py')):
                b = os.path.basename(f)
                if b in (name, 'kittests.py', 'watcher.py'):
                    continue
                t = _read(os.path.relpath(f, ROOT))
                if re.search(rf'^\s*(?:import|from)\s+{stem}\b|\bimport .*\b{stem}\b|{re.escape(name)}', t, re.M):
                    on = True
                    break
        if not on:
            out.append(f'unwired|{name} is built ({why}) but nothing switches it on: wire it (a hook in '
                       f'.claude/settings.json, handover end, or a job pack) or name why in watcher.py OFF')
    return out


def ran_faults(path=None):
    """A step switched on in .claude/settings.json that has never been seen running on this machine, though its event
    has happened in this chat (Sam's prompt for UserPromptSubmit, the chat's start for SessionStart, a tool it
    watches for PreToolUse/PostToolUse; Stop steps from the second reply on)."""
    import hookran
    try:
        hooks = json.load(open(os.path.join(ROOT, '.claude', 'settings.json')))['hooks']
    except (OSError, ValueError, KeyError):
        return []
    tools, prompts, started = set(), 0, None
    if path and os.path.exists(path):
        for line in open(path, encoding='utf-8', errors='replace'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if started is None and d.get('timestamp'):
                try:
                    started = datetime.fromisoformat(d['timestamp'].replace('Z', '+00:00')).timestamp()
                except ValueError:
                    pass
            if d.get('type') == 'user' and isinstance(d.get('message', {}).get('content'), str):
                prompts += 1
            for c in (d.get('message', {}).get('content') or []) if isinstance(d.get('message', {}).get('content'), list) else []:
                if isinstance(c, dict) and c.get('type') == 'tool_use':
                    tools.add(c.get('name'))
    out = []
    begun = hookran.since()
    late = begun is None or started is None or begun > started + 300   # marks began mid-chat: judge only steps that keep firing
    for event, groups in hooks.items():
        if late and event in ('SessionStart', 'UserPromptSubmit', 'Stop'):
            continue
        for g in groups:
            matcher = g.get('matcher', '') or ''
            for h in g.get('hooks', []):
                m = re.search(r'([\w.-]+\.(?:py|sh))"?\s*(\w+)?', h.get('command', ''))
                if not m:
                    continue
                name = m.group(1) + (' ' + m.group(2) if m.group(2) and not m.group(2).startswith('test') else '')
                if event == 'SessionStart':
                    due = os.environ.get('CLAUDE_CODE_REMOTE') == 'true'
                elif event == 'UserPromptSubmit':
                    due = prompts >= 1
                elif event == 'Stop':
                    due = prompts >= 2
                else:
                    due = bool(tools) if matcher in ('', '*') else any(re.fullmatch(matcher, t or '') for t in tools)
                if due and hookran.last(name) is None:
                    out.append(f'notrun|{name} is switched on ({event}) but has never been seen running here: '
                               f'check its hook line and that it leaves its mark (source/hookran.py)')
    return out


def _rule_faults():
    """Lesson 7 step 2: a rule whose proof broke (its kittest fails on its saved example) or a new rule with none."""
    import ruleproofs
    return ruleproofs.faults()


def check(path, film=None):
    faults = []
    for fn in (lambda: saver_faults(path), lambda: guard_faults(path), lambda: finder_faults(path, film),
               kit_faults, kittest_faults, hook_faults, unwired, lambda: ran_faults(path), _rule_faults):
        try:
            faults += fn()
        except Exception as e:                      # a check that breaks is itself a fault, never hidden
            faults.append(f'watcher|a check crashed: {type(e).__name__}: {e}')
    faults += [f'unlisted|{s} has no promise in the watcher (source/watcher.py PROMISES): add one and a kittest'
               for s in unlisted()]
    return faults


# ------------------------------------------------------------------------------------------------ the standing list
def _put_broken(new=(), named=None):
    """Add faults to / remove one from notes/logs/broken.md on the main line (in the background)."""
    import mainline
    day = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

    def fn(old):
        lines = [ln for ln in (old or '# Broken (watcher.py): each stays until fixed or named\n\n').splitlines(True)]
        have = {ln.split(' | ')[1] for ln in lines if ln.startswith('- ') and ' | ' in ln}
        if named:
            lines = [ln for ln in lines if not (ln.startswith('- ') and ln.split(' | ')[1:2] == [named[0]])]
            lines.append(f'- named {day} | {named[0]} | {named[1]}\n'.replace('- named', '  - named', 1))
        for f in new:
            sid, what = f.split('|', 1)
            if sid not in have:
                lines.append(f'- {day} | {sid} | {what}\n')
        return ''.join(lines)
    return mainline.to_main({BROKEN: fn}, 'watcher: broken list', root=ROOT)


def _main_text(rel):
    """A file as it stands on the main line (fetched by setup.sh at chat start; falls back to this copy)."""
    import mainline
    r = subprocess.run(['git', '-C', ROOT, 'show', f'origin/{mainline.MAIN}:{rel}'], capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout
    p = os.path.join(ROOT, rel)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def standing():
    """The open faults on the standing list (main line)."""
    return [ln[2:].strip() for ln in _main_text(BROKEN).splitlines() if ln.startswith('- ')]


def owned():
    """Fault ids already on the list or named in the last 7 days: a later chat is not stopped for them again
    (handover.py start lists them instead)."""
    ids = set()
    for ln in _main_text(BROKEN).splitlines():
        parts = [x.strip() for x in ln.split(' | ')]
        if len(parts) >= 3:
            ids.add(parts[1])
    return ids


def stop(stdin=None):
    """Stop hook. Quiet when all holds (but once a day asks for the alive line)."""
    try:
        inp = json.load(stdin or sys.stdin)
    except ValueError:
        return
    path = inp.get('transcript_path')
    if not path or inp.get('stop_hook_active'):
        return
    os.makedirs(STATE, exist_ok=True)
    sp = os.path.join(STATE, os.path.basename(path) + '.json')
    st = {'said': [], 'runs': 0}
    try:
        st.update(json.load(open(sp)))
    except (OSError, ValueError):
        pass
    faults = check(path)
    st['runs'] += 1
    have = owned()
    new = [f for f in faults if f not in st['said'] and f.split('|', 1)[0] not in have]
    day = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    alive = day in _main_text(DAYS) or st.get('alive') == day
    say = []
    if new:
        st['said'] += new
        subprocess.Popen([sys.executable, os.path.abspath(__file__), '_put', json.dumps(new)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        say.append('WATCHER: ' + ' | '.join(f.split('|', 1)[1] for f in new) + '. Put ONE plain line at the top of '
                   'your reply to Sam: "Broken: <what, in plain words>; fixing it first", send a push notification, '
                   'then fix it, or name it with: python3 source/watcher.py name ID "why" (ID is the word before | '
                   'in notes/logs/broken.md).')
    elif not alive:
        n = len([s for s in PROMISES if not PROMISES[s][1].startswith('named')])
        held = 'all held' if not faults else f'{len(faults)} still broken (on the list, each owned)'
        say.append(f'WATCHER (once a day): end your reply to Sam with one line: "Watcher: {n} systems checked, '
                   f'{held}." (a day with no such line means the watcher itself is down).')
    if say and not new:
        st['alive'] = day
        subprocess.Popen([sys.executable, os.path.abspath(__file__), '_day', f'{day}\t{st["runs"]} runs here\n'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    json.dump(st, open(sp, 'w'))
    if say:
        print(json.dumps({'decision': 'block', 'reason': ' '.join(say)}))


def start_lines():
    """For handover.py start: the standing list, systems with no promise, the last kit-test FAILs."""
    out = [f'BROKEN (watcher, fix or name first): {b}' for b in standing()]
    out += [f'UNLISTED (watcher): {s} has no promise; add one to source/watcher.py PROMISES and a kittest'
            for s in unlisted()]
    out += [f'UNWIRED (watcher): {f.split("|", 1)[1]}' for f in unwired()]
    try:                                            # lesson 7 step 2: where the rules stand, worst first
        import ruleproofs
        out.append(ruleproofs.start_line())
    except Exception as e:
        out.append(f'BROKEN (watcher): the rule list could not be read ({e})')
    return out


def main(argv):
    cmd = argv[0] if argv else ''
    if cmd == 'stop':
        __import__('hookran').ran('watcher.py stop')
        try:
            stop()
        except Exception:
            pass                                   # never break a chat; hook_faults sees a missing wire
        return 0
    if cmd == '_day':
        import mainline
        mainline.to_main({DAYS: lambda old: None if old and argv[1][:10] in old else (old or '') + argv[1]},
                         'watcher: alive today', root=ROOT)
        return 0
    if cmd == '_put':
        _put_broken(json.loads(argv[1]))
        return 0
    if cmd == 'name' and len(argv) >= 3:
        print(_put_broken(named=(argv[1], argv[2])) or 'could not reach the main line')
        return 0
    if cmd == 'unlisted':
        u = unlisted()
        print('\n'.join(u) or 'every system has a promise')
        return 1 if u else 0
    if cmd == 'kittests-bg':
        os.makedirs(LOGS, exist_ok=True)
        with open(KITLOG, 'w') as f:
            subprocess.run(['nice', '-n', '19', sys.executable, os.path.join(ROOT, 'source', 'kittests.py')],
                           stdout=f, stderr=subprocess.STDOUT, cwd=ROOT, timeout=1800)
        return 0
    if cmd == 'check':
        recs = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
        path = argv[1] if len(argv) > 1 else max(recs, key=os.path.getmtime)
        f = check(path)
        print('\n'.join(f) or 'watcher: all held')
        return 1 if f else 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
