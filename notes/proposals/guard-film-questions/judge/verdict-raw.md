## Leak
yes: mild. The problem file names the six-lines-above ("context-lines") rule as "the likely trigger" and points to Milburn review lesson 6, which states a fix (pass questions that name film content, keep blocking rules, tools, checks and kits). V1 is that fix almost word for word; V2 and V3 looked past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 3 | 3 | 5 | 15 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 3 | 3 | 2 | 2 | 3 | 13 |
## Sam test
Q1: Yes. An expert first stops the harm Sam actually feels (the same reply twice, because the guard runs after the text is on his screen), then tunes the sorting on labelled real replies, not on guessed word lists.
Q2: Yes, once widened: every logged block since 15 Nov (39 lines, all films), read in full from the chats' own records because the log cuts each question at 120 characters, plus the 15 Nov probe.
Q3: Root cause shown (checked: the guard is a Stop hook, logs only the second stop, says "reword the question"; probe still misses 9 of 12). Kit tests run the labelled list in every chat. Weak spot: the short-correction instruction relies on the chat obeying it, so the full block log measures it (F2).
Q4: Yes: word trimming, short corrections, self-labelling, learn-first, and (from V3) a gate on file edits were all weighed.
Q5: Each step is its own yes and can be undone alone (one reason text, one word-list change, one test list). Nothing loosens the guard before the labelled list shows it is safe.
Q6: Checked here: 39 log lines; probe 9/12 missed and "Which hook text: 1 or 2?" stopped; log written only on the second stop; Sam's "Why did you write your response 3 times?" (notes/ledger/sam/gr9hlufs.md). The split of the 39 is still unchecked until the Learn step labels them.
Q7: Sized to zero repeated replies and zero missed system asks on real data, not a word patch; honest cost about 1.2% of a week once.
Q8: Permanent; no trial. Reviewed at the end of the next film against the full block log.
## Pick
V2
## Why
V1 answers the problem's wording only: it loosens the guard on five Milburn lines while the guard already misses 9 of 12 system asks and still makes Sam read every stopped reply twice; it would cut some re-sends and change nothing he sees. V3 finds the same causes as V2 but its main change, a gate refusing edits to rules, tools and guides without a judged proposal, contradicts Sam's adopted rule that unasked changes are listed and judged at the end-of-film review, and the 15 Nov guard-holes verdict (F5) that parked exactly this gate until that review finds an unjudged change. It would also block urgent mid-film tool repairs, and it drops the question check altogether. V2 fixes what Sam sees first, then corrects the sorting only after it is measured on real replies, in separate yeses. Taken from V3: the labelling reads each full reply in the chats' records (the log is cut short); a "Critiqued:" line with the right numbers is accepted in any wording; path misreads like "notes/proposals/2.md" are fixed; and the mismatch between review item 7 and the log (the stale-test ask was sent) is named.
## Faults in the pick
- F1 [fixed] The labelling read only the 120-character log lines; it now reads each full reply from the chat records (from V3).
- F2 [named] Change 1 tells the chat to send only the missing piece; that still relies on the chat. The full block log records the length of each retry, so a chat that re-sends the whole reply shows up in the count.
- F3 [named] A Stop hook cannot hold a reply back; one short extra line per true catch remains. Removing that needs a check that runs before the text shows, which this tool does not offer.
- F4 [fixed] 10 of 39 blocks were judged proposals missing the exact Critiqued wording; that check now accepts the right numbers in any wording, and path misreads are fixed (from V3).
- F5 [named] Overlap with the plain-check proposal, which may change what the guard reads; built in whichever order Sam approves, both tested on the same labelled list.
- F6 [named] Review item 7 says the stale-test ask never reached Sam; the log says it was sent. Settled by the Learn step reading that chat.
## Final version
Learn (changes nothing, one Sonnet chat, about 0.4% of a week):
1. The guard logs every block, first time included, with the whole reply and the retry's length.
2. The chat reads the full reply behind each of the 39 logged blocks in its chat record and labels it: film question, ask to start the route, Critiqued-wording fault, path misread, or real unjudged system ask. Labels go into a fixed test list in the kit tests, together with the 15 Nov probe's 22 questions.

Change 1, its own yes (about 0.2%): when the guard stops a reply, its message tells the chat that Sam has already read it, and to send only the missing line or "ignore my last question, it is withdrawn", never the whole reply again. A kit test checks the message. To beat: full repeated replies per film from at least 5 (Milburn) to 0, counted in the full log.

Change 2, its own yes, only after Learn (about 0.6%):
- the six-lines-above rule counts only when the question points back ("that change", "this");
- asks to start or run the route pass;
- "Hook Text", "render", "recording" and similar film words no longer decide a question alone; permanence words ("every film", "from now on", "always", "every round") mark a system ask;
- a "Critiqued:" line with the right numbers passes in any wording; path misreads fixed.
Enforced by the kit test on the labelled list and the probe. To beat: 0 wrong stops on the list, 0 of the real system asks missed, probe misses 9/12 to 0.

Total about 1.2% of a week once. Reviewed at the end of the next film against the full block log.
## For Sam
### Option 1: Stop the repeats, then fix the guard on real messages
The guard (the check that reads my replies to you) runs after you have already seen a reply, so each stop makes you read it twice; and it gets it wrong about half the time, while still missing most real asks about changing how films are made. First, a stopped reply gets only a one-line correction, never a resend. Then a chat sorts every message the guard has stopped so far, and the guard is retuned and tested on those real messages before it changes.
Lost: the guard no longer treats a question as a system change just because one turned up a few lines above it.
Added: no repeated replies, fewer needless stops, a full record of every stop.
### Option 2: Only let film questions through
The guard lets questions about this film (a line, a recording, a shot, the effects) pass, and keeps stopping questions about rules and tools. Quick, but you would still see a reply twice whenever it stops one, and the guard would still miss most real asks.
Lost: a small risk of missing a system ask worded like a film question.
Added: fewer needless re-sends on film questions.
