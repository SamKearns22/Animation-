## Leak
yes: the title "finder-first" and the headline "about 65 times for every finder use" frame the fix as more finder use, which points helpers at forcing the finder. The body states no fix outright; the facts list does show the 531 non-film searches the finder cannot read, which lets a careful helper escape the frame (V2 and V3 did).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 2 | 4 | 12 |
| V2 | 4 | 3 | 3 | 3 | 4 | 17 |
| V3 | 4 | 3 | 4 | 4 | 5 | 20 |
## Sam test
Q1: Yes. An expert records what each search asked before building a locator, then removes the repeat look-ups at their source; V3 does that and does not add a third reminder.
Q2: Scope is the whole film: all 15 Milburn chats, all 779 searches (film code and the 531 elsewhere), with Protest Tiers as the comparison. It is the right evidence because it asks what the searches were for, which the ledger cannot say.
Q3: Root cause is evidenced from the hook's own text ("Building something new may search on purpose; then carry on", checked) and the ledger (silent for 68% of searches and after any first finder call). The record is written by stepcost from transcripts in every chat, and each later remedy is enforced by hook or kittest, not by reading. Weak spot: the learn step itself is a chat's labelling job; patched by a fixed label list and the replay count, checked by the judge of the results.
Q4: Five different approaches weighed, two reframes (carry knowledge between chats; fix the tools whose faults send chats into their code) that the other versions lack.
Q5: The learn step changes nothing in the films; every later change is its own yes, own bar, undone alone. Sam is not asked to trust any remedy before the replay shows it would have answered the searches.
Q6: Figures re-summed by me from milburn.json and match (779, 248/531, 328 over 49 shared files, handover.py in 12 of 15 chats, 12 finder uses, 8.04 of 32.14 points, about 24 points with zero search). Unchecked and marked: whether the reminder printed, real app costs, whether old transcripts still hold every tool input.
Q7: Sized by the 8 estimated points it targets and judged on the whole film's search share, not finder counts; it says plainly that search fixes alone cannot bring Milburn to 15%. Not the cheap version: the remedy waits for evidence rather than being skipped.
Q8: The per-search record is permanent from the first yes; each remedy is permanent once said yes and reviewed at film completion. Nothing is a trial.
## Pick
V3
## Why
The real decision: how every chat of a film gets the fact it needs (a note's lines, a kit's workings, what a fault means) in one step, across all code, judged on the film's search share. It should rest on the Milburn ledger's per-chat search split (checked) and on what each search asked (not yet measured). The smallest thing that reaches the result: record what each search asked, then build only the remedy that carries most of the cost.

V1 answers the wording: a hard gate on film code touches 32% of searches, blocks legitimate building, and bundles three changes into one yes before any evidence. V2 diagnoses well and its redirect hook (a search answered by the locator in its place) is the strongest enforcement idea, but it pre-commits to the shared-tool map and the redirect hook and to a purpose label that a chat has to decide. V3 learns first, records file and pattern automatically for every later film, names the cross-chat repeat (handover.py searched in 12 of 15 chats), and lets the evidence choose one remedy at a time. Taken from V2: the redirect form of enforcement (the hook answers the search instead of refusing it), the shared-tool maps kept current by a kittest, and the per-chat bars for film-code searches and finder misses.
## Faults in the pick
- F1 [fixed] V3's kit gate refuses a search once; V2's redirect (give the answer in the search's place, let it through when there is none) never blocks building. The final version uses the redirect.
- F2 [fixed] V3 reads transcripts through `list_events`, unchecked; stepcost already reads tool inputs from transcript files. The final version uses stepcost and falls back to `list_events` only for chats whose file is gone.
- F3 [fixed] Bars added for film-code searches per chat (under 5, Milburn 16.5) and finder misses (under 1 in 5 calls, Milburn 43 in 12), from V2.
- F4 [named] Milburn had no notes rounds, so the finder's own bar for rounds stays untested; the learn step cannot measure note-fixing searches it does not have.
- F5 [named] Search fixes alone cannot bring a Milburn-like film within 15%: with zero search cost it would still sit near 16% of a week (estimate).
- F6 [named] About 1.5% of a week is spent before any fix; Sam wanted this fixed first.
## Final version
**Learn (its own yes; changes nothing in the films; about 1.5% of a week; Sonnet).**
1. Read the search calls of all 15 Milburn chats through stepcost (transcripts; `list_events` only where a transcript is gone). Label each by the question it asked from a fixed list: place a note / learn a kit while building / a process tool's fault / repeat within the chat / repeat of an earlier chat's look-up / notes or guides.
2. Replay 60 (30 film code, 30 shared tools) against the finder as it is and against a draft map of the shared tools; count one-step answers.
3. Record whether the 17 Nov reminder printed in each chat.
4. Permanently: stepcost writes each search's file and pattern on the ledger row, so every later film reports the split at its review without a labelling chat.
Output: cost per label and per remedy, in % of a week.

**Then one remedy at a time, each its own yes, bar and undo, chosen by the largest cost the labels show:**
- Kit learning and cross-chat repeats: the finder also covers the shared tools by their maps; a kittest fails when a function has no map line; a hook answers a hand search with the finder's result in its place, and lets the search through when the finder has no confident answer (building is never blocked). Replaces the 17 Nov reminder.
- Process-tool faults: the named tools print cause and fix with every fault; a kittest checks every fault line carries a fix.
- Note-placing misses: fix the finder on the missed notes.

**Bars, measured by stepcost at the next film's review:** search cost under 10% of film cost (Milburn 25%) and under 1.5% of a week; film-code hand searches under 5 per chat (16.5); finder misses under 1 in 5 calls (43 in 12); no shared file searched in more than 2 chats (handover.py: 12).

**Cost:** learn 1.5%; each remedy 0.5-3%, against about 5.4% of a week spent searching in Milburn (Sam's reading). All reviewed at film completion.
## For Sam
### Option 1: Find out what the searches were for, then fix the biggest
Chats spend about a quarter of the film's cost hunting through files, and two thirds of that is in shared tools the code finder cannot read. First one cheap chat sorts every Milburn search by what it was looking for, and from then on every film records this by itself. Then I bring you one fix at a time, the one that saves most, each with its own target. You would notice nothing in the films, a short search line at each film's review, then one fix to say yes to.
Lost: about 1.5% of a week before any fix lands.
Added: a permanent record of every search; later, one fix at a time.
### Option 2: Build the wider finder now
The finder is extended to read the shared tools too, and when a chat starts hunting by hand, it is handed the finder's answer instead (it can still search if the finder has nothing). Faster to a fix, but built before we know whether the searches were the kind it can answer.
Lost: the 17 Nov reminder; about 6% of a week, partly at risk if the guess is wrong.
Added: maps of the shared tools kept up to date by a check; automatic answers in place of hand searches.
