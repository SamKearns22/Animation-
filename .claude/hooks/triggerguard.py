#!/usr/bin/env python3
"""Scheduled-task guard (Sam, 26 Nov: "simple enough that a proposal route isn't needed").

Why: a scheduled task that starts a fresh chat on each firing (create_trigger with create_new_session_on_fire=true)
gets NO repository attached and the default model; the tool can set neither. Open Wounds chat 17 made one; chat 18
(fired 26 Nov 03:20) ran on Sonnet without the Animation- project and could do nothing.

MAP
  decide() ... PreToolUse input -> None (allow) or the deny JSON. Refuses create_trigger with
               create_new_session_on_fire true; says the working way (wake a chat that has the project, which then
               opens the work chat with create_session). "Override" in Sam's latest message skips it (logged).
  main() ..... the hook.   python3 .claude/hooks/triggerguard.py test   (kittest scheduled_task_guard)
"""
import json, os, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(ROOT, 'notes', 'logs', 'triggerguard.log')

SAY = ("SCHEDULED-TASK GUARD: a scheduled task that starts a fresh chat on each firing gets NO Animation- project and "
       "the default model (Open Wounds chat 18, 26 Nov, could do nothing). Do this instead: schedule a wake-up into a "
       "chat that already has the project (send_later, or create_trigger with persistent_session_id and without "
       "create_new_session_on_fire), whose message tells it to open the work chat with create_session (source_url "
       "the repo, revision claude/create-claude-md-oe8z4g, the model and effort the handover names).")


def log(kind, inp):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    sid = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '') or inp.get('session_id', '') or 'local'
    name = str((inp.get('tool_input') or {}).get('name', ''))[:80]
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write('\t'.join([datetime.now(timezone.utc).isoformat(timespec='minutes'), sid[-8:], kind, name]) + '\n')


def decide(inp):
    if not str(inp.get('tool_name', '')).endswith('create_trigger'):
        return None
    if (inp.get('tool_input') or {}).get('create_new_session_on_fire') not in (True, 'true', 'True'):
        return None
    try:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        if __import__('override').skip('scheduled-task guard (fresh chat per firing)', inp.get('transcript_path'),
                                       sys.stderr):
            log('override', inp)
            return None
    except Exception:
        pass
    log('refused', inp)
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
                                   'permissionDecisionReason': SAY}, 'systemMessage': SAY}


def main():
    try:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        __import__('hookran').ran('triggerguard.py')
    except Exception:
        pass
    try:
        out = decide(json.load(sys.stdin))
    except Exception:
        return  # never break a chat over the guard
    if out:
        print(json.dumps(out))


def test():
    import tempfile
    global LOG
    LOG = os.path.join(tempfile.mkdtemp(), 't.log')
    T = 'mcp__claude-code-remote__create_trigger'
    cases = [  # (tool, input, refused?) — the first is Open Wounds chat 17's kind of call (26 Nov)
        (T, {'name': 'Open Wounds chat 18', 'prompt': 'carry on', 'run_once_at': '2026-11-26T03:20:00Z',
             'create_new_session_on_fire': True, 'initiation': 'own_followup'}, 1),
        (T, {'name': 'wake', 'prompt': 'open chat 18', 'persistent_session_id': 'session_x',
             'run_once_at': '2026-11-26T03:20:00Z', 'initiation': 'own_followup'}, 0),
        (T, {'name': 'self', 'prompt': 'open chat 18', 'cron_expression': '0 9 * * *', 'initiation': 'own_followup'}, 0),
        ('mcp__claude-code-remote__send_later', {'message': 'open chat 18', 'delay_minutes': 60}, 0),
        ('Bash', {'command': 'echo create_new_session_on_fire=true'}, 0),
    ]
    bad = [f'{t} {i.get("name", "")}' for t, i, r in cases
           if bool(decide({'tool_name': t, 'tool_input': i, 'session_id': 'test'})) != bool(r)]
    if open(LOG).read().count('\trefused\t') != 1:
        bad.append('log')
    print('triggerguard test: ' + ('OK, 5 cases' if not bad else 'FAILED: ' + '; '.join(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(test() if sys.argv[1:] == ['test'] else main())
