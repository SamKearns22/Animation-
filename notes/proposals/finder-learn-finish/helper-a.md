# Helper A: finishing the finder-first Learn step

## Leak
The problem file carries a solution: Sam's Yes to "queuing the finish as its own chat" and "several small chats at once" (helper chats reading Milburn). Ignored here.

## Results
- Milburn's 15 chats: 1,281 steps, 791 searches (251 film code, 540 elsewhere; 332 in 51 shared tools), 12 finder calls, 43 finder misses (git `669afe1f:notes/ledger/milburn.json`, my sums). The problem file's 779/248/531/328 is a few rows smaller; the gap is unchecked.
- 17 shared files were searched in 3 or more chats; they hold 253 searches (same source, my sums). This is the cross-chat repeat, known now by file, not by purpose.
- Searching cost about 5.4% of a week of Milburn's 22% (problem file; `story/status.md` for 22%).
- **New fault:** commit `e72cc7ab` (19 Nov, "Milburn real costs") rewrote `notes/ledger/milburn.json` to 17 rows and dropped every chat's search record (0 of 17 rows keep it; checked). The record the problem file points to is gone from the main line.
- Per-search file and pattern (step 4) are recorded only from the next film on; Milburn has none (0 of 15 rows had a list, checked).
- Gap: purpose per search and whether the 17 Nov reminder printed cannot be measured for Milburn without reading about a million tokens of old chats (`notes/proposals/finder-first/learn.md`).

## The real decision
Not "how to read Milburn's chats", but how the whole next film gets a cost-ranked answer to "what was each search for" in every chat, at no reading cost, so the first remedy is chosen on cost. Bigger levers than reading the past: each chat's own record, which is present and free while that chat runs, and the ledger rewrite that is losing records now.

## Root cause
Labelling was planned as a reading job done after the fact, but old records leave the container when a chat ends (`learn.md`). The learning sat outside the point where the data exists. Step 4 already moved file-and-pattern capture to the end of each chat (`source/stepcost.py`, called by the Stop hook); purpose and the reminder were not moved with it. Separately, a later job rewrote the ledger without keeping fields it did not know about.

## Approaches weighed
1. Helper chats read all 15 Milburn chats and label them. Over 1.5% of a week (unchecked); labels are a chat's judgment; about a past film.
2. Sample 3 Milburn chats. Cheaper, still costly; too small to rank six purposes.
3. (Reframe, learn-first) Label every search automatically in each chat's own end-of-chat record, by fixed rules from that chat's own record, plus whether the reminder printed. The next film is measured whole, at no reading cost.
4. Skip learning; take the count-based remedy. Chosen on counts, not cost.
Chosen: 3, after the ledger fault is fixed.

## Proposal
**Learn (changes nothing in the films):**
- L1. Put Milburn's search record back from `669afe1f`, and make the ledger rewrite keep every field it does not change. Enforced by a ledger test that fails if a rewrite drops a field. Bar: 15 of 15 Milburn rows keep their search record.
- L2. Extend the end-of-chat search record: each search gets one of the six fixed labels by rule, with no chat choosing. The rules: same file and pattern earlier in the chat = repeat within the chat; file searched in an earlier chat of this film (ledger) = repeat across chats; error just before it in a process tool = tool fault; notes or guides; a round of Sam's notes = placing a note; otherwise learning a kit while building. Plus: whether the finder reminder printed, and the chat's last 80 words before the search, so a reviewer can check the label. Enforced by the Stop hook, which already runs every chat, and by stepcost's own test. Bar: under 10% of searches unlabelled; the reminder flag present in every chat; the first film's review checks 30 labels against the chats' own words, at least 26 right.
- Ranking: after the next film's first five chats, cost per label from the ledger; the top label goes to the proposal route.

**Change (after, one at a time):** the remedy for the top label only, its own yes and bar, undone alone. A finder test that has failed since 15 Nov (`notes/proposals/finder-first/`) is a fault: fix it before the next film so finder misses are the finder's real ones.

**Cost:** L1+L2 build about 1% of a week, Opus at medium effort (unchecked); running cost nil. Set against 15% a film and against Milburn's 5.4% spent searching.

**Sam would notice:** nothing in the films; a cost-per-purpose line at the next film's review.

## Sam test
Q1: Yes; an expert measures where the data lives rather than buying back lost records.
Q2: The whole next film, every chat, beats one past film read in part.
Q3: Root cause shown; capture runs in the Stop hook, not by a chat choosing; a 30-label check catches wrong labels.
Q4: Four different approaches weighed; this one alone measures everything at no reading cost.
Q5: Nothing in films changes; each step can be undone alone; nothing to trust before the 30-label check.
Q6: Sources named; costs of the build and the 779/791 gap marked unchecked.
Q7: Sized to label every search, not a sample; the cheap trap (counts only) rejected.
Q8: Permanent record and test; reviewed at the next film's end.

## Lost / Added
Lost: Milburn's purposes, never known; one more film's first five chats search as now.
Added: a permanent purpose-and-reminder record in every chat; the ledger's lost search record put back, and guarded.

## Unchecked
Build cost; why 791 differs from 779; that the reminder's line shows in a chat's own record (other hook lines do, checked in this chat); that the rules label at least 90% of searches.
