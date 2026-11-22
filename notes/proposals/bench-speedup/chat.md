# The chat's own idea (written before the helpers run)

1. Save the start-up fits: the three numbers (seat height, knee depth, ankle height) go in a small file keyed by a
   fingerprint of what they depend on (body, keys, car); recomputed only when that fingerprint changes. 65-73 s gone
   per run, ~0 risk (same numbers).
2. Faster inside test: a distance grid around the body built once per frame (signed distance at 1 cm spacing, from
   the posed skin); points the grid says are more than ~1 cm from the skin are decided by the grid; only points near
   the skin go to the exact winding test. Proof: on 20 old frames, compare inside/outside for every point against the
   exact test: must match exactly, else widen the band.
3. Triangle fill compiled with numba (one loop, same maths, same order so ties break the same way); proof: buffers
   identical on 5 old frames.
4. House head: draw the figure once with the head on its own layer (pass a flag to the house drawing) instead of
   twice and subtracting.
5. 4 frames at a time: run() split across 4 worker processes by frame range; each writes its own log lines; joined.
6. Sam's three: a 'check' pass over all frames with no drawing (prints the fault table), then one render; a cache of
   each frame's solved pose fingerprint so a fix redraws only frames whose goals changed; finished frames saved as a
   compact bundle (the clip MP4 plus a small table of each frame's fingerprint), not PNGs, under the 50 MB limit.
Order: 1, 6 (check pass), 2, 5, 3, 4. Proof for all: same pixels and same faults on chat 39's frames.
