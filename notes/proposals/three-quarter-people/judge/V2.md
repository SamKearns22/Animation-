# Helper B: turned people drawn worse than front-on

## Leak
The problem file states no solution. The folder's `chat.md` (the chat's own idea) was opened by mistake while I listed the folder. I did not use it, and nothing below depends on it.

## Results
- **Parts lost when a person turns, Milburn cast** (picture front-three-side.jpg, checked by eye): the goth loses her fringe, her blue panels and all three piercings. Swindon's haircut changes shape, and his ears and eye bags go. The thin lad loses his pencil moustache. The shy girl's straight hair with a fringe becomes wavy. All four lose their eye bags and face folds. About 12 parts are lost across four people.
- **It is a known gap that went ahead anyway.** Milburn note 3's fix says "front only (turned views fall back to long hair: build the turned shag if scene 3 turns her)" (notes/milburn.md:220). The estimate already had a line for it: "turned shag NEW", moves 1.5% (milburn.md:88).
- **Why the checks missed it:** TURN DESIGN only asks whether someone with their own face is turned on the generic head (source/preflight.py:163). Any turned head passes, even one with missing parts. Nothing compares the turned parts with the front parts.
- **This is a repeat across films:** Ad-Vanced 42e (8 Nov: "a problem throughout the project"); Blessed notes 4, 16, 26 and 39; face tool chat 12 ("our 3/4 front poses ... look gaunt and weird"); now Milburn. Each was fixed for one way of drawing heads only (archive files, grep).
- **Cost:** the film has spent 19.56% of a week against an estimate of 24.0%; the ledger forecasts 85.6% (notes/ledger/milburn.md). The ledger shows "0 notes" although Sam gave notes 1 to 11, so it cannot count notes. That is a gap in the record.
- **Torso:** the front torso is the same red box as the turned one (picture, Swindon). The "slab" may be the house body style, not a turning fault. Not proven either way.

## The real decision
This is not about fixing four Milburn people. It is whether a person's design has **one source** that every view draws from, or a front drawing plus a hand-copied turned twin that falls behind every time a new part is added. The bigger lever is a check at the moment a part is built, not one at film time.

## Root cause
- The 8 Nov fix (`turnhead`) was designed so that "the person's own ... shapes are drawn by their own code" round a 3D head (source/turnhead.py:13).
- The people kit's turned heads (`people_turned`, 14 Nov) did not do that. They lifted the press pack's haircuts and copied part of the face code by hand (`_marks`: stubble, beard, freckles only).
- Parts added on 17 Nov (pencil moustache, piercings, the shag cut; git log) went into the front drawing only.
- The front's part code uses only the turned head's own way of placing points (f(u,v), f.pts; people_parts.py 338-527). It could have been reused as it was.
- No check stopped the gap, and the cast sheet that rule 38 asks for shows no three-quarter view, so Sam was the first to see it.

## Approaches weighed
1. **Patch the turned copy:** add each missing part to people_turned. Quick, but it falls behind again with the next new part. This is the cause, repeated.
2. **One source (chosen):** the turned head draws every face part with the front's own code, carried round the 3D head. Only what has no front drawing (the back of each haircut, the ear, the outline) is drawn separately. Plus a check that refuses a part that disappears when turned.
3. **Reframe the staging:** keep people front-on (rule 38). This contradicts Sam's direction for scene 3 ("see them from the side") and does less, so it is rejected.
4. **Learn first:** an audit of every part in every view, across the kit, the famous heads and the torso. It changes nothing and settles what the torso question needs.

## Proposal
- **Learn (changes nothing, about 0.5%):**
  - Make a table of every face-card part and clothing extra against the three-quarter, side and back views, for the people kit and the famous heads (facehouse).
  - Make a front / three-quarter / side sheet of each Milburn person beside a reference photo of a real person turned.
  - Run the Blessed replica test with turned heads on and off. This answers the unchecked line in the problem file.
- **Change 1 (heads, its own yes, about 3% of a week, Opus high, one chat):**
  - The turned kit head calls the front's own part code (hair front and fringe, streaks, piercings, pencil moustache, beard, stubble, eye bags, folds, glasses) on the 3D head.
  - The back of each haircut is drawn new, the shag's from the alt-hair photos already filed.
  - Front drawing unchanged, so Blessed's front frames stay at 0.00%. Old films' turned looks stay keyed to the old drawing (`KEYED`).
  - **Enforced:**
    - A kit test fails whenever a face-card part draws nothing in a turned view and is not on a written list of parts hidden from that side.
    - The same test runs in pre-flight for every kit person a film turns, so it is a refusal, not a chat's choice. This makes TURN DESIGN smarter rather than adding a separate check.
  - **Number to beat:** parts lost turned goes from about 12 to 0 on the Milburn cast. No repeat of the three-quarter note at the next animatic.
- **Change 2 (torso):** only if the audit's sheet shows the turned torso is worse than the front torso. It gets its own evidence and its own yes. If both are boxy, that is a separate body-look decision.
- **What Sam would notice:** the turned people now match the front ones part for part. He gets a three-quarter sheet plus clips from scenes 3 and 6.

## Sam test
- Q1: Yes. One source plus a check when a part is built is what an expert would do; patching the copy is not.
- Q2: The evidence is drawn from four films' notes, not just this one; the audit widens it to the famous heads and the torso.
- Q3: The root cause is shown in the code and the git history. Enforcement is a refusal in the kit test and pre-flight, and success is measured by counting parts lost.
- Q4: Four different approaches were weighed; one source is the only one that stops the next new part going missing.
- Q5: Front frames do not move. Old films stay keyed to the old turned heads. The change can be undone on its own, and it is shown on a sheet before anything is rendered.
- Q6: Facts carry their sources; the gaps are below.
- Q7: Sized for the cause, not for this film's four people. Torso work waits for evidence instead of a cheap guess.
- Q8: Permanent. Reviewed against Milburn's results when the film is declared complete.

## Lost / Added
- Lost: the press-pack haircuts used as kit people's turned hair (old films keep them).
- Added: about 3.5% of a week; one kit test that also runs in pre-flight; a drawing of the back for each haircut.

## Unchecked
- The 12 seconds on screen (scene 3's timing).
- How many Blessed turned frames move.
- Whether the face folds sit right on the 3D head's far side.
- Whether people.py's five-turn sheet was run for Milburn.
