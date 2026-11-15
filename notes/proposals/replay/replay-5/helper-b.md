# Helper B: what Sam should say yes to now

## Leak
The problem file lists the chat's three asks; treated as facts, not the answer.

## Root cause
The pillar exists: "A rule only holds if a check enforces it" (rulebook line 7). But that line accepts "by hand", and `gate_warnings` only prints ("not yet refusing", source/preflight.py 229). So a rule holds only if a chat reads it and chooses to follow it:
- Chats 29 and 31 made 0 page.py or codemap runs and 51 hand grep/sed calls on film code (tool-use-29-31.md); the pack names page.py (job-packs.md 32).
- No page was written for this film (`story/` holds only blessed-page.md).
- Rule 61's warning changed nothing: files of 2,283, 1,664 and 1,564 lines (limit about 1,000).
- `.claude/settings.json` has no PreToolUse hook (one that runs when a tool is called); its hooks measure money, not method.

Nothing counts tool use, so non-use is invisible until Sam asks. A pillar in words repeats line 7 and fails the same way.

## Approaches weighed
1. Pillar as a new rule: words; line 7 shows words do not hold.
2. Audit by reading: finds today's gaps, stops nothing next time.
3. Enforce at the moment of the work. A PreToolUse hook (run by the app, not the chat) blocks a hand grep on film code. It returns `page.py FILM find` output (the file and line) instead.
4. Measure every chat. `ledger.py auto` (already run after every reply) counts named-tool runs against hand searches. `handover.py end` lists any shortfall as a fault.
5. Remove the choice. `handover.py start` writes and prints the film's page itself.

Chosen: 3+4+5 as one mechanism; the audit (2) is its first full use; the pillar (1) merges into line 7.

## Proposal
- **What.** The Opus chat already on the code tool builds hook and page-at-start (no two chats on one file); the counter goes in `ledger.py auto` and `handover.py end`.
- **The pillar.** Line 7 edited: "by hand" and print-only warnings stop counting; each rule names a hook, refusal or counted tool.
- **The audit.** Every rule and kit row measured on the last two films' whole chats (Sam, 19:48): enforce, merge or remove; removals on Lost: lines.
- **Shown first.** The hook is replayed on chats 29 and 31's 51 recorded calls. It must catch every grep of film code and pass `sed -n` on lines page.py named; if not, back to Sam, off.
- **Number to beat.** Hand greps on film code 51 → 0; page.py runs per round 0 → at least 1; the ledger counts both every chat.
- **Cost.** Hook, counter, page: about 1-2% of a week (unchecked); audit 8-12% (problem file); filed as tool work, outside the film's share (rule 24).
- **What Sam would notice.** Rounds read only the lines a note touches: cheaper, fewer repeated faults; "page.py: 0 runs" is fixed before he sees it.

Questions (pick first):
1. Y: the hook, counter and page-at-start, switched on once the replay passes.
2. Y: line 7 edited as the pillar (wording sent first).
3. Y: the audit on the last two films, ending in one list with Lost: lines.

## Sam test
- Q1: An expert enforces at the moment of work and measures use, not prose.
- Q2: Audit on both films' whole chats; hook proven on recorded calls.
- Q3: Root cause shown; the counter catches paper compliance every chat.
- Q4: Five weighed; the three chosen do not rely on reading.
- Q5: One settings entry undoes the hook; shown on the record first; nothing removed without a Lost: Y.
- Q6: Sources named; costs unchecked.
- Q7: Sized to end the failure, not the cheapest prompt.
- Q8: Permanent hook, counter and rule edit, reviewed at the film's end.

## Lost / Added
Lost: "by hand" as an accepted check. Lost: free hand grep on film code. Added: a PreToolUse hook, a tool-use count in the ledger and the handover check, and the page printed at chat start.

## Unchecked
The pillar draft's 8 faults; both costs; the 51 calls' grep/sed split; the Opus chat's edits so far.
