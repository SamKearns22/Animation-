# Get-up re-plan, chat 41 (scratch tools and trial settings; not yet in bench_move.py)
- it.py PATCH.py [full] [lo hi]: frames lo..hi-1 (default 11-25 = 0.46-1.0 s) with a trial patch: joint jumps
  (fast), and with 'full' the real checks one frame at a time (~1.3 s a frame). (A 4-process version hung: numba.)
- tsheet.py OUT.jpg t1,t2,... above,outside PATCH.py: the frames drawn from above and from the door side.
- p1.py, p2.py, ...: trial breakdowns B1 (0.58 s), B1b (0.68), B2 (0.88): LEFT knee folds onto the seat first while
  he still sits (right leg hangs beside the seat by the door), then he rises onto the left knee and the right knee
  comes round the door side to its rear spot. The same breakdowns run backwards for sitting down (7.4-7.8 s).
Run from the repo root: python3 notes/bench/getup41/it.py notes/bench/getup41/p2.py full
Results so far: notes/logs/gta-chat41-live.md.
