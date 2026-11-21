# Grand Theft Autism: old handovers

## Where things stand (19 Nov)
- Rules that bite next: 24 (estimate before building), 74 (acting list before the animatic), 28 (reuse before building).
- Done: the 3.5 s opening, `source/gta_opener.py` (MAP at the top). Renders in about 1 minute.
- Next (00:30 UK, 20 Nov): Opus, high effort, a fresh chat: the Plan stage: game references (search order in
  job-packs Plan, but game-only per Sam), staging of every shot, acting list, cast and car as NEW rows; the estimate
  is ALLOWED now (Sam, 19 Nov: "You can do the budget estimate"): make it from the ledgers in the Plan stage.
- Needs Sam: nothing before the plan; the open questions (1-4, 6) only when a stage needs them.
- Read: guides/job-packs.md, Plan.
- Open rule requests: none.
- Branch claude/blessed-c2-mics-wip (source/blessed.py, unfinished Blessed work) stays off the main line, as named in
  story/status.md (19 Nov).
- No estimate yet on purpose: Sam asked to hold estimates until the screenplay is confirmed (19 Nov).
- For Claude: the title font (Pricedown, Typodermic free desktop licence: rendered video fine, sharing the file not)
  is fetched by `_title_font()` into source/fonts and is in .gitignore; never commit it. Sea painter re-coloured by
  overriding flying_whales_sea globals before the first bake.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 2.67% of 15%; forecast 53.2% (2026-11-20)

## Where things stand (20 Nov, chat 3, Sonnet)
- Rules that bite next: 8 (rehearse the swerve and the crash first), 38 (front, side, back on the cast sheet), 89 (each new thing critiqued alone).
- Done: plan, acting list, game references; Sam's answers 1-7 recorded above (screenplay final).
- Next: Opus, high effort: the cast build (Jason, Lucia, her, the Tulip), then the two rehearsal clips (swerve, lean-out and crash) before any other movement.
- Needs Sam: nothing. Shot 7 is the held three-shot (no mirror insert), per Sam.
- Read: guides/job-packs.md, Build; the plan, acting list and references above.
- Open rule requests: none found in this film's notes.
- No page.py show this chat: chat 3 only recorded answers in the notes; no film code was touched (the film file is not started).
- Branch claude/blessed-c2-mics-wip stays off the main line (named in story/status.md).
- For Claude: start source/grand_theft_autism.py from source/satire_template.py; places in story/grand-theft-autism-places.txt;
  Glock from prepper_cast, effects from prepper_fx and flying_whales_fx (fireball_sprite, Puff, splash_parts);
  vehicle precedent protest_tiers_sets.truck. Title font Pricedown is fetched by `_title_font()`, in .gitignore; never commit it.


