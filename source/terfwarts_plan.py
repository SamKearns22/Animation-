"""Terfwarts: the world drawn once, in metres (guides/film-quality-rules.md, rule 1). Every shot reads from it.

x east, z north, y up; facings in degrees (0 = north, 90 = east). Two places that never meet, side by side on one
plan: the Great Hall (x -6..6) and the cloister corridor ending at the shrunk door to the girls' bathroom (x 20..23.5).

    python3 source/plan.py terfwarts sketch OUT.jpg     the plan from above
"""

CEIL = 9.0
HALL = (-6.0, 0.0, 6.0, 30.0)
ROOMS = {
    'great hall': HALL,
    'corridor': (20.0, 0.0, 23.5, 26.0),
    "girls' bathroom": (20.0, 26.0, 23.5, 32.0),
}
DOOR_X = 21.75                 # the shrunk Great Hall door, centred on the corridor's end wall
OPENINGS = {
    'hall window': dict(wall=('z', 30.0), span=(-2.5, 2.5), sill=3.0, head=8.5,
                        to='night sky through leaded glass (refs great-hall-*)'),
    "bathroom door": dict(wall=('z', 26.0), span=(DOOR_X - 0.5, DOOR_X + 0.5), sill=0.0, head=2.1,
                          to="the girls' bathroom (shut: carved oak, Great Hall style, shrunk; refs door-1/2)"),
}
LOOKS = {
    'great hall': dict(floor=(70, 60, 52), wall=(150, 120, 84), ceiling=(30, 26, 34), thing=(110, 70, 40)),
    'corridor': dict(floor=(196, 176, 140), wall=(200, 176, 132), ceiling=(186, 160, 118), thing=(170, 150, 112)),
    "girls' bathroom": dict(floor=(220, 220, 214), wall=(236, 236, 230), ceiling=(200, 200, 196)),
}
THINGS = {
    'staff table': dict(at=(0.0, 27.0), size=(8.0, 0.9, 0.8), facing=0, why='teachers\' table across the top (refs)'),
    'west table': dict(at=(-3.4, 12.0), size=(1.0, 18.0, 0.78), facing=0, why='long house table, candles (refs)'),
    'east table': dict(at=(3.4, 12.0), size=(1.0, 18.0, 0.78), facing=0, why='long house table, candles (refs)'),
    'stool': dict(at=(0.0, 23.5), size=(0.4, 0.4, 0.45), facing=0, why='the sorting stool, short for an 11-year-old'),
    'stone bench': dict(at=(20.25, 12.0), size=(0.45, 20.0, 0.45), facing=0, why='bench along the cloister wall (ref corridor)'),
    'brass plaque': dict(at=(DOOR_X, 25.98), size=(0.34, 0.02, 0.10), facing=180, y=1.55, solid=False,
                         why="GIRLS on the door (Sam, 3 Nov: Q8 yes)"),
}
PEOPLE = {
    'harry hall': dict(at=(0.0, 23.5), facing=180, who='harry', on='stool', why='seated on the stool, facing the hall'),
    'mcg': dict(at=(-0.07, 24.0), facing=180, who='mcg', why='just behind Harry, putting the Hat on (note 6)'),
    'harry': dict(at=(DOOR_X - 0.35, 23.6), facing=0, who='harry', why='at the door, facing Myrtle'),
    'ron': dict(at=(DOOR_X + 0.4, 23.4), facing=0, who='ron', why='a step behind Harry, on his right'),
    'myrtle': dict(at=(DOOR_X, 25.3), facing=180, who='myrtle', why='floating out of the door, 0.3 m up'),
}
_E = 1.45
CAMS = {   # focal in pixels for 1080 x 1920
    'hat close': dict(pos=(0.0, 1.2, 22.45), look=(0.0, 1.2, 23.5), focal=1600,
                      why='opens the film: Harry and the Hat fill the frame (Sam, 3 Nov: no long shots of the hall)'),
    'corridor run': dict(pos=(DOOR_X, 1.3, 25.4), look=(DOOR_X, 1.1, 10.0), focal=1100,
                         why='from the door down the cloister: the boys run at the lens (front on)'),
    'myrtle': dict(pos=(DOOR_X + 0.15, 1.35, 22.0), look=(DOOR_X, 1.3, 26.0), focal=1300,
                   why="over the boys' shoulders at Myrtle and the door"),
    'boys': dict(pos=(DOOR_X + 0.55, 1.45, 25.9), look=(DOOR_X, 1.2, 23.5), focal=1150,
                 why="through Myrtle's back at Harry and Ron (the door's side)"),
}
# the film's shot names (the composition sheet's names kept above for terfwarts_compose.py)
CAMS.update({'hat': CAMS['hat close'], 'hat face': dict(CAMS['hat close'], focal=2720,
                                                        why="Harry's annoyed stare, 1.7x the hat shot (Sam's note 13.1)"), 'run': CAMS['corridor run'], 'door': CAMS['myrtle'],
             'harry close': dict(CAMS['boys'], focal=2990, why="Harry's face from Myrtle's side (2.3x the boys shot)"),
             'myrtle close': dict(CAMS['myrtle'], focal=3200, why="Myrtle's face from the boys' side (2x the door)")})
# rule 38: who each shot holds at their marks (the run is on the move: no mark)
SHOT_MARKS = {'hat': ['harry hall', 'mcg'], 'hat face': ['harry hall'], 'door': ['myrtle', 'harry', 'ron'], 'boys': ['harry', 'ron'],
              'harry close': ['harry'], 'myrtle close': ['myrtle']}
GROUPS = {}                    # no crowd: the hall is only seen behind Harry's close-up (Sam, 3 Nov)
