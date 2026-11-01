"""Patriots 4: the world drawn once, in metres (guides/film-quality-rules.md, rule 1). Every shot reads from it.

x east, z north, y up; facings in degrees (0 = north, 90 = east). The origin is the centre of the round winner's table.
Seen from above it is a clock face (Sam, 1 Nov): Claudia at 12 with the arch the banished leave by behind her, the
Patriot at 2, Romesh at 7 with the Round Table hall far behind him, Bash at 9. The camera circles the coin pile, always across
it from the person it shows, so everyone faces it (rule 38) and the Patriot's quarter is never seen until the reveal.

    python3 source/plan.py patriots4 sketch OUT.jpg     the plan from above
    python3 source/plan.py patriots4 check              its faults
"""
import math

R = 0.62                       # from the table's centre to where each person stands (the table is 0.37 m; clear of it)
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
    'to the round table': dict(wall=('z', -3.2), span=(-3.0, 3.0), sill=0.0, head=4.2),
}
LOOKS = {
    "winner's room": dict(floor=(70, 50, 36), wall=(92, 58, 34), ceiling=(40, 28, 22), thing=(120, 74, 44)),
    'round table hall': dict(floor=(64, 46, 34), wall=(84, 54, 34), ceiling=(36, 26, 20), thing=(150, 110, 60)),
    'arch passage': dict(floor=(52, 38, 28), wall=(78, 50, 30), ceiling=(30, 22, 18)),
}
THINGS = {
    "winner's table": dict(at=(0.0, 0.0), size=(0.9, 0.9, TABLE_H), facing=0,
                           why='round, light rim, cream inlaid ring, on a pedestal of turned legs (refs 01, 12); half size, then 25% less twice (Sam, 1 Nov); '
                               '0.9 m is its size as drawn beside the people (the old 0.37 was worked out wrongly; the wide view, patriots4_wide.TABLE_R, draws it from here)'),
    'coin pile': dict(at=(0.0, 0.0), size=(0.66, 0.66, 0.3), facing=0, y=TABLE_H, solid=False, on="winner's table",
                      why='large gold coins in about 7 tiers, more scattered round the base (ref 01)'),
    'fire bowl': dict(at=(-2.0, -1.6), size=(0.8, 0.8, 0.9), facing=0,
                      why='iron bowl of fire on a stand (refs 03, 09)'),
    'round table': dict(at=(0.0, -6.0), size=(4.5, 4.5, 0.78), facing=0,   # at z -6: clear of the opening (the sizes were read as width, height,
                                                                      # depth before; set right 1 Nov, it poked into the winner's room)
                        why="The Traitors Round Table (source/traitors.py round_table) behind Romesh, half as far as first built (Sam, 1 Nov); one space with the winner's room"),
}
PEOPLE = {
    'claudia': dict(at=clock(12), facing=facing_in(12), who='claudia'),
    'patriot': dict(at=clock(3), facing=facing_in(3), who='patriot'),     # Sam, 1 Nov: the Patriot at 3, Romesh at 6
    'romesh': dict(at=clock(6), facing=facing_in(6), who='romesh'),
    'bash': dict(at=clock(9), facing=facing_in(9), who='bash'),
}


def _look(hour, y=1.38):
    x, z = clock(hour)
    return (x, y, z)


CAM_Y = 1.52                   # Sam, 1 Nov (to hold 15% of a week): the "swivel" is the camera TURNING on the spot
                               # over the coin pile (the room painted once all round, patriots4_room.py), not circling


def pan(hour, focal=1146, y=1.40, why=''):
    """A camera at the table's centre, turned to look at whoever stands at this hour (it pans between them)."""
    return dict(pos=(0.0, CAM_Y, 0.0), look=_look(hour, y), focal=focal, why=why)


CAMS = {   # focal in pixels for 1080 x 1920 (1146: 20 px a degree, patriots4_room.K)
    'claudia': pan(12, why='over the coins at Claudia (the Patriot 60 deg off frame)'),
    'bash': pan(9, why='panned round to Bash'),
    'romesh': pan(6, why='Romesh; the Round Table end behind him'),
    'patriot': pan(3, why='the reveal: a cut to Claudia\'s left'),
    'claudia close': pan(12, 2000, 1.55, why='the stares, closer'),
    'bash close': pan(9, 2000, 1.55, why='staring and blinking'),
    'patriot close': pan(3, 2000, 1.55, why='eyes wide, sliding to Romesh'),
    'his view': dict(pos=(0.71, 1.62, 0.71), look=(-0.62 * 0.5, 1.2, -0.62 * 0.5), focal=820,
                     why="across the table from 1:30 (patriots4_wide.CAM_AT; Sam, 1 Nov note 28): Romesh at 6 left, "
                         "Bash at 9 right, both standing behind the table; the Patriot's shoulder bottom left (shot 9)"),
}
CAMS.update({'claudia 2': CAMS['claudia'], 'claudia close 2': CAMS['claudia close'], 'patriot 2': CAMS['patriot'],
             'traitors': dict(CAMS['patriot'], why="the Patriot points at both; Bash's and Romesh's backs in the corners"),
             'reaction': dict(CAMS['his view'], why="their reaction: just Romesh and Bash (Sam, 1 Nov)")})
GROUPS = {}
FRAMING = {   # rule 10: the Hook Text over the arch above Claudia; each key beat with its minimum hold
    'claudia': dict(hook='the arch and lattice above Claudia, top third', beats=[('the question', 1.0)]),
    'bash': dict(beats=[('hands meet at his chest, eyes close', 1.0)]),
    'romesh': dict(beats=[('sincere, hands on the table', 1.0)]),
    'patriot': dict(beats=[('eyes widen', 0.8), ('Errrr held', 2.0)]),
    'his view': dict(beats=[('their eyes slide to each other', 1.2)]),
    'reaction': dict(beats=[('eyes to each other, held', 1.0)]),
}
SHOT_MARKS = {   # rule 38: who is on screen in each shot, by mark (plan.py checks each faces the lens)
    'claudia': ['claudia'], 'bash': ['bash'], 'romesh': ['romesh'], 'patriot': ['patriot'],
    'claudia close': ['claudia'], 'bash close': ['bash'], 'patriot close': ['patriot'],
    'his view': ['romesh', 'bash'],   # the Patriot's back at the frame edge
    'reaction': ['romesh', 'bash'],
}
