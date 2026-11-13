
# Where things stand (project, 11 Nov; no film in progress)

- **Branch with the newest work:** `claude/job-i-lying-fixes` (also pushed to the main line).
- **Rules that bite next:** 30 (14 and 18 were repeated notes), 48 (one labelled sheet), 41 (lying, a neck shows).
- **Done:** 18 fixed (rule 30: the first fix failed because, seen from behind, the shirt's back and the arm round the
  head were drawn over the neck, and the collar stood alone beside the head). Now the neck is drawn after the shirt,
  rising out of the collar, and both collar bands wrap the neck's foot and turn with it. Sheets remade, numbered:
  `notes/sheets/job-i-lying-18-neck-vance.jpg`, `-driver.jpg`. Kittests: lying, shirt-and-nape, turned heads, and the
  new `lying_neck_from_behind` pass (it fails on the old code: 0 neck pixels showing).
- **Next:** wait for Sam's look at 14 and 18. On his yes, Job I lying is done; his next pick from the job list.
- **Needs Sam:** a look at 14 (picture sent earlier) and 18 (both sheets).
- **Read:** the pack in `guides/job-packs.md` ("A tool job"); `lying_flat.py` MAP, `_neck`, `_collar`, `draw`.
- **Open rule requests:** none.
- **For Claude:** seen from behind (`view in BACKS`, head not behind) `draw` calls `_neck(foot=-10)` after the trunk
  and before the `last` arms, then `_collar` (jacket band -14..6, shirt band 2..18 units along the neck); the trunk
  skips its own collar bands via sp `collar_off` (views.torso_view, back views only). Debug: one shot via
  `L.lie`/`L._fit`/`L.draw` as in `lying_flat.sheet`.



# Where things stand (project, 13 Nov; no film in progress; the aim: films at 15% of a week)
- **Rules that bite next:** 49 (likeness pack: 3+ straight-on, close, not smiling, current), 11 (roughs), 85.
- **Done (13 Nov, chat 2 of 8):** Job P (`notes/ranking-list.md`); Sam: Y to all 10. Written: rule 11 (a rough of every
  new thing), critique lines S7-S9, Protest Tiers' research booked as 'plan extras', Blessed's notes archived
  (posted), its music confirmed Pixabay. Chat limits stay 3%/5% ($5.13/$8.55). Job N waits for the next film's plan.
- **Next: chat 1 of 8 (count restarted), Opus high: the face tool (ranking item 2)**, practised on Kemi Badenoch and
  Andy Burnham (from scratch: not `burnham.py`'s head, card or photos), then a Walliams replay as a test only.
  Photos: one slow news search, 5+ each (3 straight-on, close, not smiling, current; 1-2 three-quarter); one failed
  try per source, then ask Sam. Output: three heads beside the photos on one sheet each, Sam picks; count tries.
  Then the critic bench (item 3, Opus medium) and the people kit on Protest Tiers' cast (item 4, Opus high).
- **Needs Sam:** nothing until the face sheets (and Protest Tiers' Hook Text and sound, no rush).
- **Read:** this section; `notes/ranking-list.md` item 2 and Sam's answers; `guides/job-packs.md` "A tool job";
  rule 49; kit catalogue rows for `likeness.py`, `nametest.py`, `beardkit.py`.
- **Open rule requests:** none.
- **For Claude:** new tool file, not a film file; kittest it. Protest Tiers' forecast line misreads (1% plan share) after
  'plan extras': harmless. chat-gbmazspz's ledger row (579e6f3d) left unmerged (Job O rebuilt from the app).

