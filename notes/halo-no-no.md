# Notes for Halo No-No (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/halo-no-no-handovers.md)
- **Rules that bite at this stage:** 41 (every arm ends in a visible hand: Musk's gloves at the bottom of the close-up),
  43 (eyelines: Musk at the lens except the glance on "We sure will"; Cortana at Musk), 46 (when Sam names frames, look
  at exactly those first), 40 (shot 6 ticked against its Showstopper list at its clip: done, below), 44 (usage: ask Sam
  for the week's figure).
- **Done (29 Oct, building, Opus):** the sets in `source/halo_sets.py` (space wide, ring close-up, the cabin in two
  framings; sheet `review/halo-no-no-sets.jpg`, Sam's note 5 applied: one blue galaxy). The film in
  `source/halo_no_no.py`: story, script timings (placeholders until the recordings), subtitles in chunks, the armada
  in shot 1 (15 cars, lead alone, 4 spinning) and shot 6 (8 cars skimming the hull, 3 spinning), Cortana's discharge
  and poses, the drifting Roadster in the rear window, the theme from 0:21 with its levels. Stills sheet
  `review/halo-no-no-stills.jpg` and three clips (`source/data/halo-no-no/clip-armada.mp4`, `clip-cortana.mp4`,
  `clip-ring.mp4`) sent 29 Oct. Brief checklist ticked. Kit catalogue updated (rule 28).
- **Shot 6 against the Showstopper list (rule 40, at its clip):** hull band, panels, ports, lights: yes; inner face strip
  and far arc: yes; planet behind, galaxy band, stars: yes; about 8 cars in a loose stream, each its own speed, three
  spinning, big as they pass over us and shrinking to the bend: yes; no car shadows (Sam); camera still; the theme loud,
  dipping under the two lines. Changed: the hull runs top left to lower right (ref 02's layout), flagged to Sam.
- **Done (30 Oct, notes, Opus):** Sam's notes on the stills and clips. (1) Shot 1's armada in arrowheads: a V of 5,
  a V of 3 high and a V of 3 low, each arriving at its own time, plus 4 lone spinners spread out (sheet
  `review/halo-no-no-notes-30oct.jpg`, clip `source/data/halo-no-no/clip-armada-v.mp4`). (2) Every Roadster on its four
  jets as in Roadster (shot 1 at 0.55 length so the Vs read; shot 6 and the rear-window car full). (3) "Halo Ringworld"
  fades in at 0.5 s, "Russian - Ukraine War" at 1.0 s, both out together at 4 s. (4) A small green radio light above
  the speaker grille between the seats, lit from the radio voice's first word to his last. (5) All seven recordings
  filed in `source/audio/` (trimmed to the speech; cortana-1 is Le_Epic + Kawaii joined) and the film retimed to them:
  now 44.8 s (shots 0/11.0/18.9/24.6/34.0/36.9). voices.py --film: takes match the script.
- **Next (fresh chat):** Sam's word on the 30 Oct sheet and clip. Then before the first animatic: wire the pre-flight
  checks into `halo_no_no.py` (`scene(t)` is still empty; `audits`, `layers`, `HANDS_OK`, `LOOKS_OK`, the plan's
  `SHOT_MARKS`), run `python3 source/preflight.py halo-no-no OUT_DIR`, fix or name every fault, show Sam the check sheet
  and wait for his yes (CLAUDE.md, 18 Oct). Routine from here: Sonnet.
- **Losses and my additions Sam should know about:** (30 Oct) the lone lead car is now the point of the V of 5; the
  radio light (green) is my choice of colour and place. ref 01's orange galaxy core is gone (Sam's note 5). My additions:
  the pixel crackle as small blue and white squares; Cortana's small mid-air bob now and then; the white caption with a
  black edge for "Halo Ringworld / Russian - Ukraine War"; the theme dips 7 dB under the two lines in shot 6 so the
  voices stay 6 dB clear. The Hook Text is added by finish.py at the end (not on the stills).
- **Rule requests and proposals not yet in a guide:** none.
- **Music (Sam, 29 Oct):** the theme never stops; louder in space (shots 1, 6), quieter in the car (2-5), easing over
  0.3 s at each cut; voices at least 6 dB above it.
- **Files to open:** `notes/halo-no-no.md`, `guides/satire.md`, `guides/film-quality-rules.md`, `source/halo_no_no.py`
  (`python3 source/codemap.py`), `source/halo_sets.py`, `source/halo_cast.py`.

## Plan extras (film-quality-rules 24-26)
**Ambition estimate (rule 24, 44): about 12-15% of a week.**
- New builds: Musk's face (front only, through the visor); Master Chief armour seated, front on (on `views.person`);
  anime Cortana (new head style, hologram look, about 5 poses); the Roadster cockpit (one flat painting, two
  framings); the opening space painting (planet, ring, galaxy); the ring close-up painting; the digital-discharge
  effect.
- Reused: the Roadster car (every angle, the flips) from `source/roadster.py`, recoloured red.
- No 3D builds (rule 39): every place is one flat painting per camera. The car is the Roadster film's projected car.
- Risky moves (rule 8, a clip each before the animatic): the armada entering (formation, spinners); Cortana appearing
  in the discharge; Cortana's turn to show her behind; the armada skirting the ring.
- If over budget, trim first: the turn (keep her front on), then fewer cars.

**Shots (times are estimates until the recordings are in; music starts at 0:21 of the theme):**
| shot | camera | what happens | about |
|---|---|---|---|
| 1 | wide space, upright | orange planet, Halo ring in front of it, galaxy core; Hook Text "Elon Finishes The Fight" (upper middle, 0-3.5 s); white bold caption "Halo Ringworld / Russian - Ukraine War" (lower third, 0.5-4 s); armada enters at 7.0 s (0:28 of the theme), sweeping diagonally left towards the planet, lead car alone in front, some spinning | 0-11 s |
| 2 | windscreen, facing in (two seats) | Musk in the armour at the yoke, turning it back and forth; radio line; "Sir, finishing this fight." | 11-17 |
| 3 | hard cut to Musk close-up | "If we don't stop Zelensky..." | 17-22 |
| 4 | windscreen (hard cut back) | discharge flash and pixel crackle; Cortana appears above the passenger seat; her Chungus line | 22-29 |
| 5 | hard cut to Musk close-up | "We sure will, Breeder 04." | 29-31 |
| 6 | ring close-up (Showstopper Shot) | armada skirting the ring's superstructure; over it, from inside the car, Cortana: "Musk-San, please let me die." Musk: "No." (Sam: all from space) | 31-38 |
| - | sign-off | CranbriJoos, 2 s | 38-40 |

**Eyelines (rule 25, 43):** Musk looks ahead out of the windscreen (at the lens) throughout, except a glance to
Cortana's side on "We sure will". Cortana looks at Musk.
Radio: nobody on screen.

**Sound effects (rule 26):** none (Sam: no others needed). The radio line is filtered to sound like a radio. The
discharge crackle is picture only.

**Bleeped words (rule 27):** none.

## The world (rule 1)
Space shots: painted backdrops (no rooms). Cockpit: the Roadster's two seats, camera at the windscreen facing back.
Left-hand drive: Musk on the right of the frame, the passenger seat (Cortana) on the left. Sizes from
`source/sizes.py`; the armour makes Musk about 2.1 m standing, so he fills his seat and touches the roof line.

Composition sheet sent: 29 Oct, review/halo-no-no-composition.jpg

**Shot 6, Showstopper Shot list (rule 40; Sam to approve or trim):**
- The ring's hull: a huge dark band sweeping from lower left up to top right, filling half the frame; plated in panels
  with round ports and hundreds of tiny lights (ref 02), so its scale reads.
- The ring's inner face: a thin strip along the band's top edge showing seas, land and white cloud (ref 02).
- The far side of the ring arcing high across the sky, thin, getting fainter.
- The planet behind, lower left, in shadow; the blue galaxy band top right; stars.
- About 8 Roadsters skimming the hull in a loose stream, big and near at the bottom, shrinking into the distance:
  most fly level, two or three spin nose over tail like in Roadster, each at its own speed so the stream stretches.
- ~~Each car's flat shadow on the hull~~ (Sam, 29 Oct: no car shadows).
- The camera holds still (flat painting); the cars do all the moving.
- No sounds: the theme, loud (space shot), with the last two lines over it.

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word) | done? |
|---|------|------|
| 1 | The Halo ring visible against an orange planet. | yes: shot 1, the ring over the planet's lower half |
| 2 | The Halo theme playing from .21 seconds into the track. | yes: `THEME_FROM = 21.0` |
| 3 | White bold text appears for a few seconds: "Halo Ringworld" / "Russian - Ukraine War" | yes: white bold, lower third, 0.5-4 s |
| 4 | From .28 in the theme track, a fleet of Tesla Roadsters enter the scene, streaking in Armada formation towards the Halo. | yes: `T_ARMADA = 7.0` (0:28) |
| 5 | Some are spinning in space, just like in Roadster. Others fly straight, including the one flying in front of the armada on its own. | yes: 4 of 15 spin nose over tail; the lead car flies alone in front |
| 6 | Spaceship armada sweeping diagonal left towards planet with Halo Ringworld visible in the distance (ref 01). | yes: streaming in from the right towards the planet and ring |
| 7 | Cut to Tesla Roadster interior, camera at windscreen position and facing in. | yes: shots 2 and 4 |
| 8 | At the driving wheel is Elon Musk in Master Chief's armour. It is clearly Elon Musk through the armour's view screen. | yes: face through the gold visor |
| 9 | He's turning the steering back and forth. | yes: `yoke_turn` (held, then turned the other way) |
| 10 | Voice over the radio: "Musker Chief, you mind telling me what you're doing in that Roadster?" (sounds like it's coming through the radio) | yes: subtitles now; `radio()` filter ready for the recording |
| 11 | Musk (serious): "Sir, finishing this fight." | yes, line 2 |
| 12 | Zoom in on Musk. (Sam, 29 Oct: a hard cut to the close-up) | yes: hard cut to shot 3 |
| 13 | Musk: "If we don't stop Zelensky from using the Halo, all life in the galaxy could be wiped out." | yes, line 3 |
| 14 | Back to windscreen shot. | yes: shot 4 |
| 15 | Showcase shot: Anime Girl Cortana appears, holographic and smaller, above the opposite seat, standing mid-air, after a sudden bright light of digital discharge and pixelated crackling. | yes: one-frame flash, pixel crackle, she forms in bands over the seat |
| 16 | All of her movements are overemphasised and enthusiastic, occasionally shoving forward her breasts or showing her curvaceous butt. | yes: appear, point, kawaii, thrust (side on), turn (her behind) |
| 17 | Anime Cortana: "Oh, Musker Chief, we're going to make him look like such Le Epic Chungus!! Kawaiii!!" | yes, line 4 |
| 18 | Zoom back into Musk. (hard cut) | yes: hard cut to shot 5 |
| 19 | Musk: "We sure will, Breeder 04." | yes, line 5 (with a glance at her) |
| 20 | The Roadster Armada approaching the Halo Ringworld in the famous shot from the close-up reference (02), skirting alongside its superstructure. | yes: shot 6, 8 cars skimming the hull (ref 02 layout) |
| 21 | Anime Cortana: "Musk-San, please let me die." | yes, line 6 over shot 6 |
| 22 | Musk: "No." (Sam, 29 Oct: lines 21-22 all from space, over the ring shot) | yes, line 7 over shot 6 |
| 23 | The joke: Musk thinks he's saving the world by taking weapons away from Ukraine but he's actually being a massive dweeb. | yes: the script as written, played straight |
| 24 | No other sound effects are needed. | yes: none (radio filter only) |
| 25 | Everything 2D, except Anime Girl Cortana and the Roadster Armada. | yes: paintings 2D; Cortana and the armada 3D |
| 28 | Hook Text: "Elon Finishes The Fight" (Sam, 29 Oct). | yes: `HOOK` (finish.py adds it) |
| 26 | Usage is incredibly tight: be efficient, keep the action simple. | yes: about 12-15% of a week planned |
| 27 | The theme music should always be playing, quieter but still noticeable in the Roadster scenes and louder in the space scenes. | yes: `music_gain` (space loud, cabin -11 dB, 0.3 s eases, dips under the space lines) |

## Benchmarks (rule 3): each place beside its reference, `review/halo-no-no-sets.jpg` (`python3 source/halo_sets.py sheet OUT`)
| place | item | ours |
|---|---|---|
| shot 1 (ref 01) | big orange-brown planet on the left, cut by the frame edge | yes, banded and blotched, one outline |
| | its night side top-left | yes, a dusk band then the night side |
| | thin dark ring tilted in front of its lower half | yes, the near half dark hull with tiny lights, the far half a pale strip |
| | the galaxy, back right | ref 02's blue stripe (Sam, note 5: one galaxy in both space shots), not ref 01's core |
| | violet and blue nebula | yes, flat lumps, no outline (light, not a thing) |
| | dense small stars | yes, round dots only (no four-point stars: off-style) |
| | room for the Hook Text (top) and the caption (lower third) | yes, dark sky at the top; the caption sits over the planet's lower part |
| | an open lane on the right for the armada | yes |
| | the grey warship (ref 01) | left out: the brief has only the Roadsters |
| shot 6 (ref 02) | the dark hull band sweeping from the top left down to the lower right | yes, a true circle projected (`RING_CAM`), so the sweep is right |
| | hull panels, round ports, hundreds of specks of light | yes |
| | the far side rising up the right as a thin strip of seas, land, cloud | yes, with grey rim walls |
| | the planet behind on the left | yes, lower left, its night side away from the light |
| | the blue galaxy band top right | yes, behind the far arc |
| | stars and nebula | yes |
| | no car shadows | yes (Sam, 29 Oct) |
| | room for the cars to skim the hull | yes: the space under the hull, the frame's lower half |
| cabin (refs 03-05) | white sport seats, headrest built in, shoulder wings, grey bolsters | yes |
| | the black ROADSTER plate with red letters on each headrest | yes (Musk's helmet hides his) |
| | black glass roof in a black frame | yes, two panels onto space |
| | black centre console, the screen between the seats | yes (the screen from behind, clear of Musk's arms) |
| | red trim light | yes: doors, rear bulkhead, under the dash's edge |
| | black yoke | yes (`halo_cast.yoke`) |
| | the rear window onto space, a Roadster drifting past | yes (Sam's yes, 29 Oct); the car is white like the armada (Sam: the Roadster film's white car) |
| | dark doors with handles; dash with tweeter grilles and defroster slots | yes |

## References as checklists (guides/satire.md): `references/halo-no-no/`
| reference | what it shows | ours matches? |
|---|------|------|
| 01 | opening layout: big orange-brown planet left, dark shadow side top-left; thin dark ring tilted in front of its lower half; bright galaxy core centre; a grey warship and small ships right, heading left | |
| 02 | ring close-up: the dark hull band sweeping from left to lower right then up, panelled with round ports and specks of light; inner surface a thin strip of oceans, land and cloud; planet behind left; blue galaxy band top right | |
| 03-06 | Roadster: red body, black glass roof, white sports seats with red ROADSTER on the headrests, black yoke steering, black centre console, a screen on the dash, red trim light | |
| 07-09 | Elon Musk: straight-on (08), three-quarter in a suit (07), smiling (09); receding hairline, swept hair, long face, heavy brows, small eyes, thin lips, soft jaw | |
| 10-12 | Master Chief (Campaign Evolved): olive green plates, gold visor, grey undersuit, chest plate with a ridge, big shoulder plates, side helmet lights | |
| 13-15 | Cortana (Campaign Evolved): blue, circuit lines, short bob | |
| 16 | Chief beside Cortana: her height and place beside him | |
| 20-21 | Musk talking: mouth shapes, teeth show little, lower lip full; short cropped hair in 20 | |
| 24-25 | Musk comic drawings (Sam, 29 Oct): 25 the clearest: hair swept up and back, parted on his right, deep temples, heavy straight brows close over hooded almond eyes, long nose with a round tip, defined upper lip, smirk | |
| 22-23 | Musk cartoons (Sam, 29 Oct: what to exaggerate): high forehead with deep M-shaped receding temples, hair swept up into a tuft, wide face with full apple cheeks and deep smile folds, small narrowed eyes with crow's feet, a long nose with a round bulb tip and flared nostrils, thin upper lip over a fuller lower one, round chin with a dimple, ears sticking out | |
| 17-19 | anime Cortana: big eyes, glossy bob with a long fringe lock, bodysuit with white panel lines (18), the look to copy | |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | cast | - | Musk not quite identifiable: use the cartoon refs 22-25 | rebuilt from refs 08, 22-25: high forehead, deep receding temples, hair swept up, wider face, hooded eyes, long bulb nose, defined lips, goatee (new kind) |
| 2 | cast | - | a neck in his helmet, like Damon in Roadster | neck into the undersuit collar (new kind) |
| 3 | cast | - | one Cortana pose really thrusting her breasts towards him | new side-on pose 'thrust' on "Le Epic Chungus": back arched, chest pushed at him, fists behind her (new kind) |
| 4 | cast | - | his head fills the helmet: only a thin gap to the helmet wall | visor reshaped round his head, head enlarged (new kind) |
| 5 | sets | - | two different galaxies (refs 01 and 02): keep ref 02's blue stripe | one `galaxy_band` in both space shots; ref 01's orange core gone (new kind) |

Decisions made:
- Audio: `source/audio/halo-theme.mp3` (Sam, 29 Oct), 2:58 long; film starts at 0:21, armada enters at 0:28.
- Answers 29 Oct: Sam records all voices later; build and time from the script with subtitles first. Hard cuts to
  the close-ups (no zoom). The last two lines play over the ring shot (from space). The car is the Roadster film's
  white car (`source/roadster.py`), interior from refs 03-05. Flat cartoon style for space. Cortana: flat, see-through
  blue with scan lines and a slight glow (Sam's exception, like Poker Mon's beam); a grown woman in the bodysuit of
  ref 18, fan-service played as cringe, never explicit. Musk: face clearly through a see-through gold visor, no light
  streak (it might hide him), no exaggeration (likeness straight). About 15 cars in shot 1, 8 in shot 6. Shot 6 is
  a Showstopper Shot (rule 40 list before building). Hook Text: "Elon Finishes The Fight".
- Musk talking references: 20, 21 (Sam, 29 Oct).
- Composition sheet: Sam said proceed (29 Oct); the shot 6 list and my two additions stand.
- Cast (29 Oct): Musk's visor made taller than the real helmet's so his whole face shows and talks (my call, flagged);
  the helmet's inside kept dark grey (brown read as long hair). Cortana: the high-collared bodysuit of ref 18, about
  0.6 m tall; poses appear, point, kawaii (fists by her cheeks, chest out, a wink), turn (from behind, hip popped,
  looking back over her shoulder: rule 38 exception).
- Music never stops (Sam, 29 Oct): louder in the space shots (1, 6), quieter but noticeable in the cockpit (2-5, 7-8), easing
  down and up over about 0.3 s at each cut; the voices stay at least 6 dB above it (pre-flight checks).
- Cast sheet (Sam, 29 Oct): yes to the taller visor, the high-collared bodysuit (ref 18) and the Roadster drifting past
  the back window in the car shots; **no car shadows on the ring**. Cast approved; on to the sets.
- Sets built 29 Oct in `source/halo_sets.py` (sheet `review/halo-no-no-sets.jpg`). Shot 6 follows ref 02's layout (the
  hull from the top left down to the lower right, the far side rising up the right), not my list's "lower left up to
  top right": flagged to Sam. The cars will skim under the hull, near at the bottom left, shrinking towards the turn.
- Sets sheet (Sam, 29 Oct): one note (5, the galaxy), then "go": on to `source/halo_no_no.py`.
- Stills and clips sent 29 Oct (`review/halo-no-no-stills.jpg`, three clips).
