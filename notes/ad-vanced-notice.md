# Notes for Ad-Vanced Notice (one file, numbered; mark each done as it is fixed)

## Where things stand
- **Rules that bite next:** 3 (each place ticked against its photos: `benchmark.py ad_vanced_notice_sets`), 40 (showstopper list ticked at the first rehearsal clip), 54 (only deck pieces and the funnel top break off; the hull stays whole)
- **Done (8 Nov):** all four sets built as flat paintings at real size (study, cliff and strait, close-up background, gas station) plus the tanker and pickup props; every place's list ticked; sizes check clean. Sent Sam: the set sheet, the reference sheet, a 6 s clip of the fire and the sailing tanker.
- **Next:** wait for Sam's Y/N on the sets. Then fresh chat, Opus high effort. Type: "Ad-Vanced Notice: join the arms to the shoulders (note 14, all films). Read notes/ad-vanced-notice.md". After that, the showstopper (Opus high).
- **Needs Sam:** Y/N on the sets (notes 15-16 below list what I added); his number on R1; the rest of the script; the Hook Text wording later.
- **Read:** this file (Where things stand, notes 14-16, the showstopper list); `guides/figure-rig.md` (arms) for note 14.
- **Open rule requests:** R1 (below the notes), not yet written; rule 80 is now taken by the sitting kit, so R1 would become 81.
- **For Claude:** sets in `source/ad_vanced_notice_sets.py` (MAP at the top; `BENCHMARK`, `PROP_SIZES`, `SHOTS`, `picture(t)` there for benchmark.py/sheet.py; the film file imports them). Study: `study_back(t)`, `study_pose(j)` (no kit chair or desk; desk top drawn between body and arms), `study_front()`, Vance at `STUDY_VANCE`. Strait: `strait(which, t, near=('sail'|'wreck', x), fx=fn)`, `near_x(t, t_hit)`, `X_HIT`, `place_cliff`, `cliff_shadow`, cameras `CAMS`. Gas: `gas_back()`, `gas_front()`, `place_gas`, `MAN_X`/`VANCE_X`, `gas_points()` (filler, hose_from, board box for KEEP_CLEAR). Arms: `burnham.arm`, `limbs.py`.

## Plan extras: ambition estimate (rules 24, 54, 55, 62)
Compared with MidTerminal (11%: one new room, two people), Islamocommunism (estimate 7.8%: one new set, two likenesses) and Flying Whales (45%: a whale and a 31-piece rig wreck built from nothing). This film reuses Flying Whales' sea and effects, so the showstopper costs a fraction of that.
All flat paintings, one per camera; no 3D (rule 39): no camera moves round anything.

