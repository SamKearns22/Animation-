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


## Sets side, chat 5 (moved by chat 8, 24 Nov)
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's screen place and size (24 Nov).
- **Rules that bite next:** 41 (hands on the steel bars), 89 (each new wolf pose critiqued alone), 5 (physics: feet on boards, struck wolves react).
- **Done (chat 5):** sets plan (this file); 6 references; wolves catalogued; three places built as lines with 18 new shared pieces; places rough sent.
- **Next (chat 8, Opus high, new build):** the wolves as kit parts (spruce-up fixes 1-4, then walk, sit, paw, lunge-recoil, skid, hard hat and vest, blood stains per the approved plan), each critiqued alone; no shot staged. Shots then go in film order once the cast is approved (Sam, 24 Nov).
- **Needs Sam:** nothing (Q2 Y, Q8 film order, Q9 N: 24 Nov).
- **Read:** `guides/job-packs.md` Build; this file (wolves, background action, hardest moves).
- **Open rule requests:** none.
- **For Claude:** wolf.py (side, front, side_pose, head_side); places_site.py; preview of the views: the rough's place_tile at full size.