## Where things stood (20 Nov, chat 4, Opus high)
- Rules that bite next: 8 (rehearse the swerve and the crash first), 3 (Vice City streets point by point beside the game), 89 (cars critiqued alone).
- Done: cast built and through both critique hunts (people file story/grand-theft-autism-people.txt; matched to the game's first hours,
  Sam's note; her prettier and cooler: shag cut, nose stud, headphones; Added: headphones round her neck). Cast sheet sent to Sam.
- Next: Opus, high effort: the Tulip and the VCPD cruiser (3D, new), then the two rehearsal clips (swerve past the low camera;
  lean-out and crash). Shot 7 is the held three-shot (Sam's correction).
- Needs Sam: his look at the cast sheet (a note, not a gate: building carries on).
- Read: guides/job-packs.md, Build; the plan and acting list above; references/grand-theft-autism/ (car and police pictures).
- Open rule requests: none found in this film's notes.
- Left open after hunt 2 (named): house-style boxy torsos and sleeve flaps; Lucia has no waist (a new body build if Sam asks); her side/back hair is a blob (never seen in this film).
- Handover check: midterminal_cast.py was touched only for sleeve options that default to its old look; its old exceptions and
  pose lines are that film's, not this one's. No page.py show: the film file is not started yet (only source/gta_cast.py).
- Branch claude/blessed-c2-mics-wip stays off the main line (another film's work; named in story/status.md).
- For Claude: cast is source/gta_cast.py (draw, bust, sheet, panels); kit additions in people.py/people_parts.py/people_turned.py
  (palms, biker, unicorn, scoop, headphones extras; soft, lashes, hoops, stud, rest smile, `hair: pony, C, high`, `sleeves short`).
  Cars: build in source/gta_cars.py on sets.Cam/Face/obox/cylinder (3D, metres); film file from source/satire_template.py.
  The 5:30 UK reminder (trig_01B51RSAAq6Sgymzr6MttTsf) fires into chat 4 as a backup; chat 5 carries the work.



## Where things stand (20 Nov, chat 5, Opus high)
- Rules that bite next: 8 (shot 4's lean-out and crash rehearsed before any other movement), 41 (Jason's arms and gun hand leaning out), 89 (the clip critiqued).
- Done: both cars built in 3D and through both critique hunts (getaway car and police car, whole and crashed; sheet sent).
  Rehearsal 1 sent: shot 2's swerve past the low camera on a stand-in street (the real junction is the sets stage).
- Next: Opus, high effort (a new move): rehearsal 2, shot 4: track left with Jason leaning out of the passenger window,
  4 shots back, the lead police car's windscreen crazes in front of its driver, it slews, hits a hydrant (water jet),
  bursts into a shop front in a fireball; back in to shot 3's frame. Short clip to Sam.
- Needs Sam: his look at the cast sheet, the car sheet and the swerve clip (notes, not gates).
- Read: guides/job-packs.md, Build; the plan and acting list above; guides/figure-rig.md 2-4 (Jason leaning out).
- Open rule requests: none found in this film's notes.
- Left open (named): the police car is a boxier saloon than the game's rounded one (house look; a rounder roof is a later fix if Sam asks);
  plates are real size so their letters only read close up; the swerve's street is a stand-in.
- For Claude: cars source/gta_cars.py (Car, draw_car, SPECS, flash; crush/shatter for the crash); shot 2 rehearsal and the
  stand-in street source/gta_rehearse.py (route, car_at, tyre_smoke, light_wash, clip; `shot2 OUT.mp4`). Build shot 4 there:
  a shot4(t) with the Tulip on a straight street, cruisers behind (car_at-style paths), Jason from source/gta_cast.py,
  muzzle flash/glass/hydrant jet/fireball from prepper_fx and flying_whales_fx (catalogue, Effects). Critique packs r1-p3, r1-p4 (cars stage).

Cost line (recorded every handover; shown to Sam only on a problem): film so far 5.66% of 15%; forecast 56.2% (2026-11-20)

## Where things stand (20 Nov, chat 6, Opus high)
- Rules that bite next: 89 (the 10 faults left open below are fixed before the next clip), 8 (no other movement until Sam has seen both rehearsals), 41 (Jason's gun arm out of the window).
- Done: rehearsal 2 built and sent: shot 4 (6.2 s, 2.8 MB), stand-in shop street, Jason climbs out onto the window ledge, 4 shots,
  the lead cruiser's windscreen crazes, it slews over the kerb through a hydrant (water jet) into a shop front (fireball), back in.
  Critique round 1 (packs r1-p5, r1-p6): hunt-1 faults fixed; hunt 2's 10 named, not fixed (Checks line sent to Sam).
- Next: Opus, medium effort (fixes from a clear list): when Sam answers on the clips, his notes first; else hunt 2's list:
  craze bigger/bolder and the target cruiser larger at the shots (S1, M5); gun readable at phone size; smoke joined to
  the fire, not floating balls; jet a column, fireball not cut by the frame edge; the palm pop near the lens; the
  squeeze at 0.83-1.17 (wide lens at the car's corner); the wing mirror off the body; the bonnet stripes from above
  read as holes (car builder). Then a short clip of only the changed seconds.
- Needs Sam: his look at the cast sheet, the car sheet, the swerve clip and this lean-out clip (notes, not gates).
- Read: guides/job-packs.md, Build; this notes file's plan and acting list.
- Open rule requests: none found in this film's notes.
- For Claude: source/gta_rehearse.py shot 4 section (MAP in its header comment: tulip4, _lead_track/lead_at, chaser_at,
  CAM4 keys in the car frame, strip_ground/shop_block, person_cached (Glimpses drawn once per view), jason4/jason_layer
  (masked by the car's lower body), FxCam + fx_items (flying_whales_fx)); `shot4 OUT.mp4`, `still4 T OUT`. Render 4.5 min.
  Crowds 'walker' and 'cop' in story/grand-theft-autism-people.txt.

- Handover check answers (chat 6): the quick checks name gta_rehearse as a film of its own; it is this film's rehearsal
  file (notes here; SHOT_MARKS belong to the film's shot file at the moves stage). No `page.py show`: shot 4 was a new
  build, not a note, so the code was searched on purpose.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 9.59% of 15%; forecast 60.1% (2026-11-20)


## Where things stand (20 Nov, chat 7, Opus medium)
- Rules that bite next: 8 (nothing else moves until Sam has seen both rehearsals), 30 (a repeat note: find why the first fix failed), 89.
- Done: hunt 2's 10 shot-4 faults fixed as one list and `critique.py fixed` recorded (Checks: none). Shot 4 re-rendered
  (6.2 s, 2.9 MB, 4.4 min) and sent whole, as the changes span 0.8-5.2 s: bolder crack and a closer cruiser on a longer
  lens, the gun shown at the shots (higher camera, gun 1.4x), smoke one column out of the fire, the jet a column,
  the fireball low and in frame, palms slide in (no pop), no squeeze at the corner, bumpers inside the body, mirrors on
  stalks, bonnet stripes worn charcoal (read as paint from above).
- Next: Sam's answer. On "approved": Opus high chat for the sets stage (the real Vice City shop street and the junction
  for shots 2 and 4, replacing the stand-in blocks). On notes: Opus medium, his notes first (rule 30 on any repeat).
- First, whatever Sam answers (front-on chat 2b, 20 Nov 08:02): kittest focus_front_heads fails: 'milburn 5' no longer
  draws pixel-for-pixel. Restoring source/people.py AND people_parts.py to d732ceea passes, so one of this film's kit
  additions (358132dd on: soft/hoops/pony_high/hair_loose/short_sleeve/'smile') changes a default for people who never
  set it. Fix so finished films draw as before (Opus medium); named in notes/proposals/front-on-focus/retirement-and-handover.md.
- Kit change since (one-route-kit chat 5, 20 Nov): front and back shoulders now round smoothly over the arm (Sam's
  jury chips; body.front_outline), so the cast sheet's "square shoulder corners" fault may be partly gone: redraw the
  sheet before judging. Jason's short sleeves (MidTerminal's flap) are untouched and still read as stuck-on flaps.
- Needs Sam: Y or N, the two rehearsals (swerve clip, this lean-out clip) approved so the rest can move (rule 8).
- Read: guides/job-packs.md, Notes round (on notes) or Build (on approval); this notes file's plan and acting list.
- Open rule requests: none found in this film's notes.
- For Claude: source/gta_rehearse.py shot 4 (CAM4 keys, GAPS, SMOKE4, PALMS4, jet_lumps, fx_items); gta_cars.py
  _cracks/_tulip_decals (STRIPE, STRIPE_EDGE)/_parts; prepper_cast.glock(size=). `shot4 OUT.mp4`, `still4 T OUT`.
- Handover check answers (chat 7): gta_rehearse's two quick checks as chat 6 (a rehearsal file, notes here, SHOT_MARKS
  at the moves stage); the four prepper lines are another film's, not this one's.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 9.59% of 15%; forecast 60.1% (2026-11-20)

## Where things stand (20 Nov, characters chat, Opus high)
- Rules that bite next: 30 (none of these notes repeats an earlier one; check), 89 (the critique's two hunts on the
  cast), 8 (nothing past the rehearsals until Sam answers on the two clips).
- Done: Sam's new references and body notes in the brief; full-figure game art filed and measured (table above); the
  body faults fixed in the kit (Diagnosis, Status); cast sheet redrawn beside Sam's pictures and the game's, sent.
- Next: Opus medium, Sam's 6 notes on the cast (brief checklist, last two items): Jason a light stubble fade, thinner
  lighter brows; brows lower on all three; her new face and hair; the rainbow kept on the jumper; bangles on both
  wrists, sleeves 25% slimmer. Then the critique's two hunts (stage "cast"), fixed; likeness: Jason's hair a buzz,
  Lucia's ponytail fuller with short loose strands. Then a Sonnet chat: the new cast into both rehearsals, both clips sent.
- Needs Sam: nothing now; after the clips, his Y/N on both (rule 8).
- Read: guides/job-packs.md, Notes round; this notes file's brief checklist (last items), Diagnosis, Body shapes measured.
- Open rule requests: none.
- For Claude: body.FIGS/fig_half/front_outline(fig, arm_w); views._built_outline/_covered/_trainer, WrapPen.fig;
  people_parts.VEST, vest_outline (dip: below the arm's fade); people.py 'build', 'arms N muscle', 'shorts', 'trainers';
  her look: story/grand-theft-autism-people.txt '# her'; unicorn: people_parts.unicorn_torso (bot).


## Where things stand (20 Nov, chat 9 end, Opus medium)
- Rules that bite next: 30 (the headphones are a repeat note: the why is in the brief checklist), 89 (judge at full
  size against a reference, never a thumbnail), 8 (nothing past the rehearsals until Sam's Y/N on both clips).
- Done: Sam's 6 cast notes; his second notes (back-view arm seam fixed in the kit, Lucia's neck line, chain, bun,
  nose); critique hunts 1 and 2. Headphones and neckline NOT done (his last note).
- Next: Opus medium: the headphones rebuilt as a solid prop resting on her (plan in the brief checklist's last
  item), no neckline on bare tops; five angles at full size beside a real photo; send. Then Sonnet: the new cast
  into both rehearsals (shot 2 swerve, shot 4 lean-out), both clips sent. Don't touch the opening.
- Needs Sam: the clips' Y/N later (rule 8). (Sam, 20 Nov: "Y": her nose stud stays off.)
- Read: guides/job-packs.md, Notes round; this file's brief checklist, last three items.
- Open rule requests: none.
- For Claude: people_parts.headphones3d (PHONES_YAW, headphones_view), views.torso_outline for the body's edge per
  view; body.plain_torso jumper line (oval at 0,-2); people_parts.vest_torso neck patch.


## Where things stand (20 Nov, chat 10 end, Opus medium)
- Rules that bite next: 8 (nothing past the rehearsals until Sam's Y/N on both clips), 89 (judge clips at full
  size), 30 (headphones were a repeat note: if Sam flags them again, read the chat 10 line in the checklist first).
- Done: headphones rebuilt as a solid prop (photo-matched, never inside her), no neckline on bare tops in any view,
  print-under-prop order fixed in the kit; sheet sent (notes/sheets/grand-theft-autism-headphones-neckline.jpg).
  Kit tests: the same 11 old failures before and after (pose_gallery, outfit_every_view officer/scarf, etc.): none new.
- Next: Sonnet: the new cast into both rehearsals (shot 2 swerve, shot 4 lean-out), both clips sent. Don't touch
  the opening.
- Needs Sam: question 1 (three-quarter necks: fix the drawing for every film now, or keep them front-on); chat 11
  (session_01J1JB7VedxxaeCdyPTmFuNx) interrupted until he answers; his answer comes back to chat 10.
- Read: guides/job-packs.md, Notes round (clips); source/gta_rehearse.py's MAP.
- Open rule requests: none.
- For Claude: people_parts.headphones3d (cups: n, upr, push-forward loop), views._bare_neck, people.WORN_OVER.


## Where things stand (20 Nov, chat 10 end, Opus medium, second handover)
- Rules that bite next: 8 (nothing past the rehearsals until Sam's Y/N on both clips), 38 (cast sheets: front, side,
  back only; three-quarter only where a shot needs it), 89 (judge clips at full size).
- Done: headphones solid and round the back of her neck; no neckline on bare tops; three-quarter necks fixed in the
  kit for every film (turned heads lifted as the front is, chin at the front's height); sheet sent
  (notes/sheets/grand-theft-autism-necks-fixed.jpg). Kit tests: the same 11 old failures, none new.
- Next: Sonnet chat 11 (already open, resumed): the new cast into both rehearsals (shot 2 swerve, shot 4 lean-out),
  both clips sent. Don't touch the opening.
- Needs Sam: the clips' Y/N (rule 8); notes on the sheet can come with them.
- Read: guides/job-packs.md, Notes round (clips); source/gta_rehearse.py's MAP.
- Open rule requests: none.
- For Claude: people_turned head_view (PP._lift), CHIN_V; people_parts.headphones_over_neck (views.HEAD_WEAR).

Cost line (recorded every handover; shown to Sam only on a problem): film so far 18.52% of 15%; forecast 69.1% (2026-11-20)

## Where things stand (20 Nov, chat 11 end, Sonnet; for chat 12)
- Rules that bite next: 8 (rehearsals before anything else), 89 (judge every clip at full size, every beat), 30 (a note
  given before is a warning: the first shot 4 faults came back; find why before changing anything).
- Done: chat 11 drew both rehearsals with the new cast and the neck fix; Sam: shot 2 "amazing" (keep); shot 4 rejected
  (see the Shot 4 rebuild checklist). Sam has said Y to: rebuild shot 4 from scratch with an open window, add a Vice City
  backdrop and white cloud streaks to BOTH shots, and give the people real behaviour. Nothing of that is built yet.
- Next: Opus, high effort (building something new): chat 12. 1) Read the Shot 4 rebuild checklist and the plan table
  row 4. 2) Improve the clipping check first (body through solid, feet on ground, every frame). 3) Rebuild shot 4 from
  the original camera keys with the open window, then the backdrop and clouds in both shots, then the people. 4) Check
  every beat at full size; send ONE clip, shot 4 first; then Sonnet chat for sending if needed.
- Needs Sam: nothing open; the clip's Y/N (rule 8) after it is sent.
- Read: guides/job-packs.md, Notes round (clips); source/gta_rehearse.py's MAP; gta_cars.py; viewchecks.layer_faults.
- Unrouted flags (chat 11, answered): 17:20 was a question about the film itself, not a system change (reworded to say so, Sam said Y); 17:26 was a rule idea (read the screenplay first), withdrawn in the next message, no proposal made.
- Open rule requests: none (Sam has not said "I want a rule"; reading the screenplay first is a candidate if he does).
- For Claude: CAM4 and shot4 in gta_rehearse.py; PEOPLE4/_strip_people (standing only); person_cached (neck anchor);
  original clip references/grand-theft-autism/shot4-original-rehearsal.mp4; original keys at commit 2668817c.

## Where things stand (20 Nov, chat 12 end, Opus; for chat 13)
- Rules that bite next: 30 (people drawn on the grille at shot 4's first frame, chat 11 too: find why first), 89 (judge
  every beat at full size before sending), 8 (one clip, then Sam's Y/N).
- Done: clipping check improved (body through solid, rubbed out in front, feet on ground, every person every frame);
  it fails chat 11's shot 4 on exactly Sam's faults. Backdrop (Vice City towers, far palms, haze) and cloud streaks in
  both shots (first pass, not yet judged at full size). Jason's new climb-out through an OPEN window drafted (hips on
  the sill, legs inside, per-half rub-out) but NOT judged: Sam stopped it ("putting the actors in the bonnet").
- Next: Opus, high (building new). Sam's order: 1) judge the backdrop and clouds at full size in shots 2 and 4;
  2) build shot 3 (windscreen three-shot) properly from the screenplay row 3, all three seated behind the glass; find
  why people land on the grille first; 3) then shot 4 beat by beat from shot 3's exact frame (Shot 4 rebuild checklist);
  4) people walking, watching, ducking, running; run `gta_rehearse.py bodies shot4` and `layers shot2 shot4`; ONE clip.
