# Morning report (the overnight run, 13-14 Nov)


## Job Q, the handover check (chat 1; done, about 2.2% of a week against 1.5% estimate, under the 2.25% stop)
- **Works:** `source/handover.py` saves each message you type to GitHub as it arrives; at a chat's end and the next one's start it lists any of your notes not written down. On Blessed's real chats it catches all four known drops (N8 pool table, N9 head change, N10 journalists' mics, note 47's face) and passes once they were written: no false alarms. Kittest passes.
- **Left / decide:** your Y to add one line to CLAUDE.md's handover part ("before the handover: `handover.py end`; first thing in a chat: `handover.py start` on the chat before"); my pick Y, and chats run it from now on under the tool job's rule 86. Cost per film: about $0.10 a chat; saves 2-4% on any film where a chat breaks or drops a note.

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
