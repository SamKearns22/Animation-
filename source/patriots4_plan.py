"""Patriots 4: the world drawn once, in metres (guides/film-quality-rules.md, rule 1). Every shot reads from it.

x east, z north, y up; facings in degrees (0 = north, 90 = east). The origin is the centre of the round winner's table.
Seen from above it is a clock face (Sam, 1 Nov): Claudia at 12 with the arch the banished leave by behind her, the
Patriot at 2, Romesh at 7 with the Round Table hall far behind him, Bash at 9. The camera circles the coin pile, always across
it from the person it shows, so everyone faces it (rule 38) and the Patriot's quarter is never seen until the reveal.

    python3 source/plan.py patriots4 sketch OUT.jpg     the plan from above
    python3 source/plan.py patriots4 check              its faults
"""
import math

R = 0.95                       # from the table's centre to where each person stands
TABLE_H = 0.95                 # they lean on it with both hands (refs 03, 09)
EYE = 1.5


def clock(hour, r=R):
    a = math.radians(hour * 30.0)
    return (round(r * math.sin(a), 3), round(r * math.cos(a), 3))


def facing_in(hour):
    return (hour * 30.0 + 180.0) % 360.0


CEIL = 4.2
ROOMS = {
    "winner's room": (-3.0, -3.2, 3.0, 4.0),
    'round table hall': (-6.0, -14.0, 6.0, -3.2),
    'arch passage': (-1.2, 4.0, 1.2, 7.0),
}
OPENINGS = {
    'the arch': dict(wall=('z', 4.0), span=(-1.1, 1.1), sill=0.0, head=3.2,
                     to='the dark passage the banished leave by: panelled doors, lattice above (refs 01, 03, 12)'),
    'to the round table': dict(wall=('z', -3.2), span=(-2.4, 2.4), sill=0.0, head=3.6),
}
LOOKS = {
    "winner's room": dict(floor=(70, 50, 36), wall=(92, 58, 34), ceiling=(40, 28, 22), thing=(120, 74, 44)),
    'round table hall': dict(floor=(64, 46, 34), wall=(84, 54, 34), ceiling=(36, 26, 20), thing=(150, 110, 60)),
    'arch passage': dict(floor=(52, 38, 28), wall=(78, 50, 30), ceiling=(30, 22, 18)),
}
THINGS = {
    "winner's table": dict(at=(0.0, 0.0), size=(1.3, TABLE_H, 1.3), facing=0,
                           why='round, light rim, cream inlaid ring, on a pedestal of turned legs (refs 01, 12)'),
    'coin pile': dict(at=(0.0, 0.0), size=(0.56, 0.3, 0.56), facing=0, y=TABLE_H, solid=False,
                      why='large gold coins in about 7 tiers, more scattered round the base (ref 01)'),
    'fire bowl': dict(at=(-2.0, -1.6), size=(0.8, 0.9, 0.8), facing=0,
                      why='iron bowl of fire on a stand (refs 03, 09)'),
    'round table': dict(at=(0.0, -9.0), size=(4.5, 0.78, 4.5), facing=0,
                        why='The Traitors Round Table (source/traitors.py round_table), far behind Romesh'),
}
PEOPLE = {
    'claudia': dict(at=clock(12), facing=facing_in(12), who='claudia'),
    'patriot': dict(at=clock(2), facing=facing_in(2), who='patriot'),
    'romesh': dict(at=clock(7), facing=facing_in(7), who='romesh'),
    'bash': dict(at=clock(9), facing=facing_in(9), who='bash'),
}


def _look(hour, y=1.38):
    x, z = clock(hour)
    return (x, y, z)


ORBIT = 0.55                   # the swivel: the camera circles the coin pile this far out, always across it from the
CAM_Y = 1.52                   # person it looks at, so the top tiers sit in the foreground ("over the table at her")


def orbit(hour, focal=1150, y=1.30, why=''):
    x, z = clock(hour + 6, ORBIT)
    return dict(pos=(x, CAM_Y, z), look=_look(hour, y), focal=focal, why=why)


CAMS = {   # focal in pixels for 1080 x 1920
    'claudia': orbit(12, why='across the coins at Claudia (the Patriot 60 deg off frame)'),
    'bash': orbit(9, why='circled round to Bash'),
    'romesh': orbit(7, why='circled on to Romesh; the Round Table far behind him'),
    'patriot': orbit(2, why='the reveal: circled from Claudia to her left'),
    'claudia close': orbit(12, 2100, 1.55, why='the stares, closer'),
    'bash close': orbit(9, 2100, 1.55, why='staring and blinking'),
    'patriot close': orbit(2, 2100, 1.55, why='eyes wide, sliding to Romesh'),
    'his view': dict(pos=(1.75, 1.66, 1.02), look=(-0.62, 1.45, -0.42), focal=1750,
                     why="over the Patriot's shoulder: Romesh and Bash in one frame, their eyes meeting"),
}
GROUPS = {}
FRAMING = {   # rule 10: the Hook Text over the arch above Claudia; each key beat with its minimum hold
    'claudia': dict(hook='the arch and lattice above Claudia, top third', beats=[('the question', 1.0)]),
    'bash': dict(beats=[('hands meet at his chest, eyes close', 1.0)]),
    'romesh': dict(beats=[('sincere, hands on the table', 1.0)]),
    'patriot': dict(beats=[('eyes widen', 0.8), ('Errrr held', 2.0)]),
    'his view': dict(beats=[('their eyes slide to each other', 1.2)]),
}
SHOT_MARKS = {   # rule 38: who is on screen in each shot, by mark (plan.py checks each faces the lens)
    'claudia': ['claudia'], 'bash': ['bash'], 'romesh': ['romesh'], 'patriot': ['patriot'],
    'claudia close': ['claudia'], 'bash close': ['bash'], 'patriot close': ['patriot'],
    'his view': ['romesh', 'bash'],   # the Patriot's back at the frame edge
}
