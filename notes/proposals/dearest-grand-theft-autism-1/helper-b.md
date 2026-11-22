# Helper B: start-up reading on grand-theft-autism

## Leak
None. The problem file gives no remedy. Its name for the cost ("rules, tools, first files") is itself misleading (see Results).

## Results
- Total: 11.93% of a week across 28 chats (22% of the film's 54.67%). Source: `python3 source/dearest.py grand-theft-autism`.
- What the cost actually is: `source/stepcost.py` split() counts as "start-up floor" everything in context at a chat's
  first step (the app's own instructions and tool menu, CLAUDE.md, hook output, the opening prompt), then charges it
  again at every later step. Files read after step 1 are not part of it.
- Size of the start: 80-82k tokens in every chat to 20 Nov, 91-95k on 21 Nov (ledger `split.floor_k`). This chat
  started at 95.9k (its own transcript). CLAUDE.md is 15,301 characters, about 3.8k tokens, so about 4% of the
  start. The other ~96% is the app's own text (system prompt, tool definitions, connector instructions), as
  `notes/proposals/startup-reading.md` already found on 16 Nov.
- It is paid per step, not per chat. For each chat, steps x start size x re-read price ($0.18/M Opus,
  `.claude/hooks/costwatch.py`) gives back the floor cost within about $0.15 a chat. The first-step write is small
  because the app's opening is mostly cached already.
- Steps: 2,775 in the film. Tool calls counted: 2,793 (ledger `calls`), so about one call per step. Of 1,586 steps
  that searched or read files, 1,130 came straight after another such step (ledger `search.list`). How many of those
  could have gone in one step together: unchecked.
- Faults or Sam's notes caused by this: none in the record. It is pure cost, so quality is not at stake in removing it.
- Gap: the record cannot say which part of the ~85k opening each connector (web search, page reading, documents,
  chat control) adds, why the opening grew by 13k tokens on 21 Nov, or whether film chats ever use the web tools.

## The real decision
Not "read fewer rules at start-up". The real question is how many tokens get re-read at every step of the film:
(size of the fixed opening) x (steps in the film). The repo's text is a minor part of that. Two bigger levers: the
app tool menu attached to film chats, and how many steps the film takes. Fewer steps also cut "carried history",
the film's next-biggest per-step cost.

## Root cause
Every step re-sends the whole opening. That opening is mostly the app's tool menu, which grows whenever a connector is
added. The opening is identical in all 28 chats. The chats also take about one action per step: they run searches
one after another, though the app's own instructions already tell them to group independent calls. That instruction
relies on a chat choosing to follow it, and nothing measures it. The 16 Nov fix (startup-reading, adopted) shortened
the repo's text, which is the small part, so it could not move this number much.

## Approaches weighed
1. Shorten CLAUDE.md and the packs further. Ceiling: about 4% of 11.93%, so about 0.5% of a week. It puts rules at
   risk. Rejected.
2. Reframe, fewer steps: group independent searches and reads into one step, enforced by a check, not by asking.
   Every step saved also saves its share of carried history.
3. Reframe, a smaller opening: film chats carry only the connectors films use. Sam switches off the rest in the app.
4. Learn first: measure the opening by part and measure the grouping chats missed, before changing anything.
5. Fewer, longer chats: no effect, because the cost is per step, not per chat. Rejected on the evidence above.
Chosen: 4, then 2 and 3, as two separate changes, each sized by what 4 finds.

## Proposal
**Learn (changes nothing; about 1% of a week, Opus medium):**
- L1: split the opening by source. Repo text (CLAUDE.md, hook output, opening prompt) is counted exactly. The rest
  is the app's. Find the cause of the 21 Nov rise: CLAUDE.md's growth that day was about 0.6k tokens, so the rest of
  the 13k is unchecked. Check from all films' chat records whether any film chat called the web-search or document
  tools. The per-connector size needs one empty chat with one connector off. Only Sam can do that, so it would be one
  plain question to him.
- L2: from the ledger's step lists, count the searches that did not depend on the step before them and could have
  shared a step. Result: the steps and % of a week that grouping would have saved on this film.

**Change A (only if L2 shows at least 10% of steps could have been grouped):** a check that runs after each tool
call and counts runs of single, independent searches. It prints one line in the chat, and the handover check reports
steps per call for each chat. The number to beat: grand-theft-autism's 2,775 steps per film for the same work,
measured automatically by the ledger at the end of the next film. Cost: about 1% of a week to build.
**Change B (only if L1 shows unused connectors make up at least 15k tokens):** one plain request to Sam, naming the
connectors to switch off and keeping one web search for reference photos. The number to beat: the 82-95k opening,
read from the ledger for every chat. Undone by switching them back on.
Each change is decided, enforced and judged alone, and kept or removed in the end-of-film review.
Possible saving: 2-5% of a week per film (unchecked until L1 and L2 report), against a total cost of about 2% once.
What Sam would notice: nothing in the films. At most, one settings question about connectors.

## Sam test
Q1: Yes. An expert measures the fixed context and the steps first, and avoids cutting rules for a tiny saving.
Q2: Uses all 28 chats, compares with other ledgers (82-95k everywhere), and names the gaps.
Q3: Root cause found. Enforcement is a check and the ledger, not reading. Success is a measured number.
Q4: Five different approaches weighed. Two rejected on numbers.
Q5: Learning risks nothing. A can be removed alone, and B is undone by switching connectors back on.
Q6: Sources named. Savings and the 21 Nov rise are marked unchecked.
Q7: Sized by the measured result. It avoids the cheap trap of trimming CLAUDE.md.
Q8: No trials. Each change is permanent if adopted, reviewed at the end of the film.

## Lost / Added
Lost: possibly connectors films never use (only after L1, with Sam's Y). Added: two measurements, one check, one
handover line.

## Unchecked
How many of the 1,130 back-to-back search steps were independent. Why the opening grew to 91-95k on 21 Nov. The size
of each connector. Whether film chats use the web tools. The 2-5% saving.
