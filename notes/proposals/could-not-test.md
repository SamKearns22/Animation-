# Proposal: A check that "could not test" passes as a line, so the fault it exists for reaches Sam

Status: adopted (2026-11-22; Sam "1": option 1, a test on Milburn first (changes nothing), then one ask with the numbers: an unskippable stop plus automatic cover, and a readability check if the test shows a need)

## Problem
On Milburn the name cards were hidden by hands and cut by captions twice, and Sam had to note it twice (chat 13 and
chat 18). The clipping check (the check that sees one drawn thing pass through another) never ran on the film: it
printed "COULD NOT TEST" because the film gave it no solids or layers, and that line was carried from chat to chat as
one of the old "named" lines (lines a chat lists to Sam as known, instead of fixing). A check that cannot run looks the
same as a check that ran and found little. Milburn review lesson 1 (notes/proposals/milburn-review.md, section 3);
Sam put it first in the queue (19 Nov).

## Facts
- notes/archive/milburn.md line 11 (chat 13): name cards fixed; "Why the clipping check missed it: it never ran on this
  film ('COULD NOT TEST': the film gives it no solids or layers), and that line was carried as an old quick-check line."
- notes/archive/milburn.md line 14 (chat 18): Milburn's name card again; "clipcheck COULD NOT TEST on this film (no
  solids/layers), and chat 13 judged his card clear by eye on a still where his arm was away." That is a repeat note.
- notes/archive/milburn.md line 20 (chat 15): pre-flight's 48 quick-check lines included "clipcheck COULD NOT TEST";
  all 48 "named to Sam in the Checks line, not settled".
- Where "COULD NOT TEST" is printed: source/audit.py line ~447 (HEAD 'untested'), source/kitchecks.py lines ~619 and
  ~798; source/handover.py lines ~372-385 already count an undeclared-list COULD NOT TEST as a fault at handover.
- Rule 59 (guides/film-quality-rules.md): the final render waits for an animatic that passed the picture checks.
- Milburn cost 21.99% of a week against an estimate of 24% (notes/ledger/milburn.md).

## Record
notes/archive/milburn.md
notes/archive/milburn-handovers.md
source/audit.py
source/kitchecks.py
source/handover.py
source/clipcheck.py
guides/film-quality-rules.md
notes/proposals/milburn-review.md
notes/ledger/milburn.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 44671e4a40cd9aac -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 5 found, 3 fixed, 2 named.

