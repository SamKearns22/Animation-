#!/usr/bin/env python3
"""Model guard: an expensive chat (Opus or Fable) may not do routine work (cost-fixes, model-switch Option 1, Sam's 1
on 17 Nov: "a guard that STOPS an expensive chat doing routine work").

Why: the 15 Nov check (handover.py model_faults) read only the words of the notes' Next line, and on 16 Nov the Opus
fix chats spliced animatics and ran finish.py with it silent ("splice" was not on its word list; phone-opened chains
never wrote a Next line). Nothing ever STOPPED a command: there was no PreToolUse hook in git history.

MAP
  routine() ...... a shell command -> the routine piece it RUNS, or None (also used by stepcost.py and watcher.py):
                   finish.py; a whole-film render (`source/FILM.py final|animatic` with no --span); ffmpeg writing
                   into animations/ (the splice). Clips (`final --span`) stay allowed. _runs() takes heredoc bodies,
                   VAR=x prefixes and wrappers (nice, timeout) off, so a search or code that names them is not routine
  served_model() . the model this chat is really running on: the newest assistant line of its own record, the same
                   source costwatch.py prices from (never the notes' words)
  main() ......... PreToolUse hook on Bash: on Opus/Fable + routine -> deny, with what to do instead. Escape (F3):
                   `GUARD_OK="why" ...` in front (a Sonnet open was refused, or the app fell back to Opus) is allowed
                   and logged. Every refusal and escape is a line in notes/logs/modelguard.log (date, chat, model,
                   what, command) for the end-of-film review; the watcher reads it.

    python3 .claude/hooks/modelguard.py test     (kittest: deny on Opus, allow on Sonnet, allow clips, escape logged)
"""
import json, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(ROOT, 'notes', 'logs', 'modelguard.log')
DEAR = re.compile(r'opus|fable|mythos', re.I)
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\s*\1[ \t]*(?=\n|$)", re.S)
WRAP = {'nice', 'nohup', 'time', 'timeout', 'env', 'exec', 'stdbuf'}


def _runs(cmd):
    """The commands a shell line really runs, each as its words: heredoc bodies (code being written) dropped, split
    on && ; || | and newlines, VAR=x prefixes and wrappers (nice, timeout 600 ...) taken off."""
    import shlex
    out = []
    for part in re.split(r'&&|\|\||[;|\n]', HEREDOC.sub('\n', cmd or '')):
        try:
            w = shlex.split(part, comments=True)
        except ValueError:
            w = part.split()
        while w and (('=' in w[0] and not w[0].startswith('-')) or w[0] in WRAP or re.fullmatch(r'-?[\d.]+[smh]?|-n', w[0])):
            w = w[1:]
        if w:
            out.append(w)
    return out


SAY = ("MODEL GUARD: this chat runs on {model}, and {what} is routine work for a Sonnet chat (CLAUDE.md, Models by "
       "stage). Do not run it here. Commit the fixes and clips, write the clip and finish commands in the film's "
       "notes, then open the Sonnet chat (create_session, model claude-sonnet-5-5, the Animation- project attached) "
       "and hand it those commands. Only if opening a Sonnet chat was refused, or the app fell back to this model, "
       "run it again with GUARD_OK=\"the reason\" in front; that is logged for the film's review.")


def routine(cmd):
    """The routine piece a shell command RUNS ('finish.py', 'whole-film render', 'splice into animations/'), or None.
    Judged on what runs, never on words: a grep for finish.py, or code that mentions it, is not routine work."""
    for w in _runs(cmd):
        head = w[0].split('/')[-1]
        args = [a for a in w[1:] if not a.startswith('-')]
        if head.startswith('python') and args:
            if args[0].endswith('finish.py'):
                return 'finish.py'
            if re.fullmatch(r'(\./)?source/\w+\.py', args[0]) and args[1:2] in (['final'], ['animatic']) \
                    and '--span' not in w:
                return 'whole-film render'
        if head.startswith('ffmpeg') and args and 'animations/' in w[-1]:
            return 'splice into animations/'
    return None


