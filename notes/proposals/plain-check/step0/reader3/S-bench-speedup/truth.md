The plan the options describe (the judge's final version):

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