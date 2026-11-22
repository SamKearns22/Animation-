import numpy as np
V = lambda *a: np.array(a, float)
def patch(M):
    old = M._key
    def k(name):
        d = old(name)
        if name in ('B1', 'B1b', 'B2'):
            off = M._rel_hand('K1', 'R', d['hand']['R'])[0] + V(0, 0, 0.06)   # the gun stays at his chest as he turns
            d['hand'] = dict(d['hand']); d['hand']['R'] = ('rel', off, d['hand']['R'][1])
        if name == 'B1':
            d.update(p_fwd=V(0.35, 0, 1), c_fwd=V(0.5, 0, 1),
                     knee={'L': V(0.50, 0.85, 0.32), 'R': V(0.76, 0.60, 0.20)},
                     ankle={'L': V(0.36, 0.45, 0.50), 'R': V(0.76, 0.18, 0.35)})
        if name == 'B1b':
            d.update(p_fwd=V(0.8, 0, 0.55), c_fwd=V(0.85, 0, 0.4),
                     knee={'L': V(0.64, 0.62, 0.16), 'R': V(0.80, 0.58, -0.02)},
                     ankle={'L': V(0.26, 0.70, 0.20), 'R': V(0.78, 0.18, 0.04)})
        if name == 'B2':
            d.update(pelvis=V(0.50, 0.0, 0.02),
                     knee={'L': M.KNEES['L'], 'R': V(0.74, 0.525, -0.12)},
                     ankle={'L': V(0.20, M.ANKLE_Y, 0.18), 'R': V(0.42, 0.74, -0.16)})
        return d
    M._key = k
