# Notes for BLESSED (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 67 (one full pre-flight, about 15 min), 59 (every fault fixed or named before the animatic), 14 (the check sheet with the Hook Text frame, then wait for Sam's clear yes).
- **Done (12 Nov, chat 4, Opus):** the 17 pre-flight faults answered; quick check clean. Fixed: the Bible now moves with his hand (it floated off it on the way up) and he holds the oath pose to the cut (rule 72); the judge shifts his weight and head (was dead still 2.5 s); FAMOUS uses the drawn name; each journalist has their own name (the cut check had pooled them all as one 'Journalist', the likely cause of 2 of the 3 cut faults) and a turnaround entry. The cot: lying curled from this camera drew his face upside down (looked at full size, rule 42; every lying angle tried was off the bed or out of frame), so he now SITS on the cot's edge, weeping at us, sobs heaving his shoulders. Named as meant (HANDS_OK, each looked at full size): journalists' hands under their raised kit (arrival, gates); his hand-on-heart sleeve edge; the shoulder "seams" are his hair over the shoulders; van hands clasped; the officer's grip.
- **Needs Sam:** at the check sheet: the cot change (Lost: curled up lying on it. Added: sitting on its edge, weeping at us).
- **Done (12 Nov, chat 5, Sonnet):** quick check clean; ONE full pre-flight run (12 min): 1 fault, HANDS: oath 4.83 s, Brand's left arm, the Bible hand is hidden (22% shows). The critique's second pass also fixed 6 faults itself (aviator lenses, wider gates, HM PRISON sign, phone gaze). No pass stamp, so no animatic yet.
- **Done (12 Nov, chat 6, Sonnet):** oath hand fixed; animatic 1 rendered (full size by mistake: 31 min; rule now in guides/satire.md: animatics are always `--small`), finished at 1.1x and sent (`review/blessed-animatic-1.mp4`, 8.7 MB, off GitHub as a draft). Rules written (Sam's Y): no check sheet unless asked (CLAUDE.md); animatic = `--small` (satire.md); the pre-flight audit job is below. Sam's round-1 notes 11-26 logged in the table, none fixed yet.
- **Next: Opus, medium effort (chat opened 12 Nov): notes 11-24 and 26.** Order: the mouths first (13, 15: find why the judge has none and note 5's fix never reached him, rule 30), then the body faults (14, 16), front-on Brand (13, 17, 21, 26), the sets (12, 17, 20, 22, 24), the despair shot from above (18), the zooms (23). Clips of the changed moments (`final OUT --small --span T0 T1`), no full animatic until the clips look right; then a Sonnet chat for checks and the animatic. Note 25 (Walliams) waits for Sam.
- **Needs Sam:** 1 Walliams (note 25): B (pick) / A / C; 2 front-on scope (note 26): Y (pick) / N. Note 19: if his recording differs from "Yeah, love. I'm just not feeling very...blessed right now.", he re-records.
- **Spent:** stage animatic1 about 7.2% against 2% (Sam said Y to go on); round 1 of 2 notes rounds starts now.
- **Follow-up tool fix (not done):** `kitchecks.faces` on an incremental run must not report from partial frames (keep the last full run's best face size in blessed-frames.json). Audit job after Blessed's last round (below).
- **Read:** `guides/job-packs.md` Checks and animatic; this section.
- **Open rule requests:** none.
- **For Claude (chat 4):** cot = put_seated at COT_MARK/COT_YAW, cot_pose (blessed_checks.placed updated); oath: lift = _contact - OATH_BIBLE, dn0 = T['s3']+0.05; judge jj shifts; press_sp name 'Journalist N', turnhead.PEOPLE[who].sheet; HANDS_OK list after CUT_RESTS_OK. Stills checked at 4.75, 4.9, 13.95, 25.0. blessed.py over 1,100 lines (rule 61 warning, not a fault).

## Job after Blessed's last round: the pre-flight audit (Sam: Y, 12 Nov)
Run once Blessed's last notes round is done (Opus, high to design; medium to build). For each check pre-flight runs: what it has caught (films, faults, how many were real), checks that catch the same thing twice, which merge, and which can become built-in to the drawing kit so the fault cannot happen. Start with: the face-size check (rule 50) on partial re-checks (chat 6: a false 'never 240 px' from 7 re-drawn frames; fixed in preflight.py after animatic 1).

## Sam's answers (12 Nov): 1 Y no check sheet before animatics unless he asks (CLAUDE.md written); 2 Y animatic 1 skips the sheet; 3 Y the pre-flight audit job above

## Sam's answers (11 Nov): 1 FULL (19%); 2 Y gavel kept; 3 Y joke as written; 4 Y invented judge; 5 Y BBC News look and lettering; 6 Y press pack at the gates; 7 Y trial look at the gates, tracksuit and topknot in prison; 8 sincere showman; 9 quiet, to himself

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
| 7 | S3 sentenced, looking harrowed; the judge bangs his gavel; "Well that doesn't feel very blessed." | Y: no gavel shot (Sam, 12 Nov): bang heard at the start of the dock shot 14.0 s, hollow on line 3 |
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

## The acting list (revised 11 Nov from "How Brand moves"; ticked against the film 11 Nov: every row built, checks clean)
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Yeah, I'm feeling blessed, mate..." | Brand | medium, press backs in front: the showman to the scrum | sincere showman (Sam): beaming, sunglasses lowered on "mate", chin up on "super" | swaggers in (sway per step), beads in the R hand; L hand to heart; leans in to the scrum, head tilted, on "mate"; dips at the knees, arms flung open on "super", springs up; hand to heart, small bow | "super blessed" |
| 2 "I swear by Almighty God..." | Brand | side-on in the box, judge behind (as sketch 07): the stiff showman | eyes up on "Almighty God"; chin lifts on each "blessed" | bolt upright, Bible up, right hand raised (the showman held in) | "blessed truth" |
| (gavel) | none | NO SHOT (Sam, 12 Nov): the bang is only heard, on the dock shot's first frame; Brand gives a small start | | | the bang |
| 3 "Well that doesn't feel very blessed." | Brand | close-up in the dock: the stillness cracks | quiet, to himself (Sam): hollow, eyes down | shoulders drop | "blessed" |
| montage | Brand | van close-up; cell walk with officer; cot | empty, numb, then weeping | bent over; looks round; curled on the cot, shaking | |
| 4 "Yeah, love..." | Brand | close-up at the wall phone | tearful, voice cracking | forehead to the wall, phone at ear | "at all" |
| 5 reporter | newsreader | the TV screen, then slow push on Brand | neutral | | "early release scheme" |
| (face change) | Brand | slow zoom to a close-up | dejected to amazed to overjoyed | sits up | "early release" |
| 6 "Blessed! I'm feeling so blessed..." | Brand | wide at the gates, then closer, press in front | full showman, sunglasses on, chin high | swaggers out; arms flung up and open, palms out (the messiah) on "Blessed!"; strides in; dips with arms swept open to the pack on "everybody!", springs up, head tilted | "everybody!" |

Length: about 101 words at Sam's pace (3.3 a second) is about 31 s, plus montage and beats: about 45 s.

## Notes
Sam, 12 Nov (note 10, new shot; BUILT 12 Nov chat 11, clip blessed-oath-jury.mp4 sent): "During the oath, can we 180 to the jury, staring at him. Some begin to show crossed annoyed eyebrows or share glances with each other. You can use elements from previous films to build the different faces and body shapes, as long as no characters are repeated or identifiable. That should happen for a few seconds in the middle of the oath. Then we go back to brand." Plan: a reverse shot from behind/beside the witness box onto the jury box (12 jurors, two rows, seated, pale wood like refs 05/07), a few seconds in the middle of line 2 (cut on a phrase break, e.g. from "shall be the truth" to "the whole truth", the voice carries over), then back to Brand for "...nothing but the blessed truth". Jurors built from kit parts of earlier films' faces and bodies (mixed so none is a repeated or recognisable character), all staring at the box; some brows knit (annoyed), two or three pairs swap a sideways glance. New: jury box set, 12 Glimpse jurors (rule 24), the cut. Then the critique rounds (hunt 1 faults, hunt 2) as Next says.
Sam, 12 Nov: "I don't want the gavel shot. I want the gavel heard at the beginning of the sentencing shot." Done: Lost: the gavel shot (judge raising and striking the gavel, 1.6 s) and with it the film is 1.3 s shorter (52.9 s). Added: a wooden knock made in the code at the dock's first frame, and a small start from Brand on it. Clip: blessed-sentencing-gavel.mp4.
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
| 10 | oath | 7.15-10.41 | the jury reverse shot staring at him, annoyed brows and glances, invented jurors | jury | built 12 Nov (chat 11): clip sent. Added: a 3.3 s shot inside the oath (film length unchanged) |
| 9 | gates | 49-54 | "what is going on with these ears?": ears drawn on top of long hair from behind | press | fixed 11 Nov (chat 9): no ears drawn for the bob, long and curly haircuts (turnhead `ears_hidden`); crops sent |
| 11 | arrive | 0-8.9 | camera lower, amongst or just behind the journalists: Brand more in frame, less building, 'Southwark' sign still seen | camera | open (round 1, 12 Nov) |
| 12 | arrive, gates | all | "high interest case, tons of press": a much thicker press crowd in the arrival AND the gates | press | open |
| 13 | oath | 4.5-14 | "really do not like 3/4 Brand... considering retiring it entirely": reposition so Brand is FLAT, front-on, South Park style; and "why no mouth on the judge?" (the judge is drawn with no mouth in this shot) | Brand, judge | open. WARNING (rule 30): note 5 already said "no mouths?" for the inmates: find why that fix did not reach the judge before changing anything |
| 14 | jury | 7.15-10.41 | the woman in the hijab has no neck; the men's bald heads are so huge they look a different species | jurors | open |
| 15 | sentencing | 14-25 | no mouths again (judge and anyone else): never leave a human without a mouth, and "if it's to fit the budget, that's ridiculous"; 50% of the frame is empty wall: frame tighter | judge, framing | open. Rule 30 again (see 13) |
| 16 | van | 21-25 | loves the pose; the limbs are wrong: an arm coming out of the torso, legs not attached to the body ("not the level of the last film") | Brand | open |
| 17 | cell | 25-28 | wall detailing pops in a few seconds in; the sigh is too brief to read; refine the green blanket shape; 3/4 pose to FRONT-facing, direction by the eyes | set, Brand | open |
| 18 | despair | 25.45-28.25 | lie him FLAT on the bed; camera slowly moving toward him from ABOVE; he sobs, blinks, stares upward; a Bible beside him on the sheet | Brand, camera | open. Lost: sitting on the cot's edge (chat 4). Added: lying flat, the Bible. (Chat 4 could not draw lying from the side; from above it should work) |
| 19 | call | 28-35 | the line is "Yeah, love. I'm just not feeling very...blessed right now." Check it against LINES, the subtitles and Sam's recording (blessed-3/-4); if the words differ from the recording, ask Sam | line | open |
| 20 | call | 28-35 | the crude drawn prison on the right is below standard: set it in a room, next to another phone booth | set | open. Lost: the prison painting on the right |
| 21 | call | 28-35 | 3/4 has one eye/eyebrow: face him front-on, South Park style ("in fact just do that") | Brand | open |
| 22 | tvroom | 34.75-48.41 | inmates too close together: plastic chairs, not a bench (adult wings: heavy-duty wipe-clean plastic chairs); Brand watching TV; one other man behind on the LEFT watching TV, fast asleep; behind on the RIGHT a pool table, an inmate lining up a shot; remove Brand's tears, make him dead-eyed | set, inmates, Brand | open. Lost: the bench, Brand's tears. Added: chairs, pool table, sleeper |
| 23 | news | 34.75-48.41 | slow zoom in on the reporter; slow zoom in on Brand's FACE, not his torso; his neck join looks wrong | camera, Brand | open |
| 24 | gates | 48.41-54.17 | start closer to the action; a real press pack: flashing cameras, many more individuals, journalists in professional clothes, production crew dressed for their jobs | press | open |
| 25 | gates (end) | 48.41-54.17 | MAIN EDIT: David Walliams news: officers holding him by the arms, in prison clothes, towards and into the door Brand just left; everyone front-on, South Park movement; Walliams scared and alarmed | new shot | ON HOLD: real news checked 12 Nov (Guardian, BBC, CNN): he is ACCUSED (Guardian/ITV, 10 Nov), denies it, is not arrested or charged, and a court heard he attempted suicide: prison clothes and officers show something that has not happened. Asked Sam (question 1); build nothing until he answers |
| 26 | all | all | 3/4 Brand retired (see 13, 17, 21): front-on, South Park movement for every character in the new final scene | style | open: asked Sam how far (question 2) |

Composition sheet sent: 11 Nov, notes/sheets/blessed-sets-sheet.jpg and chat 9's set-fix stills (every set)
Rehearsal clips sent: 11 Nov, blessed-arrival-moves.mp4 and blessed-gates-moves.mp4 (the showman moves; chat 10)

Decisions made:
- References fetched through the press sites' own image servers after Sam's network approval (11 Nov); Wikimedia's API rate-limited us once.
