# Cost spike: fix proposal (Sam's weekly spike analysis, 27 Nov)

Status: BUILT 27 Nov (Sam said Y to both). Results, what is solved and what is not: notes/cost-spike-fix.md.

## What I measured in this chat (27 Nov), not guessed
- A fresh chat's very first step already carries about 85,300 pieces of text (25,346 newly stored + 59,953 re-read;
  about 64,000 words). Our own rules file (CLAUDE.md) is about 4,600 pieces of that. The other ~80,000 is the app's
  own tools and instructions, which the repo cannot trim. (I cannot run /context from here; this is read from the
  chat's own usage record.)
- Cache lifetime here is one hour, not five minutes (all 25,346 stored pieces are the one-hour kind).
- Code size: 318 files, 199,491 lines, 8,297 top-level functions/classes. 63k lines are film code, 136k shared.
  28 files are over 1,500 lines; the checks file alone is 7,341.
- A full exact index (every function, who calls it, which file) builds in 7.7 seconds with plain Python and zero
  chat cost. 142 of 318 files have a MAP at the top; the other 176 do not.
- Only 301 functions (6,094 lines, 3%) are named nowhere else. Deleting dead code will not fix this.
- Reading model: a chat reads (85k + 1.5k x step) at every step. 140 steps = about 26.6M pieces read; the app log said
  about 27M for chat 30. So the model fits. Of that, 45% is the 85k floor re-read, 55% is the growing history.
  Four notes in one chat: 35 steps/note (140 steps) = 26.6M; 18 steps/note (72) = 10.0M (-62%); 12 steps/note
  (48) = 5.8M (-78%).
- Price table vs the app's real bills on 88 chats: Opus total within 6% (379 vs 358 dollars); Sonnet 28% low
  (54.5 vs 75.5). So the prices are NOT the main reason chat 36 read $4.71 against $12.50. The likely cause is calls
  the log cannot see (helper chats, restarts, a model switch). I cannot confirm: chat 36's record is not here.

## Why the existing finder (page.py show) did not stop the searching
It guesses from the words of a note and returns about 40 lines. It does not answer the question a fix really asks:
"if I change this, what else uses it, and which checks must I rerun?" So chats fall back to searching and tracing by
hand. It is also not told when to stop, and nothing counts steps per note.

## Proposal (numbered steps)
1. **Exact "who uses this" tool** (`source/touch.py NAME`). Built from the real code structure, rebuilt at session
   start (about 8 s, free) and checked at handover so it is never out of date. For a function/table: where it is
   (file:line), what calls it (film code and shared code, apart), and which checks cover it, in about 20 lines.
   Replaces the search loop. Never read whole (the full list is about 150k pieces).
2. **"What to rerun" line** from the same index: after an edit, name the few checks that touch the changed
   functions (kit test names), so a fix is not traced by hand through the 236 checks.
3. **Step counter per note.** At 12 steps on one note a one-line prompt: "say what is stuck"; at 20, stop and report.
   Kit test: a log of a chat that overruns triggers the prompt. (Not a hard cut: finishing a fix stays allowed.)
4. **One-page fix pack** (about 2,000 pieces): Rules that bite, the Locked line, the two commands above. Fixing
   chats read this, not the guides. Cuts the quarter-to-third spent reading rules before work.
5. **MAP on the other 176 files**, generated automatically, plus a check that stops a new big file without one.
   Then split the 28 files over 1,500 lines by topic, starting with the checks file (7,341 lines).
6. **Model lock at the source.** Every create_session call in the chain passes the model explicitly; a chat that
   finds itself on a different model than its handover names stops and opens the right one. (Rule exists; add the
   check that the animatic chat's switch would have tripped.)
7. **Real-cost warning.** At each chat's end the ledger records the app's own figure and flags any chat where the
   ledger's estimate is more than 25% under it; helper chats and restarts counted separately.

Lost: nothing Sam has seen. Added: one tool, one counter, one short pack (steps 1-4); steps 5-7 are tidy-up.
Expected: 10-18 steps a note instead of ~35; reading per 4 notes down 60-78% (from the model above, to be checked on
the next film).

## Google's suggestion, checked
- Check the 85k start: done, above. Google's 15-25k figure does not match this app; the project's own part is ~4.6k.
- Static map file: already exists in part (page.py, codemap.py, MAP lines). A flat file would be too big to read;
  needs to be a lookup tool (step 1). Worth keeping: the idea of exact index, free of chat cost.
- `--max-turns`, `claude --model`, `total_cost_usd`: command-line only; Sam works from the phone app, so unusable.
  The equivalents here are step 3, the model passed to create_session, and the app's figure (step 7).
- 5-minute cache and "keep top static": wrong/moot here (one-hour cache; each chat already has its own start).
- Batch notes in one warm chat: right, and matches step 3's saving, but longer chats grow the history cost; best is
  fewer steps per note.

## Needs Sam
1. Y/N: build steps 1-4 first (my pick: Y; Opus, high effort, one chat, tested on the next film's notes).
2. Y/N: steps 5-7 afterwards.
Locked by Sam: no shot, camera or beat is touched by any of this.
