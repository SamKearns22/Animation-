#!/usr/bin/env python3
"""notesteps: a step counter per note (cost-spike fix step 3, Sam's Y, 27 Nov; notes/proposals/cost-spike-fix.md).

Why: chat 30 spent about 140 steps on four notes (~35 a note). Every step re-reads the whole chat, so steps per note
is the cost: 35 a note = 26.6M pieces read for four notes, 18 a note = 10.0M, 12 a note = 5.8M. Nothing counted them,
so a chat stuck on one note searched on with no one told.

MAP
  note ......... `python3 source/notesteps.py note "8: the whale knocks the helideck away"` at the start of each note
                 (the fix pack's first step per note). With no marker in the chat, a `page.py FILM show` call starts a
                 note, so a round that never marks still counts.
  step() ....... PostToolUse hook (every tool): one tool call = one step on the open note. At 12 steps one line: say
                 what is stuck; at 20 (and every 5 after): stop this note, finish only an edit already made (the clip,
                 the commit), write what is stuck in the film's notes and report it. Never blocks: finishing a fix
                 stays allowed. Each note that passes 12 is a line in notes/logs/notesteps.log (date, chat, note, steps).
  done ......... `notesteps.py done` closes the open note (also closed by the next `note`).
  report ....... this chat's notes and their steps, for the handover and the before/after measure.

    python3 source/notesteps.py test      (kittest notes_step_counter: a chat-30-like overrun is told at 12 and 20)
"""
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STATE = os.path.expanduser('~/.claude/notesteps')
LOG = os.path.join(ROOT, 'notes', 'logs', 'notesteps.log')
ASK, STOP, AGAIN = 12, 20, 5
MARK = re.compile(r'notesteps\.py\s+note\s+(?:"([^"]*)"|\'([^\']*)\'|(\S+))')
DONE = re.compile(r'notesteps\.py\s+done\b')
SHOW = re.compile(r'page\.py\s+[\w-]+\s+show\s+(?:"([^"]*)"|\'([^\']*)\'|(\S+))')

SAY_ASK = ("STEPS: {n} steps on note \"{note}\". Before the next step, say in one line what is stuck (what you are "
           "looking for and why it is not found yet). The aim is 10-18 steps a note.")
SAY_STOP = ("STEPS: {n} steps on note \"{note}\": stop this note now. Finish only an edit already made (render its "
            "clip, commit), then write in the film's notes what is stuck and what would unstick it, and report it with "
            "the round's other notes. Start the next note with: python3 source/notesteps.py note \"N: words\".")


def _load(sp):
    st = {'note': None, 'n': 0, 'marked': False, 'notes': []}
    try:
        st.update(json.load(open(sp)))
    except (OSError, ValueError):
        pass
    return st


def _close(st, chat, log):
    if st['note'] is not None:
        st['notes'].append([st['note'], st['n']])
        if st['n'] >= ASK and log:
            try:
                os.makedirs(os.path.dirname(log), exist_ok=True)
                with open(log, 'a') as f:
                    f.write(f"{date.today()}\t{chat}\t{st['n']}\t{st['note'][:80]}\n")
            except OSError:
                pass
    st['note'], st['n'] = None, 0


def step(inp, state_dir=STATE, log=LOG):
    """One tool call -> the message to show the chat, or None."""
    tin = inp.get('tool_input') or {}
    cmd = tin.get('command', '') if inp.get('tool_name') == 'Bash' else ''
    chat = os.path.basename(inp.get('transcript_path') or 'chat').split('.')[0]
    os.makedirs(state_dir, exist_ok=True)
    sp = os.path.join(state_dir, chat + '.json')
    st = _load(sp)
    m, s = MARK.search(cmd), SHOW.search(cmd)
    if m:
        _close(st, chat, log)
        st['note'], st['n'], st['marked'] = next(g for g in m.groups() if g is not None), 0, True
    elif DONE.search(cmd):
        _close(st, chat, log)
    elif s and not st['marked']:
        _close(st, chat, log)
        st['note'] = next(g for g in s.groups() if g is not None)
    out = None
    if st['note'] is not None and not m:
        st['n'] += 1
        n = st['n']
        if n == ASK:
            out = SAY_ASK.format(n=n, note=st['note'][:60])
        elif n >= STOP and (n - STOP) % AGAIN == 0:
            out = SAY_STOP.format(n=n, note=st['note'][:60])
    json.dump(st, open(sp, 'w'))
    return out


