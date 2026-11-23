# Plain-check Step 0: the two checkers on paper (23 Nov, chain A chat 4; changes nothing)

## What was tested
25 saved messages (cases/, labels and Sam's replies in cases.json). Claude's own 19 Nov chat messages could not be
read (those chats return "not found" from this account), so the cases are the saved copies of what Sam was shown:
- must-fail (15): the 10 Milburn lessons (milburn-review.md section 3; Sam: "Explain" on 2 and 6, "don't know what you
  mean by brow cap" on 9, Y on 1, 3, 4, 8); `show` of front-on-focus (Sam 17:36 "not following your explanations") and
  of check-catches, cold-start, cost-other, finder-learn-finish (Sam 20:12 "explain my options in simple language").
  Matched to his replies by time (handover-end log), unchecked word for word.
- must-pass (7): `show` of asks Sam answered with a bare number or adopted with no "explain" reply found in his saved
  messages: aim-check, could-not-test, big-body-moves, one-route-kit, solid-body-moves, bench-speedup, fast-climb.
- routine (2): chain A chat 3's last reply (23 Nov, read from the chat record); CLAUDE.md's model note line.
- mixed (1): plain-check's own options (Sam: "convoluted", then chose 1).

## Numbers (score.py; reader3/ for C3)
| checker | must-fail caught | must-pass passed | routine passed |
|---|---|---|---|
| A, fixed shape (Problem, numbered steps, Why, You'd notice, Other option, Lost, Added) and code names | 15/15 | 0/7 | 0/2 |
| A, code names only | 1/15 (milburn.py) | 7/7 | 2/2 |
| C, blind reader as written (knows only "doesn't code, iPhone") | 15/15 | 0/7 | 0/2 |
| C2, C counting only words Sam never typed himself | 15/15 | 0/7 | 0/2 |
| C3, reader first reads Sam's own messages before 19 Nov (12 cases) | 6/6 | 0/4 | 0/2 |
To beat (Final version): every must-fail caught, 9 in 10 good asks passed, every routine passed. **Nothing met it.**

## What it shows
- The good asks break Sam's rule as much as the bad ones. C3 found 6-15 unexplained coined phrases per good ask
  ("distance grid", "compiled drawing", "working shelf", "a plan is priced") against 7-11 per confusing one ("brow
  cap", "house head", "named lines", "the guard"). Sam answered the good ones anyway: a bare "1" shows trust in the
  pick, not that he followed it. So his replies cannot tell a plain ask from an unplain one; the rule can.
- Every reader understood the gist (WRONG marks: 0-2 per message, the same in both groups); what fails is the words.
- Words one at a time don't work: Sam has typed 2,037 different words himself, including "brow" and "cap"; he still
  didn't know "brow cap". Coined phrases are the fault.
- The old shape (one paragraph per option) fails A everywhere, as expected: the new fields do not exist yet.

## What this decides (put to Sam)
The reader gate works only as Sam's rule literally says: every coined phrase explained where it appears. Built as
written it would have refused all 7 asks he was happy with, and his own model note line (the whale), so every ask gets
longer. Whether that is wanted is Sam's call (question in the handover). A (the fixed fields) is his rule's own list and
needs no learning. The reader is the C3 version (reads Sam's earlier messages first); reader.md holds it.
Cost of Step 0: about 2.6% of a week in helpers (37 Sonnet readers), against ~1.5% estimated.
