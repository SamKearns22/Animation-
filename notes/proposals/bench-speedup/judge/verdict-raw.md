## Leak
yes: the Facts list a full set of remedies (Sam's Y list from 22 Nov: distance grid with the exact test kept near the skin, compiled fill, head once, 4 at a time, saved fits, checks first, splice, frames kept). They are Sam's own words, so they must be weighed, but they anchor: V2 takes them whole. V1 and V3 weigh them and reject the grid on the facts.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 2 | 3 | 2 | 2 | 3 | 12 |
| V3 | 5 | 5 | 4 | 4 | 4 | 22 |
## Sam test
Q1: Yes. An expert measures first, stays exact, and caches by what made each result. The faster inside test is the standard exact method (capped mesh, ray count through a triangle tree). The judge checked V3's measurements here: 10,176 tested points, 48 open edges (the two wrists), 0 bad edges, 0.6-0.7 ms a point, 4 threads already in use.
Q2: The scope is right: every remaining shot-4 round (the get-up re-plan's many check runs, the full grey run, the dressed clip), not one frame. The evidence is chats 35-39's timings and the code. One gap: the ledger cannot split waiting from thinking.
Q3: The root cause is found. Every inside test sums all 20,304 triangles, and the fits re-run the solve (and so the press) on every start. The changes live inside the run and clip commands: the clip refuses to draw without a check pass on the same inputs, and stored frames are spot-re-made before sending. Nothing relies on a chat choosing to follow a note. Each step has an equality bar.
Q4: Five approaches were weighed (grid, exact faster sum, fewer frames made, no press, learn first). The grid fails on measured facts: every tested point is 1.5 or 3 mm off the skin, the skin moves each round, and the wrists are open.
Q5: Each step is its own numbered yes, all asked in one message. A step that misses its bar is reverted and reported. The old exact test stays in the code as the referee.
Q6: Sources are named. Timings after each change, the build cost and the bundle size are marked unchecked.
Q7: Exact, not approximate. No "close enough" shortcut (libigl's fast winding number is approximate and is ruled out).
Q8: Permanent tools, reviewed at film end. Nothing is a trial.
## Pick
V3
## Why
V3 rests on facts it measured (and the judge re-measured). It rejects the grid for three checked reasons. Its biggest lever is the check-only loop the get-up re-plan repeats (73 s start plus ~13 s a frame), which is where the gates were skipped (chat 37 skipped span.py, so a fault reached chat 39). Its checks-first gate makes skipping impossible.
V1 is close and sound, but it leans on libigl (unchecked, and partly approximate) and infers the processor use.
V2 builds the grid that cannot help here (all queries sit within 3 mm of the skin). It adds 4 processes without knowing that numba already uses all 4, and it bundles six changes into one order.
Taken from V1:
- saved fits first (cheapest, safest, at once speeds every span run);
- 10 random stored frames re-made before any send;
- 4 at a time only if the processors sit idle more than 30%, else dropped with a Lost line;
- "speed buys chances to check, not tokens".
Taken from V2:
- the fill keeps the same triangle order, so ties break the same way;
- a fingerprint table goes with the stored frames.
## Faults in the pick
- F1 [fixed] V3 put the inside test before the saved fits. The fits now come first: no risk, and 65-73 s off every run at once.
- F2 [fixed] V3 had no guard against a stale stored frame. V1's 10-random re-make is added; a mismatch wipes the store.
- F3 [fixed] The jumps check compares neighbouring frames, so reusing checks could hide a fault. The check pass now always covers all 197 frames; only drawing is reused.
- F4 [fixed] A ray that grazes an edge is ambiguous. That point is now handed to the old exact sum.
- F5 [fixed] An MP4 is lossy, so a splice from it would not be pixel-identical. Frames are now stored losslessly.
- F6 [named] Cost ~4.2% of a week is unchecked. The film is already at ~83% against 53.2%; this will not bring it back. It pays back in rounds and chats on this shot and on later solid-body films.
- F7 [named] Speed does not fix the broken get-up (frames 13-23, 179-186) or the look. "No notes" still needs the re-plan; speed makes it affordable to check fully.
- F8 [named] Sam's distance grid is dropped (Lost line, with the reason).
- F9 [named] Each replaced bundle grows the repository's history. The size is unchecked; there is one bundle, replaced, under 20 MB.
## Final version
**Learn first (changes nothing, ~0.4%).** Record the old test's inside/outside answers for the proof cases and every 8th frame, the fit numbers, proof.txt, 12 grey PNGs, per-part timings, and how busy the processors are during a frame. This is the sameness bar.

**Then one change at a time.** Each is its own numbered yes, all asked in one message. Each has a test that fails the build if its bar is missed; a miss is reverted and reported.
1. **Saved fits.** Seat, knee and ankle numbers are filed under a fingerprint of the body, keys, car and solve code, and redone automatically when any of them changes. Bar: identical numbers; start-up ≤5 s (was 73).
2. **Faster exact inside test.**
   - Cap the two wrist holes with 48 lid triangles.
   - Count signed ray crossings through a triangle tree (numba), then subtract the lids' exact share.
   - A ray that grazes an edge sends that point to the old sum. The old sum stays as the referee.
   - Bar: 0 answers differ on the recorded set; proof.txt byte-identical; press ≤1.5 s (was 10.1).
3. **Checks-first gate.** The clip command refuses to draw until a check-only pass over all 197 frames, on the same fingerprint, has every fault fixed or named.
4. **Frame store and splice.**
   - Each frame's drawing is filed under its exact inputs (its goals, the fits, the solve and drawing code).
   - A fix redraws only the frames whose inputs changed. Checks always run on all frames.
   - Before any send, 10 random stored frames are re-made and must match pixel for pixel; otherwise the store is wiped.
   - One lossless bundle plus a fingerprint table goes on GitHub, under 20 MB.
   - Bar: a one-span fix redraws ≤30 frames.
5. **Drawing.** Compiled fill (same triangle order), then head drawn once. Each must be pixel-identical on the 12 frames. Bar: drawing ≤5 s (was 16).
6. **4 at a time** only if the learning step (re-measured after 2) shows the processors idle more than 30% of a frame. Otherwise it is dropped, with a Lost line.

Cost: ~4.2% of a week once (unchecked), reusable on every solid-body film. Then the get-up re-plan, run with the real checks as often as it needs.
## For Sam
### Option 1: Exact speed-up, step by step
Make every test run much faster without changing a single drawn pixel or check result. First save the three body measurements the program currently redoes on every start. Then replace the slow "is this point inside the body?" sum with an exact faster one. Then the film tool refuses to draw before a full check pass, and redraws only the frames a fix changes. Each step is a separate yes. Each is kept only if old frames come out identical. You would notice clips arriving sooner after each note, and the get-up checked fully every time. About 4% of a week (an estimate).
Lost: the "distance grid" idea from your list. It cannot help here, because every point tested sits within 3 mm of the skin, where the slow exact test is needed anyway. Possibly also "4 frames at a time", if the computer is already fully busy.
Added: saved body measurements, a faster exact inside test, a no-drawing-before-checks lock, kept frames on GitHub with a spot re-check, and faster drawing.
### Option 2: Your list as given
Build the six speed-ups you named, in one go: the distance grid, compiled drawing, head once, 4 frames at a time, saved measurements, checks first, kept frames. Each one is proved on old frames. It is quicker to approve, but the grid would gain almost nothing. "4 at a time" may fight the processors the inside test already uses. One yes covers six changes.
Lost: step-by-step yeses. If something goes wrong it is harder to tell which change caused it.
Added: the same speed-ups, plus a distance grid that would mostly go unused.
