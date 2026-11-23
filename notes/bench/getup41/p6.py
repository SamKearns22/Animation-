# p4's order, re-shaped: he rises on his LEFT leg (foot in the footwell), chest ducked toward the window as at K2,
# the RIGHT foot lifting up BEFORE it swings back, so the right knee lands only once his hips are high.
import numpy as np
V = lambda *a: np.array(a, float)
def patch(M):
    old = M._key
    def k(name):
        d = old(name)
        if name in ('B1', 'B1b', 'B2'):
            off = M._rel_hand('K1', 'R', d['hand']['R'])[0] + V(0, 0, 0.06)   # the gun rides at his chest
            d['hand'] = dict(d['hand']); d['hand']['R'] = ('rel', off, d['hand']['R'][1])
        if name == 'B1':      # hips lifting, turning and leaning toward the door; right foot lifting off the floor
            d.update(pelvis=V(0.47, 0.0, -0.02), p_up=V(0.25, 1, 0.05), p_fwd=V(0.5, 0, 1), c_up=V(0.45, 1, 0.12),
                     c_fwd=V(0.7, 0, 1), h_fwd=V(0.8, -0.2, 1), lift=0.14, leg_ik=1.0,
                     knee={'L': V(0.36, 0.62, 0.40), 'R': V(0.66, 0.70, 0.32)},
                     ankle={'L': V(0.38, 0.20, 0.42), 'R': V(0.64, 0.40, 0.42)})
        if name == 'B1b':     # up on his left leg, ducked to the window (K2's chest); right knee coming down on its
            #                   rear spot, shin back across the cushion
            d.update(pelvis=V(0.54, 0.0, 0.0), p_up=V(0.45, 1, 0), p_fwd=V(1, 0, 0.2), c_up=V(1.1, 1, 0.05),
                     c_fwd=V(1, 0, -0.05), h_fwd=V(1, -0.2, -0.1), lift=0.32, leg_ik=1.0,
                     knee={'L': V(0.50, 0.62, 0.42), 'R': V(0.62, 0.40, -0.12)},
                     ankle={'L': V(0.48, 0.20, 0.40), 'R': V(0.42, 0.72, -0.20)})
        if name == 'B2':      # on both knees: the LEFT knee has come up over the cushion's front edge
            d.update(pelvis=V(0.52, 0.0, 0.02), c_up=V(0.9, 1, 0.05), h_fwd=V(1, -0.3, 0.0),
                     ankle={'L': V(0.26, 0.74, 0.20), 'R': V(0.18, M.ANKLE_Y, -0.16)})
        return d
    M._key = k