## Leak
yes (mild): the title says the check "passes as a line", which points toward "make it a stop". The facts list also names where the line is printed and that handover.py already counts it, which steers toward code-path fixes. No full fix is stated.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 3 | 2 | 4 | 13 |
| V2 | 4 | 4 | 4 | 3 | 4 | 19 |
| V3 | 5 | 4 | 4 | 3 | 4 | 20 |
## Sam test
Q1: Yes. An expert would do what V3 does: make the tool enforce the stop (not more rule text), feed the check the layers the films already paint, and cover the part the check is blind to (captions added afterwards). The first version wrongly put all of this under one yes. That is fixed below.
Q2: Yes. The evidence covers Blessed, Protest Tiers and Milburn. A scan finds solids or layers in only about 3 of 43 film files, so having no data is the normal state. The replay tests the method on Sam's real notes (chats 12, 13 and 18), not on a made-up case.
Q3: Yes after the fix. Root cause checked: pre-flight stops on the gate's COULD NOT TEST (preflight.py ~457), but it files clipcheck's as an ordinary fault (~488), and one blanket "named" flag waves all ordinary faults through (preflight ~593, film_engine ~90, finish.py ~181). It is enforced in three tools, not by a chat choosing to obey. Success is measured by replay numbers.
Q4: Yes. Four different approaches were weighed: enforce, cover by default, a "stays readable" check on the finished frame, and learning first.
Q5: Weak as written, fixed. V3 asked for one yes covering three changes, and made the stop before any cover existed, so films with no layers could stall. Now the only yes asked today is for the learning replay, which changes nothing. The stop and the cover then come back as one measured ask, and each part can be undone on its own.
Q6: Mostly. Checked: rule 19's wording, the two code paths in pre-flight, Milburn lines 11, 14, 16 and 20, and that milburn.py paints back, mid, front and "over" layers (lines 266 and 293). Unchecked: whether clipcheck would flag a hand over the card, the 3-of-43 count, the cost of the card rounds, and the gap between 22% and 32.4% on the ledger.
Q7: Yes. A stop on its own is the cheap trap, and it is turned down. The cover and the readability check are sized by what the replay shows they catch.
Q8: Yes. Nothing is trialled. Each change is permanent once Sam says yes, and is reviewed at the film's end.
## Pick
V3
## Why
V3 is the only version that finds all three causes: the blanket "named" pass, the hand-built layers that no stage owns (even though milburn.py already paints them, unused by the check), and the check's blindness to captions and the Hook Text, which finish.py adds after the picture is drawn. The last cause explains the caption touch at 1.5 s that reached the final. V2 is close and well sourced, but misses the caption blind spot as a cause. V1 checks nothing. It ignores the fact that rule 19 already demands the stop. It also claims the film template supplies solids, which is false (the template has only draw_order). Taken from V2: the blanket flag also lives in the render tool (film_engine), so the refusal goes there too; and the only way past the stop is that check's own Exceptions line with Sam's Y, which stops a film stalling with no way out. Changed from both: V3 put the stop and two builds under one yes. Now only the replay is asked for today. The stop and the cover then come back as one ask, so the stop never lands on films that have nothing to feed it.
## Faults in the pick
- F1 [fixed] Three changes bundled under one yes, and the stop made before the learning step: now learning first, then one measured ask.
- F2 [fixed] The refusal covered only pre-flight and finish.py: it now covers the render tool's lock too (film_engine).
- F3 [fixed] A film that truly cannot supply layers had no way past the stop: it now needs that check's own Exceptions line, with Sam's Y.
- F4 [named] Whether clipcheck, once fed layers, flags a hand in front of a card at all is unproven. A hand drawn correctly in front of a card is not passing through it. The replay may show that only the readability check catches it.
- F5 [named] Cost figures are estimates. Milburn's true cost disagrees between the app (22%) and the ledger (about 32%).
## Final version
**Step 1, ask today: learn (changes nothing, about 1% of a week, Opus medium).** Replay the checks on Milburn's saved code from chats 12, 13 and 18. Record:
(a) whether clipcheck catches the hand over the card at Sam's noted times, once it is given the layers milburn.py already paints;
(b) whether a "keep readable" check on the finished frames (captions and Hook Text included) catches the card notes and the caption touch at 1.5 s;
(c) how many of the last four films carried COULD NOT TEST, and which faults hid behind it.

**Step 2, one ask back to Sam with the replay numbers (permanent, each part can be undone on its own):**
1. **The stop (about 0.5%).** Clipcheck's COULD NOT TEST joins pre-flight's stop list. Pre-flight, the render tool and finish.py all refuse to let the blanket "named" flag pass it. The only way past is that check's own Exceptions line, which Sam has said Y to. Number to beat: Milburn at animatic 1 is refused.
2. **Cover by default (about 2-3%, only if (a) shows it catches the hand).** The shared painter hands each film's layers to clipcheck, and the template uses it. Number to beat: the chat 12 replay flags the card at Sam's times, and the chat 18 replay comes back clean.
3. **Stays readable (about 1.5%, only if (b) shows it is needed).** The things a film lists at planning (cards, signs, faces) are measured on the finished frames, captions included. Number to beat: it catches the 1.5 s touch, with no false alarms on the last two films.

The stop lands together with whichever cover the replay proves, never before it. Total is about 5-6% once, then nothing per film.
## For Sam
### Option 1: Test on Milburn first, then a real stop plus automatic cover
On Milburn, the check that spots one thing drawn through another never actually ran. Its "could not test" line was waved through with the other known faults, and you noted the name card twice.
First, a short test chat replays Milburn to see which fix would have caught the hand and the captions over the card. It changes nothing.
Then I come back with the numbers and one ask: a stop that no chat can skip, plus a way for each film to feed that check automatically. If the test shows it is needed, there would also be a check that names and signs stay readable once captions are on.
You would notice: no more "could not test" in the Checks line, and name cards and signs readable the first time.
Lost: about 1% of a week for the test, and one more question from me after it.
Added: a stop that can't be skipped, automatic cover for every film, and possibly a readability check.
### Option 2: Make it a stop now, and build the cover afterwards
The stop goes in straight away, and the automatic cover is built afterwards.
This is faster to switch on. But every film that doesn't feed the check yet (most of them) would halt before its animatic until someone builds that by hand. We would also be guessing which fix catches the card fault.
Lost: animatics held up on most films until the cover exists, and the test before building.
Added: the stop working today.
