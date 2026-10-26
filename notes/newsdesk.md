# Notes for Newsdesk (working name; Sam's new untitled film, 26 Oct)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/newsdesk-handovers.md)
- **Done (26 Oct, building chat, Opus high):** Sam asked for five builds before any script. Built three:
  1. the Israeli TV news studio, in 3D (`source/newsdesk_set.py`): any camera; four test cameras in `CAMS`;
  2. a news presenter, an original man of the type (`source/newsdesk_cast.py`, `PRESENTER`): every view, seated at
     the desk, on-air / grave / sign-off / talking faces;
  3. the chairs: curved-back wooden armchairs on blue spotlight pools (`source/newsdesk_props.py`).
  4. Netanyahu, satire caricature from Sam's four photos (`source/netanyahu_cast.py`): every view, blue and red ties,
     flag pin; at rest, stern, shouting, talking, smug. (Claude first wrongly refused him; Sam pointed out the series'
     other politicians.)
  5. Darth Maul, satire parody from Sam's six photos (`source/maul_cast.py`, `MAUL`, `MAUL_HOOD`): every view hood
     down and up; the glare, snarl, talking; the double-bladed lightsaber (`saberstaff`, either blade on or off) and
     four poses (`pose('stand' | 'present' | 'attack' | 'strike')`). (Claude first refused him; Sam sent photos and
     asked again, and the series already parodies film characters: Andrew the Hutt.) Awaiting Sam's notes on the sheet.
- **Next (planning, Opus high, fresh chat):** Sam's brief or script for the film. Then the plan in metres (rule 1),
  the shots, the cast sheet with whoever else is in it, and questions in one message.
- **Losses and my additions Sam should know about:** see "Additions" below (all set dressing; say no to any).
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** `python3 source/newsdesk_set.py test OUT.jpg` (the set, four cameras), `... refs OUT.jpg` (Sam's
  photos beside ours), `python3 source/newsdesk_cast.py sheet OUT.jpg` (the presenter), `python3
  source/newsdesk_props.py sheet OUT.jpg` (the chairs), `python3 source/maul_cast.py sheet OUT.jpg` and `... faces
  OUT.jpg` (Maul).

## Sam's request (26 Oct, word for word)
"Please build the following for a new untitled film: 1. Israeli TV set 2. Darth Maul (standing still in cloak and in
attack mode with lightsaber) 3. Benjamin Netanyahu 4. A believable Israeli tv presenter, male, from these mixed images
5. Props: The chairs."

| # | from the request | done? |
|---|------|------|
| 1 | Israeli TV set | built: `newsdesk_set.py` |
| 2 | Darth Maul, standing in cloak and attacking with lightsaber | built: `maul_cast.py` (standing hooded in cloak; lunge and strike) |
| 3 | Benjamin Netanyahu | built: `netanyahu_cast.py` |
| 4 | a believable Israeli TV presenter, male, from the mixed images | built: original, resembles none of the three |
| 5 | props: the chairs | built: `newsdesk_props.py` |

## The world (rule 1)
Plan in `newsdesk_set.py` (x east, z north, y up, metres): studio x -7..7, z -4..8, ceiling 4.6; newsroom behind
glass x -7..-2.5, z 8..12. Floor graphic centred (0, 1.2), radius 2.0. Desk ring: radii 2.15-2.72, 0.8 m high,
from -24 to 204 degrees (open towards the cameras). Chairs at radius 3.05; the presenter's seat at (0, 4.15) facing
south. A film module adds `PLAN` (ROOMS and OPENINGS are already there) and its own cameras.

## References as checklists (`references/newsdesk/`; `python3 source/newsdesk_set.py refs OUT.jpg`)
Studio (`set-1-wide-desk.jpg`, `set-2-desk-front.jpg`): what makes it, and how ours has it (BENCHMARK, rule 3)
| what makes the place | ours |
|---|---|
| glossy black floor | done: near-black floor, flat streaks for the reflections |
| round floor graphic: blue centre, navy band, thin red ring, pale arcs | done |
| the channel's name on the floor | done: our own mark, 'חדשות' (News) and a white wave in a blue circle; no real channel |
| a huge curved ring desk, open towards the cameras | done: 228 degrees of ring, white end caps |
| thick white desk top; blue front with a lighter band | done |
| black mesh high-back chairs behind the desk | done: five |
| tall blue screen with a soft swirl and a white upright bar | done, captioned 'משדר מיוחד' (Special Broadcast) |
| navy back wall with a row of short white ticks | done |
| white pillars, red light down their edges | done: two pillars, plus a red strip in the far left corner |
| glass to the newsroom behind (desks, monitors, red and blue screens) | done |
| dark ceiling, lighting grid, spotlights | done |
| studio camera, floor monitor | done |
| differences left: the photo's light grey-white panels on the right wall and its bright reflections | left out: navy panels (flat house style; no glows) |

