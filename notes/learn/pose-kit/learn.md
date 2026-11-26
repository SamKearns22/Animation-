# pose-kit-format Learn (R7 chat 13, 26 Nov; changes nothing)

Sources (one filtered pass): Sam's own words per chat (`notes/ledger/sam/*.md`, the handover log of every message he
typed), every R7 handover (`notes/archive/r7-handovers.md`), the cost record (`notes/ledger/r7.json`). The full
transcripts were not re-read: the saved logs already hold every typed message from Sam, and the handovers hold each
chat's dead ends. One list_events read of chat 1 showed the same messages as its log.

## 1. R7's chats: each Sam note or dead end, the layer it sat on, what would have caught it, its cost

Cost is % of a week (ledger). Layers: B = body, O = posted outfit, L = lower garments (trousers, seat, shoes, lap),
M = method (no layer: the way of working), C = cost record.

| chat | cost | note or dead end | layer | what would have caught it |
|---|---|---|---|---|
| 1 | 2.64 | Hand-drawn seated lower body (one shape, ball-knee check). Photo sites refused; Sam: "Always ask for permissions when a site fails" | M, L | Reference photo first, with a site that refuses asked about at once (Plan pack; now pose-kits.md step 2) |
| 2 | 3.33 | Retuning the no-bottom check and knee outlines by hand; judges' faults | M | Two flat rounds stop (rule 87): chats 2-4 each scored 2-3 |
| 3 | 1.95 | Photos found, then crossed legs, shoe and cloth patched view by view; judges "one dark mass", "no knees" | M, L | Same: the drawing method, not the photos, was the limit |
| 4 | 3.16 | Profile outlines, shading, staggered feet; scores still 2-3 | M | Rule 87 stop; nothing from chats 1-4 is in the passed look |
| 5 | 2.23 | Sam (24-25 Nov): "No bum/circular knees", "the legs look awful", "costing huge unacceptable expenditure". Judged proposal: 3D legs | M | A cost record that showed the true total (C1, now built). The method change came from Sam, not from a check |
| 6 | 2.32 | The measured body's legs (solid_seat). Sam: "already looking 100% better" | B | Kept: first sign the body is the right tool |
| 7 | 2.30 | Seams between solid legs and flat torso patched. Sam: "Is there a more intelligent way?" "Should we be building *all* our characters in the way Jason was built?" | B/O edge, M | A seam check between layers; and starting from the whole body, outfit on top |
| 8 | 2.31 | Mode 'body'. First try redrew her clothes: "you changed her clothes?", "You have drawn a poor version of it". Then "This pose is 100% correct", "she is FINALLY correct". Last note: "Way too curvaceous from this angle" | O, then O/B edge | An outfit diff against the posted look (C2's "refuses a redrawn outfit"); the turned-curves check (built chat 10) |
| 9-10 | 2.18 | Bust: "a very small amount of bust bump in the 3/4 poses". Purple under the jacket hem (side). "Shoes clipping on 3/4 view", "Confused shoe shapes on side view". Upright apart: "a bearing the crotch pose", "her purple jacket dips inward in a triangle" | O/B edge, L | turned_curves, jacket_under_hem, shoe_faults, apart_faults: each built after Sam's note, proved on his frame. All four are edges between layers. A photo of someone sitting relaxed with legs apart would have shown the "apart" pose before Sam did |
| 11 | 1.34 | Apart fixed by joint targets (sitting._leg_by_knee). Sam: "codify what succeeded", then "I'm not sure you have understood the crux ... the full body model and then layering clothes separately" | M | Reading the whole R7 record before writing the proposal (the first draft missed the crux) |
| 12 | 2.54 | Format judged and picked; booking fixed; guide written | C, M | Kept |
| other | 0.76 | a7520791 (0.65: preflight faults, partly R7), 2c60330e (0.11: "What is the essential fault?", booked twice) | C | Booking by --film (C1, built) |

What it adds up to: chats 1-5 and 7 (15.6%) bought nothing that is in the passed look. Every note after chat 8 fell
where two layers meet (outfit over body, hem over trousers, trousers over shoe, jacket over the lap). No check looked
at those edges until Sam named each one. Twice the outfit layer was redrawn when it should have been left alone, and
both times Sam caught it at once.

## 2. Kemi and Blair seated on the full body, under their posted outfits (mode 'body', no change to any code)

Sheets (posted look above, full body below; five views): `learn-sheet-kemi.jpg`, `learn-sheet-blair.jpg`. Seams at
full size: `learn-seams-kemi.jpg`, `learn-seams-blair.jpg`. Raw results: `learn-checks.json`. Script: `learn_sheet.py`
(scratch: it writes into the folder it is given). May drawn the same way as the control (the look Sam passed).

### What a viewer sees (full size, every seam)
- **Both, the legs are better than their posted look** in every view: thighs run forward, knees are part of the leg,
  bottoms sit on the seat. The body carries to a man and to a second woman without any per-person setting.
- **Kemi front and front apart:** the thighs bulge out past her vest at the knees in two side lobes. This is the
  pressed flesh spreading (SPREAD), tuned on May's wider jacket. A stranger would see swollen knees. **No check
  catches it in 'upright'**: the "wider than the jacket" test only runs on the apart pose.
- **Front apart (both):** the vest/jacket dips in a triangle between the thighs, with no trousers under it, the same
  fault Sam marked on May. Caught (apart_faults). Blair's legs are barely apart. Kemi's spread wider than her vest
  (caught).
- **Crossed (both):** the top thigh is one dark wedge, wider than the torso, with a lumpy outline, and the crossed
  foot hangs out to the left. Kemi has 6 leg-through-leg points (caught by leg-leg crossings; chat 6 named the same
  6). The dark wedge reads as "one dark mass" again (the old judges' note). No body-mode check looks for it.
- **Blair side:** a block of trouser rises above the lap in front of his jacket hem, a square step where the
  solid trunk's seat meets the flat jacket. **Not caught**: 'jacket under the hem' looks for jacket colour only, and
  this is trouser colour.
- **Kemi side:** her bottom shows behind the vest's back edge as a shelf. Small, but it is an outfit/body edge.
- **Shoes:** look right at full size on both.

### Which checks carry, miss or cannot run
| check (where) | Kemi | Blair | verdict |
|---|---|---|---|
| seat crossings (`solid_seat.checks`) | 0 | 0 | **carries** |
| leg-leg crossings | 6 crossed | 0 | **carries** (true fault on Kemi, known since chat 6) |
| trousers / shoes one piece | 0 | 0 | **carries** |
| jacket under the hem | 0 | 0 | **carries for its own fault**, but **misses** Blair's trouser step (it reads jacket colour only) |
| turned curves (`views.turned_curves_fault`) | 1 (bust bump 8, 3/4 and crossed) | 0 | **misreads**: it measures her posted vest, which is unchanged, so it marks the posted look. Its limit was set from Sam's note on May. Needs a limit per person, or a comparison with the posted look |
| shoe faults (`solid_seat.shoe_faults`) | 1 (front, apart: "gap" 4 columns) | 1 in 4 views ("trousers through the shoe" 6 columns) | **false alarm**: at full size the shoes look right. The near leg in front of the far shoe is counted as poking through |
| apart faults (`solid_seat.apart_faults`) | spread + triangle | triangle | **carries** (both true) but runs only on the apart pose; in 'upright' it would have caught Kemi's knee lobes |
| seated look, no bottom (`castsheet.seated_look`) | 0% every view | 21-36% | **cannot run on the body**: it fires on May's passed front (84%) and on every Kemi/Blair view, where the bottoms are plainly there. It was tuned on the hand-drawn legs; a dark jacket over dark trousers defeats it |
| seated look, ball knees / one tone | none | none | carries, but **misses** the crossed dark wedge |

**For C2:** run seat crossings, leg-leg, one-piece, jacket under the hem and apart faults, as they carry. Fix before
trusting: shoe faults (count occlusion as no fault) and turned curves (compare with the posted look, not a fixed
number). Retire no_bottom in mode 'body'. Three new edge checks are missing, each needing a saved example first:
(1) thighs wider than the torso in front views (Kemi's knee lobes), (2) trouser block above the lap at the jacket's
hem (Blair side), (3) crossed top leg wider than the torso / one dark mass (both crossed). These are only findings,
not Sam's notes, so per rule 5 each needs his frame or his Y before it becomes a rule.
