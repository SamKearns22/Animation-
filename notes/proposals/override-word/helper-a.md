# Helper A: the word Override

## Leak
The title and notes give a design (skip everything, log it, a Checks line, locked shots untouched). Ignored.

## Results
- Chat 47 could not send animatic v5. Two different guards refused (notes/grand-theft-autism.md "Chat 47"):
  1. **The send guard** found no body check and no critique (humancheck.py send_faults). Chat 47 had not run them (shot 4's full-size look and the cuts "NOT done"). This guard was right.
  2. **finish.py** (lines 209-213) refuses every animatic while any chat has an unsettled let-through. Since 23 Nov there are 4, all from two other chats, none from this film (notes/proposals/unrouted.md). Unrelated to the film; it also stopped the Hook Text and sign-off.
- Of the 3 let-throughs settled since 23 Nov, 2 were "false block" (unrouted.md).
- Sam's word reaches only the cost watch, and only when his message starts with "override" (costwatch.py line 163). handover.py lines 291-294 catches a chat that claims an override Sam never typed.
- Film at 93.83% of its 15% (notes' cost line).
- "Locked by Sam" is a prose rule only (CLAUDE.md line 20). No code reads it.
- Gap: no record of guard refusals across films (a finding).

## The real decision
Once Sam says go, which stops may still hold a film back, and how does his word reach all of them without a chat being able to fake it? There is a bigger lever: finish.py blocks every film over other chats' paperwork.

## Root cause
Each guard has its own way out; none is "Sam said so". Sam's typed words reach only the hooks that see his messages. finish.py's lock covers every chat, so one film's guard trips on another chat's backlog. The earlier "settle" fix failed: a chat cannot honestly settle another chat's entries.

## Approaches weighed
1. **One trusted record of Sam's word, honoured by every guard.** Each skipped check is named to him.
2. **Reframe: fix wrong blocks.** Scope finish.py's lock to the film's own chats. No word needed.
3. **Learn first:** log every refusal for one film, then decide which guards should hear Sam.
4. **"Send now, check after":** two sends, more notes.

Choice: 1 (Sam asked plainly); its record doubles as 3's log; 2 follows separately.

## Proposal
**Change 1 (one yes): Override.**
1. The message hook records Sam's message when it contains the whole word "override", anywhere in the message. The record lasts for that one ask and ends at his next message.
2. One shared check serves the send guard, finish.py, the proposal Stop hook, the handover check, the cost watch and the budget stop. It confirms the word in Sam's own message in the chat record, so a record a chat writes for itself fails.
3. Each guard it passes prints "Checks: not run (your Override): ...". The existing rule (never send what a check flagged without saying so) makes the message carry that line. The skipped checks run as normal on the next ask.
4. Override never deletes work, never moves a locked shot, and never skips saving. Handover faults are still written into the notes.
5. CLAUDE.md line 87 and rule 85 are reworded to match.

Proof check (saved example): chat 47's video passes with Sam's word and is refused without it. A record written by a chat is refused.
Number to beat: no Override from Sam refused by a guard, and none invented by a chat. The handover check counts both.

**Change 2 (separate yes):** "Locked by Sam" stays in the notes' handover, never in a message to Sam. The plain-words check flags the phrase in a reply. Number: zero.

**Later, its own proposal:** scope finish.py's lock to the film's own chats.

Cost: one Opus chat, about 1% of a week (unchecked), once for all films.
Sam would notice: "Override" gets the film in that reply, naming what wasn't checked.

## Sam test
- Q1: Yes; one trusted input across all guards.
- Q2: Every guard; the wrong-scope lock named as the bigger lever.
- Q3: Enforced by hooks and counted at handover. Faking is checked.
- Q4: Four approaches weighed.
- Q5: More unchecked faults may reach Sam, each named; undone by one rewording.
- Q6: Sources named; gaps marked unchecked.
- Q7: Built fully, with its proof check.
- Q8: Permanent; reviewed at film end.

## Lost / Added
Lost: when Sam says Override, the promise that what he sees has passed its checks (each gap is named).
Lost: "Locked by Sam" in his messages.
Added: one record, one shared check, one message line, one proof check.

## Unchecked
- Whether Sam typed "override" in chat 47.
- What chat 47's wait cost.
- The cost of the build.
- An earlier reply that showed "Locked by Sam", needed as change 2's saved example.
