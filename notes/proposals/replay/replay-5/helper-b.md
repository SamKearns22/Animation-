# Helper B: what Sam should say yes to now

## Leak
The problem file lists the chat's three asks (pillar rule, 8-12% audit, a prompt on hand code-searching). Treated as facts about what was sent, not as the answer.

## Root cause
The project already has the pillar. Rulebook line 7: "A rule only holds if a check enforces it". But the same line lets "by hand" count as a check, and pre-flight's `gate_warnings` only prints (source/preflight.py 228-231: "not yet refusing"). So rules and tools depend on a chat reading something and choosing to follow it. The evidence:
- Chats 29 and 31 ran codemap.py/page.py 0 times. They made 25 and 26 hand grep/sed calls on film code (tool-use-29-31.md), although the notes-round pack names page.py (job-packs.md 32-33).
- No page was ever written for this film. `story/` holds only `blessed-page.md`.
- Rule 61's warning fired and nothing changed. The film's files run 2,283, 1,664 and 1,564 lines against a bar of about 1,000 (`wc -l source/protest_tiers*.py`).
- `.claude/settings.json` has no hook at the moment a tool is called (PreToolUse). Only the cost and ledger hooks run, and they measure money, not method.

Nothing records whether a tool was used, so non-use is invisible until Sam asks. A new pillar written as words would repeat line 7 and fail the same way: no hook enforces it.

## Approaches weighed
1. **Write the pillar as a new rule.** Words in a guide. Line 7 shows this does not hold.
2. **A one-off audit by reading.** It finds today's gaps, but nothing stops the next tool from going unused.
3. **Enforce at the moment of the work.** A PreToolUse hook (run by the app, not chosen by the chat) blocks a hand grep on a film code file. In its place it hands back `page.py FILM find` output, the FILE:LINE to read.
4. **Measure use in every chat.** `ledger.py auto` (the Stop hook, already run after every reply) counts each named tool's runs against hand searches. `handover.py end` lists any shortfall as a fault.
5. **Remove the choice.** `handover.py start` writes and prints the film's page itself, so the round starts from it.

Chosen: **3 + 4 + 5 as one mechanism, and the audit (2) becomes its first full use, not a reading exercise.** Step 3 makes the right way the only way. Step 4 is how we know it worked, in every chat, for good. Step 5 means the chat does not have to remember anything. Step 1 is merged into line 7 rather than added as a second rule.

## Proposal
- **What.** (a) The Opus chat already editing the code-finding tool builds the hook and the page-at-start. It is the same tool, so there are no two chats on one file. (b) The use counter goes into `ledger.py auto` and `handover.py end`. (c) Line 7 is edited: "by hand" and print-only warnings stop counting as checks. Each rule names a hook, a refusal or a counted tool. (d) The audit runs every rule and kit row against the whole chats of the last two films (Sam's own 19:48 push). Each item ends as enforce (named hook or refusal), merge or remove. Removals go on Lost: lines for Sam's Y.
- **Shown before it is switched on.** The hook is replayed against the 51 recorded calls of chats 29/31. It must fire on every grep of film code, and it must let through `sed -n` on lines that page.py pointed to. If it fails, it comes back to Sam unswitched.
- **Number to beat.** Hand greps on film code: 51 across two chats today, target 0. page.py/codemap runs per notes round: 0 today, at least 1. Both are counted by the ledger every chat.
- **Cost.** The hook, counter and page-at-start: about 1-2% of a week (unchecked estimate). The audit: 8-12% (problem file, unchecked). It is filed as tool work, outside the film's share (rule 24, "Costs by kind").
- **What Sam notices.** Rounds read only the lines a note touches, so they are cheaper and repeat fewer mistakes. A handover that says "page.py: 0 runs" becomes a fault Claude fixes before he sees it. There are fewer yeses, each one backed by a replay.

Questions for Sam (pick first):
1. Y: the hook, counter and page-at-start, built by the Opus chat now on the tool and switched on only after the replay passes.
2. Y: line 7 edited as above (the pillar, merged). Exact wording sent first.
3. Y: the audit on the last two films' whole chats, ending in one list with Lost: lines.

## Sam test
- Q1: An agent-workflow expert enforces at tool-call time and measures adoption. They do not add more prose.
- Q2: The audit uses the whole chats of the last two films. The hook is proven on the recorded calls.
- Q3: Root cause found (no enforcement, no measure). Compliance on paper is caught by the counter in every chat.
- Q4: Five different approaches weighed; the chosen one combines the three that do not rely on reading.
- Q5: The hook can be removed from settings. It is shown on the record before it is switched on. The audit changes nothing without a Lost: Y.
- Q6: Sources are named. Costs are marked unchecked.
- Q7: It is sized to stop the failure for good, not to the cheapest prompt.
- Q8: Permanent: a hook, a counter and a rule edit, reviewed at the film's end against the counter.

## Lost / Added
Lost: "by hand" as an accepted check (each rule needs a real one). Lost: free hand grep on film code files. Added: one PreToolUse hook, a tool-use count in the ledger and handover check, and the page printed at chat start.

## Unchecked
The pillar draft's 8 faults. The 8-12% and 1-2% costs. The split of the 51 calls between grep and sed. Whether page.py existed when Protest Tiers began. The Opus chat's current edits.
