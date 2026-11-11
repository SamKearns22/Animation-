# Job packs: what each stage reads (Job J, 10 Nov; Sam: Y)

Three layers of reading. **1. The core** (CLAUDE.md, loaded by itself). **2. One pack below**, for the stage the
handover names: only the sections it lists (`grep -n '^## ' FILE`, then read those lines). **3. Look-ups**: a rule
by number (`grep -n '^| 41 ' guides/film-quality-rules.md`), a kit piece by name (`grep -n -i NAME
guides/kit-catalogue.md`), only when a note or a fault names it. The whole rulebook, satire.md or the catalogue is
never read end to end in a film chat. Each pack's "Bite" rules are the ones its stage breaks most.

## Plan (Opus, high): the brief, staging, questions, the estimate
- Read: `guides/preflight.md` Stage 1-2; `guides/satire.md` Start, Getting it right first time, The acting list;
  `guides/tiktok-design.md` Hook Text; the film's notes from `notes/_template.md`.
- Known or new: every person, set, prop, pose and move in the brief goes in the estimate table as KNOWN (a
  `guides/kit-catalogue.md` line, a `guides/pose-gallery.md` row, a "Passed the critique" row) or NEW (priced, drawn
  alone and critiqued before the cast sheet, rule 89). Known is almost free; the estimate is the new rows.
- Bite: 24, 74, 1, 38, 8. Tools: `ledger.py estimate`, `plan.py`, `catalogue.py`.

## Build (Opus, high for new things; medium from a clear plan)
- Read: `guides/figure-rig.md` 2-4, 5c (people); `guides/satire.md` Movement, One set one plan; `guides/pose-gallery.md`
  only the rows the film uses; `guides/critique-checklist.md` (what the critique will ask).
- Bite: 41, 89, 3, 28, 61, 83. Tools: `critique.py pack/record`, `posegallery.py`, `compare.py`, `codemap.py`.
- At the end: each new thing that passed the critique gets a row in the catalogue's "Passed the critique".

## Notes round (Opus, medium): Sam's notes, fixes, clips
- Read: the film's notes (open notes and Where things stand only); the code lines the film's MAP points to.
- Bite: 30, 87, 89 (with 56, 76, 79 in it), 88. Tools: `critique.py where/before`, `final OUT --small --span T0 T1`.

## Checks and animatic (Sonnet): pre-flight, check sheet, render, send
- Read: `guides/satire.md` Before every render, Render, If a check fails; `guides/preflight.md` Stage 3.
- Bite: 59, 67, 14, 89 (the critique gate), 75. Tools: `preflight.py NAME OUT --text`, then in full; `finish.py`.

## Final and posting (Sonnet)
- Read: `guides/tiktok-design.md` The video file, Sign-off, Posting; `guides/preflight.md` Stage 5.
- Bite: 70, 75, 52, 47, 37. Tools: `finish.py CLEAN OUT --film NAME`, `ledger.py log/audit`.

## A tool job (Opus, high to design; medium to build)
- Read: the job's own section in `notes/next-jobs.md`; the tool's MAP; `source/kittests.py` for its tests.
- Bite: 86, 13, 85. Every tool gets a kittest; its rule's check column names it (on Sam's yes).

## Film types (moved from CLAUDE.md, 10 Nov; the rules unchanged)
- **Quick video** (short two-person film): read only `guides/quick-video.md`. Sonnet, medium effort.
- **Satire-style film** (the TikTok series, beyond two people talking): `guides/satire.md`, always starting from
  `source/satire_template.py`, and the rulebook. `guides/best-practice.md` Part 2 only for a scene satire.md doesn't cover.
- **Motion-led films** (stunts, action): a quick animatic early, after the cast sheet.
- **Flat cartoon people:** `guides/figure-rig.md`; follow `guides/preflight.md` from the first brief. Hands are always
  a plain circle with props laid over it.
- **Yuletide horror trailer** (a separate experiment): `guides/yuletide/yuletide-trailer.md`, starting from the newest
  engine. Nothing in `guides/yuletide/` applies to the TikTok films.
