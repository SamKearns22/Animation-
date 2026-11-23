# Proposal: Women in the cast are drawn on a man's body

Status: open

## Problem
On the Brexit Is Done cast sheet v2, Sam said: "Can I just say...I'm not sure we have female bodies? Kemi's body
seems much more like a man's." Theresa May and Kemi Badenoch are both drawn with the same straight-sided body,
legs and shoes as Tony Blair, only a little narrower. A woman in our films should read as a woman from her body
and clothes at phone size and at full size, in every view, without Sam having to ask. Sam also does not want us
to search for photos of a real woman's body ("I'm not sure I want to google 'Kemi Badenoch's body' lmao").
Nothing told us this was wrong before Sam saw it.

## Facts
- Sam's words: notes/ledger/sam/xsxkqfcf.md (last lines); saved with pictures in notes/sam-notes/brexit-cast-v2/
  (n5-kemi-body-like-a-mans.jpg, n5-may-body.jpg).
- Chat 2 told Sam the kit has no woman's build. That is only partly true: source/body.py FIGS (lines ~523-526) has
  a 'woman' figure (a chest narrower than the shoulders, a waist at 0.67 of the shoulders, hips back out to 0.85),
  made for Grand Theft Autism's Lucia (20 Nov). A cast line turns it on: `body: ..., build woman`
  (source/people.py ~417). It shapes the front torso (body.front_outline), the turned torsos
  (views.torso_outline -> _built_outline, its docstring: "a woman's bust, waist and seat" in the side view) and the
  vest/tank tops (people_parts.vest_outline).
- story/brexit-is-done-people.txt: May (`body: 1.73 m, shoulders 138`) and Kemi (`body: 1.7 m, shoulders 140`) name
  no build, so both get the default man's body; Blair `body: 1.83 m` (house shoulders 150).
