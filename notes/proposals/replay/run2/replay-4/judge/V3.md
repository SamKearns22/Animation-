# Helper A: which rules and tools work

## Leak
None. The problem file states no solution (its page.py fact is evidence, not a remedy).

## Results
- Cost: no recent film came near 15% of a week. Remakes spent 35.96% (estimate 14.5), Blessed 62.21% (estimate 19), Protest Tiers 51.27% so far over 32 chats (first estimate 21.5, now 63.51) (notes/ledger/remakes.md, blessed.md, protest-tiers.md; notes/protest-tiers.md line 158).
- The record cannot say what helped. All three ledgers show "0 rounds, 0 notes, 0 repeated" for every chat, although Protest Tiers had round 1 notes and a repeated note ("frames missing", rule 30; notes/protest-tiers.md line 5). The notes and repeats are filled only when a chat runs `ledger.py log --notes` by hand (source/ledger.py lines 9, 40, 173); the Stop hook writes 0. The ledger's model column is also wrong (chats 27, 30 and 31, titled Opus, are logged "sonnet").
- Tools ignored: page.py, required by the notes-round pack, ran 0 times in chats 29 and 31; code was searched by hand 25 and 26 times (replay-record/tool-use-29-31.md). Looking at code was about 27-35% of each chat's calls and cost (bills-29-31.md, estimated).
- What acts on its own: only the setup, cost watch, handover log and ledger hooks (.claude/settings.json). Everything else depends on a chat choosing to run it. The cost watch fed on figures 20-75% too low and never stopped a chat (problem file; Sam, 19:36).
- Rule writing: Claude found 8 faults in its own "pillar" rule only after Sam asked (problem file; Sam, 19:59).
- Counts: the rulebook has 54 numbered rows plus the P rules; the catalogue table has 124 rows (grep). The problem file's 64 and 115 are not confirmed.

## The real decision
The question is not "audit 180 rules and tools". It is: **how does every film record, without any chat choosing to, which rule or tool ran, what it caught, and what reached Sam?** Without that record no rule can be judged, kept or dropped. CLAUDE.md already requires such a record ("remove a step only if it caught nothing in three films"), and it does not exist. Two levers are bigger than the one named: the 2.4-3.4x cost overrun, and turning text rules into steps that run on their own.

## Root cause
Rules and tools are written as text and judged when they are written, never by results. Three things show it.
1. Running them is optional. page.py was in the pack and was not run, and the ledger's notes column has a manual command that no chat ran.
2. They measure themselves badly. The cost watch trusted self-reported figures, and the notes column defaults to 0.
3. Nobody looks back. No step takes a note from Sam back to the rule or check that should have caught it.
Earlier fixes failed for the same reason: each added more text for a chat to read and choose to follow.

## Approaches weighed
1. **Critique sweep:** a fresh critic reviews every rule and tool. Rejected. It judges paper, not results, and it is the same kind of lazy review that produced the 8-fault rule.
2. **Learn first, from the record:** read-only helpers go through the transcripts and notes of Remakes, Blessed and Protest Tiers. Every note from Sam is traced to the rule or check that should have caught it (it ran and missed, it never ran, or no rule covers it), and every tool's real use and cost is counted.
3. **Reframe, the film measures itself:** the Stop hook fills each chat's row from its own transcript (notes from Sam, repeats, tools run versus hand searches, checks run), so every film becomes evidence automatically.
4. **Reframe, enforce instead of instruct:** the few rules the evidence shows matter become hooks that block or redirect (for example, a hand search of film code is sent to page.py).

Chosen: 2, then 3, then 4, as separate steps.

## Proposal
**Learn (changes nothing).** Sonnet helpers read the 3 films' chat records and notes. They produce one table: each of Sam's notes, the rule or check that should have caught it, and whether that rule or check ran, missed, or did not exist. A second table gives each tool's runs and cost per film. Sam gets the top 5 causes of notes and cost in plain English. Cost: about 3-5% of a week (unchecked: 75 chats to read), filed as tool work and not charged to a film.

**Change 1: the ledger fills its own row.** `ledger.py auto` reads each chat's transcript and records Sam's notes, repeated notes, checks run and tools run versus hand searches. Enforced by the Stop hook that already runs. Number to beat: the notes columns now read 0 for all 75 chats, and after the change they must match the film's notes file in every chat of the next film. About 1-2% of a week.

**Changes 2 onward, one per yes.** Each targets the top cause from the learning table. Each is enforced by a hook or a pre-flight refusal, not by text. Each carries its own number (for example, hand searches per notes chat, now 25-26, must fall to near 0). Rules that the table shows caught nothing over three films are offered to Sam for removal, each on its own "Lost:" line. Each change is reviewed when Sam declares the film complete.

**What Sam would notice:** a plain list of what causes his notes and costs. After that, fewer repeated notes and cheaper notes chats, shown in the ledger and not just claimed.

## Sam test
- Q1: An expert measures outcomes before pruning or adding, and enforces with code, not text. That is what this does.
- Q2: It uses three whole films, all their chats and all of Sam's notes, not one chat or the cheapest and dearest.
- Q3: The learning step finds the root cause. Change 1 runs on its own through the hook. Each later change has a number it must beat.
- Q4: Four different approaches were weighed (sweep, learn, self-measure, enforce).
- Q5: The learning step changes nothing. Each change can be undone alone. Sam says yes only to things shown by evidence.
- Q6: Sources are named above. Gaps are marked unchecked.
- Q7: It is sized by the result: three films, not one, and a permanent hook, not a one-off count. Its cost is stated.
- Q8: No trials. Change 1 is permanent, and each later change is reviewed when the film is complete.

## Lost / Added
- Added: one learning pass (about 3-5%), and per-chat outcome columns filled by the existing hook.
- Lost: nothing now. Later removals each get their own "Lost:" line.

## Unchecked
- Rule and tool totals (54 numbered rows plus the P rules; 124 catalogue rows).
- The learning step's cost.
- Whether every chat record from the older films can still be read.
- Why the ledger's "After the film" figures (33.55, 51.54, 80.02) differ from its headline spend.
