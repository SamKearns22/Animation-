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
