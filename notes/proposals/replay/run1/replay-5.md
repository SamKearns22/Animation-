# Proposal: what Sam should say yes to now

Status: open (replay case 5)

## Problem
Sam has been sent three asks at once: (1) write a new "pillar" rule into the rulebook (fixes aim for the biggest
lasting result; its draft was attacked once by a fresh critic, which found 8 faults, 7 then fixed); (2) run an audit
of every rule, tool and kit, about 8-12% of a week; (3) add an automatic prompt that fires when a chat starts
searching film code by hand. Meanwhile an Opus chat is already editing the code-finding tool. Sam's recent messages
(in the record) say first proposals are half-efforts until he pushes. Decide what should happen next, and what Sam
should be asked to approve.

## Facts
- Code tools: 0 runs in chats 29 and 31 although the notes-round pack names page.py (tool-use file, guides/job-packs.md).
- The project's aims (CLAUDE.md, "Rules are permanent"): high quality, fewer notes and faults, a film within 15% of a
  week; removing a step needs Sam's Y on a "Lost:" line.
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case5.md
notes/proposals/replay-record/tool-use-29-31.md
notes/ledger/protest-tiers.md
CLAUDE.md
guides/film-quality-rules.md
guides/job-packs.md
.claude/settings.json

## Verdict (the judge, word for word)
<!-- verdict-hash: 15b288182f6a4313 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes: mild. The Facts line sets "0 code-tool runs" beside "the pack names page.py", and the Problem quotes Sam saying first proposals are half-efforts. Together they push toward "words did not hold, so enforce" and toward refusing the three asks as they stand. No solution is named.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 4 | 4 | 19 |
| V2 | 5 | 5 | 3 | 3 | 4 | 20 |
| V3 | 2 | 2 | 2 | 2 | 3 | 11 |
## Sam test
Q1: Yes. An expert puts the guardrail in the harness (a hook the app runs), counts real use in every chat, and removes the choice (the page is built at chat start). Advice in prose is not what an expert would rely on.
Q2: Yes. The audit covers the whole chats of the last two films, as Sam asked at 19:48. The hook is proven on the 51 recorded calls before it is switched on.
Q3: Mostly. The root cause is shown: rulebook line 7 accepts "by hand", gate_warnings only prints, and settings.json has no PreToolUse hook. The counter catches paper compliance in every chat. Weak spot: engine files sit outside the page, so a grep on them is counted but not blocked (F1).
Q4: Yes. Five approaches were weighed, plus V1's "make the tool shortest" and "freeze" options. The three chosen approaches are the only ones that do not depend on a chat reading something.
Q5: The hook is undone by one settings entry and the rule edit by a text revert. Nothing is switched on before the replay passes, and nothing is removed without a Lost: Y. Sam still says Y before seeing the page-at-start and the counter run (F5).
Q6: The facts were checked: 0 runs and 25+26 grep/sed calls, job-packs l.32, rulebook l.7, preflight "not yet refusing", no page in story/, file sizes 2,283/1,666/1,564, rule 24's tool-work line. The costs are unchecked (F4).
Q7: Yes. It is sized to end the failure for every rule, not to add the cheap reminder prompt.
Q8: The changes are permanent: hook, counter, kittest, and a rule edit. They are reviewed at film complete. The replay is an acceptance test, not a trial.
## Pick
V2
## Why
V2 alone attacks the systemic issue Sam named at 20:00, that every rule can be complied with on paper. It does this in three ways. It edits the existing pillar line (rules are written once, edit before adding). It counts tool use in every chat, not only during the audit. It removes the choice by building the page at chat start. V3 approves all three asks as words and a soft prompt, sets no measure and finds no root cause. V1 has the better hook mechanics and the most careful fact check, but it drops the pillar, leaves line 7 accepting "by hand", and measures use only once.
Taken from V1:
- the 60-line window after a `find`;
- the rebuild of a stale page;
- the 90% replay bar;
- wiring propose.py's Stop hook (checked: not in settings.json);
- the cost source (code-looking about 1.5% of a week in chats 29 and 31: 0.33x2.57 + 0.27x2.36);
- the ledger faults.
## Faults in the pick
- F1 [fixed] The 51 calls were on "film or engine code", but page.py covers only source/FILM*.py. The hook now blocks only film files, and the counter reports engine greps separately. The film/engine split is unchecked.
- F2 [fixed] V2's pass rule ("sed -n on the lines page.py named") would strand a fix two lines off. It now uses V1's 60-line window, stale-page rebuild and 90% bar.
- F3 [fixed] Dropping "by hand" at once would leave the 21 rows that mention it unheld. Instead, each by-hand row is listed as an open fault by handover.py end until the audit converts it or Sam says Y to a Lost: line.
- F4 [named] The costs are unchecked. The hook, counter and page are 1-3% of a week (V2 says 1-2, V1 says 2-3). The audit's 8-12% is the problem file's figure. All of it is tool work, outside the film's share (rule 24).
- F5 [named] What the Opus tool chat has changed is unchecked, and so is its effort level. Building new needs Opus high.
- F6 [named] The pillar draft's one remaining fault has not been seen. The line 7 wording goes to Sam first.
- F7 [named] The counter writes into a ledger with known faults. Rows 27, 30 and 31 say "Opus" in the title but are logged as sonnet, and the header (51.27%) disagrees with After the film (33.55%). These are fixed in the same job.
- F8 [fixed] propose.py's Stop hook is now wired, as V1 proposed.
## Final version
**Order.** The Opus chat already on the code tool pushes its work, and it is merged first. If that chat is on Opus high, it builds the items below. If not, it opens an Opus high chat to build them. Two chats never work on one file.

