# Framing crowds, big vistas and wide action: lessons for every film (framing research job, 12 Nov)

A PROPOSAL for the whole project (rule 86, Learn first). **Nothing here is a rule until Sam picks numbers.**
Built from the sources in `notes/framing-research.md` "Findings" and the 16-frame study sheet
`research/framing-study.jpg` (frame numbers below are the sheet's). The rulebook and `guides/kit-catalogue.md` were
searched first: each lesson names the closest rule, check or kit piece and says what is new. The first pass's
technique notes (C1-C7, pencil marks) are folded in where they still count; the pencil technique stays in git history.

**Where they would go, so the rulebook does not grow (CLAUDE.md):** the know-how goes in `guides/best-practice.md` as
a new section **1.3c "Framing big scenes"**; only three short additions touch rules, each merged into one that exists:
rule 10 (framing planned up front), critique S1 (the eye goes to the action) and rule 6 (crowds never pop).

## The lessons (pick by number)
| # | lesson | closest rule or kit piece | what is new |
|---|---|---|---|
| F1 | **Our wide shot is tall.** A 16:9 vista loses two thirds in 9:16 (sheet 2: 3 riders of 9 survive). Stack the layers top to bottom (sky event / target / mass / foreground), each in its own band of the safe area (x 60-900, y 310-1500), not side by side (sheet 3, 14, 15). A long diagonal (a rocket trail, a jet of water) uses the frame's height. | `guides/tiktok-design.md` safe area; critique S5 (front, middle, back layers) | Layers planned as horizontal bands of the tall frame, written per shot, with the headline and Hook Text given their own band. |
| F2 | **Eye level first, and where heads go.** Choose the camera's height for what the crowd must read as: at standing height (1.7 m) every standing head sits on one line, near or far: we are among them (8, 12, 13, 14). High up, the crowd becomes a river or a knot: we see its shape (5, 6, 7). Low, the near ones tower: heroic or threatening. Mark the eye-level line on every rough. | rule 10 (camera distance); rule 1 (cameras in the plan, metres) | Camera height chosen for a stated reason per shot; the eye-level line drawn on the rough and its height in px written in the plan. |
| F3 | **One focus per beat, the only one of its kind:** brightest, warmest, or the only upright or dark thing (3 fire, 8 the dark armed figure, 12, 16). Two hot spots only if far apart and joined by a line or a move (15). **Squint test:** blur the phone-size frame; the hottest spot must sit on the beat's action. | critique S1 (the eye goes to the action); first-pass C3 | Each beat names its focus and what makes it the only one; the squint test becomes a check (a small tool blurs each beat's frame and finds the hottest spot, against the focus box the plan names): turns S1's by-hand look into a check. |
| F4 | **A crowd is one shape with one value, and one change.** Against a plain ground the mass reads as one dark or light block; heads all one way (affinity, Block) make the one change (ripple, surge, split, turn) read at once (6, 7, 2). Reactions ripple out from the cause, nearest first, a few frames per rank. | rule 74 (acting list); first-pass C4 | One value per crowd per shot in the plan; one change per crowd per beat in the action list, with its ripple direction. |
| F5 | **Backlight makes the silhouette** (13, 2): fire, a burst or bright sky behind the mass turns its edge black and makes the crowd one shape; cool on one side, hot on the other. | S7 house look (light top edge, soft shadow); `flying_whales_fx` fire | A light plan per shot: where the light sits relative to the crowd (behind for silhouette), set before the painting. |
| F6 | **Watchers point the eye:** backs in the foreground all looking one way aim us at the focus (9); faces lit only where they matter (10). | rule 10 ("who looks where"); `LOOKS_AT` eyelines | `LOOKS_AT` extended to crowds: near watchers' heads aimed at the beat's focus, checked the same way. |
| F7 | **Lines lead in:** road edges, kerbs, lamp rows, tram lines, smoke streaks run to the focus (4, 6, 13). | critique S2 (roads lead somewhere) | The set's strongest lines are placed to meet at the focus, not just to be real. |
| F8 | **Emptiness is scale:** small figures, big empty ground, long shadows (1). Few close-ups (Ran, Children of Men): the wide shot is the drama. | rule 24's Glimpse (none taller than a third of the frame) | Leave empty ground on purpose; no close-up in a crowd shot unless a beat needs a face. |
| F9 | **Chaos needs one clear moving thing and a level, still camera** (11; Lubezki's objective distance; Boucard's long lens; Gavras: "we only followed one guy"). The wildness comes from diagonals in the action, never from tilting or shaking the camera. | rule 10 (no diagonal cameras); `camfeel.py` (rule 72: fast or un-eased camera moves flagged); first-pass C5 | One named mover per chaotic beat for the eye to follow; tiers ranked by how many diagonals their action has. |
| F10 | **Centre the focus when cutting fast** (16; Mad Max: "cross hairs on her nose"): each shot's focus near the middle of the safe area (about x 480, y 900), and the movement at a cut leads to where the next shot's focus sits (eye trace). | first-pass C7 (cut on movement); rule 10 | Focus position at each cut written in the plan; the last move of one shot points to the next shot's first focus. |
| F11 | **Screen direction fixed per side** (Ran: each army always enters from its own side), held across the whole film, even between different places. | best-practice 1.3 (the 180-degree rule); `guides/satire.md` movers keep their direction | Held across separate locations, not only across cuts within one place. |
| F12 | **Far crowds are tiny and simple; near ones few and acted** (Prince of Egypt, Mulan, The Boy and the Beast). Three bands: near, at most about 12 hand-acted figures; middle, a few variants on cycles; far, a painted mass that only shimmers (heads bob, things glint). No figure changes band mid-shot; no two copies in step side by side (each starts its cycle at its own point, speed varied up to 15%, colour or prop varied). | rule 6 (pop-in test); `power_crime_cast` crowds of 2,000; first-pass C1, C2 | The band recipe with counts; a twins check added to `audit.py` (by hand turned into a check), merged into rule 6. |

## What would change in the rulebook (only on Sam's numbers)
- **Rule 10** gains one sentence (F1, F2, F9, F10, F11): "For each shot the plan names the camera height and why, the
  eye-level line, the layers as bands of the 9:16 safe area, each beat's focus (centred where shots cut fast) and
  each side's screen direction; the camera stays level and still in chaos."
- **Critique S1** gains (F3, F6, F7): "the squint test: blurred, the hottest spot is the beat's focus; near watchers
  and the set's main lines point to it". Tool: a small squint check (about 0.2% of a week to build, priced before).
- **Rule 6** gains (F12): "no two copies of one figure in step side by side". Tool: a twins test in `audit.py`.
- F4, F5, F8: know-how only, in best-practice 1.3c.

## Still to learn (Sam, 12 Nov, Blessed note 42; runs at the end of Blessed)
Dramatic framing of every beat of a screenplay, not only crowds (shot size, height, headroom, where the face sits,
what the frame leaves out). Blessed's dock shot (note 37) is the worked example; it re-uses this page and is priced
before it starts.
