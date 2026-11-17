## Leak
Hints at two remedies (shared tools on the finder; mending the day-wide flag). Set aside; judged on evidence.

## Results
- 16 Nov, 19 Opus chats, 35.18% of a week. Film-file search 6.65%, other searches 3.22%, finder 0.21% (ledger `kinds`, notes/ledger/protest-tiers.json, re-added). **Hand searching was 28% of their cost, measured.**
- Calls: 484 film-file searches plus 407 others, against 21 finder calls (ledger `calls`). Per call they cost about the same: a search ~0.014%, a finder call ~0.010%. **So "46 times" counts how often each was used, not a price gap.** The finder saves only where one call replaces several searches.
- "Tool search" is not "shared tools". It counts any search outside the film's files: notes, guides, logs, git output (stepcost.py kind_of).
- **The record cannot measure the adopted bar.** No ledger row in any film has `notes` or `round` filled in. The finder log has no chat column. handover-end.log stores only time and chat id, never fault lines (handover.py end_stamp), so "never fired" cannot be read from it. By its logic, the 09:15 show silenced it all day.
- 16 Nov held about 100 ticked note lines, many of them new action (archive/protest-tiers.md). The finder says where, not how.

## The real decision
How round chats find and understand the code for each note, at the lowest cost per note and no drop in quality. Bigger levers: results re-read every later step; reading to build; checks at the moment of search.

## Root cause
1. Use is asked in text only (job pack line 38, start reminder). The only check runs at handover, after the cost, per day.
2. Even when used, show answers "where". Build-heavy notes need "how", so reading by hand follows. Change 2 is unbuilt.
3. The record does not tie searches to notes or to finder calls, so which of these drives the 28% is unknown.

## Approaches weighed
A. A hook that refuses a chat's first film-file search until show has run in that chat. Capped by show's unknown hit rate.
B. Reframe: a side reader does the code-reading and returns only the needed lines, so they are not re-read ~50 times. Quality and cost unproven.
C. Reframe: build each film's code so a note lands in one small named place (a section per shot, shot tables).
D. Shared tools on the finder (the leak). No number behind it.
E. Learn first: make the record say which of A-D pays.
Choice: E, then the one change its result names.

## Proposal
**Learn (no film change, about 0.6% of a week).** Automatic: the Stop hook (the automatic step that runs when every chat ends) already runs stepcost on every chat. It adds to each ledger row:
- notes ticked by that chat ("[x]" lines its commits add to the film's notes);
- film-file searches split into: before the chat's first show / within 10 calls after a show (a miss) / in a chat with no show;
- other searches split by target: shared code / notes and guides / other.
The finder log gains the chat id. Read after the next film's first round day.

**Then ONE change, with its own yes, chosen by the biggest share:**
- mostly no show in the chat → A, per chat;
- mostly after a show → finder change 2, as adopted;
- mostly shared code → D;
- mostly reading to build → C, at the next build stage.

**Number to beat:** hand-search share of round-chat cost, 28% → under 15% (stepcost), with film-file searches per ticked note falling from the first measured round. Repeated notes (rule 30) must not rise.
**Cost:** about 0.6% to learn, 0.7-1.5% for the change. A round day like 16 Nov would save about 4.5% of a week (estimated).
**Sam would notice:** nothing in films; later one report and one fix to answer.

## Sam test
Q1 Expert: measure the driver; enforce by hook, not text.
Q2 Best result: whole round days, every chat, not one tool.
Q3 Comprehensive: automatic in every chat; root cause and own number.
Q4 Most intelligent: five distinct approaches, two of them reframes.
Q5 Risk: learning changes no film; removable alone.
Q6 Checked: ledger figures re-added, gaps listed.
Q7 Not cheap: sized to the measured 28%; reaches code layout if pointed there.
Q8 Nothing temporary: permanent, reviewed at film completion.

## Lost / Added
Lost: nothing in the films.
Added: four automatic measures per chat, and later one change with its own yes.

## Unchecked
- Show's hit rate on the 16 Nov notes.
- Notes fixed per chat (~100 lines is rough).
- What the "tool search" calls targeted.
- Whether the old 30%-of-steps count matches the stepcost kinds.
- The ~4.5% saving.
