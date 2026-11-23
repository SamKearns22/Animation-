# Notes for Brexit Is Done (working name) (one file, numbered; mark each done as it is fixed)


## Brief checklist (Sam's words, 23 Nov; tick each against the film before the first animatic)
(Template note, raise at the plan: the estimates proposal, notes/proposals/estimates.md, options 1 and 2.)
News: Theresa May "aghast" at Burnham's EU plans, says "Brexit is done" (BBC, Sunday with Laura Kuenssberg, 22 Nov 2026).
- [ ] 1. Theresa May "in this exact interview" (`references/brexit-is-done/may-interview-*.jpg`): seated, turned to
      screen-left, looking at the interviewer off-frame left; dark wood-panelled backdrop; plum jacket, patterned
      blouse, hands gesturing in front of her.
- [ ] 2. Kemi Badenoch in hard hat and site clothes (`badenoch-hardhat-sam.jpg`: white hard hat, glasses, long braids,
      orange-and-navy hi-vis jacket); faces the same way as May; a construction site behind her (Sam will describe it).
- [ ] 3. Tony Blair as he is today (`blair-today-sam.jpg`: grey swept-back hair, big smile, dark suit, red tie, white
      shirt); ends up facing the same way as May; place not decided ("maybe some swanky embassy sort of place?").
- [ ] Open: the script and the joke (not given yet); the site description; Blair's place.
- Reuse: Badenoch's face is already built (`source/facehouse.py` 'badenoch'); May and Blair are new faces.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Rules that bite next:** 89 (critique before cast sheet), 49 (likeness), 24 (estimate before the build).
- **Done (chat 1, 23 Nov):** May and Blair faces measured (face tool, pick B provisional); new shared hair pieces `bob` (May)
  and `back` (Blair), pearl earrings, a hard hat (front and turned), `specs`, `workwear` hi-vis jacket, own-colour sleeves;
  cast critique hunts 1-2 done; cast sheet v1 sent to Sam (`review/brexit-is-done-cast-v1.jpg`).
- **Open critique faults (named to Sam):** May's age lines faint and full-body reads weakly as a woman; Blair's back/side hair
  a plain cap; a small dark dash on the crown in three-quarter heads (turnhead's seam, also on old swept heads).
- **Next:** Sam's notes on the cast sheet (Opus, medium), then the plan once he sends the script, the site and Blair's place (Opus, high).
- **Needs Sam:** notes on the three faces; the script; the site; Blair's place.
- **Read:** `guides/job-packs.md` Plan; `source/facehouse.py` MAP (hair pieces bob/back, hard_hat).
- **Open rule requests:** none.
- **For Claude:** cast `story/brexit-is-done-people.txt`; `python3 source/people.py sheet brexit-is-done OUT.jpg`;
  `python3 source/facehouse.py turns OUT.jpg may blair`; picks in `references/faces/{may,blair}/pick` ('picked': B, provisional).
  Plan stage not done: no estimate yet (template note: raise the estimates proposal at the plan).

## Handover check, named not fixed (chat 1)
 branches gta-v5-sound-draft, gta-chat46-build, dreamy-fermi-vkhutz,
  gta-chat31 hold only GTA logs/proposals (film posted): not merged, for a tool chat; CLAUDE.md "Locked by Sam" and
  "Just go" sentence alerts and kittest move_to_shared_catches_film_fixes (N26) were red before this chat (checked on
  the saved code); no estimate yet: the plan stage sets it once the script comes. No film code yet (no `page.py show`): only the shared face tool and people kit changed.

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Every person, set, prop, pose and move in the brief gets a row: KNOWN (its kit-catalogue line, pose-gallery row or
"Passed the critique" row: almost free) or NEW (priced; drawn alone and critiqued before the cast sheet, rule 89).

First line: how much of the total is unmeasured. Each cost is the nearest measured past cost in `notes/ledger/`
(name the film and row), or 'unmeasured'; no padding, no multipliers. Each row names its stage (cast, sets, board, moves,
animatic1, round, final; board: the shot board of rule 11, ended by `rough.py sent Brexit Is Done (working name) OUT.jpg --delivered --board`; one 'round' row per notes round, priced from past films' real rounds); the stage totals go
into `ledger.py estimate Brexit Is Done (working name) PCT --stages "cast 2, sets 2.5, ..."` and each stage's end runs `ledger.py stage FILM NAME`.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py Brexit Is Done (working name) sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py Brexit Is Done (working name) OUT.jpg`)

Rehearsal clips sent: (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Shot board sent: (rule 11: every shot on one board before any move is written: `rough.py board Brexit Is Done (working name) OUT.jpg`, send
it, then `rough.py sent Brexit Is Done (working name) OUT.jpg --delivered --board`, which records it. Pre-flight refuses to run until the record
holds every shot, each with someone in SHOT_CAST, sent before the first move; and while any "done?" box below is blank:
rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 |      |      |

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

| # | shot | time | note | line | should have caught | status |
|---|------|------|------|------|--------------------|--------|
| 1 |      |      |      |      |                    | open   |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 
