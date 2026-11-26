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

## The Learn-First rule (rule 91, Sam, 26 Nov)
**Changed by Sam (26 Nov): before a new pose, remind Sam of these suggestions in one line, each with its time; he picks
which to do, if any. Nothing waits on them unless he picks.** (Was: learn first, then build.) Sam: standing, running
and sitting work on the body tool (the pose test's practice clips; May). Proven means on a sheet Sam passed with its checks green. The start check prints the rule and the
list for every pose family a job's notes name that is not proven (`handover.py start`, LEARN-FIRST; kittest `learn_first`).
**Movements and camera views too (Sam's pick 1, 26 Nov):** the list also names movements against objects and hard
camera views (GTA's lean-out, never on the list, cost about 59% of a week learned inside the film; notes/steps-breakdown.md).
Each line offers a **grey practice clip** (a plain grey figure, no film checks, sent as made) with its time; Sam still picks.
The families, as the check reads them (`family | proven? | words that name it | what must be learned | practice clip time`):

```
sitting upright | yes | upright on, seated, sitting, sits, legs crossed, legs apart | - | -
sitting other seats | no | armchair, sofa, bench, stool, lean back, reclin | the seat's height and depth, the lean, a reference photo, a sheet | one chat, about 2% of a week
leaning while seated | no | lean in, lean fwd, lean forward, leans | the hips' angle as she leans, a motion clip checked frame by frame | one chat, about 2% of a week
standing | no | standing, stands, stand up | the legs straight under the outfit, feet on the floor, a reference photo, a sheet | one chat, about 2% of a week
walking and running | no | walk, running, runs from, run from, run rampant, chasing, chase, flee, leap, jump | the legs through a stride, feet on the ground each step, a motion clip | one chat, about 2% of a week
arms beyond the lap | no | arm across, reach, raise, lift, steel bar, swing, grab, fight | arms as part of the body (now flat, drawn on top), hands on objects | two chats, about 4% of a week
lying, kneeling, crouching | no | lying, lies, kneel, crouch, fallen, on the ground, torn | the body on the floor, its weight, a reference photo, a sheet | one or two chats, 2-4% of a week
other clothes | no | skirt, dress, coat, shorts | each garment as its own layer on the body, a sheet | one chat a garment, about 2% of a week
seen from behind | no | from behind, back view, back to us, his back to, her back to | the back of the outfit, a sheet | one chat, about 2% of a week
leaning or climbing out of a vehicle | no | lean out, leans out, leaning out, climbs out, climb out, out of the window, through the window, window ledge, hangs out, gets out of the car | the body through the window frame, hands on the sill, the car moving under him, a grey practice clip checked at full size | two or three chats, 4-6% of a week
riding in a vehicle | no | steering wheel, passenger seat, driver's seat, back seat, drives, driving, in the car | seated in the car seen through glass, hands on the wheel, everyone leaning with the swerve | one chat, about 2% of a week
very close, or a limb at the lens | no | close-up, close up, extreme close, points at the camera, points at us, at the lens, towards the lens | the face or hand that fills the frame, its depth, a reference photo | one chat, about 2% of a week
```

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
