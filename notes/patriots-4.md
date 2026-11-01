# Notes for Patriots 4 (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/patriots-4-handovers.md)
- **Done (1 Nov, planning, Opus):** brief, 12 reference pictures (`references/patriots-4/`) and 6 recordings
  (`source/audio/patriots4-*.m4a`) filed and measured; plan below; questions sent to Sam in one message.
- **Done (1 Nov, later):** Sam's answers in; plan in metres (`source/patriots4_plan.py`); rough composition sheet sent
  (`source/patriots4_compose.py`).
- **Next:** Sam's notes on the sheet and his GO; then BUILDING (Opus high, fresh chat): Romesh and Bash likeness heads
  and the cast sheet, the winner's room, the film file from the template.
- **Losses and my additions Sam should know about:** none yet (proposed additions are in the questions).
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** this file; `guides/satire.md`; `source/traitors.py` (`wall`, `round_table`), `source/traitors_cast.py`
  (Claudia), `source/patriots3_cast.py` (`PATRIOT`).

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

Composition sheet sent: 1 Nov, review/patriots4-composition.jpg (`python3 source/patriots4_compose.py OUT.jpg`)

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
| 04-05 | Romesh (check coat, black rectangular glasses, curly hair, greying beard) and Bash (wavy brown hair, dark tartan suit, white shirt, open collar); both fists up, smiling; Claudia between (fringe, black jacket, white high neck) | |
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
