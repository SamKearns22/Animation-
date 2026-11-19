# Proposal: Name what is in the unexplained two thirds of each chat's cost

Status: adopted (2026-11-19)

## Problem
Sam's aim is a film within 15% of a week. The tool that splits each chat's cost into kinds of step (searches,
whole-file reads, page tool, routine, renders, pictures) leaves about two thirds of every film's cost as "other",
so nobody can say what most of the money is spent on, or which part could be cut without lowering quality. Even if
every search cost nothing, Milburn would still be far over 15%. The 15 Milburn chats' full records are no longer in
the container; reading them back through the session record is slow and costly.

## Facts
- Units (checked): the ledger's cost column is % of a week, not dollars (notes/ledger/milburn.md: "spent 32.4%").
  Sam's brief wrote it as "$32.40". At WEEK_USD 245 (provisional, .claude/hooks/costwatch.py:26) 32.4% is ~$79.
- Milburn (notes/ledger/milburn.json): 15 chats (11 Opus, 4 Sonnet), 1,281 steps, every row an estimate from the
  transcript (src "estimate"); total 32.4% against an estimate of 24.0%. Sam's own app figure at posting: 22.0%
  (milburn.json "final", src "Sam (app)"). So the transcript estimate ran ~47% above Sam's meter; the kind shares
  are shares of a total that is itself off by about half (cause unchecked: prices, WEEK_USD, or double counting).
- Cost-weighted shares over Milburn (counted from milburn.json kinds x cost): other 66.7%, tool search 16.3%,
  film-file search 8.6%, pictures 5.1%, renders 2.5%, page.py 0.5%, whole-file .py read 0.2%, routine 0.1%.
  Per chat, other runs 58-87%; calls counted as "other" per chat: 2-31.
- How "other" is made (source/stepcost.py, measure(), lines 119-200): each tool result is charged its write plus a
  re-read at every later step; the output that asked for a call is shared among its calls; whatever is left of the
  chat's real cost is added to "other", and calls kind_of() does not name (Edit, Write, Bash running python, tests,
  git, session/GitHub tools, agents) are charged to "other" too. So "other" holds: the context already there before
  step 1 (the app's own instructions and tool list, CLAUDE.md, start-up hook text) re-read at every step; Claude's
  own words and thinking with no call; reminders; and all edits, writes, python runs, tests, git and session calls.
- Prototype split, this chat (19 Nov), a throwaway script in the scratchpad, no tool changed: on
  tests/stepcost-transcript.jsonl (16 steps, $1.31): before-step-1 context 36.8%, tool search 20.9%, edits and
  writes 20.3%, left over 16.8%, python 3.9%. On this chat's own first 13 steps: before-step-1 context 73.6% (83k
  tokens at step 1). Both are short chats; no long film chat has been split this way.
- Earlier split (notes/proposals/startup-reading.md Facts, from notes/cost-diagnosis.md, 13-16 Nov): median Opus
  film chat ~78 actions ending ~220k, ~$5.6: app's own ~80k re-read ~25%, start-up reading ~15%, work history ~25%,
  output ~20%, writes the rest. Startup-reading was adopted 16 Nov (CLAUDE.md condensed); Milburn ran after it.
