import numpy as np
V = lambda *a: np.array(a, float)
def patch(M):
    old = M._key
    def k(name):
        d = old(name)
        if name == 'B1':      # seated, turning to the door; left knee lifting, right leg swinging out toward the door
            d.update(p_fwd=V(0.35, 0, 1), c_fwd=V(0.5, 0, 1),
                     knee={'L': V(0.50, 0.85, 0.32), 'R': V(0.78, 0.60, 0.20)},
                     ankle={'L': V(0.36, 0.45, 0.50), 'R': V(0.80, 0.18, 0.35)})
        if name == 'B1b':     # still seated, turned: LEFT leg folded up on the cushion front (knee by the door),
            #                   RIGHT leg hanging down beside the seat by the door
            d.update(p_fwd=V(0.8, 0, 0.55), c_fwd=V(0.85, 0, 0.4),
                     knee={'L': V(0.64, 0.53, 0.20), 'R': V(0.84, 0.58, 0.0)},
                     ankle={'L': V(0.24, 0.64, 0.22), 'R': V(0.82, 0.18, 0.06)})
        if name == 'B2':      # up on the LEFT knee (pulling on the door top), right knee coming round the door side
            d.update(pelvis=V(0.50, 0.0, 0.02),
                     knee={'L': M.KNEES['L'], 'R': V(0.72, 0.525, -0.04)},
                     ankle={'L': V(0.20, M.ANKLE_Y, 0.18), 'R': V(0.42, 0.72, -0.14)})
        return d
    M._key = k
