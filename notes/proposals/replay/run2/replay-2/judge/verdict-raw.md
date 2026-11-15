## Leak
yes: a hint, not a solution. The wording ("which chats, how many") and the priced cost of reading all 29 chats steer toward sampling more single-chat step bills; it does not name what to measure.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 4 | 3 | 4 | 4 | 5 | 20 |
| V3 | 2 | 2 | 2 | 2 | 4 | 12 |
## Sam test
Q1: Yes. An expert meters the whole system (all chats, by stage and by mechanism: fixed start-up load, work, rework) from real usage before tuning any step; that is what the pick does.
Q2: Yes. Whole film plus the two earlier films, from the app's metered figures for 66 chats (checked: 29 + 18 + 19 in app-costs.tsv), on one price base; the few chats read in full are chosen by where the overrun is, not by convenience.
Q3: Mostly. Root cause is evidenced (cost is filed per chat, never per cause; notes column is 0 everywhere; the bills were keyword guesses). Success is a number. The permanent metering runs in the Stop hook, so no chat chooses it. Weak spot named: Sam's notes per stage cannot be counted fully automatically (F3).
Q4: Yes. Four approaches weighed (more bills, whole-film table, whole-week split, permanent metering); V2's start-up autopsy added as a fifth angle.
Q5: The learning step changes nothing. Each later change is its own yes and can be undone alone.
Q6: Stage figures, chat counts, dollars, the 90k FRESH and the $245 PROVISIONAL week were checked against the ledger, app-costs.tsv and costwatch.py; the price-split fit, per-chat reading cost and transcript reach are marked unchecked.
Q7: Sized by the question (where a whole film's 51% went), not by price; the cheap trap (two more step bills) is rejected. Honest cost about 2% of a week.
Q8: The table becomes a permanent ledger page; metering is permanent; each change is reviewed when Sam declares the next film complete. No trials.
## Pick
V1
## Why
V1 and V2 both reframe correctly from "which chats to read" to "where the whole film's cost went, by stage and mechanism, on one price base", and both rest on checked figures (moves 11.30 vs 3.07 planned, round-1 moves 14.04 vs 4.45, plan extras 10.08; moves stages 25.3 of 51.3). V1 wins because it also fixes the root cause for good: per-cause metering filed automatically for every chat, so this question never needs hand-sampling again, offered as its own yes. V2 has two small fact slips (Blessed has 18 metered chats, not 24; the three overrun stages are 35 points, i.e. 69%, of the 51%, not "35% of the 51%"). From V2 I took: the start-up autopsy (what fills the 90-100k every chat starts with, checked: idle chats sit at 80-101k history); tagging each rebuild in the dear moves chats by cause (missed check, unclear brief, Sam's note), which ties cost to notes; and the plain three-bar summary for Sam. V3 measures two chats again, proposes a code-finding fix before the learning, and calls the saving small: it answers the problem's wording, not the decision.
## Faults in the pick
- F1 [fixed] The ledger rows carry chat titles, not stages, so "chats per stage" needs a mapping: the table maps each chat to a stage by its title and date and lists that mapping.
- F2 [named] Whether costbreak can read other chats' transcripts (via the earlier-chat record) is unchecked; if it cannot, those chats get the history/output split only, said on the table.
- F3 [named] Sam's notes per stage are counted by the hook only where a round is opened; free-form notes still need the chat to tag them.
- F4 [fixed] V1's 76% "tool work" figure has an unchecked period: the table states the dates it covers before it is used.
- F5 [named] The price-split fit and the $245 week are provisional (costwatch says +-20%); the shares are shown as ranges.
## Final version
**Learn first (changes nothing), one Opus-medium chat, about 2% of a week.**
1. One table, "where Protest Tiers' 51% went", on today's price base: per stage (chats mapped by title and date), planned vs spent, number of chats, and the split into fixed start-up load (chats x start-up size), re-reading, writing and output, from app-costs.tsv. The same for Blessed and Remakes. Film vs tool work, with the dates covered. Reconcile the stale 80/51/33.55 figures.
2. Start-up autopsy: list what fills one fresh chat's first 90-100k (rules, tool lists, CLAUDE.md, hook output, handover reads) and each item's size.
3. Meter six chats chosen by overrun: the two dearest moves chats, the dearest round-1 moves chat, one plan-extras chat, one cast chat, one Sonnet animatic chat, with costbreak where transcripts are reachable. Tag each rebuild by cause: missed check, unclear brief, Sam's note.
Output: one ledger page plus a three-bar picture (start-up, work, rework) and the top three causes, each as % of film spend.
**Change 1, its own yes:** the Stop hook files costbreak's per-cause breakdown, model and round notes for every chat. Number to beat: 100% of the next film's chats carry it (today 0%).
**Change 2, its own yes, only after the table:** one change aimed at the top cause. Number to beat: that cause's share and the film total on the same base, judged when Sam declares the next film complete.
## For Sam
### Option 1: Find where the whole film's money went, then meter every chat
One chat adds up what every chat of the last three films really cost (the app's own figures), stage by stage, and splits it three ways: the reading every chat does just to start, the work itself, and redoing work. It reads six of the dearest chats in full to see why the movement stages cost three times their plan. You get one page and a three-bar picture, then a separate Y/N to make every future chat record this by itself, then one fix aimed at the biggest cost.
Lost: nothing in the films; about 2% of a week for the measuring chat.
Added: a cost page per film, then automatic cost records in every chat.
### Option 2: Same page, plus a look at the start-up load, no automatic records
The same whole-film page and the same start-up check, but only two chats read in full, and the automatic per-chat records are left out. Cheaper (about 1.2% of a week), but next time the question comes up it has to be worked out by hand again.
Lost: automatic cost records for future films.
Added: a cost page per film and a list of what every chat loads at start.
