#!/usr/bin/env python3
"""override: Sam's code word (Sam, 23 Nov; proposal override-word, his pick: option 2, "one word skips everything").
"If I'm at 99% usage and I need an animatic so I can see something in motion, it is very frustrating if I can't
prevent the checks from running and locking me out of seeing the product ... I can run them again once the usage is
back." When Sam's own latest message holds the word Override (whole word, any case), every check, guard or step
between him and that one ask is skipped; each skip is logged and named to him in a "Checks: skipped by Override: ..."
line. It lasts until his next message. Never skipped: Sam's locked shots, deleting work, saving to GitHub.
A chat cannot fake it: the word is read from Sam's real message in the chat's own record (never from a file a chat
could write, nor from the opening prompt a chat sends the next one: marked "not typed" in the record); handover.py still flags a chat that claims an Override Sam never typed.

MAP
  WORD ............. the word, whole, any case
  sam_said ......... Sam's latest real message in a chat record (tool results, hook feedback, system notices skipped)
  record ........... the chat record: a hook's transcript_path, else the newest .jsonl under ~/.claude/projects
  active ........... Sam's latest message holds the word (the text, or None)
  skip(what) ....... when active: log it to notes/logs/overrides.log, print the Checks line, return True
  refuse(msg) ...... a guard's stop: skipped (printed) under Override, else sys.exit(msg)
  prompt ........... UserPromptSubmit hook: logs each Override Sam types (when, chat, his words)

    python3 source/override.py prompt     (hook)
    python3 source/override.py status     (is an Override in force in this chat now?)
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, 'notes', 'logs', 'overrides.log')
WORD = re.compile(r'(?i)\boverride\b')
NOT_SAM = ('<', '[SYSTEM', 'Stop hook feedback', 'Caveat:', '[Request interrupted')


def _text(entry):
    """Sam's typed words in one record line, or None when the line is not a message he typed."""
    if entry.get('type') != 'user' or entry.get('isMeta') or entry.get('isSidechain'):
        return None
    if entry.get('textNotTyped') or entry.get('promptSource') == 'system':
        return None             # chat 53 (23 Nov): the opening prompt one chat writes for the next (create_session) is
                                # recorded as a user line but marked not typed; its "Sam's Override" was read as his word
    c = entry.get('message', {}).get('content')
    if isinstance(c, list):
        if any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            return None
        c = ' '.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    if not isinstance(c, str):
        return None
    c = c.strip()
    if not c or c.startswith(NOT_SAM):
        return None
    return c


def sam_said(path):
    """Sam's latest real message in the chat record at path ('' when none)."""
    try:
        raw = open(path, 'rb').read()[-4_000_000:].decode('utf-8', 'replace').splitlines()
    except (OSError, TypeError):
        return ''
    for ln in reversed(raw):
        try:
            t = _text(json.loads(ln))
        except ValueError:
            continue
        if t is not None:
            return t
    return ''


def record(path=None):
    if path and os.path.exists(path):
        return path
    fs = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
    return max(fs, key=os.path.getmtime) if fs else None


def active(path=None):
    said = sam_said(record(path))
    return said if WORD.search(said) else None


def _log(kind, what, path=None):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    chat = os.path.basename(record(path) or 'unknown')[:8]
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write('\t'.join([datetime.now(timezone.utc).isoformat(timespec='minutes'), chat, kind,
                           ' '.join(str(what).split())[:300]]) + '\n')


def skip(what, path=None, out=sys.stdout):
    """True (and logged, and named) when Sam's Override skips this check."""
    if not active(path):
        return False
    _log('skipped', what, path)
    print(f'Checks: skipped by Override: {" ".join(str(what).split())[:200]}', file=out)
    return True


def refuse(msg, path=None):
    """A guard's stop: under Sam's Override it is named and skipped; otherwise the tool stops with msg."""
    if skip(msg, path):
        return
    sys.exit(msg)


def advise(msg):
    """Rule 119 (Sam, 26 Nov): a pre-flight or body check never locks out work Sam asked for. It prints its concern
    (with the circled stills and the why-line when Sam asks for them) and the work goes ahead."""
    print('Concerns (advice only, rule 93): ' + msg, flush=True)


def prompt(stdin=None):
    try:
        data = json.loads(stdin if stdin is not None else sys.stdin.read() or '{}')
    except ValueError:
        return 0
    p = data.get('prompt') or ''
    if WORD.search(p):
        _log('sam', p[:300], data.get('transcript_path'))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['prompt']:
        __import__('hookran').ran('override.py prompt')
        sys.exit(prompt())
    if a[:1] == ['status']:
        s = active()
        print(f'Override in force: "{s[:120]}"' if s else 'no Override in force')
        sys.exit(0)
    print(__doc__)
