# Notes for Roadster (one file, numbered; mark each done as it is fixed)
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 |      |      |      | open   |

Decisions made (kept so a long session or a new session never has to rediscover them):
- Source: the Tesla Roadster "flying car" unveiling clip (16 Oct 2026), 10.07 s, one continuous shot, 826x480, 30 fps.
  Car climbs a tall curved near-vertical lit ramp in a dark hangar (0-4 s), launches off the top and flips (4-5.5 s),
  lands in white smoke and spins with red light trails (6-10 s). Camera pans left to follow, then pushes in slightly.
  HUD at the bottom: left dial g-force (about 0.2-1.5) with a pitch icon, right dial speed (7 -> 67.8, peaks ~4.5 s).
  Audio: steady music/noise throughout, about -14 dB.
- Joke: Teslas go out of their way to cause a fatality "accidentally"; Elon's showing off and Mars ambitions.
- Hook Text: "Tesla Kills Two Birds With One Stone". No title.
- Style: Satire style for all assets; every space element (clouds, Earth, stars, Mars from space) in Dam's
  coloured-pencil style (`source/beaver_asteroid.py`). The car stays the Satire-style car in every shot.
- Shots: (1) shot-for-shot copy of the original, but the car keeps flipping and firing hydraulics; (2) through the
  hangar roof; (3) up through ordinary clouds; (4) wide, bursting through the high cloud layer; (5) silent Earth from
  space (as Dam); (6) flipping through the stars; (7) flipping towards Mars in the distance; (8) hard cut to The
  Martian's set, Matt Damon in his suit, silent and hopeful, eyes widen at his rescue; (9) the car drops and
  explosively flattens him: we never see him again, he is just gone; (10) broken robot voice "Fatality Avoided";
  CranbriJoos sign-off via finish.py. Length about 25-30 s, judged on the animatic.
- Dials: numbers only. Speed climbs to the speed needed to reach Mars in one hour: average Earth-Mars distance
  225 million km, so 225,000,000 km/h = about 139,800,000 mph (the original dial reads mph).
- Sound: the original clip's sound for the copied section; then the hydraulics continue through the journey, never
  too loud or annoying, getting nearer and further as the camera distance to the car changes. Sam records
  "Fatality Avoided" flat; we make it robotic and glitchy. Damon silent.
- References: Sam is sending them (Roadster, The Martian set, Damon in suit, stars and Mars-in-the-distance shots).
- Hydraulics come from the original audio (Sam, 16 Oct): the hiss band (2-8 kHz) rises from 3.25 s, peaks at 4.25 s
  (the launch off the ramp) and fades by 5.75 s; a smaller hiss at 0-1.25 s; thumps at 5.69 and 6.04 s (landing).
  Music sits under it, so the cut-out hiss is high-passed and checked on a sound-check file before any render.
- Each flip faster than the last, scene by scene (about 1.4 s per flip in shot 1 down to about 0.25 s by the Mars
  approach); each flip gets its hiss, shorter and a little higher each time, never louder than the original.
- Impact: Sam supplies the crash sound. The car crumples catastrophically on Damon: real impact (screen shake, dust
  ring, roof caved in, wheels splayed, panels buckled, glass and parts scattering under gravity and staying put).
  Damon is simply gone. When "Fatality Avoided" is spoken, one light on the wreck flickers on (a single headlight).
