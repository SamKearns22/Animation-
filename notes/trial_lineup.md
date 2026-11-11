# Trial 2: the line-up five as Glimpses (budget job, 11 Nov)

**What this is.** A cost test, not a film. Trial 1 rebuilt Link (a Lead) for 2.0% of a week. This trial measures the
"Glimpse" tier: the five characters of Remakes' line-up shot (Young Zelda, Malon, Saria, Princess Ruto, the Goron in
a frilly dress), on screen once, for about 3 seconds, in one wide shot. They are built from only what Sam gave at
the start (below). Sam: the test is Remakes, same starting information; spend what it takes; the quality on screen
as high as the real film's.

## Rules of the test (they override the usual habits where they differ)
1. **Do not open** `source/remakes_cast.py`, `source/remakes_creatures.py`, `source/remakes_panels.py`,
   `source/remakes.py`, `source/remakes_sets.py`, `notes/remakes.md`, `notes/archive/remakes-*`,
   `notes/ledger/remakes*`, or the catalogue's "Passed the critique" rows for Remakes. The kit, older films' code and
   trial 1's `source/trial_link.py` (the child body; read its MAP, then only the lines needed) are allowed.
2. New code goes in `source/trial_lineup.py` (with a MAP). Critique packs and the ledger use the name `trial_lineup`.
3. **The Glimpse tier.** Each of the five gets ONE view (front), ONE pose (below) and one small reaction on
   "ROMANCE". No turnaround, no side or back view, no faces sheet, no character drawn alone at full size. They are
   judged ONLY as the audience sees them: all five standing in the line-up frame (1080 x 1920, framed as the shot
   would be, a plain flat backdrop with a ground line: the town set is not part of this test), at phone size, with
   one 2x crop of the same frame to confirm faces and joins. Detail that cannot be seen at that size is not drawn.
4. **Batch work.** Draw all five, look ONCE at the line-up frame, write ONE list of faults, fix the whole list in one
   editing pass, redraw once. Never fix-draw-look one fault at a time.
5. **Two critique hunts, no third:** `critique.py pack trial_lineup SPEC.json`, a fresh helper each time. The panels
   are the line-up frame and its 2x crop beside each character's MAIN reference; tell the helper the owl who
   gestures at them is not in this test. After each hunt list each fault ONCE; count duplicates and "can't tell"
   answers; fix all real faults as one batch.
6. **Measure.** `python3 .claude/hooks/costwatch.py --report` at each checkpoint, into the Results table: C0 read in;
   C1 first line-up drawn; C2 own-look faults fixed; C3 hunt 1 fixed; C4 hunt 2 fixed and confirmed. Note each
   helper's token total.
7. On amber, hand over as usual (rule 85) and say at which checkpoint; the next chat carries on and adds its cost.
8. **At the end:** one sheet for Sam: the trial line-up frame at phone size and its 2x crop, and under it the film's
   real five (run `python3 source/remakes_cast.py castsheet OUT.jpg`; do not read the file). Send it in the chat
   with a 6-line summary: cost at C4, faults per hunt (found / real / duplicates / can't tell), and your honest view
   of trial against real AT THE SIZE THE SHOT SHOWS THEM. Fill in Results, commit, push to the main line and your
   branch. Push notification to Sam. No next chat: the budget chat reads the results.

## What the five need (from the plan as it stood before the build, 10 Nov)
- Estimate lines: Young Zelda, Malon, Saria: NEW, line-up only, front view, small idle acting, 1.2% for the three.
  Ruto, the Goron in a frilly dress: NEW (new body types), line-up only, front view, 1.0% for the two.
- Poses: Zelda unsure; Malon dutiful, "pick-me", kind (holds a milk bottle); Saria spunky, confident, "he's already
  picked me" (hand on hip, ocarina; she winks on "ROMANCE"); Ruto vain and pushy, preening, NOT sexual (she is a
  child; Sam: "100% correct"); the Goron slightly drooling, in a frilly dress.
- Heights against Link (1.33 m): Malon slightly shorter; the Goron about Link x 1.6; the others about Link's height.
- Flat house style, circle hands (rule 41: every arm ends in a hand).
- Reference pictures: `references/remakes/07` to `16` (MAIN: 08 or 07 Ruto, 10 Zelda, 12 and 11 Goron, 14 Malon
  right half only, 16 Saria).

### The reference checklists (as written at planning)
| reference | what it shows | ours matches? |
|---|---|---|
| 07-ruto | full body: pale grey-white smooth skin, a big teal domed fish head-fin sweeping back, purple eyes with lashes, small smile; teal fin "top" at the chest, teal fins hanging from forearms and hips; hands on hips; bare feet, pink toes. Child proportions | |
| 08-ruto | front, hands on hips, the same; confident, smug | |
| 09-zelda | with Link: white dress with purple hem band, purple tabard, blue sleeves, white head-cloth with purple band | |
| 10-zelda (MAIN) | seated three-quarter: green eyes, blond hair, pointed ears; white cloth veil and purple padded headband with a gold triforce plate; gold collar; purple tabard with embroidery; puffed pale-blue sleeves; white skirt; holds the blue ocarina. Gentle half smile | |
| 11-goron | full body: smooth, bright yellow-orange, egg-shaped head and body in one, short stubby arms and legs, rocky grey patches on the back, a small pale tuft on top of the head, big grin. About Link's height x 1.6 | |
| 12-goron (MAIN face) | close: round dark purple eyes, small black brows, a small nose, a wide smile line, a white goatee point under the chin, round belly | |
| 13-malon | white dress with a blue horse-pattern hem, yellow neckerchief, long red hair, hands clasped, kind face, slightly shorter than Link | |
| 14-malon (RIGHT HALF only: the left is the N64 game) | long red-orange hair, blue eyes; yellow neckerchief with a brooch; grey-brown knit blouse with blue embroidered short sleeves; brown belt; brown patterned apron over a purple skirt with a blue meander hem | |
| 15-saria | sitting on a stump playing the ocarina, eyes closed; green fairy beside her; green hair, green outfit, boots | |
| 16-saria (MAIN) | front: bright lime-green bob with a fringe, blue eyes, pointed ears; dark green high-collar top, lighter green tunic with a swirl pattern, a fringed shoulder; pendant; a brown belt with a bead; green shorts; holds a wooden ocarina; soft confident smile | |
| Look across all of them | the remake's puppet-theatre materials: woven, knitted, carved. In our flat style, kept as a few weave or feather strokes on the big areas (cap, tunic, KG's chest), not textures | |

