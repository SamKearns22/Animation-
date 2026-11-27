#!/usr/bin/env python3
"""Chain guard: every chat in the chain runs on the model its handover names (cost-spike fix 6, Sam's Y, 27 Nov).

Why (Sam's weekly spike report, 27 Nov, point 4): the Brexit animatic chat was set up on Sonnet and switched to Opus
partway, then ran 3 hours and restarted 5 times on Opus. The rule ("a chat on the wrong model for its next stage opens
one on the right model, never carries on") had no check that runs during a chat: modelguard.py refuses only routine
commands, so the discussion and the restarts went on unseen; and create_session could be called with no model,
leaving the new chat on whatever the parent ran.

MAP
  family() ...... a model id -> 'opus', 'sonnet', 'haiku', 'fable' or ''.
  expect() ...... `chainguard.py expect MODEL` (handover.py start calls it from the film notes' Next line): this chat
                  should run on MODEL. Kept in ~/.claude/chainguard/CHAT.
  decide() ...... the hook. PreToolUse on create_session: refused without an explicit `model` (the handover's).
                  PostToolUse on every tool: when this chat's newest reply came from another family than expected
                  (at start, or switched partway), one line: stop, open the right chat. Said again only if the model
                  changes again. "Override" in Sam's latest message skips both (logged).
  test() ........ kittest chain_model_lock: the 27 Nov animatic chat's switch trips it; a right-model chat does not.

    python3 .claude/hooks/chainguard.py test
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.expanduser('~/.claude/chainguard')
LOG = os.path.join(ROOT, 'notes', 'logs', 'chainguard.log')
CREATE = 'create_session'

SAY_CREATE = ("CHAIN GUARD: create_session needs the model passed explicitly (`model`: the one the handover's Next "
              "line names, e.g. \"sonnet\" for an animatic, \"opus\" for a fix), and the effort for Opus. Without it the "
              "new chat runs on whatever this one runs on (the 27 Nov animatic chat ended up on Opus). Call it again "
              "with model set.")
SAY_SWITCH = ("CHAIN GUARD: this chat was handed over for {want} but is now running on {got}{how}. Stop here: finish "
              "only a step already half done (a commit, a push), then open the {want} chat with create_session "
              "(model \"{want}\", the project attached, the same handover) and do no more work in this one "
              "(CLAUDE.md, Models and chats). Sam's word 'override' skips this.")


def family(model):
    m = re.search(r'opus|sonnet|haiku|fable|mythos', str(model or ''), re.I)
    return m.group(0).lower().replace('mythos', 'fable') if m else ''


def _chat(transcript):
    return os.path.basename(transcript or 'chat').split('.')[0]


def expect(model, transcript, state=STATE):
    os.makedirs(state, exist_ok=True)
    st = {'want': family(model), 'said': ''}
    json.dump(st, open(os.path.join(state, _chat(transcript) + '.json'), 'w'))
    return st['want']


def _served(transcript):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import modelguard
    return modelguard.served_model(transcript)


def _override(what, inp):
    try:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        return __import__('override').skip(what, inp.get('transcript_path'), sys.stderr)
    except Exception:
        return False


def _log(kind, detail, log):
    try:
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, 'a', encoding='utf-8') as f:
            f.write('\t'.join([datetime.now(timezone.utc).isoformat(timespec='minutes'),
                               os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '')[-8:] or 'local', kind, detail]) + '\n')
    except OSError:
        pass


def decide(inp, state=STATE, log=LOG, served=None):
    name = str(inp.get('tool_name', ''))
    tin = inp.get('tool_input') or {}
    if inp.get('hook_event_name', 'PreToolUse') == 'PreToolUse':
        if not name.endswith(CREATE) or str(tin.get('model') or '').strip():
            return None
        if _override('chain guard (create_session without a model)', inp):
            _log('override', 'create_session without model', log)
            return None
        _log('refused', 'create_session without model: ' + str(tin.get('title', ''))[:60], log)
        return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
                                       'permissionDecisionReason': SAY_CREATE}}
    sp = os.path.join(state, _chat(inp.get('transcript_path')) + '.json')
    try:
        st = json.load(open(sp))
    except (OSError, ValueError):
        return None
    if not st.get('want'):
        return None
    got_model = served(inp.get('transcript_path')) if served else _served(inp.get('transcript_path'))
    got = family(got_model)
    if got and got == st['want'] and (not st.get('seen') or st.get('said')):
        st.update(seen=True, said='')               # on the right model (again): a later switch is said anew
        json.dump(st, open(sp, 'w'))
    if not got or got == st['want'] or st.get('said') == got:
        return None
    st['said'] = got
    json.dump(st, open(sp, 'w'))
    if _override('chain guard (wrong model for this stage)', inp):
        _log('override', f"want {st['want']}, got {got}", log)
        return None
    _log('switch', f"want {st['want']}, got {got_model}", log)
    how = ' (switched partway)' if st.get('seen') else ''
    return {'hookSpecificOutput': {'hookEventName': 'PostToolUse',
                                   'additionalContext': SAY_SWITCH.format(want=st['want'], got=got, how=how)}}


def main(argv):
    if argv[:1] == ['test']:
        return test()
    if argv[:1] == ['expect']:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        import handover
        print('chainguard: this chat should run on ' + (expect(argv[1], handover.this_record()) or 'any model'))
        return 0
    try:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        __import__('hookran').ran('chainguard.py')
    except Exception:
        pass
    try:
        out = decide(json.load(sys.stdin))
    except Exception:
        return 0                                     # never break a chat over the guard
    if out:
        print(json.dumps(out))
    return 0


def test():
    """The fault, saved as an example: the 27 Nov Brexit animatic chat (Sam's spike report, point 4) was handed over
    for Sonnet and ran on Opus after a switch partway; and a create_session with no model."""
    import tempfile
    d = tempfile.mkdtemp()
    st, log = os.path.join(d, 'st'), os.path.join(d, 'log')
    bad = []
    C = 'mcp__claude-code-remote__create_session'
    if not decide({'tool_name': C, 'tool_input': {'prompt': 'animatic', 'title': 'chat 37'}}, st, log):
        bad.append('create_session without a model was allowed')
    if decide({'tool_name': C, 'tool_input': {'prompt': 'animatic', 'model': 'sonnet'}}, st, log):
        bad.append('create_session with a model was refused')
    if decide({'tool_name': 'Bash', 'tool_input': {'command': 'echo create_session'}}, st, log):
        bad.append('a Bash command was refused')
    tr = os.path.join(d, 'animatic.jsonl')
    expect('claude-sonnet-5-5', tr, st)
    served = {'m': 'claude-sonnet-5-5'}
    post = lambda: decide({'hook_event_name': 'PostToolUse', 'tool_name': 'Bash', 'transcript_path': tr}, st, log,
                          served=lambda _t: served['m'])
    if post():
        bad.append('a chat on its handover model was told to stop')
    served['m'] = 'claude-opus-5-5'                 # switched partway, as on 27 Nov
    first, again = post(), post()
    if not first or 'running on opus (switched partway)' not in json.dumps(first) or again:
        bad.append(f'switch to Opus: first {first}, repeated {again}')
    served['m'] = 'claude-sonnet-5-5'
    if post():
        bad.append('back on Sonnet but still told')
    expect('', os.path.join(d, 'free.jsonl'), st)  # no model named: never speaks
    if decide({'hook_event_name': 'PostToolUse', 'tool_name': 'Bash', 'transcript_path': os.path.join(d, 'free.jsonl')},
              st, log, served=lambda _t: 'claude-opus-5-5'):
        bad.append('spoke with no model named')
    print('chainguard test: ' + ('OK' if not bad else 'FAILED: ' + '; '.join(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
