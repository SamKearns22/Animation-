# Rule register: every rule and the check that holds it (Sam, 25 Oct)

A rule only holds if a check enforces it. Each row names the rule, where it is written, where it came from, and its
check: a tool that pre-flight runs, "to build" (the tool is on the Build list in `story/status.md`; do it by hand and
say so), or "by hand" (ticked on the check sheet before every animatic). When Sam asks for a rule, it gets a row here
in the same chat (CLAUDE.md, "Rules are permanent"). Started 25 Oct with the Prepper Minister review and an audit of
every film's notes; older rules in `guides/satire.md` are added as they come up.

| # | rule (short) | written in | from | check |
|---|---|---|---|---|
| Q1 | One plan of the world in metres | film-quality-rules 1 | Power Crime | to build (plan template) |
| Q2 | Doorways show the real next room | film-quality-rules 2 | Power Crime | to build (portal) |
| Q3 | Reference benchmark sheet before building a place | film-quality-rules 3 | Power Crime | to build (benchmark sheet); by hand |
| Q4 | Every set has layers and life | film-quality-rules 4 | Power Crime | by hand |
| Q5 | Automatic collision test | film-quality-rules 5 | Power Crime | `audit.py` |
| Q6 | Automatic pop-in test | film-quality-rules 6 | Power Crime | `audit.py` |
| Q7 | Script and mouth audit | film-quality-rules 7 | Power Crime | `voices.py --film` |
| Q8 | Rehearse risky moves as clips | film-quality-rules 8 | Power Crime | by hand |
| Q9 | Every group has a plan for every phase | film-quality-rules 9 | Power Crime | by hand |
| Q10 | Framing planned, Hook Text area, hold times | film-quality-rules 10 | Power Crime | `hookcheck.py`; by hand |
| Q11 | Composition sheet before building | film-quality-rules 11 | Power Crime | to build (pre-flight stop, Q14) |
| Q12 | Checks run on everything by default | film-quality-rules 12 | Prepper note 47 | to build |
| Q13 | Every check in the shared kit | film-quality-rules 13 | Prepper note 60 | to build |
| Q14 | Pre-flight refuses blanks in the brief checklist, or no composition sheet | film-quality-rules 14 | Prepper | to build |
| Q15 | Effect shapes checked (no stars) | film-quality-rules 15 | Prepper note 20 | to build |
| Q16 | Direction holds across a cut | film-quality-rules 16 | Prepper note 57 | to build |
| Q17 | Every figure in front of an effect hides it | film-quality-rules 17 | Prepper note 13 | to build |
| Q18 | Readability sheet at phone size | film-quality-rules 18 | Prepper notes 2, 27, 41, 46 | to build |
| Q19 | Checks print a short summary | film-quality-rules 19 | Prepper review | to build |
| Q20 | Held things aim in 3D with the body | film-quality-rules 20 | Prepper notes 11, 16, 45, 48 | to build (prop test through every view); `prepper.facing_check` meanwhile |
| Q21 | Limbs at the lens foreshortened | film-quality-rules 21 | Prepper note 42 | by hand |
| Q22 | My set dressing shown, clear of action, in the audit | film-quality-rules 22 | Prepper note 19 | `audit.py` (once Q12); by hand |
| Q23 | Film file over ~1,000 lines split per shot group | film-quality-rules 23 | Prepper review | by hand |
| Q24 | Ambition estimate at planning | film-quality-rules 24 | Prepper review | by hand |
| Q25 | Eyelines and holds per shot | film-quality-rules 25 | Prepper notes 21, 59, 61 | `LOOKS_AT` eyelines; holds by hand |
| Q26 | Every sound effect listed at planning | film-quality-rules 26 | Prepper | by hand |
| Q27 | Bleep: said or gap? placed from the sound | film-quality-rules 27; satire.md Start | Prepper notes 33, 54 | by hand |
| Q28 | Reuse first; catalogue updated | film-quality-rules 28; kit-catalogue.md | Prepper review | by hand |
| Q29 | Film time and shot number on every review copy | film-quality-rules 29 | Prepper review | to build |
| Q30 | Notes table short; "seen before" means a missing check | film-quality-rules 30 | Prepper review | by hand |
| Q31 | Clips and routine work on Sonnet | film-quality-rules 31; CLAUDE.md | Prepper review | by hand |
| S1 | People react before a hit lands | satire.md Staging | Poker Mon note 37 | by hand |
| S2 | Hand moves the object; hand drawn over it; resting hand 3 cm clear | satire.md One set | Poker Mon notes 25, 62 | `poker_mon.contact_check`, `hands_check`, `clearance_check` (copy; move to kit: Q13) |
| S3 | No added room tone | satire.md Sound | The Traitors | by hand |
| S4 | ffmpeg joins at fps=24 | satire.md Render | Strictly Crabs | by hand |
| S5 | Pupils cut to the eye's outline | figure-rig.md | Poker Mon note 77 | built into `burnham.face` |
| S6 | Hips 15% narrower; hem rises gradually on a lean | figure-rig.md section 2 | Power Crime notes 5, 46 | built into `burnham.HEM`, `views.py` |
| S7 | No off-style shorthand (stars, sweat drops, motion lines) | satire.md The look | 16 Oct | to build (Q15) |
| S8 | Bullet holes and marks only on real surfaces | satire.md Staging (marks) | Prepper note 18 | `prepper.marks_check` (move to kit: Q13) |
| S9 | One sound per hit, only when it is in frame | film-quality-rules 13 | Prepper note 23 | `prepper.crockery_check` (move to kit: Q13) |
| P1 | "I want a rule" = permanent, written the same chat | CLAUDE.md | Sam, 25 Oct | by hand; handover search |
| P2 | "Just go" skips the wait, never the checks | CLAUDE.md | Prepper first animatic | by hand |
| P3 | No animatic with a shot missing its people | CLAUDE.md | Prepper first animatic | to build (Q14) |
| P4 | Unattended runs stop after one animatic | CLAUDE.md | Prepper overnight run | by hand |
| P5 | A repeated note means the first fix failed | CLAUDE.md | Prepper notes 32/41, 33/54 | by hand |
| P6 | One handover section; old ones archived | CLAUDE.md | Prepper review | by hand |

Planned, not built (build only when a film needs it): people lying flat look like paper cut-outs (Poker Mon note 80).
