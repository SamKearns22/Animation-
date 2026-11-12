# Crowds and big action scenes: what the guides teach (Sam's note B, 12 Nov)

A PROPOSAL for the whole project, written in Protest Tiers chat 2. Nothing here is a rule until Sam picks numbers.

**Status (12 Nov): first pass only.** Built mostly from search summaries, and too much about technique. Sam: note B
is about artistic judgement and screen framing (crowds, large vistas, framing wide action, composition). The full
research job (real books, studio talks and a frame study of great crowd and battle shots) is proposed to Sam with
its cost; this page gets rewritten by it.
Each lesson names the closest existing rule or tool (rulebook and `guides/kit-catalogue.md` searched first) and says
what is new.

## Sources read (12 Nov)
- Thomas & Johnston, *The Illusion of Life* (staging: one idea at a time, read as a silhouette).
- Bruce Block, *The Visual Story* (contrast raises intensity, affinity lowers it; a diagonal move reads as more
  intense than a level one; background or toward-camera moves add contrast). Routledge and O'Reilly summaries.
- Tony Zhou, *Every Frame a Painting: Akira Kurosawa, Composing Movement* (groups band together or split apart; a
  crowd makes any feeling bigger; layer kinds of movement (weather, groups, the individual) but not all in every
  shot; cut on movement). On *Ran*: masses blocked to sweep across a locked frame; long lens stacks the ranks so armies look
  vast; a steady frame lets the chaos breathe.
- Disney, *The Lion King* stampede and *Mulan* Hun charge (Before & After interview; SIGGRAPH archive): the crowd
  system mixed parts (this horse, that rider, that hat) so no two looked alike; under time pressure the Huns were
  flat cards moved by the crowd system, not full figures.
- Digital Frontier on *The Boy and the Beast* (Mamoru Hosoda): crowds in three bands: the back done by the effects
  team as a mass, the middle by a crowd tool, only the figures near the camera animated by hand.
- Crowd "level of detail" guides (Anima, CG-Wire): hero, middle and far bands; stagger each copy's cycle start so
  copies read as different people; a badly set band edge makes figures visibly pop; extras sit in softer light so the
  main action wins; backlight turns a crowd into one big silhouette.
- The 11 Nov - 17 Oct news photos in `references/protest-tiers/` show the same thing in real life: a big crowd reads as
  a mass with a few sharp silhouettes in front (a firework, a shield line against fire, a flag against flames).

## How to sketch a big scene (read 12 Nov, used for the Protest Tiers pencil sheet)
- **Eye level is the first line** (James Gurney: "the very first line you put into your drawing", marked EL). It is
  the horizon even when buildings hide the horizon. Upshot: EL low; downshot: EL high.
- **Where heads go** (Stephanie Bower): camera at standing height: every standing head sits ON the eye-level line,
  near or far. Camera up high: near people sit low in the frame, far people climb toward the line. Camera low:
  near heads tower above the line, far heads sink toward it.
- **Value before line** (Proko, SVS, Creative Bloq): a thumbnail with the values right reads from across the room;
  line alone does not. Group many things under one shadow value. **Nearer is darker** (Dave Pimentel).
- **One focus:** "the focus of interest should be the only object of that size, shape and value in the scene"
  (Creative Bloq); the highest contrast marks it (Pimentel, after Bill Peet).
- **Depth from overlap and line weight:** far lines thinner, near lines thicker; overlap things in perspective or the
  drawing goes flat (Pimentel; Creative Bloq).
- **Lean every pose** unless it is meant to be stiff (Walt Stanchfield via Pimentel). A riot line standing straight
  against a leaning crowd is the stiffness used on purpose.
- **Silhouette test:** fill the pose solid; if the action no longer reads, redraw it (Creative Bloq).
- **Thumbnails first:** tiny frames, several, pick the one that tells the point best, then enlarge it (Creative Bloq).
  A low horizon gives clean silhouettes and depth.
- **Pencil marks that look hand-made** (Meraj, Wyvill, Isenberg, Gooch & Guy 2008, "Mimicking hand-drawn pencil
  lines"): the hand eases in and out (Flash & Hogan's minimum-jerk curve); short lines stay nearly straight, long lines
  wander more (control points every 0.5, 0.3 or 0.2 of the stroke for short, medium, long lines), with a small
  sideways "squiggle" at each control point; graphite is darkest along the middle of the stroke and fades to the sides;
  the paper's tooth breaks it up (Sousa & Buchanan). Our `pencil_cartoon.Canvas` already does tooth, grain, pressure
  and wobble.

## Proposed lessons (pick by number)
| # | lesson | closest rule or tool | what is new | where it would go |
|---|---|---|---|---|
| C1 | **Three bands.** Near: at most ~12 hand-acted figures with real Glimpse poses. Middle: a few variant figures on cycles. Far: a painted mass that only shimmers (heads bob, keys and flags glint), no single bodies. A figure never changes band during a shot. | estimate row "crowd as a field"; `power_crime_cast` crowds of 2,000; rule 6 (no popping) | a fixed recipe with counts per band; band changes banned (stops pops) | `guides/best-practice.md`, new section "Crowds and big action" |
| C2 | **No twins in step.** Every copy gets its own start point in its cycle, its speed changed by up to 15%, and a colour or prop variant; two copies of one figure never stand side by side. | rule 6 and `audit.py` (pop-in test) | an automatic twins check in the same audit (by-hand turned into a check); merges into rule 6, no new number | rulebook rule 6 |
| C3 | **One focus per beat, led by contrast.** The crowd stays in affinity (similar tones, small moves); the beat's action owns the strongest contrast in the frame (brightest light, strongest colour, the one diagonal). A squint test on each beat's frame: blurred, the hottest spot sits on the action. | rule 10 (framing and timing); best-practice 1.3 "Staging" | the squint test as a check on the beat frames; merges into rule 10 | rulebook rule 10 |
| C4 | **A crowd is one mass with one change.** It moves one way, then changes once (surge, split, turn, freeze). Reactions ripple out from the cause, nearest first, a few frames per rank, never all at once. | best-practice "Eyes lead"; rule 74 (acting list) | ripple timing, and one change per crowd per tier written in the action list | best-practice, same section |
| C5 | **Escalate with direction, keep the camera still.** Calm tiers move level and slow; the wildest tier is full of diagonals (rocket, falling helicopter, Molotov arcs). The camera stays locked so the chaos reads. | rule 10 (no diagonal cameras) | the diagonals come from the action, not the camera; used to rank the tiers | best-practice, same section |
| C6 | **Scale from depth and silhouette.** Long lens to stack the ranks; backlight (fire, strobe) to turn the mass into one silhouette; far bands darker and softer. | S7 house look (light top edge, soft shadow) | crowd lighting by band | best-practice, same section |
| C7 | **Cut on movement.** Each hard cut between scenes lands on a move (a burst, a swing, a flash) so the tiers flow into each other. | rule 10 | cut points chosen on a moving beat | best-practice, same section |

Plus Sam's other open request: **pencil sketches first.** Rough pencil sketches of each scene as Sam pictures it, sent
before any check sheet. Closest: rule 11 (one rough composition sheet before building). New: the sheet is drawn as
pencil sketches. Merges into rule 11's wording if Sam wants it for every film.
