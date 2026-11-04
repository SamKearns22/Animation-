# Notes for Islamocommunism (one file, numbered; mark each done as it is fixed)

## Where things stand
- **Rules that bite next:** 45 (the composition sheet is sent once: apply notes, never re-send), 74 (acting list before the first animatic), 14 (pre-flight gates)
- **Done:** White House front built and benchmarked 10/10; composition sheet sent 4 Nov. Office redressed (notes 5-6) and flat cameras chosen (note 4): `review/islamocommunism-office.jpg` sent 4 Nov.
- **Spent against the estimate (rule 55):** front, flag, cars, families about 1.5% (estimate 3.5); film so far about 5% of Sam's 8%.
- **Next:** Opus, medium effort, new chat: start the film code (composition notes 1-2 applied), the acting list and the stills. Type: "Islamocommunism: start the film".
- **Needs Sam:** the voice recordings (Voice Isolation off), due 5 Nov.
- **Read:** this file; guides/satire.md "Start" and "Staging and acting"; rulebook rule 74.
- **Lost / Added:** Lost: the right wing's windows sit behind the lawn flag; crosses on the spires (plain gold tips); the two gold chairs facing the Resolute desk (office). Added: clouds, mowing stripes, a picnic blanket, a ball, headscarves on two mothers; in the office: arched tiled window heads, star band on the valance, tiled dado, green carpet with a star-and-wheat seal, star on the desk front, two poster paintings for the portraits, a samovar and tea glasses, two brass lanterns, the new flags.
- **Open rule requests:** none.
- **For Claude:** office dressing `source/islamocommunism_office.py` (import it instead of midterminal_set; `door_cam()`, `TEST_CAMS` are the flat cameras); set `source/islamocommunism_set.py` (MAP at top; `paint(t)`, `comp`, `refs`, `test`; drawn 90 px high then dropped, `SHIFT`; Hook Text two rows at y 410: finish.py `--y 410`; `KEEP_CLEAR`); comp cameras in its `COMP` (Oval Office via `midterminal_set.put`/`put_seated`; side-on shot 4 sorts people before the desk); cast `source/islamocommunism_cast.py`; door/walk-in `midterminal_moves.py`. Film code not started: copy `satire_template.py` to `source/islamocommunism.py`, BENCHMARK from the set's list.

## Plan extras: ambition estimate (rules 24, 62). Compared with MidTerminal (11%, same Oval Office built new) and Terfwarts (9%).
| build or risky move | why | estimate (% of a week) | spent |
|---|---|---|---|
| White House front with Dome of the Rock gold dome and two St Basil's onion spires, lawn, fountain, red flower bed | new set, one locked camera, 3D not needed | 2.0 | 1.5 for these three rows |
| Red/green striped flag with hammer-and-sickle, crescent and star canton; on the roof and on a lawn pole, waving | new prop | 0.5 | |
| Flying cars in orderly queues; families and children playing on the lawn (small, far, simple loops) | new, background only | 1.0 | |
| Abdul El-Sayed likeness (front, side, back; seated, standing, holding phone and glass) | new cast | 1.5 | |
| Alexandria Ocasio-Cortez likeness (front, side, back; walking in, two glasses) | new cast | 1.5 | |
| Oval Office, door, walk-in, desk | reused from MidTerminal | 0.3 | |
| Clink, sips, animatic rounds | | 1.0 | |
| **Total** | | **7.8** (budget 8: tight) | |

Shots (about 40-45 s with the real voices):
1. Exterior wide, locked: cars streaming above, families on the lawn, both flags waving. Heading lower-middle-left: "USA", 1 s later "THREE YEARS INTO ISLAMIC COMMUNISM" beneath. About 5 s.
2. Oval Office wide: Abdul at the desk on the phone, sceptical (line 1). Door opens; Alexandria walks in with two mimosas (line 2). He stands (line 3).
3. Two-shot across the desk: she hands him a glass (lines 4-5), sips in silence, the dialogue run (6-12).
4. Closer two-shot for the button: "Invade Europe?" / "Invade Europe." Clink.

