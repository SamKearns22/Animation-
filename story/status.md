- House look (12 Nov): DONE and ON for every film (rule S7, sign-off included). Chats now open the next chat themselves. Notes: notes/house-look.md.
- System audit (12 Nov): FINISHED, about 3.0% of a week. Report: notes/system-audit-report.md; needs Sam's numbers 1-11.
  The honest checker (branch claude/audit-honest-checker) merges after Blessed's animatic 1 is sent.
- Blessed (12 Nov, notes round 1, chat 3 of 8): phone room (20), TV room (22), zooms (23), front-on clips (26) done and sent. Next: Opus medium chat 4 of 8 (press, Walliams, framing, cell). Needs Sam: nothing. Notes: notes/blessed.md.
remakes: Sam's notes on the final (76 tower boots, 77 wipe entrance) fixed 11 Nov, clip sent; Sam said Y: Sonnet chat re-rendering the final.
Next: Sonnet chat, final render, send to Sam.
Model: Sonnet, medium.
- Budget job (11 Nov, chat 3): built and tested: the critique lists each fault once and refuses a third hunt, the ledger stops a chat at a stage's share, one command redraws-checks-sheets, a colour check; helper kinds timed (none lighter). Next: Fable high, chat 4 (time the light helper, finish the script checks). Handover: notes/budget-job.md.
- Remakes: all fixes in (barrels, wall thump, new caption font); final render under way (Sonnet chat), at 1.1x.
  Tool job (11 Nov rules for every film): built, all six pieces (captions by default, 1.1x in finish.py, Hook Text
  gate, eyes for every cast, set check in the kit, quick.py gone); kittests and remakes check clean. Open: Sam's look
  at the KG eye sheet. Handover: notes/tool-job-universal-handover.md.

- Job M built (11 Nov): estimates split into stages; each stage's end gives "Spent X% of the Y% planned; lands at Z%",
  and the chat stops if the forecast passes the estimate by a quarter. First used on the next film (not Remakes, Sam).
- Open: Sam's look at Job I's 14 and 18.
- Next: Remakes round 2 (above), then Sam's next pick from the job list.

Read only the section you need (`grep -n '^## ' story/status.md`). Finished films and their history:
`story/archive.md`; their notes: `notes/archive/`.

## Hashtags (9 Nov)
- 30 films' views, Hook Text and tags logged (`story/metrics.md`, 9 Nov). Topic and tags don't explain the flops (Jackdaw, Halo, Vance were current; TERFwarts named no news); the first-10-s drop does.
- Hashtag rule written (Sam said Y, 9 Nov): `guides/tiktok-design.md`, Posting.
- Sam, 9 Nov: Claude suggests five tags at every final, only if they are decent (each a real, used search term; say if unchecked). Sam names the news story with each screenplay; record it in the film's brief checklist.

## TikTok results (3 Nov)
- 26 films, 92K views, 177 followers (+65% since 18 Oct). Typical film last week 5,900 views (earlier weeks 700-1,400).
- Numbers: `story/metrics.md`; reading and benchmarks: `story/growth-analysis-3-nov.md`; chart: `story/charts/account-overview.png`
  (redraw: edit `source/metrics_data.py`, run `python3 source/metrics_chart.py`). The "Hook Text names the story" rule: dropped (Sam, 7 Nov).

## Films
Remakes (10 Nov, build chat 11): KG's real talking beak; all pass-3 set faults fixed; options sheet sent in chat. Week at 69% (Sam: over budget): picks set (all A); next chat straight to the shots and the animatic. Handover: notes/remakes.md.
Elder Scrolls: Swindon: FINAL sent 9 Nov (36.6 s, 17.9 MB; Sam skipped animatic 6). Waiting for his notes or posting.
Job H FINISHED 10 Nov (overnight, Sam's "just go"): the critique checklist (37 lines from Sam's past notes) and `source/critique.py`, the fresh-eye critique every film now runs before an animatic (pre-flight refuses without it); calibrated on Elder Swindon.
Job J FINISHED 10 Nov (about 1.5%): rulebook 15 rows shorter, CLAUDE.md shorter, reading packs (`guides/job-packs.md`), hidden props flagged (Job G finished).
Job I lying bodies done 10 Nov (Sam: good); the driver's turned faces in a new chat (Opus high).
Job K FINISHED 11 Nov (two build chats): head acting, hard-edged shading (on), a copy check, check shirts bent round the body, invented people a touch uneven (not on one leg: Sam) (`notes/job-k-ai-tells.md`).
Job L FINISHED 10 Nov (about 1.3%): five by-hand rules now checked in pre-flight (bleeps, subtitle timing, drop to rest before a cut, famous faces, files on GitHub).
Next: Job I faces (new chat); the next film is the critique's first real trial. Handover: notes/next-jobs.md "Where things stand".
- **Next jobs (handover in `notes/next-jobs.md`):** (1) sitting-animation kit: CLOSED 9 Nov (Sam: finished; questions 9-10 kept as built); (2) forearm-and-elbow check for rule 78: built 8 Nov (`kitchecks.rests`; films list resting arms in `RESTS`). Rules 74, 78, 79 written 7 Nov; the touch check now says COULD NOT TEST.
- **Ad-Vanced Notice (9 Nov): FINAL sent and POSTED** (`animations/ad-vanced-notice-vertical.mp4`, 47 s, 8.1 MB). New ending (the man begs, "Ew. God, no."), street scene, line 9 outrage. Notes: `notes/ad-vanced-notice.md`.
- **Islamocommunism (5 Nov): FINAL sent** (`animations/islamocommunism-vertical.mp4`, 73 s, 7.8 MB). Week 100%. Open rule requests in `notes/archive/islamocommunism.md`.
- **MidTerminal (4 Nov): done.** Final `animations/midterminal-vertical.mp4` (57.4 s, 10.5 MB) and story post `animations/midterminal-story.png`. Cost 11% of a week (Sam: the old norm was 15-25%; always aim lower). Rules 70-75 and P8-P10 written (Sam's yes). Built (4 Nov): finish.py burns in the subtitles (rule 70) and reads the film's HOOK, checking it first (rule 75): `finish.py CLEAN OUT --film NAME`. Notes: `notes/archive/midterminal.md`.
- **Terfwarts (3 Nov): final sent** (`animations/terfwarts-vertical.mp4`, 89 s, 11.8 MB), for Sam's 5 pm post. Cost 9% of a week (58% to 67%): under the 19% estimate and the 10% target.
  Open: his two rule requests (Hook Text and sign-off in every animatic; no three-quarter views): propose wording, wait for his yes. Notes: `notes/archive/terfwarts.md`.

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
