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

