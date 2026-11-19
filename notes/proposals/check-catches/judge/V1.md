# Chat's own idea (written before the helpers)
1. Fix the silent counter first: the per-check record should not depend on a local file that a new chat never
   has; save per check, per film, every run (name, film, date, faults, a one-line sample) into the film's ledger
   whether a round is open or not. Fold quick_checks into it with check names.
2. Add "caught": each fault a check finds and the chat then fixes is a catch; at each animatic, Sam's notes are
   matched to checks (a note a check should have caught = a miss; tag by hand at note time, one word).
3. "Would Sam have seen it": mark a catch as "on screen" when it is in a frame the animatic shows, else "hidden".
4. After three films, a retirement list: checks with 0 on-screen catches in three films and their cost, each with a
   Lost line for Sam. Give job 1 the list rather than building its own.
Lost: nothing. Added: a per-check record in each film's ledger; retirement decided after three films.
