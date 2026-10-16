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
- Car references in `references/roadster/` (Sam, 16 Oct). Design read from them: white wedge supercar, faceted flat
  panels (Countach-like), black lower sill band, dark six-spoke wheels, tall rear wing, full-width red light bar,
  plate "RDSTR", four round exhausts. Front: two small triangular corner headlights + a thin white light bar across
  the nose (the wreck light is one of these corner headlights; 02 is a Model 3 lamp, used only for the glow).
  The "hydraulics" are the underside cold-gas jets: four white plumes straight down (03, 05, 08), which make the smoke
  in the original. 08's body looks like a Cybertruck/Cybercab: used for the jets and smoke only. 04 (white seats,
  red trim) is for the wreck's exposed interior. Musk (06) is not in the film.
- Mars references 09-18 in `references/roadster/` (Sam, 16 Oct). The film's real set: Wadi Rum sandstone cliffs and
  hazy orange-brown sky; the Hab is a low white segmented building with round white airlock cylinders (09, 13, 14),
  a US flag on its side, solar-panel boards, NASA crates, numbered sample flags on poles, the R2 rover with big balloon
  tyres (17). Watney's suit: orange-red and white panels, grey knee pads, big chest unit, helmet with side lights,
  WATNEY on the helmet top and a big "20"-style number on the backpack (11, 14). 10, 15 and 18 are concept/fan art
  (domes, a different rover): not used, the film's own look wins. Shot 8 is staged on 13 (the film's wide shot),
  reframed upright: cliffs high, the Hab behind, Damon by the panels, rocks and flags in front; the car falls from the
  top of the frame.
- Damon references 19-24 (Sam, 16 Oct). Helmet: clear bubble with a gold visor over the top half, the face visible
  below it; orange-and-white helmet shell rim, side lamps, a red "2" on the helmet side. Suit: orange-red and silver-grey
  panels, "ARES III" down the chest strap, a white chest control box, US flag and NASA patches on the shoulders, a red
  "2" on the shoulder and backpack, dark grey gloves with silver knuckles. Face: short brown hair, light stubble, NO
  moustache (Sam), steady blue eyes. 24 for the front.
- Space references 25-32 (Sam, 16 Oct), all drawn in Dam's coloured pencil. Shot 6 (stars): deep blue-black with soft
  blue-violet nebula wisps (25), a faint Milky Way band (26), dense small blue-white stars with a few bright
  four-point ones (27), and the green comet (28) drifting far behind the car. Shot 7 (Mars): starts small and
  side-lit in the distance (30), the car flipping towards it as it grows until it fills the upright frame half
  off-screen (31), with craters, the dark Valles Marineris scar and a white polar cap (29, 32). Hard cut to the surface.
- Ramp references 33-35 (Sam, 16 Oct). The ramp: pale grey concrete, red neon strips down both edges, a white centre
  line, rising from a flat floor plate with a small lip, curving up to near-vertical; a steel lattice scaffold tower
  behind its right side; black hangar beyond. The car starts at the foot, seen from behind (35), and climbs.
- CORRECTION to the dials: the HUD reads "G-FORCE 1.0 G" (left, with a side-on car icon) and "ALTITUDE 0.0 FT"
  (right, with a top-down car icon). The number that rose to 67.8 is ALTITUDE in feet, not speed. Plan: keep both
  real dials. Altitude climbs to the Mars distance, 738,188,976,378 ft (what one hour at Sam's 139,808,750 mph
  covers); G-force climbs to 1,274,210 G (reaching that speed in about 5 s). Speed is not shown (Sam may overrule).
- Sound files (Sam, 16 Oct), in `source/audio/`: `roadster-1.m4a` = "Fatality avoided." (3.2 s; speech 1.02-2.56 s,
  ~7 syllables as expected, -20.6 LUFS, a clean second of silence in front); `roadster-crash.mp3` = Sam's crash
  (2.1 s, sound until 1.69 s, peaks -0.4 dB: placed by when it really starts, `filmkit.place`);
  `roadster-original.m4a` = the original clip's sound. The clip itself: `references/roadster/00-original-clip.mp4`.
- Sam's notes on the cast sheet (16 Oct), all fixed: no moustache (he usually has none); the face redrawn closer to
  Damon (broad square head and jaw, dimpled chin, strong straight brows, deep-set eyes, fringe pushed up, light
  stubble); a thick neck rising out of the dark inside of the suit (no floating head); the airlock joined onto the
  Hab; the "DAYS WITHOUT AN INCIDENT" board removed (never asked for) - the hangar wall has panel seams and an EXIT sign.
- Sam's notes, round 2 (16 Oct): likeness approved. No name on the helmet (text laid over looked bad). NO close-up:
  in the Mars shot Damon is framed big enough to read his eyes (scale MARS_S, the set behind him) and they widen from
  strength 2 to 5 as the car falls. The helmet's dark inside is one shape with a flat, level top line straight across the bubble, over the neck (Sam: a dip showing more neck is not how light works). The car lands UPSIDE DOWN, jets
  off: it just drops and crashes down flat on him (the wreck is drawn upside down, wheels in the air).
