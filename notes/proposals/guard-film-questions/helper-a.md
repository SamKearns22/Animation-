# Helper A: the guard stops plain film questions

## Leak
None.

## Results
- notes/proposals/unrouted.md: 39 replies sent after a block, 15-22 Nov. My reading (full replies not kept): ~8 film
  questions (props stage, "Report", effects, Hook Text, shot 4 camera...); ~11 asks to START the route; 10 judged
  proposals missing the exact "Critiqued" line; 2 misread paths ("2.md"); ~7 real unjudged system asks. About half
  the blocks were wrong.
- The log only records a block the re-send did NOT fix (`log_unrouted` runs only on the second stop). The true number
  of blocks is unknown: a gap in the record.
- Every block makes Sam read a reply twice: the Stop hook (source/propose.py `hook`) runs after he sees it. Sam, 22 Nov (notes/ledger/sam/gr9hlufs.md): "Why did you write your response 3 times?" A true format
  catch that still cost him repeats.
- Run today: the three Milburn film questions are not changes on their own words; "Hook Text" matches "hook". Props
  stage trips via the six-lines-above rule ("run"); the other two unchecked (log cuts at 120 characters).
- notes/proposals/guard-holes.md is marked adopted (15 Nov), yet its probe run today still misses 9 of 12 change asks
  and stops "Which hook text: 1 or 2?". The last fix was never built or was lost.

## The real decision
Not "let film questions through" but: how the whole film's chats stop unjudged system asks without Sam ever reading a
reply twice. The bigger levers: when the check runs (after Sam sees text), the half of wrong stops that are not film
questions at all (route-start asks, exact-wording faults), and a guard whose adopted fix never landed.

## Root cause
1. The check runs after the reply is shown, so every stop, right or wrong, is a repeat for Sam.
2. It guesses from word lists; it cannot tell "the 1am run" from running a tool, and treats "may I start the
   route?" as an unjudged change.
3. The fault text says "reword the question", so chats word around it, and nothing tests it against real replies:
   the 15 Nov probe was invented questions, and the adopted widening was never checked as built.

## Approaches weighed
1. Trim the word lists (the problem's frame). Whack-a-mole; already failed once (Hook Text).
2. Reframe: make a stop never reach Sam twice: the block tells the chat Sam has read the reply, so send only the one
   missing line or "ignore my last question, it is withdrawn", never the whole reply again.
3. Chats mark system asks themselves; the guard checks marks plus permanence words. Relies on the writer.
4. Learn first: keep every block with its full reply and Sam's later answer, build a labelled set from real chats.
Chosen: 4, then 2, then the classifier fix measured on 4's set.

## Proposal
Learn (changes nothing): the guard logs every block, first time included, with the whole reply; one Sonnet chat labels
the 39 existing lines (film, route-start, format, path, real ask) into a fixed test list in kittests. ~0.4% of a week.
Change 1 (repeats): the block reason tells the chat to send only the missing piece, never the reply again; a kittest
checks the reason text. Beat: replies Sam sees twice per film, Milburn ≥5 (unrouted.md) to 0 full repeats, counted
from the new log. ~0.2%.
Change 2 (wrong stops), after Learn: drop the six-lines-above rule unless the question points back ("that change",
"this"); pass asks to start or run the route; "Hook Text" is not a hook; add the permanence words guard-holes named.
Enforced by the kittest on the labelled list plus the guard-holes probe. Beat: wrong stops on the labelled list 0;
real asks missed 0 of ~7, probe misses 9/12 to 0. ~0.6%.
Each its own yes. ~1.2% once, against 15% per film. Sam notices: no repeated replies, fewer re-sends.

## Sam test
Q1: an expert fixes the timing and measures on real replies before tuning words.
Q2: scope is every logged block across films, not Milburn's five.
Q3: root cause named; kittests enforce it in every chat; the probe catches a fix that never lands.
Q4: four different approaches weighed.
Q5: each change undone alone; nothing asked of Sam before the test list passes.
Q6: sources named; reading of each line marked unchecked.
Q7: sized to zero repeats and zero misses, not a word patch.
Q8: permanent, reviewed at the film's end.

## Lost / Added
Lost: the six-lines-above net, except where the question points back. Added: a full block log, a labelled test
list, short corrections instead of repeats.

## Unchecked
My labels of the 39 lines; what tripped the "Report" and effects stops; re-send cost; why guard-holes did not land.
