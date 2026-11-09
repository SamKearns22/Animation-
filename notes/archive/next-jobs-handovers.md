# Where things stand (archived 9 Nov) (project, 7 Nov; the last film is finished)

- **Rules that bite next:** 78 (resting arms show weight, never sink), 79 (full-size looks before "looks right"), 74 (acting list: shot and why, meaning questions first, no limit).
- **Done (7 Nov):** the touch check prints COULD NOT TEST when it finds no hand or object (`audit.py`, `kitchecks.py`); rules 74, 78, 79 written; two tips in `guides/figure-rig.md` s.4; reference photo `references/body-weight/leaning-on-table-forearm-forward.jpg`. Hook Text rule dropped. All on the main line.
- **Next job A, sitting kit: part 1 BUILT 8 Nov** (`source/sitting.py`, notes `notes/sitting-kit.md`); sheet and moves video sent to Sam. Part 2 after his look: Opus, high effort, new chat. Type: "Build the sitting kit, part 2, from notes/sitting-kit.md".
- **Job B, rule 78 check: BUILT 8 Nov** (`kitchecks.rests`, run by pre-flight; films list resting arms in `RESTS`; tested on the sitting kit's desk and armchair poses and planted faults).
- **Needs Sam:** a look at the sitting kit's sheet and moves video.
- **Read:** `guides/figure-rig.md` s.2 body, s.3 limbs, s.4 contacts, s.6 movement; `guides/pose-gallery.md`; `source/kitchecks.py` (touches, resting); rule 78 and 32 and L1 in the rulebook.
- **Open rule requests:** none (rule 80 written 7 Nov). New rules from A or B are proposed to Sam first.
- **For Claude:** existing seat support is only `check_seated` (hips on the seat) and the desk-seated note in figure-rig s.4; no stand-up, feet-up or seat-change poses exist yet. Check `source/moves.py`, `posegallery.py`, `figure.py` before building.




## Where things stand (project, 9 Nov, after Job C chat 1)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 44 (12% a film), 85 (cost watch).
- **Done (9 Nov):** Job C chat 1: rulebook 99 rules to 81 by merging repeats (nothing dropped but the pypi.org line), contents lists, CLAUDE.md re-sectioned (Sam: Y to all 26 points). Handovers-at-the-bottom rule written (Sam: Y).
- **Next:** Job C chat 2, the guides: Opus high, new chat: "Tidy the guides, chat 2 (Job C in notes/next-jobs.md)". Job D (APPROVED) in its own chat, any time.
- **Needs Sam:** nothing.
- **Read:** this file; the rulebook's "Merged numbers" (last section); then the guides as listed in Job C below.
- **Open rule requests:** Job D's rule comes with its build.
- **For Claude:** chat 2 also points the 63 old-number mentions (e.g. "rule 55", "rule 73", "rule 84") in guides/, source/ and notes/ at their new homes, using the rulebook's "Merged numbers"; `git grep -nE "[Rr]ules? (12|15|23|33|35|45|46|51|53|55|60|68|69|71|73|82|84)\b"`. Cost watch WEEK_USD still to calibrate.

# Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 44 (12% a film), 85 (cost watch).
- **Done (9 Nov):** Job C finished. Chat 2 (the guides, about 0.6% of a week): research and roadmap pages moved from
  guides/ to `research/`; quick-video's "Added 8 Oct" tail folded into its steps and fix table; best-practice Part 2 and
  Part 5 cut to what isn't written elsewhere (7,500 to 6,000 words; repeats of satire.md, tiktok-design.md, preflight.md,
  CLAUDE.md and the rulebook removed, nothing else dropped); contents lists on every guide; stale lines fixed (preflight's
  model sheet now front/side/back per rule 38; tiktok-design says no title by default; its "Working" section was a copy of
  CLAUDE.md); every old rule number in guides/, source/ and notes/ points at its new home.
- **Next:** Job D (APPROVED), new chat, Opus high: "Build the softer voices tool (Job D in notes/next-jobs.md)".
- **Needs Sam:** nothing.
- **Read:** this file's Job D section only.
- **Open rule requests:** Job D's rule comes with its build.
- **For Claude:** archives (`notes/archive/`, `guides/archive/`) keep old numbers on purpose (history). Cost watch
  WEEK_USD still to calibrate.



## Archived 9 Nov (Job E chat)
### Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 85 (cost watch), 87 (notes restated before fixing).
- **Done (9 Nov):** Job D built: every film's voices now get a gentle polish (warmth, the 2-5 kHz edge and treble eased
  by how bright the take is, a de-esser on s-sounds), and long loud stretches (Ad-Vanced Notice's explosion, 4 dB over)
  are evened in the master. Before/after clip of Ad-Vanced Notice line 9 sent to Sam (17 s, 3.5 MB, not on GitHub).
- **Sam, 9 Nov, on the clip: "It's better, definitely."** Kept as built. Job D closed.
- **Next:** nothing queued.
- **Needs Sam:** nothing.
- **Read:** this file's Job D section only.
- **Open rule requests:** none (S10 was already the riding rule, so the voices rule is S11, written 9 Nov).
- **For Claude:** `mossad_audio.polish` (in `line()`, before `restore_tail`) and `even_out` (in `master` and
  `limit_check`), both under `MA.POLISH` (True). Strength knobs at the top of the softer-voices block: WARMTH_DB,
  EDGE_TARGET, EDGE_CUT, SHELF_DB, DEESS_MAX_DB. `python3 source/mossad_audio.py soft NAME...` prints each take's edge and
  hiss before and after. Cost watch WEEK_USD still to calibrate.

