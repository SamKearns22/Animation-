# Helper B: plain-check

## Leak
Mild: the title ("has no check") and the decision both assume the answer is a check on the finished message. No solution is spelled out.

## Results
- The rule was rewritten once already. On 14 Nov it was "what it is, why, what you'd notice"; on 16 Nov it got its current shape (git 4b469908). Rewording it did not stop the failures.
- 19 Nov: Sam said he could not follow in **3 separate chats**. Chat h3akq5qv at 09:11: "Explain listed jobs ... in very plain language". The review chat (iqdpxykr): "Explain" on lessons 2 and 6, "don't know what you mean by brow cap" on lesson 9, and "I still don't understand" on lesson 2 again. Chat yah6eyjt at 17:36: "Our simple communication tool isn't working". Source: notes/ledger/sam/.
- In the review chat, 3 of the 10 lessons needed explaining again and one needed it twice. That was 4 extra messages from Sam in one sitting (notes/ledger/sam/iqdpxykr.md).
- The lessons themselves have no "why" and no "what you'd notice", and their steps are lettered inside a paragraph (milburn-review.md section 3).
- The route's own template for Sam ("plain English, 3-6 lines", judge.md) does not ask for the rule's shape. So a chat that copies it faithfully still breaks the rule.
- The safety check (the "hook", a script that runs as a chat finishes each reply) let 10 replies through on their second try on 19 Nov. The problem file says 8; the right count is 10, from notes/proposals/unrouted.md. Anything this hook flags is still sent if the chat tries a second time.
- Gap: there is no record of what each chat sent Sam just before he said he was confused, and no set of good messages (ones he answered with a bare number). Without these, no checker can be scored.

## The real decision
The decision is where Sam's explanations get written, across every chat in a film, not how to inspect them afterwards. Right now every chat writes its own wording from scratch, from templates that break the rule, and the writer can't see its own project words. Two levers are bigger than a check: writing the explanation once, at the source, in the rule's shape; and having a reader who doesn't know the project test it.

## Root cause
1. The places the text comes from break the rule: judge.md's "For Sam" template, and the list format the review chat used. The chats copy them.
2. The writing chat lives inside the project's words ("guard", "pre-flight", "brow cap"), so it can't see which ones need explaining. Rewording the rule (14 Nov to 16 Nov) changed what it asks for, not who checks it, which is why that fix failed.
3. The hook only checks that a judged proposal exists, never the words. And it gives way on the second try.
4. "About 10 lines" pulls against the full shape. Ten lessons in full shape is a long message, so the chat squeezed them.

## Approaches weighed
- **A. A word-and-shape check on every reply.** It would look for numbered steps, Why / You'd notice / Other option / Lost / Added, and code names (file names, backticks, underscores, tool names from kit-catalogue). It's cheap, but a chat can fill the labels with jargon and still pass.
- **B. Reframe: write it at the source.** The route's text for Sam is built in the rule's shape and refused if it isn't. Chats paste that text and don't write their own.
- **C. A blind reader.** A fresh helper sees only the message and "Sam doesn't code". It lists every word it wouldn't follow and retells the change in its own words. A wrong retelling fails.
- **D. Learn first.** Score A and C on real messages from the record before wiring anything in.
- **E. A glossary.** Fixed plain meanings for project words. Rejected: it adds reading for Sam and doesn't make the messages plainer.

Chosen: D first, then B, using whichever checker D shows works (A, C or both).

## Proposal
**Step 0, learn (changes nothing).** Gather the bad messages: the 10 lessons, the `show front-on-focus` text, and what Claude sent just before each of Sam's 5 confused messages. Gather good ones: system asks Sam answered with a bare number or Y, plus routine messages (animatics, clips). Score check A and blind reader C on both piles.
To beat: catch every bad message, pass at least 9 in 10 good asks, and pass every routine message.
Cost: about 1.5% of a week (unchecked).

**Change 1 (needs its own yes).** The route writes Sam's text in the rule's shape at the source. judge.md's "For Sam" template gets the rule's parts, changed through the route's lock because the prompts are locked. `propose.py record` refuses a verdict whose text fails the checker that won step 0. A plain-language test example (the Milburn lessons, which must fail) is added to the hook's test.
To beat: zero "explain" or "don't understand" replies on the next 3 proposals (counted from notes/ledger/sam).
Cost: 0.1–0.3% of a week per proposal (unchecked).

**Change 2 (separate yes, after Change 1 holds).** The hook requires the reply to carry the route's text word for word (it already does this for the Critiqued line). Its block message includes the exact text to paste, so the second try passes instead of sending the reply anyway.
To beat: second-try let-throughs, 10 on 19 Nov, down to 0 in the next film.

**Change 3: only if step 0 shows the checker is accurate on free-written text.** Extend the check to explanations that aren't proposals, like "explain the jobs".

What Sam would notice: each system ask looks the same every time. The problem, numbered steps, why, what changes for him, the other option, then Lost and Added. No unexplained words. Fewer "explain" replies needed.

## Sam test
- Q1: Writing it once at the source and testing with an outside reader is the standard fix when a writer can't see its own blind spots.
- Q2: The evidence covers 3 chats and 5 confused messages from 19 Nov, not just one chat.
- Q3: The root cause has evidence behind it. A blind reader stops labels filled with jargon from passing. The hook and `record` enforce it, so no chat has to remember to.
- Q4: Five different approaches weighed.
- Q5: Each change can be undone on its own. Nothing goes live until step 0 has scored it on real messages.
- Q6: Every fact has its source. Costs and the review's exact wording are marked unchecked.
- Q7: The cheap version (A alone) was rejected because it can be passed on paper.
- Q8: Each change is permanent, with nothing on trial, and is reviewed at the film's end.

## Lost / Added
Lost: messages with system asks get longer. Each proposal costs about 0.1–0.3% more.
Added: one source for Sam's text, an outside reader checking the wording, and a tested must-fail example.

## Unchecked
- The costs.
- Whether the lessons reached Sam word for word.
- How accurate the blind reader is.
- How many blocks the chats fixed themselves (only the let-throughs are logged).
