# Job packs: what each stage reads (Job J, 10 Nov; Sam: Y)

Three layers of reading. **1. The core** (CLAUDE.md, loaded by itself). **2. One pack below**, for the stage the
handover names: only the sections it lists (`grep -n '^## ' FILE`, then read those lines). **3. Look-ups**: a rule
by number (`grep -n '^| 41 ' guides/film-quality-rules.md`), a kit piece by name (`grep -n -i NAME
guides/kit-catalogue.md`), only when a note or a fault names it. The whole rulebook, satire.md or the catalogue is
never read end to end in a film chat. Each pack's "Bite" rules are the ones its stage breaks most.

## Plan (Opus, high): the brief, staging, questions, the estimate
- Read: `guides/preflight.md` Stage 1-2; `guides/satire.md` Start, Getting it right first time, The acting list;
  `guides/tiktok-design.md` Hook Text; the film's notes from `notes/_template.md`.
- Only when a shot has a mass crowd, a big vista or wide action: `research/crowds-and-big-action.md` "The lessons"
  (guidelines, not rules; Sam, 13 Nov).
- Known or new: every person, set, prop, pose and move in the brief goes in the estimate table as KNOWN (a
  `guides/kit-catalogue.md` line, a `guides/pose-gallery.md` row, a "Passed the critique" row) or NEW (priced, drawn
  alone and critiqued before the cast sheet, rule 89). Known is almost free; the estimate is the new rows.
- Estimate costs come from the ledgers' real costs per thing and per round (`notes/ledger/`), no padding, no
  multipliers; the plan's stages go in with `ledger.py estimate FILM PCT --stages`, and each stage's end runs
  `ledger.py stage FILM NAME`, whose forecast line opens that reply (rule 24).
- Bite: 24, 74, 1, 38, 8, 11. Tools: `ledger.py estimate`, `plan.py`, `catalogue.py`, `rough.py board` (then `sent --board`).
- Moved from CLAUDE.md word for word (startup fixes 4, 16 Nov): **Reference photos and reporting (full network access since 12 Nov):** I send 2-3 when I have them; otherwise search
  once, slowly, 3 per place at most: **news pages and press photo galleries first** (Al Jazeera galleries, AP, Reuters,
  euronews, dpa, local papers), free libraries (Wikimedia, Geograph, Openverse, Pexels, Unsplash) only when the news
  has nothing. **One failed try per source, then stop** and give me one numbered list of what to find, which angle and
  why.

## Build (Opus, high for new things; medium from a clear plan)
- Read: `guides/figure-rig.md` 2-4, 5c (people); `guides/satire.md` Movement, One set one plan; `guides/pose-gallery.md`
  only the rows the film uses; `guides/critique-checklist.md` (what the critique will ask).
- Bite: 41, 89, 3, 28, 61, 83. Tools: `critique.py pack/record`, `posegallery.py`, `compare.py`, `codemap.py`.
- Critique: ONE pack per stage (`"stage"` in the spec), two hunts, then `critique.py fixed`; a third is refused.
  A Glimpse (rule 24) is the exception to "drawn alone": one view, one pose, no sheet of its own; its panel is its
  shot's frame at phone size plus one 2x crop, marked `"glimpse": true`.
- At the end: each new thing that passed the critique gets a row in the catalogue's "Passed the critique".

## Notes round (Opus, medium): Sam's notes, fixes, clips
- Read: the notes printout `handover.py start --film` gives (Where things stand and the unticked notes; startup-fixes 3), not the file; then, for each note, ONE look at the code:
  `python3 source/page.py FILM show "note words"` (~40 numbered lines of the functions it touches). No greps or sed
  ranges on film files first; only if `show` misses, `page.py FILM find` or a second `show` in the thing's own words.
- Bite: 30, 87, 89 (with 56, 76, 79 in it), 88. Tools: `critique.py where/before`, `final OUT --small --span T0 T1`.
- A note about framing or staging (where people are, the camera, what is in frame): `staging.py restage FILM SHOTS
  --note N "words"`, then 2-3 numbered framings (`staging.py options`, one the script's camera line), Sam's number
  (`staging.py pick`), the shot as built on the board (`rough.py board FILM OUT.jpg --shots S`); a clip of that shot
  is refused until then (lesson staging-stills; a wrongly flagged note: `staging.py notframing FILM N "why"`).

## Checks and animatic (Sonnet): pre-flight, check sheet, render, send
- Read: `guides/satire.md` Before every render, Render, If a check fails; `guides/preflight.md` Stage 3.
- Bite: 59, 67, 14, 89 (the critique gate), 75. Tools: `preflight.py NAME OUT --text`, then in full; `finish.py`.
- The sign-off, moved from CLAUDE.md word for word (startup fixes 4, 16 Nov): **Every video
  ends with the CranbriJoos sign-off** (the beaver sipping from the carton, my slurp, 1.6 s): `python3
  source/finish.py CLEAN.mp4 animations/NAME-vertical.mp4 --film NAME` (or `["Hook Text"]` for a film with no
  `HOOK`), from the clean render in `source/data/`.

## Final and posting (Sonnet)
- Read: `guides/tiktok-design.md` The video file, Sign-off, Posting; `guides/preflight.md` Stage 5.
- Bite: 70, 75, 52, 47, 37. Tools: `finish.py CLEAN OUT --film NAME`, `ledger.py log/audit`.
- The day a film is posted: add it to `source/data/freeze/films.json`, then `python3 source/freeze.py tag --push` (its bookmark
  at the save its final video came from). The handover check refuses a video in `animations/` that no film lists.

### My accounts (Sam, 26 Oct)
(Moved from CLAUDE.md word for word, startup fixes 4, 16 Nov.)
- Channel and brand name on every platform: **CranbriJoos**. TikTok (main platform): `www.tiktok.com/@cranbrijoos`.
- YouTube Shorts is the second platform: same name and profile picture (`profile/cranbrijoos-tiktok-1080-eyes-open.png`,
  the beaver's face); every Short's description and pinned comment points back to the TikTok link.

## A tool job (Opus, high to design; medium to build)
- Read: the job's own section in `notes/next-jobs.md`; the tool's MAP; `source/kittests.py` for its tests.
- Bite: 86, 13, 85. Every tool gets a kittest; its rule's check column names it (on Sam's yes).

## Film types (moved from CLAUDE.md, 10 Nov; the rules unchanged)
- **Satire-style film** (the TikTok series, beyond two people talking): `guides/satire.md`, always starting from
  `source/satire_template.py`, and the rulebook. `guides/best-practice.md` Part 2 only for a scene satire.md doesn't cover.
- **Motion-led films** (stunts, action): a quick animatic early, after the cast sheet.
- **Flat cartoon people:** `guides/figure-rig.md`; follow `guides/preflight.md` from the first brief. Hands are always
  a plain circle with props laid over it.
- **Yuletide horror trailer** (a separate experiment): `guides/yuletide/yuletide-trailer.md`, starting from the newest
  engine. Nothing in `guides/yuletide/` applies to the TikTok films.
