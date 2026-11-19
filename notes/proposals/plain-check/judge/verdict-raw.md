## Leak
yes: mild. The title ("has no check") and the "test case that must fail" line point at a detector run on finished messages; the decision line itself is open. All three versions name it; V3 follows it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 3 | 4 | 19 |
| V2 | 5 | 4 | 3 | 4 | 4 | 20 |
| V3 | 3 | 2 | 4 | 3 | 5 | 17 |
## Sam test
Q1: Yes for the pick: fix the place the text is made, test it with an outside reader that knows only "Sam doesn't code", and calibrate that reader on Sam's own confused replies before trusting it. A regex jargon list (V3) is what an expert would not stop at.
Q2: Evidence is the right kind: Sam's 8 "I'm lost" messages across 3 chats on 19 Nov (checked in notes/ledger/sam: h3akq5qv:69, iqdpxykr:8,12,19,23,33,56, yah6eyjt:13), the template itself, and the failed 14-to-16 Nov rewrite (git 4b469908). Status explanations ("explain the jobs") are in scope but gated on the learn step.
Q3: Root cause found (the route's own template breaks the rule; a writer steeped in project words can't see them; the only check reads routing, not words). Enforced by the recorder and the hook, not by a chat choosing. Paper compliance (labels present, jargon inside them) is caught by the reader. Success is counted from Sam's own replies in the ledger.
Q4: Five approaches weighed (detector, make-at-source, blind reader, learn-first, glossary); make-at-source plus reader is the strongest.
Q5: Three separate yeses, each undone alone. Risks named: the hook refusing twice could loop a chat (F3); the reader is unproven until Step 0 scores it.
Q6: Facts checked: 10 let-throughs on 19 Nov (not 8), judge.md's "plain English, 3-6 lines", parser checks only Lost/Added, 3 of 10 lessons re-explained, route spent 79% of a week over 36 chats. Costs and reader accuracy are unchecked and said so.
Q7: Not the cheap version: the detector-only route (V3) is rejected; the reader is kept, gated on evidence, not on price. Honest cost stated.
Q8: Nothing provisional: Step 0 is measurement; each change is permanent and reviewed at film end.
## Pick
V2
## Why
V2 rests on the strongest checked evidence: it found what Sam actually failed to follow (lessons 2, 6, 9; "brow cap"; "explain the jobs") and that the rule was already rewritten once without enforcement, which is the real proof that wording alone fails. Its must-fail / must-pass sets come from real messages (asks Sam answered with a bare number vs the ones before his confused replies), so the checker is calibrated on the result that matters; V1 calibrates on three hand-picked texts. V2 measures success from Sam's replies, already logged; V1 relies on chats noting "didn't follow" by hand. Each change is its own yes.
Taken from V1: the exact fixed fields the route must fill; putting the review's lessons through the same maker (they are the failing case, and V2 left them to a kit test only); keeping the hook's film-question misfires out (they belong to their own proposal).
Taken from V3: a cheap fixed layer under the reader that refuses file and code names outright (anything with _ . / or joined capitals), as the rule says "no code names".
V3 bolts a word list onto a check that already gives way after one block and already misfires on film questions; plain words used as project names ("guard", "kit") slip past, and the list goes stale every film.
## Faults in the pick
- F1 [fixed] V2 left the review's lesson lists (the case that failed) outside the maker; now they use it.
- F2 [fixed] V2 did not say how a script can run "the reader"; it is a helper like the judge, writing a file the recorder checks by hash.
- F3 [named] Change 2, a hook that refuses twice, can loop a chat if the pasted text never matches; the refusal carries the paste-ready text and a third refusal is never made.
- F4 [named] Costs (~1.5% learn, ~2% build, ~0.2% per proposal) are unchecked estimates, on a route that has already cost 79% of a week.
- F5 [named] Changing judge.md needs the route's lock (`propose.py lock --verdict plain-check`); this verdict's own "For Sam" still follows the old 3-6-line shape.
- F6 [fixed] The rulebook row for this rule names no check; Change 1 adds it.
- F7 [named] Whether the Milburn lessons reached Sam word for word is unchecked; Sam's replies show they reached him in that form closely enough to confuse him.
## Final version
Step 0, learn (changes nothing; same chat). Build two checkers on paper: (A) a fixed shape-and-name check: problem in 1-2 sentences, numbered step lines, Why, You'd notice, Other option, one Lost: and one Added: line, and no file or code names; (C) a blind reader, a fresh Sonnet helper given only the message and "Sam doesn't code, uses an iPhone", that lists every word it can't explain and retells each step; a wrong retelling or any listed word fails. Must-fail: the 10 Milburn lessons, `show front-on-focus`, Claude's message before each of Sam's confused replies (19 Nov ledger). Must-pass: system asks Sam answered with a bare number or Y; routine animatic and clip messages. Score A, C, A+C. To beat: every must-fail caught, 9 in 10 good asks passed, every routine message passed. The winner is what Change 1 uses.

Change 1 (own yes): make the text at the source. judge.md's "For Sam" becomes fixed fields (problem, numbered steps, why, what you'd notice, other option, Lost, Added), through the lock. The parser refuses a missing field; `show` prints them in that order. `record` refuses a verdict until the reader's pass file (with the verdict's hash) exists and A passes. The end-of-film review writes its lessons through the same fields and `show`. The kit test gets the Milburn lessons as must-fail and a good ask as must-pass. The rulebook row names this check. To beat: no "explain" / "don't understand" reply from Sam on the next 3 system asks (ledger search).

Change 2 (own yes, after Change 1 meets its number): the hook requires the shown option text in the reply, as it already requires the Critiqued line; its refusal carries the paste-ready text, so the second try passes; it never refuses a third time. To beat: let-throughs from 10 a day to 0 over the next film.

Change 3 (own yes, only if Step 0 shows the reader accurate on free text): status explanations of back-end work ("explain the jobs") go through the reader before sending.

Not included: the hook taking film questions for system asks (its own proposal).
## For Sam
### Option 1: Write it right at the source, then test it on a stranger
Problem: the template that writes my asks to you breaks your plain-language rule, and nothing checks it.
1. First I test two checkers on your real messages from 19 Nov: ones you followed and ones where you said "explain".
2. Then (your yes) every ask is written in your rule's shape: problem, numbered steps, why, what you'd notice, other option.
3. A fresh helper who knows only "Sam doesn't code" must understand it, or it isn't sent.
Why: rewriting the rule on 16 Nov didn't work because nothing checked it. You'd notice: asks arrive in one shape, fewer "explain" replies; animatics unchanged.
Lost: short one-paragraph asks; a few minutes per ask.
Added: one shape for every ask, an outside reader, a measure taken from your own replies.
### Option 2: A word-and-shape filter on every message
Problem: same.
1. A check reads each ask for the parts your rule lists and a list of banned project words, and sends it back if any is missing or unexplained.
Why: quick to build. You'd notice: asks in the right shape, but a project word that looks plain (like "guard") can still slip through, and it still lets a message past after one try.
Lost: a little writing time per ask.
Added: a fixed shape and a word list to keep up to date.
