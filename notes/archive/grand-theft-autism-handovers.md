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