## The brief as a checklist (CLAUDE.md, 18 Oct)
| # | from the brief or a note (word for word) | done? |
|---|------|------|
| 1 | The White House front. It now has the dome of an Islamic Mosque alongside two Kremlin spires. | set: yes (4 Nov) |
| 2 | Two flags clearly visible, one above the entrance and one flying on a flagpole in the grounds. | set: yes, both wave |
| 3 | Red/Green striped American flag with the stars replaced by communist hammers and sickles, Islamic crescent moons and stars. | set: yes (13 stripes; navy canton, 3 of each emblem) |
| 4 | Flying cars streak in orderly queues in the skies above | set: yes (4 lanes, even spacing, speed streaks) |
| 5 | children and happy families laugh and play on the lawn | set: yes (6 groups, simple loops) |
| 6 | White heading text in the lower middle left: "USA"; 1 second later revealing beneath: "THREE YEARS INTO ISLAMIC COMMUNISM" | |
| 7 | Cut to inside the Oval Office. Abdul sat behind the desk, eyes looking sceptically at the phone he is holding to his ear. | |
| 8 | ABDUL: "Really? All diseases? Guess I don't need to call myself 'Doctor' any more." | |
| 9 | Alexandria comes through the door holding two champagne flutes, mimosas. ALEX: "President El-Sayed?" | |
| 10 | El-Sayed stands. "Good morning, Also-President Ocasio-Cortez. What do you have for me?" | |
| 11 | Alex walks to the desk. "Non-alcoholic mimosa. I figured we deserved a slow morning after we finally solved climate change." | |
| 12 | He takes the glass and chuckles. "Mashallah, it's a fine day to be a comrade." | |
| 13 | They both sip in the sun-dappled silence, smiling contentedly. | |
| 14 | ABDUL: "You know, Madam President, when we decided to combine the spiritual philosophy of Islam with the Socio-Economic doctrine of communism, I didn't expect it would work so perfectly." | |
| 15 | Alex shrugs. "Me neither. But here we are, American dream solved." | |
| 16 | ABDUL: "No suffering." | |
| 17 | ALEX: "Free everything paired inexplicably with total abundance." | |
| 18 | ABDUL: "It's crazy that nobody had suggested trying it before." | |
| 19 | A small pause. | |
| 20 | ABDUL: "So, what's next for our great American experiment?" | |
| 21 | ALEX (hopefully): "Invade Europe?" | |
| 22 | Abdul chuckles. "Invade Europe." They clink glasses. | |
| 23 | Hook Text + CranbriJoos sign-off (finish.py) on every animatic and the final. | |

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| White House front (2 photos) | white north portico, 4 columns + pediment, 4 windows each side at two storeys (my first note said 3), balustrade roof, flag on roof centre, round fountain, red flower ring, hedges, big trees both sides | yes, all (refs sheet 4 Nov) |
| Hammer and sickle | gold hammer crossing sickle, gold-outlined red star above, on red | yes, gold on the navy canton; no star above (the crescents carry the stars) |
| Crescent and star | pale crescent opening right, five-point star in its mouth, on green | yes, white on the navy canton |
| Abdul El-Sayed (2 photos) | dark suit, open white shirt no tie, short dark slicked-back hair, full short beard and moustache, flag pin, white pocket square | |
| Alexandria Ocasio-Cortez (2 photos) | long dark straight hair centre parting, black jacket, red lipstick, pearl earrings (official portrait); blush top, burgundy skirt (casual) | |
| St Basil's (Kremlin spires) | striped and diamond onion domes, red/green/blue/gold, tented red tower | yes: blue/white and green/gold/red twisted onions on red brick towers; no tented tower, no crosses |
| Dome of the Rock | big gold dome on a blue-tiled drum | yes, crescent finial |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | 1 | all | Lawn flag over the right wing: Y. "The flag should be 180'd": turned round on its pole, both flags now fly right, starry corner top left | done 4 Nov |
| 2 | 1 | 0-3.6 | Hook Text two rows in the sky: Y | done |
| 3 | 1 | all | "The back flag is too big, doesn't look proportional" (the roof flag): checked against both White House photos, the real one is small atop a tall thin pole; 150x86 px to 96x55, pole thinner | done 4 Nov |
| 4 | 2-4 | all | "Please do flat shots only, no wide 3D views": every Oval Office shot is level and square on (front on to the desk end, square on to the door), long lens; no angled or wide views. Composition shots 2-4 re-framed this way | cameras chosen 4 Nov (office sheet); film code next |
| 5 | 2-4 | all | "Make the MidTerminal Oval Office respectfully communist and Islamic": Islamic geometry, arches, tiles, lanterns, a samovar; red stars and wheat; no holy writing, no religious figures, no real portraits. Built as its own file so MidTerminal's room is unchanged | done 4 Nov, sheet sent |
| 6 | 2-4 | all | "And change the flag": the room's US flag is now the film's red/green flag; the President's flag a red banner with a gold crescent and star; crescent finials | done 4 Nov |

