## Leak
Slight: the title ("has no check") and "the test case that must fail" frame the answer as a detector on messages. Set aside below.

## Results
- The route's own Sam-facing text breaks the rule by design. judge.md's "For Sam" shape is "plain English, 3-6 lines / Lost / Added" (judge.md, lines 62-70); `show` prints it unchanged (propose.py `show`). My count over all 27 judged proposals' "For Sam" sections (notes/proposals/*.md with a verdict hash): none has numbered steps for its options (one has two numbered lines), 8 say "why/because", 15 mention "notice". Rough by-eye count of the 8 parts: 0 of 27 pass.
- front-on-focus's Option 1 (checked): one paragraph, no steps, "the BoJack way", "house head", "planning step", "best tool" unexplained.
- milburn-review.md section 3 (checked): 10 lessons with lettered inline steps, no "why" or "what you'd notice", unexplained "pre-flight", "ledger", "kit tests", "milburn.py", "chain depth", "0.14 brow cap". That they reached Sam in this form is unchecked word for word (problem file); Sam answered them by number the same day (milburn-review.md, last section).
- The only guard blocks once, then lets the reply through: 28 let-throughs logged, 10 on 19 Nov (notes/proposals/unrouted.md; the problem file says 8). The Milburn review judged 4 of its 5 blocks to be film questions taken for system asks (milburn-review.md, item 10). Precision is poor and the leak is built in.
- Cost of unclear asks: not measured. Nothing records when Sam doesn't follow (asks "what's X?", answers off-target, says he is lost). That gap is a finding.

## The real decision
Not "add a check on messages" but: who writes the words Sam reads about back-end changes, and in what shape. Every Sam-facing back-end text is made in a few places (the judge's "For Sam", the review's lessons, a chat's own "should I…" line). A bigger lever than any detector: make the makers emit the right shape, so the check only confirms the made block was sent.

## Root cause
The rule lives only as a sentence in CLAUDE.md, while the route that produces the actual text carries a contrary fixed shape (3-6 lines, two lines Lost/Added) that its parser enforces. Chats follow the machine, not the sentence. Second cause: "every technical word explained" has no definition of "technical" for this project, so no writer or check can apply it. Third: the hook's single block plus regex word-spotting means any bolt-on shape check leaks the same way the route check does.

## Approaches weighed
1. Detector: a Stop-hook check scanning every reply for the 8 parts and a jargon list. Leaks after one block, regexes on free prose misfire (as the guard already does).
2. Reframe, made-to-shape: the judge fills fixed fields (problem, numbered steps, why, what you'd notice, other option, Lost, Added); the parser refuses a missing field; one renderer prints them; the hook asks only that the rendered block (marked by its hash) is in the reply. Review lessons and other back-end asks use the same renderer.
3. Fresh-reader test: a new Sonnet helper given only the rendered block and a one-line portrait of Sam lists every word it can't explain and restates each step; any gap blocks. Tests understanding, not words.
4. Learn-first: score every past Sam-facing back-end text and calibrate the reader on known-bad and known-good examples before building.
Chosen: 4, then 2, then 3, one at a time.

## Proposal
Learn (changes nothing): score the 27 verdicts' "For Sam" and milburn-review section 3 against the 8 parts with a short script; run a fresh reader on front-on-focus, milburn-review lesson 1, and one hand-rewritten good version. Number to beat: 0 of 27 pass; the reader must fail both bad ones and pass the good one, or step 3 is not built. Also start counting, in each film's notes, "Sam didn't follow" moments (the missing measure). About 0.5% of a week.

Change 1, made-to-shape: judge.md's "For Sam" becomes fixed fields; the parser refuses a verdict without them; `show` renders the 8 parts in fixed order with a hash line; the hook requires that rendered block (not just the Critiqued line); review lessons go through the same renderer. Enforced by the parser and the hook. Beat: 100% of route outputs pass the script from the learn step; the Milburn section-3 text and front-on-focus output are refused (added to the kit test). About 1.5% of a week once.

Change 2, fresh reader: runs inside `record`; no rendered block without a pass; flagged words get an explanation written in place. Beat: zero reader-flagged words in sent blocks, and the "didn't follow" count falls film over film. About 0.2% of a week per proposal.

Not bundled: the hook letting a reply through after one block, and its film-question misfires, are their own proposal (guard-film-questions exists).

Sam would notice: every back-end ask arrives in the same shape (problem, numbered steps, why, what you'd see, other option, Lost, Added), with odd words explained on the spot.

## Sam test
Q1: Expert: fix the producer, verify output, test with a proxy reader; yes.
Q2: Best result: whole path and all 27 verdicts, not one chat.
Q3: Comprehensive: enforced by parser and hook, not by a chat choosing; reader catches paper compliance; measured by the score and "didn't follow" count.
Q4: Most intelligent: four distinct approaches weighed.
Q5: Risk: each change undone alone; reader built only if calibration passes.
Q6: Checked: sources named; unchecked items listed.
Q7: Not cheap: the reader is the costly part and is kept, gated on evidence.
Q8: Nothing temporary: each change permanent; reviewed at film end.

## Lost / Added
Lost: the short 3-6-line options; asks get longer (allowed: "may run over the 10-line limit"); about 0.2% of a week per proposal.
Added: one fixed shape for all back-end asks; a reader test; a measure of when Sam is lost.

## Unchecked
Whether the Milburn lessons reached Sam word for word; my 0-of-27 count is by script and eye, not a careful read; whether the hook can carry the rendered block's hash without false blocks on edited replies.
