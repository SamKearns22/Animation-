# Helper A: precheck-reply

## Leak
The file name ("precheck-reply") and the fact "reply_faults ... only hook() calls it" point at one answer (check the
draft before sending). Weighed below as one approach among several, not assumed.

## Results
- 43 replies logged as "sent after one block", 15-22 Nov (notes/proposals/unrouted.md, counted). First-time blocks
  fixed on resend are not logged, so the true number of doubles Sam saw is higher (gap; unchecked).
- My reading of the 43 logged lines (cut at 120 characters, so labels are rough): 12 a judged proposal missing the exact
  "Critiqued:" line; 9 a question about starting the route ("should I start the suggest-and-judge process"); 10 a film
  or meaning question (props stage, "Report" recording, shot 4 camera, Hook Text options); 3 a misread name
  ("notes/proposals/2.md"); 9 real unjudged system asks. About half the blocks were wrong.
- Two other Stop hooks also block after Sam has read the reply: watcher.py (a "Broken:" line, and a once-a-day "Watcher:
  N systems checked" line, both demanded "at the top of your reply") and ledger.py (alarms, paused:
  ALARMS_PAUSED = True). Source: source/watcher.py ~500, source/ledger.py ~322. Their doubles are logged nowhere.
- The same problem was already judged and adopted: notes/proposals/guard-film-questions.md, Sam picked Option 1 at
  23:01 on 22 Nov (git 10437bef): a stopped reply gets only a one-line correction; log every block; retune on labelled
  real replies. Not built: propose.py's last change is d54ffbba, and its block text still says "Put it through the
  route first ... or reword the question". This chat's two blocks (23:17, 23:19) came after the adoption.
- brow-limit was logged twice a minute apart (22:40, 22:41); the status chat reported Sam seeing one reply three times
  (guard-film-questions Facts).

## The real decision
Not "should one chat check its draft", but: across every chat of a film, how many times does Sam read a message he
has already read, from any hook, and how to get that to zero full repeats. Bigger levers than a precheck: building the
fix Sam already adopted, the wording of every Stop-hook block, and the guard's wrong stops.

## Root cause
1. A Stop hook runs after the reply is on Sam's screen; Claude Code has no hook that reads a reply before Sam does
   (unchecked against current Claude Code docs). So every block is a second message by construction.
2. The block texts (propose.py and watcher.py) never say Sam has read it, so chats resend whole replies. Sam's 22 Nov
   CLAUDE.md line asks otherwise, but relies on the chat recalling it while the hook text says the opposite.
3. The guard is a word list. guard-holes (15 Nov) widened it ("process", "rule"), which now stops questions about
   starting the route itself and about what Sam meant.
4. The adopted fix was not built, so the problem returned the same night.

## Approaches weighed
1. Precheck: the chat runs the guard on its draft before replying. Cuts doubles only when the chat chooses to run it.
2. Reframe: build the adopted guard-film-questions plan and apply its one-line rule to every Stop hook. Caps each
   block at one extra line, whatever its cause.
3. Learn-first: log every block from all three hooks, label them, then decide if a precheck is still needed.
4. Remove the guard and rely on the end-of-film review. Loses the catches of 9 real unjudged asks.
Chosen: 2 with 3 first, and 1 only if the measured result calls for it.

## Proposal
Learn (changes nothing; already adopted, about 0.4% of a week): every block from propose.py and watcher.py is logged,
first-time ones included, with hook, whole reply and resend length; the 43 lines and new ones are labelled from the chat
records. It also checks whether the log counts replies fixed on resend: the hook reads all text since Sam's last
message, so the blocked first copy may still be in what it checks (likely from the 23:17 line; unchecked).

Change 1 (already adopted; build it, about 0.2%): the guard's block text says "Sam has already read this reply; send
only the missing line, or 'ignore my last question, it is withdrawn'." A kit test checks the text. To beat: full
repeated replies from the guard per film, from at least 5 (Milburn) to 0, counted in the Learn log.

Change 2 (new, its own yes, about 0.1%): the watcher's block text says the same, and its daily "Watcher" line goes in
the next reply instead of forcing a resend. To beat: watcher-caused repeats to 0 (now not counted at all).

Change 3 (already adopted, after Learn, about 0.6%): retune the guard on the labelled list. To beat: 0 wrong stops on
the list, 0 real asks missed.

Change 4 (only if, after Changes 1-3, the log still shows more than one block per film; its own route run): the
draft precheck, with the Stop hook logging whether it ran.

Cost: about 1.3% of a week once, against 15% per film; nothing per chat. Sam would notice: no repeated replies; at most
a one-line correction.

## Sam test
Q1: Yes: fix the hook text everywhere and measure before adding steps.
Q2: Scope is all hooks and all chats, from the whole log and chat records, not one chat.
Q3: Enforced by the hook's own text and kit tests, not by a chat remembering; the log shows if it worked.
Q4: Four different approaches weighed; the precheck waits for evidence it is needed.
Q5: Each change is one wording or rule edit, undone alone; nothing new to trust untested.
Q6: Counts sourced; labels are my rough reading, marked so; gaps named.
Q7: Sized by the result (zero repeats), not price; no cheap version that leaves the watcher's doubles.
Q8: Permanent changes, reviewed at film end against the block log.

## Lost / Added
Lost: the watcher's daily line no longer arrives in the same reply as it fires (next reply instead).
Added: a log of every block from every hook; one-line corrections instead of repeated messages.

## Unchecked
Whether Claude Code offers any hook before a reply shows; my labels for the 43 lines; whether the guard counts the
blocked first copy on resend; how many first-time blocks occurred.
