# Pre-flight audit (Sam, 13 Nov): quick, useful, cheap, effective

## Where things stand (the ONE handover)
- **Rules that bite next:** 59 (render lock), 19 (PASS / FAULT / COULD NOT TEST, short summary), 30 (repeat notes).
- **Done (chat 1 of 8, Opus high, 13 Nov):** measured one full pre-flight on Blessed's final code (--audit, 4 cores):
  28.4 min + an 11 min fingerprint pass in a normal run (see Findings); the last 10 films' record; 5 proposals sent to
  Sam as one numbered message. Ledger row moved to its own name (Sam: "own name").
- **Next: on Sam's numbers, Opus MEDIUM (building from a clear plan): build the changes he says Y to, time one run
  on Blessed, then one short message.** This chat is amber, so it opens that chat.
- **Sam: Y to all of 1-5 (13 Nov, evening).** Needs Sam: nothing until chat 2's message.
- **Read:** this file (Findings and Proposals only); preflight.py by its MAP.
- **Open rule requests:** none written; proposals 1-5 change rules 59/67 (1), 19 (2), 13 S7 (5) on Sam's Y.
- **For Claude:** timer wrapper in the chat-1 scratchpad (gone); re-make: wrap each check's faults() and print times.

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
