# Helper A: start-up reading on grand-theft-autism

## Leak
None in the problem file (it states the cost and asks a question). The Record lists `chat.md`, the asking chat's own idea; I did not read it.

## Results
- The record says "start-up reading" cost 11.93% of a week, 22% of the film's 54.67%, across 28 chats (`source/dearest.py grand-theft-autism`). All 28 costs are transcript estimates, not the app's own figures (`notes/ledger/grand-theft-autism.md`, source column "est").
- The name is misleading. In `source/stepcost.py` split(), the "start-up floor" is everything in the chat at step 1, written once and then re-read at every later step. File reads made after step 1 are not counted in it. So the line measures **how big step 1 is, times how many steps the film takes**.
- Floor size: 80-82k tokens in every chat from 19 to 21 Nov, then 91k, 95k, 95k in the last three (ledger .json, split.floor_k). This chat also started at 95.9k (its own transcript). Across all films' ledgers, the jump appears late on 21 Nov and nowhere earlier. CLAUDE.md grew only from 12,388 to 15,301 characters, about 0.7k tokens (git history). So about 12k of the 13k jump came from outside the repository. That rise passed unseen: no check flags it.
- What fills the floor: the repository's part is CLAUDE.md (about 4k tokens), two agent files (972 characters) and hook printouts. The rest, about 75-90k, is the app's own instructions, tool descriptions and connector descriptions. Split: unchecked, because no chat records it.
- Steps: 2,775 in the film, 99 per chat on average, and 91% of them on Opus (2,514 Opus to 261 Sonnet; ledger .json). Check: 82k × 2,775 × $0.18 per million (Opus re-read price, `.claude/hooks/costwatch.py`) comes to about $41, roughly 11% of a week. That is nearly the whole line, so the cost comes from re-reading the floor at every step, not from the one write per chat. The 6-step chat a21d7f3d cost 0.08% of a week in all, so each new chat adds only about 0.1% (derived).
- Gaps: Sam's notes were not recorded for this film (0 notes, 0 rounds in the ledger), so no quality result can yet be set against cost. The record also does not show which connectors' tools film chats ever use.

## The real decision
This is not a reading problem. It is a charge paid at every step: (size of step 1) × (steps in the film) × (price per re-read). The decision is which of these three to lower for the whole film without hurting quality. Rewording our files can touch only about 5% of the size. The bigger levers are the app-side load (connectors) and the number of steps per film, which also drives Claude's writing and carried history (the dearest items 1 and 4).

## Root cause
1. Every step re-reads a step-1 load of about 82-95k tokens. Most of it is not ours, and nobody measures it, so the 13k rise on 21 Nov went unseen.
2. The film took 2,775 steps against a 15% target, 91% of them on Opus.
3. The 16 Nov condensing (`notes/proposals/startup-reading.md`, adopted) cut our text. It could not move this number, because our text is a small share of the floor. Cold-start Option 2 (`notes/proposals/cold-start.md`) said the app's part "cannot be cut by us". Connectors are switched on and off by Sam at claude.ai/customize/connectors (the app's docs), so that claim was never tested.

## Approaches weighed
1. **Condense our files again.** At most about 5% of the floor, roughly 0.6% of a week. It was already done on 16 Nov. Too small.
2. **Reframe: fewer steps per film.** More work per step (independent calls sent together) and fewer rounds. This lowers every per-step cost, not just this one. It is large, but it belongs to the item 1 proposal and needs its own evidence.
3. **Shrink the app's part.** Sam switches off the connectors that film chats never call. This could undo the 13k jump and more. Risk: a chat needs one later, for example to search for reference photos.
4. **Learn first.** Each chat's record splits the floor into our part and the app's part, flags any rise, and counts which connectors' tools were actually called over the last two films.
5. **Model mix.** Routine steps on Sonnet re-read at $0.10 instead of $0.18. This is already a rule, so it is a compliance question.

Chosen: 4 now, then 3, then 2, each as its own decision.

## Proposal
**Learn (this yes only; changes no film):** `source/stepcost.py` records, for every chat:
- our part of the floor (CLAUDE.md, agent files and hook printouts at step 1, counted);
- the app's part (the floor minus ours);
- the connectors called, with how many times.

The handover check prints one line when the floor is 3k tokens or more above the last film's. A one-off pass over this film's and the last film's transcripts (through the chat-reading tools) fills in the connector counts. Cost: about 0.5-1% of a week once, Opus medium; nothing per film after.

**Changes after, one at a time, each back through the route with its own figures:**
- **(a) Connectors.** If a connector shows zero calls across two films, Sam switches it off: one setting, undone with one setting. Number to beat: the floor back to 82k tokens or below, and no chat blocked for a missing tool. Measured on the record.
- **(b) Steps per film.** Handed to the item 1 proposal. Number to beat: fewer steps per film, with Sam's notes and repeated faults no higher than the last two films. This needs the notes count recorded first.

What Sam would notice: nothing until (a) comes to him as a plain yes or no, with the size it saves.

## Sam test
- Q1: An expert measures what fills the per-step load before cutting it. Rewording more text would not do that.
- Q2: The scope is the whole film's steps and two films' connector use, not one chat.
- Q3: It is enforced by the record and the handover check, not by a chat choosing to read. The root cause is shown with numbers.
- Q4: Five different approaches were weighed. The ones that cut text or push for Sonnet are smaller.
- Q5: This yes changes no film. Each later change is one setting or one rule, and each can be undone alone.
- Q6: Every figure names its source. The split of the app's part, and its cause, are marked unchecked.
- Q7: It is sized by the result: it goes for about 95% of the load, not the 5% that is cheap to edit.
- Q8: The record fields and the flag are permanent. They are reviewed at the film's end.

## Lost / Added
Lost: nothing now. Later, possibly a connector that no film used.
Added: three figures on every chat's record; one flag line; a one-off count of connector use.

## Unchecked
- The tokens per connector and in the app's instructions.
- What caused the 13k rise on 21 Nov.
- Whether switching a connector off removes it from cloud chats.
- The per-chat write cost (derived from one chat).
- This film's notes.