### The brief's lines
| 18 | KG gesturing at a line-up in Hyrule town square: Young Zelda (unsure), Malon (dutiful, 'pick-me', kind), Princess Ruto (preening: see Lost), a slightly drooling Goron in a frilly dress. | yes: S10 |
| 18b | Sam, 10 Nov: add Saria to the line-up (spunky, confident, 'he's already picked me') | yes: S10, Saria winks on "ROMANCE" |
| 19 | KG: "FIVE ROMANCE OPTIONS TO CHOOSE FROM" (Sam, 10 Nov: was FOUR) | yes: S10 |

### The acting list's row
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 11 "FIVE ROMANCE OPTIONS..." | KG | S10 wide line-up: everyone must read | game-show grin | wing sweeps along the line | each reacts on "ROMANCE"; Saria winks at Link, already sure |

## Results (the trial chat fills this in)
| checkpoint | cost so far (% of a week) | notes |
|---|---|---|
| C0 read in | 0.2 | chat 1 (Opus high). The chat's own start (prompt and rules) was 0.1 of it |
| C1 first line-up drawn | 1.2 | chat 1. Includes a 2-hour stop (the usage limit ran out at 14:57; resumed 17:07), so the whole chat was re-read once: the reload is part of the jump from 0.2. Code: `source/trial_lineup.py` (about 600 lines), drawn first time with no crash |
| C2 own-look faults fixed | 1.4 | chat 1. One look, 9 faults, one editing pass, one redraw: Goron too wide (clipped, over Ruto); its clasped hands on the bodice read as a bust (A1, rude shape); boxy Goron arms and legs; dress too high (lace over the goatee), thin grin; Ruto's dome a small swim cap; Ruto's face read bored; Ruto's legs and feet like a mannequin's shoes; both ocarinas hidden by hands. Amber at C2: handed over |
| C3 hunt 1 fixed | 2.3 | chat 2 (Opus high; 0.9 of it, incl. its start 0.1). Helper 1: 94,661 tokens. found 16 / real 14 / duplicates 12 / can't tell 1. Not real: Ruto's forearm fins (drawn; hands on hips put them at the hips); 'a reaction needs frames' (one still by the test's design). Fixed in one pass: Ruto's head-fin now a big hood dome sweeping back (no eye-like dot), eyes open and smug (was shut, read cringing), her hand pats the dome beside it; Zelda's brows and sideways glance unsure; Malon holds the bottle out to us in one hand; Saria's bob fuller and rounder (read as a boy); Goron a pear with shoulders, arms hanging from them, drool a small drip, its back rocks dropped (read as headphones); an automatic layout: nobody touches, margins kept, the five as big as the width allows (scale 0.47 against 0.48 before: the Goron's shoulders and Malon's arm cost the gain); the crop now holds the Goron's whole face. The pass took 5 redraws, not 1 (layout and the hidden bottle needed checking) |
| C4 hunt 2 fixed, confirmed | | found / real / duplicates / can't tell: |

## Where things stand (11 Nov, chat 1 handed over on amber at C2)
- Rules that bite next: the test's 4 (batch fixes), 5 (two hunts, no third), 6 (measure each checkpoint).
- Done: C0-C2. The five are built in `source/trial_lineup.py` (MAP at the top).
- Next (Opus, high; chat 2): `python3 source/trial_lineup.py spec 1` (renders the frame and crop, writes the SPEC),
  then `python3 source/critique.py pack trial_lineup PATH` and a NEW helper; then C3, hunt 2, C4, the end steps
  (rule 8) and the cost breakdown (`git pull` of the main line, `python3 source/costbreak.py`, its printout under
  "## Cost breakdown" naming each chat, in the Results commit). Add chat 2's cost to chat 1's 1.4.
- Known after the redraw, not yet judged: the Goron's dress hem touches the frame's right edge in the crop.
- For Claude: draws only into `source/data/trial_lineup/` (keep it off git); faults go in this table, not code comments.


## Cost breakdown
Chat 1 (eea64ed9, Opus high), at the amber handover after C2:
```
eea64ed9: 41 steps, 1.46% of a week
  kind of step                                   steps  re-read     new  written   total
  shell (other)                                     13     0.10    0.15     0.16    0.41
  talk (reply or thinking, no tool)                  4     0.00    0.31     0.00    0.31
  run a tool (draw, check, critique)                 8     0.09    0.04     0.11    0.24
  write or edit code/notes                           1     0.01    0.00     0.20    0.21
  git (merge, commit, push)                          5     0.05    0.02     0.03    0.11
  read a guide                                       6     0.04    0.03     0.01    0.08
  look at a picture                                  3     0.03    0.02     0.00    0.06
  start-up (the app, CLAUDE.md, the first message)     0     0.00    0.04     0.00    0.04
  other tool: ReadNotifications                      1     0.00    0.00     0.00    0.01
  ALL                                                      0.32    0.64     0.51    1.46
```
