# Helper A: teach-recognise

## Leak
Mild: lesson 22 and "wide panel" hint at remedies; weighed.

## Results
- Close-ups were off for the whole film. All six critique specs set `"closeups": false` (source/data/critique-src/grand-theft-autism/; checked). Sam's 14 Nov rule wants them; `pack` gives no warning (checked).
- The critic asked for the look it needed. Round 22, panel 4 was the 3.75 s frame Sam flagged: "CAN'T TELL... A full-size crop of the hand and the head would show it" (ledger round-22.txt; checked). Panel 540 px wide, arm about 60 px (checked).
- A CAN'T TELL never blocks. The send gate accepts any critique record (critique.py `status`, humancheck.py `sendgate`; checked).
- The checklist already covers faults a, b, c and g: P1, P3, P5 and P8, each with "Look: full size". No line covers d, e or f (checked).
- Crops on the test bench: Sonnet went from 4 to 7 of 12 (Blessed) and from 2 to 4 of 7 (Remakes). Opus was mixed (critic-bench.tsv; checked).
- Shot 4: 7 versions, 16 notes on v4, 10 on v7 with 3 repeats. The film is at 42.84% of 15%, forecast 93.4% (checked). "12 chats" is unchecked: about 23% of a week at 1.9% a chat.
- Gap: the film's ledger shows 0 notes and 0 repeats. Round 22's second critique has no record.

## The real decision
Does every picture Sam sees first get a fresh full-size look at every person, with no way to skip it? Two levers are bigger than "teaching": making that look happen at all, and choosing camera angles where the flat drawing holds.

## Root cause
1. Close-ups were switched off without any warning. Likely why (unchecked): shot 4's panels are saved pictures with no person boxes, so the tool cannot crop them.
2. "Can't tell" counts as a pass, and the send gate is happy with a critique that had no close-ups.
3. Only about 5 hand-picked moments are critiqued. Sam watches every frame.
4. Some angles break the flat body whatever the check. The sausage arm measured 1.26-1.37x its length.

## Approaches weighed
1. Labelled examples: give the critic Sam's 22 pictures (counted). This trains the eye, but the eye was never shown the frame.
2. Enforce the full-size look: close-ups can't be turned off, contact moments are always shown, a CAN'T TELL sends the sheet back, and the send gate checks all of this.
3. Reframe (upstream): a staging check refuses camera angles where the flat drawing breaks.
4. More measuring checks: partly built; always another shape.
5. Learn first: replay shot 4 on the critic test bench.

Chosen: 5, then 2, then 1 or 3 only if the results show they are needed.

## Proposal
**Learn (changes nothing, about 2%, unchecked).** A test-bench case built from the v4 and v7 frames Sam saw, with his 26 notes as the answer key. Run Sonnet and Opus critics three ways: as packed, with close-ups, and with close-ups plus every contact moment. Count catches, and misses no line covers.

**Change 1 (its own Y, about 1%).** In the critique tool and the send gate:
- Close-ups for people can't be switched off.
- A saved-picture panel must give person boxes, or the pack is refused.
- A CAN'T TELL on a person line re-packs with the crop it asked for. The film is not blocked, so Sam's 11 Nov rule stands.
- The send gate accepts only a critique record that had close-ups.

Number to beat: on the bench, the close-up critic catches more notes than the as-packed one (the target is set from the learn step). On the next clip, 0 repeated notes about people.

**Change 2 (its own Y, only if there are misses at full size).** Sam's pictures become a standing bench case, plus new checklist lines for d, e and f.

**Change 3 (its own Y, only if misses are tied to the camera angle).** A staging check refuses angles where a limb draws more than 1.2x its length.

Sam would notice: fewer drawing faults reaching him.

## Sam test
Q1: Yes: check the critic was shown the fault before retraining it.
Q2: Shot 4 replay plus two bench cases.
Q3: Root cause shown. Enforced in the tool and the gate. Measured at film end.
Q4: Five different approaches weighed.
Q5: Learning carries no risk. Each change is its own Y and can be undone.
Q6: Sources named. Costs unchecked.
Q7: Sized to stop the faults, not to patch shot 4.
Q8: Permanent, reviewed at film end.

## Lost / Added
Lost: critiques without close-ups.
Added: a GTA test-bench case, enforced close-ups, a re-pack on CAN'T TELL, and a stricter send gate.

## Unchecked
All costs; why close-ups were off; the 12-chat count; round 22's second critique.
