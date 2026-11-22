# Helper A: Claude's own thinking and code writing (grand-theft-autism)

## Leak
None. The problem file states the problem and the record only.

## Results
- The film spent 54.67% of a week in 28 chats against an estimate of 53.2%, with stages up to animatic 1 done and no round of notes logged yet. That is 3.6 times the 15% aim (`dearest.py`, ledger .md).
- Claude's words came to 23.86% of a week by my sum over the ledger .json (output plus Claude's earlier output carried in history; `dearest.py` says 22.3%). **Only 14.05% was the writing itself. About 9.8% was paying again to re-read Claude's own earlier words at every later step** (the "Claude's words" block against the origin, every row of `grand-theft-autism.json`).
- The chats were long: 100 to 184 steps, with 250k to 330k of history at the end (e.g. a18a5702: 159 steps, 330k, 4.37%; 77034bac on Sonnet: 184 steps, 47.6% carried history). Source: ledger .json.
- Only one row is split into named parts (7a739e72): thinking 21.9% and writing code 11.0% of that chat. The problem file says "two" such records. I found one on this film; the second is unchecked.
- **Most of the work went into redoing one 6.2-second shot.** Shot 4 has gone through at least 9 versions across chats 6 to 27 (`notes/shot4-case-study/shot4-case-study.md` §2 and §16). 22 of the 28 chats searched its code (`gta_rehearse`/`leanout`). Sam gave "the backwards arm is a gross distended sausage" a fourth time (rule 30), and he said "I am surprised you delivered it to me" (`notes/grand-theft-autism.md` lines 97, 182, 212).
- Gap: every ledger row reads "0 notes, 0 repeats" (`handover.py` line 609 says nobody logged them). So the record cannot say how much of Claude's thinking and code went to first builds and how much to redoing work Sam had already rejected. That split is what the decision turns on.

## The real decision
The decision is not "how can Claude think or write less per chat". It is "why does one film need about 24% of a week of Claude's words when the whole film should cost 15%". The unit is the whole film. Two levers are bigger than the writing itself: rework after a fault reaches Sam, and Claude re-reading its own words in long chats.

## Root cause
Claude's words are dear because the same drawing problem gets solved again and again. Each new version of shot 4 means fresh thinking and fresh code. Then every later step re-reads all of it. Two earlier attempts failed:
- The fixes for the arm patched the picture without a check that would catch the arm on the old frames. That is why the note came back a fourth time.
- The rule against repeats (rule 30, and "Seeing like Sam" point 3 in CLAUDE.md) depends on a chat reading it and choosing to follow it. Nothing stops a clip from going to Sam while a repeated note's check is missing.

The cost tools measured kinds of step, not redoing, so the waste never showed up as a number.

## Approaches weighed
1. Think and write less: lower effort, shorter replies. This is the cheap-but-worse trap and works against quality. Rejected.
2. Reframe and learn first: split Claude's words by shot, by note, and by first build against redo, using the 28 records. Then cut redo where it is shown to be largest.
3. Gate repeated notes: a clip carrying a fix for a seen-before note cannot be sent until the new check is shown to catch Sam's old picture.
4. Shorter chats so less history gets re-read. This trades against each new chat's start-up reading (22-30% of a chat), so it needs measuring before anyone sets a number.
5. Learn the drawing first: build and test the hard pose (the arm from behind or in a doorway) as a reusable kit piece before any shot uses it.

Chosen: 2 first, then 3, then 4 only if 2's numbers support it. Approach 5 is folded into 3: the gate's test is learning the drawing before the shot.

## Proposal
**Learn first (changes nothing):** a tool reads the 28 chat records and splits Claude's words three ways:
- by shot or task;
- into first builds and redoing work Sam had already seen;
- into the writing itself and the re-reading of it.

It also fills in the missing note and repeat counts from Sam's messages. Cost: about 1.5% of a week, once, on Opus medium. The result names the share spent on redo. My expectation, unchecked: well over half.

**Change 1 (only if redo is at least a third of Claude's words):** the repeat gate. The sending and handover tools refuse a clip or animatic while any note logged as "seen before" lacks a saved test: the new check run on Sam's own marked-up picture, and flagging it. Enforcement is by the tool, not by reading.
- Number to beat: repeated notes per film. Grand-theft-autism had at least one note given four times; the target is 0.
- Second number: Claude's words spent on redo, against Change 1's measured baseline.

**Change 2 (separate yes, after the next film's numbers):** a chat-length limit set from the measured break-even between re-reading history and a new chat's start-up reading. Number to beat: the 9.8% of a week spent re-reading Claude's own words.

Cost: the learning step is about 1.5%. Each change is a small tool edit of about 1-2% once. Every film then saves rework against the 15% aim.

What Sam would notice: no repeated notes reaching him. Clips that come back later but right.

## Sam test
- Q1 Expert: an expert would measure the waste (redo) before cutting the effort that makes quality. This does.
- Q2 Best result: it uses all 28 chats, not one row, and is at the film's scale.
- Q3 Comprehensive: tools enforce the gate, not memory. Each change has a number, and the root cause is named with evidence.
- Q4 Most intelligent: five different approaches weighed. Two were rejected or deferred, with reasons.
- Q5 Risk: the learning step changes nothing. Each change can be undone on its own, and nothing is untested.
- Q6 Checked: sources named; the guesses are listed below.
- Q7 Not the cheap version: it cuts redo, not thinking. Sized by the result.
- Q8 Nothing temporary: each change is made properly or not at all, and reviewed at the film's end.

## Lost / Added
- Lost: a clip with a repeated-note fix can no longer reach Sam until its check is proven, so some clips come later.
- Added: one learning tool, a repeat gate in the sending tools, and later (separately) a measured chat-length limit.

## Unchecked
- The second fully named record named in the problem file.
- Whether redo is really over half of Claude's words. The learning step answers it.
- The exact cost of the learning step and the chat-length break-even.
