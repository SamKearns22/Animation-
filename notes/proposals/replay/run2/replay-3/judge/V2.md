# Helper A: replay case 3

## Leak
Mild: "Decide what permanent change to how Claude works" presumes the answer is a rule about Claude's behaviour; I treat that as one option, not the frame.

## Results
- Code tools unused: chats 29 and 31 ran codemap.py/page.py 0 times; 25 and 26 hand searches (grep -n / sed -n) (tool-use-29-31.md).
- Hand code looks were ~33% of chat 29's estimated cost and ~27% of chat 31's (bills-29-31.md; estimates, not metered).
- Chat cost is driven by history re-reads: 92 and 117 calls, final history 252k and 229k tokens; 0 helper spawns in either (bills-29-31.md).
- Chat 29 was handed pack "Checks and animatic", which names no code tool, yet its job was fixing 107 faults in code; its handover's "For Claude" line hands over function names, a direct invitation to grep (notes/archive/protest-tiers-handovers.md, lines 316-325). Chat 31 was handed "Notes round", which does name page.py (guides/job-packs.md line 32), and still used it 0 times.
- page.py was never run on this film: no story/protest-tiers-page.md exists (only blessed-page.md); it was built and tested on Blessed only, and its kittest `round_page` fails on the main line (notes/goals-review-14-nov.md, notes/next-jobs.md).
- protest_tiers.py is 2,283 lines; rule 61 says a film file over ~1,000 lines is split (source/, guides/film-quality-rules.md row 61).
- The film: 51.27% of a week spent over 32 chats, against an estimate of 63.51% and an aim of 15% (notes/ledger/protest-tiers.md). The plan itself was 4x the aim.
- Proposals: Sam had to push four times (19:45-19:51) before the evidence scope widened (sam-to-case3.md).
- Gap: nothing in the record counts tool use per chat; the two counts above came from a helper reading transcripts by hand. Whether any other built tool is used is unknown.

## The real decision
Not "make Claude use page.py" or "make Claude propose bigger", but: the project has no feedback loop that measures, in every chat, whether the tools and rules it builds change the film's cost and notes. Bigger levers than the finding tool: chat count (32), history size per call, the plan's size (63.5%), and a film file twice the split limit.

## Root cause
1. Tools are judged when built (on Blessed), never when used: no record of use, so non-use is invisible until Sam asks.
2. Use depends on prose in a pack the chat may not be handed (chat 29) or may read and not follow (chat 31). The cheapest-looking move per call (grep) wins inside a chat.
3. The tool was never made ready for the live film (no page, failing kittest), so even a willing chat had nothing to read.
4. Proposals are sized by the chat that will pay for them, under a cost watch, and judged by the same chat; "I should have proposed that first" changes no mechanism.

## Approaches weighed
1. **Rule:** a new "always propose the best version first" rule plus "use page.py". Relies on reading and choosing; already failed (chat 31). Rejected.
2. **Force:** a hook that blocks grep/sed on film code and points to page.py. Enforced, but forces a tool not yet shown to find the right lines cheaper on this film.
3. **Reframe (feedback loop):** every chat's tool use and cost per fix is measured automatically and lands in the film's ledger; every tool and rule is then kept, fixed or dropped on that number.
4. **Learn-first:** replay chat 31's real notes through page.py on Protest Tiers and count calls against what happened.
Chosen: 3 as the permanent base, with 4 as its first use, then 2 only if 4 shows the tool wins.

## Proposal
**Learn first (changes nothing):**
- L1. Extend the hook that already runs after every tool call (costwatch) to tally each call (hand code look, page/codemap, check, render wait, edit, git) and the history size; the Stop hook (ledger.py auto) writes the tally into the film's ledger row. Kittested. Permanent; ~0.5% of a week once, ~0 per chat (estimate, unchecked).
- L2. Make page.py work on Protest Tiers (fix `round_page`), then replay chat 31's notes through `page.py find`: calls and tokens to reach the right line, against the 26 hand searches. ~0.5% (estimate).

**Then change, one at a time, each with its own yes:**
- C1 (only if L2 shows fewer calls): a before-the-call hook that, when a chat greps a film file, returns `page.py find` for those words instead. Number to beat: hand code looks per notes round, from 25-26 to under 5, read from L1's ledger line. Undone by removing one hook entry.
- C2: handover.py end refuses a Next/Read pair whose pack does not match the job's words (a "fix" job on the checks pack, as chat 29). Number: 0 mismatches.
- C3 (proposal half): back-end proposals go through the proposal route (fresh helpers, judge, Sam test) before Sam sees them, flagged by handover.py when a message to Sam proposes a tool, rule or check with no proposals file. Number: Sam's "is this the best?" pushes per proposal, from 4 toward 0.
Each later change (film-file split, helpers for searches, fewer longer-history calls) waits for L1's numbers to show its share.

**Sam would notice:** each film's ledger line says which tools were used and what a fix cost; no proposal reaches him unchallenged.

## Sam test
- Q1 Expert: an agent-ops expert instruments before enforcing; yes.
- Q2 Best result: evidence spans every chat from now on, not two; L2 replays real notes.
- Q3 Comprehensive: enforced by hooks and handover.py, not by reading; L1 shows whether it worked.
- Q4 Intelligent: four different approaches weighed; prose rules already failed.
- Q5 Risk: L1/L2 change nothing; each C is one hook or check, undone alone.
- Q6 Checked: sources named; costs of builds unchecked.
- Q7 Not cheap: sized to measure every chat permanently, not one more two-chat count.
- Q8 Nothing temporary: L1 is permanent; each C is made properly or not at all, reviewed when the film is complete.

## Lost / Added
- Added: a tool-use line in every film ledger; a page for Protest Tiers; later, up to three hooks/checks, each on its own yes.
- Lost: nothing; hand greps stay possible until C1 is approved.

## Unchecked
- Build costs (0.5% each) are estimates. Bills' cost shares are the helper's estimates. Whether page.py find beats targeted grep is unknown until L2.
