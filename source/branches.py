#!/usr/bin/env python3
"""branches: the few branches holding work the main line lacks, printed at the start of every chat (startup-fixes,
change 2, Sam's Y 16 Nov).

Why: CLAUDE.md asks every chat to merge newer work on other branches. Chats ran `git branch -r` (254 branches,
~3.9k tokens, ~2.0k read a chat) and most were cost-row bookkeeping (change 1 ended that). This copy is shallow
(history from 11 Nov), so comparing files with the main line marks every old branch as different (F2): the scan
uses each branch's OWN commits instead.

MAP
  scan() ......... fetch every branch tip; a branch is listed when the newest version its own commits (merges left
                   out) from the last DAYS days made of some file outside notes/ledger/ (cost rows and Sam's saved
                   messages reach the main line by themselves) never appeared on the main line or in this copy (judged
                   by content: the main line was rewritten once, so old branches share no commits with it); its age
                   and those files
  start .......... the SessionStart hook (.claude/hooks/setup.sh): one line per listed branch, nothing else
  unsettled() .... `handover.py end`: scans again (fresh fetch) and returns the listed branches that are neither
                   merged nor named in the film's notes (the rule: merge or name every branch the start lists)

    python3 source/branches.py start            (the start hook's printout)
    python3 source/branches.py scan [--days 30]
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAIN = 'claude/create-claude-md-oe8z4g'
DAYS = 7
SKIP = ('notes/ledger/',)


def _git(root, *a, timeout=60):
    return subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True, timeout=timeout)


def fetch(root=None, remote='origin', days=DAYS):
    """Every branch tip, and the main line's history back DAYS + 2 days (a shallow copy otherwise knows only its
    last day or so, and older merged work would look missing)."""
    root = root or ROOT
    for i in range(3):
        try:
            if _git(root, 'fetch', '-q', '--prune', f'--shallow-since={days + 2} days ago', remote,
                    f'+refs/heads/*:refs/remotes/{remote}/*', timeout=60).returncode == 0:
                return True
        except subprocess.TimeoutExpired:
            pass
        time.sleep(2 * (i + 1))
    return False


def _blobs(root, *refs):
    """Every file version (blob id) the given history ever held: work whose last version is here has been merged."""
    raw = _git(root, 'log', '--format=', '--raw', '--no-abbrev', '--no-renames', '-m', *refs, timeout=120).stdout
    return {ln.split()[3] for ln in raw.splitlines() if ln.startswith(':')}


def scan(root=None, remote='origin', days=DAYS, now=None):
    """[(branch, age in days, commit count, [files])] for branches with recent work held nowhere here, newest first.
    The main line's history was rewritten at least once (old branches share no commits with it) and this copy is
    shallow, so 'merged' is judged by content: a branch is listed when the last version its own recent commits made
    of some file (outside notes/ledger/) never appeared on the main line or in this copy."""
    root = root or ROOT
    now = now or time.time()
    since = now - days * 86400
    main = f'refs/remotes/{remote}/{MAIN}'
    have = None
    out = []
    refs = _git(root, 'for-each-ref', '--format=%(refname:short) %(committerdate:unix)',
                f'refs/remotes/{remote}/').stdout.split('\n')
    for ln in refs:
        if not ln.strip():
            continue
        ref, when = ln.rsplit(' ', 1)
        name = ref.split('/', 1)[1]
        if name in (MAIN, 'HEAD') or int(when) < since:   # a branch with recent own commits has a recent tip
            continue
        log = _git(root, 'log', '--no-merges', '--no-renames', f'--since={int(since)}', '--format=%x00%ct',
                   '--raw', '--no-abbrev', ref, f'^{main}', '^HEAD').stdout
        last, when_ = {}, {}                              # file -> its newest version from the branch's own work
        for block in log.split('\x00')[1:]:
            lines = [x for x in block.split('\n') if x.strip()]
            t = int(lines[0])
            for r in lines[1:]:
                meta, path = r.split('\t', 1)
                if path.startswith(SKIP) or path in last:
                    continue
                last[path], when_[path] = meta.split()[3], t
        if not last:
            continue
        if have is None:
            have = _blobs(root, main, 'HEAD')
        new = [f for f, blob in last.items() if blob not in have and set(blob) != {'0'}]
        if new:
            newest = max(when_[f] for f in new)
            out.append((name, (now - newest) / 86400, len(new), new))
    return sorted(out, key=lambda b: b[1])


def line(b):
    name, age, n, files = b
    shown = ', '.join(files[:3]) + (f' +{n - 3} more' if n > 3 else '')
    when = f'{age * 24:.0f} h' if age < 1 else f'{age:.0f} d'
    return f'  {name} ({when}): {n} file{"s" * (n != 1)} not on the main line: {shown}'


def unsettled(notes_text, root=None, remote='origin'):
    """Listed branches (fresh scan) neither merged here nor named in the notes: the handover's refusal."""
    fetch(root, remote)
    return [b for b in scan(root, remote) if b[0] not in notes_text]


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    days = int(argv[argv.index('--days') + 1]) if '--days' in argv else DAYS
    if argv[0] == 'start':
        ok = fetch(days=days)
        bs = scan(days=days)
        if not ok:
            print('BRANCHES: could not fetch the branch list; run: python3 source/branches.py scan')
        elif bs:
            print(f'BRANCHES with work not on the main line (last {days} days; merge or name each in the notes):')
            print('\n'.join(line(b) for b in bs))
        else:
            print(f'BRANCHES: none hold work the main line lacks (last {days} days)')
        return 0
    if argv[0] == 'scan':
        fetch(days=days)
        print('\n'.join(line(b) for b in scan(days=days)) or 'none')
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