- Lucia's line, story/grand-theft-autism-people.txt line 18: `body: 1.68 m, shoulders 140, head 62 x 94, neck 0.85,
  hem 440, build woman, arms 27, legs 0.96`. How she looked to Sam: unchecked (GTA notes in notes/archive/).
- Other body settings a line can already give: `arms N` (house 30), `legs K` (leg thickness, views.leg leg_k),
  `neck K`, `hem N` (jacket length). Shoes: one house shoe, plus `trainers` (people.py ~525); no women's shoe
  (no heel, court shoe or flat). Outfits: suit, jumper, dress, blouse; extras include `skirt` (Milburn).
- The suit's front (body.py ~586-600) and turned (views.torso_view ~684-697) drawings are one cut for everyone:
  a man's lapels and collar; May's jacket is this suit in plum with `open collar` and `extras: pattern`.
- Crowds: people.crowd_person (~249-280) picks a woman 45% of the time and gives her shoulders 134-146 and a
  shorter height, but never the woman figure: every crowd woman in every film has the man's body too (unchecked how
  many films show crowd women at full height).
- Checks: castsheet.py match compares a person's front with her own three-quarter (colours); nothing compares a
  body with whether the person is a woman. Rule list: guides/film-quality-rules.md (search "woman": unchecked).
- Sam's standing rules: every fix goes in the shared kit for all films; no rule without a working check that has
  caught a saved example (CLAUDE.md "Rules are permanent").
- Film use: May is seen seated, turned three-quarter (brief item 1, notes/brexit-is-done.md); Kemi standing on a
  building site, interviewed (item 5); both full figure on the cast sheet.

## Record
notes/brexit-is-done.md
notes/sam-notes/brexit-cast-v2/
notes/ledger/sam/xsxkqfcf.md
story/brexit-is-done-people.txt
story/grand-theft-autism-people.txt
source/body.py
source/views.py
source/people.py
source/people_parts.py
source/castsheet.py
notes/archive/
guides/film-quality-rules.md
guides/kit-catalogue.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 6c9014497e145089 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes: mild. The facts list the existing `build woman` switch, the one man's suit cut, the one house shoe and the crowd code in detail, which points helpers toward "switch on the build and add women's clothes". It names no remedy outright; all three versions treated the switch as one option only.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 3 | 2 | 3 | 15 |
| V2 | 4 | 4 | 3 | 4 | 4 | 19 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
## Sam test
Q1: Yes, as improved. An expert fixes the default (the kit draws a man unless told), adds a check that would have caught n5 on its own, and learns which clothes matter before building them. V3 alone used a measuring check only; the viewer's judge from V2 is added.
Q2: The evidence covers two films (GTA's Lucia note, 20 Nov; Brexit n5, 23 Nov), every cast file and the crowd code (checked: only Lucia's line has `build woman`; crowd_person never sets the figure). The learn step now covers every view, seated and standing, in each woman's own outfit, with Blair as the control; no photos of a real woman.
Q3: Root cause found with evidence: an opt-in build no woman gets by default, no field saying who is a woman, one man's cut of clothes, and no check, so the GTA critic could close "box body" as house style. The check runs on every cast sheet and the end-of-chat check refuses an unpassed sheet, so it does not rely on a chat choosing to read a rule. Measured by: both n5 pictures fail, Lucia and the new sheet pass, and no women's-body note from Sam on the next three films.
Q4: Four different approaches were weighed (patch two lines, change the default, learn first, a separate women's kit); learn, then default and check, then clothes, is the best and the only one that stops a third note.
Q5: Finished films draw as before (no word, no change). Each part undoes alone. The blind judge is not trusted until it fails both n5 pictures and passes Lucia and Blair; if it cannot, Sam is told plainly and only the measuring half runs.
Q6: Sources named; unchecked: how Lucia read to Sam, the judge's reliability, the clothes' cost in every view, GTA's cost from this fault, V1's "almost nothing changes" trial (no saved sheet).
Q7: Not the cheap version: clothes are built in this film before cast sheet v3, not left for a later film; the two-line patch is rejected because it already failed once.
Q8: Permanent kit parts, one rule with its saved example, reviewed at the film's end.
## Pick
V3
## Why
V3 sizes the remedy by learning first, at the smallest honest cost (about 3.3% against V2's 7%), uses Blair as a control and tests the existing build before building anything new, and makes the check bite through the end-of-chat check and the rulebook. Its weak spots were a measuring-only check (Sam's first rule: look as a viewer, not a measurer), a learn step without the seated view May is filmed in, and "Lost: nothing". From V2: the blind viewer's judge as the standing check's second half, the seated view and outfits in the learn step, every person line carrying the word, crowds passing their flag through. From V1: the concrete clothes list (a woman's jacket cut with higher, smaller lapels, a shorter shaped jacket, slimmer tapered trousers, court shoe, flat or work boot) as candidates for the learn step to rank, the observation that hanging arms may hide the waist (to be tested, not assumed), and keeping the old figure under its name for finished films. V1 lost on bundling six changes before any learning and on an unrecorded trial; V2 lost on cost and on letting the clothes wait for the next film.
## Faults in the pick
- F1 [fixed] The learn step left out the seated three-quarter view May is filmed in and each woman's own outfit; both added.
- F2 [fixed] The check only measured waist and hip, which can pass while the body still reads as a man in a man's jacket; a blind viewer's judge at phone size is added and must catch both n5 pictures before it is trusted.
- F3 [fixed] "Lost: nothing" was wrong: every new woman's cast line must say so; stated as Lost.
- F4 [fixed] Clothes could slip to a later film; they are built in this film, before cast sheet v3, limited to what the learn step shows matters.
- F5 [named] Whether a blind judge can tell a woman's body at phone size is unproven; if it cannot sort the saved pictures, it is not used and Sam is told.
- F6 [named] Cost is an estimate: about 3.3% once, possibly up to 5% if clothes are needed in every view; Brexit stands at 4.32% before animating.
- F7 [named] V1's trial (the existing build barely shows at full height) has no saved sheet; the learn step redraws and saves it.
- F8 [named] Crowd women in finished films keep the man's body; the ledger counts repeated notes only within one film, so this cross-film repeat was missed; not fixed here.
## Final version
**Learn (changes nothing; about 0.6%).** Draw Blair, May and Kemi headless, as they are and with `build woman`, front, three-quarter, side, back and seated three-quarter, each in her own outfit, at phone and full size; save the sheet. Measure shoulder, slope, waist, hip, neck, jacket length and shoes against published sewing-pattern size tables (anonymous averages, no photos of a real woman), Lucia and the GTA game art. A fresh blind judge calls each outline man or woman. Rank V1's clothes candidates by what the judge and measures show matters. List every woman in every cast file.

**Change 1, default and check (about 1.2%).** Every person line carries `woman` or `man`; pre-flight refuses a new cast line without it; `woman` turns on the woman's build; crowd women pass their flag to the body. Finished films keep their drawing (the old figure stays under its name). A cast-sheet check fails a woman whose outline sits in the man's range in any view, and the blind judge reads each woman at phone size; trusted only after both n5 pictures fail and Lucia and Blair pass. The end-of-chat check refuses an unpassed sheet; the rulebook gets the rule with n5 as its example; the kit catalogue lists the build.

**Change 2, women's clothes (about 1.5%; this film, before cast sheet v3).** Only the parts the learn step ranked: likely a shorter shaped jacket with smaller lapels set higher, slimmer trousers, a court shoe or flat, Kemi's work boots. In every view through the existing build outline. Number to beat: the judge names every woman in every view.

Sam sees cast sheet v3 before any shot is built. Total about 3.3% once, for all later films.
## For Sam
### Option 1: Learn, then a woman's body by default, with a check
Problem: Women in our films are drawn on the same box-shaped man's body and clothes as Tony Blair, and nothing warned us before you saw it. This is the second film you've noticed it in (Lucia was the first).
1. First a test that changes nothing: draw May, Kemi and Blair as outlines, standing, turned and seated, to find exactly what makes a drawn woman read as a woman, using sewing-pattern size charts, not photos of anyone.
2. Every person in the cast list is marked woman or man, and every woman, crowds included, gets a woman's body shape by default in every film.
3. A check on every cast sheet: it measures the body's shape, and a fresh helper that hasn't seen the cast list says "man or woman" at phone size. It only counts once it catches both of your pictures from this note.
4. Women's clothes, only the ones the test shows matter: likely a shorter shaped jacket, smaller lapels, slimmer trousers, a woman's shoe or Kemi's work boots.
5. You see a new cast sheet before any shot is built.
Why: The last fix changed one character only, so the fault came back; this changes the default and adds a check that would have caught it.
You'd notice: May and Kemi look like women on the next sheet, and so do women in crowds and future films.
Other option: the same steps, costing about twice as much, with the clothes as a separate yes, possibly in a later film.
Lost: every new woman in a cast list must be marked as a woman; about 3.3% of a week once (maybe up to 5%).
Added: a woman's body by default, women's clothes, one check and one rule.
### Option 2: Learn more widely, three separate yeses
Problem: Women in our films are drawn on the same box-shaped man's body and clothes as Tony Blair, and nothing warned us before you saw it. This is the second film you've noticed it in.
1. A wider test that changes nothing: May and Kemi drawn on a woman's body at five turns, seated and standing, in their outfits, listing what still looks like a man.
2. Your first yes: every person is marked woman or man, and women, crowds included, get a woman's body.
3. Your second yes: a fresh helper says "man or woman" for each person on every cast sheet, trusted only once it catches both of your pictures.
4. Your third yes: women's clothes for what the test listed, which may wait for the next film to stay within budget.
Why: Each change can be judged and undone on its own.
You'd notice: more questions from me, and May and Kemi may still wear a man's jacket in this film.
Other option: Option 1, all in this film for about half the cost.
Lost: every new woman must be marked; about 7% of a week once.
Added: a woman's body by default, the check, women's clothes later.
