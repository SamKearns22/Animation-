# Proposal: How the unfinished Learn step of finder-first gets finished

Status: open

## Problem
Sam adopted "finder-first" (18 Nov): first learn what Milburn's 779 hand searches were for, then fix one cause at a
time. The learning part is unfinished. To say what each search was for (steps 1-3), the chats' own transcripts are
needed; only a chat's step-by-step record, read through a tool, is left, and it is costly to read (about 10,000
tokens per 6 steps; the 15 Milburn chats hold about 1,300 steps). Without it the ledger gives counts per file but not
the purpose of each search, and not whether the 17 Nov reminder was shown. The question is how to get the measured
result, or whether to go on without it.

## Facts
- notes/proposals/finder-first/learn.md: step 4 (record each search's file and pattern on the ledger) done and pushed;
  steps 1-3 not done; transcripts of the 15 chats gone; reading all inline is "well over a million tokens".
- notes/ledger/milburn.json: searching $8.04 of $32.14 (25%, about 5.4% of a week, estimate); 779 searches, 248 on
  the film's code, 531 elsewhere (328 shared tools, 101 other, 81 notes, 21 guides); finder used 12 times.
- notes/proposals/finder-first.md: plan allowed about 1.5% of a week for the Learn step.
- Sam, 19 Nov: said Yes to queuing the finish as its own chat.
- A code-finder test (round_page) fails since 15 Nov and one head check since 14 Nov (see notes/proposals/finder-first/).
- Unchecked: the real cost of reading with several small chats at once; whether purposes can be told from the search
  text alone, without reading the chat around it.

## Record
notes/proposals/finder-first/learn.md
notes/proposals/finder-first.md
notes/ledger/milburn.json
source/stepcost.py
source/page.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 66a56cd8f732efd2 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the Unchecked line names "the real cost of reading with several small chats at once", which is the helper-chat idea of learn.md, and "Sam said Yes to queuing the finish as its own chat" frames the answer as a reading chat. It leans the helpers toward reading Milburn's old chats.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 3 | 2 | 3 | 4 | 15 |
| V2 | 4 | 4 | 4 | 3 | 4 | 19 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
## Sam test
Q1: Yes. An expert records the reason at the one moment it exists (the end of each chat) and stops the record being thrown away, rather than paying about 2 million tokens to rebuild one past film by hand.
Q2: A whole new film, with file, pattern and reason on every search, is wider and more current evidence than Milburn (old reminder, old finder, no patterns). The reminder question is answered now from the ledger.
Q3: Root cause shown with evidence: the cost import keeps only steps, history, kinds and calls (checked in the ledger code) and 0 of 17 current Milburn rows keep a search record (checked). Capture runs in the end-of-chat hook, not by a chat choosing. Weak spot: the labelling at review is done by a chat; fixed by tying it to the review check and cross-checking against rule labels.
Q4: Four different approaches weighed (read all, sample, record at source, skip learning); recording at source is the only one that also fixes the loss.
Q5: Two separate yeses, neither touches the films; each undone alone. Real cost of the wait: one more film searches as now (about 5% of a week).
Q6: Checked here: 15 rows, 1,281 steps, 791 counted searches (251/540, 332 shared), 12 finder calls, 12 of 15 chats searching film code before any finder call, 8 of them (77 searches) never using it. Unchecked: whether every Milburn chat ran after the reminder was installed (17 Nov 09:06), the 779 vs 791 gap, all % costs.
Q7: Sized to label every search of a whole film, not a sample; the count-only remedy (the cheap trap) is rejected.
Q8: Both changes permanent with tests; the ranking is reviewed at the next film's end.
## Pick
V3
## Why
V3 and V2 both found the bigger fault the problem missed: the 19 Nov cost import wiped Milburn's search record and will wipe the next film's too (confirmed: the import copies only four fields; 0 of 17 rows keep "search"; the record survives in git). Both move "why" capture to the end-of-chat hook, where the data exists. V3 wins because it splits the two changes into two yeses (V2 bundles them), and it answers the reminder question now from the ledger (checked: the numbers hold). V1 answers the problem's wording, pays to read a stale film, and misses the wiped record.
Taken from V2: keep about 80 words before each search (120 characters is likely too short to tell a purpose); rule-based pre-labels stored beside the text as a cross-check, with a 30-label spot check; fix the code-finder test failing since 15 Nov before the next film, so finder misses are real.
## Faults in the pick
- F1 [fixed] 120 characters of text may not show the purpose; raised to about 80 words.
- F2 [fixed] Review labelling relied on a chat choosing to do it; now part of the film's review check, cross-checked against rule labels (at least 26 of 30 agree).
- F3 [fixed] The failing finder test would make finder misses unreliable; fixed before the next film.
- F4 [named] The reminder answer is inferred from the reminder's rule and the counts, not seen printed; and not checked that every Milburn chat ran after 17 Nov 09:06.
- F5 [named] Milburn's purposes are lost for good; the first remedy waits one film (about 5% of a week of searching may repeat).
- F6 [named] 779 vs 791 searches gap unexplained; all costs unchecked estimates.
## Final version
Learn now (changes nothing): write into the Learn notes that the reminder's rule fired in 12 of 15 Milburn chats and in 8 of them the chat never used the finder afterwards (77 hand searches), sourced to the ledger in git and the reminder's rule; mark "printed" as inferred and the install-time check as open.

Change 1 (own yes): stop losing the record. The cost import keeps every field it does not change, including the search record; Milburn's 15 search records are put back from git. A ledger test fails if an import drops a field. Bar: 15 of 15 Milburn rows hold their record; after the next film's import, 100% of chats with steps keep theirs.

Change 2 (own yes): record why. The end-of-chat hook, which runs in every chat, stores with each search the last about 80 words Claude wrote before it, plus a rule label (repeat in chat, repeat across chats, tool fault, notes or guides, placing a note, learning a kit) and whether the reminder printed. Its own test holds it. Bar: at least 90% of the next film's searches carry text; reminder flag in every chat.

Before the next film: fix the code-finder test failing since 15 Nov.

At the next film's review (part of the review check, Sonnet): sort the lines into the fixed labels, compare 30 with the rule labels (at least 26 agree, else the rules are corrected), replay 60 searches against the finder, give cost per label in % of a week. The top label's remedy goes through the proposal route, one at a time.

Cost (unchecked): change 1 about 0.2% of a week, change 2 about 0.5%, review about 0.3%; about 1% in all, against Milburn's 5.4% spent searching.
## For Sam
### Option 1: Record the reason as each chat ends
A bug found: a tidy-up on 19 Nov threw away Milburn's record of what was searched, and would do the same to every film. First fix that and put Milburn's back. Then, at the end of every chat, the computer itself writes down the few sentences before each search, which say what it was for. At the next film's review one chat adds them up and says which kind of search costs most; that gets fixed first. Two separate yes/no questions; nothing in the films changes.
Lost: why Milburn's searches happened, for good; the fix for searching waits one film (about 5% of a week may repeat).
Added: a search record that is never thrown away, the reason behind every search in every film, and the reminder question answered now.
### Option 2: Read Milburn's old chats with helper chats
Several cheaper chats each read about 3 of Milburn's old chats and write what each search was for; then the fix is chosen straight away. The reading is large (about 2 million words' worth), the film used older tools, and the record-loss bug stays unless fixed separately.
Lost: about 1.5-2.5% of a week of reading (not measured), on evidence from an older setup.
Added: a measured answer for Milburn now, without waiting a film.
