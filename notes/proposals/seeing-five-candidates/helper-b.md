## Leak
Yes: "Chat's own pick: 1 first, then 2; 3 only after a test; 4 not recommended; 5 not available", and "Claude's pick, cheapest" on candidate 1. Ignored; each candidate is judged on evidence below.

## Results
- Sam's note on the first route: it "doesn't mention any of the 5 answers" (problem file). The fault reaching Sam here is an answer that dropped what he was told.
- Today's seeing on past notes: the critic bench caught 2-4 of 7 Remakes notes and 2 of 12 Blessed notes (notes/critic-bench.tsv, 14 Nov; column reading mine). Stills miss most of Sam's notes.
- Chat 36: 9 picture-check flags; 3 looked at, mostly intended crowd overlap (check-knows-intent.md). False alarms, not just misses.
- Brexit Is Done: spent 63.56% against a 52% estimate, 15 notes, 7 repeated (notes/ledger/brexit-is-done.md). Repeated notes are the cost.
- What is here now (checked in this container): OpenCV 5.1, MediaPipe 1.2.3, onnxruntime, ffmpeg installed; torch and Segment Anything not. MediaPipe is already used for faces (source/likeness.py; models in source/models/). Model download hosts for MediaPipe pose, Segment Anything weights and huggingface answered (HTTP 206). The 26 Nov failure was a git clone, not these hosts.
- Candidate 1 half-exists: the hand check already redraws each person with sleeves and hands in key colours and stacks them in drawing order (source/handcheck.py header). Only views.person people; not the 3D bodies.
- Gap: no saved note has ever been scored against any motion view. Which candidate catches Sam's notes is unknown for all five.

## The real decision
Not "which of five tools", but which way of looking, across a whole film, catches the movement and contact notes Sam has already given, with fewest false alarms. The bigger lever: we draw every frame, so the program already knows where every hand and body is; pixel-guessing tools (2, 3, 4) only add value where they see what the engine's data cannot, i.e. what actually reached the screen.

## Root cause
Every look is one instant, and the checks read plan depths, not what was drawn (preflight picture_faults uses plan depth; the drawn-layer copy lives only inside the hand check, for hands). No check has been tuned on Sam's past motion notes, so neither misses nor false alarms are counted. The first route failed for Sam because it collapsed the five into one internal winner and never showed each tested or ruled out.

## Approaches weighed
1. Build candidate 1 fully now (cheap, no downloads): sees overlap truth, but not motion; untested against notes.
2. Reframe: the engine's own per-frame record (positions, drawing order) as the source, turned into pictures Claude reads (layer copy, path picture); outside tools only as an independent check on the finished video.
3. Learn first: one test set from Sam's past notes, every one of the five run on it (or plainly marked "cannot here", with what is needed), scored cold.
4. Outside video model (5): needs another company's service, a key and Sam's yes; not buildable now.
Chosen: 3, which feeds 2. It is the only one that answers Sam's question about all five with results, not opinions.

## Proposal
**Learn (changes nothing; Sonnet; about 2.5% of a week, unchecked).** Test set: the bench's existing cases plus Brexit Is Done and GTA movement and contact notes, rebuilt from the commit Sam saw, plus five moves he passed. Each candidate, by name:
1. Who-is-where colour copy: extend the hand check's key-colour redraw to every person and prop; run.
2. Motion tracing (OpenCV, installed): frame-to-frame movement on the rendered clip; flags jumps and vanishing parts. Known weakness: flat colour fills give little to track; measured, not assumed.
3. Segment Anything: weights reachable, torch missing; install it in the container and run once. If install fails: "cannot here; needs torch installed at session start".
4. MediaPipe pose (installed, model reachable): run on our frames. Counts found bodies; a body it cannot find is logged as a possible "a stranger wouldn't read this" sign, not as a fault.
5. Video-watching model: cannot be done here. Needs another company's service, an API key through the environment's settings, and Sam's yes to send frames out. Stated, not attempted.
Plus today's stills (baseline) and the path picture from the first route. A fresh helper scores each: caught, missed, false alarms. Result goes to Sam as one table, one line per candidate.

**Then one change per yes, each with its own number:**
- Change A (best view for contact): shared, added by code to every critique pack and clip; kit test. Beat: catches more of the contact notes than stills, at most 1 false alarm on passed moves.
- Change B (best view for motion): same terms on the motion notes.
- Any outside tool only if it beats the engine views on some notes the others missed; else written down as tested and not used, with its score.
All advice only (rule 93). Reviewed when Sam declares the next film complete: its movement and contact notes against Brexit Is Done's. Each change about 1.5-2.5%; later films about 0.2% each (unchecked). Against 15% a film: a one-off system cost, not a film cost.

Sam would notice: one table naming all five with what each caught; then clips with a coloured copy or path picture, and fewer repeated movement notes.

## Sam test
Q1: Yes: an expert uses the ground truth the program already has, and tests outside tools on the client's own notes rather than ranking them by opinion.
Q2: Evidence is two films' saved notes plus the bench; the whole film's flags, not one chat.
Q3: Root cause named with sources; success is a counted catch rate; the winning view is added by code, not by a chat choosing to.
Q4: Four different approaches weighed, including reframe and learn-first.
Q5: The learn step changes nothing; each change has its own yes and comes out alone.
Q6: Installs, hosts, bench scores and ledger checked here; costs and bench column meaning unchecked.
Q7: Sized by catch rate; the cheap trap (build candidate 1 untested, drop the rest) rejected.
Q8: Permanent shared tools with kit tests; the learn step is a measurement; reviewed at film completion.

## Lost / Added
Lost: nothing; stills, sheets and current checks stay.
Added: a test set from Sam's notes, a scored result for each of the five, then up to two shared views, each on its own yes; about 2.5% once to learn, about 2% per change.

## Unchecked
Costs; which Brexit and GTA note numbers are motion or contact (taken from better-seeing-tools.md's verdict); whether torch installs within the session's limits; how optical flow and MediaPipe behave on our flat drawings; meaning of the bench table's columns.
