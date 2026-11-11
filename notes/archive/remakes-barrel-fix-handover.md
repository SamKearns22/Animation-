# Remakes: Link runs through the barrels in the camp (handover to paste into a new chat)

**Model: Opus, medium effort.** Animation- project selected; first merge origin/claude/create-claude-md-oe8z4g.

**The fault (Sam, 11 Nov, a frame from animatic 3, S7 about 19-21 s):** Link scuttles in through the gate, then
walks straight through the two barrels (the green and the red one, left of the lane) instead of round them. Here he stands
level with the red barrel and it shows through and behind his body.

**Why (found by reading the code, not yet confirmed on frames):** `_link_camp(t)` in source/remakes.py (about line 814) moves him
in a straight line (with an ease) from (x -0.8, depth WALL_D + 0.4) to his mark RS.CAMP_MARKS['link'] = (-1.25, 5.0). The barrels
are `RS.BARRELS` in source/remakes_sets.py (about line 881): (x -1.4, depth 7.3) and (x -1.3, depth 6.4). That line passes straight
through them. They are on the camp's solid list SET_BOXES ('barrels'), which checks set against set, never a moving figure against the set.

**Fix, in this order:**
1. Confirm: stills (`python3 source/remakes.py stills OUT_DIR T...`) across the scuttle (SCUTTLE[0] to SCUTTLE[1]) to see where he overlaps.
2. Route him round: add a waypoint to `_link_camp` so he runs down the clear lane to the right of the barrels (about x -0.3 to 0.2, past
   depth 6.4) and then curves left to his mark, keeping the quick-in ease and the crouched front-on run (note 37b). The barrels stay
   (Sam has seen them), unless the mark itself must move a little; the mark must stay left of KG's crest and clear of the barrels.
3. Draw order: at every frame he must be in front of the barrels when nearer the lens (depth below theirs) and behind when further.
   The camp painting draws the barrels in the set, so check that he is drawn over them, not under, once he is past.
4. Rule 56 (a fault of its kind): do the same check for every figure that moves through the camp: KG's entrance, the two gunmen,
   the grenade victim and the debris paths against SET_BOXES. List any other overlap.
5. Add a check so it cannot recur: a moving-figure-against-SET_BOXES test in `remakes.py check` (sample each figure's feet every frame
   from the gate to his mark; fail if the feet are inside a box). Propose it to Sam as a rule request if it belongs in the shared checks.
6. `python3 source/remakes.py check`, a clip of just the entrance (`final OUT --small --span T0 T1`), send it (no yes needed for a clip).

**Keep:** the film's timing (Sam is happy with the pace and may make 1.1x standard; do not shift anything), Link's arrival time,
his gate entrance and his pose. **Report** in one line: "fixed: Link now runs round the barrels. Clip sent." plus any "Lost:" line.
Update the Where things stand handover (15 lines at most), story/status.md, commit and push to the main line and the chat's branch.