def report(chat=None, state_dir=STATE):
    files = sorted((os.path.join(state_dir, f) for f in os.listdir(state_dir)), key=os.path.getmtime) \
        if os.path.isdir(state_dir) else []
    if chat:
        files = [f for f in files if os.path.basename(f).startswith(chat)]
    if not files:
        return 'notesteps: no note was counted in this chat'
    st = _load(files[-1])
    notes = st['notes'] + ([[st['note'], st['n']]] if st['note'] is not None else [])
    if not notes:
        return 'notesteps: no note was counted in this chat'
    avg = sum(n for _, n in notes) / len(notes)
    return (f'notesteps: {len(notes)} note(s), {avg:.0f} steps a note (aim 10-18): '
            + '; '.join(f'{n} on "{w[:40]}"' for w, n in notes))


def test():
    """The fault, saved as an example: a round like chat 30's (four notes, ~35 steps each, nobody told). Replayed
    here as tool calls: the counter must speak at 12 and at 20, 25, 30 on the stuck note, stay quiet on a note
    finished in 9, start a note from a show call when no marker is used, and log only the overrun."""
    import tempfile
    d = tempfile.mkdtemp()
    log = os.path.join(d, 'log')
    bad = []

    def run(chat, calls):
        said = []
        for c in calls:
            r = step({'tool_name': 'Bash', 'tool_input': {'command': c}, 'transcript_path': chat + '.jsonl'},
                     os.path.join(d, 'st'), log)
            if r:
                said.append(r)
        return said
    grep = 'grep -n "def whale" source/whale.py'
    said = run('c30', ['python3 source/notesteps.py note "8: whale knocks the helideck"'] + [grep] * 35
               + ['python3 source/notesteps.py note "9: the gull"'] + [grep] * 9 + ['python3 source/notesteps.py done'])
    want = ['12 steps', '20 steps', '25 steps', '30 steps', '35 steps']
    if [w for w in want if not any(w in x for x in said)] or len(said) != 5:
        bad.append(f'overrun: told {len(said)} times: {[x[:24] for x in said]}')
    if any('the gull' in x for x in said):
        bad.append('spoke on a note finished in 9 steps')
    lg = open(log).read().splitlines() if os.path.exists(log) else []
    if len(lg) != 1 or '\t35\t' not in lg[0]:
        bad.append(f'log: {lg}')
    said = run('c31', ['python3 source/page.py whale show "the gull lands"'] + [grep] * 12)
    if len(said) != 1 or 'the gull lands' not in said[0]:
        bad.append(f'a show call did not start a note: {said}')
    if run('build', [grep] * 30):
        bad.append('a build chat with no note was told to stop')
    r = report('c30', os.path.join(d, 'st'))
    if '2 note(s)' not in r or '35 on' not in r:
        bad.append('report: ' + r)
    print('notesteps test: ' + ('OK' if not bad else 'FAILED: ' + '; '.join(bad)))
    return not bad, '; '.join(bad) or 'told at 12, 20, 25, 30, 35 on the stuck note; quiet on a 9-step note and on a build chat'


def main(argv):
    if argv[:1] == ['test']:
        return 0 if test()[0] else 1
    if argv[:1] == ['report']:
        print(report(argv[1] if argv[1:] else None))
        return 0
    if argv[:1] in (['note'], ['done']):
        print(f'notesteps: {argv[0]} {" ".join(argv[1:])}'.strip() + ' (counted by the hook)')
        return 0
    try:
        import hookran
        hookran.ran('notesteps.py')
    except Exception:
        pass
    try:
        text = step(json.load(sys.stdin))
    except Exception:
        return 0
    if text:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': text}}))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
