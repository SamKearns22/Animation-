# Helper B: women drawn on a man's body

## Leak
None stated as a remedy. The facts lean towards "switch on `build woman`", which I treat as one option only.

## Results
- Sam has now named this fault in two films. GTA, 20 Nov: "Lucia on a man's box body". The critic saw it in both hunts, it was closed as "house style" and sent anyway (notes/archive/grand-theft-autism-notes.md 125-127). Brexit cast v2, 23 Nov: n5 (notes/sam-notes/brexit-cast-v2/notes.md).
- The GTA fix was opt-in, "so finished films draw as before" (same file, 135). Of the four named women since then, only Lucia uses it. "Her", May and Kemi do not (story/*-people.txt). Crowd women never get it (people.py 249-270). All checked.
- The build changes only the torso outline. Lapels, jacket length, trousers, shoes and stance stay one man's cut (body.py 586-600). In the n5 pictures (viewed), both women wear a straight jacket to mid-thigh, straight trousers and slab shoes, Blair's outline.
- No check knows who is a woman (castsheet.py line 19). The rulebook has no such rule (grep: none). The kit catalogue does not mention the build (grep: none).
- Cost: the Brexit cast chat cost 1.85% of a week for 3 notes, and the film stands at 4.32% (notes/ledger/brexit-is-done.md). What this fault cost GTA is unchecked.

## The real decision
Should the kit know a person's sex and draw every woman (cast and crowd, every view, every film) on a woman's body and clothes by default, with a check that refuses otherwise? The default and the check are the big levers.

## Root cause
The kit draws a man unless told otherwise, and a person's lines cannot say "woman". The one setting that changes the body is missing from the catalogue, so chat 2 told Sam it didn't exist. Even when used, the clothes stay a man's cut. The GTA fix failed because it patched one character and left the default alone, against CLAUDE.md "Every rule and fix is for all films".

## Approaches weighed
1. **Line patch:** add `build woman` to May and Kemi. This repeats the GTA failure, and the clothes stay a man's cut.
2. **Reframe:** the kit learns sex (a `woman` word; crowds already pick it). Women get the build and women's cuts by default, and a check refuses a woman with a man's outline.
3. **Learn-first:** measure what makes a flat figure read as a woman, with no photos of a real woman. Use published sewing-pattern size tables (anonymous averages), Lucia and our game art. Then a fresh blind judge sorts headless outlines.
4. **Separate women's kit:** doubles upkeep. Rejected.

Chosen: 3, then 2, one change at a time.

## Proposal
**Learn (changes nothing, about 0.6% of a week):** draw headless front and three-quarter outlines of Blair, May and Kemi as they are, and again with `build woman`. Measure shoulder, waist and hip, neck, jacket length and shoes against the size tables. A blind judge calls each outline man or woman. This sets each number below.
**Change 1, default and check (about 1.2%):** a `woman` word on people lines, which crowd women get too, makes the woman's build the default. A castsheet check fails a woman whose waist and hip sit in the man's range in any view. It must fail both n5 pictures and pass Lucia. It runs on every cast sheet, the handover check refuses an unpassed sheet, and the rulebook gets it with n5 as its example.
**Change 2, women's cuts (about 1.5%; waits for the learning result):** only the parts the judge showed matter. Likely: a shorter shaped jacket, a softer lapel, a narrower neck, slimmer trousers, a court shoe or flat. Number to beat: the blind judge names every woman in every view.
Total about 3.3% of a week, once, for all later films. Brexit carries it on top of 4.32%.
Sam would notice: May and Kemi read as women on the next sheet.

## Sam test
Q1: an expert fixes the default and adds a check, not one line.
Q2: the evidence covers two films and the crowds.
Q3: the handover enforces the check on every sheet.
Q4: four different approaches weighed. Only this one stops a third note.
Q5: each change undoes alone.
Q6: sources named, gaps marked.
Q7: covers clothes and crowds; cheap patch rejected.
Q8: permanent kit and rule, reviewed at the film's end.

## Lost / Added
Lost: nothing. Finished films draw as before.
Added: a `woman` word, women's cuts, one check and a rule, about 3.3% of a week.

## Unchecked
GTA's cost from this fault. Whether Lucia read as a woman to Sam. How many films show crowd women at full height. Whether size-table ratios suit our flat style.
