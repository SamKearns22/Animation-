## Leak
none.

## Root cause
One cause: the better path relies on a chat reading something and choosing it; nothing at the moment of action makes it happen or notices.
- Code tools: rule 61's only check warns when a file has no MAP or is over 1,000 lines (film-quality-rules.md row 61). It checks files, not behaviour. Protest Tiers' files are 2,283, 1,564 and 1,666 lines long, so the warning fires and nothing stops. `story/protest_tiers-page.md` doesn't exist, so the page was never built (checked). Result: 0 tool runs against 25 and 26 hand searches (tool-use-29-31.md). The habit beats a written line.
- Cheap first proposals: the only pressure a chat feels at every step is cost (costwatch runs after every tool call; settings.json). The chat invents, judges and sizes its own idea, so it settles on a cheap plausible one. It improved only when Sam pushed (from 2 chats to 8; problem file, Sam 19:45-19:51). It also stated a fact before checking it (problem file). `propose.py` describes a Stop hook that blocks unrouted change questions, but settings.json's Stop list holds only `ledger.py auto` (checked). Written, not wired: the same fault.
- "I should have proposed that first" is a promise with no mechanism behind it.

## Approaches weighed
1. Stronger wording in CLAUDE.md. Rejected: this is what has already failed.
2. Enforce at the moment of action: hooks redirect or block the worse path.
3. Make the tool the only easy path: build the page automatically, and put each note's file and line into the handover.
4. Review afterwards: count use and pushed proposals at film end. This finds problems but doesn't prevent them.

Chosen: 2, with 3 and 4 as parts. They remove the choice and prove it.

## Proposal
**"Built means wired"**, a permanent rulebook rule with its check. A tool, rule or gate is done only when a hook makes it happen, its use is counted per chat, and a test replays one real past case through it. Applied now:
1. **Code-search hook**, run before each command. A hand search of film or engine code builds the page if it is missing. The chat's first hand search is refused and answered with `page.py find` or `codemap.py` results for the same words. Reading known line ranges stays allowed.
2. **Wire propose.py's Stop hook**, so no change question reaches Sam unjudged.
3. **Counters** in `handover.py end`, also run from the Stop hook. They count tool runs against hand searches, and proposals marked "replaced" after a push. A new catalogue tool with no hook or counter is a fault.
4. **Reviewed** in `propose.py review` when Sam declares a film complete.

**To beat:** 0 tool runs against 25 and 26 hand searches. Code looks took an estimated 27-33% of cost (bills-29-31.md). Target: at least 1 tool run in every chat that touches film code, at most 5 hand searches, and 0 proposals replaced after a push. The counters measure this for free.

**Cost:** one Opus high tool chat, about 2.5% of a week (judged from chats 29 and 31 at 2.57% and 2.36%, protest-tiers ledger lines 57 and 59). Each refusal adds one small turn.

**Sam notices:** proposals arrive critiqued, fewer pushes, and the handover says whether the new tools were used.

## Sam test
Q1: experts enforce through the system the model runs in, not through what it reads.
Q2: built on two whole chats' records plus the gate's wiring; the counters then cover every chat.
Q3: the hooks act without being read, and the counters expose any gap.
Q4: four different approaches weighed; the record shows wording failing.
Q5: a hook could wrongly refuse. It refuses only once and returns an answer, and one settings line undoes it.
Q6: sources named; doubts listed below.
Q7: sized to make the tools get used in every chat, not by price.
Q8: permanent, reviewed at film end.

## Lost / Added
Lost: each chat's first hand search of film code.
Added: one rule, two wired hooks, counters, one handover line.

## Unchecked
Whether the page would have cost less than the hand searches (27-33% is a call-count estimate). The tool chat's real cost. Which job pack chat 29 read.
