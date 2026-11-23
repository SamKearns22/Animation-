# Helper B: which model takes Sam's notes

## Leak
The problem file names its answer: "rounds that only change words, timing or sound can go to Sonnet". Ignored here.

## Results
- Milburn had two notes rounds on Sonnet, not one. Chat 13 is Sonnet in the app's own record (notes/ledger/app-costs.tsv, model read from the app), although notes/archive/milburn.md line 10 says "Opus medium". Trust the app: it records the model the chat actually ran on. Chat 13 took 5 notes (brows, a new face mood, the lemon, name cards, a fireplace built from a photo with two new kit pieces) for 1.50%. Chat 18 took 13 notes (lines 14-18: 9 on animatic 3, 2 on the clip, "receive", the starred swear word) for 1.27%. Both figures are at the 366-dollar week (.claude/hooks/costwatch.py).
- The ledger page notes/ledger/milburn.md still shows the old week (chat 18 at 1.9%), so it disagrees with the problem file. The review's "2.3%" doesn't match either figure (unchecked).
- "No repeats" isn't quite true. Sam's note on Milburn's name card (chat 18) came back after chat 13, on Sonnet, judged that card "clear by eye" (line 14). The notes blame the clipping check, which could not run on this film. Chat 18's own addition (the goth grinning on each bolt) drew a new note at once (line 15). So 1 repeat in 18 Sonnet notes, plus 1 note caused by the fix itself.
- Sonnet already did look and build notes (chat 13), not only text.
- Size of the lever: Milburn cost 21.98% in all (80.44 dollars). Its Sonnet notes rounds cost 2.77%. With about the same amount of reading, chat 18 cost 4.65 dollars and Opus chat 11 cost 6.68 (app-costs.tsv), so Opus costs about 1.4 times as much. Moving one round to Sonnet saves about 0.5% a round, about 1% a film. One repeated note costs a whole extra round (1.3-2.5%).
- A gap in the record: the notes and repeats columns read 0 for every chat (milburn.md, blessed.md). So no record can yet compare repeats by model. The sample is one film and 18 notes.

## The real decision
The question is which model fixes each note, judged across the whole film by repeats and by faults that reach Sam, and only then by cost. The rule is already broken in practice. The bigger lever is repeats, not the price of a model.

## Root cause
1. The rule assigns a model to a whole stage ("a round of my notes"). A round mixes text notes with notes on looks and poses, so any model chosen for the round is wrong for some of its notes.
2. Nothing counts notes or repeats per chat, so neither the rule nor any change to it can be tested.
3. The Sonnet chats took the notes as they came because nothing stopped them. The model rule is only words in a handover (see notes/proposals/model-switch.md).

## Approaches weighed
1. Split rounds by kind of note: text, timing and sound go to Sonnet. Simple, but it guesses where to draw the line before any evidence.
2. Reframe: choose the model note by note, by what the fix touches. A Sonnet chat takes every round, sorts the notes and fixes text, timing, sound and re-renders itself. It hands notes on looks, poses, staging and new building to one Opus medium chat, as one list, and gets the clips back.
3. Learn first: count notes, repeats and cost per chat, by model and by kind of note, for Milburn and Blessed. Then decide.
4. Keep Opus for every round and put the effort into cutting repeats (better checks). This is the bigger lever, but it is a separate route.

Chosen: 3, then 2.

## Proposal
**Learn first (changes nothing; one Sonnet chat, about 0.5% of a week).** Read the Milburn and Blessed notes files. For each chat, record: notes taken, the kind of each note (text, timing, sound, look, pose, staging, build), repeats (a note Sam gave again on the same thing), the model the app recorded, and the cost. Fill the ledger's empty notes and repeats columns with these counts. Output: repeats per note and cost per note, by model and kind.

**Change 1 (its own yes, only if Sonnet's repeat rate on a kind of note is no worse than Opus's). Opus medium, about 1% of a week.**
- CLAUDE.md's notes line becomes: "Sonnet takes each round and sorts the notes. It fixes the kinds the record shows it handles as well as Opus. It hands the rest to one Opus medium chat as a list."
- Enforced in code at two points. When a chat is opened, the handover check compares the model the chat is really running on with the kinds of note it holds. At the end of a chat, the ledger takes the notes and repeats counts from the "Done (chat N, Sam's K notes)" lines, so every film is measured with no hand counting.
- Numbers to beat: repeats per note on Sonnet-fixed notes at or under the Opus rate, with Milburn's 1 in 18 as the baseline. Cost per note under 0.15% of a week. Both are reviewed when Sam calls the film done.

What Sam would notice: notes rounds come back from Sonnet; notes on looks and poses arrive in a second message from Opus; the film record shows a repeat count.

## Sam test
Q1: Yes. An expert would decide the model by what each fix touches, using measured repeat rates.
Q2: The evidence is two films, every chat in each. One film alone is too thin, and this proposal says so.
Q3: The root cause is a rule set per stage with no measure. The check is enforced in code, and the counts are automatic.
Q4: Four different approaches were weighed. Repeats is named as its own route.
Q5: Learning changes nothing. The change is one yes and can be undone alone. No guessed line between kinds of note.
Q6: Sources are named. Disagreements in the record are shown (chat 13's model, the ledger's old week, 2.3%).
Q7: The change is sized by repeats, not by savings. Saving 1% is not a reason to accept one more repeat.
Q8: Nothing is trialled. The change is made properly or not at all, and reviewed at the end of the film.

## Lost / Added
Lost: Opus fixing text and sound notes; the rule's "round = Opus" line.
Added: notes and repeats counted for every chat; Sonnet sorts every round; a second hand-off when a round has notes on looks.

## Unchecked
- Why the review says 2.3%.
- Whether the work Sam queued under lesson 5 already fills the notes and repeats columns (if it does, the learning step reuses it).
- Whether a film chat can read the model a chat is running on (the app-costs record could, on 13 Nov; my own lookup of these chats failed).
- Opus's true price ratio beyond these two chats.
