# Morning report (the overnight run, 13-14 Nov)


## Job Q, the handover check (chat 1; done, about 2.2% of a week against 1.5% estimate, under the 2.25% stop)
- **Works:** `source/handover.py` saves each message you type to GitHub as it arrives; at a chat's end and the next one's start it lists any of your notes not written down. On Blessed's real chats it catches all four known drops (N8 pool table, N9 head change, N10 journalists' mics, note 47's face) and passes once they were written: no false alarms. Kittest passes.
- **Decided (Sam: Y, 13 Nov; written in CLAUDE.md):** add one line to CLAUDE.md's handover part ("before the handover: `handover.py end`; first thing in a chat: `handover.py start` on the chat before"); my pick Y, and chats run it from now on under the tool job's rule 86. Cost per film: about $0.10 a chat; saves 2-4% on any film where a chat breaks or drops a note.

## Face tool (ranking item 2; HARD STOP at its 150% budget: ~5.3% of a week against 3% estimate, stop at 4.5%)
- **Exists:** `source/facepick.py`: from a likeness pack, one command draws three heads (A, B, C), each tuned until
  the likeness check passes, on one sheet beside the photos at phone size. Chat 2 fixed the six faults: the tuning
  now aims at the photo the check judges and is a search the check's own rule scores (the face finder reads cartoons
  jumpily, so step-by-step tuning never settled); glasses sized by the cartoon's eyes; hair in two colours (grey
  temples) with strand lines; calmer skin; a line-up of 14 people from every film; a drawn neck; the sheet fixed.
- **Works:** Burnham's three heads pass the check (68%, 77%, 71%; none the wrong way; first of 14), 2.5 min a person.
- **Left:** by eye Burnham still reads young and round (no cheek folds or crow's feet; no kit piece draws them, new);
  the name test, Badenoch (braids), the Walliams replay, the kittest, sending you the three sheets. About 2% more.
- **Decided (Sam, 13 Nov):** "another 100% to the budget. Continue": stop now 7.5%; face chat 3 (Opus high) opened.

## Critic bench (ranking item 3, chat 2; done, about 2.1% of a week against 1.5% estimate, under the 2.25% stop)
- **Works:** `source/critbench.py` redraws Blessed's first animatic exactly as you saw it and scores critics against your 12 real notes on it. Plain pictures: Opus caught 5, Sonnet 4. With close-ups of the people added: Sonnet 7, Opus 2 (it spent its answer on acting). Both missed the judge's missing mouth and the neck join every time. Kittest passes.
- **Decide (my picks):** 1) Y: critique packs add a close-up of every person (sheet fault, not wording: misses were too small to see). 2) Y: the critic runs on Sonnet (11 of 24 vs Opus 7, same 19 extras, about 40% cheaper). Lost: the Opus critic. Not switched yet; one film is a small test, so the next chat adds a second Blessed case (animatic 2) first.

## Rounds read a page (ranking item 6, chat 3; done, about 0.75% of a week against 0.5% estimate, at the stop)
- **Works:** `source/page.py` makes one page per film that a notes chat reads instead of the film's code: Blessed's is 8% of its code's size (about 6,600 words-worth against 81,000). For each note it names the exact lines to open (your note 28, the HM Prison officer, goes straight to the officer's drawing). Notes chats now read the page first (written in the notes-round guide). Kittest passes. Also fixed: the handover check had counted helpers' reports as your messages.
- **Waits for items 4, 5, 7 (people, places, moves kits):** then a person, place or move is a description line on the page itself, so most notes change a line on the page, not code; the full "start near 100k" saving comes then. Today's part saves the code reading (Blessed's rounds read ~60-80k of code each). Nothing to decide.

