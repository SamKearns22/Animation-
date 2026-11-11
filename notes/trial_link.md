# Trial: Link built again, the new way (budget job, 11 Nov)

**What this is.** A cost test, not a film. Young Link from Remakes is built again from scratch, from only what Sam
gave at the start (below), using the reshaped process. The question: what does one Lead character cost, and what
does the second critique hunt still find? Sam's answers: the test is Remakes, same starting information; spend what
it takes; quality as high as the real film's.

## Rules of the test (they override the usual habits where they differ)
1. **Do not open** `source/remakes_cast.py`, `source/remakes_creatures.py`, `source/remakes_panels.py`,
   `source/remakes.py`, `notes/remakes.md`, `notes/archive/remakes-*`, `notes/ledger/remakes*`, or the catalogue's
   "Passed the critique" rows for Remakes. The kit and older films' code are allowed, as on any film.
2. New code goes in `source/trial_link.py` (with a MAP). Critique packs and the ledger use the name `trial_link`.
3. **Batch work.** Draw everything, then look at it ONCE as one labelled sheet (rule 48), write ONE list of faults,
   fix the whole list in one editing pass, redraw once. Never fix-draw-look one fault at a time. Full-size crops
   only to confirm faces and joins after a batch.
4. **Two critique hunts, no third** (rule 89 otherwise as written): `critique.py pack trial_link SPEC.json`, a fresh
   helper each time, Link alone beside his references. After each hunt: list each fault ONCE (count duplicates
   listed under several lines, and count "can't tell" answers; act on a "can't tell" only if a look shows a real
   fault). Fix all real faults as one batch.
5. **Measure.** Run `python3 .claude/hooks/costwatch.py --report` at each checkpoint and write the figure in the
   Results table: C0 after reading in; C1 first full sheet drawn; C2 own-look faults fixed; C3 hunt 1 fixed;
   C4 hunt 2 fixed and confirmed. Note each helper's token total if its result reports one.
6. On amber, hand over as usual (rule 85) and say at which checkpoint; the next chat carries on and adds its cost.
7. **At the end:** one sheet for Sam: the trial Link (every view, pose and face) with references 03 and 04, and
   beside it the film's real Link made by running `python3 source/remakes_cast.py alone link OUT.jpg` (run it, do
   not read the file). Send it in the chat with a 6-line summary: cost at C4, faults per hunt (found / real /
   duplicates / can't tell), and your honest view of trial against real. Fill in Results, commit, push to the main
   line and your branch. Push notification to Sam. No next chat: the budget chat reads the results.

## What Link needs (from the plan as it stood before the build, 10 Nov)
- Estimate line: Young Link (remake design), NEW, 1.1% of a week planned. A Lead: he speaks and has close-ups.
- Views: front (his scuttle faces forward, Sam); side on for the wall two-shot (S12); the back of his cap and head
  for the S1 foreground (reference 01). No three-quarter view (rule 38).
- Faces: unsure (brows up, half smile); sceptical (one brow up, side-eye); aghast (eyes huge, mouth wide); wince;
  flat horror; deadpan (flat, half-lidded); terrified (wobbling lip).
- Poses: shrug; hands to cheeks with a jolt back; crouched front-on scuttle with hands over ears; standing still;
  held up by the collar, feet off the ground, side on.
- Height: a 9-year-old. Flat house style, circle hands (rule 41: every arm ends in a hand).
- Sam's style line at the start: "Energetic pace, exaggerated movements and enthusiasm".
- Reference pictures: `references/remakes/03-link.jpg`, `04-link.jpg` (MAIN), `01-kg.jpg` (his cap from behind),
  `09-zelda.jpg` (him beside Zelda, for size).

### The reference checklists (as written at planning)
| reference | what it shows | ours matches? |
|---|---|---|
| 01-kg (THE OPENING SHOT, Sam) | KG on a mossy branch, low camera, blue sky and white clouds; Link's woven green cap back-of-head in the left foreground, spiral pattern on it, orange hair edge. KG faces us: chunky round body, rust-brown chest, ochre-gold belly, two big swept "horn" crests of gold-tan feathers curling up and outwards, white face disc, big round blue-grey eyes in white rings with dark brows, small gold beak, white bib with two gold eye-spot circles, yellow taloned feet gripping the branch, long fanned brown tail hanging below | |
| 03-link | crouching, arm up to a light; big blue eyes, blond bowl-cut hair to the jaw, long pointed ears; green woven tunic with frayed fringes at hem and sleeves, short sleeves; brown leather strap across the chest, belt with a round silver buckle; green floppy cap with a red/brown bead band; brown boots with folded tan cuffs; wooden shield on his back. (Possibly fan art: 04 wins where they differ) | |
| 04-link (MAIN) | front, in-game: very big blue eyes, small nose and mouth, a toddler-ish round face; blond hair over the forehead; cap with red beads and a woven band; green knit shirt with a collar under a darker green tunic; chest strap, belt, buckle | |
| 09-zelda | with Link: white dress with purple hem band, purple tabard, blue sleeves, white head-cloth with purple band | |
| Look across all of them | the remake's puppet-theatre materials: woven, knitted, carved. In our flat style, kept as a few weave or feather strokes on the big areas (cap, tunic, KG's chest), not textures | |

