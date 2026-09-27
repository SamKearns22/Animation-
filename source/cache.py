"""Slow things (sculpted grids, bent bodies, hair) are kept on disk, keyed by the code and numbers they are
made from, so each is only ever made once. Set SCENE_CACHE to choose the folder."""
import hashlib
import inspect
import os
import pickle
import tempfile

CACHE_DIR = os.environ.get('SCENE_CACHE', os.path.join(tempfile.gettempdir(), 'mother_scene_cache'))


def key_of(deps, args=()):
    h = hashlib.sha1()
    for d in deps:
        h.update((inspect.getsource(d) if callable(d) else repr(d)).encode())
    h.update(repr(args).encode())
    return h.hexdigest()[:12]


def cached(name, fn, deps, *args):
    path = os.path.join(CACHE_DIR, f'{name}_{key_of(deps, args)}.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    res = fn(*args)
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = path + '.tmp%d' % os.getpid()
    with open(tmp, 'wb') as f:
        pickle.dump(res, f, protocol=4)
    os.replace(tmp, path)
    return res
