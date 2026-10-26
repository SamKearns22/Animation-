"""Netan-Yahoo! the world in metres (rule 1): one source for the composition sheet and the film (`PLAN = 'netan_yahoo_plan'`).

Studio axes: x east = screen right, z north = away from the cameras; facing in plan degrees (0 = north, 180 = towards
the cameras). Sam's horseshoe sketch (26 Oct, `references/netan-yahoo/layout-sketch.jpg`) round the floor disc, open
to the audience; Maul and Netanyahu swapped (Sam, 26 Oct).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import newsdesk_set as NS        # noqa: E402
import newsdesk_props as NP      # noqa: E402

DC = NS.DISC                     # the floor disc's centre (0, 1.2)
RING = 1.05                      # each person's distance from the disc's centre. Was 1.15: the chairs then cleared the
                                 # desk by 0.06 m and Netanyahu's looked to clip it (Sam, 26 Oct, "sloppy"). At 1.05 every
                                 # chair clears the desk by 0.15 m (the plan check demands 0.1 m: CHAIR_CLEAR)
ANGLES = {'presenter': 169.2, 'maul': 0.0, 'netanyahu': 69.0}   # degrees from east round the disc (Sam's sketch)
CHAIR_BACK = 0.6                 # each chair's centre behind its person, outwards from the disc's centre
CHAIR_R = NP.RAIL_R + 0.035      # the round chair's reach from its centre: rail centre line plus half its widest part
CHAIR_CLEAR = 0.1                # Sam (26 Oct): every chair at least 0.1 m clear of the desk
TALK_TO = (0.0, -0.5)            # every chair faces this point: angled to each other, open to the audience (Sam)


def spot(who, r=RING):
    a = math.radians(ANGLES[who])
    return (round(DC[0] + r * math.cos(a), 3), round(DC[1] + r * math.sin(a), 3))


def chair_of(p):
    """(x, z, facing) of the chair behind the person standing at p."""
    dx, dz = p[0] - DC[0], p[1] - DC[1]
    n = math.hypot(dx, dz) or 1.0
    cx, cz = p[0] + dx / n * CHAIR_BACK, p[1] + dz / n * CHAIR_BACK
    return (round(cx, 3), round(cz, 3), round(math.degrees(math.atan2(TALK_TO[0] - cx, TALK_TO[1] - cz)), 2))


P, M, N = spot('presenter'), spot('maul'), spot('netanyahu')

CEIL = 4.2
ROOMS = dict(NS.ROOMS)
OPENINGS = {'newsroom glass': dict(NS.OPENINGS['newsroom glass'], to='the newsroom')}
THINGS = dict(NS.desk_plan_things())        # the ring desk as 24 solid blocks (rule 12)
for who, p in (('presenter', P), ('maul', M), ('netanyahu', N)):
    cx, cz, cf = chair_of(p)
    THINGS[f'chair_{who}'] = dict(at=(cx, cz), size=(2 * CHAIR_R, 2 * CHAIR_R, NP.RAIL_TOP), facing=cf, round=True,
                                  clear=CHAIR_CLEAR)
PEOPLE = {'PRESENTER': dict(at=P, facing=180, who='PRESENTER'),     # bodies face each shot's camera; eyes turn
          'MAUL': dict(at=M, facing=180, who='MAUL'),
          'NETANYAHU': dict(at=N, facing=180, who='NETANYAHU')}

# Cameras (pos, look, lens); the shots' framing was agreed on composition sheets v1-v6. Their aims follow the people.
CAMS = {
    's1 start': dict(pos=(2.5, 1.65, -1.5), look=(P[0] - 0.25, 0.95, P[1]), focal=2600),   # both candidates out
    's1 end':   dict(pos=(2.5, 1.65, -1.5), look=(P[0], 1.3, P[1]), focal=5200),
    's2':       dict(pos=(0.2, 1.62, 0.2), look=(N[0], 1.45, N[1]), focal=2900),          # Maul out until shot 3
    's3':       dict(pos=(0.6, 1.62, -0.85), look=(M[0], 1.47, M[1]), focal=2700),        # Netanyahu out
    's4':       dict(pos=(-1.0, 1.6, -3.6), look=(0.3, 1.05, 1.6), focal=1420),           # all three, presenter nearest
    's4 push':  dict(pos=(-1.0, 1.6, -3.6), look=(P[0] - 0.32, 1.0, P[1] + 0.03), focal=2050),   # in on Maul on the chair
    's5':       dict(pos=(0.2, 1.62, 0.2), look=(N[0], 1.45, N[1]), focal=2900),          # as shot 2
}
GROUPS = {}


def cam(name):
    import sets as S
    c = CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


if __name__ == '__main__':
    import plan as PL
    out = PL.faults(type('Film', (), {'PLAN': sys.modules[__name__]}))
    for who, p in (('presenter', P), ('maul', M), ('netanyahu', N)):
        c = THINGS[f'chair_{who}']
        g = min(PL.gap(c, th) for k, th in THINGS.items() if k.startswith('desk'))
        print(f'{who}: stands at {p}; chair at {c["at"]}, {g:.3f} m clear of the desk')
    print('\n'.join(out) or 'plan: no faults')
