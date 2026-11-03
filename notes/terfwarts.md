# Notes for Terfwarts (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 41 (every arm ends in a hand), 18 (the Hat's face and GIRLS plaque 40 px+), 10 (Hook Text clear of the Hat's face)
- **Done:** cast sheet sent 3 Nov (`review/terfwarts-cast.jpg`): four turnarounds at real heights, McGonagall with the Hat, the run, Myrtle blocking, Harry's annoyance 1-6, faces.
- **Spent against the estimate (rule 55):** Sam's usage 58% at the start of the cast stage (target 10% for the film): well over; keep every step lean.
- **Next:** on Sam's yes and annoyance number: stills per shot, Opus medium, new chat. Sam types: "Terfwarts: make the stills".
- **Needs Sam:** Y/N on the cast; annoyance 1-6; the scream and splat sounds (before the animatic).
- **Read:** `guides/satire.md` Start step 4; rulebook Building table; `terfwarts_cast.py` MAP only.
- **Lost / Added:** Added (cast): Ron's satchel strap (ref), Myrtle's blue-and-bronze tie, a stand-in stool.
- **Open rule requests:** none
- **For Claude:** cast in `source/terfwarts_cast.py` (`person(img, cam, x, floor, s, who, yaw, j, extra, lift, head_props)`, `hat(p, cx, by, k, mood)`, `worn_hat(mood)`, Myrtle via `ghost`). `source/terfwarts.py` is the template copy: `cast` routes to the cast file; its STORY is still the template's. Harry's eyebrows show under the Hat only with the fringe at 0.46 hh.

## The joke (Sam, 3 Nov)
JK Rowling has spent years attacking the trans community and has put gender-exclusionary ideas into HBO's new Harry
Potter. Philosopher's Stone has the famous bathroom attack scene, and she is obsessed with the phantom danger of trans
people in bathrooms. The Sorting Hat calls out biological sex instead of Hogwarts houses. Myrtle blocks them from
saving Hermione with Rowling's own rhetoric. Ron is a gibbering fool who doesn't understand what's happening.

## Plan extras (rules 24-26, 54, 55)
| build or risky move | why (3D? parts the camera sees) | estimate (% of a week) | spent |
|---|---|---|---|
| Cast: Harry, Ron (one shared child body), McGonagall, Myrtle (see-through tint), the Hat | flat, front on; likeness by costume and hair unless Sam sends packs | 7% | cast built in one chat (Sam at 58% at its start) |
| Two flat paintings: Great Hall behind the close-up; cloister with the shrunk door and GIRLS plaque | rule 39, no 3D | 4% | |
| Moves: Hat placed, the run and panting halt (one rehearsal clip), Myrtle's glide to block the door | kit moves | 3% | |
| Voices, subtitles, two effects, bleep, assembly, renders | kit | 3% | |
| A round of Sam's notes | | 2% | |
| **Total** | re-estimated 3 Nov against past films (12-18%); the first figure, 69%, was not checked against them | **about 19% of a week** | |

Eyelines: Hall: Harry looks up at the Hat (annoyed). Door: Harry at Myrtle; Ron at nothing (vacant, gibbering); Myrtle
at Harry; "Ron, get it together" and "I don't like you, Ron": Harry turns to Ron.
Sound effects (rule 26): female scream (cut off suddenly), heavy splat, from behind the door. **Sam is finding them.**
Bleep (rule 27): "f******": Sam says the word, I bleep over it (method A, Sam: always).

## The world (rule 1)
Composition sheet sent: 3 Nov, review/terfwarts-composition.jpg

## The brief as a checklist (Sam, 3 Nov), ticked before the first animatic
| # | from the brief (word for word) | done? |
|---|------|------|
| 1 | All models based on the new HBO cast where possible | |
| 2 | Shot 1: Great Hall. Harry sits on the chair; the Sorting Hat is placed on his head | |
| 3 | Sorting Hat yells "BIOLOGICAL MALE." | |
| 4 | Harry reacts with annoyance | |
| 5 | Cut to Hogwarts corridor, subtitle "Later…" | |
| 6 | Harry and Ron race towards a Hogwarts interior door, shrunk so it looks like the entrance to a bathroom | |
| 7 | Moaning Myrtle appears through the door; Harry and Ron come to a panting halt | |
| 8 | Harry: "Myrtle, Hermione is under attack by a troll." | |
| 9 | Myrtle: "As a penis'd individual, you expect free license to conduct predatory behaviour inside a female-exclusive space." | |
| 10 | Harry: "What? No, Myrtle, you don't understand. Hermione could be killed at any moment." | |
| 11 | Myrtle: "Yes. By a man masquerading as a woman in a dress. I will not allow you to turn this space into a chapel of wanton molestation." | |
| 12 | Ron: "I don't like spiders, Harry." | |
| 13 | Harry (annoyed): "Ron, get it together, I'm sick of you already." | |
| 14 | Myrtle floats around to block the doorway: "When you throw open the door of a bathroom or changing room to any man so-called 'trying to save the life' of a woman, then you throw it open to anyone wanting to come inside" | |
| 15 | A scream, suddenly cut off by a heavy splat | |
| 16 | Harry: "Well it's not problem anymore Myrtle as she's f****** dead now." (six asterisks; wording as written, typo query asked) | |
| 17 | Myrtle: "Dead is a thought-terminating cliché" | |
| 18 | Ron: "I don't like them, Harry." | |
| 19 | Harry: "I don't like you, Ron." | |
| 20 | Sound effects: female scream, splat (and no others) | |
| 21 | Ron is a gibbering fool who doesn't understand what's happening | |
| 22 | Ends with the CranbriJoos sign-off (CLAUDE.md) | |
| 23 | Note 1: shot 1 brought forward so Harry and the Hat fill the frame; no long shots of the hall | |
| 25 | Note 2: Professor McGonagall (HBO series) puts the Hat onto Harry | |
| 24 | Note 1: the 3-second hook is the first joke, "BIOLOGICAL MALE", with a clear identification of what's in the frame | |

