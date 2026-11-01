# Notes for Patriots 4 (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; old ones go to notes/archive/patriots-4-handovers.md)
- **Rules that bite at this stage (rule 48):** 46 look at exactly the frames Sam names first; 45 the composition sheet
  is never re-sent; 25 (a note repeated is a warning: find why the first fix failed); 41 every arm ends in a visible
  hand (shot 12's pointing hands, the table hides anything below its edge); 43 looks at each shot's camera; 44 log usage.
- **Done (1 Nov, building, Opus high):** the cast (`source/patriots4_cast.py`, sheet `review/patriots4-cast.jpg`):
  Romesh 74% (series look: short salt-and-pepper beard, clear frames, curls), Bash 88/91%, Claudia 80/68% (rebuilt),
  all 1st in the line-up; the Patriot's stare grows slowly from 1 to 4 (Sam). The room (`source/patriots4_room.py`):
  painted once all round (rule 39): pointed arch with lattice and panelled doors behind Claudia, panelled walls, fire
  baskets, torches, candles, the Round Table hall through the opening behind Romesh (reused `traitors.wall`,
  `traitors.round_table`); the table top and coin pile a fixed foreground, the camera turning on the spot (`PanCam`).
  The film file `source/patriots4.py` (from the template): 12 shots, 49.0 s; recordings placed; subtitle chunks on the
  recording's own stretches; mouths per stretch (`parts`); plan checks clean; `plan.py` clean. Stills sheet sent:
  `review/patriots4-stills.jpg` (`python3 source/patriots4.py sheet OUT.jpg`).
- **Done (1 Nov, applying the stills notes, Opus medium):** notes 1-3, then Sam's second batch 4-8 (Notes table);
  Sam: ignore the overhead-picture question; the silences stay for now. Shot 13 added (Sam's yes to my proposal): over
  the Patriot's shoulder, his pointing arm and finger in the corner, Romesh and Bash drop their mouths open, then
  slide their eyes to each other (48.2-50.2 s; shot 12 now ends 48.2). Pre-flight wired up (`scene`, `audits`,
  eyelines by time `looking_at`, `NOTES`, benchmark paths); brief checklist ticked. Faults fixed on the way: hands
  over the table and the over-shoulder backs were misplaced at full quality (SS 2); `traitors` / `patriots3_cast`
  put the plain circle hands back on first use (loaded up front now); the table's footprint touched legs on the plan
  (R 0.62); Romesh looked the wrong way in shot 9; captions merged; the "Errrr" line shortened to fit 700 px.
  Pre-flight: 7 faults left, all named: 3 voice flags meant (Sam, note 3); 3 captions under reading time (they follow
  Bash's and Romesh's speech; longer chunks break 42 characters); shot 2 is 8.9 s (Bash's unbroken speech). Sam said
  "proceed to animatic" (his override: no wait for a yes on the check sheet; checks still run). Animatic 1 rendered
  and sent. Sam's animatic-1 notes 10-12 applied; pre-flight the same 7 named faults; clips sent (5.5-27 s cuts,
  44.5-50.2 s ending); waiting for Sam's yes to animatic 2 (check sheet sent).
- **Next (Opus medium, reading Sam's notes):** Sam's notes on animatic 1, then the clips/fixes; the final render only on
  his clear yes, then `finish.py` with the Hook Text.
- **Losses, cheats and my additions:** shot 9 is a film cheat: Romesh and Bash are drawn closer together (227 and 256
  degrees, not 210 and 270) so both faces are big enough for the eye slide; note 1's knock-ons: the people's legs now show
  under and beside the small table (they stand behind it), the floor of the winner's room is painted (dark boards:
  my addition, needed now the table no longer fills the frame's foot), the coins are 86% the size and 5 scattered
  coins instead of 9 (loss), the pedestal's lit floor ring is drawn but below the frame in every shot; on the plan the
  four stand 0.52 m from the centre, not 0.95 (no change on screen). Notes 4-8: with the camera at the table's edge
  the table fills the frame's width again in every shot, so the 25% cut shows only as less table round the pile
  (flagged to Sam); the Round Table has 8 chairs (5 round the far side, 2 side on, 1 near: more than the 4 asked, so
  some show in shot 3); the Patriot's pointing finger is an exception to the plain circle hands (Sam asked for Power
  Crime Action's); the pans no longer change zoom (every table shot is at the same distance). Shot 12 shows the backs of Bash's and
  Romesh's heads in the bottom corners so the Patriot's two-armed point has targets (addition); the Patriot's hands are
  circles (no pointing finger: house style). Set dressing from the refs only (fire baskets, torches, candles, lantern
  look); no signs or jokes of mine. Bash's two silver rings not drawn yet.
- **Usage (rule 44):** 9% of the week at the stills round (7% at the cast round, 3% at the start): about 6% spent
  on this film of the 15% budget.
- **Rules:** Sam will discuss all rule proposals at the END of the project; two are waiting (listed in the archived
  handover of the cast round).
- **Files to open:** this file; `guides/satire.md`; `source/patriots4.py` (codemap); `source/patriots4_room.py`;
  `source/patriots4_cast.py`; `review/patriots4-stills.jpg`.

## Recordings (filed 1 Nov; `python3 source/voices.py` measured)
| file | line | length | phrases (s) |
|---|---|---|---|
| `patriots4-claudia-1.m4a` | Claudia: "Romesh and Bash, remind us who you did this for?" | 7.2 s | 0.87-6.62 (5 phrases, slow) |
| `patriots4-bash.m4a` | Bash: "I did this for a wonderful organisation, they are called Choose Love. They help displaced people all over the world including queer refugees." | 9.1 s | 0.91-7.44, 7.64-8.75 |
| `patriots4-romesh.m4a` | Romesh: "I'm doing this for a cause that is very dear to my heart, it's the Refugee Council." | 6.6 s | 1.02-5.87 (3 phrases) |
| `patriots4-claudia-2.m4a` | Claudia: "And what about you?" | 3.6 s | 1.00-3.12 (3 phrases) |
| `patriots4-patriot-err.m4a` | The Patriot: "Errrrr..." (one unbroken sound) | 40.3 s | 0.37-39.82; we use about 18 s, fading gently over the last 4 |
| `patriots4-patriot-traitors.m4a` | The Patriot: "Traitors." | 2.0 s | 1.39-1.82 |
Estimated length: about 44 s plus the 2 s sign-off.

## Plan extras (film-quality-rules 24-26)
- **Ambition estimate (rule 24): about 15% of a week.** New builds: Romesh and Bash (likeness heads, outfits); the
  winner's-table room as flat paintings (rule 39: no 3D; arch with lattice, panelled walls, fire bowl, wall torches,
  candles) for 2 cameras; the round winner's table and its coin stack; Claudia's cream high-neck blouse. Reused:
  Claudia (`traitors_cast`), the Patriot (`patriots3_cast`), the Round Table and room walls far behind the Patriot
  (`traitors.round_table`, `wall`). New pose: hands pressed together at the chest (Bash, refs 07-08). Risky moves: the
  swivels (camera pans), the eye moves in the "Errrr" stretch (timing is the joke), the two-handed point.
- **Eyelines and holds per shot (rule 25):** in the shot list below.
- **Sound effects (rule 26):** none (Sam: none required). Voices only.
- **Bleeps (rule 27):** none.

## The world (rule 1): `source/patriots4_plan.py` (metres; `python3 source/plan.py patriots4 sketch OUT.jpg`)
- A round winner's table seen from above like a clock (Sam, 1 Nov: the Patriot at 2, so three quarters of the table
  are free for the shots before the reveal): Claudia at 12 (the arch the banished leave by behind her), the Patriot
  at 2, Romesh at 7 (the Round Table hall far behind him), Bash at 9. Table 1.3 m across, 0.95 m high; coins in about
  7 tiers in the middle.
- The "swivel": the camera circles the coin pile 0.55 m out, always across it from the person it shows, so the coins
  sit in the foreground and everyone faces the lens (rule 38). It swings round the pile from one person to the next.
  (Changed from "a camera turning on the spot over the centre": from there the coins are out of frame.)
- Shot 9 is over the Patriot's shoulder (his back at the frame edge): Romesh and Bash in one frame, faces big enough
  for the eye moves. Romesh three-quarter (28 degrees): list in `THREE_QUARTER_OK`.
- **3D note (rule 39):** a camera that circles needs the room from every angle on the circle, so the winner's room is
  a simple 3D set (four walls, the arch, the opening to the Round Table hall) with flat painted detail on its walls.
  The Round Table far off stays a painting (reuse `traitors.round_table`).

Composition sheet sent: 1 Nov, review/patriots4-composition.jpg
Stills sheet sent: 1 Nov, review/patriots4-stills.jpg (the room panorama, the camera turning on the spot) (`python3 source/patriots4_compose.py OUT.jpg`)

## Shot list (Sam said yes, 1 Nov; times from the recordings)
| # | camera | who, what | looks | about |
|---|---|---|---|---|
| 1 | across the coins at Claudia | "Romesh and Bash, remind us who you did this for?" | between Bash and Romesh | 6.5 s |
| 2 | circle round to Bash | his line, emotional, excited; hands meet at his chest, eyes close on "wonderful" | Claudia | 8.8 s |
| 3 | on round to Romesh | his line, sincere, hands on the table edge | Claudia | 5.6 s |
| 4 | back round to Claudia (via Bash: never past 2 o'clock) | "And what about you?"; her eyes go to her left | the Patriot (off frame) | 2.6 s |
| 5 | circle to her left: the Patriot revealed | eyes widen; "Errrr" starts | Claudia | 2.5 s |
| 6 | Claudia, close | staring intently | the Patriot | 3 s |
| 7 | Bash, close | staring, blinking | the Patriot | 3 s |
| 8 | the Patriot, close | eyes stay wide, slide sideways to Romesh (head still) | Romesh | 3 s |
| 9 | over the Patriot's shoulder | Romesh and Bash slide their eyes to each other | each other | 3 s |
| 10 | Claudia, close | staring, blinking; the "Errrr" fades out | the Patriot | 3.5 s |
| 11 | the Patriot | awkward silence, eyes still wide | ahead | 2 s |
| 12 | the Patriot | both arms out, a finger at each, narrowed accusing eyes: "Traitors." | Romesh, Bash | 2 s |

Sam's answers (1 Nov): 1 the Patriot at 2 o'clock; 2-5 yes; 6 yes, with narrowed accusatory eyes; 7 the "Errrr"
subtitle stays one fixed line; 8 Hook Text "Celebrity Traitors winners reveal their charities", over the arch;
9 Claudia as in this final (black jacket, cream high-neck blouse); 10 heights: Romesh, Bash, Patriot 1.78 m,
Claudia 1.70 m. Likeness photos 13-23 filed; cards made (`likeness.py card`): Romesh 2 straight-on usable, Bash 2,
Claudia 2 (rule 51 asks 3; Bash's card reads light stubble as a beard: check by eye; no caricatures yet).

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail, ticked before the first animatic
| # | from the brief (Sam, 1 Nov) | done? |
|---|------|------|
| 1 | Celebrity Traitors final 2026: winners Romesh Ranganathan and Sebastian "Bash" Croft at the winner's table with Claudia Winkleman | yes: all four at the winner's table (Claudia, Romesh, Bash; the Patriot revealed) |
| 2 | Winner's table: a smaller table before the arch the banished players leave through | yes (half size, pedestal: note 1) |
| 3 | The Round Table in the opposite direction (as in The Traitors film) | yes: behind Romesh, shot 3; one space (Sam's note 5) |
| 4 | A stack of large gold coins on the winner's table | yes: about 7 tiers |
| 5 | Camera looks over the table at Claudia: "Romesh and Bash, remind us who you did this for?" | yes: shot 1, over the coins |
| 6 | Camera swivels to Bash: overwhelmed, emotional yet excited: "I did this for a wonderful organisation, they are called Choose Love. They help displaced people all over the world including queer refugees." | yes: shot 2, hands meet at his chest, eyes close on "wonderful", brows up |
| 7 | Camera swivels to Romesh: "I'm doing this for a cause that is very dear to my heart, it's the Refugee Council." | yes: shot 3, sincere, hands on the rim |
| 8 | Swivel to Claudia: "And what about you?" | yes: shot 4 (the swing back via Bash, never past 2 o'clock) |
| 9 | Only now we see a fourth person at the winner's table: The Patriot. His eyes widen | yes: shot 5, eyes widen at 26.4 s |
| 10 | The Patriot must NOT appear in shot before this moment | yes: kept out of every frame before 25.6 s (picture()) |
| 11 | "Errrrrrrrrrrrrrrr" uninterrupted, 15-20 s of the 40 s file, faded gently out; his eyes stay wide | yes: about 18 s of the file, the last 4 faded; stare grows 1 to 4, no blinks |
| 12 | During it: Claudia staring intently at him | yes: shot 6 |
| 13 | Bash staring at him and blinking | yes: shot 7, blinking |
| 14 | The Patriot staring sideways at Romesh | yes: shot 8, eyes slide, head still |
| 15 | Romesh and Bash moving their eyes towards each other | yes: shot 9 |
| 16 | Claudia staring, blinking | yes: shot 10, two blinks |
| 17 | The "errrr" slowly fades away; a moment of awkward silence | yes: shot 11 (silence kept, Sam 1 Nov) |
| 18 | The Patriot points at the other two contestants: "Traitors." | yes: shot 12, both arms, fingers (Sam's note 6); then shot 13, their reaction (my addition, Sam said yes) |
| 19 | No supershots, no sound effects | yes: voices only |
| 20 | Timing of shots and the awkward looks and eye moves carry the comedy | by the animatic: Sam to judge |

## References as checklists (guides/satire.md)
| reference | what it shows | ours matches? |
|---|------|------|
| 01 | Claudia behind the winner's table, front on: grey tweed jacket; arch behind with a lattice grille, red-lit panes; dark panelled walls; table top red-brown with a cream inlaid ring; coin pyramid about 7 tiers, more coins scattered round the base | |
| 02 | Claudia, three-quarter: the coin pile, the table's light rim and edge; dining room behind (not our set) | |
| 03 | The final as aired: Bash left (dark jacket, white shirt), Claudia centre (black jacket, cream high-neck blouse), Romesh right (rust-orange suit); all lean on the table with both hands; fire bowl bottom left; arch and lattice behind | |
| 04-05 | Romesh (check coat, CLEAR squarish glasses (not black: 1 Nov), curly hair, greying beard) and Bash (wavy brown hair, dark tartan suit, white shirt, open collar); both fists up, smiling; Claudia between (fringe, black jacket, white high neck) | |
| 06-08 | Bash speaking, close: hair over his brow, looking down; emotional, mouth open; hands pressed together at the chest, two silver rings | |
| 09 | Romesh at the table: rust suit, both hands on the table edge, head down; Bash and Claudia opposite | |
| 10 | Romesh over Bash's shoulder: wall torch in an iron cage behind him | |
| 11 | Claudia listening, happy: soft smile, head tilted, cream tie-neck blouse with a gold chain | |
| 12 | The room from above: arch at the end, round winner's table on a pedestal of turned legs with a lit ring at the floor, candles along both walls, torches in cages on both side walls, panelled walls | |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | | The winner's table 50% smaller: a pedestal with a flat top | done 1 Nov: top 0.65 m (`TABLE_RX/RY` halved), edge band, four turned legs round a central column, plinth with a lit ring; coin pile refitted to cover most of the top (ref 02); plan R 0.95 -> 0.6. Overhead ref: asked (ref 12 has no table) |
| 2 | 3 | 17 s | The Round Table through the opening behind Romesh floats | done 1 Nov: legs and a central base to the hall floor, a shadow under it, floor boards, chairs at N, E, S, W (`hall_chair`) |
| 3 | 1 | 0.9-1.6 s | voices.py's "words before Romesh" flag: false alarm, Claudia draws the name out | meant (no change); the "Errrr" flag (44 syllables heard, 1 written) is meant too: one held sound. voices.py has no way to mark a flag as meant, so both will show in pre-flight: read and pass them |
| 4 | all | | Reduce the table by another 25% | done 1 Nov: top 0.49 m (`TABLE_RX/RY` x 0.75), pedestal and pile scaled with it; plan R 0.52 |
| 5 | 3 | 17 s | Chairs tucked into the Round Table (they looked turned away); no wall between the two rooms (one space); the Round Table 50% closer | done 1 Nov: chairs round the far side seen front on with the rim over their seats, side chairs edge on with seats under the rim, the near one from behind; the opening's posts and lintel gone, the hall's wall up to the shared ceiling, one floor; the table about 5 m off (was 9.5): twice the size; plan: at z -4.6, opening the full wall |
| 6 | 12 | 47.9 s | The pointing must look like pointing (as at the end of Power Crime Action) | done 1 Nov: Power Crime Action's 'point' hand (a short finger out of the round hand, a touch bigger here), both arms straight, down at the two heads in the corners, drawn over the table (`install_point_finger`, `point_at_them`, `arms_mask`) |
| 7 | 2-4 | | Camera closer, at the edge of the table | done 1 Nov: zoom 1.2; the table and coins scaled about its far edge so its near rim sits at the frame's foot (`patriots4_room.Near`, `near_for`); hands still on the rim |
| 10 | all | | (animatic 1) The swings look like the table spinning, not the camera: jump cuts are fine | done 1 Nov: plain cuts (`PANS` empty; shots 2-5 held at their person, the table's edge) |
| 11 | 13 | 48.2 s | (animatic 1) No widening at the end: just looking at each other | done 1 Nov: no dropped mouths; eyes slide to each other at 48.6 s and hold |
| 12 | 11-12 | 44.8 s | (animatic 1) R and B appear suddenly in the pointing shot: camera out a little so they are always in shot | done 1 Nov: shots 11 and 12 share one framing (zoom 1.0), Bash's and Romesh's backs in the corners of both |
| 13 | all | | (animatic 1) Claudia is round-faced; she is thin-faced | done 1 Nov: cause found: her new face's jaw was pushed 15x to win the likeness scorer, and her hair curtains framed a wide block. Sam chose The Traitors film's Claudia face (`traitors_cast.claudia_head`), kept with this film's outfit |
| 14 | 1 | 0-7 s | Claudia's eyes move between Bash and Romesh | done 1 Nov: one look per phrase, Romesh / Bash / Romesh / Bash / Romesh (`claudia_asks`) |
| 15 | 2-13 | | Orange/blue bubble round the hands on the table | done 1 Nov: the patch copied back over the table was bigger than the hand (a rim of sleeve): now the hand only |
| 16 | 3 | | Romesh's glasses' lines flicker as he talks | done 1 Nov: thicker ink outline round the clear frames (5.8, was 4.0) |
| 17 | 5-11 | 26.4 s | The Patriot's eyes change style at the stare: keep the original | done 1 Nov: the stare drawn in the library's own eye style (almond, outline, lid line, straight brows), bigger as it grows; "Traitors." uses the library's fierce brows and lid |
| 18 | 9, 13 | 38 s | The frame between the rooms is back: one room, one wall style (REPEAT of note 5) | done 1 Nov: why the first fix failed: posts gone but the hall wall kept The Traitors film's style and met the room's wall at a hard edge, seen in shot 9 (I checked only shot 3). Now the far wall is this room's panels (`panels(..., k)`), the side walls turn the corner to it (`receding`); the hall lamps are gone (loss) |
| 19 | 13 | 49 s | "This is terrible" (the Patriot's foreground pointing arm) | done 1 Nov: removed (my addition); his shoulder stays in the corner |
| 9 | 12, 13 | 48 s | "We don't get to see R and B's reactions" | done 1 Nov: shot 13 (my proposal, Sam's yes) |
| 8 | 1, 5, 9, 11, 12 | | (sent mid-work) All the other table shots closer too: camera at the table's edge, no empty floor round it | done 1 Nov: same camera as 2-4 (close-ups 6, 7, 8, 10 already fill with table); shot 9 at 1.08 with Romesh and Bash cheated a little closer (230 and 253 degrees, was 227 and 256) so both fit, hands and all |

Decisions made (kept so a new chat never has to rediscover them):
- 1 Nov: Sam sent references and recordings under "hold"; the brief came with the Opus switch. Planning only until Sam says go.
