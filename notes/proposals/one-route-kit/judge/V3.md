# The chat's own version (written before the helpers ran)

Chat 4's draft (20 Nov, in notes/proposals/one-route-kit/brief-chat4.md): 1 move every borrowed piece into the kits (no
kit loads a film file); 2 finished films' code to a locked archive folder; 3 a guard refuses new work that loads the
archive, naming the current kit piece; 4 the catalogue lists only the current kit; 5 a posted film's code goes to the
archive that day. Isolate, never delete. Other option: warnings on old files.

This chat's version, after measuring (proposal chat 1, 20 Nov):
The real fault is bigger than "old files can be found": the kit's own drawing steps are rewritten at load time by old
films (15 steps while drawing a GTA person), in a chain, so nobody can say what the kit does without running it.
Moving files to an archive folder alone would break the kit, because the kit IS those files (burnham.py, ed.py).

1. Learn first (changes nothing): a census command that prints, for any film or kit file, the old-film files it
   loads and the kit steps they replace. Baseline: GTA cast loads 12 old-film files and has 15 replaced steps. It
   runs in the start and end checks; new work may never raise the numbers.
2. Change one: the short sleeve (the fault Sam saw) becomes a kit option built to rule 41 (one outline, tapering),
   in the people kit itself; GTA stops loading midterminal_cast. Measured: GTA's replaced steps fall, and the
   handcheck seam check passes on the cast sheet.
3. Then one replaced step at a time, most-used first (arm, person, head, torso, legs): each one's current behaviour
   moved into the kit file under a plain name, the film's override deleted from the chain, a before/after sheet of
   the kit people. Stops when GTA's count is 0.
4. Finished films keep re-rendering by being pinned: each posted film gets a git tag (a saved bookmark of the whole
   project as it was) and re-renders from that bookmark in a separate folder, so its code can leave the main line
   without being lost. Their files then leave source/ (so they can't be found or loaded by new work); the pictures
   kittests compares against stay as data.
5. A guard: new code may not load a file outside the kit list, nor overwrite another file's function; the catalogue
   lists kit pieces only.
Cost guess: step 1 about 2% of a week; step 2 about 3%; step 3 about 2% per step (10%); step 4 about 3%.
