# Helper B: plain-check

## Leak
Mild: the title assumes a check on the finished message.

## Results
- The rule already failed once after a rewrite: 14 Nov (what, why, what you'd notice) replaced 16 Nov by today's shape (git 4b469908). Neither was enforced.
- 19 Nov, Sam lost the thread in 3 chats, 8 messages (notes/ledger/sam/): h3akq5qv:69 "Explain listed jobs ... in very plain language"; iqdpxykr:8,12 "Explain" (lessons 2, 6), :19 "don't know what you mean by brow cap", :23 "I still don't understand", :33 and :56 complaints; yah6eyjt:13 "not following your explanations". So 3 of 10 lessons needed re-explaining.
- The route's own template is "plain English, 3-6 lines" (judge.md:62-70): copied faithfully, it still breaks the rule.
- The hook (script run as each reply ends) let 10 replies through on a second try on 19 Nov, not 8 (unrouted.md). It checks routing, never words (propose.py:392-416).
- The route has cost 79% of a week over 36 chats (notes/ledger/proposal-route.md), so per-proposal additions must be small.
- Gap: no scored set of messages Sam could and couldn't follow exists to test a checker on.

## The real decision
The unit is everything a chat tells Sam about the system across a film: asks and status explanations. The question is where Sam's text is made and who checks it can be followed. Bigger levers than a reply check: one source for the text, and a reader outside the project.

## Root cause
1. The texts chats copy from break the rule (judge.md "For Sam", the review's lesson format).
2. A chat steeped in project words ("guard", "pre-flight", "brow cap") cannot see which need explaining; the 16 Nov rewrite changed the ask, not the checker, so it failed the same way.
3. The only enforcement checks routing, not words, and gives way on the second try.
4. "About 10 lines" pulls against the full shape, so 10 lessons were squeezed.

## Approaches weighed
- **A. Shape-and-word check on replies** (numbered steps, labels, code names). Cheap, but jargon in the labels and plain words used as project names ("guard") pass.
- **B. Reframe: make the text at the source.** The route writes Sam's text in the rule's shape and refuses failures; chats paste it.
- **C. Blind reader.** A fresh helper sees only the message and "Sam doesn't code", lists words it can't follow, retells the change; a wrong retelling fails.
- **D. Learn first.** Score A and C on real messages before wiring either.
- **E. Glossary.** Rejected: more reading, messages stay unplain.

Chosen: D, then B, enforced by D's winner.

## Proposal
**Step 0, learn (changes nothing; same day; ~1.5% of a week, unchecked).** Must-fail: the 10 lessons, `show front-on-focus`, Claude's message before each of Sam's 5 confused replies. Must-pass: system asks Sam answered with a bare number or Y; routine animatic and clip messages. Score A, C, A+C. To beat: every must-fail caught, 9 in 10 good asks passed, every routine message passed.

**Change 1 (own yes): the source.** judge.md's "For Sam" takes the rule's exact shape (via the route's lock); `propose.py record` refuses text failing D's winner; the hook's kittest gets the Milburn lessons as must-fail. To beat: zero "explain"/"don't understand" replies on the next 3 system asks (search of notes/ledger/sam). Cost ~2% to build, ~0.2% per proposal (unchecked).

**Change 2 (own yes, after Change 1 meets its number): the hook stops giving way.** It requires the route's text word for word, as it does the "Critiqued" line, and its block message carries the paste-ready text so the second try passes. To beat: let-throughs from 10/day to 0 over the next film.

**Change 3 (own yes):** non-proposal explanations ("explain the jobs"), only if Step 0 shows the checker accurate on free text.

Sam notices: every system ask has one shape, no unexplained words, fewer "explain" replies. Animatics and clips unchanged.

## Sam test
- Q1: Source-first plus an outside reader is expert practice.
- Q2: Evidence is 3 chats, 8 messages and the template, not one chat.
- Q3: `record` and the hook enforce it; the blind reader stops jargon passing on paper; success counted from Sam's replies.
- Q4: Five different approaches; B reframes, D learns first.
- Q5: Each change undone alone; none goes in unscored.
- Q6: Facts sourced; costs unchecked.
- Q7: A alone (the cheap trap) rejected.
- Q8: Changes permanent, reviewed at film end; Step 0 is measurement, not trial.

## Lost / Added
Lost: shorter system asks; ~0.2% of a week per proposal.
Added: one source for Sam's text, an outside reader, a must-fail test, a hook that no longer gives way.

## Unchecked
Costs; whether the lessons reached Sam word for word; blind-reader accuracy; how many 19 Nov blocks were fixed first try.
