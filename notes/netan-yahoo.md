# Notes for Netan-Yahoo! (brief: `prompts/netan-yahoo.md`; code to come: `source/netan_yahoo.py` from `source/satire_template.py`)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **26 Oct, 16:45: FINISHED and sent.** Final render (1080x1920, 10 min 20 s) finished with the hook + CranbriJoos sign-off:
  `animations/netan-yahoo-vertical.mp4` (4.0 MB, 35.4 s). Sam approved animatic 3 ("smashed it") but for Maul's glance in the
  wide shot (his face is drawn mirrored there: fixed in `_maul_look`). Pre-flight named, not fixed: PROP TURN (the all-angle
  staff test; never seen from behind in the film) and portal (the flat LED-blue screen seen through the glass).
- **Still open:** Sam's call on Maul's skirt panel (said nothing: left as is); Hebrew caption is my Hebrew (needs a Hebrew
  reader); rule proposal 12 held for the learnings message (see the end of this file); new kit items (this film's set,
  cast, pile pieces, `hook_text --w`) still to add to `guides/kit-catalogue.md` / `source/catalogue.py`; `story/status.md`.
- **Done (26 Oct, building chat, Opus):** the film module `source/netan_yahoo.py` (plan `source/netan_yahoo_plan.py`)
  with all five shots, the action, the 3D pile, sound and subtitles; Sam's cast notes 1-5 fixed (see "Notes from Sam");
  pre-flight clean but for shot 4's length (the brief's one continuous shot, chosen); first animatic rendered and sent
  (`--small`). WAITING for Sam's notes on the animatic.
- **Without numba:** pypi is refused for this session, so `lying.py` runs its 3D loops with numpy (about 5 s a body at
  frame size). Allowing pypi.org (claude.ai Settings, Capabilities) would make it about 20 times faster.
- **Recordings:** `source/audio/netan-yahoo-1..5.m4a` (voices.py: all fit, no duplicates). Sam's six saber sounds are
  in `source/audio/netan-yahoo-sfx/` and kept OFF GitHub (.gitignore): a new chat must ask Sam to re-attach them.
