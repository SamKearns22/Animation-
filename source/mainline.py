#!/usr/bin/env python3
"""mainline: put a few bookkeeping files straight onto the main line, never the chat's own work (startup-fixes,
change 1, Sam's Y 16 Nov).

Why: the Stop hook's cost rows went to each chat's own branch (or claude/chat-XXXX when detached) and were mostly
never merged: 7 of 9 checked chats were missing from the films' totals, and those branches filled the branch list
every chat reads at start. Now each update is its own commit on top of the newest main line, holding only its files.

MAP
  to_main() ...... fetch the main line; for each file, new text = fn(text on the main line now); a commit with only
                   those files, its parent the main line's tip (a private index: the chat's files, index and HEAD are
                   never touched); push; on refusal (another chat pushed first) fetch and redo, up to 3 tries
  config() ....... registers the ledger merge driver (`ledger.py mergefile`, .gitattributes) in this copy, so the
                   chat's own commits of the same files merge with the main line's by row, never as a clash
"""
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = 'claude/create-claude-md-oe8z4g'


def _git(root, *a, env=None, inp=None):
    return subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True, timeout=60,
                          env=env, input=inp)


def to_main(updates, msg, root=None, remote='origin', branch=MAIN, tries=3):
    """updates: {path relative to the repo: fn(old text or None) -> new text (None: leave it)}.
    Returns 'pushed', 'same' (nothing to change) or None (could not push after the tries)."""
    import tempfile
    root = root or ROOT
    for i in range(tries):
        if i:
            time.sleep(2 * i)
        if _git(root, 'fetch', '-q', remote, f'+refs/heads/{branch}:refs/remotes/{remote}/{branch}').returncode:
            continue
        base = _git(root, 'rev-parse', f'refs/remotes/{remote}/{branch}').stdout.strip()
        fd, idx = tempfile.mkstemp(prefix='mainline-idx-')
        os.close(fd)
        os.unlink(idx)
        env = dict(os.environ, GIT_INDEX_FILE=idx)
        try:
            _git(root, 'read-tree', base, env=env)
            changed = False
            for path, fn in updates.items():
                r = _git(root, 'show', f'{base}:{path}')
                old = r.stdout if r.returncode == 0 else None
                new = fn(old)
                if new is None or new == old:
                    continue
                blob = _git(root, 'hash-object', '-w', '--stdin', inp=new).stdout.strip()
                _git(root, 'update-index', '--add', '--cacheinfo', f'100644,{blob},{path}', env=env)
                changed = True
            if not changed:
                return 'same'
            tree = _git(root, 'write-tree', env=env).stdout.strip()
            c = _git(root, 'commit-tree', tree, '-p', base, '-m', msg).stdout.strip()
        finally:
            if os.path.exists(idx):
                os.unlink(idx)
        if c and _git(root, 'push', '-q', remote, f'{c}:refs/heads/{branch}').returncode == 0:
            _git(root, 'update-ref', f'refs/remotes/{remote}/{branch}', c)
            return 'pushed'
    return None


def config(root=None):
    """The ledger merge driver, for this copy (git keeps drivers out of the repo; .gitattributes names it)."""
    root = root or ROOT
    want = f'python3 "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.py")}" mergefile %O %A %B %P'
    if _git(root, 'config', '--get', 'merge.ledger.driver').stdout.strip() != want:
        _git(root, 'config', 'merge.ledger.name', 'ledger rows: union by chat')
        _git(root, 'config', 'merge.ledger.driver', want)
