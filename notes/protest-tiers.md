# Notes for protest-tiers (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 13 (Exceptions rows, looked at full size), 19 (filter printouts to faults), 85 (chat 17 handed over at amber).
- **Done (chat 17, 15 Nov, Opus medium; amber):** pre-flight now reads the critique (ledger name protest_tiers -> protest-tiers; gate clear: round 1 pass 2 fixed). Added to the film: 'haze' in draw_order, EFFECTS (10, each tier at its peak), JOKE_PROPS (crowbar, WAFFEN, WAFFEN RAUS placard, BANKA), BENCHMARK (from the sets'), PROP_SIZES (A-board; 'pavement a-board' in sizes.py), OUTFIT {}, LINE_SUBJECTS (6 kinds), LINE_OK, TOUCHES + ALLOWED + ORDER_SWAPS for the T2 run-in / T3 run-out / T4 melee, solids(t). BANKA sign 52 px along the bank (was cut to "ANKA"). "## Exceptions" table written (8 rows).
- **BLOCKER:** the full pre-flight now crashes in linecheck (RecursionError: head_view wraps itself: people_turned -> people_famous -> facehouse -> people_turned...), only inside pre-flight's child after install_probes; `linecheck.py protest_tiers` alone is clean except the LINE_OK row. Fix: make those head_view installs idempotent (or skip re-install), then re-run pre-flight and filter to faults.
- **Still to name to Sam with the animatic (--faults-named):** WAFFEN RAUS placard reads "RAUS" (cut by the frame edge; moving it in covers the sign swing); T4 Molotov flames are spiky cartoon tongues (also critique-left); the 4 critique faults left in chat 16.
- **Added:** "WAFFEN RAUS" placard in T2 (not in the brief); name it to Sam.
- **Sam (chat 11): "continue until animatic 1, I don't want anything to stop you".** Stage stops OFF until animatic 1 is sent.
- **Next: chat 18, Opus medium (a fix from a clear list):** fix the head_view recursion, re-run `preflight.py protest_tiers OUT`, clear or name what's left, then open Sonnet chat 19 for animatic 1 (`final OUT --small --faults-named`, finish.py, send, push notification).
- **Budget (15 Nov):** WEEK_USD 245 (provisional); estimate ~15%; re-check the meter at each handover.
- **Needs Sam:** nothing.
- **Read:** job pack "Checks and animatic" (preflight.md Stage 3); this section; the "## Exceptions" table; `source/protest_tiers.py` MAP.
- **Open rule requests:** as chat 15's list (archived), plus chat 16's (critique pass number; kittest to add), plus NEW (chat 17): the ledger's film name and the code name differ (fixed in ledger._paths; a kittest to add); JOKE_PROPS measures only a prop's centre, so a placard half off the frame edge passes.
- **For Claude:** branch `claude/protest-tiers-c17`; pre-flight logs in /tmp are gone next chat.

## Record (pre-flight reads these lines here; never archive them)
- Composition sheet sent: 13 Nov (pencil sketches, chat 4).
- Rehearsal clips sent: 15 Nov (chat 14): T1 0.0-2.0, T2 6.8-8.0, T3 10.4-12.0, T4 12.4-14.2, T4 13.6-15.6.

## Exceptions (rule 13: one row per thing left out of a check; looked at full size)
| check | who | why | looked at full size |
|---|---|---|---|
| camera feel | * | every tier is one locked-off lens (cam_for gives one fixed camera per tier: no pan, zoom or shake to feel); hard cuts only | chat 17: stills 4.4, 4.6, 13.0, 13.3, 14.1, 15.5 full size |
| LINE_OK | rioter t2 | the flagged "thin lines" are the black-bloc eye slits; the check's house weight reads 60 px because the figure is all black | chat 17: line sheet, all six kinds full size |
| TOUCHES | hauler*, runner*, swinger | T2 run-in 4.25-7.95 s: the raiders crush through one gap in the glass, read as one dark pack (depth capped 10-18 cm) | chat 17: 4.4 and 4.6 s full size |
| TOUCHES | front* | T3 run-out 10.8-11.0 s: feet 2 cm, the front line breaks as a pack | chat 17: preflight list (2 cm, one frame) |
| TOUCHES | policia*, rioter* | T4 melee 12-16 s: rioters slam into the shields (brief 26), capped 20 cm; one frame at 22 cm (policia4 into rioter6, 14.72 s) | chat 17: 13.3 and 14.1 s full size |
| FAST_OK | hauler* | T2 run-in 4.0-4.9 s at a real sprint (bodies 6.2 m/s at most, re-timed chat 18); sprinting feet swing ~2x the body, past the 7 m/s walking cap; their stone throws 5.2-7.25 s: a throwing hand really reaches ~20 m/s (cap 12) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | runner* | same: T2 run-in sprint 4.0-4.9 s; stone throws 4.6-7.25 s (hands, forearms) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | swinger | T2 run-in sprint 4.0-4.9 s (carrying the road sign) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | front* | T3: stone throws 8.7-10.65 s (hands, forearms); the run-out sprint from the jet 10.7-12.0 s | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | rioter* | T4: Molotov and stone throws 12-16 s (hands, forearms); running feet in the surge 12.9-13.9 s | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| ORDER_SWAPS | the same groups | the people cross in front of each other inside those three crushes | chat 17: same stills |
| EFFECT SHAPES | T2 flash | the star read is the flash disc plus the red crowbar end in one test layer; the flash alone is a round disc | chat 17: fx_t2 full size |
| EFFECT SHAPES | T4 Molotov flames | spiky cartoon flame tongues (critique named the same, left open in chat 16): a fire restyle is a drawing job for round 1 | chat 17: fx_t4 full size |

## The reporting: what each tier is based on is in `notes/archive/protest-tiers-reporting.md` (T1 Barcelona 11 Nov, T2 Frankfurt 31 Oct, T3 République 17 Oct, T4 Tirana 13-18 Oct).

## Plan extras (rules 24-26, 54, 55)
Estimate: **21.5% of a week, of which 8.1% unmeasured** (crowd-field moves, vehicles, light layers, animatic 1 for a motion film). (Rule 24: ~15% for 3 new + 1 place, ~26% for 9 + 3; this is 4 small new + 4 places + heavy effects.) Everyone is a **Glimpse** (wide shots, 4 s, none taller than a third of the frame): one view, one pose each, plus the run/throw/swing poses the moves need.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | est. % | measured from | spent |
|---|---|---|---|---|---|---|
| Plan, reporting, references, questions | | | plan | 1.0 | Blessed plan 1.0 | ~1 |
| Marching crowds x4 (Catalan + union flags, keys; Gen Z youth with signs and phones; tricolours + yellow vests + union banners; Albanian flags) | KNOWN `power_crime_cast` protester, placards, `flag_prop`, `board_prop`, recoloured | front and back; keys, phones over circle hands | cast | 0.4 | Blessed: KNOWN officer recoloured 0.3 (planned) | |
| Riot officer, one build, 4 forces (Mossos navy, German dark blue, French CRS, Albanian dark): helmet + visor, long shield, baton | KNOWN `armour`, officer body; NEW helmet, shield | flat Glimpse; front and side | cast | 0.7 | Glimpse unit 3.7 per 5 (11 Nov trials) | |
| Hooded black-clad rioter (hood up, face mask, black) | KNOWN `balaclava`, protester body; NEW hoodie | flat Glimpse; front, side, back; run, throw, swing poses | cast | 0.7 | Glimpse unit | |
| Moped with two masked riders; RPG launcher | NEW | flat, side-on 3/4 only as it races in (tier 4) | cast | 0.7 | Glimpse unit | |
| Critique helper for the cast | | rule 89 | cast | 0.5 | starting unit 0.5 | |
| Passeig de Gràcia at dusk, high wide down the avenue (Modernista fronts, plane trees, wrought-iron lamps) | NEW flat painting, one camera | refs es1, es2 | sets | 0.9 | Blessed sets: 5.24 for 6 paintings | |
| Frankfurt street at night, wet, gun store with steel shutter and glass front (breakable: shutter, glass sheet) | NEW flat painting + 2 breakable parts | refs: missing (Q5) | sets | 0.9 | Blessed sets | |
| Place de la République, low angle (Marianne monument, Haussmann fronts, trees) | NEW flat painting | refs fr1, fr2 | sets | 0.9 | Blessed sets | |
| Tirana avenue at dusk: bank left, the Education Ministry (yellow, grey trim, rounded corner bay) centre-right, burning sky | NEW flat painting | refs al1, al2 | sets | 0.9 | Blessed sets | |
| Burning container, burning car, burning bikes | NEW shapes; fire and smoke KNOWN `flying_whales_fx` | flat, one view each | sets | 0.3 | unmeasured | |
| Water cannon truck (tier 3 sweeping; tier 4 on its side, burning) | NEW | flat, side-on, 2 states | sets | 0.5 | unmeasured | |
| Police helicopter (hangs, hit, spins, falls) | NEW | flat; spin = 3 drawn turns, never 3D | sets | 0.5 | unmeasured | |
| Gun store break: shutter hauled up, glass sheet collapses (glints) | NEW parts; glass bursts KNOWN `prepper_fx` | only the shutter and the sheet break | sets | 0.4 | unmeasured | |
| Crowd as a field: sway, surge, keys wave, signs jab, split into two currents | NEW (risky; rehearsal clip) | thousands of flat figures moved by one field, the front ranks hand-acted | moves | 1.0 | unmeasured (Blessed's whole moves stage: 3.0) | |
| T2 rush and smash, freeze in the blue | KNOWN runs; NEW haul, swing (clip) | | moves | 0.8 | unmeasured | |
| T3 stones, canister, gas, water jet | KNOWN `launch`, `Puff`; NEW jet | | moves | 0.6 | unmeasured | |
| T4 RPG, spiral, fireball, shield break, melee, Molotovs | KNOWN fireball, fire, flashes, `launch`; NEW spiral, break, melee (clips) | | moves | 1.5 | unmeasured | |
| Light layers: dusk grades, phone lights, the blue strobe wash on wet ground, firelight backlight | NEW | per tier, laid over the painting | moves | 0.5 | unmeasured | |
| Animatic 1 (+ cold critique) | | | animatic1 | 2.0 | Blessed planned 2.0 (its real stage was 10.4 with cast rework) | |
| Notes round 1 | | | round1 | 2.7 | starting unit 2.7 | |
| Notes round 2 (motion films have needed two) | | | round2 | 2.7 | starting unit 2.7 | |
| Final (Sonnet) | | | final | 0.35 | starting unit 0.35 | |
| **Total** | | | | **21.45** | stages: plan 1, cast 3, sets 5.3, moves 4.4, animatic1 2, round1 2.7, round2 2.7, final 0.35 | |

Showstopper elements and rehearsal clips: archived (the clips are in "Moves plan").

## The world: first staging archived in `notes/archive/protest-tiers-reporting.md`; "Re-staged" below is the one built (cameras in the sets MAP).

## Re-staged with the framing lessons (PROPOSAL, framing research chat 3, 12 Nov; F-numbers: `research/crowds-and-big-action.md`)
Frame 1080 x 1920, safe area x 60-900, y 310-1500. Every tier, the same bands (F1): **headline** (country, then
location) top-left, y 330-540, over sky or dark building only; **focus** near the centre, about x 480, y 700-1100 at
each cut (F10); **foreground** y 1250-1500 dark and simple; nothing that matters below 1500 or right of 900.
**Screen direction (F11), whole film:** rioters and crowd on the LEFT moving right; police on the RIGHT (or far end)
facing left; the blue light (T2), water cannon (T3) and shield line (T4) all come from the right. The brief already
fits this; it is now locked. Camera locked and level in all four (F9). Crowds in three bands (F12): about 10 acted
near figures, 30-60 variants mid, a painted shimmering mass far.
- **T1 Passeig de Gràcia, dusk, wet (calm):** camera 12 m up behind the march, looking down the avenue, long lens
  (F2: high = the crowd reads as one river to the far end). Eye level y ~560, so the far end sits just below it.
  Bands: sky + headline (330-540); police line across the far end with the dusk sky behind it, silhouetted (F5),
  y 600-700; the river of heads and glinting keys y 700-1250, kerbs and lamp rows converging on the line (F7);
  nearest heads dark y 1250-1500. Hooded knot + burning container just short of the line, centre (x ~480, y ~760).
  Focus by beat: 0-1.5 the knot by the fire (warmest spot) as the key wave ripples from the front backward (F4);
  1.5-3.0 the bursts over the line (brightest), every head turns to them (F6); 3.0-4.0 the line's step forward.
  **Hook Text** (0.5-3.6 s) at y ~1300, over the backs of the near heads: no face there, clear of knot, bursts, line.
- **T2 Frankfurt, night, wet:** camera 2.6 m (F2: a phone held up from a bench in the chanting crowd: just above
  the heads, so the near heads sit low and never cover the window; eye level y ~1000) on the near pavement, square to
  the gun store across the street. Bands: dark building above
  + headline (330-700); the lit shop window, the brightest thing in the frame, centre (x 200-760, y 760-1150) with
  the hooded group in front of it, silhouetted against it (F5, F3); the wet street and its reflections 1150-1250;
  the crowd's backs, signs and phones 1250-1500+, all aimed at the window (F6), the ones at the right edge turned
  three-quarter so open mouths show. Runners cross left to right in front of the window. Focus: 0-1.5 the road sign
  swing (the one diagonal); 1.5-3.0 the smashed glass; 3.0-4.0 the blue wash sweeps in from the right, frozen
  swinger stays centre.
- **T3 Place de la République, day (heavier):** camera 0.8 m (F2: low = the front line towers, Marianne above
  all), eye level y ~1150. Bands: headline top-left over sky (330-540); Marianne and her drum centre (x 330-630,
  y 560-1000) against the black smoke from car and bikes, which makes her pale stone and the white gas stand out
  (F3, F5); black front line left of centre facing right, police two rows at the right edge facing left (shields
  cut by the frame), burning bikes in the gap, y 900-1250; burning car bottom-left, kiosk mid-right. Stone arcs
  cross left to right (diagonals, F9). Focus: 0-1.0 the surge behind the front line; 1.0-2.5 the gas swelling at
  Marianne's base (centre); 2.5-4.0 the water jet, a white diagonal from the right edge, the crowd splitting away
  left in one ripple (F4).
- **T4 Tirana, dusk (wildest):** camera 3 m, level, down the avenue; eye level mid-frame (y ~960), so the burning
  sky fills the top half. Bands: headline top-left (330-540); helicopter upper right (x ~760, y ~450); the
  ministry centre-right ablaze y 650-1050; bank on the left edge (ground floor only, Molotov target); shield line
  mid-right facing left, the crowd mass left and behind, y 1000-1300; mopeds bottom-left y 1300-1500. The rocket
  trail runs bottom-left to upper right: the frame's height used as one diagonal (F1). Focus: 0-1.0 the moped and
  the shot (bottom-left), the trail leading the eye up; 1.0-1.6 the helicopter hit and spin; 1.6-3.0 the shield
  break and melee (centre, x ~520, y ~1120), Molotovs smaller at the left; 3.0-4.0 the fireball behind the
  ministry backlights the melee into one silhouette (F5).
- **Cuts (F10):** T1 ends on the line (centre) -> T2 opens on the window (centre); T2 ends on the frozen swinger
  (centre) -> T3 opens on the surge (centre); T3 ends with the crowd flowing left -> T4 opens on the mopeds
  bottom-left. Lines and empty ground (F7, F8): no close-ups anywhere.
- **Changed from the brief (Sam Y, 13 Nov):** T2 crowd moves from "right half and behind the store" to the near
  pavement, seen from behind, facing the store (it still stays on its pavement); T2 store centre, not centre-left.

## Action lists (one line per group; Glimpses, nobody speaks: rule 74's acting list has no lines to plan)
- **T1:** marchers (from behind) sway forward 0.0-1.5, keys rise in a wave, heads turn toward the bursts 1.5-3.0 | hooded knot (5): one flicks the firework string 0.8, the others watch, one ducks at the bursts | police line (14, front on): still, then one pace forward 3.0, visors down | haze drifts left to right 3.0-4.0.
- **T2:** 8 runners sprint in from the left 0.0-0.6; two haul the shutter (0.4-1.0), one swings the hammer (1.0, glass falls 1.1-1.5); two slide through (1.3); one kicks a sign down (1.4); they keep smashing 1.5-3.0; all freeze mid-swing 3.2 | crowd (60+, on the far pavement): chant with signs jabbing on a beat, mouths open, phones waving; hold signs up in the glare 3.2-4.0.
- **T3:** smoke climbs from car and bikes from 0.0; crowd surges one step behind the front line 0.2-1.0 | front line (10) throws stones in arcs 1.0-2.0 | canister lands 1.6, gas swells over Marianne's base 1.8-2.5 | police rows hold, shields up | water cannon jet from the right 2.5-4.0: the crowd splits, scattering left; yellow vests at the back hold.
- **T4:** mopeds race in 0.0-0.6; passenger fires 0.6; rocket climbs 0.6-1.0, hits 1.0; helicopter spins down behind the ministry 1.0-2.0 | crowd surges into the shields 1.0-2.0, shields buckle | line breaks 2.0, melee 2.0-3.0, officers pushed back; 2 Molotovs arc 2.2-2.7 into the bank's ground floor | fireball rises behind the ministry 3.0, backlights all; final hold 3.0-4.0. No blood, no one shown hurt.

## Moves plan (chat 12, for the moves stage)
- **One film module, `source/protest_tiers.py`** with a MAP: `scene(t)` -> (tier, local time); `picture(t)` = the
  tier's painting `S.paint(tier, lt, ...)` with its people drawn in depth order (far to near) between the painting's
  back and its front layer; `draw_order(t)` for `critique.py where`. 4.0 s a tier, hard cuts; 16 s + 1.6 s sign-off.
- **Crowds in three bands (F12):** far = a painted shimmering mass (heads as flat dots moving on one noise field);
  mid = 30-60 small figures from `CROWD` variants, one pose each, swayed by the field; near = ~10 acted figures
  (cast.draw with a pose per the action lists). The field drives sway, surge, the T1 key wave (front to back), the
  T3 split into two currents (left), all from one function of (x, d, t).
- **Per tier, what moves (action lists above):** T1 key wave, firework string + 3 bursts, heads turn, the line's one
  pace, haze. T2 runners L->R, shutter haul (shutter 0.5->1), road-sign swing, glass 'whole'->'starred'->'gone' with
  glints, blue wash from the right 3.0-4.0 and freeze. T3 smoke, stones (`launch` arcs), canister + gas over
  Marianne's base, truck drives in from the right (x 9 -> 2.8, d 16) and its jet (a white tapering stream from
  truck()'s returned nozzle, spray at the end), the crowd splits left. T4 mopeds (moped_scene) in from bottom-left,
  RPG fired 0.6, trail to the heli (HELI_HOME), hit 1.0, heli spins (turn steps of 45, roll, hit=True, fire trail)
  and falls behind the ministry by 2.0, shield line buckles and breaks, melee, two Molotovs into the bank windows,
  fireball behind the ministry 3.0.
- **Light layers last:** dusk grades, phone lights (T2), the blue strobe wash (T2), firelight backlight (T4).
- **Headlines** (brief 2): white, country then location 0.5 s later, top-left y 330-540; Hook Text 0.5-3.6 s at
  y ~1300 (T1), via `hook_text`; sign-off by `finish.py` on the clean render in `source/data/`.
- **Rehearsal clips (rule 8):** T4 rocket -> helicopter spiral; T4 shield break into melee; T3 water cannon split;
  T2 smash with the blue wash (`final OUT --small --span T0 T1`).

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief, ticked before the first animatic
| # | from the brief (word for word where it matters) | done? |
|---|------|------|
| 1 | Satire style; four European protests, each tier more severe, based on actual reporting | Y, reporting above (ticked chat 16) |
| 2 | White headlines from Islamocommunism: Country, and underneath Location | Y (ticked chat 16) |
| 3 | Tier 1 a quarter showstopper, tier 4 the whole one | Y (ticked chat 16) |
| 4 | Find reporting and photos for each event | Y: reporting per tier (archive); Q5 photos (ticked chat 16) |
| 5 | T1 Spain: Paseo de Gracia, dusk, wide; wet after rain, streetlights on (11 Nov) (Sam Y, 12 Nov Q5-Q7) | Y (ticked chat 16) |
| 6 | T1 huge calm march to the vanishing point; raised key rings glint above heads (kept: Madrid that day); union flags and placards from different cities | Y (ticked chat 16) |
| 7 | T1 thin police line across the far end; small knot of hooded figures in front of the crowd beside one burning container | Y (knot at d 123, line d 150) (ticked chat 16) |
| 8 | T1 0.0-1.5 crowd sways forward, keys rise like a wave; a hooded figure flicks a string of fireworks toward the line | Y (ticked chat 16) |
| 9 | T1 1.5-3.0 three small bursts pop over the line; the crowd's heads turn | Y (ticked chat 16) |
| 10 | T1 3.0-4.0 the line steps one pace forward; a thin TEAR-GAS haze drifts through the keys (was pepper spray; 11 Nov reporting) (Sam Y, 12 Nov Q5-Q7) | Y (ticked chat 16) |
| 11 | T2 Germany: Frankfurt gun store, night, locked camera | Y (ticked chat 16) |
| 12 | T2 store centre-left, steel shutter half raised over a large glass front; wet street with reflections | Y (ticked chat 16) |
| 13 | T2 young crowd fills the right half and mid-ground behind the store, signs incl. a "Gen Z regelt" banner, a few phone lights; far end frame right dark | Y (crowd at the frame edges, chat 16; "WAFFEN RAUS" placard ADDED, not in the brief) (ticked chat 16) |
| 14 | T2 0.0-1.5 eight hooded figures sprint in from the left across the foreground; two haul the shutter up with a pry bar; a third swings a ripped-up give-way ROAD SIGN into the glass (was a hammer; dpa photo de4; shutter kept) (Sam Y, 12 Nov Q5-Q7); the sheet collapses, shards sparkle; two slide through the gap; a sign is kicked to the ground | Y (ticked chat 16) |
| 15 | T2 1.5-3.0 smashing continues; crowd chants: signs jab in rhythm, mouths open, phone lights wave; crowd stays on the pavement facing the store | Y (ticked chat 16) |
| 16 | T2 3.0-4.0 blue light and sirens at the far right end sweep across crowd and store; faces, signs, wet ground turn blue; the group freezes mid-swing; crowd holds signs up in the glare (final frame) | Y (ticked chat 16) |
| 17 | T2 VFX: road-sign impact flash, falling glass with glints, phone lights, moving blue strobe wash reflected on the street, siren cue; three light layers, blue wash last, lighting everything at once | Y (ticked chat 16) |
| 18 | T3 France (real top): Place de la République, low angle | Y (ticked chat 16) |
| 19 | T3 vast crowd of students and workers with tricolour flags (NO yellow vests, Sam Q4); CGT union banners across the back; Marianne above, graffiti on her base | Y (ticked chat 16) |
| 20 | T3 black-clad front line faces two police rows; burning car foreground-left; heaps of burning rental bikes (green Lime, Vélib) mid-right; a burning newspaper kiosk; daytime (17 Oct) (Sam Y, 12 Nov Q5-Q7) | Y (ticked chat 16) |
| 21 | T3 0.0-1.0 smoke rises from car and bikes; the crowd surges forward behind the front line | Y (ticked chat 16) |
| 22 | T3 1.0-2.5 front line throws paving stones in arcs; a tear gas canister lands among them; white gas swallows Marianne's lower half | Y (ticked chat 16) |
| 23 | T3 2.5-4.0 a water cannon sweeps in low from the right; the crowd breaks into two currents, scattering out left while the CGT banners hold at the back | Y (ticked chat 16) |
| 24 | T4 Albania (artificially placed top): Tirana avenue, dusk | Y (ticked chat 16) |
| 25 | T4 wide avenue under a burning sky; bank left; blazing Education Ministry centre-right; police helicopter high upper right; shield line mid-right; vast furious crowd behind the rioters | Y (ticked chat 16) |
| 26 | T4 zones: sky = helicopter and rocket; foreground = mopeds; mid-ground = melee; left buildings = Molotovs | Y (ticked chat 16) |
| 27 | T4 0.0-1.0 two mopeds, masked riders, race in from foreground left; lead passenger fires an RPG; smoke trail climbs diagonally toward the helicopter; crowd surges | Y (ticked chat 16) |
| 28 | T4 1.0-2.0 rocket hits; helicopter spins out trailing fire, falls behind the ministry; crowd slams into the shield line; shields buckle | Y (helicopter seen spinning to the roof line; crowd slam: melee reads weakly at phone size, named) (ticked chat 16) |
| 29 | T4 2.0-3.0 line breaks; rioters swarm over the shields, batons swinging, officers driven back; two Molotovs arc into the bank's ground-floor windows; glass blooms orange | Y (melee weak at phone size, named; Molotovs bloom 2.45 s) (ticked chat 16) |
| 30 | T4 3.0-4.0 fireball from the wreck rises behind the ministry, backlights the melee; tear gas, flares, a toppled water cannon truck burning at the line's end hold the final frame | Y (ticked chat 16) |
| 31 | T4 VFX: rocket trail, helicopter spiral with fire trail, fireball, shield impact flashes, melee dust, Molotov window bursts, ground fog | Y (ticked chat 16) |
| 32 | Violence stylised, no gore | Y (ticked chat 16) |
| 33 | (CLAUDE.md) Hook Text; CranbriJoos sign-off; no title; MP4 under 50 MB | Y at the animatic (finish.py: Hook Text + sign-off) (ticked chat 16) |

## References as checklists: `references/protest-tiers/checklist.md` (what each photo shows; ticked at each critique, rule 89 A2).

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 1 | cast sheet | Marcher t2, phone | Sam, 14 Nov: the phone held behind the head (full note archived) | protest_tiers_cast.pose/phone | fixed (chat 6), check 12 still to improve |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 12 Nov (my picks, told to Sam): hard cuts between tiers, 4.0 s each, 16 s + 1.6 s sign-off; headline country on the cut, location 0.5 s later, both held through the tier; T1 camera high behind the march (the police line really at the far end, a long lens so it reads); T3 police on the right so the water cannon enters from their side; gun store sign "WAFFEN" (no real shop name in the reporting); the helicopter falls behind the ministry with no crew shown.


## Sam's brief: word for word in `notes/archive/protest-tiers-brief.md` (every detail is in the checklist above).
