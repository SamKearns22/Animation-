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

