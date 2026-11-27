# Notes for patriots5 (The Patriot 5) (one file, numbered; mark each done as it is fixed)

> **Held for the next film (Sam, 16 Nov), raise at the plan, then delete this note from the template:** the estimates
> proposal (`notes/proposals/estimates.md`, options 1 and 2). Sam: use this film as the learning apparatus for budget
> and costliness; no price tests or measures on European Protests or Blessed (too mixed with other work). Put it to
> Sam again in the plan's questions, without the past-film measuring step, before `ledger.py estimate`.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/patriots5-handovers.md)
- **Rules that bite next:** 89 (critique before the cast sheet goes back), 30 (a repeat note: find why the first fix failed), 24 (the estimate, once the screenplay is in).
- **Done (chat 1, 27 Nov):** the Patriot on the new house head (made by hand, no photos: references/faces/patriot/pick) under a new house balaclava (facehouse_d, every turn); his Patriots 3 clothes kept; kit test balaclava_every_view (fails on the first sheet's missing three-quarter eye opening); sheet v1 sent; notes 1 and 3 fixed, sheet v2 sent; note 2 answered.
- **Check not built yet (note 1):** a check that finds stray ink lines inside a jacket's fill; needs a way to tell the drawing's own seams (zip, hem) from stray ones. Until then: every body looked at full size before a sheet goes.
- **Spent against the estimate:** no estimate yet (Sam is still writing the screenplay).
- **Next:** Sam's notes on the Patriot's sheet (Opus, medium); then, when Sam gives the screenplay and title, the plan (Opus, high): kitfilm.py begin patriots5.
- **Needs Sam:** Y or N on the shoulder-seam fix (note 2); his look at sheet v2.
- **Read:** guides/job-packs.md Notes round (for sheet notes), Plan (when the screenplay comes).
- **Lost / Added:** Lost: his old big cartoon eyes and boxy head. Added: house eyes and brows, a rounded knit hood fitted to the head, the knit moving over the mouth.
- **Open rule requests:** none.
- **Locked by Sam:** nothing yet (no shots); the Patriot's clothes, badges and poppy are as Sam approved them in Patriots 3.
- **For Claude:** `python3 source/patriots5_cast.py sheet OUT.jpg`; person: patriots5_cast.patriot(mood), draw(); balaclava: facehouse_d (balaclava_front/turned), turned via _turn_hair, ears hidden; `neck_c` (shared): a covered neck's colour in body.plain_torso, views_c, turnhead.neck_over. Open Wounds (brexit-is-done) posted 27 Nov; its notes file stays in place because acting.py reads its acting list (move to shared: repoint that, then archive it). Branches named at start, not merged (logs and old GTA drafts only, nothing for this film): claude/jolly-ramanujan-2lcl2o, claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31.

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Every person, set, prop, pose and move in the brief gets a row: KNOWN (its kit-catalogue line, pose-gallery row or
"Passed the critique" row: almost free) or NEW (priced; drawn alone and critiqued before the cast sheet, rule 89).

First line: how much of the total is unmeasured. Each cost is the nearest measured past cost in `notes/ledger/`
(name the film and row), or 'unmeasured'; no padding, no multipliers. Each row names its stage (cast, sets, board, moves,
animatic1, round, final; board: the shot board of rule 11, ended by `rough.py sent FILM OUT.jpg --delivered --board`; one 'round' row per notes round, priced from past films' real rounds); the stage totals go
into `ledger.py estimate FILM PCT --stages "cast 2, sets 2.5, ..."` and each stage's end runs `ledger.py stage FILM NAME`.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py FILM sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py FILM OUT.jpg`)

Rehearsal clips sent: (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Shot board sent: (rule 11: every shot on one board before any move is written: `rough.py board FILM OUT.jpg`, send
it, then `rough.py sent FILM OUT.jpg --delivered --board`, which records it. Pre-flight refuses to run until the record
holds every shot, each with someone in SHOT_CAST, sent before the first move; and while any "done?" box below is blank:
rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 | Sam, 27 Nov: "run The Patriot character through our new drawing style to bring him up to speed" | sheet sent, awaiting Sam |
| 2 | Sam, 27 Nov: "Start a new film file/ledger for The Patriot 5. I am still writing the screenplay." | yes |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
|   |      |      |

## Exceptions (rule 13): anyone or anything left out of a check, one row each (a pattern like Journalist* is fine); pre-flight refuses a film setting's exception (HANDS_OK, LINE_OK, any *_OK, ALLOWED_POPS) with no row here; a code comment is never a reason. check: the setting's name, or 'house look', 'lap', 'drawing checks', 'camera feel' (who: the shot)
| check | who | why | looked at full size (sheet, panel) |
|---|---|---|---|

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

Status: one line of what was done (no "Was:"; git keeps the history), "new kind" or "seen before" (a "seen
before" note means a check is missing: add it), and the note's line in `guides/critique-checklist.md` (rule 30):
a new line's id, or an old one and why it missed (line unclear, sheet didn't show it, no critique).
"Should have caught": the check that should have caught the note before Sam saw it (its name as pre-flight prints
it, e.g. AUDIT, SHOT CAST, caption), or "none" when no check could; the handover check refuses a blank one
(check-catches change 2, Sam's Y 20 Nov), so misses are counted without guessing.
"Critique saw it?": yes if the fresh-eye critique of that round had already flagged it, no if it looked and missed
it, "no critique" if none ran (Sam's Y, 26 Nov): after a few films it shows whether the critique sees what Sam sees;
the handover check refuses a blank one.

| # | shot | time | note | line | should have caught | critique saw it? | status |
|---|------|------|------|------|--------------------|------------------|--------|
| 1 | cast sheet | front | "strange vertical lines in the belly area" | new | none: I looked at the sheet at phone size only, not each body at full size (Seeing like Sam, 1); no check sees pieces drawn for an old body landing inside a new one | no critique | fixed: Patriots 3's belly-swell edges no longer drawn; the shared body has a 'stout' build (belly in its own outline, side and three-quarter too) |
| 2 | cast sheet | back, 3/4 back | "explain the greying out of the sleeves? You did that with Blair too" | seen before (Blair) | none: the shoulder join (limbs.py, the arm fading into the body near the shoulder) assumes the sleeve is the jacket's cloth; a grey sleeve on a black body fades as a smear | no critique | answered; fix waits for Sam's Y (a hard shoulder seam where the sleeve's colour differs from the body's) |
| 3 | cast sheet | side, three-quarter | "Fix your notes": my named faults (collar a box beside the neck with a zip in the air; the chin's dark V) | new | none (I named them myself, unfixed) | no critique | fixed: the knit's neck stops at the collar so the collar wraps round it; zip and hem fitted to the stout body; ribs stop above the chin's bottom rings |

Decisions made (kept so a long session or a new session never has to rediscover them):
- The Patriot's face under the knit is made by hand (no photos: he is fictional), the average face pushed thick-set; only his eyes and brows show, in the house look (as May and Kemi).
- Kind: character update (no film shots yet).
