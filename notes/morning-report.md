# Morning report (the overnight run, 13-14 Nov)


## Job Q, the handover check (chat 1; done, about 2.2% of a week against 1.5% estimate, under the 2.25% stop)
- **Works:** `source/handover.py` saves each message you type to GitHub as it arrives; at a chat's end and the next one's start it lists any of your notes not written down. On Blessed's real chats it catches all four known drops (N8 pool table, N9 head change, N10 journalists' mics, note 47's face) and passes once they were written: no false alarms. Kittest passes.
- **Decided (Sam: Y, 13 Nov; written in CLAUDE.md):** add one line to CLAUDE.md's handover part ("before the handover: `handover.py end`; first thing in a chat: `handover.py start` on the chat before"); my pick Y, and chats run it from now on under the tool job's rule 86. Cost per film: about $0.10 a chat; saves 2-4% on any film where a chat breaks or drops a note.

## Face tool (ranking item 2; HARD STOP at Sam's 7.5% stop: ~8.2% of a week spent, chats 1-3)
- **Exists:** `source/facepick.py` (three heads A/B/C tuned until the likeness check passes, one sheet) and, new in
  chat 3, `source/agelines.py`: cheek folds, crow's feet, eye bags, forehead and mouth lines MEASURED in the photos
  (depth less plain skin's own reading, so it is fair to every skin tone; times the person's age when given), drawn
  after the check like a beard (the face finder read Burnham's cheek folds as his lips). Soft grey temples on both
  sides (was a hard square on one); braids measured from the photo's hair ripple and drawn as plaits from a parting.
- **Works:** Burnham passes with lines on (71/80/62%, first of 14); Badenoch passes (75/76/73%, first of 14). Name
  test (Burnham, before the age scale): picked first from 6 look-alikes on A only (B, C: Starmer first); named
  unprompted on none. The helpers say: his big dark eyes and heavy brows (the cartoon's eyes are small).
- **Faults named:** Badenoch: a hard band at brow height where the crown lines meet the plaits.
- **Left (~1% of a week):** the Walliams replay (w06, w07, w01, w02; tries vs his five chats); the kittest for
  facepick and agelines (rule 86); the braid band; Burnham's eyes. Sheets sent to Sam: Burnham, Badenoch.
- **Decide:** 1) Burnham A/B/C; 2) Badenoch A/B/C; 3) Y/N ~1% more to finish the left list (pick Y); 4) Y/N rule
  49.3 adds: "Age lines (agelines.py) are drawn after the check too: the face finder reads a cheek fold as the lips."

## Critic bench (ranking item 3, chat 2; done, about 2.1% of a week against 1.5% estimate, under the 2.25% stop)
- **Works:** `source/critbench.py` redraws Blessed's first animatic exactly as you saw it and scores critics against your 12 real notes on it. Plain pictures: Opus caught 5, Sonnet 4. With close-ups of the people added: Sonnet 7, Opus 2 (it spent its answer on acting). Both missed the judge's missing mouth and the neck join every time. Kittest passes.
- **Decide (my picks):** 1) Y: critique packs add a close-up of every person (sheet fault, not wording: misses were too small to see). 2) Y: the critic runs on Sonnet (11 of 24 vs Opus 7, same 19 extras, about 40% cheaper). Lost: the Opus critic. Not switched yet; one film is a small test, so the next chat adds a second Blessed case (animatic 2) first.

## Rounds read a page (ranking item 6, chat 3; done, about 0.75% of a week against 0.5% estimate, at the stop)
- **Works:** `source/page.py` makes one page per film that a notes chat reads instead of the film's code: Blessed's is 8% of its code's size (about 6,600 words-worth against 81,000). For each note it names the exact lines to open (your note 28, the HM Prison officer, goes straight to the officer's drawing). Notes chats now read the page first (written in the notes-round guide). Kittest passes. Also fixed: the handover check had counted helpers' reports as your messages.
- **Waits for items 4, 5, 7 (people, places, moves kits):** then a person, place or move is a description line on the page itself, so most notes change a line on the page, not code; the full "start near 100k" saving comes then. Today's part saves the code reading (Blessed's rounds read ~60-80k of code each). Nothing to decide.


## People from a description (ranking item 4; in progress: chat 4 of the job done, about 2.3% of a week of 8%, stop 12%)
- **Works so far:** `source/people.py` draws a person from about 8 plain lines (height, build, skin, face, haircut, beard, glasses, clothes). Blessed's 16 invented people (judge, both officers, newsreader, three inmates, twelve jurors) redrawn from their lines match the finished film exactly (0.00% of pixels differ on 8 frames). Kittest passes; every old kittest passes (61); no film uses it.
- **Left (chat 4b, Opus medium):** Brand in his four looks, Walliams, the press pack, invented people turning their heads; then the new-beside-finished sheets for you. Nothing to decide yet.
