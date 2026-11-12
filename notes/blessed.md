# Notes for BLESSED (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (hunt 1's faults fixed as one list, then hunt 2, then `critique.py fixed`), 67 (one full pre-flight, then the check sheet), 61 (blessed.py is 1,140 lines: move the moves into blessed_moves.py).
- **Done (11 Nov, chat 10, Opus high):** Brand's pre-scandal manner researched (4 reviews, cited in "How Brand moves"); the acting list and his moves changed to match (swagger walk, lean in on "mate", knee dip with arms flung open on "super" and "everybody!", chin-up preening, arms up and open on "Blessed!", chin lifts in the oath); clips sent. Head acting from the voice added for Brand and the newsreader (rule 74 gap). Hook Text placed at y 420 (it was over his hair; hookcheck clear). Brief checklist ticked; acting list ticked; sheets lines added. Critique hunt 1 (stage "animatic") recorded: 15 faults. Stopped on amber (2.2%).
- **Next: Opus, medium effort.** Type: "Blessed: fix critique hunt 1 as one list, hunt 2, then pre-flight and the check sheet with the Hook Text frame; stop for Sam's yes on animatic 1. Read CLAUDE.md, then notes/blessed.md Where things stand." Hunt 1 triage (look first, 2x crops): likely real: the dip and chin-up too small to read at phone size (dip 34 to ~60, chin -1.3 to ~-2.5); scarf gone in the 3/4 walk; hair a plait in side views; shades a thin gold bar (ref 02: big black aviators); TV room: bench not seen, blue too strong, fang-like teeth; royal arms read as animals; heart hand without forearm at 3.6. Check before fixing: court orange vs buff (ref 00); gatehouse "blank" vs ref 18; Brand tiny in the wide gates. Likely false: single frames can't show the swagger; his L hand is on screen right front-on; the prison bun is Sam's answer 7; at 51.2 he is on his mark.
- **Animatic 1 status (12 Nov 01:10, chat 10):** NOT rendered. Full pre-flight (faults-named) found 99 faults, mostly tool noise (SHOT CAST 'never on screen', plan room overlaps, journalist hands); the real one: the oath's raised right arm folded its elbow under 25 degrees at 4.92 s, which stopped the render at frame 59. Fixed (a waypoint in `oath`); the code changed, so pre-flight must run again (about 13 min) before `final source/data/blessed-clean.mp4 --faults-named`, then `finish.py ... --film blessed`. A scheduled chat (trigger at 1:01 London) was set to do the hunt-1 fixes; do the render after them.
- **Needs Sam:** a look at the two movement clips (arrival, gates).
- **Read:** `guides/job-packs.md` Notes round and Checks and animatic; this section; "How Brand moves".
- **Open rule requests:** none.
- **For Claude:** hunt 1 = source/data/critique/blessed/r1-p1 (spec in it); new: GAITS['swagger'], `_sway`, `_dip`, `GATE_V`/`GATE_OPEN`, `HEAD_LIFE`, `KEEP_CLEAR`; pre-flight --text faults left: newsreader mouth check at 52 s (her faded line under the gates: allow or stop her track at the fade), fast captions (lines 2, 3, 5), oath shot 9.6 s, SET_FEET missing (rule 13).
## The moves plan (moves chat 5, 11 Nov; build it in blessed.py, a "moves" section after "faces and moods")
Takes (seconds, film time): L1 0.62-3.65 one stretch ("feeling" ~1.26, "mate" ~2.36, "super" ~2.75); L2 stretches from 4.98: +0.12-2.05 ("I swear by Almighty God"), 2.32-4.22, 4.53-5.31, 5.62-6.34, 6.62-8.21 ("...the blessed truth"); L3 16.36-18.39; L4 from 28.75, last stretch +4.47-5.05 ("at all right now"); L6 from 49.21: "Blessed!" +0.12-0.72, rest +1.07-3.70.
- **Helpers:** port `word_at` (with ANCHORS for L2 'Almighty' (0, 0.42), first 'blessed' (1, 0.2), last 'blessed' (4, 0.62); L6 'everybody' (1, 0.72)) and `_bump` from `ad_vanced_notice.py` 106-120, 244. `_toward(j, side, tgt, g, pole, shape)`: blend the hand's CONTACT point (wrist + forearm unit x HAND[shape], not the wrist, or it pops) to the target, then `V.arm_to`. Hand circle = wrist + 12 along the forearm, radius 26 (`satire_style.install_circle_hands`).
- **arrive:** walk in ('walk' gait, phase +0.37 so mid-stride at the cut) from (1.2, 4.9) to the mark (0.45, 3.9) on ST.OUT (`ST._mark` gives screen x, y, ppm), yaw -45, stop at ~1.35 s, snap to front (yaw 0). Prayer beads hang from the R fist all shot (`grips.held`, a loop of small beads). L hand to the heart (30, 135, 78), pole 'in', palm, from "feeling" to "mate" - 0.35; up to the shades' bridge (`j['on_face']`) for "mate", the shades lower ON "mate" (brand_mood: replace L1 start + 0.9 with word_at); arms open, palms up, on "super"; L back to the heart with a small bow (lean 6, head nod) on the last "blessed"; to rest by 4.4 (rule 72).
- **oath:** stays yaw -45 at his mark. 0.15-0.65 s into the shot: far hand R holds the Bible at the chest (~(20, 160, 110), a black book with a gold cross, drawn as a projected box like `handset_pose`, `grips.held`); near hand L raised palm out beside the head (~(-(sw+90), -40, 60), pole 'out'; check the elbow by eye). Eyes up (gaze_dy -0.6) only on "Almighty God", ahead otherwise; a small lean-and-nod bump on each "blessed". Arms down from line end + 0.1 to + 0.5 (cut 14.04).
- **gavel:** judge `put_seated` at (540, 1780, 620); set `ST.GAVEL_LIFT = (T['s3'] + 0.15, T['s4'] + 1)` so the set stops drawing the resting gavel. R hand to the handle end (~ world (880, 1404); handle runs right of the head at (760, 1404)) 14.15-14.4; raise to shoulder 14.4-14.75; strike 'fast' 14.75-14.94 (T['bang']); a small rebound, then rest on the block. Draw the held gavel AFTER `ST.front` (the block is in the front layer) in world coords with `ST.gavel(p, x, y, ang)`, then redraw the hand circle over its handle (P1). Stern face; a tiny head jolt on the bang.
- **dock:** hands clasped low (both to (+-10, 420, 60), pole 'back'). Mood 'neutral', eyes ahead, until 15.9; then 'hollow' (eyes snap down) and the shoulders drop over 1.0 s eased (bob +12, head_dy +10, lean 4).
- **van:** seated yaw 35, bent over: lean 28, forearms on the thighs, hands clasped between the knees, head down, staring; a slow +-1.5 degree sway in lean (the van). No other move.
- **escort:** the cell painting fits a level camera exactly: `Level(1.55, 803.0, 1000.0, cx=540)` (eye 1.55 m, back wall at d 3.39 m: the bed's near end lands on the painted one within 10 px). Door in the right wall at x ~1.05, d 1.55-2.6. Brand starts in the doorway (1.0, 2.1) mid-stride, 'stroll' to (0.15, 2.35), side on facing left (yaw -90), stops ~23.8; snaps to yaw -30, looks round numbly with `head_yaw` (left 24.1, gaze up to the window 24.7, back down 25.2), eased. Officer one step behind and nearer the lens (x + 0.45, d - 0.25), same gait, his near hand ('L' facing left) on Brand's near upper arm; lets go at the stop and stands by the door. Marks: (Level.p(x, d), Level.ppm(d)); replace STAGE['cell'] guesses.
- **cot:** `lying.lie(sp, 'side', x, z, yaw, ground=0.45)` drawn with `lying_flat.draw(img, cam, k, sp, t)` (the house-style lying body). The 3D camera for the cot close-up (cell painting at B.Cam(1.55, 330, 1240)): `sets.Cam((0, 1.55, 0), (0, 1.55, 1), focal=1550, shake=(325.5, -677.35))`. Mattress top 0.45 m, x -1.05 to -0.25, d 1.39 to 3.39, pillow at the far end: head on the pillow (~d 3.1), knees towards us. Weeping face and tears; a sob every ~0.9 s (shoulders, neck, head nudged up 0.5 cm and back). Run `lying.contact_faults`.
- **phone:** keep `handset_pose`; lean 5, head down (head_dy +8, gaze down); a slow head shake (+-10 head_yaw over 1 s) on "at all right now"; free hand limp.
- **tvroom / push:** slouched (lean -6, head_dy +6) while the eyes drift up; on 'amazed' (eyes and face snap) he sits up over 0.6 s eased (lean 0); on 'overjoyed' lean forward 6, head up.
- **gates:** split into 'gates' (wide, ST.GATE camera, a slow push 1.0 to 1.35 on the door) and 'gates2' (a closer B.Cam on the same painting, centred on his mark), the cut at ~50.05 (after "Blessed!"). Wide: he steps out of the wicket door (x 0.15-1.15 at d GATE_D + 0.37) in the first 0.8 s and flings his arms wide ON "Blessed!" (hands go out to the side on the way up: figure-rig 3's waypoint). gates2: he strides the last steps into his mark (d 6.0 to 4.6) arms wide, stops, a double pump of the arms on "everybody!", holds. Add to SHOTS, VIEW, SHOT_CAST.
- **Checks to add:** each touch in TOUCHES (officer's hand, gavel, Bible, handset), the lying body's contact faults; `blessed.py check` clean; stills of every shot's first and last frames before the clips.

## Sam's answers (11 Nov): 1 FULL (19%); 2 Y gavel kept; 3 Y joke as written; 4 Y invented judge; 5 Y BBC News look and lettering; 6 Y press pack at the gates; 7 Y trial look at the gates, tracksuit and topknot in prison; 8 sincere showman; 9 quiet, to himself

## The questions asked (kept for the record)
1. Budget: **Lean, about 15%** (pick) or Full as written, about 19%. 8-12% is not reachable for this script without cutting a scene: it has 8 places and 7 people (MidTerminal, 11%, had 1 room and 3). Lean keeps every line and beat; the van and TV room become close-ups on Brand against dark, simple backgrounds; the cell and phone share one prison painting; the TV-room inmates are silhouettes.
2. The gavel: English judges never use one. **Keep it** (pick: it reads at once and Brand's line answers it) or no gavel (the judge just says the sentence).
3. Sex offenders were left out of the real early-release schemes. **Keep the joke as written** (pick: it is the satire) Y/N.
4. The judge: **an invented red-robed judge** (pick), not the real judge's face. Y/N.
5. The TV: **BBC News look with "BBC NEWS" lettering** (pick; parody) or an invented channel.
6. "everybody!" at the gates: **the same press pack waiting outside** (pick, reused) or an empty street.
7. "Usual attire" at the gates: **his trial look: dark jacket, open white shirt, crucifix, sunglasses, long white scarf, hair loose** (pick); prison: grey tracksuit, hair in the topknot from the sentencing sketch.
8. Line 1 tone: **sincere showman** (pick: believes his own performance, lowers the sunglasses, hand on heart) or a wink to camera.
9. Line 3 "doesn't feel very blessed": **quiet, to himself, deadpan** (pick) or said up to the judge.

## Plan extras: the estimate (Sam chose FULL, 19%: every place drawn in full, TV-room inmates as real Glimpse figures, two notes rounds; the lean rows below plus: sets +1.2 (van and TV room as full paintings, cell and phone separate), cast +0.4 (two inmates), round2 2.5)
Unmeasured: about 4.5 of the 15 (the sets and the support cast have no measured flat-painting or support figure yet; Remakes' sets cost about 2.7 each with three critique passes, the target is 0.7).

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | est. % | measured from | spent |
|---|---|---|---|---|---|---|
| Plan, references, questions | | | plan | 1.0 | Remakes plan 1 | ~1 |
| Brand (Lead): likeness, beard, long curly hair, topknot, 2 outfits | NEW | flat, all views the shots use; front, side, back | cast | 2.5 | Link trial 2.0 a Lead + outfits | |
| Judge (Support), red robe, wig, seated at the bench, chest up | NEW | one view (front), upper body only | cast | 0.5 | unmeasured (target 0.6) | |
| Prison officer (Support) | KNOWN `power_crime_cast` Met officer, recoloured | walk beside Brand | cast | 0.3 | unmeasured | |
| Newsreader on TV | KNOWN `newsdesk_cast.PRESENTER`, restyled | front only | cast | 0.2 | unmeasured | |
| Press pack (arrival and gates) | KNOWN `press_secretary.reporter` + photographers | from behind | cast | 0.1 | reuse | |
| Southwark Crown Court outside | NEW flat painting, one camera | ref 00 | sets | 0.9 | unmeasured | |
| Courtroom, two cameras (witness box with judge behind; glass dock) | NEW flat painting x2 | refs 05, 07, 08, 11 | sets | 1.0 | unmeasured | |
| Prison inside: cell (door, cot, toilet) + wall phone, one painting | NEW | close shots | sets | 0.6 | unmeasured | |
| Van cubicle and TV room: dark close-up backgrounds, TV flicker, silhouettes | NEW | close shots only | sets | 0.4 | unmeasured | |
| BBC-style studio on the TV | KNOWN `newsdesk_set`, restyled red | one camera | sets | 0.3 | reuse | |
| Prison gates outside | NEW flat painting | no reference (Sam: none needed after sentencing) | sets | 0.6 | unmeasured | |
| Moves: press walk and gestures, oath (Bible, hand up), gavel, van slump, escorted walk, weeping on cot, phone, TV face change with zoom, gate exit | mostly KNOWN (walks, sitting, lying, phone_ear); oath and weeping NEW | rehearsal clips: gate exit, face change, escort | moves | 1.5 | unmeasured | |
| Animatic 1 + Fable cold critique before it | | Fable (about 1%) to cut a notes round (2.5) | animatic1 | 2.0 | Remakes Fable r3 about 1 | |
| Notes round 1 | | | round | 2.5 | budget-job target from Remakes rounds | |
| Final | | | final | 0.5 | Remakes final 0.5 target | |
| **Total** | | | | **15.0** | (Full: + 1.2 sets, + 0.4 cast, + 2.5 second round = about 19) | |

## The brief as a checklist (Sam, 11 Nov)
| # | from the brief (word for word where it matters) | done? |
|---|------|------|
| 1 | Title: Blessed. News: Russell Brand sentenced to ten years for sexual assault and rape (real: 10 y 6 m, 9 Nov 2026) | Y: title in the notes only (no title on screen, CLAUDE.md); real sentence 10 y 6 m kept in the notes |
| 2 | Joke: he repeats his overly Christian "feeling blessed" line at arrival, sentencing, prison, then is released by Labour's early release scheme | Y: "blessed" at arrival, oath, dock, phone; release by the scheme at the gates |
| 3 | Brand loquacious and ostentatious in his acting, balanced with the press's descriptions at each stage (below) | Y: showman at arrival, oath (held in) and gates, from "How Brand moves"; press descriptions per stage (below) |
| 4 | Court drawings and press pictures for arrival, the stand, sentencing (none needed after sentencing); automatic retrieval fixed if it fails | Y: refs 00-20 filed and matched (court, box, dock, gates); fetched through the press sites after Sam's approval |
| 5 | S1 arrives at court, first day; approaches the press: "Yeah, I'm feeling blessed, mate, super blessed." | Y: arrive 0-4.5 s, line 1 to the press pack |
| 6 | S2 takes the stand: "I swear by Almighty God that the blessed evidence I shall give shall be the truth, the whole truth, and nothing but the blessed truth." | Y: oath 4.5-14 s, Bible and raised hand, judge behind |
| 7 | S3 sentenced, looking harrowed; the judge bangs his gavel; "Well that doesn't feel very blessed." | Y: gavel 14-15.6 s (Sam's Y), dock 15.6-19.5 s, hollow on line 3 |
| 8 | Montage: police van, bent over himself, empty and shocked | Y: van 19.5-22.3 s, bent over, numb |
| 9 | Montage: escorted into his cell by an officer, looking around numbly | Y: escort 22.3-25.5 s, officer's hand on his arm, looks round |
| 10 | Montage: weeping on the cot | Y: cot 25.5-28.3 s, weeping, sobs |
| 11 | Prison phone, dejected: "Yeah, love. I'm not just not feeling blessed at all right now." (Sam's wording kept) | Y: phone 28.3-34.8 s, Sam's wording kept |
| 12 | Shared room watching TV absently, TV light flickering on him; his eyes drift up to the screen | Y: TV room 34.8-37.4 s, blue flicker, eyes drift up |
| 13 | Screen: BBC news desk; reporter: "Our breaking news. The government has announced a new round of the early release scheme—" | Y: TV 37.4-43.6 s, BBC-style desk (Sam's Y), newsreader line 5 |
| 14 | Zoom in on Brand: dejected to amazed and overjoyed; the reporter's words drift away and fade: "as way of dealing with the prison capacity crisis. The Prime Minister has said that it is necessary to stop overcrowding." | Y: push 43.6-48.4 s, zoom, dejected to amazed to overjoyed; her voice fades after two phrases |
| 15 | Brand leaves the prison gates in his usual attire: "Blessed! I'm feeling so blessed right now, everybody!" | Y: gates 48.4-54.2 s, trial look (Sam's answer 7), press pack (answer 6) |
| 16 | Budget 8-12%; say honestly in advance if not; Fable 5.2 allowed where it makes a difference | Y: told in advance (8-12% not reachable); Sam chose Full 19%; spent 12.4% before this chat |
| 17 | Hook Text (pick: "Russell Brand this week") and the CranbriJoos sign-off | Y: Hook Text "Russell Brand this week" at y 420 (clear of sign and face, hookcheck); sign-off by finish.py |

## The press's descriptions by stage (brief 3)
- **Arrival (13 Oct):** dark glasses, long brown-grey wavy hair, grey beard; dark/grey jacket, open-neck white shirt, crucifixes of varying sizes, prayer beads, a long white scarf (another day a red one); held his wife's hand; "made a beeline for the media scrum"; "Hello, mate!"; "Today, I feel blessed... That's my prayer." (BBC, Sky, ABC)
- **The stand (28 Oct):** dark suit, white open-necked shirt; took the Bible oath loudly; stood bolt upright, hands clasped behind his back; nervous start, unusually loud "no"s; later hands in pockets; terse, flashes of irritability. Gaunt, thinner. (BBC, AP)
- **Verdict and sentencing (5 and 9 Nov):** hair in a topknot; stood upright in the glass dock, limited emotion; "Sit down Mr Brand"; mouthed "I'm good, I'm good" as he was led away. (BBC, sketches)
- So: the showman at arrival and the gates; the stiff, too-loud showman in the box; the stillness cracks only at the sentence.

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| 00 court outside (Wikimedia) | buff brick, dark band sign "CROWN COURT SOUTHWARK", steps and rails left, planted beds, pavement | |
| 02 arrival (Guardian) | aviator-style black sunglasses lifted by right hand, grey jacket, white open shirt, grey beard darker at the moustache, long dark curls | |
| 05, 07 witness box (Elizabeth Cook) | Brand side-on in the box, brown-olive jacket, open white shirt, mic on stalk; judge behind in red robe, white wig, bands, glasses; pale wood, pale wall | |
| 08 sentencing (Cook, Sky) | topknot, grey jacket, white shirt, standing in the glass dock, security officers seated behind | |
| 09, 10 dock (Quenzler) | straight-on face: deep-set eyes, long nose, beard grey at the chin; dark open shirt | |
| 11 verdict (Cook, BBC) | Brand standing in the dock, dark jacket, hands clasped low; judge in red, side-on, at a mic | |

## How Brand moves (before the scandal; one search pass, 11 Nov)
Sources: LA Times, Chris Lee, 14 Jun 2008 (Roxy show: "louche, preening British rock star", "Jagger-esque rock star
charisma", "exaggerated pantomime moves", "neurotic twitchiness", "looked up to face the capacity crowd"); The Comic's
Comic, 22 Jul 2008 (NYC debut: "slithering, crouching and twirling about onstage, his sprawling updo of hair flowing and
bouncing behind him"; walks out into the audience for crowd work; "I'm not Christ"); Guardian, Brian Logan, 20 Sep 2021
("charismatic and animated as ever", "sells it with brio"); The Times, Dominic Maxwell, 2021 ("does he believe he's the
Second Coming?", "he owns the stage").
1. **The swagger:** a rock-star strut, chest out, leaning back a touch, a loose sway of the head and shoulders over
   each step, a long easy stride. (Built: the 'swagger' walk, 108 steps a minute, with a head roll per step.)
2. **Big open-handed gestures:** whole arms, hands open, flung wide; pantomime, never small. (Built: arms open at
   shoulder height on "super"; up and open on "Blessed!".)
3. **The dip:** drops at the knees on the punchline and springs back up. (Built: on "super" and on "everybody!".)
4. **Goes to the crowd:** leans in close to people. (Built: leans in to the scrum on "mate", head tilted.)
5. **Preening:** chin up, looking up and out at the room. (Built: chin up on "super", "Blessed!" and each "blessed"
   in the oath.)
6. **The messiah joke:** arms out, palms open, the Second Coming. (Built: the gates' "Blessed!".)
7. **Twitchy underneath; hair bouncing:** not built (the hair has no bounce in our kit; small fidgets would muddy the
   held poses on phone-sized frames).
The showman is the arrival, the oath (held in: bolt upright, only the chin lifts) and the gates; prison has none of it.

## The acting list (revised 11 Nov from "How Brand moves"; ticked against the film 11 Nov: every row built, checks clean)
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Yeah, I'm feeling blessed, mate..." | Brand | medium, press backs in front: the showman to the scrum | sincere showman (Sam): beaming, sunglasses lowered on "mate", chin up on "super" | swaggers in (sway per step), beads in the R hand; L hand to heart; leans in to the scrum, head tilted, on "mate"; dips at the knees, arms flung open on "super", springs up; hand to heart, small bow | "super blessed" |
| 2 "I swear by Almighty God..." | Brand | side-on in the box, judge behind (as sketch 07): the stiff showman | eyes up on "Almighty God"; chin lifts on each "blessed" | bolt upright, Bible up, right hand raised (the showman held in) | "blessed truth" |
| (gavel) | judge | close on the judge | stern | gavel down | the bang |
| 3 "Well that doesn't feel very blessed." | Brand | close-up in the dock: the stillness cracks | quiet, to himself (Sam): hollow, eyes down | shoulders drop | "blessed" |
| montage | Brand | van close-up; cell walk with officer; cot | empty, numb, then weeping | bent over; looks round; curled on the cot, shaking | |
| 4 "Yeah, love..." | Brand | close-up at the wall phone | tearful, voice cracking | forehead to the wall, phone at ear | "at all" |
| 5 reporter | newsreader | the TV screen, then slow push on Brand | neutral | | "early release scheme" |
| (face change) | Brand | slow zoom to a close-up | dejected to amazed to overjoyed | sits up | "early release" |
| 6 "Blessed! I'm feeling so blessed..." | Brand | wide at the gates, then closer, press in front | full showman, sunglasses on, chin high | swaggers out; arms flung up and open, palms out (the messiah) on "Blessed!"; strides in; dips with arms swept open to the pack on "everybody!", springs up, head tilted | "everybody!" |

Length: about 101 words at Sam's pace (3.3 a second) is about 31 s, plus montage and beats: about 45 s.

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 1 | cast sheet | - | "small-looking head, a double-sized chin/beard area"; use Sam's photo b10 as the usual reference | Brand | fixed 11 Nov: face drawn 15% bigger (HEAD_K), beard cut to just below the chin and tapered, hairline raised (tall forehead), hair slimmer and to just past the shoulders; likeness 66% on b01, 48% on b10 (three-quarter with sunglasses: the tool reads its forehead wide and jaw narrow, against b01) |
| 2 | cast sheet | - | "chin still big" (warning: note 1 again) | Brand | fixed 11 Nov: why note 1's fix fell short: the chin push (P4.TUNE chin_long 22, set for the likeness check's "long chin") kept the lips high and the lower face long; now 4. The beard tip ends just below the chin; the moustache is a band over the lip with drooping ends and a small soul patch (b10), not a dark box. Likeness 64% on b01 |
| 3 | recordings | - | Sam's six voice files (11 Nov), filed by length against the script: `source/audio/blessed-1.m4a` arrival (8.9 s), `-2` oath (13.1 s), `-3` "doesn't feel very blessed" (3.9 s), `-4` phone (6.4 s), `-5` gates (4.9 s), `-bbc` the newsreader (22.4 s). Not yet heard against the words (no speech-to-text here): check at the animatic | all | filed |
| 4 | arrive, gates | all | "the journalists are blob people": the press pack from behind (press_secretary.reporter, the kit's own, not stand-ins) reads as blobs: give them shoulders, collars, ears, hair with shape, arms, at least one turned three-quarter | press | done (cast chat 8: standing people, turning heads, eight haircuts, three turned; same pack at both; stills sent) |
| 5 | tvroom, push | 34.75-48.41 | "the prisoners have strange heights, proportions and details next to Russell; no mouths?": they are the real cast (INMATE in blessed.py), not stand-ins; Brand is drawn bigger (_Big head, nearer mark), so they look small and plain; match their scale and head size to his, give them mouths and faces with detail | inmates | done (cast chat 8: Brand's face system at his size, one bench depth, eyes up; stills sent) |
| 6 | cot | 25.45-28.25 | "the lying pose doesn't look quite right, maybe in motion": the same as fault 2; add a cot clip (25.45-28.25) to the rehearsal clips | Brand | done (moves chat 7: curled along the bed, head on the pillow; clip sent) |
| 7 | gates | 48.41-54.17 | "the press need to be a lot closer to the gate. Brand is a distant speck" | press, Brand | fixed 11 Nov (chat 9): gatehouse at 9 m not 18, pack in a horseshoe round the wicket, wide shot framed tighter; stills sent |
| 8 | arrive, gates | all | "they should face him, rather than at walls"; "that cost a round of notes" | press | fixed 11 Nov (chat 9): every journalist's body and head turned to Brand. Why it slipped: note 4's fix turned three to glance aside for variety, and P2's gaze check only covers the acting list. Lesson proposed |
| 9 | gates | 49-54 | "what is going on with these ears?": ears drawn on top of long hair from behind | press | fixed 11 Nov (chat 9): no ears drawn for the bob, long and curly haircuts (turnhead `ears_hidden`); crops sent |

Composition sheet sent: 11 Nov, notes/sheets/blessed-sets-sheet.jpg and chat 9's set-fix stills (every set)
Rehearsal clips sent: 11 Nov, blessed-arrival-moves.mp4 and blessed-gates-moves.mp4 (the showman moves; chat 10)

Decisions made:
- References fetched through the press sites' own image servers after Sam's network approval (11 Nov); Wikimedia's API rate-limited us once.