def served_model(transcript):
    """The model of the newest assistant reply in this chat's own record ('' when there is none yet)."""
    try:
        with open(transcript, 'rb') as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 600_000))
            tail = f.read().decode('utf-8', 'replace').splitlines()
    except (OSError, TypeError):
        return ''
    for ln in reversed(tail):
        if '"assistant"' not in ln:
            continue
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if d.get('type') == 'assistant' and not d.get('isSidechain'):
            m = (d.get('message') or {}).get('model')
            if m and m != '<synthetic>':
                return m
    return ''


def log(kind, model, what, cmd, sid):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write('\t'.join([datetime.now(timezone.utc).isoformat(timespec='minutes'), sid[-8:], model, kind, what,
                           ' '.join(cmd.split())[:200]]) + '\n')


def decide(inp):
    """The hook's answer for one PreToolUse input: None (allow silently) or the JSON to print."""
    if inp.get('tool_name') != 'Bash':
        return None
    cmd = (inp.get('tool_input') or {}).get('command', '')
    what = routine(cmd)
    if not what:
        return None
    model = served_model(inp.get('transcript_path'))
    if not DEAR.search(model):
        return None
    sid = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '') or inp.get('session_id', '') or 'local'
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source'))
    if __import__('override').skip(f'model guard ({what} on {model})', inp.get('transcript_path'), sys.stderr):
        log('override', model, what, cmd, sid)
        return None
    if re.search(r'(^|[;&|\n]\s*)GUARD_OK=', cmd):
        log('escape', model, what, cmd, sid)
        return None
    log('refused', model, what, cmd, sid)
    why = SAY.format(model=model, what=what)
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
                                   'permissionDecisionReason': why}, 'systemMessage': why}


def main():
    try:                                   # Sam, 21 Nov: every switched-on step leaves a 'seen running' mark
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source'))
        import hookran
        hookran.ran('modelguard.py')
    except Exception:
        pass
    try:
        inp = json.load(sys.stdin)
        out = decide(inp)
    except Exception:
        return  # never break a chat over the guard
    if out:
        print(json.dumps(out))


def test():
    import tempfile
    global LOG
    d = tempfile.mkdtemp()
    LOG = os.path.join(d, 'g.log')

    def rec(model):
        p = os.path.join(d, model + '.jsonl')
        with open(p, 'w') as f:
            f.write(json.dumps({'type': 'assistant', 'message': {'model': model, 'content': []}}) + '\n')
        return p
    opus, sonnet = rec('claude-opus-5-5'), rec('claude-sonnet-5-5')
    ask = lambda c, t: decide({'tool_name': 'Bash', 'tool_input': {'command': c}, 'transcript_path': t,
                               'session_id': 'test'})
    cases = [  # (command, record, refused?) — the 16 Nov routine tails, and what must stay allowed
        ('python3 source/finish.py animations/drafts/x-clean.mp4 animations/drafts/x-animatic.mp4 --film x', opus, 1),
        ('python3 source/protest_tiers.py final /tmp/a.mp4 --small', opus, 1),
        ('ffmpeg -i a.mp4 -i b.mp4 -filter_complex concat=n=2 animations/drafts/protest-tiers-animatic.mp4', opus, 1),
        ('python3 source/protest_tiers.py final /tmp/c.mp4 --small --span 12 15', opus, 0),
        ('python3 source/finish.py a.mp4 b.mp4 --film x', sonnet, 0),
        ('python3 source/page.py protest-tiers show "the flag"', opus, 0),
        ('git add animations/drafts/x-animatic.mp4', opus, 0),
        ('GUARD_OK="sonnet open refused" python3 source/finish.py a b --film x', opus, 0),
        ('grep -n "finish.py" guides/job-packs.md', opus, 0),
        ("python3 - <<'EOF'\nos.system('ffmpeg -i a animations/drafts/x.mp4')\nEOF", opus, 0),
        ('cd /r && timeout 900 nice -n 19 python3 source/finish.py a b --film x', opus, 1),
    ]
    bad = [c for c, t, r in cases if bool(ask(c, t)) != bool(r)]
    logged = open(LOG).read()
    if 'escape' not in logged or logged.count('\trefused\t') != 4:
        bad.append('log: ' + logged)
    print('modelguard test: ' + ('OK, 11 cases' if not bad else 'FAILED: ' + '; '.join(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(test() if sys.argv[1:] == ['test'] else main())
