# Notes for Netan-Yahoo! (brief: `prompts/netan-yahoo.md`; code to come: `source/netan_yahoo.py` from `source/satire_template.py`)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **Done (26 Oct, planning chat, Opus):** questions sent in one message, all answered (below); sound effects and references
  asked for. "President" changed to "Prime Minister" in the brief and script (Sam). Nothing built, no pictures, no render.
- **Next:** wait for Sam's references and sounds (incoming). Then, still PLANNING in this chat: check the references
  (missing ones named), the plan in metres, the composition sheet (rule 11). Then BUILDING (presenter variant, leap-roll,
  cuts and pieces, saber glow, Hebrew screens, sound): Opus, high effort, fresh chat. Sam: "begin build once happy with
  references".
- **Already built (Newsdesk building chat):** the studio (`source/newsdesk_set.py`), the presenter (`newsdesk_cast.py`,
  `PRESENTER`), Netanyahu (`netanyahu_cast.py`), Maul with the double-bladed saber and four poses (`maul_cast.py`), the
  wooden armchairs (`newsdesk_props.py`). Details: `notes/newsdesk.md`. Sam has no notes on the Maul sheet.
- **Losses and my additions Sam should know about:** additions he approved: leap and landing thump, pieces hitting the
  floor, chair creak, steam hiss (sounds; my code); the steam wisps; the hood falling back in the roll. Set dressing: NONE
  (Sam: the real sets are very clean); no ON AIR light, no desk props, no news sting, no studio ambience.
- **Ambition estimate (rule 24, estimate):** cast and set built; the cost is the action. About 12-18% of a week. Sam took
  no trims.
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** `prompts/netan-yahoo.md`, this file, `notes/newsdesk.md`, `story/status.md` (Newsdesk section only).

## Sam's answers (26 Oct, to the questions in one message; "yes" = my recommendation)
1. Maul sheet: no notes; use him as built.
2. Presenter, younger: same navy suit and glasses; no beard, no grey; darker, fuller hair; quicker head moves; more upright.
3. Staging: all three STAND the whole film, on the open floor in front of the desk: Netanyahu screen left, presenter centre,
   Maul screen right about 4 m from the presenter (room for the leap). The brief's "in his chair" (shot 2) is overruled.
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
(To do at planning: the built studio, screens upstage with the Hebrew text, three chairs and the presenter's chair set, a camera for each shot.)

Composition sheet sent: (rule 11: the 3-4 key shots, before building; write the date and file here once Sam has it.
Pre-flight refuses to run until this line has them, and while any "done?" box below is blank: rule 14)

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
| still requested | a lightsaber cut look (DONE, pack 2); a debate layout; a cat guarding a spot; Netanyahu surprised or impressed; a presenter type (optional); the saber sounds | |

## Notes from Sam (numbered; mark each done as it is fixed)
| # | shot | time | note | status |
|---|------|------|------|--------|
