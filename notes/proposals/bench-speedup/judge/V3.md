# Helper A: bench speed-up

## Leak
The Facts list the remedies (distance grid, compiled fill, head once, 4 at a time, saved fits, Sam's three). I weighed them as options only.

## Results
- Grey frame ~15 s, fold press 10.1 s of it. Start-up ~73 s. Dressed still 105 s, fits 65 s of it (learn-step.md "chat 39").
- Measured here:
  - The inside test costs **0.71 ms per point**, and numba already uses **4 threads**.
  - The tested skin is 20,304 triangles and 10,176 points.
  - It is closed except **two 24-point holes** (the wrists), with 0 bad edges.
- Every tested point is a skin point stepped **1.5 or 3 mm** out (`_inside2`).
- The fits call solve(), which runs the press, so the start-up is mostly inside tests too (fit_ankles).
- Runs: full grey run 51 min (chat 35). Middle clip 2,908 s for 131 frames (chat 38).
- Cost: shot 4 ~39% of a week. The film is at 82.55% against an estimate of 53.2%. Bench chats cost 1.5-3.6% each (ledger).
- Broken: frames 13-23 and 179-186 (chat 39). They need a re-plan, tested with span.py many times.
- Gap: no record splits a chat's cost into waiting and thinking.

## The real decision
How to make every remaining shot-4 round (get-up re-plan, look, dressed clip) take the fewest chats, with pictures and checks unchanged. The biggest lever is the check-only loop the re-plan repeats (73 s plus ~13 s a frame), not the drawing.

## Root cause
Every point sums all 20,304 triangles, about 14,000 point-tests a frame (inferred). The fits redo this on every start-up, and were never cached because no one knew they were slow until chat 39. The distance grid fails here:
- the skin moves every round, so the grid would be rebuilt on every call;
- it has no inside or outside at the wrist holes;
- every point is within 3 mm of the skin, where the exact test must stay anyway.

## Approaches weighed
1. **Distance grid:** rejected, measured above.
2. **Exact, faster sum:** cap the two wrist holes with 48 lid triangles, count ray crossings through a triangle tree, then subtract the lids' exact share. The same number by arithmetic.
3. **Reframe, fewer frames made:** a record of each frame keyed by its exact inputs. A fix re-makes only the changed frames, and the record is kept between chats.
4. **Reframe, no press:** better skin bending at the folds. It changes pixels, so it belongs to the look stage.
5. **Learn-first:** record the old test's answers and use them as the bar.

Chosen: 5, then 2, then 3, then drawing. Each is its own yes.

## Proposal
Learn first (changes nothing): record every inside/outside answer for the proof cases and every 8th frame, plus the fit numbers, proof.txt, 12 grey PNGs and the per-part timings.

Then one change at a time. Each has a test file that fails the build if its bar is missed:
1. Faster exact inside test. Bar: 0 answers differ, proof.txt byte-identical, press ≤1.5 s (was 10.1).
2. Fits saved under a fingerprint of the body, keys, car and code; any change re-fits automatically. Bar: identical numbers, start-up ≤5 s (was 73).
3. Frame record, splice, and a bundle on GitHub under 20 MB. Bar: a one-in-between fix redraws ≤30 frames, and reused frames are pixel-identical.
4. Checks-first gate: the clip command refuses to draw until a check-only pass on the same fingerprint has every fault fixed or named.
5. Compiled fill, then head once, then 4 at a time, each pixel-identical on the 12 frames. Bar: drawing ≤5 s (was 16). 4-at-a-time is judged after 1-2, because numba already uses all 4 threads.

Cost (unchecked estimate): about 4.2% of a week once, reusable on every solid-body film. Sam would notice faster clips and fewer chats per round, with the same pictures.

## Sam test
- Q1: an expert would measure, stay exact and cache by inputs.
- Q2: scoped to the whole remaining shot-4 loop.
- Q3: equality bars and gates that refuse, so no chat has to choose to follow it.
- Q4: five approaches weighed; the grid was rejected by measurement.
- Q5: each step undoes alone, and none ships before its test passes.
- Q6: sources named, estimates marked.
- Q7: no close-but-not-exact shortcut.
- Q8: permanent tools, reviewed at film end.

## Lost / Added
Lost: nothing drawn or checked. The distance-grid idea is dropped.
Added: the answers test, the fit cache, the frame bundle (under 20 MB), the clip gate.

## Unchecked
Timings after each change, the bundle size, the build costs, and the ~14,000 tests a frame.