### His lines in the brief
| 1 | All references from the 2026 remake, not the N64 game | yes: the remake designs (cast sheets) |
| 5 | Camera: looking down from KG's perspective at Link and Navi. Link: "Uh, yeah, I think so?" | yes: S2 |
| 7 | Link close up. He looks sceptical. Navi is gently nuzzling his cheek. Link: "Ok?" | yes: S4 (Navi bobs in to his cheek) |
| 11 | Camera back on Link, aghast, Navi floating: "Oh my god!" | yes: S6, Navi bobs up startled (named: no hands to cheeks) |
| 14 | Link scuttling in beside him: "I don't think I can do this." | yes: S7 (named: slides in with a bob, hands at his ears, not a crouched run) |
| 17 | Link: "This is horrible." | yes: S9 (bits falling, one onto his cap) |
| 20 | Close up of Link, deadpan: "I am 9 years old." | yes: S11 |
| 21 | KG picks him up with his wings like a tough guy by the lapels, shoves him hard against a town square wall. KG furious, Link terrified. KG hissing and spitting. Navi watches, growing redder into grenade mode. | yes: S12 (lifted to the wall by the collar; fury, spit; Navi reddening) |
| 23 | Close up on Link against the wall: "I want to go home." | yes: S13 |
| 24 | Energetic pace, exaggerated movements and enthusiasm, very little time between lines | yes: gaps 0.15-0.6 s |

### His rows of the acting list
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 2 "Uh, yeah, I think so?" | Link | S2 high angle from KG's eyes: small and unsure | eyebrows up, half smile | shrug, Navi circling | "think" |
| 4 "Ok?" | Link | S4 close-up: the doubt is the beat | one brow up, side-eye | still; Navi nuzzles his cheek | "Ok" |
| 6 "Oh my god!" | Link | S6 close-up: the reaction | eyes huge, mouth wide | hands to cheeks, jolt back; Navi startled bob | "god" |
| 8 "I don't think I can do this." | Link | S7 same wide: scuttles in at KG's side, facing forward, in from off camera (Sam, 10 Nov) | wince | crouched front-on scuttle (`GAITS['front_run']`, low), hands over ears | "this" |
| 10 "This is horrible." | Link | S9 close-up, dirt falling past | flat horror | frozen, a bit of debris lands on his cap | "horrible" |
| 12 "I am 9 years old." | Link | S11 close-up: deadpan is the joke | dead flat, half-lidded | still | "9" |
| 13 "Now listen here, you shit. You're gonna..." + 13b "And you've got some god-damn CHOICES..." | KG | S12 two-shot side on at the wall | fury, hiss, spit flecks | grabs the collar, lifts, slams on "Now" (was "Trust"); jabs his face on "shit"; shakes on "CHOICES"; Navi reddening behind | slam on "Now", shake on "CHOICES" |
| 14 "I want to go home." | Link | S13 close-up pinned to the wall | terrified, wobbling lip | feet off the ground, held | "home" |

## Results (the trial chat fills this in)
| checkpoint | cost so far (% of a week) | notes |
|---|---|---|
| C0 read in | 0.3 | chat 1 (Opus high): merge, trial brief, Build pack sections, refs on one sheet |
| C1 first full sheet | 1.0 | chat 1: `source/trial_link.py` written (head 3 views, cap, tunic, boots, 7 faces, 5 poses), sheet drawn, not yet looked at. AMBER here: handed over (rule 6) |
| C2 own-look faults fixed | 1.3 | chat 2 (Opus high): one look, 8 faults in one list (sheet overlaps, long neck, faint brows, deadpan not half-lidded, weak side-eye, shrug read as arms out, cheeks read as hands on head, collar lump on his back), one fix pass, faces confirmed full size |
| C3 hunt 1 fixed | | found / real / duplicates / can't tell: |
| C4 hunt 2 fixed, confirmed | | found / real / duplicates / can't tell: |

## Where things stand (11 Nov, chat 1 of the trial, handed over on AMBER at C1)
- Rules that bite next: trial rule 3 (batch: one look, one fault list, one fix pass), 89 (two hunts, fresh helper each), 41 (circle hands, arms one piece).
- Done: C0 0.3%, C1 1.0% (Results above). Link drawn in `source/trial_link.py` (MAP at the top); sheet: `python3 source/trial_link.py sheet OUT.jpg` (2 s); faces full size: `... faces OUT.jpg`. The sheet has NOT been looked at yet.
- Next (Opus, high effort): draw the sheet, look at it ONCE beside refs 03/04/01, write ONE fault list, fix it in one pass, redraw, crop faces/joins to confirm: C2. Then hunt 1 (`critique.py pack trial_link SPEC.json`, panels as "img"), fix: C3; hunt 2, fix, confirm: C4. Then the comparison sheet with `python3 source/remakes_cast.py alone link OUT.jpg` (run it, never read it), the 6-line summary to Sam, Results filled, push to the main line, push notification. No next chat at the end.
- Needs Sam: nothing (spend already agreed).
- Read: this file (rules of the test, What Link needs); the Build pack in `guides/job-packs.md` only if a fault needs it. Cost so far adds up across chats: add chat 1's 1.0% to yours.
- Open rule requests: none.
- For Claude: hooks in trial_link install() (B.head, V.head_view, V.arm, V.leg for who=='link'); person(img, cam, x, floor, s, yaw, j, extra, lift, t); pose(name, t); MOODS; scratch sheet at the chat's scratchpad (redraw it, don't commit drafts).
