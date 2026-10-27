"""Patriots 3: the world drawn once, in metres (guides/film-quality-rules.md, rule 1). Every shot reads from it.

x east (along the slit wall), z north (towards the sea), y up; facings in degrees (0 = north, 90 = east). The origin
is where the Gunner stands at the MG42 (source/patriots3_bunker.py: the slit is 1.9 m wide, its sill 0.99 m up, the
wall 0.7 m thick from z 1.11 to 1.81). The casemate is 4.6 m wide and 3.5 m deep under a 2.4 m concrete ceiling; the
door is in the back wall, behind the gun and to its right, onto a covered concrete passage that runs east to daylight.

    python3 source/plan.py patriots3 sketch OUT.jpg     the plan from above
    python3 source/plan.py patriots3 check              its faults
"""
Z_IN, Z_OUT, SILL, SLIT_TOP = 1.11, 1.81, 0.99, 2.05

CEIL = 2.4
ROOMS = {
    'casemate': (-2.6, -2.4, 2.0, Z_IN),
    'passage': (-1.0, -3.6, 3.4, -2.4),        # covered concrete passage behind the door, open at its east end
}
OPENINGS = {
    'slit': dict(wall=('z', Z_IN), span=(-1.3, 0.62), sill=SILL, head=SLIT_TOP,
                 to='the beach (patriots3_bunker.beach_layer): grey sea to a high horizon, ships, landing craft, '
                    'hedgehogs, smoke'),
    'door': dict(wall=('z', -2.4), span=(0.2, 1.1), sill=0.0, head=1.95),
    'passage end': dict(wall=('x', 3.4), span=(-3.6, -2.4), sill=0.0, head=2.2,
                        to='daylight: the open trench, sandbags, grass and grey sky'),
}
LOOKS = {
    'casemate': dict(floor=(96, 94, 88), wall=(118, 116, 108), ceiling=(92, 90, 84), thing=(120, 100, 70)),
    'passage': dict(floor=(104, 100, 92), wall=(140, 136, 126), ceiling=(112, 108, 100)),
}
THINGS = {   # set dressing (rule 22; my additions, Sam can say no): kept clear of every place where action happens
    'ammo crates': dict(at=(1.55, 0.72), size=(0.62, 0.42, 0.5), facing=0),
    'shelf': dict(at=(1.88, -1.75), size=(0.22, 1.0, 0.04), facing=0, y=1.25),
    'field telephone': dict(at=(1.88, -1.6), size=(0.18, 0.24, 0.16), facing=270, on='shelf'),
    'range card': dict(at=(-0.34, Z_IN - 0.02), size=(0.6, 0.02, 0.28), facing=180, y=2.08, solid=False,
                       why='a card pinned to the wall above the slit (ref bunker-1)'),
}
# where each person stands, mark by mark (the film moves them between these): label: at, facing, who
PEOPLE = {
    'gunner at the gun': dict(at=(0.0, 0.0), facing=0, who='gunner'),
    'loader at the gun': dict(at=(-0.55, 0.1), facing=0, who='loader'),
    'gunner turned': dict(at=(0.0, -0.05), facing=165, who='gunner'),          # turned round to the door
    'loader turned': dict(at=(-0.55, 0.05), facing=140, who='loader'),   # front on to shots 2 and 4
    'patriot in the doorway': dict(at=(0.62, -2.32), facing=330, who='patriot'),   # leans on the door's west post
    'patriot approached': dict(at=(-0.9, -1.3), facing=35, who='patriot'),     # talking distance, south-west of them
    'gunner facing him': dict(at=(0.0, -0.05), facing=215, who='gunner'),
    'loader facing him': dict(at=(-0.55, 0.05), facing=195, who='loader'),
    'gunner after the blast': dict(at=(1.85, -0.6), facing=271, who='gunner'),     # thrown against the east wall
    'loader after the blast': dict(at=(0.9, -1.3), facing=283, who='loader'),      # a few steps back (Sam, 27 Oct)
    'gunner watching him': dict(at=(1.85, -0.6), facing=326, who='gunner'),   # turned to the gun: front on to
    'loader watching him': dict(at=(0.9, -1.3), facing=351, who='loader'),    # shot 9 (rule 38)
    'patriot at the gun': dict(at=(0.0, 0.0), facing=0, who='patriot'),
}
# Every camera (the film's cam_for builds a sets.Cam from these; focal in pixels for 1080 x 1920)
CAMS = {
    's1': dict(pos=(-25.0, 90.0, 340.0), look=(0.0, 0.0, 70.0), focal=1150, outside=True,
               why='high above the sea, behind the six craft, looking south at the black cliffs'),
    's2': dict(pos=(0.95, 1.65, -1.6), look=(-0.3, 1.3, 1.6), focal=1000),        # behind the crew; door behind us
    's3': dict(pos=(-0.6, 1.7, 0.8), look=(0.62, 1.25, -2.4), focal=1500),        # over the crew's helmets, the door
    's4': dict(pos=(0.55, 1.5, -1.3), look=(-0.3, 1.45, 0.3), focal=1300),        # the crew from in front: the
    's6': dict(pos=(-0.55, 1.6, -1.45), look=(-0.28, 1.45, 0.05), focal=1150),    # front on, beside the Patriot (Sam)
                                                                                # across the frame, never at the lens
    's5': dict(pos=(1.85, 2.15, -2.25), look=(-1.0, 1.0, 0.3), focal=760),        # the wide: high, back-right corner
    's8': dict(pos=(-2.45, 1.65, -0.5), look=(1.0, 1.2, -0.5), focal=760),        # from the west wall, side on (Sam)
    's7': dict(pos=(0.6, 1.5, -0.2), look=(-0.9, 1.4, -1.3), focal=1500),         # the Patriot, from beside the gun
    's9 start': dict(pos=(0.45, 1.42, 1.5), look=(0.99, 1.3, -2.36), focal=820, outside=True,
                     why='in the slit itself, beside the barrel, facing into the bunker'),
    's9 end': dict(pos=(0.45, 1.42, 1.5), look=(1.55, 1.45, -1.29), focal=1700, outside=True,
                   why='the push-in on the two soldiers in the far corner'),
}
GROUPS = {
    'the crew': dict(arriving='at the gun from the start (firing, spotting)',
                     stopped='turned round to the Patriot; small weight shifts, glances at each other; the salute',
                     leaving='thrown back by the blast to the far corner, then stand there dumbfounded to the end'),
}
FRAMING = {   # rule 10: where the Hook Text sits (an empty area) and each key beat with its minimum hold
    's1': dict(hook='the grey sky above the French fields, top third', beats=[('craft and cliffs read', 1.2)]),
    's2': dict(beats=[('firing', 1.0), ('the turn, startled', 0.6)]),
    's3': dict(beats=[('the Patriot leaning in the doorway', 1.0)]),
    's4': dict(beats=[('they look at each other', 0.5), ('back at him', 0.4)]),
    's6': dict(beats=[('the salute', 0.6)]),
    's7': dict(beats=[('arms darting, upset', 1.0)]),
    's8': dict(beats=[('the blast at the slit', 0.4), ('they stumble back', 0.8), ('he walks to the gun', 1.0)]),
    's9 start': dict(beats=[('the sad head shake', 1.0), ('firing, the room lit', 1.4),
                            ('their eyes meet', 1.2)]),
}
SHOT_MARKS = {   # rule 38: who is on screen in each shot, by mark (plan.py checks each faces the lens)
    's2': ['gunner at the gun', 'loader at the gun', 'gunner turned', 'loader turned'],
    's3': ['gunner turned', 'loader turned', 'patriot in the doorway'],
    's4': ['gunner turned', 'loader turned'],
    's5': ['patriot in the doorway', 'patriot approached', 'gunner facing him', 'loader facing him'],
    's6': ['gunner facing him', 'loader facing him'],
    's7': ['patriot approached'],
    's8': ['patriot approached', 'gunner facing him', 'loader facing him', 'gunner after the blast',
           'loader after the blast', 'patriot at the gun'],
    's9': ['patriot at the gun', 'gunner watching him', 'loader watching him'],
}