## References as checklists (`references/terfwarts/`)
| reference | what it shows | ours matches? |
|---|------|------|
| harry-hbo-clapper | HBO Harry: messy dark-brown hair, thin round wire glasses, pale, slight smile; black robe, maroon V-neck jumper with gold trim, white shirt, maroon-and-gold striped tie | |
| ron-hbo | HBO Ron: thick wavy ginger hair, round freckled face, small smirk; striped jumper (dark green neck) | |
| hermione-hbo | HBO Hermione: long, very bushy dark-brown hair, broad smile, olive skin; robe, white shirt, maroon striped tie | |
| sorting-hat-scene-1/2 | Great Hall: brown patched pointed hat over Harry's eyebrows; stool/chair; candles on long tables; tall leaded windows; stone walls; staff table behind | |
| sorting-hat-face | The Hat's face: folds make brow, eyes and a wide mouth near the base; brown suede, a torn patch on one side | |
| corridor | Fan-vaulted stone cloister (Gloucester): honey stone, tracery windows right, stone bench left, flagstones, arch at the far end | |
| troll-bathroom | The film's girls' bathroom: white tiles, cubicle doors left, sinks right, troll grey and huge | |
| myrtle-1/2/3 | Myrtle (film, Shirley Henderson look): see-through pale blue, dark bunches/pigtails with a fringe, round glasses, cardigan with buttons, striped tie | |
| harry-ron-hbo-pair | HBO Harry straight on (glasses, black hair over brow, robe, striped tie); Ron behind (ginger, satchel strap); Ron close, talking, three-quarter, red check shirt | |
| trio-hbo-cloister | The three in the cloister: dark plum-black robes to the shins, Ron shortest-looking with ginger crop, Hermione's long bushy hair; stone arcade, flagstones | |
| great-hall-hbo-students | HBO Great Hall: long tables with lamps both sides, students in the aisle, chequered floor, stained window over a pointed arch, banners | |
| great-hall-empty-candles | Empty Great Hall: hundreds of floating candles, gold walls, long tables and benches, eagle lectern | |
| great-hall-oxford | Christ Church hall (the real one): hammerbeam roof, portraits, big window at the end, wood panelling, table lamps | |
| mcgonagall-hbo | HBO McGonagall: tall, slim; dark grey hair swept up in a low bun with a side wave; thin dark rectangular glasses; dark red lips; long tailored blue-grey tartan coat, high black collar; carries a book with a white quill | |
| door-1/2 | Great Hall door: pointed stone arch with clustered columns, carved oak double doors in square panels with faces and crests, two ring handles | |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 2 | 1 | comp | McGonagall puts the Hat onto Harry (HBO reference sent) | open: planned as one shot, she stands behind Harry's shoulder and lowers the Hat (new kind) |
| 1 | 1 | comp | Bring shot 1 forward: Harry and the Hat fill the frame; no hall wide; the hook is "BIOLOGICAL MALE" in 3 s | done on the sheet: hall wide cut, the close-up opens the film (new kind) |

Decisions made:
- Sam, 3 Nov: Sam records all voices (always); bleeps always method A (word said, bleeped over); Sam finds the scream
  and splat; likeness from the photos sent (HBO Harry, Ron); Myrtle from the film look; Hermione and the troll off
  screen (may change); "it's not a problem anymore" (typo fixed); GIRLS plaque on the door: yes.
- Sam's note 1 (3 Nov): the film opens on the close-up; the Hat yells at about 0.5 s; Hook Text in the space above the Hat. Lost: the hall wide and the students.
- My picks (in the composition sheet): the Hat sits on Harry's head as the film opens (no one seen placing it); the
  boys run at the lens down the cloister; shot/reverse at the door; Myrtle's blocking glide ends arms spread.
- Sam, 3 Nov, "Y all": the layout approved; Harry, Ron and McGonagall recognisable by costume, hair and glasses (no likeness tool); McGonagall places the Hat.
- Rule requests (Sam, 3 Nov, "always" / "no need to ask in future"): proposed, waiting for his yes (see Open rule requests).
