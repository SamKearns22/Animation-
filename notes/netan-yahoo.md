# Notes for Netan-Yahoo! (brief: `prompts/netan-yahoo.md`; code to come: `source/netan_yahoo.py` from `source/satire_template.py`)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **Done (26 Oct, planning chat, Opus):** all questions answered ("Sam's answers" below); references packs 1-5 in
  (Maul movement, wounds, debate layout, Netanyahu faces; the cat dropped; the presenter left to me); the plan in metres
  and three versions of the composition sheet (`source/netan_yahoo_comp.py`); Sam: "let's build". "President" is
  "Prime Minister" everywhere. Nothing built yet.
- **Next: BUILDING, Opus high effort, fresh chat.** In order: (1) start `source/netan_yahoo.py` from
  `source/satire_template.py` with the PLAN, cameras, `SHOT_CAST`, `BENCHMARK` from the plan below; (2) the younger
  presenter (answer 2: a `PRESENTER` variant, say what changed); (3) eye direction (`sp['look']`) on the Netanyahu and
  Maul heads; Netanyahu's surprised and impressed faces (pack 5) and a 1-6 strength sheet; (4) the big Hebrew screen
  caption 'עימות לראשות הממשלה 2026' and the hook "Israeli Prime Ministerial Debate"; (5) Maul's moves from pack 1: ready
  stance, ignition, leap-flip (hood falls back), crouch landing, three strikes and follow-through, spring onto the chair,
  territorial crouch with head snaps (answer 11); (6) the cuts: flare, sparks, flat smoke, orange rims cooling, four
  pieces falling into a pile, steam (answers 8-9, pack 2; no blood); the presenter's reactions (hands up, then the arch);
  (7) the saber glow (answer 10). Then the cast sheet; then, motion-led, early clips of the risky moves (rule 8): the
  leap-flip and landing, the three strikes and pieces, the spring onto the chair.
- **Waiting on Sam:** the saber sounds (ignition, hum, three swings, a sizzle per cut; kept OFF GitHub); the recordings
  (later today; "Prime Minister" in the line; "shit" said in full, S heard, rest bleeped).
- **Already built:** studio `source/newsdesk_set.py`, presenter `newsdesk_cast.py`, Netanyahu `netanyahu_cast.py`, Maul
  `maul_cast.py` (saberstaff, 4 poses), chairs `newsdesk_props.py`. Reuse: sparks, flat smoke, steam (`prepper_fx.py`),
  falling pieces (Poker Mon's `launch`), lying pieces (`lying.py`).
- **Watch out:** this planning session could not install `numba` (pypi.org blocked), which `lying.py` needs. If the
  building chat hits it, Sam can allow pypi.org in claude.ai Settings, Capabilities.
- **Losses and my additions Sam should know about:** spacing 1.8 m (his photo: 2.5-3 m; the tall frame); the flip is
  mostly upwards (about 1 m of travel); shot 4 is now front-left, so the presenter is nearest (the photo had the right end
  nearer); Netanyahu leaves the frame during shot 4's push-in. Additions he approved: thump, pieces landing, chair creak,
  steam hiss (sounds, my code), sparks and smoke at the cuts, steam wisps, hood falling back. No set dressing.
- **Ambition estimate (rule 24, estimate):** about 12-18% of a week; the action is the cost.
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** this file, `prompts/netan-yahoo.md`, `notes/newsdesk.md` (the built cast and set),
  `guides/satire.md`, `guides/film-quality-rules.md`, `guides/figure-rig.md`, `story/status.md` (Newsdesk section only).

## Sam's answers (26 Oct, to the questions in one message; "yes" = my recommendation)
1. Maul sheet: no notes; use him as built.
2. Presenter, younger: same navy suit and glasses; no beard, no grey; darker, fuller hair; quicker head moves; more upright.
3. Staging: all three STAND the whole film, on the open floor in front of the desk. The brief's "in his chair" (shot 2)
   is overruled. REVISED by Sam's layout reference (pack 3): presenter at the screen-LEFT end, Maul in the MIDDLE, Netanyahu
   screen RIGHT, about 2.5-3 m apart (my choice: Maul next to the presenter keeps the leap-flip to about 3 m, and Netanyahu
   watches it all from the far end). Maul leaps screen-left.
4. Presenter's chair: a third wooden armchair (as the candidates'), behind him; all action on the open floor.
5. Shot 3: a close shot on Maul matching shot 2's on Netanyahu (same size and height).
6. Maul IGNITES the saber: both blades light as he springs; the ignition sound leads the jump.
7. Hood falls back in the roll; he lands bare-headed, horns showing. Cloak stays on.
8. Three strikes: shoulder to hip (diagonal), then the other arm, then across the thighs. Four pieces (head and shoulder,
   torso, arm, legs) fall into a pile where he stood. He sees it coming and raises his hands first.
