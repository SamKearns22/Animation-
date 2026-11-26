#!/usr/bin/env python3
"""MAP (startup fixes change 4, Sam's Y, 16 Nov): no CLAUDE.md sentence is ever lost.

Text may leave CLAUDE.md only word for word: to the rulebook (guides/film-quality-rules.md) or a pack
(guides/job-packs.md). A dated tag such as "(Sam, 13 Nov)" may leave its sentence only if the rulebook's
"Dates moved from CLAUDE.md" table holds a row: the sentence's first words | the tag, word for word.

  split(text) ........ CLAUDE.md -> sentences (bullets, headers, '. ' ends; whitespace and ** ignored)
  lost(old, files) ... the old sentences found in none of the new files (after moved tags are taken out)
  tag_rows(text) ..... the rulebook's moved-tag rows: [(first words, tag)]
  faults() ........... every CLAUDE.md change since this check began (each commit, then the working copy)

  python3 source/sentences.py check            the faults; exit 1 if any (handover.py end runs it too)
  python3 source/sentences.py lost OLD.md      one old CLAUDE.md against today's files

A later rewording (only with Sam's Y on its own proposal) must add its own allowance here: MERGED_23NOV is the first.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['CLAUDE.md', 'guides/film-quality-rules.md', 'guides/job-packs.md']
TAGS_HEADER = 'Dates moved from CLAUDE.md'


def norm(s):
    s = s.replace('**', '')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([.,;:)])', r'\1', s)
    s = re.sub(r'[;,]\s*\)', ')', s)
    s = re.sub(r'\(\s*\)', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def _blocks(text):
    out, cur = [], []
    for ln in text.splitlines():
        start = re.match(r'\s*(#+\s|-\s|\|)', ln) or not ln.strip()
        if start and cur:
            out.append(' '.join(cur)); cur = []
        head = re.match(r'\s*#+\s', ln)
        ln = re.sub(r'^\s*(#+|-)\s+', '', ln)
        if ln.strip():
            cur.append(ln.strip())
        if head and cur:                    # a header is a block of its own
            out.append(' '.join(cur)); cur = []
    if cur:
        out.append(' '.join(cur))
    return out


def split(text):
    out = []
    for b in _blocks(text):
        for s in re.sub(r'([.!?](?:\*\*)?)\s+', r'\1\n', b).split('\n'):
            s = norm(s)
            if len(s) > 2:
                out.append(s)
    return out


def corpus(text):
    return ' ' + ' '.join(norm(b) for b in _blocks(text)) + ' '


def tag_rows(rulebook):
    rows, on = [], False
    for ln in rulebook.splitlines():
        if ln.startswith('#'):
            on = TAGS_HEADER in ln
        elif on and ln.startswith('|') and not ln.startswith('|---'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[1] and not cells[0].startswith('CLAUDE.md rule'):
                rows.append((norm(cells[0]), norm(cells[1])))
    return rows


SAM_REWORDED = {   # sentences Sam himself rewrote (his words now stand in their place): never "lost"
    'The chain stops only at the budget stop (rule 24)': 'Sam\'s answer 2 on the check audit (26 Nov, notes/check-audit.md Q5): the budget stop is deleted, so the chain line drops it',
    'One question at a time (Sam, 26 Nov, "1.': 'withdrawn: written in by mistake (R8 chat 1 misread Sam\'s "1. Y"); Sam\'s '
                                                  'answer was N (26 Nov): every open decision stays in one message',
    'Y"; this replaces "every open decision in one message" above)': 'the same withdrawn line (Sam: N, 26 Nov)',
    'Every stage aims at three things (Sam, 13 Nov)': 'Statement One (Sam, 22 Nov), top of CLAUDE.md, and "Every stage '
                                                     'aims at Statement One" in "Rules are permanent"',
    'Every stage aims at three things: high quality': 'the same, reworded again by Sam\'s 22 Nov Statement One',
    'Be honest about what I can do (Sam, 21 Nov)': 'Statement Two (Sam, 21 Nov), top of CLAUDE.md',
    # Settled by crowd pool chat 1 (26 Nov): the two 23 Nov rewordings were Sam's (chat 48: Override, his pick; the
    # Locked line out of messages, "it doesn't help me"), their current words stand in CLAUDE.md today; the 26 Nov ones
    # are his pose-test chat 1 words ("No, I don't think we need to run it through the proposal step"; "advise
    # whether you want to run a certain suite of checks"; "It doesn't have to be perfect").
    'Every handover has a "Locked by Sam" line naming the cameras and beats that must not move':
        'the same sentence, now "... It stays in the notes, never in messages to me" (Sam, 23 Nov)',
    '"Just go"': '"Just go" (or any override) skips waiting for my yes ... (Sam\'s Override pick, 23 Nov)',
    'No check sheet before an animatic unless I ask':
        '"No check sheet before an animatic unless I ask: render the animatic and send it" (checks advised, Sam 26 Nov)',
    'The proposal route: "Every change to rules': 'The proposal route, on request only (Sam, 26 Nov)',
    'The proposal route (Sam, 15 Nov': 'The proposal route, on request only (Sam, 26 Nov)',
    'The guard refuses an unjudged ask': 'The proposal route, on request only: "No automatic guard" (Sam, 26 Nov)',
    'The body check runs only when asked (`BODYCHECK=1`); kit tests at a major film\'s start and end only': 'the same sentence; the film\'s start and end now named (Sam, 26 Nov: "The '
                                        'beginning of the film is when I give you the screenplay and title. The end of '
                                        'the film is when I ask for any lessons on the film")',
    'Changes made without asking are listed and judged in the end-of-film review':
        'The proposal route, on request only (Sam, 26 Nov): run when Sam asks',
    'Choose views the drawing can carry.': 'Seeing like Sam 4, now bold-split by Sam\'s 21 Nov wording',
}


MERGED_23NOV = {   # CLAUDE.md trim to under 2,800 words (Sam: "Override", 23 Nov): repeats merged, each rule kept once
    'Choose views the drawing can carry (for a NEW shot': 'same item, "(new shots only; see Fix the drawing...)"',
    "I don't know how to code.": 'Plain words, always ("I can\'t follow code names, file names or jargon")',
    'Explain in plain English': 'Plain words, always (any technical word is explained where it appears)',
    'No code names; any technical word is explained': 'Plain words, always',
    'No code names or file internals': 'Plain words, always, and the handover\'s "For Claude" line for code names',
    "The handover's 3 lines go at the bottom": 'Fresh chats and the handover: "The 3 lines at the bottom of every message"',
    'New rules and lessons are proposed first': 'The proposal route, and "I want a rule"',
    'Every stage aims at Statement One': 'Statement One, top of CLAUDE.md; the rest kept as "Something new? ..."',
    'Every idea for cost or speed makes new things better': 'Statement One ("Cost comes down only by working smarter")',
    "Before every handover, search the film's notes for rule requests": 'the handover\'s "Open rule requests (searched '
                                                                        'for in the film\'s notes)"',
    'The Animation- project is always attached': 'same sentence, now also "a chat without it adds it ... says so"',
    'No chat ends under about 40 steps': 'same sentence; "routine stages always go on Sonnet" is Models by stage',
    'A message never says "start a new chat"': 'The 3 lines at the bottom (never a request to start a chat or type)',
    'A fresh chat for every round and every cost warning': 'same sentence; "change model only by a new chat" is the '
                                                            'wrong-model rule in Models and chats',
    'The handover is the film\'s ONE': 'same sentence; Next now carries "model and effort ... one line why"',
    'The 3 lines at the bottom say': 'The 3 lines at the bottom of every message to me',
    "Every handover names the next chat's model AND effort": 'the handover\'s Next (model and effort ...)',
    'Every chat starts with the Animation- project selected': 'The Animation- project is always attached (... adds it)',
}


def lost(old, files):
    """old: the old CLAUDE.md text; files: {path: new text}. Returns the old sentences not found word for word
    (a sentence Sam himself rewrote, SAM_REWORDED, is not lost: his new words stand in its place)."""
    body = ''.join(corpus(t) for t in files.values())
    rows = tag_rows(files.get('guides/film-quality-rules.md', ''))
    miss = []
    for s in split(old):
        if s in body or any(s.startswith(k) for k in {**SAM_REWORDED, **MERGED_23NOV}):
            continue
        t = s
        for words, tag in rows:
            if words in t and tag in t:
                t = norm(t.replace(tag, ''))
        if t == s or t not in body:
            miss.append(s)
    return miss


def _git(*a):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _at(rev):
    return {f: _git('show', f'{rev}:{f}') or '' for f in FILES}


def faults():
    out = []
    since = (_git('log', '--format=%H', '--diff-filter=A', '-1', '--', 'source/sentences.py') or '').strip()
    revs = (_git('log', '--format=%H', f'{since}..HEAD', '--', 'CLAUDE.md') or '').split() if since else []
    for c in reversed(revs):
        old = _git('show', f'{c}^:CLAUDE.md')
        if old is None:           # shallow copy: the parent is not here; GitHub's copy was checked when it was made
            continue
        out += [f'SENTENCE lost from CLAUDE.md in {c[:8]}: "{s[:110]}"' for s in lost(old, _at(c))]
    head = _git('show', 'HEAD:CLAUDE.md')
    if head is not None:
        now = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in FILES}
        out += [f'SENTENCE lost from CLAUDE.md (not yet saved): "{s[:110]}"' for s in lost(head, now)]
    return [f + ' -> put it back, or move it word for word to the rulebook or a pack' for f in out]


def main(argv):
    if argv[:1] == ['check']:
        f = faults()
        for x in f:
            print(x)
        print('Checks: sentence check: ' + (f'{len(f)} CLAUDE.md sentences lost' if f else 'no CLAUDE.md sentence lost'))
        return 1 if f else 0
    if argv[:1] == ['lost'] and len(argv) > 1:
        now = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in FILES}
        m = lost(open(argv[1], encoding='utf-8').read(), now)
        for s in m:
            print('LOST:', s)
        print(f'{len(m)} lost')
        return 1 if m else 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
