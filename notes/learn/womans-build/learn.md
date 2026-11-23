# Learn step: what makes our drawn woman read as a woman (Open Wounds chat 4, 23 Nov)

Sam's Y to option 1 (notes/proposals/womans-build.md "Final version"). Changes nothing; this is what was learned.
Sheets: `outline-as-now.jpg` (headless black outlines), `colour-as-now.jpg` (the same, in colour). Rows: May as now,
May + the existing `build woman` (GTA's Lucia build), Kemi as now, Kemi + `build woman`, Blair (a man: the control,
Sam 23 Nov "obviously, Tony Blair is a man"). Views: front, three-quarter, side, back, seated three-quarter.
Drawn by `draw.py` + `sheet.py` (here). Judge: a fresh helper that saw only the 25 outlines, shuffled, at phone size
(`judge1.txt`, key `judge_key.json`).

## The blind judge (25 headless outlines)
| who | front | 3/4 | side | back | seated 3/4 | read as a woman |
|---|---|---|---|---|---|---|
| May as now | man 5 | man 4 | man 1 | man 2 | man 4 | 0 of 5 |
| May + build woman | man 5 (tie and lapels) | man 4 (tie, lapels) | woman 3 (chest, waist) | woman 2 | man 4 (tie, lapels) | 2 of 5, weak |
| Kemi as now | man 2 (boxy) | man 1 (box) | man 1 (box) | man 2 (boxy) | man 1 (box) | 0 of 5 |
| Kemi + build woman | woman 2 | man 1 (box) | woman 3 | woman 2 | woman 1 | 4 of 5, all weak |
| Blair (man) | man 5 | man 4 | woman 2 | man 2 | man 5 | man 4 of 5 |

Confidence 1 (a guess) to 5 (obvious). Both n5 complaints confirmed: as drawn, May and Kemi read as men in all 10 views.

## Measured against sewing-pattern size charts (anonymous body tables, no photos of anyone)
Ottobre regular fit (women EU 38, height 168: bust 88, waist 70, hip 96 cm, back width 35.6; men EU 50, height 180:
chest 100, back width about 40); Simplicity UK 14 (bust 98, waist 80, hip 108). Front widths taken as shares of each.
| measure | women (charts) | men (charts) | our build woman | our man / house body |
|---|---|---|---|---|
| hip over shoulder width | about 1.0 | about 0.84 | 0.80 (a man's) | 0.83-0.88 |
| waist over bust | 0.80 | 0.88 | 0.76 | 0.92 |
| hip over bust | 1.09 | 1.0 | 0.84 (a man's) | 0.86 |
| narrowest waist (units below the neck) | about 225 | about 260 | 275 (low) | none |
| widest hip | about 350 | | 360 | |
| jacket hem width | at the hip, flared | box, straight | box (0.85) | box |

## What matters (ranked by what the judge named and the measures)
1. **The neckline.** A strip down the middle of an open jacket reads as a man's shirt and tie at 4-5 (May's striped
   blouse in its narrow V, in 3 of 5 views, even on the woman build). A woman's neckline: a wider, shallower opening,
   the blouse spread across it, no centre strip; smaller lapels set higher.
2. **Hips as wide as the shoulders**, the waist higher (about 225) and narrower (0.70 of the shoulders). Our build has
   a man's hip-to-shoulder ratio, so front and back still read as a box.
3. **Three-quarter and seated views get the shape too.** The build does nothing visible there now (judge: "neutral
   box"): the arms and the straight jacket hide it.
4. **Arms that show the waist:** the elbow in at the waist, the forearm out over the hip (the rig's arms angle out
   from the shoulder, so they cover the sides).
5. **A shorter, shaped jacket** ending at the hip, following the waist and hip, not a straight box hem.
6. Never named by the judge at phone size: trousers, shoes, neck. Slimmer trousers and a woman's shoe stay small
   touches, not the fix. Kemi's work boots only for likeness.

## Found on the way (why nobody saw it)
- **The cast file's body lines never reached May or Kemi.** People drawn on a face tool head (`head: house ...`) drop
  every body setting except height: `shoulders 138`, `build woman`, `arms`, `hem` were silently ignored. So adding
  `build woman` to their cast lines would have changed nothing on the sheet. Fixed in Change 1.
- Crowds already pick a woman or a man per member (height, lashes, lips) but never told the body.

## Every woman in every cast file
| film | women | state |
|---|---|---|
| blessed | guard2, juror2, juror4, juror6, juror7, juror9, juror11; women in the press crowd | finished: draws as before |
| facetool | kemi | test file |
| grand-theft-autism | lucia (`build woman`), her; women among walkers and cops | finished: draws as before |
| milburn | goth, waif | finished: draws as before |
| protest-tiers | wife, granny; women among the protesters | finished: draws as before |
| brexit-is-done | may, kemi | this film: Change 1 and 2 |
