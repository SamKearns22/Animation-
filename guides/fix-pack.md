# Fix pack: the one page a fixing chat reads (cost-spike fix 4, Sam's Y, 27 Nov)

For a round of Sam's notes (Opus, medium): read this page and the notes printout `handover.py start --film FILM`
gives, nothing else of the guides unless a note names a rule (then only that rule's row:
`grep -n '^| 41 ' guides/film-quality-rules.md`). Aim: **10-18 steps a note** (was ~35; every step re-reads the
whole chat, so steps are the cost).

## Locked by Sam
The film's notes carry a "Locked by Sam" line: the script, shot order and lengths, every camera and framing, and
what happens in each shot. Fix the drawing, never the shot. If a view seems not to work, say what the project would
need to learn to draw it, before asking Sam.

## Rules that bite (by number; the row only if you need the detail)
- **30** a note seen before means the first fix failed and a check is missing: find why first, tell Sam, add the check.
- **87** restate each note in one line with how it will be fixed; a fix that fails twice stops: 2-3 options as stills.
- **89** critique before every send; **88** one check sheet per round, re-checks in words or cropped changed frames.
- **61** answer a note by reading the lines it touches, never a whole file (every big file opens with a MAP).
- **48** never look at an unchanged picture again; **19** every check ends PASS, FAULT or COULD NOT TEST.
- Every fix is for all films: a fix that can only live in one film's code gets a "move to shared" line.

## Each note, in this order (about 6-12 steps)
1. **Mark it** (1 step, counted from here): `python3 source/notesteps.py note "8: the whale knocks the helideck"`.
   At 12 steps you are asked to say in one line what is stuck; at 20, stop the note: finish only an edit already
   made (its clip, the commit), write what is stuck in the film's notes and report it with the round.
2. **Find the code** (1 step): `python3 source/page.py FILM show "note words" --shot SHOT --at SECONDS --who WHO`
   (~40 numbered lines of the functions it touches). No grep or sed on film files first.
3. **Before changing a function, ask who else uses it** (1 step each, ~10 lines):
   `python3 source/touch.py NAME` (or `MODULE.NAME`): where it is, what calls it (film code and shared code apart),
   the checks it feeds and the kit tests that reach it, with the one command to rerun them. `touch.py "find WORD"`
   lists the functions whose name holds a word; `touch.py MODULE` shows a whole file's users. Never open the index.
4. **Edit** (1-3 steps). After an edit to code the chat is told one line: `After this edit: ... RERUN (N kit tests,
   about T): python3 source/kittests.py --names ...` (or `--changed`). Run that line, not the whole suite.
5. **Look** (1-2 steps): a short clip of just those seconds (`final OUT --small --span T0 T1`) or one cropped sheet of
   the changed frames; as a viewer at phone size first, then every point where two things meet at full size.
6. **Close it**: one line in the notes table ("8: fixed - the whale now knocks the helideck away. Clip sent."), plus
   "Lost:" / "Added:" lines for anything taken away or added.

## When the code is the problem
- `touch.py NAME` says "name-only maybe": a use on a value it cannot name (`film.frame_image()`); check those few
  by eye before trusting "no other caller".
- "+N kit tests reach it only through a command's main()": a whole-tool run; the final's kit run covers them.
- A fix in a shared function used by other films: the RERUN line already includes their kit tests; never skip them.
- A note the code cannot carry yet (a view or move the drawing cannot do): say in plain words what must be learned
  first (Statement Two), never a workaround that only looks like it worked.

## At the end of the chat
`python3 source/handover.py end --film FILM` (it now also checks the who-uses-this index and the MAPs), then
`python3 source/notesteps.py report` (steps per note, for the before/after measure) goes in the handover's Done line,
and `python3 source/ledger.py appcost FILM COST` with the app's own cost figure (get_session, this chat).
