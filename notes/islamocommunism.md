# Notes for Islamocommunism (one file, numbered; mark each done as it is fixed)

## Where things stand
- **Rules that bite next:** 55 (spent vs estimate), P8 (check sheet before every animatic), 74 (acting list)
- **Done (5 Nov):** final rendered and sent: `animations/islamocommunism-vertical.mp4` (73 s, 7.8 MB, 12 fps). Week's usage 100% at the end.
- **Next:** Sam posts it. Then the end-of-project rule write-ups below (new chat, Opus), only when credits allow.
- **Needs Sam:** nothing.
- **Read:** this file's notes 8-19.
- **Open rule requests:** (a) body weight and surfaces, limb extension (Sam, 4 Nov; photo reference). (b) the acting-list guide should plan each line's shot, use the quality tools and ask the questions that carry the script's meaning (Sam, 4 Nov). (c) lesson: do not say a change "looks right" from a thumbnail; look at full size and say what is seen. (d) lesson: a shallow copy of a pose shares its nested dicts (the hand bug). (e) people exactly square to the lens sit on the drawing's mirror line: nudge them 0.3 degrees (`MS.to_cam`). Wording for each to be proposed to Sam first.
- **Faults named to Sam (final):** three subtitles on screen about 1.1 s; the 12 s close-up on line 6 (chosen); mouth check on "You know," and "Invade Europe." (the check's syllable count); hand checks on the desk arm and phone hand; the clink "turned" flag (false); a small hop of the handset as he rises.
- **For Claude:** film `source/islamocommunism.py`; cuts `cut_of(t)`; `PHRASES` (mouth and subtitles per pause); `desk_arm_item`, `phone_item`, `handset_k`; sound: voices + clink + slurp + anthem (`_anthem`).

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
| 6 | White heading text in the lower middle left: "USA"; 1 second later revealing beneath: "THREE YEARS INTO ISLAMIC COMMUNISM" | yes: 0.6 s / 1.6 s |
| 7 | Cut to inside the Oval Office. Abdul sat behind the desk, eyes looking sceptically at the phone he is holding to his ear. | yes: shot 2, front on, handset at his ear, eyes to it |
| 8 | ABDUL: "Really? All diseases? Guess I don't need to call myself 'Doctor' any more." | yes (est. timing till the take) |
| 9 | Alexandria comes through the door holding two champagne flutes, mimosas. ALEX: "President El-Sayed?" | yes: shot 3, square on to the door, two mimosas |
| 10 | El-Sayed stands. "Good morning, Also-President Ocasio-Cortez. What do you have for me?" | yes: he rises (1.6 s), then the line |
| 11 | Alex walks to the desk. "Non-alcoholic mimosa. I figured we deserved a slow morning after we finally solved climate change." | yes: walks in from the right to the desk end |
| 12 | He takes the glass and chuckles. "Mashallah, it's a fine day to be a comrade." | yes: takes it from her hand, chuckle, line |
| 13 | They both sip in the sun-dappled silence, smiling contentedly. | yes: both sip 2.4 s, eyes half shut, smiling |
| 14 | ABDUL: "You know, Madam President, when we decided to combine the spiritual philosophy of Islam with the Socio-Economic doctrine of communism, I didn't expect it would work so perfectly." | yes |
| 15 | Alex shrugs. "Me neither. But here we are, American dream solved." | yes: shrug on "Me neither" |
| 16 | ABDUL: "No suffering." | yes |
| 17 | ALEX: "Free everything paired inexplicably with total abundance." | yes |
| 18 | ABDUL: "It's crazy that nobody had suggested trying it before." | yes |
| 19 | A small pause. | yes: 0.9 s, then the cut |
| 20 | ABDUL: "So, what's next for our great American experiment?" | yes: shot 6, closer |
| 21 | ALEX (hopefully): "Invade Europe?" | yes: brows up |
| 22 | Abdul chuckles. "Invade Europe." They clink glasses. | yes: chuckle, line, clink |
| 23 | Hook Text + CranbriJoos sign-off (finish.py) on every animatic and the final. | finish.py on every animatic (none yet) |

## Acting (rule 74; front on at their marks, rule 38; every shot flat, note 4)
| line | who | face | body | lands on |
|---|---|---|---|---|
| 1 "Really? All diseases?..." | Abdul | sceptic (one brow up), eyes to the handset; dry half-smile from "Guess" | seated, handset at his right ear; small head tilt | "All"; "Guess" |
| (hang-up) | Abdul | | handset down to the desk, 0.45 s | after line 1 |
| 2 "President El-Sayed?" | Alex | bright smile, eyes off left to him | through the door, two flutes held up at the waist, stops a metre in | the door opening |
| 3 "Good morning..." | Abdul | warm smile to the door side | rises (1.6 s) then speaks; open palm out | "What do you have for me?" |
| 4 "Non-alcoholic mimosa..." | Alex | smile, eyes on him | walks in from the right to the desk end; holds his glass out | "after we finally solved..." |
| (row 12) | Abdul | smile | takes the glass, a small chuckle (head bob) | before line 5 |
| 5 "Mashallah..." | Abdul | smile | glass at the waist | |
| (row 13) | both | eyes half shut, contented, looking out | both sip, 2.4 s of silence | |
| 6 "You know, Madam President..." | Abdul | smile, eyes on her | free hand open, palm up | "when we decided ... communism" |
| 7 "Me neither..." | Alex | flat, then smile | shrug: shoulders up, free palm out | "Me neither" |
| 8 "No suffering." | Abdul | calm, satisfied | still | |
| 9 "Free everything..." | Alex | smile | free hand sweeps open | "total abundance" |
| 10 "It's crazy..." | Abdul | smile | slow small head shake of wonder | |
| (row 19) | both | smiles | 0.9 s hold, cut | |
| 11 "So, what's next..." | Abdul | thinking, eyes up and away, then to her | still | "great American experiment" |
| 12 "Invade Europe?" | Alex | hopeful, brows up | glass now in the hand nearer him | |
| 13 "Invade Europe." | Abdul | smile | chuckle, then the clink: glasses meet over the desk corner | the clink after the line |

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
| 7 | 2-6 | all | "Change her out to this one so she stands out next to Abdul" (photos 436824a4, 4833f72c): white suit, jacket and trousers, ivory V-neck top, gold lapel pin, small gold earrings. Checked against both photos: they also show her hair pulled back (asked: Q1) | done 4 Nov, sheet sent |

Composition sheet sent: 4 Nov, review/islamocommunism-composition.jpg (4 key shots: outside with Hook Text and heading; Oval Office wide, Abdul seated, Alex at the door; across the desk; side-on two-shot for the clink)

Decisions made:
- Hook Text: "MAGAs Worst Nightmare" (Sam, 4 Nov).
- Clothes: El-Sayed charcoal suit, open collar, pocket square, flag pin; AOC white suit, ivory top, gold pin and earrings, red lips (Sam's note 7, 4 Nov; was black with pearls).
- Hair (Sam, 4 Nov: "Abdul's too big, almost hat-like; Alex's wavier and thicker, a bit straighter"): his cropped close to the skull; hers a full curtain each side, waves growing to the ends.
- Likeness check 4 Nov: El-Sayed 60% (on 107e061d; re-based onto patriots4's average), AOC 68% (on 0019c908). Aim 60%+.
- Facial hair (Sam, 4 Nov, close-up 18d7e6e5: "a thin black moustache and a small black goatee. He is quite a handsome man"): full beard removed; thin moustache, goatee from the lower lip round the chin, faint jaw shadow; eyes opened a little. Likeness now 57% (was 60% with the full beard; the check reads moustaches poorly).
- Beard, round 3 (Sam: "do you not see the thin beard around his chin and lower cheeks?"; "not anywhere near that thick, nor up to the top of the ears"). Why the first fix failed: I followed the words of the note ("moustache and goatee") and dropped the beard the photos show. Now checked against all six of his refs: a short narrow jaw beard from mid-ear, joined to the thin moustache at the mouth corners, soul patch; face leaner. Likeness 41% (the meter misreads beards; judged by eye beside every ref).
- Rule request (Sam, 4 Nov: "Always check every reference, don't just reply to my words"): written as rule 76 (Sam's Y, 4 Nov).
- Cast approved (Sam's YY, 4 Nov); brows then straightened and thickened to match his refs.
- Cast code: `source/islamocommunism_cast.py` (measured heads; AOC hair 'aoc_long' for side/back).
- Phone is the desk handset (the Resolute desk already has phones).
- White House (4 Nov, my picks): one painting for the locked camera (rule 39). Wind from the left, both flags fly right (Sam's note 1, 4 Nov: "the flag should be 180'd"; first they flew left, seen from the back). The lawn flag's pole stands right of the fountain, the flag in front of the right wing (clearest against the white front). Hook Text two rows in the sky at y 410 (one row will not fit the safe width); the set sits 90 px lower so it clears the dome. Heading "USA" lower-left at y 1270-1490 over the lawn, white with a black edge (Anton).
| 8 | 1 | 0-5 | Heading text bigger | done 4 Nov (USA 156, rows 68) |
| 9 | 5 | 24.5-25.5 | He took the glass with the far hand; it jumped | done: front-on people sat on the drawing's mirror line, rounding drew him mirror-image in the wide shot; fixed for everyone. Missed because the handover touch check could not find the hand ("not in the scene") and I named that as paperwork |
| 10 | 4 | 13.4-15 | Rise: no lean and sink first | done |
| 11 | 2 | 5-10 | Free arm forward, resting on the desk top (two notes) | done: drawn again after the desk |
| 12 | 5 | 25-31 | Close on him for "Mashallah", then both closer for the sip | done (the upright frame limits how close a two-shot can be) |
| 13 | 5 | 28.8-31.2 | Sip tilt halved | done |
| 14 | 5 | line 8 | "No poverty." | done |
| 15 | all | | Brow and head moves on key words | done (BEATS) |
| 16 | 2 | 9.9-10.4 | HELD (do at the audio render): when he puts the phone down his hand goes into the table and disappears. Plan: a desk phone base on the desk top at his right; the handset lands on it with his hand above the desk top throughout. Added: the phone base | held |
| 17 | 6 | 'Invade Europe?' | HELD: Alex even more excited. Plan: brows higher and wider eyes, bigger smile, a lift and small bounce on "Europe" (still bright and hopeful, like a picnic idea) | held |
| 18 | 4 | rise | HELD: his rise 50% faster. Plan: 1.6 s becomes about 1.07 s; line 3 and the cuts after it move earlier by about half a second, so the film is half a second shorter | held |
| 19 | 2 | 11.6-15 | Phone put down: two hands, handset vanished and slid into the base | fixed 5 Nov: the overlay's comparison copy shared the hand settings (switched his real hand on beside the handset's own); one owner for hand and handset until the rise; hand ends higher so the handset rests on top. Lesson: a shallow copy of a pose shares its nested dicts |

## Acting questions (rule 74, Sam 4 Nov: Y to all)
1. Tone: totally sincere and wholesome, no wink. 2. "Doctor": dry half-smile, faintly put out. 3. "Invade Europe?": bright, hopeful, like a picnic idea. 4. "Invade Europe.": instant warm agreement, then the clink in the two-shot.
