## Leak
The title and facts point to three remedies already chosen: make chats use the finder, add a "tool map" page, and use the app's figure. They are weighed below as options, not taken as given.

## Results
- Milburn: 15 chats, 1,259 steps, recorded 32.14% (all rows "estimate"); Sam read 22% from the app (problem file; ledger notes/ledger/milburn.json, milburn.md).
- **The money is in history, not searching.** "Other" is 21.4 of 32.14 points (67%), and 58-87% of every chat. History at the end is 91k-299k (milburn.json). Search output is re-read on every later step, so its true cost sits partly inside "other". The ledger does not measure how much.
- **The "531 tool-definition loads" are a misreading.** In source/stepcost.py `kind_of` (lines 64-97), "tool search" means any grep or partial read of a file that is not the film's code. The 531 split as: shared tools 328, other 101, film notes 81, guides 21 (summed from milburn.json). Loading tool definitions (ToolSearch) is counted as "other". No fact in the record supports "hundreds of definition loads".
- **Most of the cost came before any note round.** The ledger stages say sets, props, build and board had used 29.43% by the end, against 3.4% planned (8.7 times over). Moves, fx and the rounds had not started. The ledger's own forecast said "lands at 100.4%" (milburn.md), and no chat acted on it.
- The finder answers notes. 74 hand searches were in chats with no show call. 43 were "misses" (a hand search within 10 calls after a show), so the finder's answer fell short even when it was used. The show log has 13 calls, and 6 have no match score (notes/logs/milburn-show.log).
- **Gap: the ledger cannot tell build from notes.** Every row says stage "auto", notes 0. Yet the show log holds Sam's notes (e.g. "goth eyebrow…", "Andy arm table"). So "hand search in a note round vs a build" cannot be answered from it.
- app-costs.tsv has no Milburn row. Its last entries are protest-tiers, 15 Nov.

## The real decision
How to keep a whole film under 15% while it is being made. The two biggest levers are the cost of building new things, which was 8.7 times its plan, and history re-read on every step (67%). Both depend on knowing the real figure during the film. Search habits are a small part of this.

## Root cause
1. No real figure arrives in time. The estimate came out 46% high (32.14 vs 22), and the forecast that did exist was advisory: nothing made a chat stop and re-plan.
2. The stage plan for building (3.4%) was not sized against what new sets, props and people actually cost.
3. The finder reminder (.claude/hooks/finderwarn.py) failed because it is aimed at note rounds. It says itself that "building something new may search on purpose", and most Milburn chats were building. When the finder was used, 43 misses show its answer was often incomplete.

## Approaches weighed
1. **Force the finder:** block hand searches of film code until `show` is run. This targets about 9% of the spend and gets in the way of build chats. Rejected as the first move.
2. **Reframe to history size:** limit how much each search or read adds to history (a hook that turns long outputs into filtered summaries), and extend the finder to shared tools (328 searches). Promising, but its size is unmeasured.
3. **Steer the film on the real figure:** every handover records this chat's real app cost, and the film's running total is set against its stage plan. If the forecast passes 15%, the next chat must re-plan before it builds. This works at the level of the whole film.
4. **Learn first:** fetch the real figures, label each chat's stage, and measure how much history comes from search output. This changes nothing.

Chosen: 4, then 3, then 2 only if 4 shows it pays.

## Proposal
**Learn (changes nothing, about 1.5% of a week):**
(a) Read the app's real cost for all 15 Milburn chats (their session ids are in milburn.json) and import it with `ledger.py app`. Work out how far off the estimate is.
(b) Label each chat build or notes from its transcript and the show log, then count hand searches per note in note chats only.
(c) For each chat, measure the share of history that is search or read output.

**Change 1 (alone, about 1% to build):** `handover.py end` refuses to hand over until this chat's own app figure is in app-costs.tsv. The chat reads it with get_session, which every chat can do. The handover line then shows "film so far X% of 15%; forecast Y%". When the forecast is over 15%, the next chat's start check makes it write a re-plan for the remaining stages, or put the choice to Sam. Number to beat: every row of the next film is "app", and its forecast is within 2 points of its final cost.

**Change 2 (only if (c) shows search output is at least 20% of history):** a hook that trims long search output to the matching lines, measured against history at the end of each chat.

**Change 3 (only if (b) shows note chats miss after `show`):** improve the finder's answer. A new reminder is not the fix. Number to beat: misses per show fall from 43/12.

Each change is reviewed against the next film's ledger when Sam declares that film complete.

What Sam would notice: each handover gives the film's real cost so far. When it heads past 15%, he hears about it before the money is spent, not after.

## Sam test
Q1 Expert: an expert measures where the tokens go (history) before policing one habit. That is done here.
Q2 Best result: the scope is the whole film and all 15 chats with real figures, plus Protest Tiers for comparison.
Q3 Comprehensive: Change 1 is enforced by a refusal in the handover check, not by a reminder. The reminder that failed is explained above.
Q4 Most intelligent: four different approaches were weighed. The frame was corrected (history and build cost, not searches).
Q5 Risk: learning changes nothing. Each change can be undone alone. Sam is asked to approve nothing unshown.
Q6 Checked: the sources are named, and gaps are listed below.
Q7 Not the cheap version: it targets the 67% and the 8.7-times overrun, not the cheapest fix that sounds right.
Q8 Nothing temporary: each change is made properly or not at all, and reviewed at the end of the film.

## Lost / Added
Lost: about 1.5% of a week to learn, and one extra step per handover (reading the app figure).
Added: the real cost during the film, a forced re-plan once the forecast passes 15%, and an end to search fixes made on a misread figure.

## Unchecked
- Whether Sam's 22% (71 to 93) covers only Milburn chats.
- Whether get_session still returns cost for finished chats.
- Whether the Milburn transcripts are still readable for (b) and (c).
- Why the cost job stopped after 15 Nov.
