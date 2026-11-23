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

## Verdict (the judge, word for word)
<!-- verdict-hash: 95ab783d027391ae -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper B, V3 = helper A. Picked: V2 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: the title gives the design ("one code word that skips any check, guard or step ... and drop the 'Locked by Sam' line"), and the film notes the facts point to carry a draft wording (skip all, log it, a "Checks: skipped" line, never Locked shots). V1 follows it closely; V2 and V3 set it aside.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 4 | 2 | 4 | 14 |
| V2 | 4 | 4 | 3 | 4 | 4 | 19 |
| V3 | 3 | 3 | 4 | 3 | 4 | 17 |
## Sam test
Q1: Yes. An expert would split the stops into three kinds (waits for Sam's yes, quality checks, wrong blocks) and treat each on its own; one word for all three hides wrong blocks and sends unchecked work as if checked.
Q2: The one case (chat 47) is thin, so the pick widens it: a week of refusals across every job is sorted before the record-through-the-mix change is built. The wrong block is already shown by the record (all 4 open let-throughs come from two other chats; 2 of the 3 settled since 23 Nov were "false block"), so that fix does not wait.
Q3: Root causes named with evidence: guards cannot hear Sam (only the cost watch reads his message); the finishing tool ties every film to other chats' backlog; the sound mix makes a new video without the body-check record. Each change has a replay test and a count at handover; Sam's word is checked against his own message in the chat record, so a chat cannot fake it.
Q4: Four approaches weighed by the helpers (universal word, fix the blocks, override by kind, learn first); the pick combines the strongest.
Q5: Each change is its own yes and undoes alone. The real risk is line 87: on Override, unchecked work can reach Sam, labelled, with the checks run next; this is put to him as a question, not assumed.
Q6: Facts checked: cost-watch "override" lines 163-168, finishing tool lines 209-213, handover OVERRIDE fault lines 291-294, Stop hook blocks once then logs, no code reads "Locked", 4 open let-throughs. Costs and whether Sam typed Override in chat 47 are marked unchecked.
Q7: Sized by the result: it fixes the causes, not just adds the word; the cheap one-word version (V1) is rejected.
Q8: Permanent changes, each with its check; reviewed against the film's results when Sam declares it complete. The learning step is a one-off measurement, not a trial.
## Pick
V2
## Why
V2 is the only version that answers the real decision (which stops should yield to Sam, and why chat 47 was stuck) rather than the wording. It sees that chat 47 hit two different stops: a right one (no body check, no critique) and a wrong one (the finishing tool refusing every film over two other chats' unsettled paperwork), and that one word would hide the second instead of fixing it for every film. It keeps Statement One by labelling unchecked work and running the checks next, and puts the change to line 87 to Sam as a question. V1 bundles both requests, skips quality checks silently, and leaves the wrong block in place. V3 is honest and fake-proof but defers the wrong-block fix, which today stops every film.
Taken from V3: Sam's word is confirmed against his own message in the chat record (not a file a chat could write); the message line wording "Checks: not run (your Override): ..."; the handover counting both "Override refused" and "Override invented".
Changed from V2: the learning step now gates only the mix-record change; the wrong-block fix, Override and the Locked line go ahead on Sam's yes, since the record already justifies them.
## Faults in the pick
- F1 [fixed] V2's cost figure was wrong (97.83%); the notes say 93.83% of the 15%, forecast 97.4%.
- F2 [fixed] V2 made every change wait on a week of learning; only the mix-record change needs it.
- F3 [fixed] V2's Override record was a log the prompt hook writes; now also confirmed against Sam's own message in the chat record (V3).
- F4 [named] The Override design rests on one case (chat 47); whether Sam typed the word there is unchecked.
- F5 [named] On Override, unchecked work can reach Sam (labelled); this changes line 87 and needs his Y.
- F6 [named] Build costs (about 2.8% of a week in all) are estimates, unchecked.
- F7 [named] Four separate yeses instead of the one thing Sam asked for: more to answer, but no bundled risk.
## Final version
Learn (no change, about 0.4%): sort a week of refusals from every job (guard logs, unsettled let-throughs, handover log, chats' "REFUSED") into real fault, wrong block, or waiting for Sam; confirm whether the v5 silent render had a body-check record. This decides change 2 only.

Change 1, finishing tool counts only this film's let-throughs (about 0.4%). Replay test: this film passes; a film with its own let-through is refused. Number to beat: 0 films refused for another job.

Change 2, after learning: the body-check record survives the sound mix, and the animatic command prepares the critique pack (about 0.6%). Replay test: the send guard finds the record after the mix. Number: 0 unchecked animatics handed over.

Change 3, Override (about 1.2%). The message hook logs Sam's message when it contains the whole word "override" (any case); it lasts for that one ask, until his next message. One shared check, used by the send guard, the finishing tool's route stop, the proposal Stop hook, the handover check, the cost watch and the budget stop, confirms the word in Sam's own message in the chat record; a chat-written record fails. Waits for Sam pass. Quality checks pass only with "Checks: not run (your Override): ..." in the message, and run as normal next. Never: fake records, moving a locked shot, a final render without his yes, deleting work or history, skipping saving. Handover lines 291-294 still catch an invented Override; the handover counts Overrides refused and invented. CLAUDE.md line 87 and rule 85 reworded. Replay test: chat 47's video is refused without the word, passes with it, and a chat-written record is refused. Number: 0 Overrides refused, 0 invented.

Change 4, "Locked by Sam" stays in the notes' handover (later chats need it), never in a message to Sam. CLAUDE.md line 20 reworded; the plain-words reply check flags the phrase; Sam's 10:54 words are its saved example. Number: 0.

Question for Sam: may Override send an unchecked animatic, labelled, with the checks following? This changes his line 87. Pick: Y.
## For Sam
### Option 1: Override for waits, and fix the wrong stops
Problem: In chat 47 the film was built but could not be sent. One stop was right (its checks hadn't run); the other was wrong (the finishing step refuses every film while other chats have paperwork left open), and your word "Override" had no way to reach either.
1. The finishing step only looks at this film's own open paperwork, so other jobs never hold your film.
2. When you type "Override", anything that is only waiting for your yes goes ahead for that one request; it only counts if it is in your own message, so a chat cannot fake it.
3. If Override sends you something whose checks haven't run, the message says exactly which ("Checks: not run (your Override): ..."), and the checks run straight after.
4. A week of past refusals is sorted first, then the check results are made to survive the sound step so films stop arriving unchecked.
5. The "Locked by Sam" line stays in the notes for later chats, never in messages to you.
Why: it fixes why the film was stuck for every film, not just this once, and still never passes off unchecked work as checked.
You'd notice: Override gets you the film in that reply, with any unchecked parts named; no more films stuck for other jobs; no Locked line.
Other option: Option 2, one word that skips everything in one go.
Lost: the promise that every video you see has passed its checks (only when you type Override, and each gap is named); the Locked line in your messages.
Added: a record of each Override; one "not run" line when checks are skipped; four separate yes-or-no questions.
### Option 2: One word skips everything
Problem: Your word "Override" only works when a chat is running out of money; everywhere else the stops between you and your film can't hear it, so you waited a whole chat for one video.
1. When you type "Override" anywhere in a message, every stop between you and that request is skipped, once.
2. Each skipped stop is named in the reply; a chat cannot say you typed it when you didn't.
3. Locked shots, deleting work and saving are never skipped.
4. The "Locked by Sam" line leaves your messages.
5. The wrong stop that blocks every film over other chats' paperwork is fixed later, as a separate question.
Why: it does exactly what you asked, in one change.
You'd notice: Override always gets you what you asked for in that reply.
Other option: Option 1, which also fixes why the film got stuck.
Lost: checks you may rely on, whenever you type Override; the wrong stop stays until a later fix.
Added: one record of each Override and one line naming what was skipped.
