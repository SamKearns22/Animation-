# Helper B: what to measure next

## Leak
None stated as a solution; the wording leans toward "read more chats" (it prices reading all 29). Ignored.

## Results
- Protest Tiers: 51.27% spent over 32 chats (not 29), forecast 56%, against the 15% aim (3.4x); its own estimate was 63.51% (4x the aim). Source: notes/ledger/protest-tiers.md.
- Where it overran, by stage (stage table, same file): moves 11.30 spent vs 3.07 planned; round-1 moves 14.04 vs 4.45; unplanned plan extras 10.08; cast 5.96 vs 2.09. **Moves stages = 25.3 of 51.3 (49%).**
- Chats 29 and 31 cost 2.57 + 2.36 = 4.9%, under a tenth of the film. Their bills (bills-29-31.md) are keyword counts, cost guessed, not metered; no category tops ~33%.
- 66 chats across three films already have metered usage in notes/ledger/app-costs.tsv. My fit over its 53 Opus rows (rough): ~50% of dollars is re-reading history, ~27% writing it, ~22% output; cost tracks final history size (correlation 0.87).
- Tool and rule work in other ledgers totals ~76% of a week (morning-report alone 28.05). Period unchecked.
- Gaps: every ledger shows 0 rounds, 0 notes, 0 repeated, so cost cannot be tied to Sam's notes. Problem file says Blessed ~80%, Remakes ~51%; their rows sum to 62.21 and 35.96 (the 80.02/51.54 in protest-tiers' "After the film" line, which also gives Protest Tiers 33.55%, do not reconcile). Chats 27, 30, 31 are titled Opus but logged "sonnet". `source/costbreak.py` already meters a chat's cost by kind of step but was not used for the bills.

## The real decision
Not "which chats to read next" but: where did the whole film's 51% go, by stage and by mechanism, so one change can target the biggest share and be judged on the next film. Bigger levers: moves stages (49%), chat length, chat count (32), the estimate itself (4x the aim), tool work outside films.

## Root cause
Cost is recorded per chat, never per cause: no metered breakdown is stored and notes/rounds columns are empty, so audits fall back to hand-sampling a chat or two. The two bills were picked for convenience, both from one late stage, and were not metered.

## Approaches weighed
1. **Read more chats** (as framed): per-step detail, but costly and hand-guessed.
2. **Reframe to the whole film from data in hand:** stage overruns, chats per stage, and the history/output split from app-costs.tsv for all 66 chats., near-free; says where, not which steps.
3. **Reframe to the whole week:** film vs tool/rule work.
4. **Learn-first, permanent metering:** `ledger.py auto` (the Stop hook) runs costbreak on each chat's own transcript and files the breakdown, plus notes and rounds, so no one reads transcripts again.
Chosen: 2 + 3 + a small metered sample from 1 now (learning); 4 offered as its own change after.

## Proposal
**Learn first (changes nothing).** One Opus-medium chat builds one table, "where Protest Tiers' 51% went": per stage, planned vs spent, chats, and the history/writing/output split; the same for Blessed and Remakes; film vs tool work per week; reconcile the ledger figures above. Then meter six Protest Tiers chats, chosen for the biggest stages, not convenience: the two dearest moves chats, the dearest round-1 moves chat, one planning-extras chat, one cast chat, one Sonnet animatic chat, using costbreak's method where transcripts are reachable. Output: the top three causes, each as % of film spend. Cost ~2% of a week (data ~0.5, six chats ~1.2-1.5, unchecked per-chat rate), against 3-4% for all 29.
**Change 1, its own yes:** permanent metering in the Stop hook (approach 4), enforced by the hook, not by a chat choosing. Number to beat: 100% of the next film's chats carry a breakdown and notes count (today 0%).
**Change 2, its own yes, only after the table:** one change aimed at the top cause found. Number to beat: that cause's % of film spend and the film total vs Protest Tiers' 1.6% per chat, judged when Sam declares the next film complete.
Sam would notice: one plain table, then one yes at a time.

## Sam test
Q1 Expert: meters the whole system before tuning a step.
Q2 Best result: whole film plus three films plus tool work; sample picked by spend.
Q3 Comprehensive: change 1 runs in every chat by hook; success is a number.
Q4 Intelligent: four different approaches weighed.
Q5 Risk: learning changes nothing; each change undone alone.
Q6 Checked: sources named; estimates marked.
Q7 Not cheap: whole-film data plus metering.
Q8 Nothing temporary: the table is a measurement; metering is permanent, reviewed at film end.

## Lost / Added
Lost: nothing. Added: one learning chat (~2%); later, metering in the Stop hook.

## Unchecked
Per-chat reading cost; my price-split fit; whether other chats' transcripts give per-step usage; the period of the tool-work ledgers.
