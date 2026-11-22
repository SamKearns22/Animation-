# p6 + B1c (0.78 s; 7.576 s sitting down): the LEFT foot lifted out of the footwell, knee high, BEFORE the knee goes
# down onto the cushion (it came up through the seat front and the floor); gun hand tucked in (arm was in the door)
import numpy as np
V = lambda *a: np.array(a, float)
def patch(M):
    old = M._key
    M.BREAKDOWNS[:] = sorted(M.BREAKDOWNS + [(0.78, 'B1c'), (7.576, 'B1c')])
    def k(name):
        if name == 'B1c':
            d = k('B1b')
            d.update(knee={'L': V(0.46, 0.84, 0.40), 'R': V(0.62, 0.40, -0.12)},
                     ankle={'L': V(0.40, 0.56, 0.44), 'R': V(0.32, 0.71, -0.18)}, lift=0.38)
            return d
        d = old(name)
        if name in ('B1', 'B1b', 'B2'):
            d['hand'] = dict(d['hand']); d['hand']['R'] = ('rel', V(-0.15, 0.04, 0.24), d['hand']['R'][1])
        if name == 'B1':      # hips lifting, turning and leaning toward the door; right foot lifting off the floor
            d.update(pelvis=V(0.47, 0.0, -0.02), p_up=V(0.25, 1, 0.05), p_fwd=V(0.5, 0, 1), c_up=V(0.45, 1, 0.12),
                     c_fwd=V(0.7, 0, 1), h_fwd=V(0.8, -0.2, 1), lift=0.14, leg_ik=1.0,
                     knee={'L': V(0.36, 0.62, 0.40), 'R': V(0.66, 0.70, 0.32)},
                     ankle={'L': V(0.38, 0.20, 0.42), 'R': V(0.64, 0.40, 0.42)})
        if name == 'B1b':     # up on his left leg, ducked to the window; right knee down on its rear spot
            d.update(pelvis=V(0.54, 0.0, 0.0), p_up=V(0.45, 1, 0), p_fwd=V(1, 0, 0.2), c_up=V(1.1, 1, 0.05),
                     c_fwd=V(1, 0, -0.05), h_fwd=V(1, -0.2, -0.1), lift=0.32, leg_ik=1.0,
                     knee={'L': V(0.50, 0.62, 0.42), 'R': V(0.62, 0.40, -0.12)},
                     ankle={'L': V(0.48, 0.20, 0.40), 'R': V(0.42, 0.72, -0.20)})
        if name == 'B2':      # on both knees: the LEFT knee has come down over the cushion's front edge
            d.update(pelvis=V(0.52, 0.0, 0.02), c_up=V(0.9, 1, 0.05), h_fwd=V(1, -0.3, 0.0),
                     ankle={'L': V(0.26, 0.74, 0.20), 'R': V(0.18, M.ANKLE_Y, -0.16)})
        return d
    M._key = k
