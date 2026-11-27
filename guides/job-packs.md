# Job packs: what each stage reads (Job J, 10 Nov; Sam: Y)

Three layers of reading. **1. The core** (CLAUDE.md, loaded by itself). **2. One pack below**, for the stage the
handover names: only the sections it lists (`grep -n '^## ' FILE`, then read those lines). **3. Look-ups**: a rule
by number (`grep -n '^| 41 ' guides/film-quality-rules.md`), a kit piece by name (`grep -n -i NAME
guides/kit-catalogue.md`), only when a note or a fault names it. The whole rulebook, satire.md or the catalogue is
never read end to end in a film chat. Each pack's "Bite" rules are the ones its stage breaks most.

## Plan (Opus, high): the brief, staging, questions, the estimate
- When Sam gives the screenplay and title: `python3 source/kitfilm.py begin FILM` (the film's start: the kit tests run in the background; rule 90). It also writes "Kit found at the start" into the notes (B3, 27 Nov): the catalogue's rows per brief line, and the face tool started for each real person whose front photos are filed as `references/faces/NAME/NN-front-WHERE.jpg` and named in the brief (no brief yet: `kitfilm.py lookups FILM` once it is written). File a new person's photos there before `begin`.
- When Sam asks for the film's lessons: `python3 source/kitfilm.py lessons FILM` first (the film's end: the kit tests; rule 90).
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
- **Find the kit by words first** (replay test 2, Sam's Y, 27 Nov): `python3 source/catalogue.py find "what the film
  needs"` per person, set, prop and move: the catalogue's best rows. **A real person:** `facepick.py NAME OUT FRONT.jpg ...
  --says "beard=.., glasses=.., age=N"` (about 2 min), then a people-file block (`head: house NAME, hair PIECE, look
  detail`, copy May's in `story/brexit-is-done-people.txt`). facepick prints the hair piece that fits, or **NEW: no hair
  piece fits**: that is a NEW row in the estimate, priced. Pieces: swept, back, bob, bald, braids, long (straight, middle
  parting, past the shoulders; B2). A beard over 0.4 of the lower face is drawn solid and short in the hair's colour
  (B1; `--says beard=stubble|full|grey` overrides; `beard: short C` in the people file). `people.colour_faults(FILM)` names skin, hair or beard far from
  the photo; put it right with the file's `skin:` / `beard: boxed C` lines.
- Each stage's end: `ledger.py stage FILM NAME` also keeps that stage's steps (for comparing films later).
- Bite: 24, 74, 1, 38, 8, 11. Tools: `ledger.py estimate`, `plan.py`, `catalogue.py`, `rough.py board` (then `sent --board`).
- Moved from CLAUDE.md word for word (startup fixes 4, 16 Nov): **Reference photos and reporting (full network access since 12 Nov):** I send 2-3 when I have them; otherwise search
  once, slowly, 3 per place at most: **news pages and press photo galleries first** (Al Jazeera galleries, AP, Reuters,
  euronews, dpa, local papers), free libraries (Wikimedia, Geograph, Openverse, Pexels, Unsplash) only when the news
  has nothing. **One failed try per source, then stop** and give me one numbered list of what to find, which angle and
  why.
- **A site that refuses (Sam's Y, 25 Nov: "Always ask for permissions when a site fails like that and I'll happily
  grant it"):** when a site refuses me (a download blocked, "too many requests", a login needed), I ask Sam straight
  away, in one numbered question, what would let it through (a permission, a key, or another site), instead of giving
  up. If the block is my tools' own safety check, which Sam can't switch off from his phone, I say so plainly and try
  the app's page-reading helper (web-fetch) first. Saved example: notes/learn/site-refusal/r7-chat1.md.

## Build (Opus, high for new things; medium from a clear plan)
- Read: `guides/figure-rig.md` 2-4, 5c (people); `guides/satire.md` Movement, One set one plan; `guides/pose-gallery.md`
  only the rows the film uses; `guides/critique-checklist.md` (what the critique will ask).
- Bite: 41, 89, 3, 28, 61, 83. Tools: `critique.py pack/record`, `posegallery.py`, `compare.py`, `codemap.py`.
- Critique: ONE pack per stage (`"stage"` in the spec), two hunts, then `critique.py fixed`; a third is refused.
  A Glimpse (rule 24) is the exception to "drawn alone": one view, one pose, no sheet of its own; its panel is its
  shot's frame at phone size plus one 2x crop, marked `"glimpse": true`.
- At the end: each new thing that passed the critique gets a row in the catalogue's "Passed the critique".

## Notes round (Opus, medium): Sam's notes, fixes, clips
- **First, the one-page fix pack, `guides/fix-pack.md`** (cost-spike fix 4, Sam's Y, 27 Nov): each note marked
  (`notesteps.py note`), found (`page.py show`), its functions' users and kit tests asked (`touch.py NAME`), the
  RERUN line run; it replaces reading the rest of this pack for a fixing chat.
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
- **The every-frame watch (Sam's Y, 27 Nov; seeing test):** named in the one-line check offer before every clip or
  animatic (about 1 minute a second of film to render plus the look). On his Y: `seeing.py render CASE --film MOD
  --span T0 T1`, then `seeing.py watch CASE --film NAME`: only frames changed since that film's last watch are shown
  (Sam: "doesn't check the same footage twice"); `--all` shows everything. Claude looks at every flag at full size
  first (a third were real, most of the rest something hidden behind something in front: settle those with the
  who-is-where view) and tells Sam only the real ones. Evidence: notes/seeing-test/flags-checked.md.

## Final and posting (Sonnet)
- Read: `guides/tiktok-design.md` The video file, Sign-off, Posting; `guides/preflight.md` Stage 5.
- Bite: 70, 75, 52, 47, 37. Tools: `finish.py CLEAN OUT --film NAME`, `ledger.py log/audit`.
- The day a film is posted: add it to `source/data/freeze/films.json`, then `python3 source/freeze.py tag --push` (its bookmark
  at the save its final video came from). The handover check refuses a video in `animations/` that no film lists.
- The day a film is posted (Sam, 27 Nov: "check back in on what you just said and ensure that it is true"): the first
  film posted after Open Wounds is checked against the 27 Nov estimate (notes/cost-spike-fix.md, "Estimate to check"):
  its real cost against what was said, told to Sam plainly, the film called by its title. `handover.py end` flags it
  until the notes carry "## Estimate checked" (estimate_faults).

### My accounts (Sam, 26 Oct)
(Moved from CLAUDE.md word for word, startup fixes 4, 16 Nov.)
- Channel and brand name on every platform: **CranbriJoos**. TikTok (main platform): `www.tiktok.com/@cranbrijoos`.
- YouTube Shorts is the second platform: same name and profile picture (`profile/cranbrijoos-tiktok-1080-eyes-open.png`,
  the beaver's face); every Short's description and pinned comment points back to the TikTok link.

## A tool job (Opus, high to design; medium to build)
- Read: the job's own section in `notes/next-jobs.md`; the tool's MAP; `source/kittests.py` for its tests.
- Bite: 86, 13, 85. Every tool gets a kittest; its rule's check column names it (on Sam's yes).
- An essential tool also gets its line in `source/toolhealth.py` TOOLS: a plain promise, a reach test worked out from the project now, a real-use test on last week's records (R14).

## A pose kit job (Opus, high to build a new pose; medium for notes on it)
- Read: `guides/pose-kits.md` (the default tool, the layers, the order of work); the film's Brief checklist.
- First reply says the default tool (the start check prints the line); another tool only with its reason (Sam, 26 Nov).
- Bite: 87, 30, the proposal route.

## Film types (moved from CLAUDE.md, 10 Nov; the rules unchanged)
- **Satire-style film** (the TikTok series, beyond two people talking): `guides/satire.md`, always starting from
  `source/satire_template.py`, and the rulebook. `guides/best-practice.md` Part 2 only for a scene satire.md doesn't cover.
- **Motion-led films** (stunts, action): a quick animatic early, after the cast sheet.
- **Flat cartoon people:** `guides/figure-rig.md`; follow `guides/preflight.md` from the first brief. Hands are always
  a plain circle with props laid over it.
- **Yuletide horror trailer** (a separate experiment): `guides/yuletide/yuletide-trailer.md`, starting from the newest
  engine. Nothing in `guides/yuletide/` applies to the TikTok films.
