# Helper A: late faults

## Leak
No solution is stated. The framing leans toward moving checks earlier; I tested that rather than assuming it. One fact is wrong (below).

## Results
- Fix-only chats cost 16.0% of 53.6%. Gate-or-tool-only chats (17, 18, 29, 30) cost about 8% (`notes/proposals/learn/protest-tiers-costs.md`).
- Faults found at the gates: hunt 1 found 21 (15 phone-size), hunt 2 found 16, the full pre-flight found 44 (mostly undeclared lists), and the quick check found 107 (67 teleports; 16 not broken down by kind, unchecked). One reached Sam: "frames missing" (`notes/archive/protest-tiers-handovers.md`).
- **Correction:** a span clip runs no checks. `source/film_engine.py` 196-215: `lock = not span`, and `check` stays False.
- The quick check (`--text`) already runs clipcheck, audit and viewchecks in seconds (`source/preflight.py` 400-460). It could not run until chat 28 (a name mismatch).
- The phone-size check (`viewchecks.readability_faults`) needs JOKE_PROPS, which was declared in chat 17, after both hunts.
- No hook runs kittests, and `handover.py` runs no film checks (`.claude/settings.json`).
- Gap: chats 9-32 are unreadable, but branches `claude/protest-tiers-c13` to `c31` hold each chat's code, so the checks can be replayed.

## The real decision
Across the whole film: how many handovers separate making a fault from finding it? The levers are bigger than one check: every gate sits at stage end (rules 59, 67, 89), checks lack their inputs until late, and shared tools are untested.

## Root cause
No build chat ever runs a machine check. Its stills and span clips check nothing, its lists were undeclared, and the gates fire only after the stage. Earlier fixes were text a chat could skip: rule 24's "phone size" measured nothing, and chats 14 and 15's lessons were never written. Chain 4's workaround was sized to one build, with no test across the pose range. Nothing tests the shared tools, so films run them first.

## Approaches weighed
1. **Reframe:** the build chat closes its own faults. `handover.py end` runs the quick check and refuses on unnamed faults.
2. **Critique each step:** costs 3% a film; worth it only if most faults are eye-only.
3. **Learn first:** replay the checks on each build branch and attribute every fault.
4. **Tools tested first:** run kittests when a shared tool changes.
5. **Fewer, longer chats:** rejected, because long histories drive cost (49% is re-reading, `notes/cost-diagnosis.md`).

Chosen: 3, then 1, then 4, each gated on 3's numbers.

## Proposal
- **Learn (changes nothing, about 1%, Sonnet):** run main-line `preflight.py protest_tiers OUT --text` on c13, c15-17 and c21-26, and run kittests. The output is a table: each fault, the chat that made it, whether it was visible at that chat's end, and its kind. Change 1 proceeds only if at least 60% were visible.
- **Change 1 (Opus medium, about 1.5%):** `handover.py end` runs the quick check whenever the code hash has changed. It refuses on unnamed faults, and an undeclared list is a fault. At red budget the handover goes through with the faults put first. Counts go to the ledger. **Beat:** at most 10 faults first found by a non-building chat (was 107 and 44), and zero gate-only chats (was 4).
- **Change 2 (about 0.75%, only if the replay supports it):** `handover.py end` runs kittests when tools changed. **Beat:** zero film chats on shared-tool faults (was chat 18 and parts of others).
- **Eye-only faults** wait for the replay's numbers.
- **Cost:** about 3% once, filed as tool work. The saving is unchecked (an estimated 4-8% a film).
- **What Sam notices:** fewer chats before each animatic, and fewer notes like "frames missing".

## Sam test
- **Q1:** Yes. Stop faults where they are made, enforced by a tool.
- **Q2:** Learn-first widens the evidence; Blessed is unchecked.
- **Q3:** Enforced by refusal; named faults are counted.
- **Q4:** Five approaches were weighed.
- **Q5:** False positives (chat 18's note (a)) could breed waivers; they are counted. Each change is one flag, undone alone.
- **Q6:** Sources are named, gaps marked.
- **Q7:** Sized to the 8%, not to its price.
- **Q8:** Each change is permanent once made, and reviewed at the film's end.

## Lost / Added
Added: about 1 minute of checks per build handover, and some fixing before handing over. Lost: handing over with unseen faults (except at red). Nothing in the films changes.

## Unchecked
- The breakdown of 16 of the 107 faults.
- Whether old branches run under main-line tools.
- kittests' run time.
- The saving per film.
- Blessed's causes.