- Shot plan (16 Oct, stills sheet `python3 source/roadster.py stills OUT.jpg`): 1 hangar 0-10.6 s (the original to
  6 s, then hops on its jets flipping every 1.4 s, full jets and up at 9.6 s); 2 out through the roof 10.6-12.0;
  3 clouds 12.0-13.6; 4 cloud sea 13.6-15.4; 5 Earth 15.4-17.6; 6 stars 17.6-19.6; 7 towards Mars 19.6-21.8;
  8 Mars 21.8-29.0 (a speck at 22.9, eyes 2->5, impact 24.2 with shake and a dust burst, the line's file at 25.0,
  "Fatality avoided" and the lamp at 26.0). Flip periods per shot 1.4 -> 0.3 s. Dials on until the impact; long
  numbers sit on a plate under the dial. Damon at MARS_S 0.85 so the wreck lands on the ground in frame.
  29 s + the 2 s sign-off.
- Sam's notes on the stills (16 Oct), fixed: shot 1 follows the original's camera (still on the ramp for the climb,
  then panning left with the car as it flies, lands and hops; the ramp leaves the frame on the right; the hangar is
  4000 px wide, with red floor light strips and small blue lights as in the original). Shot 8: the car falls straight
  down onto him, so it is full size at his distance from the first frame (never growing), drawn in front of him;
  he can't see straight up, so its reflection grows in his visor and its shadow spreads round his feet; it drops into
  the top of frame 0.35 s before the impact, upside down, nose towards us. Mars zoomed out (MARS_S 0.64). Dials
  bigger (radius 92, numbers 38 px) inside the safe area (x 165 and 800, y 1385); a long number shows short in the
  dial (1.3M, 738B) and in full on a plate above it.
- Sam's animatic notes (16 Oct), done: (1) shot 1 rebuilt from the original frame by frame (3.0-6.8 s at 6 fps): it
  climbs round the curl (pitch 0 -> 170 deg, mid-ramp at 0 s, the top at 4.3 s) and hangs upside down under it;
  falls at 4.55 s, turning nose-down then upright by 5.5 s; the jets ignite at 5.0 s mid-turn; it flies left on its
  jets, sinking into the smoke, and settles at 6.7 s; the camera holds until 4.6 s then pans left with it. Then its
  own hops and flips, and straight up at 9.2 s. The shot ends at 10.05 s, where the original's sound ends (the crowd
  as it shoots up); the sound is cut at the transition. (2) A crunch through the roof (a 0.45 s slice of Sam's crash,
  quieter). (3) Damon given 3 more seconds: looks about, a deep sigh (shoulders up then sinking, hands drop), looks
  at the floor as if nobody is coming, then the shadow, he looks up, eyes widen, the crash. Film 31.4 s + sign-off.
  (4) Hook Text: "Tesla Kills Two Birds With One Stone 🚀" (the rocket as a Noto emoji image at the end of the line).
  (5) New standing rule for every film: natural, moderate movement (guides/satire.md, best-practice.md 1.2).
  Space shots: Sam loves them - leave them alone unless he asks.
- Sam's animatic-2 notes (16 Oct), done: the ramp is now ONE 3D curve (flat run, curve to vertical, tall vertical,
  the curl to 170 deg, then a 3.8 m overhang the whole car hangs from) seen from the side-diagonal camera of his
  170-deg reference; the car is placed on the same curve with the same camera (`car_on_ramp`), so it stays centred
  on the surface in perspective every frame; off the top it rolls upright while its nose dips to the ground, jets
  firing, then flies left. Exit signs removed (no signs in the hangar). Dial car icons removed (cluttering). Shot 8:
  once the car's underside reaches his helmet he is squashed down under it (never passes in front of him). The dust
  rebuilt after Sam's dust-storm photo: a dense low wall, many ragged billows with dark undersides and pale tops,
  streaky curtains, dark grit spraying out, dirt clods, stones and car parts on Mars gravity landing and staying;
  the cloud thins over ~2 s to a haze. Not Looney Tunes.
- Sam's animatic-3 notes (16 Oct), done: the car starts nearer the bottom of the ramp (as the original); the G-force
  climbs through the journey (4 G at the launch, the full 1.27M by the stars shot), not in a second; the dust larger
  and lasting longer (thick for a second, the plume thinning over 3.4 s; the low dust in front settles first so the
  wreck and its lamp show on the line); the sigh slower, bigger and clearer (a big breath in, eyes closed on the long
  breath out, shoulders sinking lower, hands coming down slowly; +0.6 s, film 32.0 s); the visor reflection was a
  white blob that read as a bubble coming through the helmet - now a tiny upside-down car, wheels up.
- Sam (16 Oct): the sigh read as happy and content (mouth corners up, closed eyes as calm arcs). Now: uneasy while
  looking about (flat mouth, brows up in the middle), weary on the sigh (lips apart on the breath out, closed eyes
  drooping at the outer corners), low and lonely looking at the floor (mouth corners down, sad brows); alert at T_SEEN.