- **Next:** Sam's animatic notes (reading notes: Opus medium); the skirt panel is his call on the animatic.
- **My own critique still open:** the pieces are flat cut-outs turned to lie (a pile, but 2D); the flip is the drawing
  turned on screen (true for shot 4's camera); Maul's skirt panel stays stiff in the strikes; the saberstaff is not a
  solid in the collision audit (the strikes on the presenter are meant contact anyway).
- **Losses and my additions Sam should know about:** everyone 0.1 m nearer the disc's centre (chair fix). Additions:
  thump, pieces landing (Sam's body-falling sound), chair creak, steam hiss (sounds, my code), sparks and smoke at the
  cuts, steam wisps, hood falling back. No saber hum (none sent). No set dressing.
- **Ambition estimate (rule 24, estimate):** about 12-18% of a week; the action is the cost.
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** this file, `prompts/netan-yahoo.md`, `source/netan_yahoo.py`, `guides/satire.md`,
  `guides/film-quality-rules.md`.

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
- POSITIONS (Sam's sketch, 26 Oct, `references/netan-yahoo/layout-sketch.jpg`): a horseshoe round the floor disc,
  open to the audience. Presenter left (-1.13, 1.42), NETANYAHU at the back a little right of centre (0.41, 2.27),
  MAUL right (1.15, 1.2) (Sam swapped these two, 26 Oct); all about 1.15 m from the disc's centre (0, 1.2).
- FACING (Sam, 26 Oct): bodies and heads face each shot's CAMERA (our people look less good at a diagonal); only the
  EYES turn: the presenter's to the candidates (screen right), the candidates' to the presenter (screen left). Building
  must add eye direction (`sp['look']`) to the Netanyahu and Maul heads: they ignore it now (the presenter's reads it).
- REVEALS (Sam, 26 Oct): neither candidate is seen before his line. Shot 1 is straight in front of the presenter, tight
  enough that Maul's blades stay out (checked on the sheet); shot 2 shows no Maul. Shot 4 is the first time all three
  are seen together.
- Chairs (wooden armchairs): each 0.6 m behind its person, outwards from the disc's centre (clear of his legs, and
  of the desk's inside edge), every chair TURNED towards a point in front of the disc (0, -0.5): angled to each other
  as for a conversation, open to the audience (Sam). NO blue spotlight pools or chair shadows (Sam: they clipped).
- Maul's leap-flip: from (1.15, 1.2) to a crouch 0.85 m from the presenter, towards Maul: about 1.4 m of travel,
  right to left across the front of the disc, passing in front of Netanyahu. The pile: where the presenter stood; his chair is behind it, so Maul springs over the pile.
- Cameras (all in `source/netan_yahoo_comp.py`): s1 from front-right (2.5, 1.65, -1.5), zooming in on the presenter
  (lens 2600 to 5200), both candidates out of frame (checked); s2/s5 (0.2, 1.62, 0.2) on Netanyahu, chest up, Maul out
  of frame (checked); s3 (0.6, 1.62, -0.85) on Maul, the same framing, Netanyahu out of frame (checked); s4 (-1.0, 1.6, -3.6): all three head to foot inside the
  disc, the presenter nearest, Netanyahu between them at the back, Maul nearest on the
  right with his saber (lens 1420), then it PUSHES IN as Maul ignites,
  ending on Maul crouched on the presenter's chair with the pile in front (lens 2050); Netanyahu leaves the frame
  during the push (his reaction is shot 5). The presenter is screen-left whenever the candidates are in shot.
- Draw order to build properly: the ring desk is one item sorted by one point, so it drew over Netanyahu; the sheet
  cheats. Building splits the desk into pieces (satire.md: nearer is always on top).
- Hook Text: the dark ceiling band at the top of every shot; the floor at the bottom of the wide is left clear (TikTok's
  caption bar).
- To fix when building: the Hebrew caption on the big screen is far too small (the set's old caption box): make it big
  across the screen; the people in the wide are about a quarter of the frame tall (the photo's angle in a tall frame).

Composition sheet sent: 26 Oct, the plan and the key shots (`source/netan_yahoo_comp.py`; sent in the planning chat); second version 26 Oct after Sam's notes (face the camera; no candidate before his reveal); third, shot 4 closer (front-left, pushes in); fourth, everyone inside the floor disc; fifth, Sam's horseshoe sketch, chairs angled, no pools; sixth, Maul and Netanyahu swapped; seventh (building chat), the chairs clear of the desk. Sam: "let's build" (26 Oct).
## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note | done? |
|---|------|------|
| 1 | Satire style, TikTok; follow satire.md and film-quality-rules; start from `source/satire_template.py` | done: `source/netan_yahoo.py` (the template's wiring; the 3D set parts as Prepper's) |
| 2 | Plan only until Sam says go; nothing built or shown before sound effects and references are requested and questions asked | done (planning chat; Sam said go) |
| 3 | Israeli news presenter, younger and more energetic than the built one, serious in role | changed by Sam (26 Oct): the bearded presenter as built; energetic: quicker head moves, more upright |
| 4 | Introduces two candidates in a "prime ministerial debate"; everyone standing, chairs behind them (all stand throughout) | done: all three stand throughout, chairs behind (answer 3) |
| 5 | Netanyahu introduced as "liberal moderate gently-gently incumbent Prime Minister Netanyahu"; nods in acknowledgement | done: line 2; the nod on "Netanyahu" (`NOD`) |
| 6 | Darth Maul introduced as "Sith Lord and Scourge of the Galaxy"; glowers from under his hood; bloody-eyed menace | done: line 3; hood up, the glare, unblinking |
| 7 | Presenter asks Maul about the West Bank; awkward silent beat while Maul stares | done: line 4; silent beat 20.5-22.3 s, Maul still |
| 8 | Presenter's eyes flick to the camera briefly, then back | done: `FLICK` 21.05-21.45 s |
| 9 | Maul ignites his twin lightsaber, leaps acrobatically, forward roll, lands in a predatory crouch | done: ignition (the sound leads), leap-flip (hood back), crouch landing |
| 10 | Presenter alarmed; Netanyahu mildly surprised | done: presenter alarm, hands up before the blows; Netanyahu mild surprise (1) |
| 11 | Maul slices the presenter into a pile of steaming chunks: fluid, fast, cuts match where the strikes land | done: three strikes, cut lines where they land, four 3D pieces into a pile, steam (Sam's note 4: lying.py) |
| 12 | Maul steals the presenter's seat, leaps on it like a cat guarding territory, menacing and triumphant | done: springs onto his chair, crouched, head snapping round |
| 13 | Netanyahu, surprised and a bit impressed: "Shit, he's good"; subtitle "S***", said in audio, S heard and the rest bleeped | done: line 5; S heard, bleep from the vowel (rule 27); subtitle S*** |
| 14 | Shock level 3; gravity, nothing fully cartoony; no blood; clean cuts; accurate lightsaber sound effects and visuals (soft glow) | done: no blood, scorched cuts; soft glow on blades only; Sam's sounds (no flare, Sam 26 Oct) |
| 15 | Screens in the background: News logo and "Prime Ministerial Debate 2026" in Hebrew (answer 14) | done: the debate caption big on the screen; the News logo is the floor graphic's (not on a screen) |
| 16 | Shot 1: zoom in across the studio to the presenter, mid-large to mid-close | done: shot 1 zooms in (lens 2600 to 5200) |
| 17 | Shots 2 and 5: close shot on Netanyahu; shot 3: the matching close shot on Maul, staring still at the presenter | done: shots 2/5 on Netanyahu; shot 3 the matching close on Maul (answer 5) |
| 18 | Shot 4: mid shot with all three and the presenter's chair | done: shot 4 wide with all three and the presenter's chair, pushing in |
| 19 | Hook Text: "Israeli Prime Ministerial Debate"; CranbriJoos sign-off at the end (standing rule) | done: `HOOK`; finish.py adds the Hook Text and the CranbriJoos sign-off |
| 20 | Dialogue recordings arrive later in the day | done: five recordings in (`source/audio/netan-yahoo-1..5`) |
| 21 | No set dressing added (Sam: real sets are very clean) | done: no set dressing |
| 22 | Presenter's chair: a third wooden armchair behind him | done: a third armchair behind him |

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
| 1 | cast | - | presenter's three-quarter looks like another man (glasses, face like Burnham); shirt and tie wrong | done: his own three-quarter head from his front drawing (`newsdesk_cast.head_view`); shirt V under his chin (`v_at`, views) |
| 2 | cast | - | everyone thinner in head and body on the eyes row | done: the sheet squeezed the crops (sheet bug, not the cast); crops now keep the tile's shape |
| 3 | 4 | strikes | small explosions at the strikes not needed | done: the flare removed; sparks and a little smoke kept (pack 2) |
| 4 | 4 | pile | pieces must be 3D like bodies on the ground; slump fully to the floor; a little further from the chair | done: lying.py pieces (scorched faces), falling under gravity, flat on the floor, the pile 0.38 m further out (towards us) |
| 5 | - | - | presenter: the bearded one; Netanyahu strength 4 on both shot 5 faces; skirt panel: decide on the animatic | done; done; open (animatic) |
| 6 | 5 | 28.5- | the pile stuck over Netanyahu; it has no reason to be in the shot | done: the settled pile's saved drawing had no camera in its key, so shot 4's copy was pasted into shot 5; keyed by camera now |
| 7 | 1 | 0.5- | subtitle: "It's time to introduce the candidates for tonight's debate" | done |
| 8 | 1 | 0-3.95 | Hook Text in the animatic, on his left, with 😅 at the end | done: screen left beside his head (his own left has no room as the camera pushes in), three rows (hook_text --w), stamped on the animatic; hookcheck clear |
| 9 | 4 | to 22.3 | Maul stares to the right, not at the presenter | done: turned 40% towards the presenter before and at ignition; iris travel 0.4 -> 0.55 |
| 10 | 4 | - | zoom in a little | done: lens 1420 -> 1650 (leap and strikes still in frame) |
| 11 | 4 | pile | pieces float / sit on each other; shadows show; head's neck end looks like an eye | REPEAT of note 4. Why it failed: fixed turns, then dropped to the lowest point only (balanced on one point), and no check between pieces. Now: each piece settles on its broadest side (lowest centre of weight), kept out of the others, head with the neck end turned away; shadow only where it touches (reach 3 cm) |

## Rule proposals held for the end-of-project learnings message (Sam, 26 Oct: "save it, we discuss it then"; NOT in a guide yet)
- **Proposed rule 12 (guides/film-quality-rules.md, check: by hand on the check sheet, or a tool later):** "Pieces or bodies
  that fall must settle on their broadest side (lowest centre of weight), must not overlap or rest on one another, and
  cast a shadow only where they touch the floor. Any saved ('cached') drawing must record which camera it was drawn for,
  so it can never be reused in a shot with another camera." (From notes 6 and 11, Netan-Yahoo!, 26 Oct.)
- Also for that message: the hook can now sit beside a person (`hook_text.py --w`, three rows); `1f605.png` emoji added.
