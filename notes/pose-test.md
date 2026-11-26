# Pose test (blank test scene; Sam, 26 Nov)

Sam: "Open a fresh chat and open a blank test environment. Run the background people and their movements on the new
model engine and show me a five second render of each of what they look like."

## Brief checklist
- [x] A blank test scene of its own: `source/pose_test.py`, results in `notes/learn/pose-test/` (Open Wounds' code untouched; its poses are only read)
- [x] Item 6, worker torn by two wolves: `pose-test-torn.mp4` (body tool 0-1.1 s; the lying part is the OLD lying body, labelled on the frame)
- [x] Item 7, worker sprints and leaps off the scaffold: `pose-test-runner.mp4`
- [x] Item 8, men with steel bars: `pose-test-bars.mp4` (arms still flat, drawn on top)
- [x] Item 11, staff fleeing: `pose-test-flee.mp4` (a man in a suit; a dress is not on the body tool yet)
- [x] Plain background, moving as in the film, 5 s each, small MP4s (0.1-0.2 MB), sent in the chat
- [x] Checks stray_ink and leg_tone on every 12th frame (Checks line below)

Locked by Sam: Open Wounds' shots, cameras, beats and all its background movements (this test only reads them).

## What the body tool can and cannot draw yet (rule 91, Learn-First)
| person | on the body tool now | what must be learned first |
|---|---|---|
| torn worker (6) | digging, the hit, knees buckling, down onto the hips | lying on the ground: the trunk laid flat, its weight on the floor, a reference photo, a contact check (pose() only leans the trunk about the hips) |
| runner (7) | the whole sprint and the leap, legs solid through the stride | the foot turning at the ankle (heel peel, toe-off, toes down in the air): pose() keeps every foot flat |
| bar men (8) | legs and body solid while they brace and jab | arms as part of the body, hands closed on the bar (mode 'body' keeps the flat sleeves on top) |
| fleeing staff (11) | a man in a suit: front run at us, three-quarter, side-on run | a dress or skirt as its own layer (the body tool put trousers on a woman in a dress: it changes her posted outfit) |

## How the body tool was opened to standing people (for this scene only)
- `views.r7_on` is seated only: pose_test wraps it for specs with `stand_solid`; `lay_over` (seated knees over the jacket) skipped when not seated (standing, it laid the thigh's front over the jacket: a trouser block on the hem).
- `solid_seat._smooth` cropped to the person (same picture, about a quarter of the time): wrapped in pose_test.
- `solid_seat.draw`: new spec flag `legs_soft` (each leg one soft mass, no crease line where a bent knee folds): it removed a loose tick inside the runner's knee. Shared, off unless a spec asks.
- move to shared: the three pose_test wrappers (r7_on for standing, lay_over off when standing, _smooth crop) go into views/solid_seat once Sam picks a standing pose to build; until then they stay test-only (no film draws standing people on the body tool).

## Checks
stray_ink flagged runner, bar men and digger on most sampled frames. Looked at full size: all but one are the leg line
meeting the flat jacket's hem, and the posted collar tick: the check cannot tell a line that meets the hem from a loose
end (a weakness to fix before it guards standing people). One real: a crease tick inside the runner's bent knee, fixed
(`legs_soft`). leg_tone: clean on all four.

## Open rule requests
None.

## Where things stand (pose-test chat 1, 26 Nov, session_01U3pKR3DtLpm97GCSPH6Kke)
Rules that bite next: 91 (Learn-First), 87 (two rounds no gain: stop), 2 (every note becomes a check).
Done: four 5 s clips on the body tool, sent; what each still needs listed above.
Next: Sam's pick of which to learn first (Opus, high: building new); that chat starts with a reference photo and a sheet for it (guides/pose-kits.md, Order of work).
Needs Sam: which movement to learn first (question in the chat).
Read: guides/job-packs.md Plan pack; guides/pose-kits.md; this file.
Open rule requests: none.
For Claude: source/pose_test.py (MAP); solid_seat.draw legs_soft; stray_ink's hem false alarm.

## Override (Sam, 26 Nov: "override all checks and produce it")
Skipped by Override: the body check and fresh critique on runner, bars and flee (torn's body check ran: clean); the
handover end check's 12 items (branches, CLAUDE.md sentences, cost estimate, kit test pose_job_line red) left for the
next chat. Clips sent are the 14:45-15:00 renders (legs_soft on).
