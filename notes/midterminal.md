# Notes for MidTerminal (one file, numbered; mark each done as it is fixed)

## Where things stand
- **Rules that bite next:** 49-51 (likeness: Trump needs a pack), 28 (reuse before building), 11 (composition sheet before shots)
- **Done (4 Nov, Opus):** cast built (Satan new, Epstein measured 79% 1st of 7, Trump rebuilt 32% 2nd of 7: not passing); Oval Office set built, four cameras.
- **Spent against the estimate (rule 55):** no estimate yet (no brief); cast and set about 8% of a week.
- **Next:** Sam's look at the cast and set; then the brief (story, lines). Planning: Opus, high effort, same chat while short.
- **Needs Sam:** Trump likeness pack (3+ straight-on, not smiling; a three-quarter; a talking one); the story.
- **Read:** guides/satire.md 'Start' and 'Getting it right first time'.
- **Lost / Added:** Added: our own simplified seal (eagle in a ring, no words); generic portraits (no real face).
- **Open rule requests:** none.
- **For Claude:** `source/midterminal_cast.py` (MAP at top; `sheet`, `faces`, `head`), `source/midterminal_set.py` (`test`, `refs`); refs in `references/midterminal/`. Satan's wings: `spread` 0..1 (default 0.2). Trump's rosebud pout: `pout=True`.

## The brief as a checklist
| # | from the brief or a note | done? |
|---|------|------|
| 1 | Oval Office set from Sam's five photos: gold curtains, blue carpet (Sam's pick 1) | yes |
| 2 | Flat cartoon style (pick 2: Y) | yes |
| 3 | Satan: humanoid, suited (refs satan-1, -2); horns and wings from ref 2, kept modest (my pick; Sam didn't answer) | yes |
| 4 | Jeffrey Epstein (3 refs), dark polo (Sam's pick) | yes |
| 5 | Donald Trump (3 refs) | likeness 32%: needs photos |

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| oval-1 | gold swag valance, 3 windows, Resolute desk, leather chair, flags, navy carpet, seal, chairs, busts, alcove | yes (busts on side tables, not the desk) |
| oval-3 | fireplace with portrait, cream sofas, yellow armchairs, grandfather clock, flowers, phones | yes |
| oval-5 | room from above: oval, 4 pedimented doors, alcoves | yes |
| satan-1/2 | black suit, red tie, gold pin, pocket square, slicked black hair, red eyes; horns, red wings | yes |
| epstein-1..3 | grey swept hair, tanned lined face, half-smile, dark polo | yes |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|

Decisions made:
- Carpet texture is 1 px a cm; close-ups on the seal look a little blocky: redraw it at 2 px a cm if a shot goes close.
