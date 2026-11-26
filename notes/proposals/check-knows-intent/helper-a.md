## Leak
Partly: the Facts say "a Claude helper can look at a still and read a text (critique.py)", which points at one remedy. Weighed, not assumed.

## Results
- Chat 36: 6 hands + 3 rests lines (source/data/brexit_is_done-picture-checks.txt). Of 3 crowd "hand over another body" frames looked at, 2 were ordinary overlap and 1 (29.33 s, a guest's bent arm behind Blair's neck) showed a real oddity under the wrong label (problem file).
- Chat 17: 16 faults; chat 19 fixed real ones (May's chop, Kemi 12.42 s, doorway guests) and wrote "meant" rows for the rest: 2 HANDS_OK, 4 ALLOWED_POPS, 34 pre-flight lines (notes/archive/brexit-is-done-handovers.md).
- The hand-over-body test flags a hand over anyone drawn within 10% of the same size (source/handcheck.py, NEAR = 0.1): about a metre of depth, so runners side by side always "touch". It never reads the plan in metres.
- The HANDS_OK rows (source/brexit_is_done.py) cover only kind 'no hand'; chat 36's crowd lines are kind 'over …', so chat 19's meant staging could not cover them.
- The 3 RESTS lines (Blair's wrists 3 cm below the armrest, May's hand 4 cm into her thigh) look like real faults; Blair's may come from note 19's fix. Unchecked.
- Cost of answering checks: not separable in the ledger (rows per chat, stage mostly "auto"). That gap is a finding.

## The real decision
How is every concern, film-wide, judged against the picture and what the scene means, so meant staging stops coming back and real faults are never waved through? Bigger levers: give the checks the depth and action the film holds; state meaning with the action.

## Root cause
1. The checks lack what the film already has: depth in metres and the action lists (site_actors, room_actors). A flat overlap test with a 10% size margin cannot tell "in front" from "touching".
2. "Meant" is written afterwards, keyed to a check's wording, a person and a second (waivers.split, HANDS_OK kinds), so it does not follow the drawing. Sam declined the fingerprint fix (answered-faults-return.md).

## Approaches weighed
1. **Judge helper**: a fresh helper gets each concern's still, the screenplay line and the action, and answers meant / fault / can't tell.
2. **Better checks (reframe)**: the hand test uses plan depth: a touch only where the hand would really meet the other body. Meaning is stated with the action ("runs in a pack", "through the doorway") and read by every check.
3. **Store nothing**: no saved "fine" answers; every animatic is judged afresh, so nothing goes stale.
4. **Learn first**: sort every picture-check line of chats 17-36 into real, meant and wrongly named, by check kind, before changing anything.

Chosen: 4, then 2, then 1 where still needed, with 3's rule.

## Proposal
**Learn (changes nothing):** a Sonnet chat sorts every saved picture-check line of chats 17-36, each frame full size, into real / meant / wrongly named, by kind; and whether plan positions reach the hand check. About 1% of a week.
**Change 1 (its own yes):** the hand-over-body test uses depth in metres. Number to beat: drops the meant crowd lines of chats 17 and 36 and still catches every real one the sort found. Enforced by a kit test built from those frames. About 1.5%.
**Change 2 (own yes, only if meant lines remain):** an action entry carries a plain "what is meant" line that checks read; such concerns still print as "meant: …". Kit test: doorway guests, side-on runner. About 1.5%.
**Change 3 (own yes, only for what stays unclear):** the judge helper gets rule 93's circled still, the screenplay line and the action; it judges on every animatic and saves nothing; its verdict is advice on the Checks line. Number: agrees with the sort on every saved line. About 0.3% per animatic.
Per film after setup: about 0.3-0.6% against 15%. Sam would notice correct Checks lines and meant staging not returning.

## Sam test
Q1: fix the measuring first; judge only what it cannot reach.
Q2: the whole film's record (chats 17-36), not one chat.
Q3: root cause shown; kit tests make it run in every chat, not reading.
Q4: four different approaches weighed.
Q5: each undone alone; nothing trusted untested.
Q6: sources named; unknowns listed.
Q7: sized by result; no judge papering over a weak check.
Q8: permanent, with kit tests, reviewed at film end.

## Lost / Added
Lost: the HANDS_OK table for hands, once change 2 covers it. Added: a depth-based touch test, a "what is meant" line on actions, a judge pass per animatic.

## Unchecked
Whether plan positions reach handcheck; the RESTS lines' cause; helper costs; the earlier real/meant split (the sort's job).
