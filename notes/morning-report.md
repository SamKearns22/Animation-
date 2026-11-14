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


## People from a description (ranking item 4; done, chats 4, 4c, 4d: about 6.8% of a week against 8%, under the 12% stop)
- **Works:** `source/people.py` draws a person from about 8 plain lines and a crowd from one block: Blessed's 16 invented people, Brand in all four looks, Walliams (test only) and the whole press pack (31 journalists from 16 lines) match the finished film exactly (0.00% on 13 frames). New: every invented person now turns with their own face, haircut and beard (before, the side and back were a plain stand-in head). Every old kittest passes; no film uses it. Sheets: `notes/morning/people-kit-replicate.jpg` (finished beside kit), `people-kit-cast.jpg` (everyone at five turns), `people-kit-changes.jpg` (the 3 frames that change). Cost per film once approved: a new person ~10 lines, a crowd ~16 (Blessed's cast code 1,661 lines -> ~250 lines).
- **Decide (my picks):** 1) Y: invented people turn with their own face (changes 2 Blessed frames: the officer in the corridor, inmate 2 in the TV room; their heads are now the size of their own front heads, bigger than the old stand-ins; inmate 2's beard reads as a dark patch when he looks down: look at the changes sheet). 2) Y: each journalist keeps their own hair colour (the film had copied some; the gates shot changes 0.5%). 3) Y: approve the kit for the next film. Left: the judge's wig from the side (he is bald there, as in the film); Walliams' turned head.

## Places from a description (ranking item 5; done, chats 5, 5b, 5c, 5d: about 7.1% of a week against 8%, under the 12% stop)
- **Works:** `source/places.py` draws a place from plain lines: Blessed's 13 sets (court outside, courtroom x4, prison gates, van, cell, cot, phone room, TV room, TV) redrawn from 162 piece lines and match the finished film's paintings and 12 frames within 0.004% (bar 0.05%; sheet `notes/morning/places-kit-replicate.jpg`). Cost per film: Blessed's sets took 1,491 lines of code; the same places are 226 description lines, and a note on a place now finds its one line on the page.
- **Found:** the kit's own boxes caught one overlap the film's hand-made list missed (its box was out of date): the phone room's Samaritans notice is pinned half across the second booth's blue hood. Left as you saw it.
- **Decide (my picks):** 1) Y: approve the places kit for the next film's sets (no film uses it until you say). 2) N: leave Blessed's notice as posted (it's finished; the check now catches this on new films).

## Moves from the acting list (ranking item 7, chats 7-8 of 3; about 4.8% of a week so far against 6%, stop 9%)
- **Works:** a film's moves are plain lines, one block per acting-list row (`story/blessed-moves.txt`, now ~140 lines
  of moves). Chat 8 added sitting (seated, and on a chair through the sitting kit), timed head and eye moves, idle life
  and the escort's walk. The kit now redraws 16 people-in-shots in Blessed (Brand in every shot but the cot, the
  judge, both dock guards, the escorting officer, the guard's eyes) identical to the film: every joint each 1/12 s;
  26 test frames 0.000%. Left as named code (one-offs): the jury, the cot, the two inmates, Walliams' struggle.
- **New check:** every row of the film's acting list must have a block landing on its word. On Blessed it caught two
  drifts: the dock slump comes at the start of line 3, the list says on "blessed"; the face change comes 2.6 s after
  "early release", the list says on it. The film is right (Sam saw it); my pick: correct the list's words, no film change.