**1. Code-search hook.** A PreToolUse hook (the app runs it before a command) acts on grep, sed or cat of source/FILM*.py.
- Until `page.py FILM find` has run in the chat, the hook blocks the command and returns find's FILE:LINE answers instead.
- After a find, reads within 60 lines of those lines pass.
- A stale page is rebuilt first.
- Engine files are not blocked, only counted.
- It gets a kittest, and rule 61 names it.

**2. Removing the choice.** `handover.py start` builds and prints the film's page.

**3. The counter.** `ledger.py auto` counts named-tool runs against hand searches in every chat. `handover.py end` lists a shortfall as a fault. The same job fixes the ledger's model column and its two totals.

**4. Route hook.** propose.py's Stop hook is wired into settings.json.

**5. The pillar.** Line 7 is edited, with the wording sent to Sam first. A rule holds only through a hook, a refusal or a counted tool. "By hand" and print-only warnings are listed as open faults until they are converted.

**6. The audit.** Every rule, tool and kit row is measured on the last two films' whole chats: did it run, did it fire where the work happens, did it help. Each row ends as enforce, merge or remove, and every removal goes on a Lost: line. The result is one ranked list.

**Shown first.** The hook is replayed on the 51 recorded calls. It must block every film-file grep, and 90% of the replayed finds must land within 60 lines. If not, find is fixed, or the result goes back to Sam with the hook off.

**Numbers to beat.**
- Film-code hand greps: 51 to 0 unrouted.
- page.py runs per round: 0 to at least 1.
- Code-looking share of calls: 27-35% to under 10%.
- Notes and repeats per round: no rise.

**Cost.** Unchecked estimates: 1-3% of a week for items 1-5, 8-12% for the audit. All of it is tool work.

**Review.** Reviewed at film complete.

Questions (pick first):
1. Y: items 1-4, switched on once the replay passes.
2. Y: the line 7 edit (wording first).
3. Y: the audit, ending in one list with Lost: lines.
## For Sam
### Option 1: Make the tools impossible to skip, then check every rule the same way
Chats 29 and 31 never used the code-finding tool we built. Instead they searched film code by hand 51 times, because nothing made them use the tool. Under this option the app itself stops a hand search of film code and hands back the tool's answer instead. Every chat starts with the film's page already open. Every chat's tool use is counted, and a skipped tool shows up as a fault before you see anything. The pillar becomes one edited line in the rulebook, not a new rule. Then every rule and tool from the last two films is checked the same way. It is proven on the 51 real searches before it goes on.
Lost: rules counting as held when they are only ticked "by hand"; free hand searching of film code.
Added: a block on hand searches, a page at every chat start, a use count on every chat, an audit with one ranked list.
### Option 2: The block only, with a shorter audit
This also stops hand searches of film code, with the same safety margins and the same proof on the 51 searches. The audit is a script that grades every rule as "blocks, warns or by hand" and checks whether each one ran in the last two films. There is no rulebook change and no use count on each chat, so a rule that is skipped later is only caught at the next audit.
Lost: the pillar rule and the read-through audit; checking every chat.
Added: a block on hand searches, the route's own hook, and a cheaper audit script (an unchecked estimate of 4-6% of a week).