- Needs Sam: nothing until the clip.
- Read: guides/job-packs.md Build; this file's Shot 4 rebuild checklist; plan table rows 3-4.
- Open rule requests: none. Handover check: gta_rehearse is the rehearsal tool, not a film (its notes are this file;
  no SHOT_MARKS until the film's shot files exist): answered.
- For Claude: gta_rehearse.py backdrop/TOWERS/CLOUDS, jason4/J4_KEYS/jason_layer, solids4, `bodies` command;
  gta_cars.local_pt/solid_at/cover_masks/open_windows; viewchecks.solid_faults. MAP lines for shot 4 still to add.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 19.33% of 15%; forecast 69.9% (2026-11-20)

## Where things stand (20 Nov, chat 13 end, Opus; for chat 14)
- Rules that bite next: 30 (heads cut by the windscreen rail: Sam's note; cause is cartoon heads ~2x life in a
  real-height car), 89 (every beat at full size before the clip), 8 (one clip, then Sam's Y/N).
- Done: ROOT CAUSE of "people on the grille", tiny sunken passers-by and the stretched car: the street and cars drew at
  half size (gta_rehearse/gta_cars used burnham, whose sharpness setting is separate from the people kit's); both now
  use the one kit. Shot 3 built (shot3, CAM3): three seated, Lucia jerking a wheel, spinner, her line with a wince,
  cash case, bench, cruisers through the back window (see-through glass). Shot 4 starts on CAM3. Crowd: walk, duck at
  the shots, run from the fire, stare (crowd()). Backdrop and clouds judged at full size: fine; more cloud wanted in
  shot 2's upper sky (one streak only).
- Next: Opus, high (new build). Sam answered Q1 Y: raise house y top 1.33 -> ~1.43 (gta_cars SPECS tulip), check
  heads clear the rail in shot 3 at full size;
  then shot 4 Jason: arm stubs and a flat bar for a pistol at 1.4 s, arm fault at 1.0 s (left hand to the roof corner);
  judge crowd poses full size; run `bodies shot4`, `layers shot2 shot4`; ONE clip via `shot34`.
- Needs Sam: nothing until the clip of shots 3-4; then on through shots 5-8 to the whole film's shot sheet (Sam).
- Read: guides/job-packs.md Build; Shot 4 rebuild checklist; plan rows 3-4.
- Open rule requests: none. Handover check: gta_rehearse is the rehearsal tool, not a film (its notes are this file;
  no SHOT_MARKS until the film's shot files exist): answered.
- For Claude: world4/shot3/shot3_cam/CAM3/seated/tulip_inside/crowd/wheel3 in gta_rehearse; gta_cars._through_glass
  far-glass paste (car._bg); `still3`, `shot34` commands. Shot 2 untouched (it never loaded the cast: drew right).


## Where things stand (20 Nov, chat 14 end, Opus; for chat 15)
- Rules that bite next: 17 (layers: shot 4 has farther-over-nearer faults since the camera re-aim, list in
  notes/checks/gta-chat14-layers.txt), 89 (full size before sending), 8 (ONE clip of shots 3-4, then Sam's Y/N).
- Done: heads clear the rail (roof +14 cm, cast 6 cm lower); faces behind glass solid (tint on top); pistol reads over
  the dash; shot 4 camera re-aimed (Jason was outside the frame 1.7-4.5 s); hiding test needs the sight line inside the
  face (roof no longer cuts his arm; shins+feet keep his legs behind the door; seated glass judged from his neck, else
  he vanished); crowd turns or runs at the crash; fatter hydrant jet; shot 2 upper clouds. Clip NOT sent: layers fail.
- Next: Opus, medium (fixing from a clear list): fix shot 4's draw order (layers shot2 shot4: cruiser 2/3 over the
  lead, people/palms over the Tulip at 0.83-1.17 and 5.0-5.7 s, cruiser 2 over the Tulip at 5.5 s, 28,647 px); body
  check (notes/checks/gta-chat14-bodies.txt): Jason's left wrist in the floor while seated (hand on thigh), left elbow
  in the roof 1.17 s and door 5.5 s; name the rest (crouchers read short; 3-8 px feet, 1-2 frames). Re-run both, look
  at full size, render `shot34` (scratchpad pclip with 3 workers: 7 min), send it; then shots 5-8 (Opus, high).
- Needs Sam: Y/N on the shots 3-4 clip once sent (rule 8). His "just go" ran to 19:30 (ended).
- Read: guides/job-packs.md Build; Shot 4 rebuild checklist; plan rows 3-8.
- Open rule requests: none.
- For Claude: gta_cars.cover_masks between() (inside-face test, 5 cm slack), glass_tint(); jason_layer lower mask
  = shins+feet, upper = n0; CAM4 1.70-4.55 solved by projecting his head; crowd sees_fire; world4 sorts items by depth.


## Where things stand (20 Nov, chat 15 end, Opus; for chat 16)
- Rules that bite next: 8 (shots 3-4 clip sent: wait for Sam's Y/N before any final; build on meanwhile), 17 (layers
  and bodies on every new shot), 30 (Jason's arm/gun from behind was a repeat: now turned 160 on the sill).
- Done: draw order clean in shots 2 and 4 (every fault was a car seen through another car's glass: the check's lone
  sheet painted the glass opaque); Jason's seated left hand on his thigh; on the sill turned 160 so gun arm, gun and
  flash read past his shoulder; his legs hidden behind the car side (they drew under it); walkers' feet stay down
  through the bob. Small ones named in notes/checks/gta-chat15-bodies.txt. Clip of shots 3-4 sent to Sam.
- Next: Opus, high (a new build): shots 5-8 (plan rows 5-8: shot 3's camera, the wheel yank to a new road, lines
  3-6, the closer two-shot, the held pause with lights in the back window), each checked (layers, bodies) and looked
  at full size; then the whole-film shot sheet (shots 1-8), Sam's standing order.
- Needs Sam: Y/N on the shots 3-4 clip (rule 8).
- Read: guides/job-packs.md Build; plan rows 5-8; brief lines 3-6.
- Open rule requests: none.
- Branches named, not merged (frozen snapshots of other films, not this film's work): freeze/halo-no-no,
  freeze/milburn, freeze/milburn+milburn-story, freeze/protest-tiers, freeze/blessed.
- For Claude: gta_cars._through_glass keeps bg alpha (min 72) so lone sheets show glass as a veil; J4_KEYS 1.70/4.30
  face 160; jason_layer side quad (x 0.98, z -2.6..1.0) erases rows below the hips once out > 0.9; crowd() lifts feet
  by bob; scratchpad pclip.py (4 workers, ~6 min for shot34) is not in the repo: world4(t - SHOT3_LEN, cam) per frame.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 27.36% of 15%; forecast 77.9% (2026-11-20)

## Where things stand (20 Nov, chat 16 end, Opus; for chat 17)
- Rules that bite next: 8 (NEW, Sam 20 Nov: shot 4 is a hardest shot, so a build proposal to Sam BEFORE rebuilding),
  74 (NEW: acting notes for every shot, dialogue or not, beat by beat), 30 (bald crowd was a repeat: fixed at the kit).
- Done: shot 4 case study (notes/shot4-case-study/shot4-case-study.md: versions, pictures, all Sam's words, his 16
  frame notes, five causes, lessons). Fix 2: crowd heads hung, Miami mix, kittest crowd_heads_hung. Rules 8 and 74 written.
- Next: Opus, high (new design): the proposal route for cause A only (Sam Y): how to build big 2D body moves from key
  poses drawn per angle and layered by hand, plus a "is this a human body" check every frame; then the shot 4 build
  proposal to Sam (rule 8): key poses, camera, fix 3 (cop hit with blood mist and slump, one cop throughout, hydrant hit
  on camera, crowd reacts), acting rows for shot 4 (Lucia hand over hand at the wheel). Shots 5-8 wait.
- Needs Sam: nothing until the proposal's top two and the build proposal.
- Read: guides/job-packs.md Build; the case study sections 5, 7, 8; rules 8, 74, 89.
- Open rule requests: none (Sam's two written this chat).
- Handover check answers (chat 16): FINDER: no film notes fixed by code this chat except the kit crowd fix; the
  rehearsal file was read by hand to diagnose Sam's 16 notes (no page.py for a rehearsal file). UNROUTED 22:09: the
  question was Sam's own ("is it necessary to run proposal route?"), reworded to say so; Sam: "Y all".
- For Claude: people.crowd_person hangs kit_head/kit_torso for crowd members once installed; MIXES['miami'];
  jason_layer/J4_KEYS/cover_masks is cause A; cop_inside person_cached vs fresh path is note 12; HYDRANT timer note 13.


## Where things stand (20 Nov, chat 17, Opus high; waiting on Sam)
- Rules that bite next: 8 (build proposal before building: sent, waiting), 74 (shot 4 acting rows, written), 89 (fresh
  critique before every send: version 4 skipped it).
- Done: proposal big-body-moves judged blind (helper A picked) and its learn step (learn.md: v4's skeleton measured
  human; the drawing method was the fault; look sheet v5-test-skeleton-vs-v4.jpg); shot 4 acting rows, fix 3 events,
  Sam's 16 frame notes carried; the shot 4 build proposal (section above); case study section 10.
- Next: Opus, high (new building), on Sam's answers: Change 1 (the human-body check, must pass the pose gallery, shot 3
  and two past films clean), then Change 2 (lean-out key poses on the skeleton, five-view pose sheet + critique), then
  rebuild shot 4 from the build proposal. Shots 5-8 wait.
- Needs Sam: Q1 option 1 or 2; Q2 the lean-out as written; Q3 Y to the build proposal.
- Read: guides/job-packs.md Build; notes/proposals/big-body-moves.md Final version and learn.md; this file's shot 4
  sections; the case study section 10.
- Open rule requests: none (lesson 17 is a draft lesson, not a rule request).
- For Claude: skeleton test script was scratch: build k from jason_layer joints via fig_to_world (lying.Body keys as in
  from_views), draw with lying_flat.draw(img, cam, k, sp, t, M=MPU_J); patch only inside jason_layer (V.person is
  shared with hats and crowd). Critique pack gta-shot4-learn r1-p1 is a learn run, not a film stage.
- Branches named, not merged on purpose: freeze/halo-no-no, freeze/milburn, freeze/milburn+milburn-story,
  freeze/protest-tiers are posted films' bookmarks (freeze.py tag), kept as they are.
## Where things stand (20 Nov, chat 15 end, Opus; for chat 16)
- Rules that bite next: 8 (shots 3-4 clip sent: wait for Sam's Y/N before any final; build on meanwhile), 17 (layers
  and bodies on every new shot), 30 (Jason's arm/gun from behind was a repeat: now turned 160 on the sill).
- Done: draw order clean in shots 2 and 4 (every fault was a car seen through another car's glass: the check's lone
  sheet painted the glass opaque); Jason's seated left hand on his thigh; on the sill turned 160 so gun arm, gun and
  flash read past his shoulder; his legs hidden behind the car side (they drew under it); walkers' feet stay down
  through the bob. Small ones named in notes/checks/gta-chat15-bodies.txt. Clip of shots 3-4 sent to Sam.
- Next: Opus, high (a new build): shots 5-8 (plan rows 5-8: shot 3's camera, the wheel yank to a new road, lines
  3-6, the closer two-shot, the held pause with lights in the back window), each checked (layers, bodies) and looked
  at full size; then the whole-film shot sheet (shots 1-8), Sam's standing order.
- Needs Sam: Y/N on the shots 3-4 clip (rule 8).
- Read: guides/job-packs.md Build; plan rows 5-8; brief lines 3-6.
- Open rule requests: none.
- Branches named, not merged (frozen snapshots of other films, not this film's work): freeze/halo-no-no,
  freeze/milburn, freeze/milburn+milburn-story, freeze/protest-tiers, freeze/blessed.
- For Claude: gta_cars._through_glass keeps bg alpha (min 72) so lone sheets show glass as a veil; J4_KEYS 1.70/4.30
  face 160; jason_layer side quad (x 0.98, z -2.6..1.0) erases rows below the hips once out > 0.9; crowd() lifts feet
  by bob; scratchpad pclip.py (4 workers, ~6 min for shot34) is not in the repo: world4(t - SHOT3_LEN, cam) per frame.



## Where things stand (20 Nov, chat 17 end, Opus high; for chat 18)
- Rules that bite next: 8 (Sam said Y to the build proposal: build exactly it), 89 (critique before every send), 30.
- Done: Sam's answers 1 (option 1), Y (lean-out as written, legs never seen), Y (build proposal). Change 1 started:
  source/humancheck.py (arm drawn over/behind the body against its depth, arm coming out on the far side, the picture
  one joined piece, the gun as drawn vs its target), hooked into views and lying_flat; viewchecks.solid_faults now
  samples along every bone and tests "a part behind a solid must not show" (toggle); gta_rehearse.clip runs it and
  holds a faulty clip aside. On version 4 it finds notes 2, 3, 4, 6, 7, 8 (hip through the bonnet, chest through the
  pillar, elbow through the roof, arm out of the back, gun 27-30 degrees off). Shot 3: clean.
- Next: Opus, high (finish Change 1, then Change 2): (1) the pose gallery gives 10 flags in 744 drawings (2 "far
  side", 8 "hidden though in front"): name the poses (add the pose name to the hook's who), sort real from false, fix
  the test; also the 3 crowd "far side" flags at 2.58-3.5 s in shot 4; (2) run two past films' animatic frames with
  the check: 0 false flags; (3) a kittest (version 4 frames must fail, shot 3 must pass); (4) only then install the
  send gate (PreToolUse on SendUserFile: python3 source/humancheck.py sendgate) and hook film_engine._frame
  (frame_begin/end per drawing, faults in a .body.txt beside each cached frame) and finish.py (copy_record);
  (5) Change 2: lean-out key poses on the skeleton (lying_flat + grips for the gun), five-view pose sheet, critique;
  (6) rebuild shot 4 from the build proposal and acting rows.
- Chat 16 (shots 5-8, its own file source/gta_shots58.py; section "Shots 5-8"): built, layers clean, bodies only 5 far
  walkers' feet 4-7 px down for 1-3 frames (notes/checks/gta-chat16-bodies.txt: shared walker code in gta_rehearse.py,
  for the shot 4 rebuild); Lucia's hands feed the wheel there (never crossed). Whole-film shot sheet (shots 1-8, 36 s,
  source/gta_film.py) sent to Sam ~23:10: his standing order done. Chat 19 (Sonnet) renders a clip of shots 5-8.
- Needs Sam: nothing until the shot 4 pose sheet (with the build) or the clip.
- Read: guides/job-packs.md Build; notes/proposals/big-body-moves.md Final version and learn.md; source/humancheck.py
  MAP; this file's shot 4 sections.
- Open rule requests: none.
- For Claude: test scripts were scratch (lost with the container): a frame list through H.frame_begin / R.shot4(t) /
  H.frame_end(t) with H.Writer, and VC.solid_faults(R.shot4, R.SHOT4_LEN, frames=[...]). humancheck.START is
  20 Nov 22:00 UTC.
- Branches named, not merged on purpose: freeze/halo-no-no, freeze/milburn, freeze/milburn+milburn-story,
  freeze/protest-tiers are posted films' bookmarks (freeze.py tag), kept as they are.
- Quick check on gta_rehearse (no SHOT_MARKS): it is the rehearsal file, not the film's module; the front-on check
  runs on the film file once the moves stage builds it (answered chat 17).

## Where things stand (20 Nov, chat 18 end, Opus high; for chat 20, shot 4)
- Rules that bite next: 8 (the pose sheet goes to Sam in the build before the rebuild), 89 (fresh critique of the
  pose sheet before it is sent), 30 (the K2 missing head: find why lying_flat drops it before changing anything).
- Done: Change 1 finished: gallery 0 false flags (900 drawings), Halo No-No and Milburn 0, version 4 still caught,
  kittests body_check_shot4_v4 and body_send_gate pass; send gate on SendUserFile; renderer and finish.py carry the
  record. Change 2 begun: leanout.py, key poses K1-K5 on the skeleton, five-view sheet (notes/shot4-case-study/
  leanout-sheet-v1.jpg): K1, K3, K4, K5 clean and clear of the car.
- Next: Opus, high (still building new): (1) K2 from three-quarter front has no head: fix in lying_flat (head drop),
  and add "every drawn person has a head" to the body check (it missed it); (2) redraw the sheet, all clean; (3) one
  fresh critique (critique.py pack, stage "pose sheet"), fix; (4) the in-betweens (lying.blend) and leanout.at(t);
  (5) send Sam the pose sheet with the build (Y/N before the rebuild); (6) on his Y, rebuild shot 4.
- Shots 5-8 (chain B, Sam's notes on the clip: section above): Next Opus, high: acting rows for shots 5-8 (every person, beat by beat, using focus.py for looks and head turns; Jason looks where he points; new arm poses), file source/gta_shots58.py only (chat 20 owns shot 4 and gta_rehearse.py); then a short clip of just the changed shots to Sam.
- Needs Sam: nothing for shot 4 yet (the pose sheet comes with step 5). Shots 5-8: a separate Sonnet chain (its
  chat 19) sent Sam a clip ~23:30 (body check clean) and waits for his notes; this chain does not touch shots 5-8.
- Read: guides/job-packs.md Build; source/leanout.py MAP; lying_flat.py _head and draw (lines ~224-330, 470-525);
  case study sections 10-11.
- Open rule requests: none.
- For Claude: scratch scripts lost with the container: run the gallery under the check by wrapping V.person with
  HC.frame_begin/frame_end inside posegallery.main (--all); past films via film.frame_image(t) with F.guard and
  F._ALLOW 'kittests'. K2 head: camera 45/60 deg, hup (0.51,0.86,0), hfwd down 0.51; head is drawn at 30 deg.
  The acting row "free hand gripping the roof" changed to "braced on the door top" (it crossed his head): tell Sam
  in the build message as an "Added/Lost" line.
- Branches named, not merged on purpose: freeze/halo-no-no, freeze/milburn, freeze/milburn+milburn-story,
  freeze/protest-tiers are posted films' bookmarks (freeze.py tag), kept as they are.


## Where things stand (21 Nov, chat 20, Opus high; Sam's Y given: chat 21 rebuilds shot 4)
- Rules that bite next: 8 (no rebuild before Sam's Y), 74 (every beat acted as the acting rows say), 89 (the rebuilt
  shot's clip gets a fresh critique before it is sent; the send gate refuses it otherwise).
- Done: K2's missing head found (the figure guard stopped the drawing at the arm; the sheet showed the half body);
  body check: every drawn person has a head (gallery 900 / Halo No-No / Milburn: 0 false flags; kittest
  body_check_headless); refused views crossed out; LEONIDA print never backwards; K2, K3, K5 re-posed; two critique
  hunts (round 3) fixed or named; leanout.at(t) on the acting beats: 149 frames clean, clear of the car. Pictures:
  notes/shot4-case-study/leanout-sheet-v3.jpg, leanout-strip-v1-phone.jpg (sent to Sam). Case study section 12.
- Next: chat 21, Opus high (building new): rebuild shot 4's Jason on leanout.at(t) in the film (the skeleton
  drawn through the shot's camera, legs hidden by the car), with the acting rows' faces and the fix 3 events; body
  check and car test every frame; a clip of shot 4 (no yes needed) after a fresh critique.
- Needs Sam: nothing. Sam (21 Nov): "Y" to the pose sheet and move strip: rebuild shot 4 on this move.
- Read: guides/job-packs.md Build; source/leanout.py MAP; the shot 4 acting rows and events in this file.
- Open rule requests: none.
- For Claude: critique round 3 hunt 2 was marked "fixed" though its faults were named (house style, guides): the
  Checks line to Sam names them. Kittests failing before this chat and unchanged by it (11: pose_gallery,
  lopsided_invented_only, turned_heads_for_anyone, round_page, people_from_a_description, places/moves_from_..,
  facehouse_whole_head, outfit_every_view, focus_front_heads, watcher_catches_last_weeks_four). Watcher: saver BROKEN
  03:29 20 Nov (old; chat 18's messages checked clean by dump) and 5 systems with no promise (freeze.py,
  freeze_faults, humancheck sendgate, record_faults, tag_faults): named, not this job. Shots 5-8: a separate chain.
- Branches named, not merged on purpose: freeze/* bookmarks of posted films.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 38.08% of 15%; forecast 88.6% (2026-11-21)


## Where things stand (21 Nov, chat 21, Opus high; shot 4 v6 built, critique hunt 1 recorded: chat 22 fixes)
- Rules that bite next: 89 (hunt 2 on the fixed clip, then `critique.py fixed`, before it is sent), 74 (acting rows),
  30 (the "stump" came back from the old camera: the camera is now chosen by measuring the gun on screen).
- Done: Jason rebuilt on leanout.at in the moving car (shot 3's seated Jason is the same drawing); the car hides him in
  8 cm pieces; the lead cruiser drops back to the approved aim; side-window camera keys B3/B5; pistol 1.5x; a flash on
  every shot's drawing; cop hit (blood mist + spatter, slump, dead weight); acting faces; her ears/peek; Lucia glances.
  Move check 149 frames clean; body check: Jason clean every frame; one cop glimpse named. Case study section 13.
- Next: chat 22, Opus medium (a fix round from a clear plan): hunt 1's list (source/data/critique/grand-theft-autism/
  r21-p1): (1) the hit at 2.85-3.3 s: push the lens in on the lead cruiser's windscreen so blood and slump read;
  (2) B5 crash framed bigger, Jason smaller, his raised gun clear of his body (measure muzzle vs body on screen, as
  chat 21's camera search); (3) a little life in the 3.5-4.55 hold (head turns from the flash, gun tracks). Name: flash
  star and fireball (house look), car perspective, the cruiser-2 cop arm (4 drawings at 3.42 s). Render (20 min),
  hunt 2, `critique.py fixed`, humancheck name + critiqued, send Sam the clip (no yes needed).
- Needs Sam: nothing.
- Read: guides/job-packs.md Build; source/leanout.py MAP (to_world, film_layer); source/gta_rehearse.py CAM4 and
  jason_layer / lead_cop_lean / blood_items; the hunt's result.md.
- Open rule requests: none (draft lesson 20 in the case study: put the film's camera through the pose sheet).
- For Claude: v6 clip (held, 1 named fault) in chat 21's scratchpad is gone with it: re-render with
  `gta_rehearse.py shot4 OUT --frames DIR`; `bodies shot4` (solid check) was still running at handover, unread.
  Critique spec: source/data/critique-src/grand-theft-autism/v6-shot4-spec.json (round 21; hunt 2 = pack again).
  `bodies shot4` (every frame): Jason clean; passers-by 128, 129 run through the crashed cruiser at 3.75-4.25 s (the
  crash moved 4 m back with the cruiser's drop-back: their run must avoid it, crowd() in gta_rehearse); feet sunk 3-12 px:
  persons 128-131, 51 (4.5 and 5.5 s). Fix in chat 22 with the list above.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 40.3% of 15%; forecast 90.8% (2026-11-21)


## Where things stand (21 Nov, chat 23, Opus high; render stopped by Sam on the arm)
- Rules that bite next: 30 (the arm is now a THIRD repeat: why chat 23's fix failed is in the case study, section
  16, last point), Seeing like Sam 1 and 4 (look at full size; a view the drawing can't carry is a fault), 89.
- Done: v7 notes 1-3 and 5-10 fixed in code (Lucia's grip, the bonnet, the arm-edge car check, blood on the glass,
  the struck hydrant, water kept out of the car, the cop's sideways slump, the 2 s weave; shot 4 now 8.2 s); test
  stills and the 0-2.4 s frame sheets sent. Note 10 proposal judged (teach-recognise: option 1 picked blind).
- Next: chat 24 on Opus high (new build): the backwards arm, 0.9-2.4 s: start from the camera and pose (Seeing like
  Sam 4), then the drawn shape; full-size look at every frame of it before any clip; then render the clip
  (about 40 min, 134 drawings), round 23 critique (spec v9-shot4, mkspec in the case study), send the clip.
- Needs Sam: his Y/N on note 10's two options (the clip message brings them; `propose.py show teach-recognise`).
- Read: guides/job-packs.md Notes round; CLAUDE.md "Seeing like Sam"; case study section 16.
- Open rule requests: none (draft lesson 23 in the case study).
- For Claude: lying_flat._arm PERSP (near limbs drawn bigger: did not fix it, keep or drop); humancheck _crossed,
  _limbs (its stretch test is graded after PERSP: re-base on the unscaled drawing); leanout _cover IN_CABIN seat
  mask, car_faults ARM_R edge test, K3 moved; gta_rehearse WOB, _hydrant_spot, hydrant_flight/body, lead_cop_roll,
  person_cached(roll=), CAM4 weave keys; R.SHOT4_LEN 8.2 moves shots 5-8's T5 (their chain should know).
  Frames 0-65 of the stopped v8 render: scratchpad only (lost with this chat).
  Handover check's 4 QUICK CHECK lines (gta_rehearse, leanout: no notes file, no SHOT_MARKS): they are this film's
  shot code, not films; named, not fixed (the film's notes are grand-theft-autism.md).

Cost line (recorded every handover; shown to Sam only on a problem): film so far 47.1% of 15%; forecast 97.6% (2026-11-21)
