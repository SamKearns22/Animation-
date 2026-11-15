# Helper B

## Leak
None stated. The file frames the choice as three ready-made asks, which narrows it.

## Results
- Chats 29 and 31 ran codemap.py/page.py 0 times; hand `grep -n`/`sed -n` on film or engine code 25 and 26 times (replay-record/tool-use-29-31.md).
- Those looks were ~33% of chat 29 (2.57% of a week) and ~27% of chat 31 (2.36%): ~1.5% of a week in two chats (bills-29-31.md; shares are estimates, unchecked).
- The page the notes-round pack says to read first was never made: no `story/protest-tiers-page.md` exists; only Blessed has one (job-packs.md).
- Rule 61's only check warns on a missing MAP or a file over 1,000 lines (rulebook). `protest_tiers.py` is 2,283 lines (counted): its split did not happen either. Nothing checks that the tool is used; the only tool-call hook is the cost watch (.claude/settings.json).
- Film: 53.2% of a week spent, 63.5% estimate, 32 chats (ledger/protest-tiers.md), over three times the 15% aim. The ledger records 0 notes and 0 rounds although round 1 ran: "fewer notes" cannot be measured today.
- Sam: first answers were half-efforts; "a systemic issue that could apply to every rule, test, kit and process" (sam-to-case5.md).
- Gap: no record shows, for any film, which tools and checks its packs name were actually run.

## The real decision
Not "which of three asks", but why work named on paper does not happen across a film's chats, and what makes it happen. Bigger levers: steps done by machine and use measured in every chat.

## Root cause
Tools and rules are opt-in text. Here the page the pack points to was never built, so the step failed silently and grep was the only path. Nothing measured or blocked the fallback. page.py and rule 61 were written and named but enforced nowhere; a pillar rule is more text of that kind. The Opus chat now editing the code-finding tool improves a tool no chat runs, before anyone knows why.

## Approaches weighed
1. Write the pillar rule now: text again; complies on paper, same failure.
2. Full audit of everything (8-12%): a sweep before results show what matters; earlier audits (12 Nov, 400 lines) gave ideas that did not land.
3. Learn-first, reframed: count adoption from transcripts for every tool and check the packs name, over Protest Tiers' 32 chats and the last finished film. The audit, sized by evidence.
4. Enforce by machine: handover start builds the page; a hook catches hand greps on film code and points to `page.py find`.

Chosen: 3, then 4 as the first single change; the rule waits for evidence.

## Proposal
- **Now:** the in-flight tool edit stops at a clean commit until step 1 reports.
- **Step 1, learning (changes nothing):** a Sonnet chat lists per chat the pack named, its tools, which ran, hand code looks; tests `page.py find` on 10 real notes; reports why the ledger counts no notes. ~2-3% of a week (unchecked), filed as tool work (rule 24).
- **Change 1 (own Y, after step 1):** `handover.py start` builds the page; a hook warns on hand greps of `source/FILM*.py` with the `page.py find` line ready, and logs each. Beat: hand code looks per notes-round chat from ~25 to 5 or fewer, cost share from ~30% to under 10%, read from the log; reviewed when Sam declares the next film complete. ~1% of a week.
- **Then, one at a time:** each skipped tool or check step 1 finds gets its own mechanism and number. The pillar rule comes last, from what worked: every rule names the machine that makes it happen and its number.
- **Sam notices:** one Y now; a table of used and unused tools; fewer hand-searches billed.

## Sam test
- Q1 Expert: measure adoption, enforce in the harness, not prose.
- Q2 Best result: two whole films, every named tool.
- Q3 Comprehensive: root cause found; enforced by hook and handover, measured by a log.
- Q4 Intelligent: four different approaches; text-only ones fail the evidence.
- Q5 Risk: step 1 changes nothing; each change has its own Y and is removable alone.
- Q6 Checked: sources named; estimates marked unchecked.
- Q7 Not cheap: the audit is kept in full where it matters (adoption); changes sized by their numbers.
- Q8 Nothing temporary: permanent changes, reviewed at film end.

## Lost / Added
- Lost: the 8-12% sweep as asked (replaced by the adoption count); the pillar rule now (comes later); the tool edit pauses.
- Added: one learning chat; a hook on hand code looks; the page built at every handover start.

## Unchecked
Grep cost shares; step 1 and change 1 costs; which pack chat 29 was told to read; the ledger's 33.55% "after the film" line against its 53.2% spend.