- Record: ~/.claude/projects holds only this chat's transcript (checked). The ledger stores per chat only steps,
  end history, kind shares and call counts (milburn.json), not the transcript. list_events: two small reads of one
  Milburn chat (session_01J1JB7YBXPnoLsQGLnhHAxi) returned pages with no assistant events; whether its events carry
  per-step token usage is unchecked. Sam's brief: ~10k tokens per 6 steps through list_events, so all 1,281
  Milburn steps is ~2.1M tokens read (at Opus's $8/M write price at least ~$17, ~7% of a week; estimate).
- ledger.py auto (the Stop hook) runs stepcost on every chat at its end (stepcost.py docstring), so any change to
  stepcost measures every new chat from then on at no extra cost.

## Record
notes/ledger/milburn.json
notes/ledger/milburn.md
notes/ledger/protest-tiers.json
source/stepcost.py
source/ledger.py
.claude/hooks/costwatch.py
notes/cost-diagnosis.md
notes/proposals/startup-reading.md
notes/proposals/chat-size-and-model.md
tests/stepcost-transcript.jsonl

## Verdict (the judge, word for word)
<!-- verdict-hash: aff69280c0d67f04 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the title ("Name what is in ... other") frames the answer as relabelling the leftover, and the Facts' "prototype split" and "How other is made" list the very sub-kinds to split it into. It also states, unchecked, that the kind shares are "shares of a total off by about half"; the record (notes/proposals/cost-other/milburn-usage.md) shows the dollar estimate matches the app within 1%, so the gap is the week size, not the shares.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 2 | 3 | 4 | 5 | 18 |
| V2 | 4 | 3 | 4 | 4 | 5 | 20 |
| V3 | 2 | 2 | 3 | 3 | 5 | 15 |
## Sam test
Q1: Yes, as patched: an expert first splits real dollars by where the tokens came from (start-up floor, carried history, new writes, Claude's own output), for the whole film, then cuts the biggest block. Done here on real app figures.
Q2: Whole film, real app dollars for 13 of 15 Milburn chats (milburn-usage.md), plus Sam's own notes count (milburn-review.md: 33 notes, 4 repeats). No costly replay of transcripts.
Q3: Root cause named (stepcost charges only tool results; everything else falls to the leftover). The new split runs by itself at every chat's end, and its test fails unless the parts add to the chat's real cost within 1% with a leftover under 5%, so it cannot pass on paper.
Q4: Five approaches weighed across the versions (more labels, exact split by origin, learn from app figures, replay transcripts, cut now); exact split plus the existing app figures is the best of them.
Q5: One change in this yes, one file, guarded by its test, undone by reverting it. Cuts come later, each with its own yes and number.
Q6: Facts checked: app $74.59 vs ledger $73.84 on 13 chats (milburn-usage.md); 33 notes and 4 repeats (milburn-review.md); WEEK_USD 245 "PROVISIONAL" (costwatch.py:26). Start-up floor share and the two missing chats: unchecked, marked.
Q7: Sized to remove the leftover entirely, not to relabel it; ~1.5% of a week once, stated.
Q8: Permanent once made; reviewed at the next film's end against its numbers.
## Pick
V2
## Why
V2 is the only version resting on measured results: it read the app's real usage for 13 Milburn chats and found the estimate right in dollars, which settles the 47% gap as the week size (already owned by notes/proposals/estimates.md, so not bundled) and gives a real split now (re-read 45%, writes 30%, output 25%). V1 proposes a learning step whose answer is already in the repo and leaves the gap's cause "unchecked"; its strong part is the design of the tool change. V3 gives up the Milburn answer and bundles the gap fix with the labels, and its labels still leave a leftover.
Taken from V1: split each step exactly by token origin (no leftover by design), with a test that the parts add to real cost within 1% and the leftover is under 5%, in place of V2's "leftover under 15%". Taken from V3: no list_events replay. Added by the judge: V2's second change (record each chat's purpose and notes) is dropped from this yes because Milburn review item 5 already proposes the ledger counting notes and repeats; it goes there, not duplicated.
## Faults in the pick
- F1 [fixed] V2's leftover target (15%) let a split pass while still hiding cost; now an exact origin split, leftover under 5%, parts within 1% of real cost (from V1).
- F2 [fixed] V2 put two record changes in one plan; the notes/purpose record moves to Milburn review item 5, so this yes is one change.
- F3 [fixed] V2's learning step re-did work already in milburn-usage.md; it shrinks to adding the start-up floor and fix-chat columns from data in the repo (~0.3%).
- F4 [named] Two Milburn chats (5c55685c, ce8f146c) have no app figure, and step-1 size per Milburn chat is not stored; the floor share for Milburn is an estimate (~90k x steps).
- F5 [named] Sam's 22% may include other jobs run on 17-18 Nov; the week size is settled in the estimates proposal, not here.
- F6 [named] This measures and names; it cuts nothing by itself. The cut comes next, against its measured share.
## Final version
**Learn (changes nothing; Sonnet; ~0.3% of a week).** Add to milburn-usage.md, from data already in the repo: per chat, the start-up floor (step-1 context, ~90k where unstored, marked estimate, x later steps x read price), carried history, writes, output; and each chat's purpose from its title and the notes table (new work, note fix, handover). Result: Milburn's real dollars by block and by purpose, ranked. No list_events replay.

**Change 1 (this yes; Opus medium; ~1-1.5% of a week).** stepcost splits every step exactly by token origin from its usage: the step-1 context re-read (start-up floor, stored per chat), carried history (split by the call that wrote it, with Claude's own words and edits as kinds), new writes, output. It runs at every chat's end through the Stop hook. Its test, on the fixture transcript, fails unless the parts add to real cost within 1% and the leftover is under 5%. Number to beat: leftover under 5% on every chat of the next film (Milburn: 58-87%); three chats checked against the app's figure within 5%.

**Not in this yes.** The week size (estimates proposal); the ledger counting notes and repeats (Milburn review item 5); the cost cut, proposed next against the block the table ranks first, with its own number.
## For Sam
### Option 1: See where every dollar goes, then cut the biggest
The cost meter can't say what two thirds of each chat's money went on. We checked the app's real figures for Milburn: the money is right; the "% of a week" was off because the week's size is still a guess (that is fixed separately). This makes the meter split every step's cost into its real parts (the rules every chat re-reads, past work carried along, new writing, Claude's own words), with nothing left as "other". It runs by itself on every chat. You'd notice one short table of where Milburn's money went, then a cut aimed at the biggest part.
Lost: nothing in the films; about 1.5% of a week once.
Added: an exact cost split on every chat, and Milburn's answer now.
### Option 2: Label the leftover, learn from the next film
Add more labels to the meter's "other" pile and wait for the next film's numbers before deciding anything, without looking back at Milburn. Cheaper to think about, but a leftover pile stays and the answer comes a film later.
Lost: Milburn's answer now; a cut one film later.
Added: more labels on every chat from the next film.