- **Comparison sheet:** `notes/morning/moves-kit-replicate.jpg` (finished frame beside the kit's, 30 frames across all shots): every one 0.000% different.
- **Cost per film:** Blessed's moves stage was about 1.5% of a week; with the kit a person's moves are a few description lines (Blessed's: 173 lines in one plain file for 16 people-in-shots), so my estimate is ~0.5% per film, to be confirmed on the next film. The kit itself cost ~5% (stop 9%).
- **Found:** one old test (the round-page size check) now fails: the page is 16.4% of Blessed's code, bar 15% (it was 8% when built; the code grew). Not caused by the moves kit; the film is unchanged. Left for the next page job.
- **Decide:** Y/N the moves kit for the next film (my pick Y: all of Blessed but four one-offs matches); Y: correct the acting list's two words (dock slump, face change), no film change.

## The rough of every new thing (ranking item 1, chat 10; done, about 0.45% of a week against 0.5% estimate, under the 0.75% stop)
- **Works:** one command draws a single sheet of everything new in a film's people, places and moves files, with the kits themselves (so the rough is what will be built): people front, side and back; each place's painting with blue outlines where its people stand; each person's moves at up to 5 key moments with the word under each. It remembers what you've seen, so only new or changed things come again ("changed since ..."), and the pre-flight warns about anything built that never went on a rough. A new film with no voice yet still gets true poses (timing waits for the voice). Blessed test: 60 things in about 1 minute; sheet `notes/morning/rough-blessed.jpg`. Every kit test passes.
- **Cost per film:** a rough sheet is a 1-minute command and one look from you, instead of hand-drawn roughs; it aims at the ranking list's ~4% of rebuild notes (Blessed notes 4, 5, 20, 22, 32, 39 were rebuilds a rough would have shown).
- **Decide (my picks):** 1) Y: the rough sheet goes to you once per film before building, plus a small one whenever something new is added. 2) Y: the place outlines stay as depth markers only (where across the picture people stand is set later by the shot, so the outlines are spread evenly; the van and phone ones are big because those people are near the lens).

## Critic bench on Remakes (chat 2; done, about 2.8% of a week against the 2.25% stop: over, see Checks)
- **Works:** a Remakes test (`source/bench/remakes-a3*.json`): 15 stills from the version Sam's notes 68-77 were on, 7 of his notes as the key. Caught, out of 7: plain pictures Opus 1, Sonnet 2; with close-ups of every person Opus 3, Sonnet 4. Both films together (19 notes): plain Opus 6, Sonnet 6; close-ups Opus 5, Sonnet 11. Extras about the same for all (9-11 a run).
- **Missed by all four:** the hazed near flower box, townsfolk standing in the house walls, the banner in one wall shot only: all place faults, which person close-ups don't help. Next improvement: line S6 gets a side-by-side of the shots of one set, and S2 a close-up of far people against buildings.
- **Built (Sam's Y, 14 Nov):** critique packs now add a close-up of every person (from the film's own record of where people stand, or boxes in the spec); rule 89 says so; kittest passes. The ledger now records overnight builds and tests apart from the films (Sam, 14 Nov): this chat had been billed to Remakes and tripped its budget stop.
- **Decide:** Y/N the critic runs on Sonnet (my pick Y: 11 of 19 with close-ups against Opus 5, same extras, about 40% cheaper). Lost: the Opus critic.
- **Checks:** budget slipped: 2.8% against the 2.25% stop (the rerun after the false budget stop, and the close-ups build in the same chat).

## Sam's answers (14 Nov, morning)
- Face tool: 1) Burnham **C**; 2) Badenoch **C** ("best for the house style and matching the features"); 3) **Y**, finish the left list; 4) **Y**, rule 49.3 line written.
- People kit: 1) **all people** turn with their own face (famous ones too: Walliams' turned head); 2) explain, then **all people** keep their own hair colour; 3) approve after a run-through of the kit's contents.
- Places kit: 1) approve after a run-through of the contents; 2) explain the notice question.
- Critic: 1) explain the close-ups; 2) not yet: test the critic again on Remakes and report back.
- Second answers (14 Nov): notice on Blessed left as posted (Y); close-ups of every person in critique packs (Y; the Remakes critic test still decides Sonnet); people kit: everyone, famous too, keeps one look in every pose and turn (Y); people kit approved (Y); places kit approved (Y); moves kit approved (Y); acting list's two words corrected (Y); the rough sheet once per film before building, plus a small one for anything new (Y). Open: a rule for one look in every pose (proposed as rule 90, waits for Sam's Y).
