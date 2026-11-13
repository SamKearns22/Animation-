
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


