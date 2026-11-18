# Proposal: Turned people are drawn worse than front-on people

Status: adopted (2026-11-18)

## Problem
People made with the people kit look worse the moment they turn away from the camera. Seen half-turned (the
three-quarter view) or side on, each one stops looking like the same person and looks cruder than the front-on
drawing: hair, facial hair, piercings, face lines and the shape of the body change or vanish. Sam (17 Nov): "our 3/4
characters still look like shit compared to our other poses"; "the actual models themselves have an immediate
reduction in quality and fidelity". Scenes 3 and 6 of Milburn show the four young people mostly half-turned, so the
fault is on screen for about 12 of the film's 68 seconds, and every future film with walking or side-on people meets
it.

## Facts
- Picture: three-quarter-people/front-three-side.jpg (this chat, 18 Nov): goth, Swindon, thin lad, shy girl drawn
  front (0), three-quarter (45) and side (90) at the same size. Counted differences, front vs three-quarter:
  goth: front hair is the new `shag` cut (heavy choppy fringe, blue streak panels); turned it is the plain `long`
  purple hair, no fringe, no blue, and her brow, lip and nose piercings are gone. Swindon: front crop with short
  sides; turned a combed helmet; front eye bags and smile folds gone; his ears gone. Thin lad: his pencil moustache
  is gone turned. Shy girl: front long straight hair with a fringe; turned long wavy hair. All four: the front
  face's eye bags, folds and ear detail are gone; brows thinner; skin flat.
