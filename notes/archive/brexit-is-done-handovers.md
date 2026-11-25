# Brexit Is Done: old handovers

## Chat 1 handover (archived chat 2) (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Rules that bite next:** 89 (critique before the sheet goes back), 49 (likeness), 30 (a repeat note: find why the first fix failed).
- **Done (chat 1):** May/Blair faces, hair pieces bob/back, hard hat, specs, workwear; cast sheet v1 sent; Sam's notes saved
  (`notes/sam-notes/brexit-cast-v1/notes.md`, 3 notes + "your fresh eye points are true too"). Sam said Y to the plan.
- **Next (chat 2, Opus medium, notes round):** 1 one shape for each new hair piece in every view (the turned crown clamp at -0.44
  in `_turn_hair0` flattened Blair; turned hair must match the front's height and width); 2 Kemi: orange shoulders and sleeves,
  navy chest only (her photo), turned hat sits flat/wide, glasses run off the face; 3 May's age lines stronger, reads as a woman
  at full height; Blair's side/back hair not a plain cap; the dark dash on the crown in three-quarter heads; 4 the new check:
  front|3/4 pair at one scale, hair and clothes measured in both, fault past 15%, tested on Sam's 3 saved notes; the sheet
  maker refuses a figure touching a tile edge; 5 critique hunts, then cast sheet v2 to Sam with full figures.
- **Needs Sam:** notes on v2; the script; the site; Blair's place.
- **Read:** `guides/job-packs.md` Notes round; `source/facehouse.py` MAP and `_turn_hair0`, `bob_shapes`, `back_shapes`, `turned_hat`.
- **Open rule requests:** none (the new check goes through the proposal route if it becomes a rule).
- **For Claude:** `python3 source/people.py sheet brexit-is-done OUT.jpg`; `facehouse.py turns OUT.jpg may blair`; Sam's sheet
  was assembled by hand in chat 1 (crops of the people sheet): build it in a tool this time.


# Chat 2 handover (moved by chat 3, 23 Nov)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Rules that bite next:** 30 (a repeat note: find why the first fix failed), 49 (likeness), 89 (critique before a sheet).
- **Done (chat 2):** Sam's 3 cast notes fixed in the shared tools: one hair shape in every view (hair shell), side/back
  strokes, Kemi's hi-vis as her photo, turned hard hat, far braids, May's age lines and patterned blouse, narrower
  shoulders; `castsheet.py` (sheet + front/3/4 match, tested on Sam's 3 notes); kittest N26 fixed (archived notes name).
  Two critique hunts; 6 left open as named (likeness taste on faces Sam picked; Blair's 3/4 shirt and tie do not turn).
- **Next (chat 3, Opus high: a new build and the plan):** on Sam's Y, a woman's build in the shared body kit (narrower
  shoulders, waist, hips, jacket cut, shoes) for May and Kemi; Kemi's yoke stops at her collar (notes 5-6); then the
  plan from the script ("Open Wounds", brief items 4-12): sets, the wolves from Cry Minister on the new kits, estimate.
- **Needs Sam:** the woman's-build ask was withdrawn (no proposal behind it): chat 3 puts it through the proposal
  route first (`propose.py new womans-build`), then asks Sam; notes on the next sheet.
- **Read:** `guides/job-packs.md` Notes round; `source/castsheet.py` MAP; `source/facehouse.py` `_turn_hair0`, `turned_hat`.
- **Open rule requests:** none (the front/3/4 match may become a rule: proposal route first).
- **For Claude:** `python3 source/castsheet.py sheet brexit-is-done OUT.jpg`; `castsheet.py match brexit-is-done`;
  `castsheet.py selftest`; Blair's 3/4 tie box is the kit's three-quarter suit torso (views.WrapPen 'three').



# Chat 3 handover, with chat 4 lines (archived chat 4, 23 Nov)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Rules that bite next:** 30 (note 5 is a repeat of GTA's "Lucia on a man's box body"), 49 (likeness), 89.
- **Done (chat 3):** note 6 fixed (Kemi's orange stops outside her collar, any build); note 5 through the proposal
  route (judged: helper B's, 8 found, 4 fixed, 4 named; sent to Sam as two options); Sam's v2 notes saved with
  pictures; reserve list made (Sam: 6+6 body shapes and today's tool chats, notes/next-jobs.md R1-R6).
- **Chats are named "Open Wounds"** (Sam, 23 Nov); the film's files keep the name brexit-is-done.
- **Chat 4 so far (paused by Sam at 22:24, restart 23:51 UK):** learn step done (notes/learn/womans-build/learn.md:
  as drawn, May and Kemi read as men in all 10 views). Change 1 half built, not yet checked: `woman`/`man` in the body
  line (people.SEXED, BEFORE_SEX; load refuses a new film's person without it), face-tool people now keep their body
  line, crowd women flagged, new build body.FIGS 'female' (old 'woman' kept for GTA) with arms out a little
  (views.standing). Sam's note 7: right for May, wrong for Kemi ("just does not have that body").
- **Next (chat 4 on restart, Opus high):** Kemi's own build, measured from several photos of her (Sam 22:28: "maybe check a few photos"; full-length, standing, the search order in guides/job-packs.md Plan; her likeness, so her photos are right here, unlike the general body's size charts), never guessed (Sam: not 'slimmer' than May),
  then run the kit tests on finished films, the cast-sheet check (fails both n5, passes Lucia and Blair), Change 2
  (neckline first: May's striped blouse reads as a tie), cast sheet v3 to Sam.
- **Two chats from 23:50 (Sam: "continue the character work here and pass off sets and other essential film work to
  another chat"):** chat 4 (this one) keeps the people: May, Kemi, Blair, the woman's body, its check, cast sheet v3.
  The sets chat (Opus high, planning) does the plan for brief items 4-18: the three places (May's dark wood-panelled
  interview room, Kemi's building site under a grey sky, Blair's oak-panelled room), the wolves (a new animal: the
  kit catalogue first), the background action, the blood plan (Q2, still waiting for Sam's Y), the estimate and the
  shot board. It never edits people.py, body.py, views.py, castsheet.py or story/brexit-is-done-people.txt (chat 4's),
  writes its notes in notes/brexit-is-done-sets.md, and pushes only to its own branch; chat 4 merges both onto the
  main line once its checks pass.
- **Kemi's photos (chat 4, 23:52):** one try per source, none full length: Wikimedia (refused: too many requests),
  BTA's AP gallery (pictures load by script), news pictures (Irish News/PA at the lectern, waist up; GB News a face),
  Alamy (pictures load by script). Asked Sam for 2-3 full-length standing photos.
- **Needs Sam:** 2-3 full-length photos of Kemi standing (chat 4); Q2 blood plan (item 18): his Y goes to the sets chat.
- **Read:** `guides/job-packs.md` Build; notes/proposals/womans-build.md "Final version"; notes/sam-notes/brexit-cast-v2/.
- **Open rule requests:** none (the proposal's check becomes a rule only with Sam's Y).
- **For Claude:** `castsheet.py sheet brexit-is-done OUT.jpg`; build switch `body: ..., build woman` (body.FIGS);
  chat 3's try: scratch kemi_torso.py style draw via castsheet.draw(sp, yaw, PP).
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/brexit-chat4`** (not on the main line: its people code is not yet tested on finished films). The sets chat (chat 5, session_01U3pKQzpCX39nxRRegF2T7U) works the places, wolves and estimate on its own branch; merge both.
- **Rules that bite next:** 30 (note 5 repeats GTA's Lucia), 49 (likeness: Kemi's build from her photos), 89.
- **Done (chat 4):** learn step (notes/learn/womans-build/learn.md: as drawn, May and Kemi read as men in all 10 views; the cast's body lines never reached face-tool people). Change 1 half built: `woman`/`man` in the body line (people.SEXED, BEFORE_SEX; load refuses a new film's person without it), face-tool people keep their body line, crowd women flagged, body.FIGS 'female' (GTA's 'woman' kept), arms a little out (views.standing). Sam's note 7: right for May, wrong for Kemi.
- **Next (chat 6, Opus high: new build):** Kemi's own build from Sam's full-length photos (he is asked for 2-3; measured, never guessed; not slimmer than May; shown beside the photos); kit tests on finished films (each must draw as before); the cast-sheet check (fails both n5 pictures, passes Lucia as a woman and Blair as a man; wired into handover end, which now lists castsheet as UNWIRED); Change 2 (neckline first: May's striped blouse in a narrow V reads as a tie); cast sheet v3 to Sam; merge chat 5's branch and push the main line.
- **Kemi's photos from Sam (23 Nov ~00:00):** references/brexit-is-done/kemi-full-1-portrait-sam.jpg (standing, front,
  dark blazer, cream dress), -2-seated-sam.jpg (perched on a sofa arm, legs crossed, heels), -3-walking-sam.jpg (white
  wrap top with a peplum, dark trousers). Measure her shoulders, waist, hips and legs from these; never guess.
- **Needs Sam:** Q2 blood (sets chat).
- **Read:** `guides/job-packs.md` Build; notes/learn/womans-build/learn.md; notes/proposals/womans-build.md "Final version"; note 7.
- **Open rule requests:** none.
- **For Claude:** learn drawings: notes/learn/womans-build/draw.py (draw2 style: sp['figure']='female', castsheet._setup); FIGS 'female', FIG_HEM in body.py; views.standing 'female' arms; Kemi's own build likely a second FIGS entry chosen by a `build` word on her body line.


### chat 6 (24 Nov)
- **Newest work: branch `claude/brexit-chat6`** (chat 4's and chat 5's branches merged in; not on the main line: the cast-sheet check refuses the handover, see Next).
- **Rules that bite next:** S12 (women's bodies: new, its check `castsheet.py build`), 30, 89.
- **Done (chat 6):** Kemi's own build `straight`, measured from Sam's 3 photos (notes/learn/kemi-build/measure.py; sheet notes/learn/kemi-build/measure-v1.jpg: bust 0.76, waist 0.74, hip 0.85 of the shoulders, drawn the same; May keeps 'female', approved by Sam). Cast-sheet build check (shape in 4 views, likeness to each woman's photos, the blind judge's record), wired into handover end; catches both n5 and note 7, passes Lucia and Blair (kittest `womens_builds`). Change 2 started: a woman's neckline (wide, shallow, blouse collar out, small lapels), front and three-quarter.
- **Blind judge, 2 rounds (notes/judge/brexit-is-done-cast.json):** Blair man in all 4 views. Round 2 (after the turned edges took the side's bust and seat, views TURNED_SIDE): May woman in all 4 (front, back 5; turned, seated 3). Kemi still fails: woman only 2 front and back ("could also be a man in a plain jacket"), MAN turned (2) and seated (3): "straight body, no waist".
- **Next (chat 7, Opus high: new build):** Kemi reads as a woman in every view WITHOUT changing her measured widths (handover end refuses until then: the judge's STOP lines). What is left to learn: her photos show a woman's straight build reads by clothes and posture (her blazer ends at the hip, the dress shows under it; her arms hang clear of the waist): try learn.md items 4-5 (arms, a jacket ending at the hip, the hi-vis shaped as in badenoch-hardhat-sam.jpg) and the seated torso; redraw (judge.py), a FRESH judge each round, save the record; then cast sheet v3; push the main line once end is clean.
- **Sets (chat 5, notes/brexit-is-done-sets.md):** three places built, wolves catalogued; it opens the wolves build chat once Sam answers.
- **Needs Sam:** Q2 blood, Q8 the four hardest moves, Q9 estimates (all asked by the sets chat).
- **Read:** `guides/job-packs.md` Build; notes/learn/womans-build/learn.md "What matters"; this section.
- **Open rule requests:** none.
- **For Claude:** FIGS 'straight' + WOMEN_FIGS, _womans_neckline/WOMAN_V in body.py; views.torso_view 'three' woman neckline, _built_outline 'straight' side; castsheet.build_faults / judge_faults / build_selftest; handover.castsheet_faults; Kemi's line `build straight`.



## Sets side, chat 5 (moved by chat 8, 24 Nov)
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's screen place and size (24 Nov).
- **Rules that bite next:** 41 (hands on the steel bars), 89 (each new wolf pose critiqued alone), 5 (physics: feet on boards, struck wolves react).
- **Done (chat 5):** sets plan (this file); 6 references; wolves catalogued; three places built as lines with 18 new shared pieces; places rough sent.
- **Next (chat 8, Opus high, new build):** the wolves as kit parts (spruce-up fixes 1-4, then walk, sit, paw, lunge-recoil, skid, hard hat and vest, blood stains per the approved plan), each critiqued alone; no shot staged. Shots then go in film order once the cast is approved (Sam, 24 Nov).
- **Needs Sam:** nothing (Q2 Y, Q8 film order, Q9 N: 24 Nov).
- **Read:** `guides/job-packs.md` Build; this file (wolves, background action, hardest moves).
- **Open rule requests:** none.
- **For Claude:** wolf.py (side, front, side_pose, head_side); places_site.py; preview of the views: the rough's place_tile at full size.

### chat 7 (24 Nov, before Sam's Y)
- **Newest work: branch `claude/brexit-chat7`** (chat 6's and chat 5 sets' at b21275a2 merged in; NOT on the main line: handover end stops on the judge, below).
- **Rules that bite next:** S12 (women's bodies, `castsheet.py build`: shape, likeness, crotch, judges), 30, 89.
- **Done (chat 7):** Kemi on her measured widths (0.76/0.74/0.85, unchanged): jacket to her hip, seat into the thighs, women's legs, turned bust ahead of the arm (each build at its own bust height), back's curve, seated knees together/hands near hips, her slimmer arms (`arms 24`); nubs fixed (neckline, yoke). Note 8 (camel toe) fixed and its check built (castsheet crotch_faults). Notes 10 and 11 (Blair's teeth 'fleshy'; a spike at his smile's corner) fixed, checks castsheet teeth_faults and mouth_spike_faults; both catch Sam's saved pictures, wired into build and handover end. Judges: three fresh a round, middle verdict (castsheet JUDGES); judge sheet blanks all hair. Cast sheet v3 sent: notes/learn/kemi-build/cast-v3.jpg.
- **Judges (notes/judge/brexit-is-done-cast.json):** May and Blair pass every view. Kemi front 3, back 3; turned and seated ON THE LINE: her identical drawing got 3/3/3 in both (v5d) then 2/2/2 (v5e, the record; judges compared her with May's figure: "like 1 but no hair strands"). More curve would go against her photos (note 7): Sam asked (Q1 below).
- **Known faults (fix next):** May turned: the bust bump reads pointed (TURNED_BUST female 28 at 140, SD 42: try wider/softer, keep the judge's 3); Kemi turned: the orange yoke's inner corner hangs as a tab under the near braid (people_parts.workwear_torso yoke, wrapped; on earlier sheets too).
- **Next (Opus high):** Sam's answer to Q1; the two known faults; judges again; kit tests (a full run on the final code: the chat 7 run was still going at handover); handover end clean; push the main line.
- **Needs Sam:** Q1: accept Kemi's turned and seated views as they are (on the line to body-only judges; clearly a woman with her head and braids), Y/N.
- **Read:** `guides/job-packs.md` Build; this section.
- **Open rule requests:** none.
- **For Claude:** views WOMAN_LEGS/WOMAN_LEG(_TURNED)/WOMAN_HIP_OUT/WOMAN_THIGH_IN/_hip_out/_thigh_edges/_seat_into_thighs/_woman_knee/TURNED_BUST(_Y); body.seat_hem/trouser_seat/_top_y; people `jacket 440`, `arms 24`; sitting.spec_upright women's branch; castsheet crotch_line/crotch_faults/teeth_share/teeth_faults/JUDGES; faces.house_mouth grin; judge.py hair blank.



### chat 8/7 handover (moved by chat 9)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: the main line** (chat 7 pushed it: chats 4-8 merged, the wolves kit included).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three centre right in May's place and size, May a little wider (note 9); the cast as on cast sheet v3 ("Y to Kemi, cast sheet is ready", 24 Nov).
- **Rules that bite next:** S12 (women's bodies, `castsheet.py build`), 41 (hands on the steel bars), 74 (each wolf's beats).
- **Done (chat 7):** the cast approved (notes/learn/kemi-build/cast-v3.jpg): Kemi on her measured build, a woman in every view (front and back to three blind judges, turned and seated by Sam's eye); notes 8 (camel toe), 10 (fleshy teeth), 11 (smile spike) fixed, each with a check catching Sam's picture (castsheet crotch_faults, teeth_faults, mouth_spike_faults); three fresh judges a round (JUDGES); all 139 kit tests passed (finished films unchanged).
- **Known faults, before May's shot:** May turned: the bust bump reads pointed (views.TURNED_BUST female 28 at 140, SD 42: wider and softer; her shot is turned); Kemi turned: the hi-vis yoke's inner corner hangs as a tab under the near braid (people_parts.workwear_torso); 7 closed curves through one point twice in facehouse hair (lines 987, 1042, 1056, 1156, 1385, 1570, 1639, 1651): look for spikes at full size. Any drawing change makes the judge record stale: three fresh judges again (Sam's Y covers only this drawing).
- **Next (chat 9, Opus high: the board and shots, new moves):** the known faults above, then the shots in film order (May, then Kemi with the site action, then Blair), per notes/brexit-is-done-sets.md (shot table, background action, the wolves kit).
- **Needs Sam:** nothing (his eye on the wolves sheet: any note goes to the sets chain).
- **Read:** `guides/job-packs.md` Build; notes/brexit-is-done-sets.md "Where things stand" and the shot table; this section.
- **Open rule requests:** none.
- **For Claude:** views WOMAN_LEG*/TURNED_BUST(_Y)/_seat_into_thighs; body.trouser_seat; people `jacket 440`, `arms 24`; sitting.spec_upright women's branch; castsheet crotch_/teeth_/mouth_spike_faults, JUDGES, judge record `sam_ok`; faces.house_mouth grin; wolf.py (pose, shadow, draw).


# chat 9
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat9`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three centre right in May's place and size, May a little wider (note 9); the cast (cast sheet v3 plus chat 9's three small fixes).
- **Rules that bite next:** 41 (hands on the steel bars), 74 (each wolf's beats), 5 (feet on boards, struck wolves react).
- **Done (chat 9):** the three known cast faults fixed: May's turned bust rounder (views.TURNED_BUST female 27, SD 52 at 145); Kemi's hi-vis side strip runs into the waist band (no tab under the braid; front shows orange sides, Added line told to Sam); hair and hat outlines through each point once (Kemi's turned hat nub gone) with check castsheet.hair_spike_faults (catches the old drawing; wired into build and handover end). Two rounds of three fresh blind judges (record v6b): May woman in all 4; Kemi 3/4 and seated 3; Kemi front 2 (Sam's Y on the same drawing), back 2 (Sam: move on from the characters).
- **Sam, 24 Nov (92% of the week used):** "We might have to move on from the characters now, please, as we are running out of space to complete the film!" No more character work: shots only.
- **Next (chat 10, Opus high: the board and shots, new moves):** write source/brexit_is_done.py (copy milburn.py's frame route: people.load, scale_at, person(), places.picture lines from story/brexit-is-done-places.txt), shots in film order (May, then Kemi with the site action, then Blair) per notes/brexit-is-done-sets.md shot table; `rough.py board` once May's shot draws.
- **Needs Sam:** nothing now; the chain is paused at the budget stop (92%).
- **Read:** `guides/job-packs.md` Build; notes/brexit-is-done-sets.md shot table and background action; milburn.py MAP and lines 130-150.
- **Open rule requests:** none.
- **For Claude:** views.TURNED_BUST(_Y,_SD per build); people_parts.workwear_torso `yl`; facehouse.curve (dedupes) over _curve; castsheet.hair_spike_faults(raw=True for the old); judge record sam_ok kemi front/back.


# chat 10 (first handover)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat10`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size on screen (face centre about 62-64% across, eyes on row 700), May about waist up (note 9); the cast (no more character work, Sam 24 Nov).
- **Rules that bite next:** 74 (May's hand gestures and head on her line), 41 (hands on the steel bars, shot 2), 5 (feet on boards, struck wolves react).
- **Done (chat 10):** source/brexit_is_done.py (milburn's frame route; MAP at the top): shot 1 draws: May seated turned screen-left in the slatted room, lens 1450 (wider than the 1800 plan, note 9), her chair shown (the tall frame shows her lap), a dark floor (Added). Board for shot 1 (story/brexit-is-done-board.txt) sent to Sam and recorded. Fixed in the film's code: the drawing scale set before the room paints (frame 1 lost the floor).
- **Next:** on Sam's Y to shot 1's board: Opus high: shot 2 (Kemi in May's place and size, the site, items 6-9 by the background-action table), its board row, then shot 3; May's gestures and lips (moves file) before the animatic. On a note: fix the drawing, never the camera he approved.
- **Needs Sam:** Y or N to shot 1's board (framing, the chair and floor showing).
- **Read:** `guides/job-packs.md` Build; notes/brexit-is-done-sets.md shot table and background action; brexit_is_done.py MAP.
- **Open rule requests:** none.
- **For Claude:** seated(img, who, L, X, d, t, yaw, pose, chair) draws anyone seated through a LevelCam; shot numbers live in dicts (MAY) because the board reads every upper-case number as a beat; board --shots 1 until shot 2 draws (picture raises NotImplementedError past 7.5 s).


# chat 10
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat10`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size (head top, eye row 700, chin, face centre about 64% across), May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7 (Sam, 24 Nov: "list it as a reserve job"), never worked on in this film.
- **Rules that bite next:** 74 (each wolf's and worker's beats; May's gestures), 41 (hands on the steel bars), 5 (feet on boards, struck wolves react).
- **Done (chat 10):** source/brexit_is_done.py draws all three shots (people placed and matched, places from the places file; Kemi's concrete frame moved back to 26 m so the grey sky shows; Blair's doors open on shot time). Board of all three sent to Sam and recorded. Sam's note 12 (seated knees, no bottom): a kit stopgap (views.knee_cap, views.seat_bottom), check castsheet.seated_faults, reserve job R7.
- **Next (Opus high: new moves):** shot 2's background action by the sets file's table (wolf.py kit; workers through standing(); dust and blood as approved), then shot 3's chase and the lunge, then the moves file (May's gestures, lips on stand-in timing, eyes off-frame left for all three: the `look` channel), then the Sonnet chat for the animatic (finish.py with the Hook Text and sign-off). Sam asked for the animatic next: no more boards unless he asks. The JUDGE stop is skipped by Sam's Override (24 Nov) until R7.
- **Needs Sam:** his eye on the board (any note to the next chat); nothing blocks.
- **Read:** `guides/job-packs.md` Build; notes/brexit-is-done-sets.md background action; wolf.py catalogue line; brexit_is_done.py MAP.
- **Open rule requests:** none.
- **For Claude:** rerun `python3 source/kittests.py` first (chat 10's full run was stopped mid-way; people_from_a_description passes after the SEAT_DROP name clash was fixed: the new constants are BOTTOM_*); shots' numbers live in dicts (MAY, KEMI, BLAIR) because the board reads upper-case numbers as beats; places.LevelCam.of(desc, view).



## Where things stood (chat 11) (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat11`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size (head top, eye row 700, chin, face centre about 64% across), May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7, never worked on in this film.
- **Rules that bite next:** 74 (the guests' and wolves' beats in shot 3; May's gestures), 5 (people through the doorway, never the wall; the tray lands), 41 (hands on the tray; tubes in hands).
- **Done (chat 11):** shot 2's whole background action by the sets table (source/brexit_is_done_action.py): W1 digs, Wa/Wb leap from the left, knock him down (lying.fall), feed out of step, his hat flies and rolls, the shovel falls flat, scraps, drops that land and soak, a pool; W2 sprints the 9.6 m lift and leaps out of frame left, Wc/Wd chase, skid, snarl, turn, pace back; W3-W5 jab tubes, We/Wf lunge and flinch, Wg circles, W5's swing stops on a standard; Wh sits, Wi paws (grooves stay), Wj/Wk walk across in hats and vests. Shared: places.paint_with (actors among pieces far to near), crowd `hats: hardhat` (people_hats.hardhat), figure.SIDE_ON (a side-on arm is read as side-on). Kit tests: all pass (womens_builds and kit_people_never_generic rerun alone after the mid-run edit).
- **Next (Opus high: new moves):** shot 3's chase and the lunge (room_actors in the action file: the four guests through the doors at 0.4, the tray, Wl-Wo after them, Wp's leap from frame right cut at 9.4 s; guests are crowd `guest` 0-3), then the moves file (May's gestures, lips on stand-in timing, all three looking off-frame left: the `look` channel), then the Sonnet chat for the animatic (finish.py, Hook Text, sign-off). No more boards unless Sam asks.
- **Needs Sam:** nothing blocks.
- **Read:** `guides/job-packs.md` Build; notes/brexit-is-done-sets.md background action (shot 3 table); brexit_is_done_action.py MAP; wolf.py catalogue line.
- **Open rule requests:** none.
- **For Claude:** views.person's returned points are person units from the neck base, unmirrored (action file's `_screen` turns them to pixels; move to shared: views); the site's outer scaffold seed went 3 -> 13 so no barrier hides the bar fight (dressing only); overrides.log recorded chat 10's prompt to this chat as "sam" because it quoted Sam's Override: source/override.py should count only Sam's own typed messages (move to shared fix, next chat checks it first).




# Chat 12 handover (moved by chat 13, 25 Nov)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/bold-maxwell-31au7y`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size (head top, eye row 700, chin, face centre about 64% across), May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7, never worked on in this film.
- **Rules that bite next:** 5 (nothing through anything: a runner's back foot near a wolf's jaws; the tray lands), 74 (May's gestures on her words), 89 (the chase's critique pack before the animatic).
- **Done (chat 12):** blind judge round on redrawn outlines (May and Blair clear; Kemi turned/seated woman 2, Sam's Y stands). Shot 3 built: 14 passes (the four through the doors, then back across, staggered), the tray flies on at the butler's swerve, hops and rattles flat, three glasses shatter into pools that stay, four wolves at their heels at the guests' pace, Wp leaps in above-right of Blair's head 9.0-9.33 at 2.3 m. Shared fixes: soft shadows were SOLID BLACK on every frame (ink.glaze; wolf._blend, shot 2 too); crowds made before the kit loads drew the bald stand-in head straight on (people.crowd_person; kittest kit_people_never_generic now catches it, example notes/learn/crowd-front-head/); front-on wolf 1.38x too big (wolf.FRONT_K); places.paint_with `beyond`: people in the corridor clipped to the doorway, behind the swinging leaves.
- **Next (Opus high: new moves):** first watch shot 3 whole at phone size and full size (python3 source/brexit_is_done.py stills OUT 17.5..26.9 every 1/12): legs at the new run stride (0.95 m), every wolf's jaws against the runner ahead, the tray and glasses; then its critique pack (rule 89); then the moves file story/brexit-is-done-moves.txt (May: hands low, one open palm turning up as her photos; lips on stand-in timing via mouths.track; blinks; head life; all three `look` off-frame left), as milburn.py's face_sp/acted; then the Sonnet chat for the animatic.
- **Needs Sam:** nothing blocks.
- **Read:** `guides/job-packs.md` Build; figure-rig 6 (mouths, eyes lead); milburn.py face_sp/acted (lines 195-260) and story/milburn-moves.txt head; brexit_is_done_action.py MAP (shot 3).
- **Open rule requests:** none.
- **For Claude:** 8 old film files still draw see-through fills with Draw(img,'RGBA') on RGBA frames (grep): move to ink.glaze when one is touched. The evening gown reads as a burgundy tunic and trousers front-on (skirt drawn only turned): cast locked, name it to Sam with the animatic, not fixed here. override.py's "sam" logging of a quoted Override (chat 11's note) still unchecked. castsheet._same_outlines (the judge re-asked only when the outlines change, pixel for pixel) runs for this film only, as judge.py is this film's: move to shared.



# Chat 13 handover (moved by chat 14, 25 Nov)
## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat13`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size (head top, eye row 700, chin, face centre about 64% across), May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7, never worked on in this film (R7 runs in its own chat since 25 Nov: session_01U3pKR21qH3HD4urog8SVBy; its new lower body is switched OFF for this film).
- **Rules that bite next:** 74 (May's gestures land on her words), 5 (nothing through anything: hands on the chair arms, Kemi's hands), 85 (cost watch).
- **Done (chat 13):** kit tests: the start-up run passed (139); after the fixes, the run, chase, gait and moves tests passed. shot 3 watched whole and fixed: runners sank into a lunge (shared run: a foot is down for at most 0.75 leg of travel, moves.RUN_SWEEP; kittest run_hips_stay_up, example notes/learn/run-lunge/); guests met head-on nose to nose and a wolf ran through a guest and past a hand (now waves: everyone in frame runs the same way, two abreast, the near one leading by 0.45 s, both wolves behind; shared checks moves.head_on and moves.within_reach, kittests movers_never_meet_head_on and side_by_side_out_of_reach, examples notes/learn/chase-meetings/). 14 passes became 11 (no animatic had them). Critique pack r5 (source/data/critique/brexit-is-done/r5-p1): see the line below.
- **Next (Opus high):** first, Sam's Y (25 Nov, chat 13, Q1): "the full kit tests run only when a chat changed a shared tool, and always before an animatic and a final render; a chat that changed only its film's files skips the run and the wait": take it through the proposal route (`source/propose.py new kit-tests-when`, pack, judge, record), then build it in handover.py's start-up/end check with a kittest. Then fix critique r5's faults as one list (`critique.py record` printed them; S4, S1 and panel 1-2 A1 were my strip crops, marked false): (a) the lunge wolf shows only as a brown blob with teeth at the right edge for 2 frames (26.75-26.83): make it read as a wolf leaping at his head in the frames before the locked cut; (b) side-on runners: the far arm's round hand shows on the chest while its arm is hidden (P5); (c) near-lane runners tread on the fallen tray and it never moves (rule 5): it skids or tips, or their feet clear it; (d) the tray reads as a disc and the flutes as specks at phone size, and its flat landing and the pools did not read in the strip: look at full size; (e) can't-tells: wolves long and stretched in run frames, Blair's hair a helmet. P7 (Blair's knee balls, no bottom) is R7, locked: name it to Sam with the animatic. Then `critique.py fixed`. Then the moves file story/brexit-is-done-moves.txt and its film side (acting.py FILMS has only blessed and milburn: add `_brexit`, as `_milburn`): May (hands low, one open palm turning up as her photos; small nods on "referendum" and "wolves"), Kemi (staring at the interviewer, a curt nod on "job"), Blair (the big grin held from 25.0); lips on stand-in timing (mouths.track), blinks (F.blinks), head life (headlife) for all three, all three `look` off-frame left; then the Sonnet chat for the animatic (tick the brief checklist first).
- **Needs Sam:** nothing blocks.
- **Read:** `guides/job-packs.md` Build; acting.py MAP (lines 1-90) and FILMS (840-905); milburn.py face_sp/acted (195-260); brexit_is_done.py seated/standing (88-150).
- **Open rule requests:** none.
- **For Claude:** moves.head_on / within_reach (shared, catalogued) run in kittests on this film's chase: a later film with movers calls them on its own table (moves.chase_movers). 8 old film files still draw see-through fills with Draw(img,'RGBA') (move to ink.glaze when touched). The evening gown reads as tunic and trousers front-on and side-on mid-stride: cast locked, name it to Sam with the animatic. override.py's quoted-Override logging still unchecked. castsheet._same_outlines is this film's only: move to shared. The stills command takes times one by one (the old handover's "17.5..26.9" form fails).



### Chat 14 handover (archived chat 15)
- **Newest work: branch `claude/open-wounds-chat14`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size, May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7 (its own chat, switched OFF here).
- **Rules that bite next:** 74 (moves land on their words: check the clip, not just `acting.py check`), 5 (Blair's hands on the chair arms; the kicked tray), 85 (cost watch).
- **Done (chat 14):** kit-tests-when through the proposal route (judge picked a different version from Sam's Y: Q1 to Sam, not built yet). Shot 3 critique r5 fixed as one list: the lunge wolf's head, eye, jaws and paws in frame for 4 of its 5 frames; shared: dark sleeves lifted so a black arm over a black jacket reads (views.sleeve_colour, kittest dark_sleeve_reads), loose floor things kicked along by feet (moves.kicked/trodden, kittest trodden_things_move); tray rim, shine, handles, flute stems. The moves: story/brexit-is-done-moves.txt and the film's side (acting.FILMS 'brexit-is-done'; brexit_is_done.py faces and moves: word_at, TRACK lips, BLINKS, head life on a stand-in loudness, MOODS); acting kit: any sitting-kit pose as a stance, seated gestures keyed from rest (Blessed draws unchanged: kittest moves_from_the_acting_list).
- **Next (Opus high, a new build):** build Sam's acting plan ("Acting plan" below, 25 Nov): every beat of all three lines in the moves file (new hand places, moods per beat, May in motion from the first drawing), `acting.py check`, then a short clip of each line, watched at phone size and at full size (hands on laps/chair arms, nothing through anything), fixed, sent to Sam (clips need no yes). Then the Sonnet chat: tick the brief checklist, the animatic (finish.py on the clean render, Hook Text and sign-off), send it to Sam with the named items: P7 Blair's knees/no bottom (R7, locked), the evening gown reads as tunic and trousers mid-stride (cast locked), Blair's hair a smooth helmet (cast locked), the run's long stretched wolves (the approved shared wolf). Then wait for his notes.
- **Needs Sam:** Q1 (kit tests: the judged version or his own) — does not block the animatic.
- **Read:** `guides/job-packs.md` Build; acting.py MAP (lines 1-90); the Acting plan below; story/brexit-is-done-moves.txt; brexit_is_done.py faces and moves (search 'faces and moves').
- **Open rule requests:** none.
- **For Claude:** stills times are written 01.00 in file names. May's palm: the right hand ('palm up' place, 3.5-6.5 s). The start-up kit run was stopped and rerun on chat 14's final code (notes/logs/kittests-last.log). castsheet._same_outlines still film-only: move to shared.


## Chat 15 handover (archived chat 16)
- **Newest work: branch `claude/brexit-chat15`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size, May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7 (its own chat, switched OFF here).
- **Rules that bite next:** 5 (nothing through anything: the fallen worker's limbs on the ground), 89 (a fresh look before anything goes to Sam), 85 (cost watch).
- **Done (chat 15):** Sam's acting plan built in story/brexit-is-done-moves.txt (every beat of all three lines: May in motion from the first drawing, finger, tap, palm, chops, open hands, satisfied smile; Kemi's press, point back over her shoulder at the wolves, chop, pats; Blair's palms, hand to chest, chop, palm flip, shrugs, palms out), a mood per beat (brexit_is_done.py MOODS); 19 hand places moved to the shared library (acting.PLACES); `final` clip command; acting.py check passes; two fresh-look hunts, their acting faults fixed. Kemi's clip sent. kittest seated_r7_switch: Blair's stale fingerprints re-taken (only chat 14's sleeve lift moved him).
- **Next (Opus medium, a fix from a clear list):** shot 2's background workers, first seen moving this chat: the 7 body-check lines in Exceptions (fallen worker 1's arms and neck 8.67-8.92 s, workers 3 and 4's far arms 8.17 and 9.67 s): fix the drawings in brexit_is_done_action.py, render `final OUT --small --span 7.5 17.5` until the body check is clean. Then open the Sonnet chat: tick the brief checklist, the animatic (finish.py on the clean render, Hook Text and sign-off), send with the named items (R7 knees/no bottom, gown, Blair's helmet hair, the stretched run wolves, the critique's left items below).
- **Needs Sam:** "Override" to send May's and Blair's clips (fixed after the second fresh look; the tools allow no third); Q1 (kit tests) still open — neither blocks the animatic.
- **Read:** `guides/job-packs.md` Notes round; brexit_is_done_action.py MAP; the Exceptions rows for shot 2.
- **Open rule requests:** none. Tool gap for the proposal route: a video fixed after hunt 2 cannot pass the send guard (no third hunt allowed); a "verify the fixed frames" look is needed.
- **For Claude:** critique left (named, not acting): R7 knees/May's chair (locked), May/Blair hair (cast locked), shot 3 floor plates and props, the white wolf reads as a rug, wolf scale doorway vs lunge, the doorway frame 1. Kemi points back over her near shoulder (the scaffold wolves) - the critic thought the pack is on her other side; kept: "backwards" is behind her.
