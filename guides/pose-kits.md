# Pose kits: how to build a new pose (pose-kit-format, Sam's pick 1, 26 Nov)

Read this for any job that makes a new pose or a pose kit (sitting, standing, moving, a new person in a pose).
Why it exists: R7 (May's natural seated legs) took 11 chats and about 26% of a week. Chats 1-5 and 7 patched
hand-drawn legs and bought nothing kept. What Sam passed ("100% correct", "she is FINALLY correct") was the method
below. Every later note was where two layers meet. Proposal and verdict: `notes/proposals/pose-kit-format.md`.

## The default tool (say it at the start)
**The full measured body, posed by its joints, with the person's posted outfit laid on top unchanged.**
The start check prints the line to say (`handover.py start`, POSE JOB). Sam's words: "give me the options to use other
tools for a pose if a situation requires it. No hard stop on handover. Just tell me you're using the default tool when
you start unless I say otherwise." So another tool is allowed; name it and why in that first line. Nothing refuses.

## The layers, bottom to top
1. **Body**: `source/solid_seat.py` (`build`, `pose`, `draw`): the MakeHuman body from the person's spec, posed by its
   own skin weights as ONE closed body on the kit's joints (`sitting.realize`), through the kit's own camera, house flat
   colours and ink. Mode `seat_solid='body'`. A fault in the body is fixed by moving joints, never an outline.
2. **Posted outfit**: torso, arms, blouse, lapels drawn exactly as posted, on top. Never redrawn (chat 8: "you changed
   her clothes?", "You have drawn a poor version of it"). The body shows only below the outfit's hem.
3. **Lower garments, each its own layer**: trousers as a shell on the body, the seat, shoes, the lap opening. Each
   new look sits behind a flag on the pose (`lap_open`, `leg_gap`), so locked poses and posted films cannot move.

## Order of work
1. **Brief as pictures**: the views Sam will judge (front, both three-quarters, side), each full size with the feet
   in frame. List what is locked (poses, films, outfit) and prove it pixel-identical before and after
   (kittest `seated_r7_switch`; chat 11's 'upright' diff: none).
2. **A reference photo first**, saved in `notes/learn/KIT/refs/`. A site that refuses is asked about at once (Plan
   pack). Chat 10 judged "apart" by the shins alone with no photo, and Sam called it "bearing the crotch".
3. **Pose by joint targets**: where the knee and foot go (`sitting._leg_by_knee`), not foot numbers tuned by eye
   (chat 10's tuning pushed the knees out).
4. **Checks at every layer edge**, run on every tile of the sheet, reading the PNG (a JPEG fooled a colour check,
   chat 11). These exist and are proved on Sam's frames: curves of the flat torso over the body
   (`views.turned_curves_fault`, kittest `turned_curves`); jacket colour under the hem (`jacket_under_hem`); shoe against
   trouser hem (`solid_seat.shoe_faults`, `shoe_shapes`); legs spread and jacket triangle (`solid_seat.apart_faults`,
   `legs_apart_spread`, `jacket_triangle`); all seated ones in `solid_seat.checks()`.
5. **A new note means a new check first**: save Sam's marked frame, write the picture check, prove it red on his frame
   and green on the fix, then show him.
6. **One labelled sheet** at full size beside the posted look and the reference (`sheet_solid.tile(who, yaw, POSE,
   full=True)`). No blind judges before Sam unless he asks.
7. **Two rounds with no real gain on one note: stop** and tell Sam what must be learned (rule 87).
8. **Cost**: every chat's seed names `--film NAME`, so it is billed to the job (`ledger.py rebook NAME` moves any
   strays; the start check runs it).

## Do not repeat (R7's dead ends)
- Hand-drawn leg outlines and guessed tubes patched view by view (chats 1-5): each patch moved another view.
- Seams between solid legs and a flat torso (chat 7): Sam asked "Is there a more intelligent way?"
- The whole person in 3D, clothes included (mode 'whole'): looked worse (judges 2.7 against 3.0; Sam: "The 3D looks
  much worse" on model-body-all).
- Checks that pass numbers while the picture is wrong (chat 10: every seated check 0 on spread legs).

## Not yet proven (open with a "what must be learned" step, not this format)
Standing and moving poses on the body; Kemi, Blair or anyone but May in mode 'body'; clothes other than a jacket over
trousers (vest, skirt, dress). The next step (Learn, chat 13) tries Kemi and Blair seated and lists which checks carry.

## Still to build (pose-kit-format, in order)
Learn (done 26 Nov: `notes/learn/pose-kit/learn.md`, which checks carry to Kemi and Blair) → the tool as one command (body, outfit on top, layers, four views beside the
posted look and reference, every carrying check, locked diff) → checks on every person → the stall stop, live once the
scorers agree with Sam's verdict on May. Done 26 Nov: billing by `--film` and `rebook` (kittests `ledger_told_film`,
`ledger_rebook`); the start line (kittest `pose_job_line`).
