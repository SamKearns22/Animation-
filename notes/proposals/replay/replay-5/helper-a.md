## Leak
None: the problem lists three asks but picks none.

## Root cause
Enforced things happen; chosen things don't.
- Enforced, and working: cost watch, ledger stop, finish.py refusals (`.claude/settings.json`; rows 24, 75, 85).
- Chosen, and failed: the pack names page.py (`guides/job-packs.md` l.32); chats 29 and 31 ran it 0 times and made 51 grep/sed searches instead (`tool-use-29-31.md`).
- The tool works (codemap.py runs on `protest_tiers.py`); no `story/protest-tiers-page.md` was ever built.
- Rule 61 only warns: `protest_tiers.py` is 2,283 lines (limit 1,000) and its MAP has no line numbers, so grep is shortest.
- 13 of 63 rule rows are checked "by hand", 5 only warn (keyword count).
- `propose.py hook` (the route's Stop hook) is not wired into settings.json here.
- A prose pillar rule and an advisory prompt both rely on choice.

## Approaches weighed
1. **Approve all three.** More prose relying on choice: the cause.
2. **Enforce, don't instruct.** Wire the route's hook; block hand-searches until the page is used; audit enforcement on real chats.
3. **Make the tool shortest.** Split files, line-numbered MAPs; leaves every other "by hand" rule.
4. **Freeze until the film is complete.** Fails Q8; the next film repeats it.

Pick: 2, with approach 3's automatic page rebuild included.

## Proposal
First, the Opus tool chat pushes and is merged before anything touches that tool.

1. **Wire `propose.py hook` into Stop.**
2. **Code-search hook (PreToolUse on Bash).**
   - It blocks grep, sed or cat on `source/FILM*.py` until `page.py FILM find` has run in the chat.
   - It rebuilds a stale page.
   - After a `find`, reads within 60 lines of what it pointed to pass.
   - Kittest; rule 61 names it.
   - Before switch-on, the 51 real searches replay through `find`: 90% must land within 60 lines, else `find` is fixed first.
3. **An enforcement audit instead of the read-through.**
   - A script grades every rule and kit tool as blocks, warns or by hand.
   - It counts whether each actually ran in the last two films' chats.
   - Each "by hand" or never-run item goes through the route; its fix is a check, or says why not.
4. **No separate pillar rule:** already Q3 and Q7 (`sam-test.md`); rules are written once (CLAUDE.md).

**Numbers to beat**
- Hand-searches: 51 in two chats to 0 unrouted (hook-logged).
- Code-looking share of calls: 27–35% (`bills-29-31.md`) to under 10%.
- Notes and repeats per round: no rise, per the ledger.

**Cost (estimates, from ledger chats at 1.3–2.6% each)**
- The hook and its acceptance test: 2–3% of a week.
- The audit: 4–6% of a week.
- Tool work, outside the film's share (rule 24). Code-looking in chats 29 and 31: about 1.5% (estimate).

**What Sam notices:** one Y now; notes rounds that cost less; proposals that arrive already critiqued; one ranked list from the audit.

## Sam test
- **Q1:** guardrails in the harness, not reminders: expert practice.
- **Q2:** whole chats of both recent films.
- **Q3:** blocks, not asks; the audit measures what ran.
- **Q4:** four approaches; only enforcement fixes the shared cause.
- **Q5:** 90% bar and post-`find` passes guard against stranding; undo is one settings line; proven before switch-on.
- **Q6:** sources named; costs marked estimates.
- **Q7:** sized to enforce every rule.
- **Q8:** permanent, kittested, reviewed at film complete (`propose.py review`).

## Lost / Added
- Lost: the separate pillar rule, the 8–12% read-through audit, and the soft prompt.
- Added: two hooks, an enforcement audit script, and the audit's proposals.

## Unchecked
- The pillar draft's one remaining fault.
- What the Opus tool chat is changing.
- Whether `find` reaches 90%.
- The audit's exact cost.
- Ledger rows 27, 30 and 31 are titled "Opus" but logged as sonnet.
- The ledger header shows 51.27% spent, but "After the film" shows 33.55%.