- Picture: three-quarter-people/in-scenes-3-6.jpg (frames 13.0 s and 39.5 s): the same faults at film size; the
  turned torsos read as flat slabs (Swindon's shirt a red box; arms drawn over it as thin tubes; no shoulder line).
- The front head of a kit person is drawn by source/people_parts.py `front_head` (line ~214: beard, pencil moustache
  279, eye bags and folds 263, piercings 324). The turned head of a kit person is drawn by source/people_turned.py
  (its MAP: haircuts from behind LIFTED from Blessed's press pack; TURNED maps each kit haircut to a press-pack one:
  'shag' -> 'long', line 40 "front only so far") on source/turnhead.py's 3D head (TurnFace). people_turned has no
  pencil moustache, no piercings, no streaks (grep, this chat).
- The turned torso is source/views.py `torso_view` and `torso_outline` (lines 516-623): one outline per view; the
  three-quarter torso is a single polygon in the jacket colour.
- Famous people (Andy, Pat) use source/facehouse.py's house head turned through turnhead (`install_turned`); kittest
  `facehouse_whole_head` has been failing since 15 Nov (named, not this film).
- Earlier, the same complaint about measured faces (Ad-Vanced Notice note 42e, archive): "Neither the side nor the
  three-quarter view looks like him: a different draw style"; fixed 8 Nov by carrying the person's own front design
  round a 3D head (turnhead). That fix is what people_turned uses, but only for the parts it was given.
- Where the milburn film uses turns: scene 3 (yaw 40, snapped to the 45 view, `views.snap`), scene 6 (walking right,
  side and three-quarter), scenes 4/7 (Andy and Pat seated, front). source/milburn.py YAW3, forest_pose.
- guides/figure-rig.md section 9 lists as missing: "Mouth shapes for profile and three-quarter faces"; "Back and
  three-quarter-back views".
- Cost so far: film ~19.2% of a week (ledger). Sam's Y to the top recommendation is given in advance (Decisions,
  17 Nov 23:07). Unchecked: how much of the press-pack people in Blessed changes if the turned heads change (kittest
  `people_from_a_description` replicates Blessed's frames pixel for pixel).

## Record
notes/proposals/three-quarter-people/front-three-side.jpg
notes/proposals/three-quarter-people/in-scenes-3-6.jpg
source/people_parts.py
source/people_turned.py
source/turnhead.py
source/views.py
source/people.py
source/facehouse.py
story/milburn-people.txt
guides/figure-rig.md
guides/kit-catalogue.md
notes/archive/ad-vanced-notice.md

## Verdict (the judge, word for word)
<!-- verdict-hash: f92e3b39cb27fb9e -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: mild. The Facts say the 8 Nov fix "is what people_turned uses, but only for the parts it was given", list the missing parts one by one and call the turned torso "a single polygon". Together these point toward adding the missing parts and fixing the torso polygon. The file proposes no solution in so many words. Both helpers also say they opened the chat's own idea (chat.md) by mistake.

## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 3 | 3 | 4 | 18 |
| V2 | 5 | 4 | 4 | 4 | 4 | 21 |
| V3 | 3 | 3 | 2 | 2 | 3 | 13 |

## Sam test
Q1: Yes. One source design that every view draws from, with an automatic parity refusal, is what an expert would build. The final version adds an identity test: the turned head at 0 degrees must equal the front head, which turnhead already promises.
Q2: The evidence is wide enough: four jobs of turned-view notes (Ad-Vanced 42e, Blessed note 4, face tool chat 12, Milburn), the git history of 17 Nov and both pictures. The audit adds famous heads, the torso and the Blessed replica.
Q3: The root cause is shown and checked. people_turned `_marks` hand-copies only stubble, beard and freckles, and five front parts were added on 17 Nov to the front only. The old "draws nothing" check plus a hand-written hidden list could be passed on paper, so it is fixed below: each part is toggled on and off, and whether a part is hidden is worked out from the head's shape. Pre-flight refuses, so no chat can choose to skip it.
Q4: Four approaches were weighed: patch the copy, one source, staying front-on, and learning first. One source is the only one that stops the next new part going missing.
Q5: Front frames must not move. That is now tested, not assumed: the front code has to be split, so the Blessed replica must hold at 0.00%. Old films stay keyed to the old turned heads. Each change undoes on its own. Sam sees a sheet before anything is rendered. The torso waits for evidence.
Q6: Checked: on-screen time (scene 3 11.0-15.3 s and scene 6 34.0-41.6 s, so 11.9 s), milburn.md:88 and :220, preflight.py TURN DESIGN, the 17 Nov git log, the ledger figures (19.56% spent, 85.6% forecast) and `_marks`. The cost figures are estimates and are marked so.
Q7: Sized for the cause across the kit, not the cheap patch (V3). It does not pay for a torso rebuild before the audit shows it is needed.
Q8: Permanent. It is logged as a kit job and reviewed against Milburn's results and the next film's notes.

## Pick
V2

## Why
V2 is the only version that answers the real decision. That decision is one source for every view across the kit, enforced by a refusal, and changed only where the measured results say so. It is also the only version that questions the torso. The picture bears this out: the front torso is the same red box, and the turned slab is mostly the arms drawn across the body, so a torso rebuild before the audit would be a change made ahead of the learning. V2 also states that the back of each haircut must be redrawn. The picture shows why this matters: the shy girl's front hair is "long" too, yet it turns wavy, so carrying the front parts round the head is not enough on its own.

V1 is close, but it commits to the torso build (1.5%) before any evidence and lists three changes at a total of 4.8%. V3 is the patch in disguise: it rebuilds the turned parts "from the same numbers", which is a second copy that will fall behind again. It also bundles four changes into one yes, has no learning step, names scene 4 for clips (Andy and Pat are front-on there) and gives an unmeasured 2%.

Taken from V1: the parity measure toggles each face-card item on and off at 0, 45 and 90 degrees, which beats V2's "draws nothing" test. Also from V1, the cast sheet gains a three-quarter tile for anyone a shot turns, kept as its own small yes.

Added by the judge: an identity test at 0 degrees, and "hidden from this side" computed from the head's geometry instead of a hand-written list.

## Faults in the pick
- F1 [fixed] V2's check passed any part that draws something, however wrong (straight hair turning wavy would pass). Replaced by V1's on/off parity test per item plus a 0-degree identity test against the front head.
- F2 [fixed] V2's hand-written list of parts hidden from a side was an escape hatch a chat could add to. Hiddenness is now computed from where the part sits on the 3D head at that yaw (TurnFace's own visible test).
- F3 [fixed] The cause by which faults reached Sam (rule 38's cast sheet has no three-quarter tile) was named but left open. It is added as Change 3 with its own yes.
- F4 [named] The front code draws the outline and ears inside the same function as the face parts, so reusing it means splitting the front code. Front frames could move. This is guarded by the Blessed replica holding at 0.00%, which is unchecked until it is run.
- F5 [named] Famous heads (facehouse) have the same kind of fault, and their kit test has been failing since 15 Nov. The audit measures them but this proposal does not fix them.
- F6 [named] The ledger records "0 notes" for Milburn although Sam gave 11, so "fewer notes" can only be counted by hand from the notes file until the ledger is fixed.
- F7 [named] The film is already at 19.56% against a 15% aim. This costs about 3.5% more, logged as kit work, and the estimate is unchecked.

## Final version
**Learn (changes nothing, about 0.5% of a week):**
1. Parity measure for every kit person on record and the famous heads. Each face-card item and clothing extra is drawn on and off at 0, 45, 90 and 135 degrees. An item that changes the front but not a turned view, and whose place on the head is visible at that yaw, counts as dropped. Today's count is the number to beat (about 12 on the Milburn four).
2. A front / three-quarter / side sheet of the Milburn four beside a photo of a real person turned. Torso compared front against turned.
3. The Blessed replica test run with turned heads on and off.

**Change 1, heads (its own yes, about 3%, Opus high, one chat):**
- The turned kit head draws every face part with the front's own code on the 3D head: fringe, streaks, piercings, pencil moustache, beard, stubble, eye bags, folds and glasses. The front's outline and ear code is split from its parts code.
- Only the outline, ear, nose bridge and back of each haircut are drawn separately. The backs are redrawn to match each front cut (the shag from the filed alt-hair photos; straight "long" stays straight).
- Old films stay keyed to their old turned heads.
- Enforced: a kit test and a pre-flight refusal for every kit person a film turns. It requires zero dropped parts, and the turned head at 0 degrees must match the front head. This makes TURN DESIGN smarter rather than adding a new check.
- Beat: dropped parts go from about 12 to 0, Blessed front frames stay at 0.00%, Sam passes the turnaround sheet, and there is no repeat of the three-quarter note at the next animatic.

**Change 2, torso:** only if the audit sheet shows the turned torso worse than the front. It needs its own evidence and its own yes. If both are equally boxy, it becomes a separate body-look decision.

**Change 3, cast sheet (its own yes, about 0.3%):** the cast sheet gains a three-quarter tile for anyone a shot turns, and the sheet check refuses a sheet without it.

Sam sees the turnaround sheet, then clips of scenes 3 and 6. Reviewed against Milburn's results and the next film's notes.

## For Sam
### Option 1: One drawing for every angle, checked by machine
Turned people are drawn from the same drawing as the front-on ones, so the fringe, blue streaks, piercings, moustache, eye bags and hair all follow them round. A machine check, which you never see, refuses any film where a turned person loses a part. You get a front / half-turned / side sheet of the four, then clips of scenes 3 and 6. The bodies are measured first and only changed with your yes.
Lost: the old borrowed hairstyles on turned people (old films keep theirs).
Added: about 3.5% of a week once, for every future film; one refusing check; a half-turned picture on each cast sheet.
### Option 2: Rebuild heads and bodies together now
The same head rebuild, plus the turned body redrawn now with shoulders and sleeves, without measuring first whether the body is really worse than the front one. Quicker to see everything change at once, but it could spend effort on a body problem that is really the house style.
Lost: the old borrowed hairstyles and the current turned body shape.
Added: about 4.8% of a week once; the same check and cast-sheet picture.
