# Notes for Bingo Bingo (source/polanski.py; one file, numbered; mark each done as it is fixed)

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | - | Zack: lighter skin, much lighter facial hair (from Sam's four photos) | done 14 Oct (faded sides, receding temples, short light salt-and-pepper beard) |
| 2 | card close-ups | 21-46 s | never show the other options before he reads them (no spoilers) | done: unread items blurred out of focus; focus racks to each item as it is read |
| 3 | shout | ~4.9 s | subtitle exactly "Zionism IS racism!" | done (plain caption, not all-capitals) |
| 4 | opening | 0-5 s | desk against the wall; Zack starts with his back to us, spins round to the advisor for his interjection | done (back view, 0.3 s spin) |
| 5 | all | - | use the new fluid arms and legs (Cry Minister) | done: merged the Cry Minister branch; limbs.py, walker.py, satire audit |
| 6 | all | - | no robot voice on animatics (stand-ins only for timing) | done |
| 7 | card close-ups | 21-46 s | reveal by the camera's frame, never blur | done v3: card laid out as a brainstorm sheet (1 top left, 2 top right, 3 across the bottom); close-ups at 10.5x hold one item; checked in `checks()` |
| 8 | walk-in | 0-2.5 s | the walk looks horrible | v3 cheat: he walks behind a cloth-covered campaign table in the foreground (legs hidden, body bob and sway); proper walks wait for the movement system |
| 9 | the turn | ~4.3 s | flips like paper | v3: cut on the action (head and cheek come round in the wide; the close-up finishes the turn); proper turns wait for the movement system |
| 11 | card | ~24 s | reveal "Shoplifting" only as he reaches the word | done v4: card stays face down until the word, then flips in 0.25 s; items 2 and 3 land on "North Sea" and "Nuclear"; while turning the card only carries item 1 |
| 12 | the turn | ~4 s | swivel and thin, then suddenly round in the next shot: use South Park's method | done v4: one shot, real drawings swapped view by view (views.py), the head a drawing ahead; a second render with four directions only (TURN4=1) for Sam to choose |
| 13 | the turn | ~4 s | try a straight 180 | done: TURN180=1, back view to front in one drawing, hands on the desk until the pop |
| 14 | the shout | ~4.6 s | "why this pose?" (arms straight out, forearms hanging, eyes shut) | done: held key poses for the arm raise (desk, beside the head, up), no blink through the shout |
| 10 | foreground | 0-20 s | the laptop sat on a giant grey box | done: a campaign table with a green VOTE GREEN cloth to the floor; everything on it lies low (nothing in front of the card) |

Decisions made (kept so a long session or a new session never has to rediscover them):
- Card spoilers: a 9:16 frame wide enough to read one line always holds the whole card, so framing can't hide the
  other items; shallow focus does.
- Stand-in voices (espeak-ng) time the film until Sam records; they are never heard in anything sent to Sam.
- Finger guns: the one named exception to circle hands (a stub finger and thumb).