Presenter (`presenter-1..3.jpg`): the type, never a face
| the refs show | ours |
|---|---|
| navy or charcoal suit, white shirt, dark tie | navy suit, white shirt, deep burgundy tie with a fine stripe |
| dark-framed glasses (2 of 3) | slim tortoiseshell rounded rectangles |
| trimmed dark beard (2 of 3) | a close-cropped beard along the jaw, joined moustache |
| clip mic on the tie | done, with its lead |
| level, serious on-air face | on-air default; grave and sign-off faces |
| his own (resembles none of them) | long narrow face, high forehead, wavy hair pushed back, heavy straight brows, hazel eyes, a little grey at the temples |

Netanyahu (`netanyahu-1..4`): compared with `compare.py` on the front photo
| the photos show | ours |
|---|---|
| thick white hair combed back, side parting, receded temples | done |
| long face, heavy lower half, soft chin | done |
| hooded eyes, bags, grey brows low and straight | done |
| long broad nose, fleshy wings | done |
| wide thin-lipped mouth, deep folds past the corners | done |
| navy suit, white shirt, blue or red tie, flag pin on his left lapel | done (both ties) |
| unsure | the three-quarter and side heads come from the shared side-view drawing: hair and colours are his, the face details are simpler |

Maul (`references/maul/maul-1..6`): face compared with `compare.py` on `maul-6-face.jpg`
| the photos show | ours |
|---|---|
| bald, a ring of short pale horns round the crown | done (6 at the front, a ring of 7 from behind) |
| red skin; black mask round the eyes to the temples; forehead stripe and flames; cheek stripes; black nose tip and lips; black chin with two red stripes | done |
| yellow eyes, orange ring, red rims, no brows | done (the lids make the glare) |
| pointed ears | done |
| black hooded cloak, wrap tunic, wide sash with a strap, pleated skirts, black gloves and boots | done, hood up and down |
| high black collar, no skin at the throat | done |
| double-bladed red lightsaber, held in the middle; one blade lit in ref 1 | done: hilt 0.56 m, blades 0.65 m each (measured on ref 2; added to `sizes.py`) |
| ref 3: the snarl, the staff level in a low stance | done (snarl face; 'attack' pose) |
| unsure | the three-quarter and side faces carry less paint than the front (kept readable at that size); the markings are simplified, not stroke-for-stroke |

Chairs (`chairs-1.jpg`)
| the photo shows | ours |
|---|---|
| two identical chairs side by side, facing us | done |
| curved top rail wrapping into the arms, deepest at the back | done |
| warm teak, four round legs, front legs carry the arm ends | done |
| tan leather seat | done |
| each in its own oval of blue spotlight on black | done, with a darker shadow under each |
| left out | the legs' taper and splay (kept straight: cleaner in the house style) |

## Additions (my own: say no to any)
The channel mark and the two Hebrew captions; people at work in the newsroom (simple blocks, far away); the studio
camera and floor monitor; the red strip in the far left corner; the clip mic's lead; the grey at the presenter's
temples; the shadow under each chair. Maul: the 'strike' pose (staff raised to cut; not in the photos); flat
blades with an ink outline and no glow (house style; the Poker Mon soft glow is there if you'd rather).

## Checks run (26 Oct)
- Line work (`python3 source/linecheck.py newsdesk_cast`): presenter and chair clean; `maul_cast`: clean.
- Sizes: presenter 1.80 m; desk 0.8 m (sitting height); chair 0.76 m beside the 1.75 m person; both added to
  `sizes.py` ('wooden armchair', 'news desk').
- Not run yet (no film module or script): pre-flight, plan check, benchmark.py (done by hand above).

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 |      |      |      | open   |

Decisions made:
- The set's channel is invented; no real broadcaster's name, logo or lettering.
- The presenter is an original person blended from the type; he is not any of the three reference presenters.
