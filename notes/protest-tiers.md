# Notes for protest-tiers (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/FILM-handovers.md)
- **Rules that bite next:** 24, 74, 1 (Plan pack bites)
- **Done:** 12 Nov: Sam's brief saved below word for word. Nothing built yet.
- **Next:** Plan, Opus high (chat 1 of 8): reference search (reporting + photos per event), brief checklist, estimate, staging, questions.
- **Needs Sam:** nothing yet.
- **Read:** guides/job-packs.md "Plan" and "Film types" (satire film); the Islamocommunism film's white headlines (notes/archive/islamocommunism.md, source code for its headline style).
- **Lost / Added:** none
- **Open rule requests:** none
- **For Claude:** film name `protest-tiers`; reuse Islamocommunism's white Country/Location headline style; 4 tiers x ~4 s.

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Every person, set, prop, pose and move in the brief gets a row: KNOWN (its kit-catalogue line, pose-gallery row or
"Passed the critique" row: almost free) or NEW (priced; drawn alone and critiqued before the cast sheet, rule 89).

First line: how much of the total is unmeasured. Each cost is the nearest measured past cost in `notes/ledger/`
(name the film and row), or 'unmeasured'; no padding, no multipliers. Each row names its stage (cast, sets, moves,
animatic1, round, final; one 'round' row per notes round, priced from past films' real rounds); the stage totals go
into `ledger.py estimate FILM PCT --stages "cast 2, sets 2.5, ..."` and each stage's end runs `ledger.py stage FILM NAME`.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py FILM sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py FILM OUT.jpg`)

Rehearsal clips sent: (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Composition sheet sent: (rule 11: the 3-4 key shots, before building; write the date and file here once Sam has it.
Pre-flight refuses to run until this line has them, and while any "done?" box below is blank: rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 |      |      |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
|   |      |      |

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

Status: one line of what was done (no "Was:"; git keeps the history), "new kind" or "seen before" (a "seen
before" note means a check is missing: add it), and the note's line in `guides/critique-checklist.md` (rule 30):
a new line's id, or an old one and why it missed (line unclear, sheet didn't show it, no critique).

| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 1 |      |      |      |      | open   |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 


## Sam's brief (12 Nov, word for word)

Create a short film in satire style about these four European protests. Each one has an increasing tier of scene severity based on actual reporting. Give them the white headlines from Islamocommunism with Country and underneath Location. Consider each tier a rising showstopper, with tier 1 being a quarter of one and tier 4 being the whole showstopper. Find reporting and photos on each event for references

Tier 1, Spain (lowest): Paseo de Gracia, dusk, wide.
* Crowd: a huge, calm march fills the avenue to the vanishing point. Raised key rings glint above the heads (a real detail from the strike, a symbol of housing), with union flags and placards from different cities.
* Contact: a thin police line crosses the far end. A small knot of hooded figures stands in front of the crowd, beside one burning container.
* 0.0-1.5 s: the crowd sways forward and the keys rise like a wave. A hooded figure at the front flicks a string of fireworks toward the line.
* 1.5-3.0 s: three small bursts pop over the line and the crowd's heads turn.
* 3.0-4.0 s: the line steps one pace forward, and a thin pepper-spray haze drifts through the keys.

Tier 2, Germany: Frankfurt gun store, night. Locked camera.
Frame: the gun store sits centre-left, with a steel shutter half raised over a large glass front. The street is wet and shows reflections. A crowd of young protesters fills the right half and the mid-ground behind the store, holding signs (a "Gen Z regelt" banner among them) with a few phone lights. The far end of the street, frame right, is dark.
* 0.0-1.5 s (the rush and smash): eight hooded figures sprint in from frame left across the foreground. Two haul the shutter up with a pry bar, and a third swings a hammer into the glass. The sheet collapses and shards sparkle in the streetlight. Two figures slide through the gap, and a sign is kicked to the ground as the others hit the frame.
* 1.5-3.0 s (the chanting crowd): the smashing continues at the store while the crowd behind it chants. Signs jab up and down in rhythm, mouths are open, and phone lights wave. The crowd stays on the pavement, facing the store, with the break-in in front of them.
* 3.0-4.0 s (the police arrive): blue light and sirens appear at the far right end of the street and sweep across the crowd and the store front. Faces, signs and wet ground turn blue. The group at the store freezes mid-swing, and the crowd holds its signs up in the glare as the final frame.
VFX: a hammer impact flash, a falling glass sheet with glints, phone lights, a moving blue strobe wash with reflections on the wet street, and a siren sound cue. Three light layers, with the blue wash arriving last so it lights everything at once.

Tier 3, Paris (real top): Place de la République, low angle.
* Crowd: a vast crowd fills the square in yellow vests and tricolour flags. Union banners hang across the back, and Marianne stands above, graffiti on her base.
* Contact: a black-clad front line faces two police rows, with a burning car foreground-left and burning bicycles mid-right.
* 0.0-1.0 s: smoke rises from the car and the bicycles, and the crowd surges forward behind the front line.
* 1.0-2.5 s: the front line throws paving stones in arcs. A tear gas canister lands among them and white gas swallows Marianne's lower half.
* 2.5-4.0 s: a water cannon sweeps in low from the right. The crowd breaks into two currents, scattering out left while the vests hold at the back.

Tier 4, Albania (artificially placed top): Tirana avenue, dusk.
* Frame: a wide avenue under a burning sky. A bank sits on the left, the blazing Education Ministry at centre-right, and a police helicopter hangs high at upper right. A shield line runs across the mid-right, with a vast, furious crowd filling the avenue behind the rioters. Zones: sky for the helicopter and rocket, foreground for the mopeds, mid-ground for the melee, left buildings for the Molotovs.
* 0.0-1.0 s: two mopeds with masked riders race in from foreground left. The lead passenger shoulders an RPG and fires, and the rocket's smoke trail climbs diagonally toward the helicopter. The crowd surges behind them.
* 1.0-2.0 s: the rocket hits and the helicopter spins out of the sky, trailing fire, falling behind the ministry. The crowd slams into the shield line and the shields buckle.
* 2.0-3.0 s: the line breaks. Rioters swarm over the shields in furious melee, batons swinging, and officers are driven back. Two Molotovs arc from the crowd into the bank's ground-floor windows, and the glass blooms orange.
* 3.0-4.0 s: a fireball from the wreck rises behind the ministry and backlights the melee. Tear gas, flares and a toppled water cannon truck burning at the line's end hold the final frame.
VFX: rocket smoke trail, helicopter spiral with a fire trail, a fireball, shield-line impact flashes, melee dust, Molotov window bursts and ground fog. The violence stays stylised, with no gore.
