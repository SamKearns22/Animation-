"""Milburn-look check (Sam 20 Nov): the posted Milburn's frames (from its bookmark) beside the same frames drawn with
today's kit. Run from the repo root: python3 notes/proposals/one-route-kit/measure/milburn_look.py OUT_DIR T [T ...]
argv: OUT_DIR T [T ...]"""
import sys, os
sys.path.insert(0, 'source')
out = sys.argv[1]; ts = [float(x) for x in sys.argv[2:]]
os.makedirs(out, exist_ok=True)
import numpy as np
import freeze, milburn as M
for t in ts:
    a = freeze.film_frame('milburn', t)
    b = M.frame_image(t).convert('RGB')
    if b.size != a.size:
        b = b.resize(a.size)
    A, B = np.asarray(a, np.int16), np.asarray(b, np.int16)
    d = (np.abs(A - B).max(axis=2) > 24)
    a.save(f'{out}/posted-{t}.png'); b.save(f'{out}/kit-{t}.png')
    np.save(f'{out}/diff-{t}.npy', d)
    print(f'{t:6.2f}s shot {M.scene_of(t) if hasattr(M, "scene_of") else ""}: {d.mean() * 100:.2f}% of pixels differ', flush=True)
