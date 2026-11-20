# Helper B: big body moves and a "this is a human body" check

## Leak
The facts give an answer: lesson 10 (key poses drawn per angle, layered by hand) and a two-part build (method plus check). Weighed below as one option, not assumed.

## Results
- Shot 4: four versions; version 3 rejected; version 4 drew 16 notes, 8 from one cause, Jason as a flat figure bent toward 3D points (notes 2, 3, 4, 6, 7, 8, 11, 15) (case study s.7, cause A).
- Version 4 passed the point checks. The fresh-eye critique (rule 89) was not run on it, the same failure as version 3 (case study s.7 E). The tool that makes the finished clip has no critique step in it (searched `source/finish.py`), so rule 89 only happens if a chat chooses to run it.
- Body-placement faults keep coming back: 11 earlier notes across past films (critique checklist P7, lines 29 and 81).
- Film cost: estimated 53.2% of a week, spent 27.71% over 17 chats, heading for 78.2% (ledger). **Gap:** the ledger counts cost per chat, not per shot, so shot 4's own cost cannot be read.
- The kit already has the means. `lying.py` holds a 3D skeleton. `lying_flat.py` draws it with the house's own flat torso (front to back views), sleeves, legs and head laid along it, nearer pieces over farther ones. `lying.solids` passes the body's limbs to the every-frame collision test (rule 5). The cars are 3D (catalogue row 77). The catalogue lists this skeleton only for lying down and high cameras (row 70), and it has never been used for an upright move.

## The real decision
The decision is not "how to fix shot 4" or "add one more check". It is two things for every film. First, how a person is built whenever their body leaves the tested standing or seated poses. Second, how judging by eye becomes impossible to skip. How the body is built is the bigger lever: a real skeleton gives joins, lengths, sides and depth by construction, so most of the faults never arise.

## Root cause
- The shot had no 3D body. A flat standing drawing was bent by a flat arm-solver toward 3D points. Depth was faked by masks cut at three points. Turning past side-on swapped the drawing while the arm targets and drawing order stayed set for the front.
- The check tested about 15 points because points were all the shot had.
- The 160-degree turn failed because it was judged on one frame (lesson 12).
- Both bad versions went out because the critique exists only as words in the rulebook, with nothing in the tools enforcing it.

## Approaches weighed
1. **Hand-drawn key poses per angle, layered by hand** (lesson 10). New drawing work for every new move in every film. Hand layering repeats the mask fault, and a check is still needed on top.
2. **Reframe: one 3D skeleton for every big move,** drawn with the flat house pieces (`lying_flat`), extended from lying to any pose. Depth against 3D cars comes piece by piece. "Human" becomes measurable on the skeleton: fixed bone lengths, joint limits, left and right sides, no limb through another, the collision test every frame.
3. **Check-only:** a cold critique of every person every 0.25 s, enforced at sending. It catches faults but builds nothing right, so more rounds.
4. **Learn first:** run the existing means on version 4's moments and measure what each would have caught, before changing anything.

Chosen: 4, then 2, then the gate from 3, each as its own yes.

## Proposal
**Learn (changes nothing; Opus, high; about 1% of a week, unchecked).**
- (a) A fresh helper critiques version 4's frames cold; count how many of the 8 cause-A notes it names.
- (b) Pose the 3D skeleton through shot 4's existing 3D keys and draw it with `lying_flat` through shot 4's camera at 6 moments. Put it on one sheet beside version 4, full and phone size. Run its limbs through the collision test against the car; count faults.
- (c) List what the flat pieces lack upright: sitting on the sill, the gun hand, seen from behind.

**Change 1, the body route (only if (b) reads as human on the sheet).**
- The catalogue's row for big moves (climbs, turns past side-on, leaning out, car doors, falls) points to the 3D skeleton. Pre-flight refuses a big move built on the flat standing figure.
- Number to beat: on shot 4's next animatic, 0 notes of the cause-A kinds; 0 collision faults in every frame; the next film's big move gets 0 repeated body notes.
- About 3% of a week once (unchecked), then reused.

**Change 2, the human-body check (Opus, medium).**
- It runs on the skeleton: limb lengths within 3%, elbows and knees inside human ranges, each arm on its own side of the chest, no limb through another or the body. It also checks the drawing: each drawn piece touches its parent piece; gun barrel aimed within 10 degrees of its target.
- It runs inside pre-flight and the finishing tool. A fault blocks the render unless named.
- Number to beat: flags all of notes 3, 6, 7, 8 on version 4's poses; 0 false flags on the pose gallery.
- About 1.5% of a week.

**Change 3, the critique gate (only if (a) caught 6 of 8 or more).**
- The finishing tool refuses a clip or animatic that has no critique record for that render.
- Number to beat: 0 clips sent without a critique.
- About 0.3% of a week.

Total about 6% of a week once (unchecked), against 15% a film. This film is over budget already. The return is fewer rebuilds: shot 4 took four versions.

**What Sam would notice:** one sheet, Jason's climb drawn by the 3D skeleton beside version 4. Then shot 4's build proposal (rule 8) using it. Then each change as its own Y.

## Sam test
- Q1: An expert fixes how the body is built, not the paint over it, and enforces the review rather than rewriting it.
- Q2: Evidence is drawn from shot 4 plus 11 past body notes across films; the learn step tests on real frames.
- Q3: Root cause found. Enforced by pre-flight and the finishing tool, not by a chat reading a rule. Each change has a number to beat.
- Q4: Four different approaches weighed; this one removes the cause and the others only catch it.
- Q5: The learn step changes nothing. Each change can be undone alone. Nothing is trusted unseen: the sheet comes first.
- Q6: Sources named; estimates and the look marked unchecked.
- Q7: Sized to the result (skeleton, check and gate, as the evidence earns them), not cheap masks.
- Q8: Each change is permanent when made, reviewed at the film's end.

## Lost / Added
- Lost: hand-layered masks for big moves; sending a clip without a critique.
- Added: one learn sheet; the skeleton route for big moves; a human-body check; the critique gate.

## Unchecked
- Whether Sam accepted `lying_flat`'s look (Job I).
- Whether the 3D cars give depth per pixel or per piece.
- All cost estimates.
- Shot 4's own cost (the ledger has no per-shot split).
