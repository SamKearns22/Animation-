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
