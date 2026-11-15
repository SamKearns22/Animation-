# Helper A: replay case 5

## Leak
Partial: the problem file lists three asks already on the table (pillar rule, 8-12% audit, a start-of-search prompt). I judged them as options, not as the answer.

## Results
- Code tools unused: chats 29 and 31 ran codemap.py/page.py 0 times; 25 and 26 hand `grep -n`/`sed -n` calls on film or engine code instead (tool-use-29-31.md).
- The notes-round pack names page.py as the way to read (guides/job-packs.md, Notes round). Rule 61's only check is `preflight.gate_warnings`, a **warning**, not a stop (guides/film-quality-rules.md, rule 61).
- The page was never made for this film: `story/` holds only `blessed-page.md`, no protest-tiers page (directory listing).
- Rule 61 says split files over ~1,000 lines; protest_tiers.py is 2,283, _sets 1,666, _cast 1,564 lines (wc). The warning fired or not, nothing changed.
- Cost: protest-tiers spent 51.27% of a week against 63.51% estimated, 32 chats; "round1 moves" planned 4.45%, spent 14.04% (39.17 to 53.21) (notes/ledger/protest-tiers.md). Each notes-round chat ~2.2-2.6%.
- Gap: the ledger records **0 notes and 0 repeated in all 32 chats**, and its closing line says 33.55% while the table says 51.27%. The record cannot measure "fewer notes", one of the three aims.
- Sam (sam-to-case5.md): first proposals are half-efforts; the problem is "systemic ... every rule, test, kit and process".

## The real decision
Not "which of three asks", but: **does each rule actually change what chats do, across the whole film?** Sam's own diagnosis is systemic; the evidence fits it (a rule plus a tool plus a pack line, and 0 uses). Bigger levers than a prompt or a pillar's wording: whether checks stop or merely warn, and whether the record can measure notes at all. And Sam must not be asked for three yeses while a fourth change (the Opus edit to the code tool) is already in flight.

## Root cause
Rules are enforced by a chat reading them and choosing to comply. Rule 61 shows every layer failing: the pack line is read or not; the page was never generated for this film, so `page.py find` had nothing to search; the only check is a warning; oversize files make grep the quicker route. A pillar rule written in words has the same weakness (its draft took 8 faults in one critique), and the critique only tests the text, not whether chats obey it.

## Approaches weighed
1. **Write the pillar rule now** (as asked). Adds words a chat can still skip; the same failure mode.
2. **Reframe: enforce, don't write.** Turn the rules that matter from warnings into automatic stops/hooks the chat cannot pass by choice (a PreToolUse hook on hand grep/sed of film code; pre-flight stopping on oversize files and a missing page).
3. **Learn first: compliance audit of the last two films' whole chats.** For every rule with a tool or check: did its tool run, did its check fire, did it stop, what did skipping cost. Fills the notes gap from the transcripts.
4. Sweep and rewrite every rule, tool and kit at once. Too broad; cannot tell what worked.

Chosen: **3, then 2 one change at a time**, with change 1 able to go now because its evidence is already in.

## Proposal
**Now, one yes:** pause the in-flight Opus edit of the code tool (a change with no stated number to beat) and run the learning step.
- **Learn (changes nothing):** a compliance audit over every chat of protest-tiers and the film before it: per rule with a tool or check, runs vs. chances, fired/stopped, and cost of the chats that skipped it; plus each round's notes and repeated notes counted from Sam's messages and back-filled into the ledger. Output: a ranked list of rules by cost of non-compliance. Cost ~4-6% of a week (unchecked estimate; the asked audit was 8-12% because it also judged content).
- **Change 1, after its yes (evidence already in):** code reading is enforced, not advised: a PreToolUse hook refuses `grep`/`sed` on film code unless the page for that film exists and was queried this chat; pre-flight stops (not warns) on a film without a page or a file over 1,000 lines. Number to beat: 0 of 51 lookups through the page today; target every lookup through page.py in the next notes round, measured by the same count. Enforced by the hook, not by reading.
- **Changes 2, 3 ...:** the audit's top rules, one per yes, each with its own number and measure.
- **Pillar rule:** waits for the audit; if kept, it is written as a check (every change names a number and a measure, verified at film close), not as advice.
- Sam notices: one decision now instead of three; fewer hand-read rounds; notes counted so "fewer notes" can be shown.

## Sam test
Q1 Expert: enforcement over instructions is the standard agent-workflow answer; yes.
Q2 Best result: whole chats of the last two films, as Sam asked, not one film or two chats.
Q3 Comprehensive: root cause named with evidence; success measured by tool-call counts; the hook acts in every chat without reading.
Q4 Most intelligent: four different approaches weighed; the one that removes choice wins.
Q5 Risk: learning changes nothing; change 1 is one hook, removable alone; a hook that wrongly blocks shows at once.
Q6 Checked: sources named; estimates marked unchecked.
Q7 Not cheap: the audit covers every chat of two films and every checked rule; the cheap version (a prompt) is rejected.
Q8 Nothing temporary: each change made properly as a stop, reviewed against results at film close.

## Lost / Added
Lost: the in-flight code-tool edit pauses; the pillar rule is not written today.
Added: one compliance audit (~4-6%); one hook and two pre-flight stops after their yes; notes counts in the ledger.

## Unchecked
Audit cost; whether chats 29/31 saw the rule-61 warning; the previous film's tool use; why the ledger's closing figure (33.55%) differs from 51.27%; ledger models (chats 27, 30, 31 titled Opus, logged Sonnet).
