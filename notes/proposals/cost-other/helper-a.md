# Helper A: the unexplained two thirds

## Leak
None. The Facts lean towards splitting stepcost's "other"; weighed below, not assumed.

## Results
- Milburn: 15 chats, 1,281 steps, ledger 32.4% against Sam's app 22.0%; 33 notes, 4 repeats (milburn.json; milburn-review.md).
- "Other" is 58-87% of every chat (milburn.md). A step costs about $0.062 on average ($79.4 / 1,281, milburn.json at WEEK_USD 245).
- Prices do not explain the 47% gap. In app-costs.tsv (85 chats, real app dollars plus read, write and output
  tokens), costwatch's prices give $332 against the app's $317 for Opus. So the gap is WEEK_USD (provisional) or
  double counting. A WEEK_USD error scales every chat alike and leaves the shares true; double counting does not.
  Which it is: unchecked.
- Rough split from the ledger alone (steps and end history, an 83k start, linear growth; my estimate): starting
  context re-read ~22%, carried history re-read ~21%, new history written ≥18%, output and the rest ~38%.
- The app's usage figure (get_session) gives each chat's dollars and read, write and output tokens without the
  transcript (app-costs.tsv header, 13 Nov). Whether it still answers for Milburn: unchecked.
- Gap: nothing records how many steps went on rework against first builds.

## The real decision
The decision is which lever brings a whole film from 22% to 15% (a 32% cut) without losing quality. Cost ≈ steps ×
context per step × read price, plus writes and output. Steps per film and context per step are bigger levers than
any kind of call. Naming "other" is only the tool for choosing between them.

## Root cause
stepcost was built to answer the search question, so it charges cost to kinds of tool call. Most cost belongs to
no single call: the ~83k start re-read at every step, Claude's own writing (code in Edit and Write) re-read later,
and the calls it does not name. All of it falls into the remainder (stepcost.py measure(), read). The startup-reading
cut (16 Nov) trimmed repo text, but ~80k of the ~90k start is the app's own (startup-reading.md line 22), so the
start-up share stayed near 22%.

## Approaches weighed
1. More call kinds in stepcost. "Other" gets smaller, but there is always a remainder.
2. Reframe: split each step exactly by where its tokens came from (start, carried history, new writes, output),
   then split only the history part by call kind. No remainder.
3. Learn first: the app's usage figures for the 15 Milburn chats, plus the ledger, answer Milburn now.
4. Read the transcripts back with list_events (~7% of a week). Costs more than 3 for little extra.
5. Cut steps straight away. There is no evidence yet of which steps.
Chosen: 3, then 2.

## Proposal
**Learn (changes nothing).** One Sonnet chat reads the app's usage figure for each Milburn session and sets it
against the ledger rows. The same ratio on every chat means WEEK_USD; differing ratios mean double counting. The
chat gives Milburn's split by token origin, and its steps by stage and by rework, as a table in the proposals
folder. ~0.3-0.5% of a week.

**Change 1 (its own yes, after the table).** stepcost splits every chat exactly by token origin; the history part
is split by call kind, with Claude's own writing as a kind. It runs at every chat's end (the Stop hook). Its test
fails unless the parts add up to real cost within 1% and the remainder is under 5%. Number to beat: a remainder
under 5% on every new chat (now 58-87%). ~1% of a week, Opus medium.

**Then, each separately:** a WEEK_USD fix if that is the cause, and the lever the table ranks first, each through
the route with its own number, held to the next film. None of these is in this yes.

Sam would notice: one message on where Milburn's 22% went and why the meter read 32; then no big "other".

## Sam test
Q1: Yes. An expert splits cost exactly by token origin before choosing a lever.
Q2: All 15 chats on real app figures; it adds the rework count.
Q3: The test needs the parts to add up and the remainder under 5%, so it cannot pass on paper; it runs on every chat.
Q4: Five approaches weighed; only this one removes the remainder.
Q5: Learning changes nothing; Change 1 is one file, guarded by its test, and undone by reverting it.
Q6: Sources named.
Q7: Sized for a full split, not a relabelling; ~1.5% once.
Q8: Permanent once made; reviewed at the next film's end.

## Lost / Added
Lost: nothing; the call kinds stay. Added: an exact split on every chat; Milburn's answer; the cause of the 47%.

## Unchecked
Whether get_session still answers for Milburn; the cause of the 47%; my rough split; both costs.
