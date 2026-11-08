# Where the project stands

Read only the section you need (`grep -n '^## ' story/status.md`). Finished films and their history:
`story/archive.md`; their notes: `notes/archive/`.

## TikTok results (3 Nov)
- 26 films, 92K views, 177 followers (+65% since 18 Oct). Typical film last week 5,900 views (earlier weeks 700-1,400).
- Numbers: `story/metrics.md`; reading and benchmarks: `story/growth-analysis-3-nov.md`; chart: `story/charts/account-overview.png`
  (redraw: edit `source/metrics_data.py`, run `python3 source/metrics_chart.py`). The "Hook Text names the story" rule: dropped (Sam, 7 Nov).

## Films
- **Next jobs (7 Nov, handover in `notes/next-jobs.md`):** (1) sitting-animation kit: part 1 built 8 Nov (`source/sitting.py`, `notes/sitting-kit.md`; rule 80), sent to Sam; part 2 next (Opus, high); (2) forearm-and-elbow check for rule 78 (Opus, medium), straight after (1). Rules 74, 78, 79 written 7 Nov; the touch check now says COULD NOT TEST.
- **Ad-Vanced Notice (7 Nov): place photos filed, composition sheet sent.** Cast approved; 15 place photos with
  9-10 things each. Next: Sam's yes, then build the sets (Opus high). Waiting on Sam: the rest of the script. Notes: `notes/ad-vanced-notice.md`.
- **Islamocommunism (5 Nov): FINAL sent** (`animations/islamocommunism-vertical.mp4`, 73 s, 7.8 MB). Week 100%. Open rule requests in `notes/islamocommunism.md`.
- **MidTerminal (4 Nov): done.** Final `animations/midterminal-vertical.mp4` (57.4 s, 10.5 MB) and story post `animations/midterminal-story.png`. Cost 11% of a week (Sam: the old norm was 15-25%; always aim lower). Rules 70-75 and P8-P10 written (Sam's yes). Built (4 Nov): finish.py burns in the subtitles (rule 70) and reads the film's HOOK, checking it first (rule 75): `finish.py CLEAN OUT --film NAME`. Notes: `notes/midterminal.md`.
- **Terfwarts (3 Nov): final sent** (`animations/terfwarts-vertical.mp4`, 89 s, 11.8 MB), for Sam's 5 pm post. Cost 9% of a week (58% to 67%): under the 19% estimate and the 10% target.
  Open: his two rule requests (Hook Text and sign-off in every animatic; no three-quarter views): propose wording, wait for his yes. Notes: `notes/terfwarts.md`.

## System audit (2 Nov)
- Sam's audit of the whole system: done (A1-A14, M1-M7; A7, the doubled checks, needed no change: on a closer look they never run together on one film). The rulebook is now one file,
  `guides/film-quality-rules.md`; CLAUDE.md is shorter; old guides are in `guides/archive/`; Yuletide has its own
  folder; the films' notes are in `notes/archive/`.

## Yuletide (a separate experiment, not finished; `guides/yuletide/`)
- Next time: start from the newest engine (`guides/yuletide/yuletide-trailer.md`, "When we next work on Yuletide").
- Done (October): the animation test (`animations/yuletide-animation-test.mp4`), the look book, the tone guide, the
  premise and title cards (`story/yuletide.md`), hair simulation (not yet in a finished shot).
- Open (October):
  - **FIRST: the mother's right wrist is bent unnaturally in almost every chop** (director's note). Measured
    over every drawing: Shot 1 bends 30-45 deg up/down all the time and sits at the 25 deg sideways limit in
    14 of 32 drawings (every impact and the rest after); Shot 2 35-50 deg; Shot 3 50 deg at the start, fine
    (10 deg) only in the raised hold, where the blade was allowed to tip and turn with her arm
    (`raised_cleaver` in `s3_closeup.py`). A natural chop keeps the wrist within about 20 deg (more only when
    cocked back at the top of a lift) and never at its sideways limit.
    Cause: every recipe fixes the cleaver's angle and the hand's grip on the handle, so the wrist takes up
    all the difference. Fix: in every frame, turn the cleaver (tilt about its edge, pitch, turn about the
    vertical) to suit her forearm so the wrist stays near straight, keeping the edge square across the ham at
    each impact so the slices stay clean; tighten `checks.py` to about 30 deg up/down and 15 deg sideways for
    the chopping hand. Then re-render Shots 1-3 (animatic first) and rebuild
    `animations/yuletide-animation-test.mp4`.
  - The girl's neckline reads as a square neck (after trimming her head piece so her shoulder skin no longer
    shows through her top and hair); a round crew collar band would be nicer.
  - A check in `checks.py` for skin poking through clothes (a first attempt could not tell it from the
    throat above a collar).
  - Speeding up the hair grid build (~90 s per drawing).
  - The parting at the mother's crown reads as a squared-off patch, and a faint bright line runs along her
    hairline, when the camera looks down on her hair.
  - Next (director): lock a full trailer shot list timed to the finished score
    (`music/horror-trailer-score.m4a`) before building more.

## Working within the budget (Sam's Claude plan)
- The plan is charged for Claude's work, not render time: short chats, one stage each, few pictures.
- Render in the background and report once at the end.