Composition sheet sent: 4 Nov, review/islamocommunism-composition.jpg (4 key shots: outside with Hook Text and heading; Oval Office wide, Abdul seated, Alex at the door; across the desk; side-on two-shot for the clink)

Decisions made:
- Hook Text: "MAGAs Worst Nightmare" (Sam, 4 Nov).
- Clothes: El-Sayed charcoal suit, open collar, pocket square, flag pin; AOC black jacket, red lips, pearls (Sam's Y).
- Hair (Sam, 4 Nov: "Abdul's too big, almost hat-like; Alex's wavier and thicker, a bit straighter"): his cropped close to the skull; hers a full curtain each side, waves growing to the ends.
- Likeness check 4 Nov: El-Sayed 60% (on 107e061d; re-based onto patriots4's average), AOC 68% (on 0019c908). Aim 60%+.
- Facial hair (Sam, 4 Nov, close-up 18d7e6e5: "a thin black moustache and a small black goatee. He is quite a handsome man"): full beard removed; thin moustache, goatee from the lower lip round the chin, faint jaw shadow; eyes opened a little. Likeness now 57% (was 60% with the full beard; the check reads moustaches poorly).
- Beard, round 3 (Sam: "do you not see the thin beard around his chin and lower cheeks?"; "not anywhere near that thick, nor up to the top of the ears"). Why the first fix failed: I followed the words of the note ("moustache and goatee") and dropped the beard the photos show. Now checked against all six of his refs: a short narrow jaw beard from mid-ear, joined to the thin moustache at the mouth corners, soul patch; face leaner. Likeness 41% (the meter misreads beards; judged by eye beside every ref).
- Rule request (Sam, 4 Nov: "Always check every reference, don't just reply to my words"): written as rule 76 (Sam's Y, 4 Nov).
- Cast approved (Sam's YY, 4 Nov); brows then straightened and thickened to match his refs.
- Cast code: `source/islamocommunism_cast.py` (measured heads; AOC hair 'aoc_long' for side/back).
- Phone is the desk handset (the Resolute desk already has phones).
- White House (4 Nov, my picks): one painting for the locked camera (rule 39). Wind from the left, both flags fly right (Sam's note 1, 4 Nov: "the flag should be 180'd"; first they flew left, seen from the back). The lawn flag's pole stands right of the fountain, the flag in front of the right wing (clearest against the white front). Hook Text two rows in the sky at y 410 (one row will not fit the safe width); the set sits 90 px lower so it clears the dome. Heading "USA" lower-left at y 1270-1490 over the lawn, white with a black edge (Anton).

