# The chat's own idea (written before the helpers ran)

Root cause: the skeleton is already right (sitting.realize solves hip, knee, ankle in 3D); the failure is drawing the
volume of a thigh and shin as hand-written 2D outlines. A 2D outline has no depth, so foreshortening (front view) and
one leg over another (crossed) have to be faked per view, and each fake breaks another view. Four chats of patches
(27% of a week) prove the method, not the patch, is wrong (rule 30).

Idea: draw a seated person's lower body (waist to feet) as the measured 3D body, the way GTA's dressed Jason was drawn
(Sam: "It looks very good"), and keep the flat house upper body over it.

1. Generalise the bench body into a kit piece (source/body3d.py, reusing bench_pose.posed, bench_draw raster/ink,
   dressed_draw's colours): any kit person's build from their spec (height, woman/man, build -> MakeHuman's six
   numbers), clothing parts from their spec (trousers or skirt with its hem length, shoes, socks or bare skin), posed on
   sitting.realize's hip/knee/ankle joints (pixels -> metres), drawn through the kit camera in house colours and house
   ink: outlines on the silhouette, at part borders and where depth jumps (the top leg over the under leg, the knees
   over the thighs from the front).
2. Lower body only, so a person looks the same standing and sitting from the waist up: the 3D pelvis and legs are
   drawn first, the flat torso over them; the top's hem hides the join (no fades, which is where arm3d's "sausage"
   came from). Seated poses and sit/stand moves only; standing legs stay as they are (no note on them).
3. The chair is a solid in the same depth pass, so the seat hides and is hidden by depth, and crossings are counted.
4. The check first (no rule without a working check): a drawn-vs-solid leg test, the flat leg outline against the 3D
   body's outline from the same skeleton, must flag Sam's sheet v4 (front blob, vanishing 3/4 thigh, crossed shin) on
   the saved pictures; plus body-chair and leg-leg crossings = 0 and each clothing part one piece (no islands).
5. One test sheet (the same 4 views x May, Kemi, Blair) beside sheet v4 and beside the approved standing people at
   phone size; a fresh critic and judge_r7.py must score 4+ before Sam sees it.
6. Fixed cap: 6% of a week (two Opus high chats). If the sheet is not believable by then, stop and tell Sam what is
   missing. No outline patching.
7. Finished films replay unchanged: the old leg drawing stays behind a switch (Open Wounds' locked frames).

Lost: chats 1-4's hand-drawn leg shapes; possibly the exact bum shape (the 3D pelvis replaces it; judged against the
accepted one). Added: 3D seated legs for every film; a drawn-vs-solid leg check (also rule 41's G4-11 "2D legs", written
"cannot yet").
Risks: trousers and skirts never tried on the bench (part labels by bone and height); the flat torso over a 3D pelvis
may not meet cleanly in the side view; women's builds untried.
