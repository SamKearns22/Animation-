# Proposal: The word Override: one code word that skips any check, guard or step between Sam and one ask; and drop the 'Locked by Sam' line from messages to Sam

Status: open

## Problem
Sam asked (23 Nov, his words): "make sure 'Override' works as a universal code word for skipping steps on all parts
of the project." Today the word works in one place only (the cost watch at red). Elsewhere the guards that stand between
Sam and what he asked for (the send guard for videos, the finishing tool's proposal-route stop, the proposal Stop hook,
the handover check) have no way to hear him, so a chat that Sam has told to go on still cannot: chat 47 built animatic
v5 and could not send it to him, and Sam (iPhone app only, little usage left) waited a whole chat for it.
Second request (Sam, 23 Nov 10:54): "Please remove the 'locked by Sam' section of communication as it doesn't help me."
The line lives in every handover by a CLAUDE.md rule; handovers' bottom lines reach Sam's messages.

## Facts
- Sam's request, word for word: notes/grand-theft-autism.md "Chat 47" (Sam's rule request line); his Y to running the
  route for it is in the same line.
- Existing override uses: CLAUDE.md line 87 ("'Just go' (or any override) skips waiting for my yes, never the checks or
  the hand-over"); CLAUDE.md line 148 and rulebook rule 85 (cost watch red: hand over unless Sam types 'override');
  .claude/hooks/costwatch.py lines 163-168 (reads a prompt starting "override"); source/handover.py lines 291-294 (fault
  when a chat treats something as an override Sam never typed); source/ledger.py line 611 (a bare "override" is not a note).
- Guards that refused or would refuse chat 47's send: source/humancheck.py sendgate (PreToolUse on SendUserFile: body
  check record + critique, rule 89); source/finish.py lines 209-213 (refuses while propose.open_letthroughs() lists
  unsettled entries: 3+ today, from other chats e0605414 and 9c3f62f3, not this film); source/propose.py hook (Stop
  hook blocking change asks without a verdict). Hooks list: .claude/settings.json.
- CLAUDE.md "Statement One" (quality never cut) and "Fix the drawing, never the shot" (Locked shots) stand above any
  speed rule; "Rules are permanent" says every rule needs a working check that caught a saved example (Sam's Y, 23 Nov).
- "Locked by Sam" line: CLAUDE.md "Fix the drawing, never the shot" says every handover has one; no code check reads it
  (grep of source/ and .claude/hooks/ for "Locked": none). Handover bottom 3 lines go to Sam; the rest is notes.
- Chat 47 already stopped showing the line to Sam (notes "Where things stand (23 Nov, chat 47 done)").
- Saved example of the fault: chat 47's refusals (notes "Chat 47": "Blocked: SendUserFile needs a body check record +
  critique (rule 89); finish.py refuses ... Writing a stand-in record was refused.")

## Record
CLAUDE.md
guides/film-quality-rules.md
notes/grand-theft-autism.md
.claude/settings.json
.claude/hooks/costwatch.py
source/humancheck.py
source/finish.py
source/propose.py
source/handover.py
source/ledger.py
