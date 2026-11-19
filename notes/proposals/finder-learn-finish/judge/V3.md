# Helper B: finishing finder-first's Learn step

## Leak
The problem file hints at its idea: "several small chats at once" reading the old transcripts. I set it aside.

## Results
- Milburn: 15 chats with a search record, 1,281 steps (summed from milburn.json at e72cc7ab~1). 12 finder calls; 251 film-code searches and 540 elsewhere (my sum, 791). The problem file says 779 (248/531), and I could not find where the gap comes from.
- Searching was about 25% of the film's cost, about 5.4% of a week (problem file; Milburn's final cost was 22% of a week, milburn.json `final`).
- **The current milburn.json no longer holds any search record.** Today's real-cost import (commit e72cc7ab, `ledger.py app_import`) carries only `steps, hist_k, kinds, calls` onto the app row and drops `search`. It survives only in git history. Step 4's new record (each search's file and pattern) will be wiped the same way on the next film, at the moment its review needs it.
- **Step 3 (did the 17 Nov reminder print?) can be answered from the ledger, with no transcripts.** `finderwarn.py` (installed 17 Nov 09:06) prints at a chat's first film-code search made before any finder call. 12 of 15 chats made such a search: 8 never called the finder at all (77 hand searches between them) and 4 called it later. So the reminder fired in 12 chats, provided the hook ran, and in 8 of them the chat never once used the finder afterwards. Whether it actually printed and wasn't swallowed by an error is unchecked.
- Reading the old chats: about 10,000 tokens per 6 steps × 1,281 steps ≈ 2.1M tokens (learn.md's figure, scaled by me). Its cost in % of a week is unchecked.
- Milburn's patterns were never recorded (`list` was absent from every row), so even a full read rebuilds them by hand.

## The real decision
The question isn't "how do we read Milburn's dead chats". It's how every film, from now on, gets the reason behind each search, recorded while the chat's own record still exists, so the first finder remedy is chosen on cost and not on counts. Bigger levers than the reading method: (a) the import that deletes the search record, and (b) the record keeping *what* was searched but not *why*.

## Root cause
The learning plan assumed old transcripts could be read later. That was marked unchecked in finder-first.md and turned out false: each chat's record leaves with its container. The Stop hook is the only moment the full record exists. It saved counts, then file and pattern, but never the sentence Claude wrote just before searching, which is the purpose. On top of that, app_import throws the search record away.

## Approaches weighed
1. Helper chats read Milburn's records step by step (about 2.1M tokens). The evidence is stale (the reminder and finder changed mid-film) and the patterns are rebuilt by hand.
2. Skip the labels and take the count-based remedy now. Cheap, but the choice rests on counts, not cost.
3. Reframe: capture the purpose automatically at the Stop hook for every chat, label it at the next film's review, and answer step 3 from the ledger now (learn-first).
4. A small Milburn sample (2 heaviest chats, about 250 steps, about 400k tokens). One film's two chats is narrow evidence, and it's still the old tools.

Chosen: 3. It gives the widest and most current evidence (a whole new film), costs almost no reading, and runs in every chat without any chat having to remember it.

## Proposal
**Learn now (changes nothing):** write the step 3 result above into learn.md, sourced to the ledger and the hook's rule.

**Change 1 (its own yes): stop losing the record.** app_import keeps `search` on the app row, and Milburn's search records are put back from git. Enforced by a ledger test. Number to beat: after the next film's import, 100% of chats with steps still hold their search list (Milburn: 0%).

**Change 2 (its own yes): record why.** stepcost's search record also stores, with each search, the last 120 characters Claude wrote before it. It runs in the Stop hook on every chat, so no chat has to choose to do it. Number to beat: 90% or more of the next film's searches carry a non-empty reason.

**Learn at the next film's review:** one Sonnet chat sorts the about 800 short lines into finder-first's fixed labels, replays 60 searches against the finder, and gives the cost per label in % of a week. Then the finder-first remedies follow, one at a time, ranked by that cost.

**Cost (unchecked estimates):** change 1 about 0.2% of a week, change 2 about 0.4%, review labelling about 0.3%. That's about 0.9% in total, against the plan's 1.5% and Milburn's 5.4% spent searching. Within 15% per film.

**What Sam would notice:** nothing in the films. Two yes/no questions now, then a measured ranking at the next film's review instead of a guess.

## Sam test
Q1 Expert: yes. It instruments the system at source rather than digging through records that are gone.
Q2 Best result: a whole new film with patterns and reasons beats one old film without either.
Q3 Comprehensive: automatic in the Stop hook, held by a test and two measured numbers. Weak spot: the labelling is still done by a chat, so it's checked by the replay.
Q4 Intelligent: four different approaches weighed; this is the only one that fixes the record loss.
Q5 Risk: each change can be undone alone and doesn't touch the films. The risk is the remedy coming one film later.
Q6 Checked: sources named. Costs and the reminder actually printing are marked unchecked.
Q7 Not cheap: it's sized to get the full purpose evidence, not to dodge the reading. Skipping the reading is a result of better evidence, not a saving for its own sake.
Q8 Nothing temporary: both changes are permanent and reviewed when the film is done.

## Lost / Added
Lost: Milburn's search purposes, for good, and the remedy waits one film (about 5% of a week of searching may repeat).
Added: a search record that survives the cost import, a reason on every search in every film, and the reminder answer now.

## Unchecked
Whether the reminder printed (and wasn't swallowed by an error) in the first 17 Nov chat. The 779 vs 791 gap. All costs in % of a week. Whether 120 characters of Claude's text is enough to tell the purpose (the review's replay tests this).
