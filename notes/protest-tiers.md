# Notes for protest-tiers, now named **European Protests, Ranked** (Sam, 16 Nov; the old name stays only inside file and tool names; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 30 (say why a first fix failed: G4 plinth), 74 (acting list before the animatic), 83 (people through set/props).
- **Two lines of chats (Sam, 16 Nov):** GERMANY chats (t2 code only) and BACK-HALF chats (France + Albania, t3/t4/end code only). Each merges the main line before every push and keeps to its own lines below.
- **GERMANY done (Germany chat 4, 16 Nov, Opus; stopped at amber):** G16 clothing (DRESS t2 in the cast, from de5), O7 hats (crowd + rioters), G13 four hits / growing cracks / shatter at 2.95 / sign flung 3.2 / cheer / swinger loots a pistol; runner1/2 takes 3.6/3.75. `check`: 0 Germany faults. Stills looked at; no clip sent yet.
- **GERMANY next (Opus medium, a fresh chat):** build G12 (foreground: heads-and-shoulders at the frame's left/right edges, d 4-5, middle and door kept clear: near heads at d<6 cover the pavement line y~1480), G14 (inside the door: walk in to d 15.2 then sideways behind the wall, out the same way, never a pop), G15 (stones from off right-near at the lit upper-right window x 2.2-3.5, z 5-7.4: chip 3.9, chip 4.5, through 5.2), G17 (out of the door bursting 0.5 s, then sprint with stock in four directions: pose 'carry_run' = sprint gait + carry arms), G18 (BOARD_TO about (1.6, 10.4), 0.75 s flight, 1.5 m arc, 2 turns), G19 (sounds: wood-smash at each SIGN_HITS, glass-smash at T2_SHATTER, stone-hit per stone, protest-crowd from 15 s in under T2; MA.load works). Then `check`, acting/beat list (rule 74), clip `final OUT --small --span 6 14.5` to Sam, one line per note (G12-G19, O7). O8/O9 (numbers bigger, Sam's ding) are quick: do them too.
- **BACK-HALF done (back-half chat 4, 16 Nov, Opus medium):** F10 built (car up-left by Marianne, burning in place, silver, roof on; crowd keeps a clearing; pushers/steam gone); SET_BOXES t3 re-measured (bikes out, car in, car/monument meant); police files 0.75 m apart, rear files a beat later (check: T3 clean); T3 beat + acting list in the beat list; France clip 14.5-22.5 sent to Sam. Earlier (chat 3): F4-F9, F11 built.
- **BACK-HALF done (back-half chat 6, 16 Nov, Opus medium; stopped at amber):** F12-F23 BUILT (t3 code + cast/sets t3-only pieces), see "Build plan" under F23; draws without a fault at 14.6/16/18.5/20.5; not yet looked at full size or checked.
- **BACK-HALF next: Opus medium, back-half chat 7:** look at stills full size and fix (car 2, bare right paving, anything else), `check` (T3 clean), T3 acting/beat list (rule 74), then clip `final OUT --small --span 14.5 22.5` to Sam with one line per note, the rule 30 lines for F15, F16, F18, F20 (in each note), Lost/Added lines (Lost: the walk-in; the kiosk; the run-up throw style not built). Albania: its own chat.
- **ALBANIA done (Albania chat 1, 16 Nov, Opus high; stopped at amber):** A1-A3 built: T4 camera 6 m up and wider (sets CAMS t4, RF4 identity), road drawn before buildings, bank from d 24, crowd 13.7-62 m clear of the bank, Molotov landings world points (LAND_W/land()); LENS t4 12.5: shield surf (SURF, surf_pos, draw_surf_shield, drawn lit after backlight) + police rout (ROUT_LAG/V/LANE) 7.9-10.4, HOLD 10.4, fireworks FW0 8.0; end A/C on the old lens (low_cam, RF4_LOW, S.CAM4_LOW), END_BG0 = T4_LEN. Clip sent: animations/drafts/protest-tiers-albania-clip.mp4 (rout lanes fixed after it rendered).
- **ALBANIA next: Opus medium, Sam's notes on the Albania clip** (Needs Sam: 1 Y/N wider view; 2 Y/N shield surf + rout; 3 Y/N end shots keep the street-level lens). Then acting list (rule 74) for 7.9-12.5, `check` (T4 faults: rioter5/6 22.5-23.2, policia6/7 24.8 old), SET_BOXES/KEEP_CLEAR t4 re-measure if the check asks. Named, not fixed: the "Hey!" caption runs ~0.1 s into shot B (as before). The ledger's round2 STAGE STOP fired at the end of this chat (22% vs 2.7% share): X1 forbids telling Sam; the budget chat settles it before any next Albania chat starts.
- **Quick-check faults (handover check, back-half chat 6):** ALLOWED_POPS hauler1 has no Exceptions row: Germany's (t2 door), for the Germany chat. T3 not yet checked after the F12-F23 build.
- **Needs Sam (one numbered list per chat):** Germany clips Y/N; Overall+Spain still Y/N; France still sheet / clip. Diagonal Hook Text rule: through propose.py first.
- **Read:** job pack "Notes round"; "## Round 2 notes" (your chat's lines); this section.
- **Open rule requests:** diagonal Hook Text for every film (proposed 16 Nov; on Y: guides/tiktok-design.md Hook Text + hook_text.py default --tilt -7).
- **Branches named (not merged, waiting on Sam):** claude/beautiful-brown-vutd0l, claude/blessed-c2-mics-wip, claude/audit-honest-checker; claude/bald-heads-fix merged only after Sam's Y there.
- **X1:** no budget, cost or estimate talk to Sam for the rest of this film.
- **Budget stop Y (Sam, 16 Nov, in chat R2-2, at 15.22% of a week for round 2):** finish ONLY Germany (faults, placard off the door, sign meets glass, shop front in the clip check + rule 30 line, O7 hats), send the Germany clips with one numbered list (incl. Overall+Spain still Y/N), then STOP and wait for Sam before any France or Albania work.
- **Budget stop again (end of chat 3, 16 Nov):** round 2 at 20.13% of a week vs 2.7%. Not raised with Sam (X1: no budget talk this film); work stopped at his questions; the next chat settles it with chat 2 / the ledger before more work.
- **For Claude:** main line claude/create-claude-md-oe8z4g; back-half branch claude/protest-back-half. T2: t2_actors, _door_walk, board_pose, t2_door, t2_stones/chips; sets t2() door + prop_crate; cast kick/reach_lo/reach_hi/gun_up/swing_face. T3: FRONT3/BACK3/CRS_X/CRS_D/crs_adv/crs_guard/_missile/t3_fx; sets MON_X, BIKES3, CAR3, CAMS t3 (420, 900, 1550, 4.5), RF3 identity; cast shield_up, line_walk.

## Round 2 notes"; back half's notes to come.
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

## Round 4 France notes (Sam, 16 Nov, on the France round 3 clip; word for word in the bullets; plan after the dash)
- [ ] F12 Start with the crowds already throwing; the approach walk does not look good. - Cut the walk-in: frame 0 has the front and back rows in place, mid-throw at their own phases (no surge-in for actors or sprites).
- [ ] F13 More police and more crowds in the background around the statue; "I don't want to see empty space in this mass riot." - Fill the empty paving: crowd right of the base and behind the police (sprites), a third police group/reserve behind the truck lane and a line along the base's right; no bare paving band left on screen.
- [ ] F14 The gas canister lands amongst the police and not the crowd. - Its throw goes from the police toward the crowd: it lands in the crowd's front rows, the gas spreads there (the rioters cough/turn), not over Marianne's base/police.
- [ ] F15 Implement the different-races feature from OVERALL (O4). - Rule 30 (repeat of O4): O4 gave each ACTED rioter a skin from the city's mix, but the crowd SPRITES (marchers, most of the screen) and the officers' faces were left out; extend CITY_MIX (Paris) to the crowd sprites (clear the sprite cache) and keep F5's officer skins.
- [ ] F16 The throwing movements are too in sync, not individual enough. - Rule 30 (repeat of F9): F9 only changed each thrower's rate (1.47-1.71, all within 15%) and phase; every throw is the same overarm curve (_volley) from the same stance, so they still read as one. Fix: 3-4 throw styles (overarm, sidearm, lob, short two-step run-up), a pause to pick up a stone between throws, rates spread far wider, each thrower's own stance and lean.
- [ ] F17 The press hut is very low detail, looks out of place, its fire is wrong and bad: improve it or replace with another burning car. - Replace the kiosk with a second burning car (reuse the F10 car, another colour/angle), its fire built like F10's (flames out of the windows and roof).
- [ ] F18 The police remain static and uniform, absorbing all the thrown objects without raising their shields. - Rule 30 (repeat of F2/F9): crs_guard raises shields only 0.8-2.6+J3 then lowers them for the whole cannon part while stones still land, only the front two files raise, and nothing reacts to a hit. Fix: shields up for as long as missiles fly; each officer jerks his shield toward the missile that lands near him (flinch on impact, the missile bounces off); rear ranks hold shields overhead; small shuffles and turns between hits.
- [ ] F19 Apply the 'different clothes' logic for the rioters from the Germany notes here. - Find it in the Germany chats (not in this file yet; look there first, rule: earlier chats before asking) and apply it to the French rioters.
- [ ] F20 Even smaller rocks. - Rule 30 (repeat of F6): F6 took them from big to .10 m, still read big at this framing; make them 0.05-0.06 m, matt, and fewer per throw.
- [ ] F21 The smoke hangs limply in the air when it could be drifting over the crowd. - The car's and the far smoke drift and roll right-to-left over the crowd (wind), thinning as they go, animated every frame.
- [ ] F22 Some of the crowd slide backwards at the touch of the water cannon: keep them protesting in place; the cannon stays on the rioters, who turn fluidly and flee. - Sprites stay and keep protesting (no field() break for marchers); only the acted black-bloc rioters are hit, turn (blended, no snap) and run.
- [ ] F23 Make the truck's arrival and the water firing happen more evenly across the scene's length. - Re-time: truck enters ~2.0, jet on ~3.5, sweeps the rioters through 3.5-7.5 (not all at the end); beat list updated.

### Build plan (back-half chat 5's plan, rewritten by back-half chat 6 from the notes' dashes: chat 5 could not be read) and what chat 6 BUILT (16 Nov; not yet looked at full size, not checked)
- F12 built: no walk-in; throwers in place from frame 0 mid-plan (throw_plan starts at -3 s); crowd pressed up (field t3 constant +0.55, no surge).
- F13 built: crowd_t3 extras: CRS reserve sprites d 18.6-27 x 2.6-12.5 (shield_up:1 / line), cordon d 28.2 x 3-15.5, crowd right of the base d 29.5-46 x 8.5-20; officer sprites seeded i>=10 (make_person).
- F14 built: t3_gas: canister GAS_FROM (4.1, 16.2) -> GAS_LAND (-3.9, 18.6) 1.25-1.7; sprites within 3.2 m turn away; gas drifts left, thins. Old gas over the base removed from t3_fx.
- F15 built (cast marcher(): Paris CITY_MIX skin for tier t3, 32 faces); officers keep F5.
- F16 built: STYLE per thrower (throw / throw_side / throw_lob, new cast poses), own arm speed 0.5-0.9 s, 'pickup' pose between throws 0.25-1.3 s, blends via _thrower; lobs (FLIGHT .75) land on the rear file's overhead shields. Run-up style NOT built (foot slide risk): name it to Sam.
- F17 built: kiosk off (S.t3 kiosk=False); second car S.CAR3B (7.0-8.8, 22-25.2), red, CAR2_MOVE yaw 35, roof + flames (sets _car box/col). Looks small/boxy in the first still: look full size.
- F18 built: crs_guard up from 0 to last_land()+0.4; jolt() on each hit (shield_up/shield_over t = jolt); rear file 'shield_over'; shuffles + yaw sway; 'shield_walk' (shield up) while stepping; ADV_T 3.7.
- F19 built (= Germany G16, ref de5): cast street_clothes() for tier t3 rioters: 6 outfits (black bloc, black/grey puffer with quilting, grey hoodie under black coat, navy + white mask, olive + blue mask; grey/light trousers, white trainers).
- F20 built: flying stone .055 m, spent .045, debris .05, in-hand stone_r 17.
- F21 built: t3_columns: both cars' smoke puffs drift right->left over the crowd, roll, thin (3 alpha bands); far smoke in the set drifts (S.drift_smoke, t3 drift=True).
- F22 built: no jet split in field(); t3_crowd sprites never slide; struck rioters knocked a step, turn (blend) and run until off the frame's left edge (no OFF_L vanish).
- F23 built: J3 0.95; TRUCK_IN 2.0 (drives 2.0-3.4); JET_ON 3.5; jet_aim walks d 16.6 -> 9.4 over 3.55-7.0; each thrower breaks at jet_reaches(his d).
- Still to do (next chat): look at full-size stills 14.6/16/18.5/20.5 (sheet showed: car 2 small, right paving at x>9 d 18-24 still bare-ish, truck big over the right); `check` (T3 clean; check tables using J3 shift with it: verify the T3 rows ~2790-2840), acting/beat list (rule 74), clip 14.5-22.5 to Sam.


## Round 3 France notes (Sam, 16 Nov, on the France clip; Albania on hold)
- [x] F4 (built back-half chat 3, first pass, not yet checked) Move the France action closer to Marianne; protesters clambering up and celebrating on the statue (fr3 photo shows people on the plinth).
- [x] F5 (built back-half chat 3, first pass, not yet checked) The police are all the same model: vary them (height, build, skin, kit details, stance).
- [x] F6 (built back-half chat 3, first pass, not yet checked) Stones too big and too shiny: smaller, matt.
- [x] F7 (built back-half chat 3, first pass, not yet checked) Too little distance between protesters and police: open the gap.
- [x] F8 (built back-half chat 3, first pass, not yet checked) Remove the burning bikes. The water cannon approaches through two separate groups of police (the block split, a lane between).
- [x] F9 (built back-half chat 3, first pass, not yet checked) No group moves uniformly (robotic): every group, the police lockstep included, gets small per-person variance in timing, stride, angle.
- [x] F10 (built back-half chat 4: car at x -5..-3, d 31-34, side-on, silver, roof with a burning hole; crowd keeps a clearing in front of it, no flags over it; jet stays on the crowd; pushers and steam gone) (Sam: Y, 16 Nov, via parent: "Include a burning car in the upper left of the scene, burning near the statue and behind the protestors." So: no pushers, no shove; a silver estate car, roof on (fr3), burns where it stands, upper left, near Marianne, behind the protesters. Lost: the shove and the pushers. TO BUILD, back-half chat 4) Q: was the car shove in the reporting? Answer: no. fr3 (17 Oct) shows a silver estate car burning where it stood near Marianne, roof on; the shove was our way of doing round 1's "a burning car rolls". Sam: "the car has no roof" = ours is drawn roofless. Plan if Y: car burns in place as in fr3, roof drawn, no pushers.
- [x] F11 (built back-half chat 3, first pass, not yet checked) Vary the missiles: some fruit, a firework or two, a few bottles that smash on the shields.
- [ ] A0 (Sam 16 Nov: hold off on Albania, then: start Albania in a separate chat) Albania chat 1 does A1-A3 in t4/end code.

## Round 2 notes (Sam, 16 Nov, on animatic 2; film reopened; this chat: Overall, Spain, Germany; back half's notes to come)
- [x] O1 (chat R2-1: label white 54 px at 1 s, number in tier colour pops at 2 s, ding in soundtrack) Intensity heading bigger; numbers coloured by tier: Spain green, Germany orange, France red, Albania dark red; the numbers appear 2 s into each scene with a gentle ding.
- [x] O2 (fit_lines/sign_text in cast; S.text maxw on WAFFEN, PRESSE; T2 'WAFFEN RAUS' placard's holder stands at the frame edge: G4 re-staging moves her in) Sign, placard and shopfront text always fits neatly inside its board (some spills off now).
- [~] O3 (HOOK tilt -7, until 2.0; rule wording proposed to Sam, waiting) Hook Text in Blessed's diagonal style, gone after 2 s (rule request: diagonal style standard for every future film; wording proposed, waiting for Sam's number).
- [x] O4 (C.rioter(seed=name, tier): skin from CITY_MIX, iris, brows, head size; check faces in the Germany still) Black-clad rioters: not all the same face/skin; each city's groups reflect its population (e.g. Paris's Black and Middle Eastern share); faces reused from kit or randomised sensibly; rioters stay young.
- [x] O5 (people_parts.TRUE_SKULL, switched on in protest_tiers_cast.py only; Sam's Y 16 Nov, hair/fringe left as is; on the main line) Bald heads: a round skull the size of the same person's head under hair (Blessed's jury had the same fault); every haired head and every other film unchanged. Sprite cache cleared; check the bald protester at Germany 6.2 s in the next render.
- [x] O6 (Permanent Marker, Apache licence, source/fonts; research: heavy hand-drawn marker caps, condensed to fit) Protest-sign font: handwritten marker style researched from real signs, not computer text.
- [x] S1 (LENS t1 6.0; T1_KEYS 3.0, 50% of members, a 0.7 s wave; line steps 4.0, gas 4.2) Spain 6 s; keys raised at 3 s, by half the crowd.
- [x] S2 (blocks 133.5 m, no cross-street gaps) Join the gaps between the flat buildings along the avenue.
- [x] S3 (t1_actors empty; T1_ROCKETS: 10 throws from the front ranks 0.45-5.3 s, arcs 5-6.7 m, bursts over the line; CHECK: rockets cross the heading block y 350-560 on the left) No black-clad figures; fireworks thrown from the crowd mass, higher, more of them across the crowd's front at different times.
- [x] S4 (T1_CONTAINER (-7, 176) behind the line's left; new _container: lid upright, ribs, soot, flames only in the mouth, smoke column) Burning skip: back-left of the police line (not on it), better drawn, flames not spilling far over the lid.
- [x] S5 (second rank d +1.6, x +0.85) Second rank of police two paces behind the first, standing in the gaps.
- [x] O7 (built Germany chat 4: cast beanie/hat_cap; marchers: every bald one + 1 in 4 short-haired (marcher()); t2 rioters via DRESS) (Sam 16 Nov, chat 3) Too many bald heads in one place looks strange: put common hats on part of the crowd: beanies and caps (crowd sprites and acted rioters where it suits; clear ~/.cache/protest-tiers-sprites).
- [ ] O8 (Sam 16 Nov, chat 3) Intensity numbers 50% bigger.
- [ ] O9 (Sam 16 Nov) Use Sam's ding for the numbers: `sounds/protest-tiers/ding.mp3` (freesound community 101492; replaces the made ding).
- [x] S0 (Sam 16 Nov, on the 0-14.5 clip) Spain: "really good" (the Overall+Spain still question answered).
- [ ] S6 (Sam 16 Nov) Spain: the police advance once more, in the middle, between the opening second and the existing advance (line steps 4.0).
- [ ] S7 (Sam 16 Nov) Spain fireworks sound: `sounds/protest-tiers/fireworks.mp3` (freesound community 29629), timed to the rockets/bursts (Sam asked: sound effect allowed).
- [ ] Q1 still open: Germany Y/N on the 0-14.5 clip.
- [ ] G12 (Sam 16 Nov, on the 0-14.5 clip) More foreground protesters (some were lost moving them off the door) while the action stays clear.
- [x] G13 (built Germany chat 4: SIGN_HITS 1.6/2.05/2.5/2.95 in four places, cracks grow (t2_chips), shatter T2_SHATTER 2.95; t2_sign flung at SIGN_DROP 3.2; cheer; loots pistol TAKE swinger 4.85, off left lane 13.4; runner1/2 takes moved to 3.6/3.75) The road-sign man breaks the window, then just flaps the sign about: he hits the glass in several places (more cracks each time) until it all shatters; then he throws the sign to the ground and celebrates or loots.
- [ ] G14 The looters who run into the shop vanish mid-frame: they go round a corner inside, out of sight (not a pop).
- [ ] G15 Some thrown rocks hit the upper (first-floor) window: chip it / shatter through.
- [x] G16 (built Germany chat 4: photo arrived as de5; cast DRESS['t2']: tops black/dark-grey/navy/grey/light-grey/khaki, puffers, grey joggers, light-grey trousers, white trainers, hood/beanie/cap, black/blue/white/grey masks, teal backpack; per rioter from his name; F19 adds DRESS['t3']) Reference photo of the Frankfurt looting: diversify the rioters' clothing from it, and note anything else it teaches.
- [ ] G17 The looters leaving the shop sprint out in different directions, fleeing (not a calm walk off left).
- [ ] G18 The kicked A-board flies further across the scene.
- [ ] G19 Sounds (Sam's files, sounds/protest-tiers/): wood-smash.mp3 for the sign hits; glass-smash.mp3 for the shatter; stone-hit.mp3 for the rocks; protest-crowd.mp3 under the scene, taken from 15 s into the file onwards (it has voices from there).
- [ ] G1 Germany 2-3 s longer, so the action breathes.
- [ ] G2 Stones pelted from off camera at the shop first.
- [ ] G3 The glass attacker turns and hits the glass (contact), not a flat swing at the air.
- [ ] G4 (Sam 16 Nov: 'we definitely have rules for people clipping through objects and background' = rule 83, people through furniture/set, checked BY HAND on stills before each animatic; rule 30: say why that hand check missed the plinth, and make it automatic for the shop front) Camera a little right: window's left edge on the screen's left edge; a shop door in the space on the right; rioters kick it open and flood in; looters come back out through the same door, stolen things not clipping (they walked through the wall at the window's centre: answer why the clipping check missed it).
- [ ] G5 (Sam 16 Nov: replace it with a crate of beer, easy through a door) Q: the mannequin of a military man? (answer: Sam's round 1 "TV or mannequin"; the camo was invented, a hunting/gun-shop guess)
- [ ] G6 Q: why does the broken glass dance on the ground? (answer: fix so landed shards lie still)
- [ ] G7 Street-sign kick: a run-up and a hard kick; the sign drawn clearer.
- [ ] G8 Q: white glints on the backs of heads? (answer and fix)
- [ ] G9 Right-side rioters mime taking with nothing in hand: reporting (FAZ 31 Oct: two weapons taken) -> they take two guns.
- [ ] G10 (Sam: Y, the freeze is no good) No freeze when the sirens start: the action carries on.
- [ ] G11 Stills and clips to Sam for each part; once all Y, an animatic of the front half (Spain + Germany).
- [ ] F1 (Sam 16 Nov, France) Camera too low: everything is a mess of movement. Raise it to an 'above the head' view, not aerial, so the crowd, the thrown objects, the statue, the water cannon and the burning car each have room. References (3 photos, saved in `references/protest-tiers/r2-france/`): the crowd seen over heads, water jet crossing frame, police shield line from above shoulder height.
- [ ] F2 Police are static: a thicker cluster (more ranks, more officers), actively defending against missiles with the riot shields (shields up, thrown things hit and bounce), then advancing in practised lockstep when the water cannon arrives.
- [ ] F3 With the camera raised, re-stage the French pieces so each has its own moment (advancing crowd, thrown objects, statue, cannon, burning car).
- [ ] A1 (built, Albania chat 1: camera 6 m up (was 2.8), wider (10 m across the line, was 6.6); bank wall drawn to the frame's edge; crowd deeper and nearer; Molotov landings now on the bank's windows in any view; clip sent) (Sam 16 Nov, Albania + end scene) Perspective flattens everything: keep the same angle but draw back and up: wider, slightly more aerial view of the square.
- [ ] A2 (built, Albania chat 1: 12.5 s; shield surf + police rout 7.9-10.4, hold 10.4-12.5; beat list updated; clip sent) Extend the Albania action by 2-3 seconds (new action at full speed, no slow motion). Time goes in the beat list; the end scene shifts later.
- [ ] A3 (built, Albania chat 1: shots A and C keep the old street-level long lens, a cut to a close-up (from 6 m up the riders had only crowd and road behind them); background now runs straight on from the cut; clip sent) (Sam: 'Albania and Conclusion' are one note) Check the end scene (the A/B/C parts) against the wider framing so it still reads.
- [ ] X1 (Sam 16 Nov) Never mention budget, cost or estimates to Sam for the rest of this film (budget work is going on elsewhere; the figures are off). The cost-watch lines in handovers and messages are left out for this film.

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
  splits (was 2.5-4.0). **5.5-6.5 NEW** the truck pushes forward about 1.5 m, the jet sweeping. **6.0-8.0** (round 3,
  F10: the shove is gone) the jet keeps sweeping, the police step forward in lockstep, the crowd flows away left (so T4
  opens bottom-left, as now). The silver estate car burns where it stands the whole shot, upper left, 6 m in front of
  Marianne's base, behind the protesters, its black smoke leaning left (fr3).
  **T3 acting list (rule 74; no lines in France, so the moves):** front line: each throws on his own beat (_jit), runs
  out left when the jet hits; back row: steps up into the gaps at 2.5, throws; on the base: cheerers wave, two climb,
  flags sway; police: shields up, flinch on each hit, rear files step forward a beat after the front (no lockstep
  robots, F9; no feet into the man ahead); truck: drives up the lane between the two groups, jet on the front line;
  car: no one near it (people keep off a fire), flames and smoke only.
- **T4 Albania (12.5 s since round 2, A2; 11/10; the showstopper):** (round 2, A1: camera 6 m up, wider; the end's A and C keep the old street-level lens) 0.0-1.0 as now (mopeds, RPG at 0.6, hit at 1.0).
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
  **7.9-10.4 (round 2, A2, new):** a rioter is hoisted out of the near crowd on a captured riot shield, flag up, and
  passed hand to hand left to right over the heads (lurching, lit by the fire); from 8.0 the beaten police turn and
  run off right, each at his own moment and pace (F9); fireworks go up from 7.8. **10.4-12.5** the gleeful hold:
  crowd jumping, the surfer tossed up and down on the shield, fireworks again, the toppled water cannon burning.
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
| ALLOWED_POPS | hauler1 | G4: into and out of the dark shop through its door (clipped to the doorway); G14 replaces the pop with a walk round the corner inside | Germany chat 3 clip 0-14.5; Germany chat 4 stills 10.0-10.9 |
| ALLOWED_POPS | hauler2 | G4: into and out of the dark shop through its door (clipped to the doorway); G14 replaces the pop with a walk round the corner inside | Germany chat 3 clip 0-14.5; Germany chat 4 stills 10.0-10.9 |
| ALLOWED_POPS | runner4 | G4: into and out of the dark shop through its door (clipped to the doorway); G14 replaces the pop with a walk round the corner inside | Germany chat 3 clip 0-14.5; Germany chat 4 stills 10.0-10.9 |
| ALLOWED_POPS | runner5 | G4: into and out of the dark shop through its door (clipped to the doorway); G14 replaces the pop with a walk round the corner inside | Germany chat 3 clip 0-14.5; Germany chat 4 stills 10.0-10.9 |
| ALLOWED_POPS | back* | T3 back row steps up out of the packed crowd sprites (2.2-2.5 s) | chat 27 critique panel 4 full size |
| ALLOWED_POPS | surfer | T4 (A2): hoisted up out of the packed near crowd on the shield at 7.9 s (he is one of the crowd sprites, drawn live from then) | Albania chat 1: stills 30.6, 31.3 full-size crops |
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
