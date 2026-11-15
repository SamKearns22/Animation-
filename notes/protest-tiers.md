# Notes for protest-tiers (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most)
- **ON HIATUS (Sam, 15 Nov): no work on this film until the deeper problems are solved** (`notes/proposal-route.md`). Animatic 3 stands as sent; Sam's notes on it come when the film resumes.
- **Rules that bite next:** 30 (a repeated note: find why the first fix failed), 85 (cost watch), 66 (no old file stands in for a new render).
- **Done (chat 31, Opus medium, 15 Nov): Sam's note 1 on animatic 2 ("frames missing") fixed.** Why the first fix failed (rule 30): chats 14/25 skipped over mid-throw/mid-swing instead of fixing the arm (a skip sized to one build; blends still folded the elbow), and `--faults-named` let a stopped drawing through as black. Now the throwing/swinging hand swings round clear of the shoulder (`protest_tiers_cast._clear_of_shoulder`), blended arms are re-bent until the guard passes them at the actor's turn (`protest_tiers._resolve_mixed_arms`), skips removed. Tested: the 3 spots draw; all 1,243 throws/blends in t2-t4 at every drawing pass the guard; clips of 7.5-8.7, 14.3-15.5, 20.2-21.4 s: no black frame (darkest mean 73), sent to Sam.
- **Paused (15 Nov, Sam via parent chat):** the page.py `show` job is paused, to be redone through the new proposal route (notes/proposal-route.md). Its work is on branch `claude/page-tool-c1946` and was ALREADY on the main line (1787a2f, wired into the round pack, rule 61 and handover start) before the pause; not reverted, waiting on Sam.
- **Tool (15 Nov, Sam's Y, film untouched):** a notes round now looks at code in one step per note: `python3 source/page.py protest-tiers show "note words"` (~40 lines; the round pack, rule 61 and `handover.py start` point to it).
- **Ledger:** stages 'round1 moves' and 'animatic2' marked done (both were finished; the hook was reading the old stage). Film 53.2% of a week; Sam's Y covers ~60%.
- **Next: Sam's notes on animatic 3: Opus medium** (deciding and fixing; clips with `final OUT --small --span T0 T1`; splice fixed seconds into `animations/drafts/protest-tiers-animatic.mp4`, video only, animatic time = clean/1.1 + 0.065). Then Sam's Y before any full render.
- **Chain stopped (chat 31):** create_session refused: lineage depth 8 (a platform limit). Sam asked: 1 Opus renders animatic 3 here; 2 he starts the Sonnet chat.
- **Animatic 3 made by splice (chat 31, Sam sent animatic 2 back; no redraw):** the 3 fixed spots (clean 7.5-8.7, 14.3-15.5, 20.2-21.4 s, stamped clips) overlaid on animatic 2 (video only, its sound untouched; animatic time = clean/1.1 + 0.065). No dark frame (816 checked), seams looked at. Saved as `animations/drafts/protest-tiers-animatic.mp4` (rule P16 written; finish.py saves future ones with the clean render). Picture faults still named as in animatic 2 (71 named, not fixed).
- **Needs Sam:** notes on animatic 3; Y/N to the proposal "a stopped drawing never ships" (chat 31's message).
- **Read:** job pack "Notes round"; this section; "## Exceptions".
- **Open rule requests:** the 'a stopped drawing never ships' proposal (film_engine: a stopped drawing refuses the render even with --faults-named; finish.py scans for black frames) was answered (Sam, Y): written as rule P17, naming not blocking. P16 is written.
- **For Claude:** branch `claude/protest-tiers-c31` (= main line). finish.py's --film is the module name `protest_tiers`.

## Round 1 notes (Sam, 15 Nov, on animatic 1): proposals answered (chat 19), planned (chat 20), nothing built yet
- Q1 (chat 20, open): the honest price of everything asked is ~29.3% more, the film near 63.5% (his Y was ~43-47%). 1 Y go to ~63.5% (my pick); 2 stop at 47% for a look at what exists.
Sam's answers: 1 Y the tourist husband says "Hey!"; 2 Albania's intensity shows 11 from the start (no jump); 3 gags a, b, c (Molotov seller's cart, selfie in front of the falling helicopter, granny throws a Molotov overarm); 4 Y tourists: cap, shorts, bum bag, camera, "Greetings from Tirana" tote, crouched behind bins; 5 Y each tier gets new action, never slow motion (T2 second wave carries stock out, TV or mannequin; T3 second volley, truck pushes forward, a burning car rolls); 6 Y go ahead at ~43-47% of a week for the film.
- [ ] R1 (brief row 34) The joke: each tier is worse until Albania, which is off the charts; Albania's riot is not a protest, it is how they spend their time.
- [ ] R2 (rows 35-37) New end scene: (a) a second RPG moped pulls up, two riders, fires at something in the sky off screen; rioters clash with police behind; someone says "Hey!" and they look to the side. (b) a side alley: two American tourists cowering, husband and wife; he says "We're just tourists! Why are y'all protesting?" (c) back to the riders: one says "Bro, what's a 'protest'?"; the other shrugs.
- [ ] R3 (row 38) Under each place heading, slightly smaller red text "Intensity Level:" 2, 4, 8, 11 out of ten.
- [ ] R4 (row 39) Tier lengths 4 / 6 / 8 / 10 s (Spain, Germany, Paris, Albania); re-pace each scene to fit.
- [ ] R5 (row 40) Albania is the showstopper: the most fluid, best-designed effects; lean into gleeful violence and absurdity.

## Round 1 plan (chat 20, 15 Nov, Opus high; Sam said go; nothing built yet)
**Estimate: about 29.3% of a week more, so the film lands near 63.5%** (34.2% spent; 1.6% of the new work is
unmeasured). Sam's Y was ~43-47% (chat 19's range, which chat 19 itself called low): asked again (Q1 below). Ledger:
`ledger.py` has the stages below as `round1 plan/cast/sets/moves`, `animatic2`, `round2`, `final`, each share = its price.
Units from this film's own ledger: a new Glimpse 1.3 (cast stage 5.96 for 4 builds, critique in), a painting or prop
0.6 (sets 4.74 for 8 pieces), action 0.6 per second (moves 11.3 for 16 s, less the crowd field and light layers, reused);
a Lead 1.9 (Remakes' real cost per character, `notes/budget-job.md`).

| thing, build or risky move | KNOWN / NEW (closest kit piece) | tier, why, parts seen | stage | est. % | measured from |
|---|---|---|---|---|---|
| This plan | | | round1 plan | 1.5 | chat 1's plan, 1.53 |
| Husband, American tourist: baseball cap, polo, shorts, bum bag, camera on a strap | NEW on the people kit + house head | Lead (speaks); front only, chest up over the bin; mouths on his take, head life | round1 cast | 1.9 | Remakes 1.9 a character |
| Wife: sun visor, sunglasses pushed up, "Greetings from Tirana" tote | NEW, people kit | Support (gasps); front, chest up; one pose + the gasp | round1 cast | 1.3 | Glimpse unit 1.3 |
| Granny: headscarf, cardigan, long skirt, shopping bag on her arm | NEW, people kit | Glimpse; one view (3/4 not needed: side-on throw); reach, overarm throw | round1 cast | 1.3 | Glimpse unit |
| Molotov seller + his cart (apron, flat cap, moustache; cart with striped umbrella, crates of bottles, a little flame, a hand sign "MOLOTOV 200 LEK") | NEW (cart: nothing in the catalogue) | Glimpse; front; light, hand over, applaud | round1 cast | 1.3 | Glimpse unit |
| Selfie rioter (peace sign, phone up, back to the helicopter) | KNOWN rioter + marcher phone pose | Glimpse | round1 cast | 0.3 | KNOWN recolour line |
| Moped riders at 2-3x their T4 size: rim light (critique: they merge into the road), head turns, the shrug | KNOWN `moped_scene`, rioter | Lead by rule 24 (one speaks) but masked: no mouths; head life on the voice | round1 cast | 0.6 | unmeasured part 0 (KNOWN) |
| Cast critique helper (rule 89) | | | round1 cast | 0.5 | starting unit |
| Side alley, front on: two wheelie bins, graffiti, drainpipe, laundry line, fire glow at the far mouth | NEW painting (closest: the sets' Tirana avenue palette) | one camera | round1 sets | 0.6 | painting unit 0.6 |
| End shots A and C: the T4 avenue through a tighter `Reframe` (same painting, no new set) | KNOWN `Reframe`, T4 painting | side-on, bottom-left of the avenue | round1 sets | 0.1 | |
| Props: flat-screen TV, camo hunting mannequin, boxes (T2); traffic cone, bike wheel (T3) | NEW small | flat, one view | round1 sets | 0.3 | prop unit, half each |
| Re-time to 4/6/8/10 s + end scene; Intensity line; the 4 picture-check singles; Marianne's olive branch | edit `scene_of`, `overlay` | | round1 moves | 0.6 | unmeasured |
| T2 +2 s: the second wave carries stock out; the freeze moves to 5.2 | KNOWN runs, carry grips | | round1 moves | 1.2 | 0.6 a second |
| T3 +4 s: second volley, the truck pushes forward, the burning car rolls into the jet (steam) | KNOWN `launch`, truck, car | | round1 moves | 2.4 | 0.6 a second |
| T4 +6 s: the 3 gags, the melee redone so it reads, the gleeful hold | KNOWN throws, phone; NEW vault, shield flip | | round1 moves | 3.6 | 0.6 a second |
| T4 effects (R5): round flickering flames (no spikes), smoke dark at the base and lit orange from below, round window blooms, a rolling fireball, embers, fireworks in the hold | edit `flying_whales_fx` fire/smoke (catalogue line 35) | | round1 moves | 1.0 | unmeasured |
| End scene 7.6 s: skid, RPG, "Hey!", the turn, his line (mouths, head life), "Bro...", the shrug; stand-in voices for timing; captions | KNOWN `mouths`, `headlife`, `subtitles`, espeak stand-ins | | round1 moves | 4.6 | 0.6 a second |
| Moves critique helper | | | round1 moves | 0.5 | starting unit |
| Animatic 2 (36 s, ~30 min render, cold critique) | | Sonnet | animatic2 | 2.5 | animatic 1: 2.13 for 16 s |
| Notes round 2 | | | round2 | 2.7 | starting unit |
| Final | | Sonnet | final | 0.5 | 0.35 + the longer render |
| **Total** | | | | **29.3** | |

**Smarter, not less (already in the price):** shots A and C reuse the T4 painting through a reframe (no new street);
the couple are seen chest-up over the bins (no legs, no walk); riders and the selfie rioter are built pieces; stand-in
voices time everything, so Sam records once and nothing is re-cut.

**Build order (the joke first, so the costliest part is right first):** 1 re-time + Intensity line (the skeleton,
cheap); 2 cast: husband, wife, seller + cart, granny, riders larger (one critique pack); 3 alley + props; 4 end scene
(clips: A skid + fire, C the shrug); 5 T4 effects, gags and melee (clips: selfie + helicopter, seller to the granny's
throw); 6 T2 and T3 extensions (clip: the car rolling into the jet); 7 checks, stand-in timing, captions, animatic 2.

### Beat list (times in seconds from each shot's cut; no slow motion: every added second is new action at full speed)
Film: T1 0-4, T2 4-10, T3 10-18, T4 18-28, end 28-35.6, sign-off 1.6 s: **37.2 s**. Hard cuts throughout.
Headings as now (country on the cut, place 0.5 s later), then **"Intensity Level: 2/10"** at 1.0 s, red (the
blue-strobe-safe red of the T4 fire, about 220 40 40), about 80% of the place line's size, under the place line,
left-aligned with it, held to the cut; T4 reads **11/10** from its first frame like the others (no count-up); no
headings in the end scene. Check: the third line stays over sky or dark building in all four (T1: above the line at y 600).
- **T1 Spain (4 s, Intensity 2/10): unchanged.** Hook Text 0.5-3.6 as now.
- **T2 Germany (6 s, 4/10):** 0.0-3.0 as now (runners, shutter, road sign, glass, slide through, A-board, smashing).
  **3.0-5.0 NEW:** the second wave comes back out through the gap jogging right: one with a flat-screen TV, two
  carrying a camo hunting mannequin like a plank, one with a tower of boxes; two smashers start on the second pane;
  the crowd's phones swing to follow them. **5.0-6.0** the blue wash sweeps in from the right (was 3.0-4.0); all
  freeze at 5.2, the mannequin frozen in the same pose as its carriers; crowd holds signs up.
- **T3 France (8 s, 8/10):** 0.0-2.5 as now (smoke, surge, first volley, canister 1.6, gas on Marianne).
  **2.5-4.0 NEW** second volley, twice the throwers: stones, a traffic cone, a bike wheel; impact flashes on the
  shields; gas keeps spreading. **4.0-5.5** the water cannon drives in from the right, jet on at 4.5, the crowd
  splits (was 2.5-4.0). **5.5-6.5 NEW** the truck pushes forward about 1.5 m, the jet sweeping. **6.0-8.0 NEW** four
  rioters shove the burning car (foreground left) into the gap; it rolls toward the police; the jet hits it at 7.2,
  a burst of steam; the crowd flows away left (so T4 opens bottom-left, as now).
- **T4 Albania (10 s, 11/10; the showstopper):** 0.0-1.0 as now (mopeds, RPG at 0.6, hit at 1.0).
  **1.0-2.6** the helicopter spins down at its present rate with more turns (longer fall, same speed), fire trail,
  drops behind the ministry at 2.6 with a small fireball. **1.2-2.8 gag b:** mid-ground, a rioter turns his back to
  it, phone up at arm's length, peace sign; the phone flashes at 2.6 as it lands; he checks the photo, thumbs up.
  **1.0-4.0** crowd slams the shields (1.0-2.0), the line breaks 2.0; melee redone to read at phone size: rioters
  vault the shields, one shield spins up into the air, officers shoved back, clear silhouettes against the fire;
  no one hurt. **3.0-6.0 gag a:** by the bank, the seller's cart; three rioters queue; he lights a rag and hands
  over a bottle at 3.4, 3.8, 4.2; each buyer throws at once; arcs 3.6-5.6 into the bank's ground-floor windows,
  round orange blooms. **6.0-7.4 gag c:** a granny steps up, pays, takes one, throws overarm at 6.6: the highest,
  longest arc of the film, over the melee into the bank's first floor at 7.3, the biggest bloom; the seller
  applauds; rioters cheer, fists up. **7.5** the fireball rolls up behind the ministry and backlights everyone.
  **8.0-10.0** the gleeful hold: crowd jumping, flags waving, fireworks bursting overhead, the toppled water cannon
  burning at the line's end; round flickering flames and embers everywhere.
- **End scene (7.6 s, no headings), Sam's R2:**
  **A (2.4 s), the T4 avenue reframed tight on the bottom-left, side-on:** 0.0-0.5 a second moped skids in from the
  left and stops (dust and tyre smoke); 0.8 the passenger fires the RPG up and out of the top of frame (backblast,
  trail climbing off the top right); behind, rioters clash with police at mid distance. 1.6 **"Hey!"** (the
  husband, off screen left, captioned); 1.8-2.1 both riders snap their heads round to the left.
  **B (2.8 s), the side alley, front on:** the couple crouched behind two wheelie bins, chest up over the lids.
  0.0 the wife gasps (hand to mouth). 0.3 the husband rises a little, palms out: **"We're just tourists!"**
  (0.3-1.4), **"Why are y'all protesting?"** (1.5-2.6). Both look screen right (where the riders are).
  **C (2.4 s), tighter reframe of A, the two riders:** 0.1 the driver turns his head back to the passenger:
  **"Bro, what's a 'protest'?"** (0.2-1.3); 1.4-2.0 the passenger looks to camera and shrugs, big, one palm up, the
  RPG on his shoulder; hold to 2.4. Hard cut to the sign-off.
  Times are set by the stand-in voices (espeak, for timing only, never heard in anything sent: best-practice
  "Straight to the animatic"); Sam's takes replace them line by line.

### The acting list (rule 74; the three lines; tone is clear from Sam's joke, so no questions)
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Hey!" | husband (off screen) | A: off screen, so the riders' turn is the beat | (not seen) | (not seen) | the riders' heads turn on "Hey" |
| 2 "We're just tourists! Why are y'all protesting?" | husband | B: front on, chest up over the bin: his fear is the set-up | brows up and together, eyes wide, looking right; mouth on the take | rises from the crouch, palms out at "tourists", one hand flicks toward the street on "protesting"; head life on the voice | "tourists", "protesting" |
| (gasp) | wife | B: beside him | eyes wide, brows up | hand to mouth, clutching the tote | 0.0 |
| 3 "Bro, what's a 'protest'?" | driver (masked) | C: two-shot: the sincere puzzle is the punchline | masked: eyes squint, brows knit (the mask hides the mouth) | head turns to the passenger, a small tilt on "protest" | "protest" |
| (shrug) | passenger | C | brows up, blank eyes to camera | big shrug, one palm up, RPG on the shoulder | 1.4, after the line |

Lines for Sam to record after animatic 2 (he records every voice): "Hey!", "We're just tourists! Why are y'all
protesting?", the wife's gasp, "Bro, what's a 'protest'?".

## Record (pre-flight reads these lines here; never archive them)
- Composition sheet sent: 13 Nov (pencil sketches, chat 4).
- Rehearsal clips sent: 15 Nov (chat 14): T1 0.0-2.0, T2 6.8-8.0, T3 10.4-12.0, T4 12.4-14.2, T4 13.6-15.6.

## Exceptions (rule 13: one row per thing left out of a check; looked at full size)
| check | who | why | looked at full size |
|---|---|---|---|
| camera feel | * | every tier is one locked-off lens (cam_for gives one fixed camera per tier: no pan, zoom or shake to feel); hard cuts only | chat 17: stills 4.4, 4.6, 13.0, 13.3, 14.1, 15.5 full size |
| LINE_OK | rioter t2 | the flagged "thin lines" are the black-bloc eye slits; the check's house weight reads 60 px because the figure is all black | chat 17: line sheet, all six kinds full size |
| POPS | runner6, runner7 (T2 3.0-3.5); back* (T3 2.2-2.5) | the looters step out of the dark shop through the glass gap; the back row steps up out of the packed crowd sprites (chat 26, `ALLOWED_POPS`) | chat 26: stills 7.2, 8.1, 13.0 |
| ALLOWED_POPS | runner6 | T2 looter steps out of the dark shop through the glass gap | chat 26 clip, chat 27 critique panels 1-3 |
| ALLOWED_POPS | runner7 | T2 looter steps out of the dark shop through the glass gap | chat 26 clip, chat 27 critique panels 1-3 |
| ALLOWED_POPS | back* | T3 back row steps up out of the packed crowd sprites (2.2-2.5 s) | chat 27 critique panel 4 full size |
| ALLOWED_POPS | buyer* | T4 cart queue: the buyers step out of the packed crowd into the queue (2.2-2.35 s, chat 29: was 2.6) | chat 27 critique panels 8-10 full size |
| ALLOWED_POPS | granny | T4: she steps out of the packed crowd to the cart (5.7-5.85 s) | chat 27 critique panels 9-10 full size |
| TOUCHES | hauler*, runner*, swinger | T2 run-in 4.25-7.95 s: the raiders crush through one gap in the glass, read as one dark pack (depth capped 10-18 cm) | chat 17: 4.4 and 4.6 s full size |
| TOUCHES | front* | T3 run-out 10.8-11.0 s: feet 2 cm, the front line breaks as a pack | chat 17: preflight list (2 cm, one frame) |
| TOUCHES | policia*, rioter* | T4 melee 12-16 s: rioters slam into the shields (brief 26), capped 20 cm; one frame at 22 cm (policia4 into rioter6, 14.72 s) | chat 17: 13.3 and 14.1 s full size |
| FAST_OK | hauler* | T2 run-in 4.0-4.9 s at a real sprint (bodies 6.2 m/s at most, re-timed chat 18); sprinting feet swing ~2x the body, past the 7 m/s walking cap; their stone throws 5.2-7.25 s: a throwing hand really reaches ~20 m/s (cap 12) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | runner* | same: T2 run-in sprint 4.0-4.9 s; stone throws 4.6-7.25 s (hands, forearms) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | swinger | T2 run-in sprint 4.0-4.9 s (carrying the road sign) | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | front* | T3: stone throws 8.7-10.65 s (hands, forearms); the run-out sprint from the jet 10.7-12.0 s | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| FAST_OK | rioter* | T4: Molotov and stone throws 12-16 s (hands, forearms); running feet in the surge 12.9-13.9 s | chat 18: clipcheck speeds (feet 8-12 m/s, hands 13-14); T2 still 4.0 s full size |
| ORDER_SWAPS | the same groups | the people cross in front of each other inside those three crushes | chat 17: same stills |
| FAST_OK | back* | T3 run-out from the jet 14.7-18.0 s, legs only (thighs, shins, feet at 2-2.8x the body's 4.5 m/s, same sprint as front*); their turn and throw-to-run were snaps, fixed chat 29 (blended, eased off), so arms and bodies are still checked | chat 29: clipcheck speeds (legs 7-9 m/s); NOT yet looked at full size: the animatic |
| FAST_OK | pusher* | T3 run-in to the car 14.4-16.2 s and run-off 17.3-18.0 s, legs only (same sprint); run-in slowed to 1.5 s and pose changes blended, chat 29 | chat 29: clipcheck speeds (legs 7-9 m/s); NOT yet looked at full size: the animatic |
| FAST_OK | selfie* | T4 run-off right 21.25-24.0 s, legs only; slowed to 3.2 m/s, set off eased, turn blended, chat 29 | chat 29: clipcheck speeds; NOT yet looked at full size: the animatic |
| FAST_OK | buyer* | T4 run-off right 21.5-26.0 s, legs and upper arms (pumping at 7.2-7.4 m/s); slowed to 3.2 / 2.8 m/s, set off eased, turn blended, chat 29 | chat 29: clipcheck speeds; NOT yet looked at full size: the animatic |
| FAST_OK | rioter2* | T4 the vault over the shields 19.9-20.9 s, legs only (leaping strides); named here | chat 29: clipcheck speeds |
| FAST_OK | rioter5* | the same vault, 0.12 s later | chat 29: clipcheck speeds |
| EFFECT SHAPES | T2 flash | the star read is the flash disc plus the red crowbar end in one test layer; the flash alone is a round disc | chat 17: fx_t2 full size |
| EFFECT SHAPES | T4 Molotov flames | spiky cartoon flame tongues (critique named the same, left open in chat 16): a fire restyle is a drawing job for round 1 | chat 17: fx_t4 full size |

## The reporting: what each tier is based on is in `notes/archive/protest-tiers-reporting.md` (T1 Barcelona 11 Nov, T2 Frankfurt 31 Oct, T3 République 17 Oct, T4 Tirana 13-18 Oct).

## First plan (archived chat 20): `notes/archive/protest-tiers-plan-r0.md` (estimate 21.5%, the re-staging with
the frame bands and cameras per tier, the 4 s action lists, the moves plan). The bands and cameras still hold; read only
the tier a note touches. Timings: "## Round 1 plan" below replaces them.

## The brief as a checklist (CLAUDE.md, 18 Oct): rows 1-33 (Sam's first brief, ticked chat 16) are in `notes/archive/protest-tiers-plan-r0.md`; their T2-T4 times are replaced by row 39 (R4) and the round 1 beat list. Recheck them there at the animatic 2 tick.
| # | from the brief (word for word where it matters) | done? |
|---|------|------|
| 34 | R1 The joke: each tier worse until Albania, off the charts; Albania's riot is not a protest, it is how they spend their time | ticked chat 28: the tiers escalate 2/4/8/11 and Albania's riot has the gags (cart, selfie, granny) and the end scene ("what's a protest") |
| 35 | R2a A second RPG moped pulls up, two riders, fires at something in the sky off screen; rioters clash with police behind; "Hey!" (the husband, Sam Q1) and they look to the side | built chat 24 (shot A), ticked chat 28 (shot in the animatic) |
| 36 | R2b A side alley, two American tourists cowering, husband and wife (cap, shorts, bum bag, camera, "Greetings from Tirana" tote, crouched behind bins: Sam Q4); he says "We're just tourists! Why are y'all protesting?" | built chat 24 (shot B) |
| 37 | R2c Back to the riders: one says "Bro, what's a 'protest'?"; the other shrugs | built chat 24 (shot C) |
| 38 | R3 Under each place heading, slightly smaller red text "Intensity Level:" 2, 4, 8, 11 out of ten; Albania at 11 from the start (Sam Q2) | ticked chat 28: "Intensity Level: N/10" in red under each place name at 1.0 s (overlay); Albania 11/10, no counting up |
| 39 | R4 Tier lengths 4 / 6 / 8 / 10 s; each scene re-paced with new action, never slow motion (Sam Q5: T2 stock carried out, TV or mannequin; T3 second volley, truck pushes forward, a burning car rolls) | ticked chat 28: LENS 4/6/8/10 s; T2 carries stock out, T3 second volley, car shoved into the jet; no slow motion |
| 40 | R5 Albania the showstopper: the most fluid, best-designed effects; gleeful violence and absurdity; gags a (Molotov seller's cart), b (selfie in front of the falling helicopter), c (granny throws a Molotov overarm) (Sam Q3) | ticked chat 28: round flames, lit smoke, fireball, fireworks, gags a/b/c, hold jumps; critique passes 5-6 (8 smaller faults named in the ledger) |
| 41 | Captions on the end scene's lines (rule 62); stand-in voices for timing only, never heard (best-practice) | built chat 24 |

## References as checklists: `references/protest-tiers/checklist.md` (what each photo shows; ticked at each critique, rule 89 A2).

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 1 | cast sheet | Marcher t2, phone | Sam, 14 Nov: the phone held behind the head (full note archived) | protest_tiers_cast.pose/phone | fixed (chat 6), check 12 still to improve |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 12 Nov decisions (hard cuts, heading timing, T1 camera, T3 police right, "WAFFEN", no helicopter crew): `notes/archive/protest-tiers-plan-r0.md`. 15 Nov: tiers 4/6/8/10 s + end scene (Sam R4).


## Sam's brief: word for word in `notes/archive/protest-tiers-brief.md` (every detail is in the checklist above).
