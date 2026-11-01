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
- **Next (READING SAM'S NOTES on the stills, Opus MEDIUM, fresh chat):** take Sam's notes in one batch; apply them
  (building from a clear plan: Opus medium). Then pre-flight (`python3 source/preflight.py patriots4 OUT_DIR`: the
  brief checklist must be ticked first; `scene(t)`, `layers(t)` and the audits are NOT yet written: copy the
  template's flat `scene()` and add them), the check sheet, and the animatic only on Sam's clear yes.
- **Open questions for Sam (asked 1 Nov):** (1) voices.py hears about 3 syllables before "Romesh" in Claudia's first
  recording (0.9-1.6 s) that no script word covers: is there an extra word, or is she just slow? (2) the dead silence
  before the "Errrr" (25.8 s) and after it fades (44.8 s): meant (brief 17), recommended: keep. The "Errrr" itself is
  flagged by voices.py (44 syllables heard, 1 written): meant, one held sound.
- **Losses, cheats and my additions:** shot 9 is a film cheat: Romesh and Bash are drawn closer together (227 and 256
  degrees, not 210 and 270) so both faces are big enough for the eye slide; shot 12 shows the backs of Bash's and
  Romesh's heads in the bottom corners so the Patriot's two-armed point has targets (addition); the Patriot's hands are
  circles (no pointing finger: house style). Set dressing from the refs only (fire baskets, torches, candles, lantern
  look); no signs or jokes of mine. Bash's two silver rings not drawn yet.
- **Usage (rule 44):** 7% of the week at the cast round (3% at the start); ask Sam again at this handover.
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
| 1 | Celebrity Traitors final 2026: winners Romesh Ranganathan and Sebastian "Bash" Croft at the winner's table with Claudia Winkleman | |
| 2 | Winner's table: a smaller table before the arch the banished players leave through | |
| 3 | The Round Table in the opposite direction (as in The Traitors film) | |
| 4 | A stack of large gold coins on the winner's table | |
| 5 | Camera looks over the table at Claudia: "Romesh and Bash, remind us who you did this for?" | |
| 6 | Camera swivels to Bash: overwhelmed, emotional yet excited: "I did this for a wonderful organisation, they are called Choose Love. They help displaced people all over the world including queer refugees." | |
| 7 | Camera swivels to Romesh: "I'm doing this for a cause that is very dear to my heart, it's the Refugee Council." | |
| 8 | Swivel to Claudia: "And what about you?" | |
| 9 | Only now we see a fourth person at the winner's table: The Patriot. His eyes widen | |
| 10 | The Patriot must NOT appear in shot before this moment | |
| 11 | "Errrrrrrrrrrrrrrr" uninterrupted, 15-20 s of the 40 s file, faded gently out; his eyes stay wide | |
| 12 | During it: Claudia staring intently at him | |
| 13 | Bash staring at him and blinking | |
| 14 | The Patriot staring sideways at Romesh | |
| 15 | Romesh and Bash moving their eyes towards each other | |
| 16 | Claudia staring, blinking | |
| 17 | The "errrr" slowly fades away; a moment of awkward silence | |
| 18 | The Patriot points at the other two contestants: "Traitors." | |
| 19 | No supershots, no sound effects | |
| 20 | Timing of shots and the awkward looks and eye moves carry the comedy | |

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

Decisions made (kept so a new chat never has to rediscover them):
- 1 Nov: Sam sent references and recordings under "hold"; the brief came with the Opus switch. Planning only until Sam says go.
