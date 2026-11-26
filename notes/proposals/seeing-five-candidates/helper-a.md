## Leak
Yes: the Facts close with the chat's own pick ("1 first, then 2; 3 only after a test; 4 not recommended; 5 not available") and call candidate 1 "Claude's pick, cheapest". Ignored.

## Results
- Installed here now (checked by import): OpenCV 5.1 with contrib (candidate 2's motion tracing is ready), MediaPipe 1.2.3 (candidate 4's library; its pose model file is not bundled, `.tflite` search empty), onnxruntime 1.29 (can run an exported cut-out model for candidate 3 without torch; torch is not installed).
- Network: the Google model store and Hugging Face both answered (HTTP 200 through the proxy, checked 26 Nov). The makehuman block (problem file) was a git clone; model files for 3 and 4 look fetchable (download itself unchecked).
- Candidate 1 already half exists: the hand check redraws each flat person alone with sleeves and hands in key colours and stacks them in drawing order (source/handcheck.py header). It covers only views.person people, not the steep-camera 3D bodies or older films' figures (same header).
- Candidate 5: no video-watching model in this setup; Claude reads stills only (problem file; nothing in the record contradicts it).
- The critic bench (source/critbench.py, notes/critic-bench.tsv, 20 rows) holds only Blessed and Remakes cases: no movement cases, so no way of seeing has ever been scored on Sam's motion notes. That gap is the main finding.
- Cost so far: Brexit Is Done spent 63.56% against a 52% estimate, 15 notes, 7 repeated (notes/ledger/brexit-is-done.md). How many of those 15 were motion or contact: unchecked.
- Chat 36: 9 picture flags, 3 looked at, mostly meant crowd overlap (problem file; check-knows-intent.md).

## The real decision
Not "which of five tools", but: which way of seeing, across every movement shot of a whole film, catches the motion and contact faults Sam has had to note, without false alarms, at a cost a 15% film can carry. Bigger lever than any outside tool: our engine already knows every hand's exact position each frame; candidates 2, 3 and 4 guess back from pixels what the engine knows exactly. Their real worth is where the engine has no data: finished video (the 3D bodies, old animatics) and Sam's reference photos.

## Root cause
Every look is one instant, and the exact paths the engine computes are never turned into a picture or a number Claude reads. The first route found the same and was not approved because it dropped Sam's five by name, not because it was wrong (better-seeing-tools.md, Sam's words in the problem file).

## Approaches weighed
1. Adopt the chat's ranking (1, then 2) on reasoning alone: untested, the bench gap stays.
2. Reframe: engine data first (path picture, who-is-in-front strip), outside tools only for pictures the engine did not draw.
3. Learn first: one cold test of all five on the same saved notes, then one change at a time for whatever wins. (Chosen; it carries 2 inside it.)
4. Wait for a video model: honest but leaves Sam's notes as the only motion check.

## Proposal
**Learn (changes nothing; Sonnet; about 2.5% of a week, unchecked).** Add movement cases to the critic bench from Brexit Is Done's motion and contact notes (rendered from the commit Sam saw) plus five moves Sam passed. A fresh helper who has not seen the notes scores each candidate cold, by name:
1. Who-is-where colour copy: the hand check's key-colour layers, stacked in order, given for every frame of the move.
2. Motion tracing: OpenCV frame-to-frame movement on the rendered clip, printed as jumps and vanishings; set beside the same numbers taken straight from the engine, to show which is truer.
3. Cut-out model: one small exported model run through onnxruntime, if it downloads; tried on old animatic frames and the 3D bodies.
4. Pose finder: MediaPipe on our frames, and separately on reference photos (where it is trained to work).
5. Video model: recorded "cannot be done here: would need a model that watches video, which this setup does not have". No workaround dressed up as one.
Result: caught, missed and false alarms per candidate; "cannot be tried here" stated plainly for any that will not install.

**Then one change per yes, each with its kit test, each undone alone:**
- Change A: the best motion view becomes shared, added by code to every movement clip and critique pack (advice only, rule 93). Beat: at least 6 of 8 motion cases cold, at most 1 false alarm on the passed moves, no lost Blessed or Remakes catches. About 2.5%.
- Change B (only if 3 or 4 scored): that tool checks pictures the engine has no data for (3D bodies, old animatics) or reads poses from reference photos. Beat: catches a case the engine-data views missed, no false alarm. About 1.5%.
- No change is built for a candidate that scored nothing.
Later films: about 0.2% a film for the added pictures. Reviewed when Sam declares the next film complete: its motion and contact notes against this film's.
Sam would notice: one plain line per candidate on what it did and whether it works here; later, one path picture with each movement clip and fewer notes about hands and who is in front.

## Sam test
Q1: Yes: test on the client's own notes, exact data before pixel guesses, outside tools where they fit.
Q2: Evidence is a whole film's motion notes plus passed moves; more cases from GTA if Brexit has too few (count unchecked).
Q3: Root cause shown; success is a counted catch rate; the change is added by code, not by a chat choosing to.
Q4: Four different approaches weighed; the chosen one compares all five on equal terms.
Q5: The learn step changes nothing; each change has its own yes and comes out alone.
Q6: Installs, network, ledger and bench checked; costs and note counts unchecked.
Q7: Sized by catch rate, not price; the cheap trap (adopting candidate 1 untested) is rejected.
Q8: Permanent shared tools with kit tests; the learn step is a measurement, not a trial.

## Lost / Added
Lost: nothing; stills, sheets and critique stay.
Added: movement cases on the bench, a scored line for each of the five, then at most two shared seeing tools. About 2.5% once, up to 4% more if both changes pass.

## Unchecked
Whether the model files actually download; how many of the 15 notes are motion or contact; all costs.
