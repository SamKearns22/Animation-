# Helper B: checks that know what the scene means

## Leak
Leak: the fact "a Claude helper can look at a still and read a text (critique.py)" points at one means. Weighed below as one option, not assumed.

## Results
- Chat 36: 9 picture-check faults, 3 matched an answered row, 6 did not (problem file; source/data/brexit_is_done-picture-checks.txt lists the 9).
- Of the 6, the 3 RESTS are on the leads, not the crowd: May's hand sinks 4 cm into her thigh (16 frames); Blair's two wrists sit 3 cm below the armrest top (42 and 109 frames). These are intended rests drawn wrong, the same kind as Sam's note 19 ("hands hover rather than resting", seen before). Knowing the intent would not excuse them. Not looked at (problem file).
- The 3 crowd "hand over another body" faults: the film already says why runners' hands hide (HANDS_OK, source/brexit_is_done.py 129-133), but only for the kind 'no hand', never 'over *' (handcheck._allowed), and '*workers 2' matches worker 2 only, while the faults name workers 3, 4, 5. The purpose was written; it was written at the wrong grain.
- One of the 3 (29.33 s, a bent arm behind Blair's neck) "reads oddly" (problem file): possibly real.
- The drawing code states the purpose where it draws (figure.allow, "a guest running side on: the back arm swings behind the body", brexit_is_done_action.py 896); the hand check never reads it. The same purpose is copied by hand into HANDS_OK and into the notes' Exceptions.
- Cost of answering flags: not in the record. The ledger (notes/ledger/brexit-is-done.md) has no line for it. Film spent 55.84% of a week against 15%. This gap is a finding.
- Since rule 93 checks never lock, so a false flag now costs reading time and buries real faults in noise (Milburn's 61 lines, waivers.py 214).
- Sam declined the "reopen answered notes" fix (answered-faults-return.md).

## The real decision
Not "how do answered rows survive a drawing change", but: across every film, how is each flag sorted, without hand-written rows, into "meant, stay quiet" or "drawn wrong, fix it". Bigger levers: where intent is written (once, at the action that causes it), and the half of flags that are real drawing faults.

## Root cause
Intent and check are joined by hand, after the flag, in a text row keyed to a name, a second and exact words. The action that drew the overlap knows what it meant; the check is blind to it. Any redraw breaks the join; a narrow row (one kind, one worker) misses its own case.

## Approaches weighed
1. **Intent travels with the drawing (reframe).** Shared actions (side-on run, crowd pass, doorway entry) mark each person in each frame with what they mean; the checks read it from the frame record. A redraw carries it along.
2. **Ask a picture helper when unsure.** Each unexplained flag goes with its still and the screenplay line to a Claude helper: "meant or wrong?"
3. **Fix the drawing so the flag never fires.** Teach small side-on figures' hands and fix rests sinking (Sam's offered option).
4. **Learn first.** Sort every flag on record into meant, real, unclear, by looking.
Chosen: 4, then 1, then 2 only for what 4 shows is left; 3 runs anyway for every real fault.

## Proposal
**Learn (changes nothing):** one chat looks at the first still of every picture-check flag this film has had (chat 17's 16, chat 20's 34 answered, chat 36's 9) at full size; each is marked meant, real or unclear, with what in the brief or action list makes it meant. Saved as examples. This gives the number: what share is noise.
**Change 1, intent at source:** every shared action that hides or overlaps limbs declares it in the frame record (person, limb, kind, cause); the hand, overlap and pop checks skip only that exact pattern. Never excusable by intent: anything through a body, sinking, hovering (extend figure.NEVER_ALLOWED). A film-only declaration needs an Exceptions row. Kittest: stays quiet on all "meant" examples; still flags every "real" one (note 19, chat 36's RESTS, the May finger, 29.33 s if real). Beat: meant flags on chat 36's animatic 0, real flags silenced 0.
**Change 2, only if the learn step finds unclear flags left after change 1:** the picture helper, judged first against every saved example; trusted only when it calls no real fault meant.
Cost (unchecked estimate from ledger build chats, 2-4.3%): learn about 1.5%, change 1 about 2.5%, change 2 about 2% once, about 0.2% a film to run. One-off; per film it saves reading and answering rows.
Sam would notice: shorter Concerns lists, nearly all real; rests and hands fixed in the drawing.

## Sam test
Q1: an expert puts intent at its source, not in exception lists. Q2: evidence is the whole film's flag record, not one chat. Q3: runs in code on every frame; no chat chooses; kittest proves both ways. Q4: four different routes weighed. Q5: each change undoes alone; nothing trusted until it passes saved examples. Q6: sources named; gaps marked. Q7: sized to stop noise and keep real faults, not a cheap silencer. Q8: permanent shared change, reviewed at film end.

## Lost / Added
Lost: hand-written HANDS_OK and pop rows for meant crowd actions. Added: an intent mark per action, a kittest, possibly a picture helper.

## Unchecked
Costs; whether picture checks ran in chats 22 and 26; whether 29.33 s is real; the RESTS stills; the meant share of chat 20's 34 rows.