| build or risky move | why (parts the camera sees) | estimate (% of a week) | spent |
|---|---|---|---|
| JD Vance likeness (front, side, back; seated, walking at the lens, close-up, arm round, thumbs at himself) | new cast | 2.0 | |
| Study (bookcases, fireplace with a fire loop, desk, draped flag, crystal glass): one flat painting | new set | 1.0 | 1.0 |
| Cliff and strait (rock and sand foreground, sea from the Flying Whales painting re-lit for hazy daylight, far-shore smudge) | new set, sea reused | 1.0 | 0.9 (and the close-up's background) |
| Oil tankers (one side-on model, copies varied in size and colour; a wake for the moving one) | new prop | 0.6 | 0.5 (the wreck hull too) |
| Showstopper, in the cliff shot behind Vance: missile, flash, fireball, flaming pieces, splashes, smoke column, the wreck burning | effects reused; the hull stays whole with a torn hole amidships; only deck pieces and the funnel top fly (rule 54) | 1.5 | |
| Close-up with the burning wreck behind | the cliff shot's wreck re-framed | 0.3 | |
| Gas station (canopy, pumps, price board, shop, flat Midwest land) | new set | 1.0 | 0.9 |
| The big man (invented: 17 stone, goatee, balding, checked shirt, jeans; pump and hose) | new cast | 0.7 | |
| 4x4 pickup (side-on only) | new prop | 0.6 | 0.4 |
| Arm round the shoulder; both thumbs at himself | risky move | 0.3 | |
| Animatic rounds | | 1.0 | |
| **Total so far** | Sam's target (7 Nov): about 10%, like Terfwarts (9%) and MidTerminal (11%) | **10.0** | |

Sound effects (rule 26): the fireplace crackle (the script names it); the explosion and the pieces splashing (my pick). Asked in question 9.

## Showstopper elements (rule 40: Sam approves or trims before building; ticked at the first rehearsal clip)
| # | element | how it moves |
|---|---|---|
| 1 | The strait: calm sea to a hazy horizon, far shore a grey smudge | still, slow ripples |
| 2 | The tanker flotilla, 6-8 ships at anchor at different distances | still |
| 3 | The nearest tanker, under way to the right | slow, wake spreading behind it |
| 4 | Vance in front, walking on calmly, never looking round | as shot 2 |
| 4b | The missile: a black dart, small, no smoke trail | drops steeply from the sky, top left, in about 0.4 s |
| 5 | The flash: the whole frame goes white | 3 frames, then fades over 0.3 s |
| 6 | The fireball, huge, swallowing the ship's middle | swells and climbs, burns down to fire in about 1.5 s |
| 7 | Flaming pieces of tanker (deck plates, pipework, the funnel top) | thrown high and wide, tumbling, trailing flame |
| 8 | Splashes where each piece hits the sea | a crown and a falling column each; pieces sink |
| 9 | Black smoke pouring up in billows | rises and leans with the wind, keeps coming (never fades) |
| 10 | The wreck: hull whole, torn open amidships, burning | stops, fire tongues and smoke for the rest of the scene |
| 11 | The sea lit orange under the fire | follows the fire |
| 12 | A camera jolt and a 2-frame freeze on the hit | as Flying Whales |

## The brief as a checklist (CLAUDE.md, 18 Oct)
| # | from the brief (word for word) | done? |
|---|------|------|
| 1 | We are in an oak-lacquered study. | |
| 2 | JD Vance sits behind the desk. He projects an aura of confidence. He has a friendly and sincere demeanour. | |
| 3 | Behind him, a wall of book cases | |
| 4 | and on the right, a fireplace crackling softly. | |
| 5 | A crystal glass of water is before him on the desk. | |
| 6 | An American flag is draped over the left hand side of the desk. | |
| 7 | VANCE: "Hello, America. I'm J.D Vance." | |
| 8 | Cut to an Omani desert cliffside. | |
| 9 | In the background, the vast expanse of the Strait of Hormuz. The waters go on and on, the other side of the strait just a gentle grey smudge in the distance. | |
| 10 | Upon the waters, a flotilla of oil tankers floating in the stillness. | |
| 11 | The closest one to the scene is moving, however, sailing towards the right edge of the screen, ripples in its wake. | |
| 12 | Upon the cliffside, J.D Vance is walking calmly and gently towards the camera. He looks at the screen with sincere eyes. | |
| 13 | VANCE: "I know things haven't gone well recently. That you have your concerns. But there's something I need you to know." | |
| 14 | Showstopper shot: a black object, a missile from Iran, whips from the sky and strikes the moving tanker. | |
| 15 | Everything is enveloped in light as it erupts in a massive fireball. | |
| 16 | Flaming bits of tanker fly through the air and smash into the waters. | |
| 17 | Smoke vomits into the sky. | |
| 18 | Close up on JD's face, the flaming wreck upon the sea over his ~~right~~ **left** shoulder (Sam, 7 Nov: the screenplay was wrong). | |
| 19 | VANCE: "None of this is my fault." | |
| 20 | A Midwest gas station. | |
| 21 | A seventeen stone man in blue jeans and a checkered shirt, black goatee and a balding pate, stares up in unforgiving anger at the forecourt price board. | |
| 22 | It says that the Diesel price is $6.15. | |
| 23 | He stands next to his 4x4, holding the pump in his hand. | |
| 24 | J.D Vance walks in from the right and cheerfully puts his arm around the man. | |
| 25 | VANCE: "Aggravating, right? You know who isn't responsible?" | |
| 26 | He points at himself with both hands/fingers. VANCE: "This guy." | |
| 27 | The joke: Vance sincerely claims he isn't responsible for the election, prices or war, despite being Vice President. | |
| 28 | Hook Text + CranbriJoos sign-off (finish.py) on every animatic and the final. | |

## Acting (rule 74; front on, rule 38)
| line | who | face | body | lands on |
|---|---|---|---|---|
| 1 "Hello, America. I'm J.D Vance." | Vance | warm half-smile, eyes to the lens, brows soft | seated upright, hands folded on the desk; a small nod | nod on "America" |
| 2 "I know things haven't gone well recently." | Vance | sincere, brows up a touch in the middle | walking slowly at the lens, arms easy | brows on "haven't gone well" |
| 3 "That you have your concerns." | Vance | understanding, slight tilt of the head | still walking | tilt on "concerns" |
| 4 "But there's something I need you to know." | Vance | earnest, eyes steady | stops at his mark, one open hand to chest height | stop on "need" |
| (showstopper) | | | | |
| 5 "None of this is my fault." | Vance | calm, sincere, a reassuring small smile; never looks round (Sam, 7 Nov) | still, the fire's glow on his face | smile on "fault" |
| 6 "Aggravating, right?" | Vance | cheerful, big friendly smile | arm round the man's shoulders, a small squeeze | squeeze on "right" |
| 6 (same) | the man | fury fixed on the board; eyes slide to Vance on "right" | rigid, pump still in his hand, doesn't return the hug | eyes on "right" |
| 7 "You know who isn't responsible?" | Vance | eyebrows up, teasing | leans in a little | lean on "responsible" |
| 8 "This guy." | Vance | proud grin, eyes to the lens | arm comes off; both thumbs at his own chest (Sam, 7 Nov; his call over rule 69's pointing finger) | points on "This" |
| 8 (same) | the man | ask Sam: the script continues here | | |

## References as checklists (never draw blind)
| reference | what it shows | ours matches? |
|---|------|------|
| Vance likeness pack (rule 51) | 3 official portraits straight-on (2023, 2025, 2026) and a 2022 caricature, from Wikimedia Commons; the speaking photos were too far away to use. Hair medium-dark brown swept up and over from a parting on his right (our left), receding M; brows heavy, low, near straight; narrow hooded blue eyes; broad nose tip; short full brown beard with a ginger cast joined to the moustache; thin lips; broad upper face | yes: likeness check 73% / 81% / 66%, nothing the wrong way, 1st in the line-up (7 Nov) |
| Cliff and strait: `cliff-musandam-plateau`, `-road`, `-fjord` | 9 things listed (layered grey-brown limestone, stony plateau and track, sheer cliffs into the sea, calm blue-teal sea, haze, far shore a grey smudge, pale sky, no plants but a thorn tree, hard high sun) | yes, all 9 ticked (8 Nov) |
| Tankers: `tanker-side-wake`, `tanker-side-dark`, `tankers-at-anchor-haze` | 10 things (long and low, dark hull with red band, white bridge block aft, funnel band, deck pipe run, cranes amidships and raised bow, no names, all pointing one way at anchor, V wake under way, far ones grey bumps) | yes, all 10 ticked (8 Nov) |
| Gas station: `gas-iowa-canopy`, `gas-price-pylon`, `gas-price-board`, `gas-nozzle-filler` | 10 things (lit canopy with band, pump islands with posts, pumps with screens and black hoses, pylon board with blank top, lit prices ending in a small 9, DIESEL/REGULAR/PREMIUM rows, concrete forecourt, flat land and power poles, grain elevator, low shop) | yes, all 10 ticked (8 Nov) |
| Pickup: `pickup-side`, `pickup-rear` | 9 things (full-size crew cab 5.9 x 1.9 m, square grille, bed and tailgate, big wheels, arches and running board, big mirrors, fuel flap driver side ahead of the rear wheel, side on facing left, white paint) | yes, all 9 ticked; grille and bonnet out of the gas shot (rear half in frame) (8 Nov) |
| Study: `study-abbotsford`, `study-canons-ashby`, `study-oak-fireplace` | 10 things (floor-to-ceiling oak bookcases, leather books with gold bands, tall bays and cornice, lacquer shine, fireplace in the book wall on the right, black firebox and logs, mantel clock and candlesticks, gilt portrait over it, pedestal desk, warm low light) | yes, all 10 ticked (8 Nov) |

All lists in `source/ad_vanced_notice_comp.py` (`PLACES`), each photo's source in `references/ad-vanced-notice/sources.txt`; now the ticked `BENCHMARK` in `source/ad_vanced_notice_sets.py` (8 Nov).

Composition sheet sent: 7 Nov, `python3 source/ad_vanced_notice_comp.py comp OUT.jpg` (4 key shots, the cliff in two moments: study with the Hook Text band; cliff walk; cliff hit, Vance screen left, the tanker behind to his left; close-up, wreck over his left shoulder (screen right); gas station, arm round). Rough stand-ins: the driver faces the lens and the arm round is a hand on his shoulder; the build makes him glare up at the board.
Added (set dressing, from the photos, Sam to OK): a gilt portrait over the mantel, a mantel clock and candlesticks; a grain elevator, power poles and a low shop at the gas station; a white pickup.

## Questions sent to Sam (7 Nov)
1. The rest of the script: build now (cast, sets, showstopper) and fit the rest in when it comes (Y), or wait (N)?
2. Jokes early: the first laugh comes at about 11 s. Keep it as written, starting the cliff walk mid-stride (1), or cut the cliff line to "There's something I need you to know." (2)?
3. Vance photos: I gather the straight-on, three-quarter and talking photos myself (Y); you send one or two caricatures you like?
4. Hook Text: "JD Vance's new campaign ad" (1), or your wording (2)?
5. Showstopper: its own wide shot, nearer the tanker, no Vance in it (1), or the cliff shot held, Vance walking on in front, unaware (2)?
6. Close-up: Vance never looks round at the fire (Y)?
7. "This guy": both index fingers at his chest (1), or both thumbs (2)?
8. Price board: add Regular and Premium rows under Diesel, true to a real board, no joke (Y)?
9. Sounds: the fireplace crackle, the explosion and the splashes, nothing else (Y)?
10. Outfit: the same navy suit and red tie in every shot (Y)?

## Sam's answers (7 Nov)
1 Y: build now, fit the rest in when it comes. 2: keep the cliff walk as written (walking on the strait like a gentle political ad is itself a joke); Sam is reworking the dialogue for an earlier joke. 3: I find the photos (network now allows Wikimedia: new "Animation-" environment); Sam finds cartoons. 4: Hook Text later. 5 = 2: the explosion happens behind Vance in the cliff shot. 6 Y: never looks round. 7 = 2: both thumbs. 8 Y: Regular and Premium rows added. 9 Y: crackle, explosion, splashes only. 10 Y: navy suit and red tie throughout. Budget: about 10% of a week.

## Sam's answers on the composition (7 Nov)
1 Y: build the sets from these shots. 2 Y: Vance stops screen left, the tanker blows up behind him to the right. 3 Y, as long as the prices are peak Iran-war prices: Regular 4.39, Premium 5.25, Diesel 6.15 (his), each with the small 9. Source: AAA/Fortune, 6 Nov 2026: regular peaked at $4.29 national average and diesel topped $6 during the war; scaled to his $6.15 diesel, premium about 85 cents over regular. 4: white pickup. The added set dressing stands (no objection). All sets are flat 2D paintings, one per camera (rule 39), confirmed to Sam.

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | cast | | Vance has a light scrub of beard rather than the thick beard drawn | done: a pale tint flecked with short hairs; side view 'stubble'. New kind |
| 2 | cast | | The four emotions show an identical picture for Vance | done: each mood now moves brows, lids and mouth clearly (soft smile, open grin, one-sided smirk, earnest brows); "proud" added for "This guy". New kind |
| 4 | cast | | Draw this beard (close-up ref) on an empty face; get it really correct | done: measured on Sam's close-up (vance-beard-sam.jpg): level cheek line at the nose's base, full sparse moustache, dark band under the jaw, lighter chin front, soul patch with light patches either side, broad round bottom, salt-and-pepper flecks; test sheet beside the ref (`beard`). Likeness 71/85/65%. New kind |
| 6 | cast | | The beard is not right: convoluted, sort of disgusting | done: why note 4 failed: both fixes copied the photo's texture (a tint, then flecks and five tones) against the house style (flat colour, hand-cut shapes). Seen before (note 1) |
| 7 | cast | | Beard, as Sam described it: a small patch under the lip; a medium moustache; a dark/medium brown/silver beard covering from the lip corners to the face line, round the jaw, halfway up the chin; skin between it and the patch | done: four flat shapes in one silver-brown, ink round the outer edge only; likeness 70/68/62%. Seen before (notes 1, 4, 6) |
| 8 | cast | | Shape right; now the texture and colour | done: ash-brown body, darker jaw underside, moustache a touch warmer; edges facing skin are rows of small sharp tufts; a staggered grain of short silver-ash strokes falling down and in. Flat shapes, no random flecks. New kind |
| 9 | (tool) | | Build a tool that nails both beards (Vance, Abdul) on first analysis | done: `source/beardkit.py`. Photo gives the shape; Sam's words set what photos can't judge. Vance (2 words) and Abdul (3 words) largely match their finals (review/beardkit-test.jpg). Sam: a sensible approximation, largely correct. New kind |
| 10 | cast | | The driver's anger: 4; chequered sleeves ("checkered shirts tend to be 100% in pattern") | done: anger 4 is his default; the check runs along both sleeves. New kind |
| 5 | cast | | Anger 6 is the first face that registers as anger | done: the scale restarts there (new 1 = old 6) and goes stronger. New kind |
| 3 | cast | | Checked shirt: thicker colours, black and red | done: red with wide black bands, cut to his outline in every view; sleeves plain red. New kind |
| 11 | close-up | | The wreck goes over his LEFT shoulder: the screenplay had it wrong | done: wreck and smoke moved to screen right, Vance to screen left of centre; brief row 18 corrected. New kind |
| 12 | cast | | The check pattern doesn't go all the way to the edges of the clothes | done: why notes 3 and 10 didn't hold: to stay inside the outline, each band was only drawn where its whole width fitted, so every band stopped half a band short and left a plain red rim (and the sleeve bands were shortened on purpose). Now the check is printed full length and trimmed to the shirt's own red cloth (`_cloth`), so it meets the ink line on body, sleeves and collar; one band down each sleeve's middle so the sleeves still read against the body. Seen before (notes 3, 10) |
| 13 | gas station | | Prices must be peak Iran-war prices | done: Regular 4.39, Premium 5.25, Diesel 6.15 (see answers). New kind |
| 14 | all films | | Join the arms to the shoulders: they look like two separate parts, not one flowing body; for all future characters | to do next (kit job, Opus high): tested 7 Nov, `limbs.install` (the template's one-outline shoulder) makes no visible difference on the satire figures: each arm is still a tube with its own rounded cap sitting on the body's shoulder corner. Fix in the shared figure kit so the sleeve grows out of the shoulder: one outline from the collar over the shoulder and down the arm, no cap or line at the join (an armpit crease only when the arm lifts); cast sheets drawn with the same arms as the films. Before/after sheet across several past casts (Vance, the driver, Trump, Abdul) for Sam. Rule proposed (below). New kind |
| 15 | all sets | | Build the sets (Sam, 8 Nov) | done: one module, `source/ad_vanced_notice_sets.py`; each place ticked against its photos (rule 3), sizes clean. Changes from the composition: the study's back wall moved from 3.6 to 5 m back (at 3.6 m the desk hid the fire); the gas station looks over the pump island (its curb hides the men's feet; the man stands between the pump and his truck, as at a real pump), the board raised over the man's head, the two men a little left so the truck's rear wheel shows between them; two anchored tankers moved out from behind the headland (6 at anchor + the moving one). New kind |
| 16 | all sets | | Things I added (Sam to OK) | Added: a buttoned oxblood leather chair behind Vance. Added: a layered limestone headland across the bay on the right. Added: a thorn tree on the cliff rim (left). Added: a yellow post at the pump island's end, a canopy column (left edge), power poles with wires, field strips. Added: the pump shows an empty holster (the nozzle is in the man's hand). The close-up's tanker is drawn as the wreck (fire and smoke come with the showstopper). |

Rule proposals (waiting for Sam's number):
- R1 (Sam, 7 Nov: "all future character models"): rulebook rule 80, "Arms and body are one piece: the sleeve grows out of the shoulder with one outline from the collar, over the shoulder and down the arm; no line, cap or step where the arm meets the body (only an armpit crease when the arm is lifted). Every cast sheet draws the arms exactly as the film does." Check: a shoulder-seam test in `linecheck.py` that fails on any ink line across the shoulder join, run on every cast sheet.

Decisions made:
- Film name `ad-vanced-notice`; vertical 1080 x 1920 like the rest of the series.
- The close-up's wreck is over his LEFT shoulder = screen right (Sam, 7 Nov, correcting the screenplay); it matches the cliff shot, where the tanker is on his left too.
- No brand names on the gas station, the tankers or the pickup.
