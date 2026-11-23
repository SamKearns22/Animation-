# the other account's order: HIPS UP first (pulling on the door top), then the RIGHT (window-side) knee onto its
# rear spot, then the LEFT knee comes up over the cushion's front edge onto its front spot. The legs never cross.
import numpy as np
V = lambda *a: np.array(a, float)
def patch(M):
    old = M._key
    def k(name):
        d = old(name)
        if name in ('B1', 'B1b', 'B2'):
            off = M._rel_hand('K1', 'R', d['hand']['R'])[0] + V(0, 0, 0.06)   # the gun rides at his chest
            d['hand'] = dict(d['hand']); d['hand']['R'] = ('rel', off, d['hand']['R'][1])
        if name == 'B1':      # hips lifting off the seat, leaning forward and turning to the door; feet on the floor
            d.update(pelvis=V(0.46, 0.0, -0.02), p_up=V(0.2, 1, 0.1), p_fwd=V(0.4, 0, 1), c_up=V(0.35, 1, 0.25),
                     c_fwd=V(0.5, 0, 1), h_fwd=V(0.6, -0.2, 1), lift=0.10, leg_ik=1.0,
                     knee={'L': V(0.33, 0.62, 0.40), 'R': V(0.62, 0.62, 0.36)},
                     ankle={'L': V(0.33, 0.18, 0.44), 'R': V(0.62, 0.18, 0.42)})
        if name == 'B1b':     # hips up, turned to the door, ducked; RIGHT knee down onto its rear spot, right shin
            #                   back across the cushion; LEFT foot still on the floor in front
            d.update(pelvis=V(0.52, 0.0, 0.0), p_up=V(0.35, 1, 0), p_fwd=V(1, 0, 0.35), c_up=V(0.8, 1, 0.1),
                     c_fwd=V(1, 0, 0.2), h_fwd=V(1, -0.4, 0.2), lift=0.24, leg_ik=1.0,
                     knee={'L': V(0.52, 0.60, 0.46), 'R': V(0.62, 0.40, -0.12)},
                     ankle={'L': V(0.46, 0.18, 0.44), 'R': V(0.24, 0.70, -0.16)})
        if name == 'B2':      # on both knees: the LEFT knee has come up over the cushion's front edge
            d.update(pelvis=V(0.50, 0.0, 0.02), c_up=V(0.9, 1, 0.05), h_fwd=V(1, -0.4, 0.05),
                     ankle={'L': V(0.26, 0.74, 0.20), 'R': V(0.18, M.ANKLE_Y, -0.16)})
        return d
    M._key = k
