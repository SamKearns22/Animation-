# Notes for BLESSED (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (fresh-eye critique once the film draws frames), 41 (arms end in hands), 74 (acting list before animatic 1).
- **Done (11 Nov, build chat 2, Opus high):** the cast in `source/blessed_cast.py` (Vance pattern). Brand: measured face, beard, long curls, topknot, aviators (on / lowered), 10 moods, three looks (trial, stand/dock, prison), turned heads. Likeness 64% on b01 (pass) after Sam's notes 1-2 (bigger head, short chin and beard; b10 is the usual reference). Sam's six recordings filed (note 3). Judge (invented, wig front only), prison officer, newsreader. Two by-eye critique passes: fixed the judge's missing wig, the officer's lab-coat look, the topknot cone, the lowered shades, the turned hair's spikes and the strip across his face. Cast sheet, faces sheet, likeness sheet in `notes/sheets/blessed-*.jpg`, sent to Sam.
- **Spent against the estimate:** plan ~1%; cast stage 2.41% of 4% planned (ledger: lands at 11.4%).
- **Next:** build chat 3 (Opus, high effort), opened by build chat 2 on Sam's Y: the sets (court outside, courtroom x2, prison cell + phone, van, TV room, BBC-style studio, gates), then `source/blessed.py` from `satire_template.py`.
- **Needs Sam:** nothing until the sets sheet (Sam: Y to the cast, 11 Nov).
- **Read:** `guides/job-packs.md` Build; this file; `source/blessed_cast.py` MAP only.
- **Lost / Added:** Lost: prayer beads on his chest (read as dots; can go in his hand). Added: none.
- **Open rule requests:** none.
- **For Claude:** `critique.py pack` needs film frames (`blessed.py` not built), so rule 89's fresh-eye helper was not run on the cast; run it on the first set/shot frames. Likeness: `P4.TUNE['brand']` was tuned against b01+b03; the dark moustache and the long beard tip carry the chin and nose measures (slimming them dropped b03 to 44%). Judge side/back views are bald (wig is front only: he is only seen front-on at the bench). Turned long hair: `_turned_long` (screen units).

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
| 1 | Title: Blessed. News: Russell Brand sentenced to ten years for sexual assault and rape (real: 10 y 6 m, 9 Nov 2026) | |
| 2 | Joke: he repeats his overly Christian "feeling blessed" line at arrival, sentencing, prison, then is released by Labour's early release scheme | |
| 3 | Brand loquacious and ostentatious in his acting, balanced with the press's descriptions at each stage (below) | |
| 4 | Court drawings and press pictures for arrival, the stand, sentencing (none needed after sentencing); automatic retrieval fixed if it fails | |
| 5 | S1 arrives at court, first day; approaches the press: "Yeah, I'm feeling blessed, mate, super blessed." | |
| 6 | S2 takes the stand: "I swear by Almighty God that the blessed evidence I shall give shall be the truth, the whole truth, and nothing but the blessed truth." | |
| 7 | S3 sentenced, looking harrowed; the judge bangs his gavel; "Well that doesn't feel very blessed." | |
| 8 | Montage: police van, bent over himself, empty and shocked | |
| 9 | Montage: escorted into his cell by an officer, looking around numbly | |
| 10 | Montage: weeping on the cot | |
| 11 | Prison phone, dejected: "Yeah, love. I'm not just not feeling blessed at all right now." (Sam's wording kept) | |
| 12 | Shared room watching TV absently, TV light flickering on him; his eyes drift up to the screen | |
| 13 | Screen: BBC news desk; reporter: "Our breaking news. The government has announced a new round of the early release scheme—" | |
| 14 | Zoom in on Brand: dejected to amazed and overjoyed; the reporter's words drift away and fade: "as way of dealing with the prison capacity crisis. The Prime Minister has said that it is necessary to stop overcrowding." | |
| 15 | Brand leaves the prison gates in his usual attire: "Blessed! I'm feeling so blessed right now, everybody!" | |
| 16 | Budget 8-12%; say honestly in advance if not; Fable 5.2 allowed where it makes a difference | |
| 17 | Hook Text (pick: "Russell Brand this week") and the CranbriJoos sign-off | |

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

## The acting list (draft; "ask Sam" where open)
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Yeah, I'm feeling blessed, mate..." | Brand | medium, press backs in front: the showman to the scrum | sincere showman (Sam): beaming, sunglasses lowered on "mate" | swagger in, hand to heart, beads in the other hand | "super blessed" |
| 2 "I swear by Almighty God..." | Brand | side-on in the box, judge behind (as sketch 07): the stiff showman | eyes up on "Almighty God", leaning on each "blessed" | bolt upright, Bible up, right hand raised | "blessed truth" |
| (gavel) | judge | close on the judge | stern | gavel down | the bang |
| 3 "Well that doesn't feel very blessed." | Brand | close-up in the dock: the stillness cracks | quiet, to himself (Sam): hollow, eyes down | shoulders drop | "blessed" |
| montage | Brand | van close-up; cell walk with officer; cot | empty, numb, then weeping | bent over; looks round; curled on the cot, shaking | |
| 4 "Yeah, love..." | Brand | close-up at the wall phone | tearful, voice cracking | forehead to the wall, phone at ear | "at all" |
| 5 reporter | newsreader | the TV screen, then slow push on Brand | neutral | | "early release scheme" |
| (face change) | Brand | slow zoom to a close-up | dejected to amazed to overjoyed | sits up | "early release" |
| 6 "Blessed! I'm feeling so blessed..." | Brand | wide at the gates, press in front | full showman, sunglasses on | arms flung wide, scarf flying | "everybody!" |

Length: about 101 words at Sam's pace (3.3 a second) is about 31 s, plus montage and beats: about 45 s.

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 1 | cast sheet | - | "small-looking head, a double-sized chin/beard area"; use Sam's photo b10 as the usual reference | Brand | fixed 11 Nov: face drawn 15% bigger (HEAD_K), beard cut to just below the chin and tapered, hairline raised (tall forehead), hair slimmer and to just past the shoulders; likeness 66% on b01, 48% on b10 (three-quarter with sunglasses: the tool reads its forehead wide and jaw narrow, against b01) |
| 2 | cast sheet | - | "chin still big" (warning: note 1 again) | Brand | fixed 11 Nov: why note 1's fix fell short: the chin push (P4.TUNE chin_long 22, set for the likeness check's "long chin") kept the lips high and the lower face long; now 4. The beard tip ends just below the chin; the moustache is a band over the lip with drooping ends and a small soul patch (b10), not a dark box. Likeness 64% on b01 |
| 3 | recordings | - | Sam's six voice files (11 Nov), filed by length against the script: `source/audio/blessed-1.m4a` arrival (8.9 s), `-2` oath (13.1 s), `-3` "doesn't feel very blessed" (3.9 s), `-4` phone (6.4 s), `-5` gates (4.9 s), `-bbc` the newsreader (22.4 s). Not yet heard against the words (no speech-to-text here): check at the animatic | all | filed |

Decisions made:
- References fetched through the press sites' own image servers after Sam's network approval (11 Nov); Wikimedia's API rate-limited us once.
