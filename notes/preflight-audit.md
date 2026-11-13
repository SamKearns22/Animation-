# Pre-flight audit (Sam, 13 Nov): quick, useful, cheap, effective

## Where things stand (the ONE handover)
- **Rules that bite next:** 59 (the lock: an animatic now runs the picture checks itself), 19 (one line per fault), 30.
- **Done (chat 2 of 8, Opus medium, 13 Nov):** all five built. 1: pre-flight is the quick check (no fingerprint pass,
  no picture pass); the animatic render (--small) draws with the probes on and keeps no video on a fault; a clean one
  stamps the code "pictures checked", which the final needs (or preflight --pictures). 2-3: report.group (one line per
  fault, by check, shot and who, with span and count); COPIES no longer matches a named person with themselves.
  4: shots over 8 s an info line; PROP TURN kept only for people seen at yaws 30+ degrees apart. 5: MOUTH (views.Eyes
  marks, measured from the eye whites) and TURN DESIGN (own front face, generic turned head). Rules 59, 67, 19, 13
  reworded. New kittests pass (render_lock, preflight_lines_grouped, every_face_has_a_mouth); full suite: see Next.
- **Done (chat 3 of 8, Sonnet medium, 13 Nov):** kittests: the one failure WAS ours (views.Eyes.line drew through the
  wrapped pen: Vance's turned head changed); fixed, all kittests now pass (the budget test passes too). Also fixed a crash
  in preflight (`logged` unset without pictures). Timed run on Blessed (finished, no film change; pre-flight needs
  `--audit` or the notes gates to run on a finished film): quick pre-flight 59 s (5 grouped lines); animatic render
  with picture checks 29 min 8 s (4.7 MB, 36 faults found: HANDS 21, LAP 6, other 5, COPIES 1, CUT 1, TURN DESIGN 1,
  UNSEEN 1; not fixed, video not sent). Total ~30 min vs old ~54 min (40 + 14.5). Not saved: render is 2x the old
  animatic because it now also checks every frame.
- **Next: nothing queued.** Sam decides what to do with the audit's result (see message).
- **Lost (to tell Sam):** the incremental re-check (fingerprints): the render redraws every frame anyway; the contact
  sheet unless asked (--pictures). **Added:** mouth check, turn-design check, final needs a clean animatic first.
- **Needs Sam:** nothing. Sam: Y (13 Nov) to the timed run; Blessed marked finished (no film changes).
- **Read:** this section only; preflight.py by its MAP if a fault needs a fix.
- **Open rule requests:** none (59, 67, 19, 13 written on Sam's Y).
- **For Claude:** render check mode: film_engine.render (check=..., _checked, picture_faults at the end); stamp
  field 'pictures'; mouth: views.Eyes.mouth_seen; turn: turnhead.GENERIC. chat-qfystema's 1 newer commit is a ledger
  row only (not merged). The render on Blessed is the first real test of check mode: if it crashes, fix there.

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

**Time (Blessed, 762 frames, 4 cores, measured 13 Nov):** text and set checks 57 s (film load 16, film checks 13,
linecheck 19, clipcheck 6); fingerprint pass (draws every frame plain, 3.5 s a frame) ~11 min, every normal run;
picture checks (every frame drawn with probes, 7.5 s a frame) 24 min full; film audits 2.2 min; sheet 1.3 min.
So a full run ~40 min, a re-run ~15 min even for one changed frame (the fingerprint pass). Animatic render 14.5 min.
Re-runs fall back to full whenever a check file changes; 5 of the 6 such commits since 11 Nov were drawing-kit files.
**Noise (Blessed final, --audit): 137 faults + 356 repeat lines.** DIRECTION 38 (press extras swapping sides at one
cut: Sam's note 46's kind, but 38 lines), HANDS 43 (33 on extras), COPIES 20 (a bug: a person matched with itself),
LAP 14 (real by Sam's 13 Nov checklist), "press0 stands in the sign" once a frame (360), 2 cm crowd brushes.
**Cost:** Blessed's animatic 1 stage cost 9.8% of a week against 2% planned (99 faults, then 17, then reruns).

## Proposals sent to Sam (13 Nov): Sam Y to all
1. One drawing pass per animatic: the render runs the picture checks while it draws (stops on a fault); pre-flight
   before it is the 1-minute check. Saves the 11 min fingerprint + up to 24 min picture pass (~15-35 min an animatic).
2. One line per fault: grouped by check, shot and who, with time span and count; extras' hand touches and crowd side
   swaps summed per cut. 137+356 lines -> about 20.
3. Fix two false-fault bugs: COPIES (a person with itself), per-frame repeats.
4. Lost: "shot over 8 s" stops being a fault (6 of 10 films flagged it, always chosen; caught nothing); the prop-turn
   test only for props seen turning (9 false, 0 real in 10 films).
5. New: every face on screen has a mouth (Blessed 5, 15, 45); a head keeps its design through a turn (N9).
