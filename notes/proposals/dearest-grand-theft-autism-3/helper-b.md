# Helper B: memory lapses on grand-theft-autism

## Leak
None. The problem file states a cost and a question, no solution.

## Results
- Total: 3.11% of a week on lapses, out of 54.67% for the film (source: `source/dearest.py grand-theft-autism`; I re-added each chat's split in `notes/ledger/grand-theft-autism.json` and got 3.11).
- They are bunched up, not spread out. One chat (caff6f5e, 20 Nov, Opus, 138 steps, 302k of history at the end) cost 1.52%, half the total. Next come c079f576 at 0.46%, 423495d7 at 0.40%, 78cd6210 at 0.27% and 77034bac (Sonnet) at 0.24%. The other three cost 0.01 to 0.11% each (source: the ledger .json).
- All 8 chats ended with big histories (186k to 302k). Each had 3 to 22 renders (source: the ledger .json, `hist_k` and `calls.renders`).
- Notes and faults: the ledger shows 0 notes from Sam on this film, so no lapse can be linked to a fault that reached him (source: `notes/ledger/grand-theft-autism.md` line 5).
- Across the week the figure was 4.22% in 11 chats (source: `notes/proposals/dearest-week.md`).
- **Gap: the record does not say why any lapse happened.** `source/stepcost.py` (around line 474) counts a lapse whenever a step writes more than the chat grew. It keeps no record of the time since the last step, or of what the chat was waiting for (a render, Sam, a helper). So we cannot yet tell a lapse caused by time running out from one caused by something else, and that is the cause the remedy depends on.

## The real decision
The question is not "how to make one cost line cheaper". It is this: across the whole chain of chats in a film, where does a chat sit idle while carrying a big history, and what decides the price of that idle time? A lapse costs about the size of the history times the price of writing it again. That makes two levers bigger than the lapse itself: how big the history is when the chat waits, and whether that waiting happens inside a big chat at all.

## Root cause
Most likely (unchecked, because the gap above hides the timings): Claude's short-term memory of a chat (the "cache") expires after a few minutes of silence. Then the next step pays again to re-read the whole history at the dearer writing price. The record fits this. The dearest chat was the longest and largest, and lapses only show up in chats that ran renders. The rule "one wait per render" means a chat sits silent through each render. A chat that waits with 300k of history pays about 300k tokens again per long wait. The only guard so far is the "back after more than an hour" handover rule in CLAUDE.md. It only covers gaps over an hour on amber or red, so the shorter waits during renders fall outside it. A cause other than time is also possible, such as a change at the start of the chat breaking the memory, and only the timings can rule it out.

## Approaches weighed
1. **Learn first: time every lapse.** Have the cost tool record, for each lapse, the gap in minutes and what came just before it (a render, Sam's reply, a helper's report). Read that across the 11 lapse chats of the week. This changes nothing about how films are made.
2. **Reframe: wait while the history is small.** Put long renders where the history is small: at the start of a fresh chat, or after a handover. A big chat would never sit idle.
3. **Keep the memory alive longer.** Use the longer one-hour memory, if the tools allow it here (unchecked). Each write costs more, but there are far fewer lapses.
4. **Shorten the waits.** Faster or chunked renders, so no silence lasts long enough for the memory to expire.

Choice: 1 first, because each of 2 to 4 fixes a different cause, and only the timings show which cause is real. After that, exactly one of 2, 3 or 4, whichever the timings point to.

## Proposal
**Step A (learning; changes nothing).** Add to the cost tool's split, for every lapse, the gap before it and what the chat was waiting for. Show it as one line per chat in the ledger. Its test is a made-up chat with a known 10-minute gap before a render, which it must label correctly. Then run it on the week's 11 chats and write down how lapse cost splits by cause. Done when every lapse in the week has a cause, with none listed as unknown. Cost: about 1 to 2% of a week, once.

**Step B (one change, chosen by A's result).**
- If render waits cause most of it: the handover check flags any wait longer than the memory lasts in a chat whose history is over about 150k, and the chat hands over before the render, not after.
- If Sam's gaps cause most of it: the existing "back after more than an hour" rule is widened to cover the memory's real lifetime.
- If neither: approach 3 or 4, put to Sam on its own.

Number to beat for Step B: lapses below 1% of a week per film, against 3.11% now, measured by `dearest.py` at the next film's end with nothing else changed. It is reviewed at the film-end review and undone alone if it misses. Sam would notice nothing in the films. He would see one cost line shrink, and B would come back to him as its own question.

## Sam test
- Q1 Expert: an expert measures the timing of cache misses before fixing them. That is what Step A does.
- Q2 Best result: A uses the whole week (11 chats), not only this film.
- Q3 Comprehensive: A finds the root cause. B's fix lives in the handover check, so it does not depend on a chat choosing to follow it. B is measured against 1%.
- Q4 Most intelligent: four different approaches were weighed, and the choice between them is left to the evidence.
- Q5 Risk: A changes nothing, and B can be undone on its own.
- Q6 Checked: sources are named; the cause is marked unchecked.
- Q7 Not cheap: A measures every lapse, not a sample.
- Q8 Nothing temporary: A is a permanent part of the cost tool, and B is a permanent change or none at all.

## Lost / Added
Lost: nothing. Added: a cause and a gap on each lapse in the cost record; later, one check or rule change, decided by its own yes from Sam.

## Unchecked
- That the memory expiring after a silence is the cause.
- Whether a one-hour memory is available in these chats, and what it costs.
- The timings of the gaps themselves.
