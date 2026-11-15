# Helper B: late faults

## Leak
Some. The facts lean towards one answer: chat 29's hand-made "span check" and the open question of whether a span clip runs clipcheck. I weighed that as one option among several.

## Results
- 8 critique, rework, re-render or code-finding chats cost 16.0% of a week out of 53.6% (protest-tiers-costs.md).
- Chain 3: the quick pre-flight in chat 28 found 107 faults (67 teleports) in work built in chats 25-26. Chats 29 and 30 (2.24 + 2.36%) fixed them (handovers, lines 306-318). Chat 26 had reported "Checks on T2/T3: clean". Which checks it ran: unchecked.
- The quick pre-flight runs clipcheck and audit (preflight.py ~417-419, 458). It takes seconds per shot (chat 29: "5 s a tier"). A span clip runs only the picture checks, not clipcheck or audit (film_engine.py 282-288). That is checked.
- Chain 2: 44 faults, mostly lists the film had never declared. JOKE_PROPS was one of them. Without it, rule 18's readability check (viewchecks.py 370) can only report "no JOKE_PROPS". So the mechanical part of chain 1's phone-size faults (15 of 21) had no check that could run while building.
- Chain 5: the documented hyphen name broke the quick pre-flight until chat 28, which found the underscore form (line 306). Two kittests were failing on the main line (line 228).
- Chain 4: 8 black frames reached Sam (note 1, line 333).
- Gap: nobody has measured how many gate faults were already present, and machine-findable, at the end of the chat that built them.

## The real decision
The question is not "which check runs earlier". It is "what does a building chat have to show before it may hand over", looked at across every chat in the film. Two levers are bigger than any single check:
- the building chat's exit condition;
- whether the film declares the lists the checks need early enough for those checks to run at all.

## Root cause
All the checks that caught chains 2 and 3 already existed. They were placed at the round's gate (rules 59, 67, 89). A building chat's "done" is "built + clips sent", and nothing machine-checks that. `handover.py end` is mandatory, but it runs no check on the film itself (handover.py 392-415). Three things made it worse:
- Missing declarations made checks COULD NOT TEST or silent.
- A broken tool (the name mismatch) stopped even a willing chat from running the quick check.
- A worked-round fault (the throwing arm) came back because nothing rechecked it in later chats.

## Approaches weighed
1. **Build-chat exit gate (reframe).** `handover.py end` runs the quick pre-flight whenever the chat changed the film's code. Each fault must be fixed, or written in Exceptions with a reason, before the handover.
2. **Declare first.** The plan stage writes every list pre-flight needs. At plan end, any COULD NOT TEST counts as a fault, so the checks can bite from the first build chat.
3. **Checks inside rehearsal clips.** The span clip also runs clipcheck and audit on its span. This only covers the spans that get clipped.
4. **Learn first.** Check out the code as it stood at the end of each Protest Tiers build chat (branches c13, c21-c26) and run today's quick pre-flight on each. This counts which gate faults were already there and machine-findable, and times the check. Repeat for the last two Blessed build chats.
5. **Fewer, longer chats** (build + fix in one). This goes against the cost watch and the history-cost finding (cost-diagnosis.md), so it was rejected.

Chosen: 4 first, then 1, then 2, each only if 4's numbers support it.

## Proposal
**Learn (changes nothing).** One Opus medium chat replays the quick pre-flight at about 8 build-chat commits. Output: a table with one row per gate fault, showing whether it was present and machine-findable at the end of its build chat, the run time, and which tool faults blocked it. Cost: about 1.5% of a week, one time only. Numbers: Protest Tiers 33 chats / 53.6%, Blessed about 22 (ledgers).

**Change 1, only if the replay shows 50% or more of gate faults findable at build end.**
- `handover.py end --film NAME` maps the film name to its code module (fixing the hyphen/underscore fault for every tool).
- If the film's code changed in this chat, it runs the quick pre-flight and lists every fault as a handover fault.
- How it is enforced: the handover check is already mandatory, and the next chat's `start` reports any skipped `end`.
- Number to beat: new clipcheck/audit faults at the round's gate (Protest Tiers 107 and 44) should be 0, apart from faults named in Exceptions. Fix-only chats per film should fall below 8 (16.0%). Both are read from the gate printout and the ledger at the end-of-film review.
- Cost: about 1% to build. Per film, seconds per build chat, plus fixes made while the code is fresh (cheaper than a fresh chat's start-up, which is about 49% history, cost-diagnosis.md).

**Change 2, separate, only if the replay shows COULD NOT TEST hid faults.** The plan stage's hand-over fails while pre-flight lists any undeclared list. Number to beat: 0 "declare" faults at the first gate (Protest Tiers 44). Cost: about 0.5%.

Sam would notice fewer rework rounds, animatics that arrive sooner, and fewer notes like "frames missing".

## Sam test
- Q1: Yes. Gating at the point of creation, enforced by a hook rather than by memory, is what an agent-workflow expert would do.
- Q2: The evidence spans the build chats of two films, not one chain.
- Q3: Enforced by the mandatory handover check. Naming a fault instead of fixing it is visible, because the named count is reviewed.
- Q4: Five different approaches weighed. This one acts on the exit condition, the lever that sets the chat count.
- Q5: Each change can be undone alone. Nothing is asked of Sam before the replay shows it works on real commits.
- Q6: Every source is named. Gaps are listed below.
- Q7: Sized to reach 0 gate faults, not a cheap reminder line.
- Q8: These are permanent changes. The replay is a measurement, not a trial. Each change is reviewed at film end.

## Lost / Added
- Lost: building chats can no longer hand over with known clipcheck/audit faults left silent.
- Added: one learn chat (about 1.5%), a name mapper, a check run at handover, and a declaration step at plan.

## Unchecked
- Which checks chat 26 ran.
- The quick pre-flight's run time on a whole film.
- Whether old commits still run under today's tools.
- Blessed's causes.
- Whether the figure guard's stops (chain 4) show up in the quick pre-flight.
