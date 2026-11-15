# Proposal: stop half-effort fixes and tools that are built and then not used

Status: open (replay case 3)

## Problem
Sam (his messages are in the record): the first proposals he gets are sized to what is cheap, not to what gives the
best result, and better ones come only when he pushes. Tools built to cut cost were then not used. Saying "I should
have proposed that first" does not stop it happening again. Fixes to the project need to deliver huge results.
Decide what permanent change to how Claude works stops this, for good.

## Facts
- Chats 29 and 31 ran the code-finding tools (codemap.py, page.py) 0 times, and searched film code by hand (grep -n
  or sed -n) 25 and 26 times (record: tool-use file).
- In this chat Claude first proposed a 2-chat measurement, then (after Sam asked) an 8-chat one; it also told Sam the
  tools "weren't used" before it had checked (the check later confirmed it).
- The rulebook is guides/film-quality-rules.md; CLAUDE.md holds the rules about working with Sam, including
  "Rules are permanent" and "Back-end proposals get a plain explanation".
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case3.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
CLAUDE.md
guides/film-quality-rules.md
guides/job-packs.md
guides/kit-catalogue.md
source/handover.py
.claude/settings.json

## Verdict (the judge, word for word)
<!-- verdict-hash: ade58f5c184361bd -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V2 (helper A). Critiqued: 5 found, 2 fixed, 3 named.

## Leak
yes: mild. "Decide what permanent change to how Claude works" frames the answer as a behaviour rule about Claude, and the facts list only tool counts and the 2-chat/8-chat story, which steers helpers toward "a rule plus a wider measurement". No concrete solution is given.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 2 | 4 | 12 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 5 | 4 | 3 | 4 | 4 | 20 |
## Sam test
Q1: Yes. An agent-workflow expert counts usage automatically, gets the tool ready for the live film, proves it finds the right lines, and only then puts it in the chat's path. That is the order here.
Q2: The count runs on every chat from now on, and the same counter is run back over all 32 Protest Tiers chats, so nothing rests on two chats. The page is scored on real notes from chats 29 and 31.
Q3: The root cause is named with evidence: the tools live in prose a chat may not be handed (chat 29 got the checks pack) or may ignore (chat 31), and nothing counts use. The counter and the handover refusal run in every chat by hook, not by reading. A chat can still get round it with an empty "reason" for skipping the tool. That is named (F3).
Q4: Five approaches were weighed across V2 and V3: a prose rule (already failed), a forcing hook, a counting loop, learning first, and a smaller film file. The pick takes the loop as the base and adds the hook only once the evidence earns it.
Q5: The learning steps change no film. Each later change is one hook or one check with its own yes, removed by deleting one entry. Sam is not asked to trust the page tool until it has hit the right lines in at least 8 of 10 real notes.
Q6: The counts, the never-built page, the failing page test, the 2,283-line file and the pack mismatch were all checked against the record. The cost shares are a helper's estimates. Build costs and the per-film saving are unchecked. The ledger disagrees with itself (51.27% vs 33.55%).
Q7: It is sized to catch every future unused tool and every under-sized proposal, not to patch page.py alone. Its honest cost is about 2-3% of a week once, unchecked.
Q8: The counter, the refusal and the proposal gate are permanent once Sam says yes. The replay is a measurement, not a trial. Each piece is reviewed against the film's results when Sam declares the film complete.
## Pick
V2
## Why
V1 answers the wording: a new prose rule, the same kind of fix that already failed in chat 31. It also gets a fact wrong (29 chats; the ledger shows 32), and it forces the code tools before anyone has checked they work on this film. V2 and V3 both find the real cause and the right order (count, prove, then enforce, one yes each). V2 wins on facts and cost. It found that the page tool was never made ready for Protest Tiers (no page, failing test), which V3 left unchecked. It found that chat 29 was handed a pack that names no code tool. And it builds the count into the hook that already runs after every action, so the count is permanent instead of a one-off 2-3% helper read. From V3 I took: the handover refusal when a stage's named tool shows 0 uses with no reason (V2 had no general enforcement); the 8-of-10 bar for the page tool, which measures accuracy rather than just fewer calls; and the ledger clash flag.
## Faults in the pick
- F1 [fixed] V2 judged the page tool on "fewer calls" alone; a tool can be cheaper and point to the wrong lines. The 8-of-10 bar was added (from V3).
- F2 [fixed] V2 counted use but nothing acted on a zero. The handover refusal was added (from V3).
- F3 [named] A chat can get past the refusal with a thin reason. The reason is printed on Sam's Checks line, so he sees it.
- F4 [named] The build costs, the cost shares and the per-film saving are estimates. Which ledger total is right is unresolved.
- F5 [named] The bigger levers (32 chats with long histories, a film file twice the split limit) are not fixed here. They wait for the counter's numbers.
## Final version
**Cause.** Built tools reach a chat only as text in a job pack, which the chat may not be handed (chat 29) or may not follow (chat 31). The tools are tested when they are built, never when they are used. The page tool was never run on Protest Tiers, and its test fails on the main line. Proposals are sized and judged by the chat that pays for them.

**Learn (changes no film):**
- L1. The after-every-action hook (costwatch) tallies each action: hand code look, page/codemap, check, render wait, edit, git. At Stop, ledger.py auto writes "code tools N / hand looks M" into the film's ledger row. Kittested. Then the same counter is run over all 32 Protest Tiers chats, giving tool use by stage. The run also settles the 51.27% vs 33.55% clash.
- L2. Fix the page test, build the Protest Tiers page, and replay 10 real notes from chats 29 and 31 through `page.py find`. Score whether it lands on the lines the chat actually edited, and what it costs against the 25-26 hand looks.

**Then one change per yes:**
- A. handover.py end refuses a handover while the stage's named tool shows 0 uses with no written reason. The reason goes on Sam's Checks line. It also refuses a Read pack that does not match the job (a fix job on the checks pack). Target: every row counted, 0 mismatches.
- B. Only if L2 scores at least 8 of 10: a before-the-action hook that answers a hand search of a film file with the page lines. Target: at most 3 hand looks per chat (from 25-26), notes-round chats under 2.4% of a week, read from L1.
- C. handover.py end flags any message to Sam that proposes a tool, rule or check without its proposal-route files (helpers, judge, Sam test). Target: Sam's "is this the best?" pushes go from 4 toward 0.

Splitting the film file and cutting history size wait for L1's numbers. Cost: about 2-3% of a week once (unchecked). Each piece is undone by removing one hook or check entry.
## For Sam
### Option 1: Count, prove, then wire in
From now on, every chat automatically counts which tools it used, and the count goes on the film's cost sheet. First I make the code-finding tool actually work on this film and test it on 10 of your real notes. It only goes into every chat if it finds the right lines at least 8 times out of 10. A chat that skips its stage's tool can't hand over without saying why, and you see the reason. No proposal of mine reaches you without first going through the fresh-judge test.
What you'd notice: cheaper notes rounds, and fewer "is this the best?" pushes.
Lost: a chat can no longer quietly skip its tool.
Added: a tool count on every film's cost sheet, a working page for this film, and later up to three checks, each asked separately.
### Option 2: Measure once, then decide
One helper reads all 32 of this film's chats and reports, for each stage, what was used. It also tests the code-finding tool on 10 real notes. Then I propose the fixes the results call for. It's cheaper to start, but nothing keeps counting after that read, so the next unused tool would again go unseen until you ask.
Lost: the permanent count on every chat.
Added: one full report on this film's tool use.
