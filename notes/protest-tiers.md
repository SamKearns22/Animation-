# Notes for protest-tiers, now named **European Protests, Ranked** (Sam, 16 Nov; the old name stays only inside file and tool names; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 30 (say why a first fix failed: G4 plinth), 74 (acting list before the animatic), 83 (people through set/props).
- **Two lines of chats (Sam, 16 Nov):** GERMANY chats (t2 code only) and BACK-HALF chats (France + Albania, t3/t4/end code only). Each merges the main line before every push and keeps to its own lines below.
- **GERMANY done (Germany chat 5, 16 Nov, Opus medium):** G12 near crowd at both edges, G14 round the corner inside, G15 upstairs window (chip, chip, through), G17 sprint out four ways, G18 board 3.4 m, G19 Sam's sounds, O8 numbers 81 px, O9 Sam's ding. Earlier (chat 4): G16, O7, G13. `check`: 0 Germany faults. T2 beat + acting list written. Clip 6-14.5 sent to Sam.
- **GERMANY handover check (chat 5), named not fixed:** T2 limb speeds 7-13 m/s (runner1 0.92 run-in, unchanged code; hauler1/swinger/looters: sprint gait feet and the swing's hands at 12 fps) and front/back swaps (people passing in separate lanes: runners, swinger, looters); 'WAFFEN RAUS placard not on screen 7.5-8.5' (its holder at the frame edge, O2/G4); 'T2 sign-on-glass flash draws nothing in its test' (the test's time 1.05 is before the first hit 1.6: move it). Looked at stills 7.6-14.4 and the clip frame 8.58: they read fine. The next Germany chat sets ORDER_SWAPS and the flash test time.
- **GERMANY next (Opus medium, Germany chat 6):** build G20, G21, G22 (plans in the notes), `check` (0 Germany faults), clip `final OUT --small --span 6 14.5` to Sam, one line per note; then, on Sam's Y, the front-half animatic (Sonnet chat; G11).
- **BACK-HALF done (back-half chat 4, 16 Nov, Opus medium):** F10 built (car up-left by Marianne, burning in place, silver, roof on; crowd keeps a clearing; pushers/steam gone); SET_BOXES t3 re-measured (bikes out, car in, car/monument meant); police files 0.75 m apart, rear files a beat later (check: T3 clean); T3 beat + acting list in the beat list; France clip 14.5-22.5 sent to Sam. Earlier (chat 3): F4-F9, F11 built.
- **BACK-HALF done (back-half chat 6, 16 Nov, Opus medium; stopped at amber):** F12-F23 BUILT (t3 code + cast/sets t3-only pieces), see "Build plan" under F23; draws without a fault at 14.6/16/18.5/20.5; not yet looked at full size or checked.
- **BACK-HALF done (back-half chat 7, 16 Nov, Opus medium):** stills 14.6-21.8 looked at full size: lone marcher in the gap dropped (no neighbour within 1.3 m), car smoke columns 18 puffs + faint newborn puffs (lone puffs read as rocks), far-smoke lumps restart small, thrown wheel .8 (was 1.25), car 2 4.2 m long (CAR3B 6.8-8.7, 21.8-26.0); T3 check rows moved to SWEEP (throw hands 0-7.2, run-out from 3.55): `check` T3 clean; T3 beat + acting list rewritten; clip animations/drafts/protest-tiers-france-clip.mp4 sent.
- **BACK-HALF next: Opus medium, back-half chat 8:** F24 France sound (Sam's paris-riot.mp3 + the banked effects; water cannon on the jet), clip 14.5-22.5 to Sam. Sam Y'd F12-F23 ("FANTASTIC WORK"). Albania: its own chat.
- **Stage stop (end of back-half chat 6):** Sam said Y in chat 7 (16 Nov); chat 7 carried on.
- **ALBANIA done (Albania chat 3, 16 Nov, Opus high; stopped at amber):** build plan steps 1-10 BUILT (t4/end code; cast shrug/moped faces; sets bank fires A5, ministry holes/craters A6, truck to d 44, ALLEY_CAM F 1450) + A14 (metal track from 19.88 s, ducked under lines) + A15 (explosions) + A16 (Sam: no raised part: police behind a SANDBAG WALL on the ground, d 26.3, clipped at its top). Stills 22.6-42.9 draw without a fault; not yet looked at full size, `check` not run. Seen at a glance, to fix in step 11: bank window glows far too big (wash out BANKA); RPG craters too big and star-like; melee rioters and police overlap into one mass; surf drawn near the left edge; Molotov fires on the bank large.
- **ALBANIA chat 4 (16 Nov, Opus; stopped at amber):** A17 crowd mix BUILT (one still looked at), A18 police varied DONE, A24 hair DONE (T4), A25 arms-through-long-hair OPEN (diagnosis in A25). The sprite cache key is 'v2-hair-clear' (first render redraws sprites: slower). Germany G20-G22 were never pushed by Germany chat 6: Germany chat 6b (session_01GznaATrmF2ZZWRhTSQHptf) rebuilds them.
- **ALBANIA next: Opus high, Albania chat 5:** A25, then A19 (craters/holes blended), A20 (BANKA on a real fascia sign), A21 (two more mopeds before the RPG one, pillion firing in the air, sizes/colours/riders' clothes varied), A22 (RPG riders: black/grey hoodies, different eyes), A23 (shot B 2.8 -> ~3.6 s for Sam's take), then step 11 below (stills full size, check, acting list, clip 22.5-END to Sam, one line per note).
- **Sam (16 Nov, ~94% of his usage): stay in Albania chat 3, it carries on at 18:19 when his usage resets; build A17-A23 there, then step 11.** Previously: **ALBANIA next: Opus high, Albania chat 4:** step 11: stills 22.5-43.6 full size and fix the list above, `check` (new T4 table rows: mp*/mr*/carrier* contacts, FAST_OK for sprite steps; tune to the real faults), T4 + end beat/acting list (rule 74), clip `final OUT --small --span 22.5 43.6` to Sam with one line per note A4-A16 (Lost: the seller's queue, the police rout; the granny throws without buying). Old 67 T4 faults (the rout) are gone with it.
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

## Round 3 Albania notes (Sam, 16 Nov, on the Albania clip; Albania chat 2)
Sam's answers to chat 1's questions are carried by these notes (wider view kept; the rout replaced; end shots re-framed below).
- **Done (Albania chat 2):** A13 take saved (source/audio/protest-tiers-bro.m4a: _take() picks it up as the 'bro' line). Cast poses BUILT and drawn on a test sheet (fine at phone size): 'punch', 'machete' (blade prop machete()), 'aim_rifle' / 'rifle_up' (AK prop rifle(): wood stock + handguard, curved magazine), 'aim_pistol' (gun_aimed()), 'dance'; u = phase/recoil.
- **Build plan A4-A12 (Albania chat 2, for chat 3: build exactly this):**
  1 Speed: live actors cost 0.15 s each, sprites 0.006 s. Add make_pose state 'p:NAME:U' (-> C.pose(sp, NAME, float(U), 0, force)) and an Actor flag spr=True that draw_actor pastes as a sprite (force=name seeds each rioter's face); u quantised to 6 steps. Group members are such Actors inside t4_actors (so one depth sort, and the audit sees them).
  2 Timing (lt): MOPED0 5.5 (old moped/rocket/hit/fall code keyed on hl = lt - MOPED0: fire 6.1, hit 6.5, fall 6.5-8.1); heli flies in from off top-right 4.6-5.6 to HELI_HOME, hovers; T4_FIRE 8.1 = landing (no gap); CHEER 8.3; HOLD 8.6; FW0 8.6; SURF (8.6, 11.8). Mopeds: in from x -6 to x -2.4 / -3.4 at d 10.5 / 11.8 over 0.6 s and STAY (no rev-off: the selfie is to their right).
  3 FRONT melee d 12.2-16.4 (4 rows), contact line x 0.6 + 0.35 sin(lt*1.3 + d): 24 rioters left (yaw 90; front row punch / machete, rear rows throw stones at the police), 24 police right (yaw -55; front row baton_up / pushed, rear shield_up:1 / line). Runs all 12.5 s (continues after the crash). Flying shield kept (at x 1.0, 3.0-4.0); melee dust continuous.
  4 MIDDLE d 18-25, x -7..-1: 8 gunmen at x ~-1.2 (5 aim_rifle, 3 aim_pistol, yaw 75 at the police), bursts 0.4 s every ~1.6 s at own offsets (u 1 on flash frames); 16 yell/throw stones (arcs in world: lerp + z parabola, cam.p). After CHEER: gunmen rifle_up firing into the air, the rest cheer + jump. Granny (live) at (-6.0, 17.2) yaw -120, overarm Molotov 3.4 -> bank first floor (-9, 27.3, 7.8) at 4.1 (biggest bloom), cheers after CHEER; no buying.
  5 POLICE IN COVER: raised terrace x 1.5-11, d 26.3-40, 0.8 m up, low wall 1.0 m on its front edge (d 26.3) + 1.5 m return along x 1.5: terrace top in the sets painting (S.t4), the front face + wall drawn as a sorted item at d 26.3 in the people loop (so it hides them). 10 officers d 27.2, x 2-8, lift 0.15 crouched (helmets peep), pop up (lift 0.8, aim_pistol yaw -100) 0.6 s every ~2 s at own offsets, firing; never after CHEER. Toppled truck moves to TRUCK_D4 44 (SET_BOXES t4 re-measure).
  6 BACK d 29-40, x -8..-1.5: 13 dancing (p:dance, jumps), 5 Molotov throwers (yaw -90 at the bank windows, yaw 162 at the ministry), a throw each ~2.4 s at own offsets; molotovs() takes a world list (thrower hand -> target, apex, big); blooms stay lit.
  7 Remove cart, seller, buyers (draw_cart, buyers, seller_j, sold, SALES/SLOT/CART, the 'cart' sort item) and the old rout, vault and crowd_t4 mass; check tables (FAST_OK, ALLOWED_POPS, ALLOWED_CONTACTS, ORDER_SWAPS, EFFECTS rows naming buyer*/SALES/rioter2/5/policia rout) rewritten to the new names and times.
  8 fx: muzzle flashes (glow + star) at muzzle = (x + fx*0.9, d + fd*0.9, 1.45 + lift), 1-frame tracers toward the target, sparks + dust on the wall top; police flashes back at the middle crowd. Selfie (1.7, 10.4) keyed on hl (turns at hit + 0.2, flash with the fall), stands watching before. Surf over the middle crowd at SURF_D 21, x -6 -> -2, carried by 4 cheering sprite carriers moving under it (draw_surf_shield arms to them).
  9 Sets: A5 the bank's windows (ground and upper, ~6) burning, flames streaking out, scorched; A6 the ministry: ~250 bullet holes (dark dot, pale chipped ring) over the wing and bay, 5 RPG craters (jagged dark hole, scorch streaks); the HUGE explosion: fireball x1.7, white flash 0.15 s, shock ring, debris.
  10 End A (A9): rim=None in end_riders (the orange outline). B (A10): ALLEY_CAM F 2000 -> ~1450, and the hard-coded hide line ppl.paste(..., (0, 1300, W, H)) recomputed from the bin-lid height through the camera. C (A11/A12): 'ec' 2.4 -> ~3.4 s (Sam's take: speech ~1.85 s with a pause; line at 0.2), shrug AFTER the line (~2.25-2.85): passenger head yaw 45 toward the driver (not to camera), eyes on him (sp look), brows up and knit, shoulders up ~60, near hand palm up at chest height, head tilt; driver head -45 back toward him, eyes on the passenger (sp look; moped_scene gets drv_face/gun_face dicts merged into each sp). Caption stays English (subtitle).
  11 Then stills sheet 22.5-42 full size, `check`, beat + acting list (rule 74), clip `final OUT --small --span 22.5 END` to Sam.
- [ ] A4 Three crowds in the overhead T4. FRONT: fierce melee with police, 20-30 a side: fists, thrown objects and machetes v batons and riot shields. MIDDLE: 20-30 yelling and throwing at the police opposite, who crouch in cover; a line of protesters fire AK47s and pistols; the police on the raised part of the square fire back and duck behind a low wall. BACK: 10-20, most dancing, others facing the buildings on the left or the ministry throwing Molotovs at the windows.
- [ ] A5 Buildings on the left: flames streak out of the windows too.
- [ ] A6 Education ministry covered in bullet holes and RPG craters.
- [ ] A7 Helicopter comes in too early: it arrives midway; then the mopeds with RPGs arrive and shoot it down; the crash, then the huge explosion immediately after, causing the jubilant celebration and crowd surfing. Police in the middle stay in cover; the front melee carries on.
- [ ] A8 Remove the Molotov salesman entirely (cart, seller, queue). (Granny kept: she throws from the middle crowd, no buying.)
- [ ] A9 End shot A (focus on a moped rider): remove the odd highlight round them; blend naturally into the scene.
- [ ] A10 End shot B (the Americans): draw the camera back; the picture is good but too close.
- [ ] A11 End shot C: the speaking Albanian moves his eyes to the other one.
- [ ] A12 End shot C: the other one's shrug must read: a real shrug, genuinely perplexed, eye contact with the driver (no idea what a 'protest' is: this is just another day in Albania).
- [ ] A13 Sam's Albanian take of the driver's line: source/audio/protest-tiers-bro.m4a (speech 1.1-3.0 s of the file); the English line stays as its subtitle.
- [ ] A14 (Sam 16 Nov) Music for the Albania scene: `sounds/protest-tiers/heavy-metal.mp3` (his track, 129 s), from 20 s into the file (where the heavy riff starts: check by ear/loudness and start on the riff's first hit), under T4 and on through the end scene; ducked (muffled: quieter + low-pass) under each dialogue line so the voices are clear, back up between lines.
- [ ] A16 (Sam 16 Nov, Albania chat 3) There is no 'raised part' of the square: the middle police hide behind sandbags / a low wall instead. Plan step 5 changed: no terrace; a low sandbag wall (~1.0 m, two courses of bags) on the ground across x 1.5-9 at d 26.3 with a short return along x 1.5; the officers crouch behind it and pop up to fire.
- [~] A17 (Albania chat 4: BUILT, seen in one still 28.5: crowd_t4 mass back (Tirana mix, 64 looks, fists, flags, jumps in the hold); about 2 in 5 group members bare-headed marchers (spr), the rest rioters in DRESS['t4'] (Germany pack + colour); a build whose arm fails in a pose falls back to the hooded rioter. To look at: far rows show many gold beanies; check the whole shot.) (Sam 16 Nov, on chat 3's stills) The original crowd was deleted and everyone is a hooded man: it must be a HUGE MIX as before (the Germany clothes pack: street clothes, colours, hair, hats). Plan: bring back the crowd_t4 mass (painted sprites, marchers' mix) around and behind the three groups; the three groups' rioters drawn from the street-clothes mix (C.rioter street_clothes / marcher looks), not all black bloc.
- [x] A18 (Albania chat 4: each T4 officer his own build/skin/kit via 'policia|NAME' sprites; helmets one shade of white each, France untouched) Police are identical: vary them as the France pack does (each officer his own build and kit: officer(seed=name, tier) as T3's F5/F13).
- [ ] A19 RPG craters and bullet holes look pasted on top: blend them into the building (softer edges, scorch fading into the ochre, smaller/irregular craters with broken masonry, holes following the facade's light).
- [ ] A20 'BANKA' is words pasted on the image: put it on a real sign on the bank (a fascia board / lettered panel on the building's face, in its perspective).
- [ ] A21 Two more mopeds zoom by BEFORE the RPG one, the pillion firing into the air; different sizes and colours; the riders in varied clothes.
- [ ] A22 Keep the RPG riders in the black/grey hoodies but give them different eyes (eye sets) from each other.
- [ ] A23 Sam's American tourist take saved: source/audio/protest-tiers-hey.m4a (0.43 s) and protest-tiers-tourists.m4a (3.06 s; raw in references/protest-tiers/takes/). The tourists line now runs past shot B's end (37.7 + 3.06 > 40.2): B 2.8 -> ~3.6 s.
- [ ] A24 (Sam 16 Nov, on chat 4's test sheet) Women's hairstyles only on women, men's styles on men (unless stated); no natural blond on darker skin. DONE for T4 (Albania chat 4): the crowd file's women are its bob/pony/long members: they now get lashes and lip colour; men keep men's cuts; hair colour follows skin (cast.t4_street). The other tiers' marchers were NOT changed (ask Sam if he wants it for every film: a rule request).
- [ ] A25 (Sam 16 Nov) Arms must not pass through hair (long hair: the wound-up throwing arm, the cheer's arm behind the head sink into it with a soft blur). Long hair kept (Sam: don't exclude it); the arm should go slightly round it. Tried (chat 4): film hair_clear() drops the elbow below the hair's lower edge (y 95 long / 40 bob, person units) when an arm's line crosses the hair behind the head: works for bob (machete), but long hair covers the shoulder itself, so every backward arm still enters it and the reroute reverts. Next: draw the far arm OVER long hair with its ink outline (or clip the hair's mass where the arm passes), and find the soft fade at the sleeve top (it is the 'blend'); test on scratch sheet t_mix2 (marchers 5, 13 long; throw 0.0 yaw 90, cheer 0.6 yaw 60).
- [ ] A15 (Sam 16 Nov) The helicopter crash's sound: the explosions from the Blue Planet film (Flying Whales: `source/audio/flying-whales-sfx/explosion-major.mp3` for the big explosion at the landing T4_FIRE, `explosion-minor.mp3` for the RPG hit); see flying_whales_sound.clip() for how they were levelled.

## Round 5 France notes (Sam, 16 Nov, on the France round 4 clip)
- [x] F24 (built chat 8: t3_sound(); paris-riot.mp3 read by loudness/spectrum: 0.4-6.4 voiced crowd -> bed looped under all T3 (0.35); 7.0-14.7 broadband hiss = cannon, 9.6-13.4 slice at JET_ON 3.5 to SWEEP end 7.0 (0.5); no engine in the recording, none laid; stone-hit on 22 stone shield hits, glass-smash on 3 bottles, fireworks.mp3 crackle on 2 fireworks, far block x0.75; fruit silent; peak 0.82; check: T3 clean (4 T4 pass-throughs are Albania's); clip sent) Sam: "FANTASTIC WORK" (F12-F23: Y). Sound for France: "I have added a video of a Parisian riot which you can take sound from, alongside other banked sound effects -- you will hear the water cannon distinctly." - Sam's recording's sound saved as `sounds/protest-tiers/paris-riot.mp3` (14.7 s, from his screen recording). Listen through it (loudness over time; find the water cannon's hiss/roar and the crowd); lay France's sound: crowd bed from it under all of T3, the water cannon's sound from JET_ON 3.5 to the sweep's end 7.0 (truck engine 2.0-3.4 if it has one), and the banked effects (stone-hit.mp3 on shield hits, glass/other where the moves call for it). Clip `final OUT --small --span 14.5 22.5` to Sam.

## Round 4 France notes (Sam, 16 Nov, on the France round 3 clip; word for word in the bullets; plan after the dash)
- [x] F12 (built chat 6, looked/checked chat 7; clip sent) Start with the crowds already throwing; the approach walk does not look good. - Cut the walk-in: frame 0 has the front and back rows in place, mid-throw at their own phases (no surge-in for actors or sprites).
- [x] F13 (built chat 6, looked/checked chat 7; clip sent) More police and more crowds in the background around the statue; "I don't want to see empty space in this mass riot." - Fill the empty paving: crowd right of the base and behind the police (sprites), a third police group/reserve behind the truck lane and a line along the base's right; no bare paving band left on screen.
- [x] F14 (built chat 6, looked/checked chat 7; clip sent) The gas canister lands amongst the police and not the crowd. - Its throw goes from the police toward the crowd: it lands in the crowd's front rows, the gas spreads there (the rioters cough/turn), not over Marianne's base/police.
- [x] F15 (built chat 6, looked/checked chat 7; clip sent) Implement the different-races feature from OVERALL (O4). - Rule 30 (repeat of O4): O4 gave each ACTED rioter a skin from the city's mix, but the crowd SPRITES (marchers, most of the screen) and the officers' faces were left out; extend CITY_MIX (Paris) to the crowd sprites (clear the sprite cache) and keep F5's officer skins.
- [x] F16 (built chat 6, looked/checked chat 7; clip sent) The throwing movements are too in sync, not individual enough. - Rule 30 (repeat of F9): F9 only changed each thrower's rate (1.47-1.71, all within 15%) and phase; every throw is the same overarm curve (_volley) from the same stance, so they still read as one. Fix: 3-4 throw styles (overarm, sidearm, lob, short two-step run-up), a pause to pick up a stone between throws, rates spread far wider, each thrower's own stance and lean.
- [x] F17 (built chat 6, looked/checked chat 7; clip sent) The press hut is very low detail, looks out of place, its fire is wrong and bad: improve it or replace with another burning car. - Replace the kiosk with a second burning car (reuse the F10 car, another colour/angle), its fire built like F10's (flames out of the windows and roof).
- [x] F18 (built chat 6, looked/checked chat 7; clip sent) The police remain static and uniform, absorbing all the thrown objects without raising their shields. - Rule 30 (repeat of F2/F9): crs_guard raises shields only 0.8-2.6+J3 then lowers them for the whole cannon part while stones still land, only the front two files raise, and nothing reacts to a hit. Fix: shields up for as long as missiles fly; each officer jerks his shield toward the missile that lands near him (flinch on impact, the missile bounces off); rear ranks hold shields overhead; small shuffles and turns between hits.
- [x] F19 (built chat 6, looked/checked chat 7; clip sent) Apply the 'different clothes' logic for the rioters from the Germany notes here. - Find it in the Germany chats (not in this file yet; look there first, rule: earlier chats before asking) and apply it to the French rioters.
- [x] F20 (built chat 6, looked/checked chat 7; clip sent) Even smaller rocks. - Rule 30 (repeat of F6): F6 took them from big to .10 m, still read big at this framing; make them 0.05-0.06 m, matt, and fewer per throw.
- [x] F21 (built chat 6, looked/checked chat 7; clip sent) The smoke hangs limply in the air when it could be drifting over the crowd. - The car's and the far smoke drift and roll right-to-left over the crowd (wind), thinning as they go, animated every frame.
- [x] F22 (built chat 6, looked/checked chat 7; clip sent) Some of the crowd slide backwards at the touch of the water cannon: keep them protesting in place; the cannon stays on the rioters, who turn fluidly and flee. - Sprites stay and keep protesting (no field() break for marchers); only the acted black-bloc rioters are hit, turn (blended, no snap) and run.
- [x] F23 (built chat 6, looked/checked chat 7; clip sent) Make the truck's arrival and the water firing happen more evenly across the scene's length. - Re-time: truck enters ~2.0, jet on ~3.5, sweeps the rioters through 3.5-7.5 (not all at the end); beat list updated.

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
- [x] O8 (built Germany chat 5: 81 px, was 54) (Sam 16 Nov, chat 3) Intensity numbers 50% bigger.
- [x] O9 (built Germany chat 5: sfx('ding') in soundtrack; the made ding removed) (Sam 16 Nov) Use Sam's ding for the numbers: `sounds/protest-tiers/ding.mp3` (freesound community 101492; replaces the made ding).
- [x] S0 (Sam 16 Nov, on the 0-14.5 clip) Spain: "really good" (the Overall+Spain still question answered).
- [ ] S6 (Sam 16 Nov) Spain: the police advance once more, in the middle, between the opening second and the existing advance (line steps 4.0).
- [ ] S7 (Sam 16 Nov) Spain fireworks sound: `sounds/protest-tiers/fireworks.mp3` (freesound community 29629), timed to the rockets/bursts (Sam asked: sound effect allowed).
- [ ] Q1 still open: Germany Y/N on the 0-14.5 clip.
- [x] G12 (built Germany chat 5: five more in the t2 crowd list, d 4.4-6.4 at both edges, heads below the pavement line) (Sam 16 Nov, on the 0-14.5 clip) More foreground protesters (some were lost moving them off the door) while the action stays clear.
- [x] G13 (built Germany chat 4: SIGN_HITS 1.6/2.05/2.5/2.95 in four places, cracks grow (t2_chips), shatter T2_SHATTER 2.95; t2_sign flung at SIGN_DROP 3.2; cheer; loots pistol TAKE swinger 4.85, off left lane 13.4; runner1/2 takes moved to 3.6/3.75) The road-sign man breaks the window, then just flaps the sign about: he hits the glass in several places (more cracks each time) until it all shatters; then he throws the sign to the ground and celebrates or loots.
- [x] G14 (built Germany chat 5: _door_walk: in to IN_D 15.2, sideways to IN_SIDE behind the wall, back at OUT_D 16.0; props clipped too (draw_prop); ALLOWED_POPS moved to the corner) The looters who run into the shop vanish mid-frame: they go round a corner inside, out of sight (not a pop).
- [x] G15 (built Germany chat 5: UP_STONES 3.9/4.5 chip, 5.2 through; t2_upstairs: hole, cracks, glass falls and lies still) Some thrown rocks hit the upper (first-floor) window: chip it / shatter through.
- [x] G16 (built Germany chat 4: photo arrived as de5; cast DRESS['t2']: tops black/dark-grey/navy/grey/light-grey/khaki, puffers, grey joggers, light-grey trousers, white trainers, hood/beanie/cap, black/blue/white/grey masks, teal backpack; per rioter from his name; F19 adds DRESS['t3']) Reference photo of the Frankfurt looting: diversify the rioters' clothing from it, and note anything else it teaches.
- [x] G17 (built Germany chat 5: pose carry_run (sprint gait + carry arms, cast); EXIT per looter: right, near right, near left, at us) The looters leaving the shop sprint out in different directions, fleeing (not a calm walk off left).
- [x] G18 (built Germany chat 5: BOARD_TO (1.0, 9.8), 0.75 s, 1 m arc (1.5 m hid the third hit), two turns: 3.4 m, was 1.9) The kicked A-board flies further across the scene.
- [x] G19 (built Germany chat 5: sfx() in soundtrack: crowd from 15 s under T2, wood x4, glass at 2.95, stone per stone, glass upstairs 5.2) Sounds (Sam's files, sounds/protest-tiers/): wood-smash.mp3 for the sign hits; glass-smash.mp3 for the shatter; stone-hit.mp3 for the rocks; protest-crowd.mp3 under the scene, taken from 15 s into the file onwards (it has voices from there).
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
- [x] S8 Sam's Y to carry on past the round2 stage stop (16 Nov).
- [x] Q1 (Sam 16 Nov, on the Germany chat 5 clip) "Almost done ... Overall really good."
- [ ] G20 (Sam 16 Nov) Some of the glass fractures on the main window spread beyond the frame. - Plan: t2_chips draws on its own layer, masked to the window rect T2_WR (screen), so no crack line leaves the pane.
- [ ] G21 (Sam 16 Nov) The people who collect the pistols should run off in different directions; now they pace off with the same movements in the same direction. - Plan: new pose 'gun_run' in the cast (sprint gait + the gun_up arm; add to the gait branch at line ~951 and the gun_up arm branch ~1063). After each take: 0.25 s step back and turn, then sprint at moves.speed('sprint'): runner1 (takes 3.6, from (0.95, 13.45)) toward us-left to (-4.0, 9.9); runner2 (3.75, from (1.7, 13.45)) toward us-right to (4.5, 10.0); the swinger (4.85, from (-0.2, 13.45)) left along the shop front to (-5.0, 13.2). Check paths against runner3 at (-1.2, 12.7) and the door traffic.
- [ ] G22 (Sam 16 Nov) Move the sign to the right a little and have the kick land more convincingly. - Plan (the A-board): BOARD (-0.4, 12.75) (was -0.7), runner3's keys +0.3 m (kick from x -1.2). Why it looked weak: the board leaves at 2.3 but the kick's foot strikes at u 0.6 = 2.42, and the board's tilt snaps 0 -> 90 on the kick frame. Fix: BOARD_KICK 2.42 (the strike), BOARD_LAND 3.17, tilt 810 * ease(u) (smooth from standing, two and a quarter turns, face down), a 0.1 m bounce on landing before the skid; BOARD_TO about (1.3, 9.8).
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
- **T2 Germany (8.5 s since round 2, 4/10; Germany chat 5):** 0.35-1.1 stones from off left chip the glass; 0.2-1.55
  the haulers sprint in and lever the shutter up; the swinger hits the glass four times (1.6, 2.05, 2.5, 2.95), more
  cracks each time, through at 2.95, flings the sign down 3.2, cheers, loots a pistol 4.85 and goes off left; runners
  1-2 throw, take a pistol each 3.6/3.75, walk off left guns up; runner3's run-up and kick 2.3: the A-board flies 3.4 m
  toward us, two turns, lands 3.05 (G18); hauler1 kicks the door 2.45; four go in 2.75-3.75 and round the corner inside
  (G14); upstairs: stones 3.9 and 4.5 chip the lit window, 5.2 goes through, its glass falls and lies still (G15); out
  with stock at 4.6/5.6/6.6/7.6, a burst out of the door then a sprint: right, toward us right, toward us left, straight
  at us (G17); the blue at 6.8, everything carries on to the cut. Near us at both edges, heads and shoulders (G12).
  Sound (G19, O9): the crowd under it all (its file from 15 s), wood at each hit, glass at the shatter and upstairs,
  a stone for each stone, Sam's ding at 2.0, the siren at 6.8.
  **T2 acting list (rule 74; no lines in Germany, so the moves):** the swinger winds up and jolts back off the glass
  each hit, then fists pumped, half turned to us, before he loots; runners eye the cubbies and reach; looters come out
  heads down at a flat-out sprint, stock hugged; the near crowd faces the shop, signs jab on the chant, phones swing
  round after the looters at 4.7. Checked against the stills 7.6-14.4 (Germany chat 5).
- **T3 France (8 s, 8/10; round 4 re-time, F12-F23, back-half chat 7):** **0.0** already mid-riot: the front and back
  rows in place and throwing at their own phases (no walk-in, F12); both cars burning (silver by Marianne, red on the
  police side, F17), their smoke drifting right to left over the crowd (F21); the square full: crowd round the base's
  right, CRS reserve and cordon behind the block (F13). **1.25-1.7** a canister from the police block lands in the
  crowd's front rows, the gas spreads there, the nearest turn away (F14). **2.0-3.4** the water cannon drives in from
  the right. **3.5** jet on; **3.55-7.0** it walks down the rioters' line far to near, each thrower breaking and running
  left as it reaches him (F23); the marchers stay protesting in place (F22). **3.7** the police step forward in lockstep,
  shields up (F2). **7.0-8.0** the line holds, the last rioters run off left (so T4 opens bottom-left).
  **T3 acting list (rule 74; no lines in France, so the moves):** throwers: each his own style (overarm, sidearm, lob),
  arm speed 0.5-0.9 s, a stoop to pick up a stone between throws, stones 5-6 cm (F16, F20); hit by the jet: knocked a
  step, turn (blended) and sprint off the left edge; gassed marchers: turn away; on the base: cheerers wave, flags
  sway; police: shields up while missiles fly, each jolts toward the hit near him, the rear file holds shields
  overhead, small shuffles and turns, then the lockstep advance (F18); truck: up the lane, jet on the throwers; cars:
  no one near (people keep off a fire). Checked against the moves (chat 7 stills 14.6-21.8): matches.
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
| ALLOWED_POPS | carrier* | A7: the four carriers step up out of the middle crowd under the surf shield at 8.6 s | NOT yet looked at full size: Albania chat 4 (step 11) |
| ALLOWED_POPS | surfer | A7: hoisted up out of the middle crowd at 8.6 s | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | mr* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | mp* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | gun* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | mid* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | mol* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | dan* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | cov* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | carrier* | T4 round 3 (A4): crowd sprites step their moves in sixths (punches, machetes, throws, dances, bursts, the pop over the sandbags), so hands/arms/legs jump one drawing a frame by design; bodies still checked | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | granny* | A8: her overarm Molotov throw at 3.4 s (a throwing hand ~20 m/s) | NOT yet looked at full size: Albania chat 4 (step 11) |
| FAST_OK | selfie* | A7: the turn at the hit and the cheer after the crash | NOT yet looked at full size: Albania chat 4 (step 11) |
| ALLOWED_CONTACTS | mp* / mr* | A4: the melee: fists, machetes and batons meet on the line; ranks packed (depth-capped 0.25 / 0.08) | NOT yet looked at full size: Albania chat 4 (step 11) |
| ALLOWED_CONTACTS | carrier* / surfer | A7: the carriers hold the shield he rides, shoulder to shoulder | NOT yet looked at full size: Albania chat 4 (step 11) |
| ORDER_SWAPS | mp* / mr*, carrier* / mid*, gun* | A4/A7: the melee's wandering contact line; the surf carried through the middle crowd | NOT yet looked at full size: Albania chat 4 (step 11) |
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