9. Cut faces: scorched black with a thin orange rim, suit cloth visible, nothing inside shown, wisps of flat steam (reuse
   the mug steam, `prepper_fx.py`). No blood.
10. Saber: the soft glow (Sam's Poker Mon exception) on the blades only.
11. Maul on the seat: crouched on it, one hand on the armrest, saber held low across him, head turning to glare; holds ~2 s.
    Sam (pack 4, no photo: the cat was a metaphor): "ready for more action, crouched, territorial, staring around". So:
    the crouch from `maul-7-landing-crouch` on the seat, weight forward, both blades still lit and held ready; the head
    snaps from look to look (rule: eyes jump), body still; no settling back or relaxing.
12. Netanyahu: shot 4 mild surprise = brows up, small lean back, no step. Shot 5: a strength sheet (1-6) for Sam to pick;
    default 3.
13. Bleep: the "S" sound is HEARD; the bleep covers the rest of the word, from just after the S. Subtitle "S***, he's good."
    Place it from the sound itself (rule 27).
14. Hebrew: the logo is the set's made-up channel 'חדשות' (News). Screen caption (after answer 15): 'עימות לראשות הממשלה 2026'
    (Debate for the Premiership 2026). My Hebrew, not certain: Sam told it may be worth a Hebrew reader's check.
15. "Prime Minister" everywhere: script "incumbent Prime Minister Netanyahu"; Hook Text "Israeli Prime Ministerial Debate";
    the screen caption above.
16. Length: about 30 s plus the 2 s sign-off (estimate): OK.

## Plan extras (film-quality-rules 24-27)
- Bleep: the word is said in full; S heard, bleep over the rest (answer 13).
- Sound effects (rule 26): Sam sends the saber sounds (ignition, hum, three swings, a slice sizzle per cut; Star Wars
  sounds stay OFF GitHub). I make in code: leap push-off and landing thump, pieces hitting the floor, chair creak, steam
  hiss. Placeholders are named in every send until his arrive.
- Eyelines: shot 1 presenter to camera (audience); shot 2 Netanyahu to presenter; shot 3 Maul to presenter, held and
  still; shot 4 all to presenter, then the presenter's eyes flick to the camera and back; Maul on the chair glares around;
  shot 5 Netanyahu looking at Maul on the chair.

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py FILM sketch OUT.jpg`); places benchmarked against
references in `BENCHMARK` (rule 3, `python3 source/benchmark.py FILM OUT.jpg`)
The plan (metres, the studio's own: x east = screen right, z north = away from the cameras; facing in plan degrees,
180 = towards the cameras). The rough sheet's code holds these numbers: `source/netan_yahoo_comp.py` (copy into the film's
`PLAN` and cameras when building; run `python3 source/netan_yahoo_comp.py OUT.jpg` from the repo root).
- Everyone stands in front of the ring desk's open front, in a shallow line (Sam's layout photo), 1.8 m apart:
  presenter (-1.8, -0.8), Maul (0.0, -0.65), Netanyahu (1.8, -0.95).
- FACING (Sam, 26 Oct): bodies and heads face each shot's CAMERA (our people look less good at a diagonal); only the
  EYES turn: the presenter's to the candidates (screen right), the candidates' to the presenter (screen left). Building
  must add eye direction (`sp['look']`) to the Netanyahu and Maul heads: they ignore it now (the presenter's reads it).
- REVEALS (Sam, 26 Oct): neither candidate is seen before his line. Shot 1 is straight in front of the presenter, tight
  enough that Maul's blades stay out (checked on the sheet); shot 2 shows no Maul. Shot 4 is the first time all three
  are seen together.
- Chairs (wooden armchairs on blue pools): 0.75 m straight behind each person. The presenter's is Maul's goal.
- Maul's leap-flip: from (0.0, -0.65) to a crouch about 0.85 m in front of the presenter: about 1 m of travel, mostly
  UP (the flip). Spacing is 1.8 m, not the photo's 2.5-3 m: the phone's tall frame cannot hold three people wider apart
  at a readable size.
- The pile: where the presenter stood, falling towards his chair. Maul then springs onto the chair (seat 0.46 m).
- Cameras: s1 at (-1.8, 1.65, -5.4), straight in front of the presenter, zooming in (lens 2400 to 5200) from full
  figure to waist up; s2/s5 (1.8, 1.62, -3.05) straight in front of Netanyahu, chest up; s3 (0.0, 1.62, -2.75) straight
  in front of Maul, the same framing; s4 (-3.2, 1.6, -4.6), FRONT-LEFT (Sam, 26 Oct: "closer to the
  action", half the old wide was darkness): the presenter nearest and biggest, the line receding to Netanyahu; all
  three head to foot at the question (lens 1520, aim (-0.3, 1.1, -0.75)); it PUSHES IN as Maul ignites, ending on Maul
  crouched on the presenter's chair with the pile in front (lens 2050, aim (-1.35, 1.05, -0.35)); Netanyahu leaves the
  frame during the push (his reaction is shot 5). The presenter is screen-left whenever the candidates are in shot.
  To refine when building: the presenter's hand touches the left edge at the start (rule: nobody touches the edge);
  the bottom quarter is dark studio floor (TikTok's caption bar sits there).
- Hook Text: the dark ceiling band at the top of every shot; the floor at the bottom of the wide is left clear (TikTok's
  caption bar).
- To fix when building: the Hebrew caption on the big screen is far too small (the set's old caption box): make it big
  across the screen; the people in the wide are about a quarter of the frame tall (the photo's angle in a tall frame).

Composition sheet sent: 26 Oct, the plan and the key shots (`source/netan_yahoo_comp.py`; sent in the planning chat); second version 26 Oct after Sam's notes (face the camera; no candidate before his reveal); third, shot 4 closer (front-left, pushes in). Sam: "let's build" (26 Oct).
## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note | done? |
|---|------|------|
| 1 | Satire style, TikTok; follow satire.md and film-quality-rules; start from `source/satire_template.py` | |
| 2 | Plan only until Sam says go; nothing built or shown before sound effects and references are requested and questions asked | |
| 3 | Israeli news presenter, younger and more energetic than the built one, serious in role | |
| 4 | Introduces two candidates in a "prime ministerial debate"; everyone standing, chairs behind them (all stand throughout) | |
| 5 | Netanyahu introduced as "liberal moderate gently-gently incumbent Prime Minister Netanyahu"; nods in acknowledgement | |
| 6 | Darth Maul introduced as "Sith Lord and Scourge of the Galaxy"; glowers from under his hood; bloody-eyed menace | |
| 7 | Presenter asks Maul about the West Bank; awkward silent beat while Maul stares | |
| 8 | Presenter's eyes flick to the camera briefly, then back | |
| 9 | Maul ignites his twin lightsaber, leaps acrobatically, forward roll, lands in a predatory crouch | |
| 10 | Presenter alarmed; Netanyahu mildly surprised | |
| 11 | Maul slices the presenter into a pile of steaming chunks: fluid, fast, cuts match where the strikes land | |
| 12 | Maul steals the presenter's seat, leaps on it like a cat guarding territory, menacing and triumphant | |
| 13 | Netanyahu, surprised and a bit impressed: "Shit, he's good"; subtitle "S***", said in audio, S heard and the rest bleeped | |
| 14 | Shock level 3; gravity, nothing fully cartoony; no blood; clean cuts; accurate lightsaber sound effects and visuals (soft glow) | |
| 15 | Screens in the background: News logo and "Prime Ministerial Debate 2026" in Hebrew (answer 14) | |
| 16 | Shot 1: zoom in across the studio to the presenter, mid-large to mid-close | |
| 17 | Shots 2 and 5: close shot on Netanyahu; shot 3: the matching close shot on Maul, staring still at the presenter | |
| 18 | Shot 4: mid shot with all three and the presenter's chair | |
| 19 | Hook Text: "Israeli Prime Ministerial Debate"; CranbriJoos sign-off at the end (standing rule) | |
| 20 | Dialogue recordings arrive later in the day | |
| 21 | No set dressing added (Sam: real sets are very clean) | |
| 22 | Presenter's chair: a third wooden armchair behind him | |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|---|---|
| Pack 1, Maul movement (26 Oct; `references/maul/maul-7..11`) | | |
| `maul-11-aerial-flip` (stunt photo) | the "forward roll" done IN THE AIR: a forward flip off a springboard, upside down at the top, knees tucked, cloak billowing out, staff held upright in one hand, hood up going in | to build (leap-flip); my choice: the roll is this aerial flip, not a roll along the floor |
| `maul-9-leap-tuck` (figure) | the top of the leap: knees tucked high, body tilted back, free hand reaching up and out with fingers spread, saber arm low, cloak and skirts flaring below, snarl | to build |
| `maul-7-landing-crouch` (painting) | the predatory crouch: one knee near the floor, the other foot planted, free hand's fingertips splayed on the floor in front, head low and eyes up glaring, hood down, cloak pooling round him, staff held out to the side, both blades lit | to build; also the model for the crouch on the chair (answer 11) |
| `maul-10-wide-guard` (figure) | ready stance after ignition: feet very wide, knees bent, saber hand raised back with the blade up, free arm flung out sideways, fingers spread, sash and skirts flaring | to build (from 'attack' pose) |
| `maul-8-low-lunge` (photo) | follow-through after a strike: deep lunge, torso twisted, staff diagonal across behind him with both blades lit, free hand forward and open, looking back over his shoulder | to build (from 'strike' pose) |
| saber look (refs 8, 9, 10) | blades: a near-white core with a red edge and a soft red halo; hilt silver with black grips | answer 10: soft glow, blades only |
| Pack 2, lightsaber wounds (26 Oct; `references/netan-yahoo/wound-1..4`) | | |
| `wound-1-blade-through-torso` | the moment of contact: a bright flare where the blade meets the body (white-yellow centre, orange round it), the cloth round the cut glowing, the blade's far end showing through | to build: a flare at each strike for a few frames, lumpy (house style, rule 15) |
| `wound-2-arms-cut-sparks` | a limb cut through: a burst of orange sparks and embers and a puff of grey smoke at the cut; the sleeve end left glowing orange | to build: sparks and flat smoke from the kit (`prepper_fx.py`), at each cut |
| `wound-3-arm-on-floor` | a cut-off arm lying flat on the floor, the sleeve end towards us, the hand curled beyond it | to build: how the pieces lie. Its BLOOD is left out (brief: no blood): cut ends are scorched black |
| `wound-4-stab-reactions` | the person struck: back arched, head thrown back, mouth open, arms jerking up; the striker close and driving through | to build: the presenter's reaction as each strike lands (after he raises his hands, answer 8) |
| cut edges (refs 1, 2) | edges start glowing bright orange and cool | answer 9 updated: rims glow bright orange at the cut, cool to a thin orange line on black over about a second; then wisps of steam on the pile |
| Pack 3, debate layout (26 Oct; `references/netan-yahoo/debate-layout.jpg`): Sam wants THESE angles and perspective | | |
| `debate-layout` (UK TV debate) | three people standing in a shallow line across the stage, about 2.5-3 m apart, full bodies, feet visible; the presenter at the LEFT end turned three-quarter towards the candidates; the candidates turned three-quarter back towards him and the camera; the right-hand end of the line slightly nearer the camera; camera in front, a little left of centre, a little above head height and tilted slightly down, wide enough for all three with room above; a big screen on the back wall at head height between the presenter and the middle person (our Hebrew caption goes there); a large round dark floor graphic in front of them; curved blue and purple light strips on the back wall; clear glass lecterns | to plan: this is shot 4's framing and the basis of every camera. Lecterns LEFT OUT (not in the brief; chairs behind them instead; asked Sam) |
| Pack 5, Netanyahu surprised (26 Oct; `references/netan-yahoo/netanyahu-*.jpg`) | | |
| `netanyahu-surprised` | both brows raised high, inner ends highest; deep forehead lines; eyes wide, looking up and off to one side; mouth open mid-word, lower lip dropped; head tilted a little; three-quarter view; red tie, flag pin | to build: shot 5 as the line is said, and the "mild surprise" in shot 4 at a smaller strength |
| `netanyahu-impressed` | one brow raised higher than the other; lips pressed together, corners slightly down; eyes turned sideways; a wry, sizing-up look; blue tie | to build: shot 5's hold after the line ("a bit impressed") |
| shot 5 face, my plan | cut in on the surprised face; says "S***, he's good" with it; settles into the pressed-lips, one-brow look and holds | the strength sheet (answer 12) shows both faces at 1-6 |
| tie, my choice | red (stands out against the blue studio at phone size) | Sam to say no |
| still requested | DONE: wound look (pack 2), debate layout (pack 3), Netanyahu faces (pack 5); DROPPED: the cat (Sam: a metaphor; described instead, answer 11); STILL TO COME: a presenter type (optional), the saber sounds | |

## Notes from Sam (numbered; mark each done as it is fixed)
| # | shot | time | note | status |
|---|------|------|------|--------|
