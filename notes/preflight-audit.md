# Pre-flight audit (Sam, 13 Nov): quick, useful, cheap, effective

## Where things stand (the ONE handover)
- **Rules that bite next:** 19 (PASS / FAULT / COULD NOT TEST, short summary), 59, 24 (real costs only).
- **Done:** brief written by cost job chat 2 (13 Nov). Sam's philosophy for every stage: checks made more
  intelligent, improved and condensed so the film (1) is high quality, (2) draws fewer notes and faults, (3) lands
  within 15% of a week, every time. CLAUDE.md "Rules are permanent": improve the check that missed, merge overlaps,
  remove only what caught nothing in three films with Sam's Y on a "Lost:" line.
- **Next: chat 1 of 8, Opus HIGH (diagnosis and design):** the job below. First merge the main line and cost chat
  4's branch (session ..YcS6kXZ4oqFySTEMa is editing `preflight.py`: COULD NOT TEST, Blessed's clipcheck solids);
  touch no file it is editing until it has pushed.
- **Needs Sam:** nothing until the audit's numbered Y/N message.
- **Read:** this file; `notes/cost-diagnosis.md` "Job B results" only; `preflight.py` by its MAP (`codemap.py`).
- **Open rule requests:** none.
- **Sam (13 Nov, 15:55): the audit's cost goes under its own name (preflight-audit), not Blessed's.** The Stop hook's
  `ledger.film_of` picked 'blessed' (this chat named Blessed's files most) and fired Blessed's budget stop. At the
  handover, move this chat's row from notes/ledger/blessed.json to notes/ledger/preflight-audit.json. Paused until 17:00
  (Sam); a scheduled message resumes this chat then.

## Known so far (from the notes, 13 Nov)
- **Time:** 9-15 min a run on Blessed (14 min 46 s in chat 3), up to 40 min on earlier films; re-run after every
  fix (about 13 min each), so 2-3 runs an animatic.
- **Effective?** Mixed. Real catches on record: hands (rule 41, the busiest), subtitles, loudness mouths, Blessed's
  folded-back elbow (N1, printed as "allowed", so it passed). Noise: one run printed 99 faults, mostly tool noise
  ("never on screen", plan rooms); the mouth check over-reads drawn-out words (4 films). Silent misses: clipcheck
  tested nothing on Blessed (no solids), so the pool player through the table passed (N8).
- **Cost:** the run itself is cheap in tokens (Blessed 17 faults, ~1.9k filtered); the cost is the chat reading and
  answering each fault at ~5 cents an action at 200k, the waits, and the re-runs. Not yet measured per run.

## The job
1. **Measure each of pre-flight's checks** (about 12 check files, 43 imports): run time (time each on Blessed's
   current code, one run, `--text`); faults it raised on the LAST 10 FILMS (Sam, 13 Nov: they are all very different, and
   some catch what others don't; ledger round files, notes and archive notes, commit messages); for each: real catch, false alarm, could not test,
   and whether Sam later named the same fault (caught, missed, or let through).
2. **Cost per animatic** from the app's real figures: the actions spent answering pre-flight in one Blessed chat
   (one `list_events kinds=["assistant"]` page around a pre-flight run, never the whole chat).
3. **Design, by the new order:** improve the checks that missed Sam's notes (overlaps in motion, arms bending the
   wrong way, repeats); merge checks that overlap; propose removing only what caught nothing in the 10 films. Targets: one
   run under 5 minutes (only changed shots re-checked; the rest cached), one short list of real faults with frame and
   fix, no "allowed" for a fault Sam has noted, every check PASS / FAULT / COULD NOT TEST, and its cost per animatic.
4. **End with one numbered Y/N message to Sam:** each change with what it saves (minutes, % of a week, measured),
   what it catches, "Lost:" lines for anything removed. Change no rule or tool before his numbers; then hand over to
   an Opus medium chat to build.
5. Keep the chat small: batch commands, filtered printouts, hand over before 200k.

## Findings (chat 1 of 8, 13 Nov; real figures)
**What pre-flight did on the last 10 films** (notes, archive notes, commit messages; R = real fault fixed, N = noise
or a choice Sam had made, M = Sam later noted what it missed):
| Film | Pre-flight's record |
|---|---|
| Blessed | 99 faults (mostly noise: shot cast 'never on screen', plan rooms) -> 17 -> 1. R: oath arm fold (stopped the render), oath hand hidden, Bible floating off the hand, frozen judge (= Sam 36), 3 arms back to rest before a cut, lying pose (= Sam 6). Caught but let through: N1 elbow ('allowed'), 45 newsreader mouth (named). M: N8 pool player through the table and N3 fist through the Bible (clipcheck had no solids), 5/15 no mouths, 14/16/23 necks and limb joins, 17 wall detail pops in, 51 sudden zoom (camfeel built the day after), N9 head changes on a turn |
| Remakes | 16, all named: syllable counter misreads (5), prop-turn test on people who never turn (8), no scene(t) (1), a 1.5 s caption (1), critique (1). R: 0 |
| Elder Swindon | hung twice (forked workers, OpenMP); animatic 1 without it (Sam); later 15 min; long shots chosen (2) |
| MidTerminal | R: press palm through the body (hands); 6 caption speeds (estimates, then fixed by recordings) |
| Terfwarts | R: run arms, captions joined, livelier mouths; wiring gaps (scene, cameras) |
| Patriots 4 | R: hands over the table; 7 named each round (3 voice flags meant, 3 captions under reading time) |
| Flying Whales | 6 named, all noise (people/room checks on a film with neither: fixed by HAS, rule 58); 12 s shot chosen; 7.5 min |
| Halo No-No | R: music 3-5 dB over voices, a 0.5 s caption, thin lines; 5 named |
| Netan-yahoo | clean but the chosen long shot; named: prop turn on a staff never seen from behind, a flat portal |
| Prepper Minister | R: stool into the island, robot through an opening's edge (collisions); 11 shared faults unread at render |
