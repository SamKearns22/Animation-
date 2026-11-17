#!/usr/bin/env python3
"""Finder reminder: one line, at a chat's first hand search of a film's code, when that chat has not used the code
finder (page.py FILM show) yet (finder-use Option 1, Sam's 1 on 17 Nov). It warns, never blocks: a build chat may
search on purpose.

Why: the reminder printed at chat start, and the end-of-day flag (one show call anywhere silenced it for all chats),
never reached the moment of searching; on 16 Nov 6 of 19 Opus chats never called the finder and hand search of the
film's code cost 6.65% of a week.

MAP
  film_re() ...... every film's code: source/NAME*.py for each notes/NAME.md (or archive/) that has a source/NAME.py
  main() ......... PostToolUse hook (Bash, Grep, Glob, Read): reads only the chat record's new lines since last time
                   (state in ~/.claude/finderwarn/), notes a show call, and on the first film-code search with no
                   show yet says the line once. A search is what stepcost.kind_of calls a 'film-file search'.

    python3 .claude/hooks/finderwarn.py test
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'source'))
STATE = os.path.expanduser('~/.claude/finderwarn')
SAY = ("FINDER: this is a hand search of {film}'s code and this chat has not used the code finder yet. For a note, "
       "look first with ONE step: python3 source/page.py {film} show \"the note's words\" --shot SHOT --at SECONDS "
       "--who WHO (about 40 lines, the functions it touches). Building something new may search on purpose; then "
       "carry on.")


def film_re():
    names = []
    for f in os.listdir(os.path.join(ROOT, 'notes')) + os.listdir(os.path.join(ROOT, 'notes', 'archive')):
        code = f[:-3].replace('-', '_')
        if f.endswith('.md') and code not in names and os.path.exists(os.path.join(ROOT, 'source', code + '.py')):
            names.append(code)
    if not names:
        return re.compile(r'(?!x)x')
    return re.compile(r'source/(%s)[A-Za-z0-9_]*\.py' % '|'.join(sorted(map(re.escape, names), key=len, reverse=True)))


def decide(inp, state_dir=STATE):
    import stepcost
    name, tin, path = inp.get('tool_name'), inp.get('tool_input') or {}, inp.get('transcript_path') or ''
    os.makedirs(state_dir, exist_ok=True)
    sp = os.path.join(state_dir, os.path.basename(path) + '.json')
    st = {'offset': 0, 'shown': False, 'warned': False}
    try:
        st.update(json.load(open(sp)))
    except (OSError, ValueError):
        pass
    if st['warned']:
        return None
    try:
        with open(path, 'rb') as f:
            f.seek(st['offset'])
            for raw in f:
                if not raw.endswith(b'\n'):
                    break
                st['offset'] += len(raw)
                if b'page.py' not in raw or b'"tool_use"' not in raw:
                    continue
                try:
                    blocks = (json.loads(raw).get('message') or {}).get('content') or []
                except ValueError:
                    continue
                if any(isinstance(b, dict) and b.get('type') == 'tool_use'
                       and stepcost.SHOW.search((b.get('input') or {}).get('command', '')) for b in blocks):
                    st['shown'] = True
    except OSError:
        pass
    cmd = tin.get('command', '') if name == 'Bash' else ''
    if stepcost.SHOW.search(cmd):
        st['shown'] = True
    out = None
    fr = film_re()
    if not st['shown'] and stepcost.kind_of(name, tin, fr) == 'film-file search':
        where = ' '.join(str(tin.get(k, '')) for k in ('command', 'path', 'glob', 'pattern', 'file_path'))
        film = fr.search(where).group(1).replace('_', '-')
        st['warned'] = True
        text = SAY.format(film=film)
        out = {'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': text}}
    json.dump(st, open(sp, 'w'))
    return out


def main():
    try:
        out = decide(json.load(sys.stdin))
    except Exception:
        return  # never break a chat over a reminder
    if out:
        print(json.dumps(out))


def test():
    import tempfile
    d = tempfile.mkdtemp()
    film = next(m.group(1) for m in [film_re().search('source/protest_tiers.py')] if m)
    bad = []

    def run(tag, calls, has_show=False):
        p = os.path.join(d, tag + '.jsonl')
        with open(p, 'w') as f:
            if has_show:
                f.write(json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Bash',
                        'input': {'command': f'python3 source/page.py {film} show "the flag"'}}]}}) + '\n')
        return [decide({'tool_name': n, 'tool_input': i, 'transcript_path': p}, os.path.join(d, 'st'))
                for n, i in calls]
    grep = ('Bash', {'command': 'grep -n "def flag" source/protest_tiers.py'})
    shared = ('Bash', {'command': 'grep -n "def arm" source/moves.py'})
    r = run('a', [shared, grep, grep])
    if r[0] or not r[1] or r[2]:
        bad.append(f'no show: want quiet on a shared tool, one line at the first film search, then quiet; got {r}')
    if any(run('b', [grep, grep], has_show=True)):
        bad.append('warned after a show call')
    print('finderwarn test: ' + ('OK' if not bad else 'FAILED: ' + '; '.join(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(test() if sys.argv[1:] == ['test'] else main())
