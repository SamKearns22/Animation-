# Blessed: old handovers

## Build chat 1 (11 Nov)
- **Rules that bite next:** 49 (likeness check 60%+ before the cast sheet), 41 (every arm ends in a hand; one outline shoulder to arm), 89 (critique: Brand alone beside his photos, two passes).
- **Done (11 Nov, build chat 1, Opus high):** Brand's likeness pack filed, `references/blessed/likeness/` (b01-b03 straight-on, not smiling: Courthouse News, Guardian, BBC; b04 talking; b05 smiling; b06, b07, b09 sunglasses; b08 topknot sketch); his face card `brand-card.jpg`/`.json`. Card: close-set eyes (84th), long narrow face (77th), narrow forehead (76th), wide nose (73rd); "short nose" is unsure (photos disagree; by eye his nose is long and straight: trust the eye). It missed his beard: by eye a full beard, dark at the moustache, grey-white at the chin and jaw; long dark-brown curls past the shoulders, grey streaks, high hairline.
- **Spent against the estimate:** plan about 1%; build chat 1 about 1% (pack only; amber on reading).
- **Next:** build chat 2 (Opus, high effort): build Brand in `source/blessed_cast.py` copying `ad_vanced_notice_cast.py`'s Vance pattern (P4 MEASURED from `brand-card.json`, beard by hand like `scrub_beard`, turnhead register); `likeness.py check` 60%+; then judge, officer, newsreader; cast sheet to Sam.
- **Needs Sam:** nothing until the cast sheet.
- **Read:** `guides/job-packs.md` Build; this file; `source/ad_vanced_notice_cast.py` lines 1-78, 229-300, 376-416, 750-871 only.
- **Lost / Added:** none yet.
- **Open rule requests:** none.
- **For Claude:** sources that worked 11 Nov: Courthouse News (www.), Guardian (i.guim.co.uk, `s=none&width=1400`), BBC (ichef), Sky (e3.365dm.com), AP via WJTV; upload.wikimedia.org thumbs (429 after ~5); commons pages via firecrawl_scrape. Refused: AP/People/NYT/Independent/NPR/SCMP. Police interview stills are straight-on but small.



## Build chat 2 (cast), 11 Nov
- **Rules that bite next:** 89 (fresh-eye critique once the film draws frames), 41 (arms end in hands), 74 (acting list before animatic 1).
- **Done (11 Nov, build chat 2, Opus high):** the cast in `source/blessed_cast.py` (Vance pattern). Brand: measured face, beard, long curls, topknot, aviators (on / lowered), 10 moods, three looks (trial, stand/dock, prison), turned heads. Likeness 64% on b01 (pass) after Sam's notes 1-2 (bigger head, short chin and beard; b10 is the usual reference). Sam's six recordings filed (note 3). Judge (invented, wig front only), prison officer, newsreader. Two by-eye critique passes: fixed the judge's missing wig, the officer's lab-coat look, the topknot cone, the lowered shades, the turned hair's spikes and the strip across his face. Cast sheet, faces sheet, likeness sheet in `notes/sheets/blessed-*.jpg`, sent to Sam.
- **Spent against the estimate:** plan ~1%; cast stage 2.41% of 4% planned (ledger: lands at 11.4%).
- **Next:** build chat 3 (Opus, high effort), opened by build chat 2 on Sam's Y: the sets (court outside, courtroom x2, prison cell + phone, van, TV room, BBC-style studio, gates), then `source/blessed.py` from `satire_template.py`.
- **Needs Sam:** nothing until the sets sheet (Sam: Y to the cast, 11 Nov).
- **Read:** `guides/job-packs.md` Build; this file; `source/blessed_cast.py` MAP only.
- **Lost / Added:** Lost: prayer beads on his chest (read as dots; can go in his hand). Added: none.
- **Open rule requests:** none.
- **For Claude:** `critique.py pack` needs film frames (`blessed.py` not built), so rule 89's fresh-eye helper was not run on the cast; run it on the first set/shot frames. Likeness: `P4.TUNE['brand']` was tuned against b01+b03; the dark moustache and the long beard tip carry the chin and nose measures (slimming them dropped b03 to 44%). Judge side/back views are bald (wig is front only: he is only seen front-on at the bench). Turned long hair: `_turned_long` (screen units).


## Where things stand (the ONE handover)
- **Rules that bite next:** 74 (acting list before animatic 1), 41 (arms end in hands: the gavel, the oath, the phone), 89 (critique the moves).
- **Done (11 Nov, build chat 3, Opus high):** the sets, `source/blessed_sets.py`: court outside, courtroom from three cameras (witness box, the bench, the glass dock), van cubicle, cell (+ cot close-up), landing wall phone, TV room, the TV with the BBC-style studio (newsdesk restyled red), the prison gates. `source/blessed.py` from the template: Sam's six takes timed (54 s), 12 shots, everyone placed at their marks in held poses, press pack with TV cameras and boom mics, the phone handset and its cord, the face change's push-in, the newsreader's voice fading. Refs found for the cell and gates (12-14, 18-20); none reached for the van or TV room. Critique: two fresh-eye passes, faults fixed; checks clean (mouths, voice, set overlaps, benchmark). Sets sheet sent to Sam.
- **Spent against the estimate:** plan ~1.2, cast 2.41, sets 5.19 of 5.0 planned (this chat hit red at 5.2%). Ledger: lands at about 10% of the 19%.
- **Next:** the moves chat (Opus, high effort: the oath and the weeping are new poses): the acting list's moves in `blessed.py`'s shot functions (press walk and gestures, oath with Bible and raised hand, the gavel strike, van slump, escorted walk in, lying curled weeping on the cot via `lying.py`, phone dejection, eyes up and the face change, gates exit through the wicket door with arms flung wide), then rehearsal clips (gate exit, face change, escort).
- **Needs Sam:** a look at the sets sheet (no answer needed to go on); 2-3 photos of a prison van cubicle and a prison TV/association room if he has them (none reached us).
- **Read:** `guides/job-packs.md` Build; this file; `source/blessed.py` MAP; `blessed_sets.py` MAP and STAGE only.
- **Lost / Added:** Added: the royal arms (lion and unicorn) over the bench, a clock and a door on the courtroom wall (a real Crown Court has them; not in the sketches' crops). Lost: none.
- **Open rule requests:** none.
- **For Claude:** pass 2's kept items (not faults, or the moves stage's): hair loose at trial and the gates, topknot from the dock on (Sam's answer 7); 'BBC NEWS' lettering (Sam's answer 5); the turned long hair reads as a braid from the side (cast: `_turned_long`, look in the moves stage at yaw -45); the arms' supporters read loosely at phone size; Brand's head is bigger than the inmates' (the likeness `_Big`). This chat's cost had to be put in the ledger by hand (`ledger.auto(transcript)`): the session started outside the repo so the project's Stop hook did not run. Prison phone: `handset_pose` + `phone_cord` (near hand 'L' when facing left).


## Where things stand (moves chat 5, 11 Nov)
- **Rules that bite next:** 41 (arms end in hands: the gavel, the oath, the Bible, the phone), 89 (critique the moves), 74 (acting list before animatic 1).
- **Done (11 Nov, moves chat 5, Opus high):** planned every shot's moves against the code and the kit (below, "The moves plan"); no code changed: the chat hit the amber cost mark after the planning (a worker restart doubled its reading).
- **Next (Sam: Y, 11 Nov, to about 1.5% more):** moves chat 6 (Opus, medium effort: building from a clear plan): build "The moves plan" in `source/blessed.py`, rehearsal clips (gate exit, face change, escort), two critique passes, send Sam the clips; `ledger.py stage blessed moves` at the end.
- **Needs Sam:** a look at the sets sheet (no answer needed); photos of a prison van cubicle and a prison TV room if he has them.
- **Read:** `guides/job-packs.md` Build (figure-rig 2-4 and 5c, satire.md Movement, the pose-gallery rows named in the plan); this file's "The moves plan"; `source/blessed.py` (480 lines, whole); `blessed_sets.py` MAP, `cell` (line 574), `court_bench_front` and `gavel` (406-440), `gates` wicket door (950).
- **Lost / Added:** Added (planned): a second gates camera (wide: he steps out of the wicket door; then closer at his mark for the rest of the line). Lost: none.
- **Open rule requests:** none.
- **For Claude:** carry on from the plan; don't re-derive it. Prison phone: `handset_pose` + `phone_cord` (near hand 'L' when facing left). Kept from the sets stage: hair loose at trial and gates, topknot from the dock on; Brand's head bigger than the inmates' (`_Big`).

## Moves chat 7 (11 Nov)
- **Rules that bite next:** 74 (acting list before animatic 1), 24 (the estimate and the stop), 89 (critique: done for moves).
- **Done (11 Nov, moves chat 7, Opus medium):** faults 1-5 fixed (oath: raised palm on the near side by the head, Bible in the far hand on the white shirt with a pale page edge; cot: curled along the bed, head at the pillow, contact check clean; gavel: hand on the bench top from the cut, raise to y 1000; van: fists clasped in front of the knees; arrival: hand at the shades' side, nose clear). Sam's note (testimony head) fixed: the head outline folded at the left temple (notch), a hair stroke left the hair, the beard tufts became stair steps and skin flecked under the chin when he turns. `touch_faults()` in `checks()` (gavel hand, Bible, officer's grip; proved it catches a moved hand); checks clean. Stills sheet and 3 clips sent; two critique passes (one fault: the amazed mouth read as a tongue; now a round O).
- **Next:** cast chat 8, Opus, high effort: Sam's notes 4 (press pack from behind: shoulders, collars, ears, shaped hair, arms, one turned three-quarter) and 5 (inmates: scale and head size matched to Brand, mouths, face detail); stills of arrive, gates, tvroom, push; one critique pack; `ledger.py stage blessed cast` at the end; then animatic 1 prep (acting list, check sheet), Opus medium.
- **Needs Sam:** a look at the stills sheet and the four clips. (Sam: Y, 11 Nov, to notes 4 and 5, about 1% more; keep to it.) Photos of a van cubicle and a TV room still welcome.
- **Read:** `guides/job-packs.md` Build (figure-rig 2-4, 5c); this section; the Notes table rows 4-5.
- **Open rule requests:** none.
- **For Claude:** `blessed_cast._outline` (P4.outline_uv retraced the upper-left temple; fixed for Brand only, other films untouched); beard tufts scale with |sin yaw| on TurnFace (`ta`); `COT_AT` (x, d, flip, yaw); `OATH_RAISE`/`OATH_BIBLE`/`OATH_BOOK`; `GRIP_AT` feeds the touch check. Push close-up crops the hair top late: left as is.



## Where things stand (cast chat 8, 11 Nov)
- **Rules that bite next:** 74 (acting list before animatic 1), 24 (the estimate: forecast 20.2% against 19%, Sam's ~1% included), 89 (critique: done for cast).
- **Done (11 Nov, cast chat 8, Opus high):** note 4: the press pack are standing people (shoulders, collars, arms, legs) with turning heads (skull, both ears, neck, eight shaped haircuts), three turned three-quarter and glancing aside in profile; TV cameras, booms in raised hands, phones held up; the same pack at the gates as at the arrival (Sam's answer 6); one journalist moved so Brand's chest shows at the arrival. Note 5: inmates on Brand's measured face at his size (lips, brows, nose, ears, eye bags, stubble, a beard, freckles, real hair), one bench depth, eyes up at the TV. Found: every planned eye move (oath up, dock and van down, the TV) was under a pixel (gaze_dy taken as drawing units): fixed for Brand and the inmates. Two hunts recorded, fixed, `critique.py fixed`; checks clean; stills sent.
- **Left (set faults the critique found, outside notes 4-5):** TV room: the cue rack reads as a puppet rig, no blue TV glow, four stools not a bench; gatehouse unlike ref 18 (wide front, grilled arch); Brand tiny in the wide gates shot; the arrival boom crosses the sign's H.
- **Next:** Sam opens chat 9 by hand (project Animation- selected, Opus, medium effort) with the backup file "blessed-chat8-work.bundle" attached: apply it (`git pull blessed-chat8-work.bundle claude/blessed-moves-c7`), push to the chat branch and the main line, then animatic 1 prep (acting list, brief ticks, check sheet; stop for Sam's yes). Chat 8 was started by a schedule without push rights, so nothing here is on GitHub yet and it opened no next chat (chain level 8 of 12).
- **Needs Sam:** a look at the notes 4-5 stills; Y/N on fixing the TV-room and gates set faults (about 0.5%); Y/N on a rule "Sam starts each new chat by hand" in place of the self-opening chain.
- **Read:** `guides/job-packs.md` Checks and animatic (and Notes round for the set faults if Sam says Y); this section.
- **Open rule requests:** none.
- **For Claude:** `blessed_cast.inmate_head` (INMATE_FACES), `press_person`/PRESS_STYLES (TH.Person per haircut, `_Big` without `_lift`); `blessed.press_sp/press_pose/press`, PRESS_YAW, `_phone_up`; `blessed_cast.gaze()` scales gaze_dy; `_turned_long(colour, length)`. Setup hook now installs with `python3 -m pip` (pip was another Python).

## Handover after chat 9 (11 Nov)
- **Rules that bite next:** 89 (sets hunts on the new gatehouse, TV-room bench and press pack before the animatic), 74 (acting list ticked), 75 (Hook Text placed at animatic 1).
- **Done (11 Nov, chat 9, Opus):** chat 8's backup applied and pushed. Rule written: Sam starts each new chat by hand (CLAUDE.md). Set faults fixed (Sam's Y): TV room has one bench at knee height, a noticeboard in place of the cue rack, a blue TV glow; gatehouse redrawn to ref 18 (rusticated pilasters, sandstone arch, square grille over a plain timber gate, yellow bollards, sign on posts) and brought to 9 m; wide gates shot framed tighter (zoom 1.4 to 1.7); boom at the arrival shortened under the sign. Sam's notes 7-9: ears no longer drawn over long hair; the press pack crowds the gate and everyone faces Brand at both places. Checks clean; stills sent.
- **Next (opened by chat 9 at Sam's ask), Opus, high effort:** (1) Sam's ask: find a description of how Brand acted and moved before the scandal (stand-up, interviews, red carpets: one search pass, a few sources, cited in these notes), turn it into a short "how Brand moves" list, and revise the acting list and his moves in blessed.py to match (clips of changed seconds; Lost/Added lines). (2) Animatic 1 prep: sets hunts (critique.py), brief and acting list ticked, check sheet with the Hook Text frame; stop for Sam's yes. High effort: new movement built from research.
- **Needs Sam:** a look at the set-fix stills.
- **Read:** `guides/job-packs.md` Checks and animatic; Notes round if the hunts find faults; this section.
- **Open rule requests:** none (the crowd-facing lesson: Sam, 11 Nov, "context dependent": not a rule; decide where each crowd looks in the staging).
- **For Claude:** `ST.gates` rebuilt (`_rustic`, `_arched_window`, GATE_D 9); `press(..., at=(x, d))` sets each journalist's yaw towards the mark (PRESS_YAW now unused), `reach` for the boom; `G2_FROM/TO` 8.5/7.6; turnhead.draw skips ears when sp['ears_hidden']; `_cam` gates zoom 1.4-1.7; gates2 zoom 1.9; tvroom bench at y 1290.



## Where things stand (chat 10, archived 12 Nov by chat 11)
- **Rules that bite next:** 89 (hunt 1's faults fixed as one list, then hunt 2, then `critique.py fixed`), 67 (one full pre-flight, then the check sheet), 61 (blessed.py is 1,140 lines: move the moves into blessed_moves.py).
- **Done (11 Nov, chat 10, Opus high):** Brand's pre-scandal manner researched (4 reviews, cited in "How Brand moves"); the acting list and his moves changed to match (swagger walk, lean in on "mate", knee dip with arms flung open on "super" and "everybody!", chin-up preening, arms up and open on "Blessed!", chin lifts in the oath); clips sent. Head acting from the voice added for Brand and the newsreader (rule 74 gap). Hook Text placed at y 420 (it was over his hair; hookcheck clear). Brief checklist ticked; acting list ticked; sheets lines added. Critique hunt 1 (stage "animatic") recorded: 15 faults. Stopped on amber (2.2%).
- **Next: Opus, high effort (new shot: the jury, Sam's note 10 above "## Notes" table), then the critique round.** Then as before: Type: "Blessed: fix critique hunt 1 as one list, hunt 2, then pre-flight and the check sheet with the Hook Text frame; stop for Sam's yes on animatic 1. Read CLAUDE.md, then notes/blessed.md Where things stand." Hunt 1 triage (look first, 2x crops): likely real: the dip and chin-up too small to read at phone size (dip 34 to ~60, chin -1.3 to ~-2.5); scarf gone in the 3/4 walk; hair a plait in side views; shades a thin gold bar (ref 02: big black aviators); TV room: bench not seen, blue too strong, fang-like teeth; royal arms read as animals; heart hand without forearm at 3.6. Check before fixing: court orange vs buff (ref 00); gatehouse "blank" vs ref 18; Brand tiny in the wide gates. Likely false: single frames can't show the swagger; his L hand is on screen right front-on; the prison bun is Sam's answer 7; at 51.2 he is on his mark.
- **Animatic 1 status (12 Nov 01:10, chat 10):** NOT rendered. Full pre-flight (faults-named) found 99 faults, mostly tool noise (SHOT CAST 'never on screen', plan room overlaps, journalist hands); the real one: the oath's raised right arm folded its elbow under 25 degrees at 4.92 s, which stopped the render at frame 59. Fixed (a waypoint in `oath`); the code changed, so pre-flight must run again (about 13 min) before `final source/data/blessed-clean.mp4 --faults-named`, then `finish.py ... --film blessed`. A scheduled chat (trigger at 1:01 London) was set to do the hunt-1 fixes; do the render after them.
- **12 Nov (Sam):** no gavel shot, the bang heard at the dock's first frame: done, clip sent (film now 52.9 s; times above moved 1.3 s earlier after the oath). Pre-flight must be rerun on this code.
- **Needs Sam:** a look at the movement clips (arrival, gates, sentencing).
- **Read:** `guides/job-packs.md` Notes round and Checks and animatic; this section; "How Brand moves".
- **Open rule requests:** none.
- **For Claude:** hunt 1 = source/data/critique/blessed/r1-p1 (spec in it); new: GAITS['swagger'], `_sway`, `_dip`, `GATE_V`/`GATE_OPEN`, `HEAD_LIFE`, `KEEP_CLEAR`; pre-flight --text faults left: newsreader mouth check at 52 s (her faded line under the gates: allow or stop her track at the fade), fast captions (lines 2, 3, 5), oath shot 9.6 s, SET_FEET missing (rule 13).

## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (hunt 1's faults fixed as one list, then hunt 2 with the jury shot, then `critique.py fixed`), 67 (one full pre-flight, then the check sheet with the Hook Text frame), 30 (if Sam's note on the jury comes back, find why first).
- **Done (12 Nov, chat 11, Opus high):** Sam's note 10 built: the jury shot (7.15-10.41 s, cut in the pause after "Almighty God", back after "shall be the truth"; voice carries over). New set court_jury (panelled wall, windows, jury-room door, two oak tiers, jug and notepads); 12 invented jurors (front only, Glimpses) from the inmates' face system with the press pack's haircuts seen from the front, plus new bob/long/curly/bun/pony/receding hair and glasses; on "the blessed evidence" brows knit one after another, two sceptical brows, two pairs swap glances, one blank stare; a slow push in. Clip sent (blessed-oath-jury.mp4). `blessed.py check` clean. Stopped on amber (1.2%) before the critique round.
- **Next: Opus, medium effort (fixes from a clear triage list).** Type: "Blessed: fix critique hunt 1 as one list, hunt 2 (include the jury shot), `critique.py fixed`, then ONE full pre-flight and the check sheet with the Hook Text frame; stop for Sam's yes on animatic 1. Read CLAUDE.md, then notes/blessed.md Where things stand." Hunt 1 triage (look first, 2x crops): likely real: the dip and chin-up too small to read at phone size (dip 34 to ~60, chin -1.3 to ~-2.5); scarf gone in the 3/4 walk; hair a plait in side views; shades a thin gold bar (ref 02: big black aviators); TV room: bench not seen, blue too strong, fang-like teeth; royal arms read as animals; heart hand without forearm at 3.6. Check before fixing: court orange vs buff (ref 00); gatehouse "blank" vs ref 18; Brand tiny in the wide gates. Likely false: single frames can't show the swagger; his L hand is on screen right front-on; the prison bun is Sam's answer 7; at 51.2 he is on his mark. Jury shot, for hunt 2 to judge: the caption sits over the front row's chests; a tall empty box front below them; long-haired juror 4's hair is a heavy black block.
- **Animatic 1 status:** NOT rendered. Sam: Y (12 Nov) to about 1% more for this stage (it stood at 2.84% of its 2%): one Opus medium chat, then a Sonnet chat to render and send. Pre-flight must run again on this code (about 13 min) before `final source/data/blessed-clean.mp4 --faults-named`, then `finish.py ... --film blessed`.
- **Needs Sam:** a look at the jury clip (note 10) and the movement clips (arrival, gates, sentencing).
- **Read:** `guides/job-packs.md` Notes round and Checks and animatic; this section; "How Brand moves".
- **Open rule requests:** none.
- **For Claude:** hunt 1 = source/data/critique/blessed/r1-p1; jury: source/blessed_jury.py (FACES, JURORS, ACT, draw), blessed_cast FRONT_FACES/_hair_mass/_hair_front/_glasses, blessed_sets court_jury/_mid/_front + STAGE['court_jury'], blessed.py T['jury'], T['oath2'], shots 'jury' and 'oath2' (oath split); SET_BOXES and BENCHMARK have no court_jury rows yet (rule 83/3: add before pre-flight); pre-flight --text faults left from chat 10: newsreader mouth check at 52 s, fast captions (lines 2, 3, 5), oath shot length, SET_FEET missing (rule 13).


# Moved from notes/blessed.md, 12 Nov (chat 3 of 8): built or settled

## The moves plan (moves chat 5, 11 Nov; build it in blessed.py, a "moves" section after "faces and moods")
Takes (seconds, film time): L1 0.62-3.65 one stretch ("feeling" ~1.26, "mate" ~2.36, "super" ~2.75); L2 stretches from 4.98: +0.12-2.05 ("I swear by Almighty God"), 2.32-4.22, 4.53-5.31, 5.62-6.34, 6.62-8.21 ("...the blessed truth"); L3 16.36-18.39; L4 from 28.75, last stretch +4.47-5.05 ("at all right now"); L6 from 49.21: "Blessed!" +0.12-0.72, rest +1.07-3.70.
- **Helpers:** port `word_at` (with ANCHORS for L2 'Almighty' (0, 0.42), first 'blessed' (1, 0.2), last 'blessed' (4, 0.62); L6 'everybody' (1, 0.72)) and `_bump` from `ad_vanced_notice.py` 106-120, 244. `_toward(j, side, tgt, g, pole, shape)`: blend the hand's CONTACT point (wrist + forearm unit x HAND[shape], not the wrist, or it pops) to the target, then `V.arm_to`. Hand circle = wrist + 12 along the forearm, radius 26 (`satire_style.install_circle_hands`).
- **arrive:** walk in ('walk' gait, phase +0.37 so mid-stride at the cut) from (1.2, 4.9) to the mark (0.45, 3.9) on ST.OUT (`ST._mark` gives screen x, y, ppm), yaw -45, stop at ~1.35 s, snap to front (yaw 0). Prayer beads hang from the R fist all shot (`grips.held`, a loop of small beads). L hand to the heart (30, 135, 78), pole 'in', palm, from "feeling" to "mate" - 0.35; up to the shades' bridge (`j['on_face']`) for "mate", the shades lower ON "mate" (brand_mood: replace L1 start + 0.9 with word_at); arms open, palms up, on "super"; L back to the heart with a small bow (lean 6, head nod) on the last "blessed"; to rest by 4.4 (rule 72).
- **oath:** stays yaw -45 at his mark. 0.15-0.65 s into the shot: far hand R holds the Bible at the chest (~(20, 160, 110), a black book with a gold cross, drawn as a projected box like `handset_pose`, `grips.held`); near hand L raised palm out beside the head (~(-(sw+90), -40, 60), pole 'out'; check the elbow by eye). Eyes up (gaze_dy -0.6) only on "Almighty God", ahead otherwise; a small lean-and-nod bump on each "blessed". Arms down from line end + 0.1 to + 0.5 (cut 14.04).
- **gavel (REMOVED 12 Nov, Sam: no gavel shot; only the bang is heard at the dock's first frame):** judge `put_seated` at (540, 1780, 620); set `ST.GAVEL_LIFT = (T['s3'] + 0.15, T['s4'] + 1)` so the set stops drawing the resting gavel. R hand to the handle end (~ world (880, 1404); handle runs right of the head at (760, 1404)) 14.15-14.4; raise to shoulder 14.4-14.75; strike 'fast' 14.75-14.94 (T['bang']); a small rebound, then rest on the block. Draw the held gavel AFTER `ST.front` (the block is in the front layer) in world coords with `ST.gavel(p, x, y, ang)`, then redraw the hand circle over its handle (P1). Stern face; a tiny head jolt on the bang.
- **dock:** hands clasped low (both to (+-10, 420, 60), pole 'back'). Mood 'neutral', eyes ahead, until 15.9; then 'hollow' (eyes snap down) and the shoulders drop over 1.0 s eased (bob +12, head_dy +10, lean 4).
- **van:** seated yaw 35, bent over: lean 28, forearms on the thighs, hands clasped between the knees, head down, staring; a slow +-1.5 degree sway in lean (the van). No other move.
- **escort:** the cell painting fits a level camera exactly: `Level(1.55, 803.0, 1000.0, cx=540)` (eye 1.55 m, back wall at d 3.39 m: the bed's near end lands on the painted one within 10 px). Door in the right wall at x ~1.05, d 1.55-2.6. Brand starts in the doorway (1.0, 2.1) mid-stride, 'stroll' to (0.15, 2.35), side on facing left (yaw -90), stops ~23.8; snaps to yaw -30, looks round numbly with `head_yaw` (left 24.1, gaze up to the window 24.7, back down 25.2), eased. Officer one step behind and nearer the lens (x + 0.45, d - 0.25), same gait, his near hand ('L' facing left) on Brand's near upper arm; lets go at the stop and stands by the door. Marks: (Level.p(x, d), Level.ppm(d)); replace STAGE['cell'] guesses.
- **cot:** `lying.lie(sp, 'side', x, z, yaw, ground=0.45)` drawn with `lying_flat.draw(img, cam, k, sp, t)` (the house-style lying body). The 3D camera for the cot close-up (cell painting at B.Cam(1.55, 330, 1240)): `sets.Cam((0, 1.55, 0), (0, 1.55, 1), focal=1550, shake=(325.5, -677.35))`. Mattress top 0.45 m, x -1.05 to -0.25, d 1.39 to 3.39, pillow at the far end: head on the pillow (~d 3.1), knees towards us. Weeping face and tears; a sob every ~0.9 s (shoulders, neck, head nudged up 0.5 cm and back). Run `lying.contact_faults`.
- **phone:** keep `handset_pose`; lean 5, head down (head_dy +8, gaze down); a slow head shake (+-10 head_yaw over 1 s) on "at all right now"; free hand limp.
- **tvroom / push:** slouched (lean -6, head_dy +6) while the eyes drift up; on 'amazed' (eyes and face snap) he sits up over 0.6 s eased (lean 0); on 'overjoyed' lean forward 6, head up.
- **gates:** split into 'gates' (wide, ST.GATE camera, a slow push 1.0 to 1.35 on the door) and 'gates2' (a closer B.Cam on the same painting, centred on his mark), the cut at ~50.05 (after "Blessed!"). Wide: he steps out of the wicket door (x 0.15-1.15 at d GATE_D + 0.37) in the first 0.8 s and flings his arms wide ON "Blessed!" (hands go out to the side on the way up: figure-rig 3's waypoint). gates2: he strides the last steps into his mark (d 6.0 to 4.6) arms wide, stops, a double pump of the arms on "everybody!", holds. Add to SHOTS, VIEW, SHOT_CAST.
- **Checks to add:** each touch in TOUCHES (officer's hand, gavel, Bible, handset), the lying body's contact faults; `blessed.py check` clean; stills of every shot's first and last frames before the clips.

## The questions asked (kept for the record)
1. Budget: **Lean, about 15%** (pick) or Full as written, about 19%. 8-12% is not reachable for this script without cutting a scene: it has 8 places and 7 people (MidTerminal, 11%, had 1 room and 3). Lean keeps every line and beat; the van and TV room become close-ups on Brand against dark, simple backgrounds; the cell and phone share one prison painting; the TV-room inmates are silhouettes.
2. The gavel: English judges never use one. **Keep it** (pick: it reads at once and Brand's line answers it) or no gavel (the judge just says the sentence).
3. Sex offenders were left out of the real early-release schemes. **Keep the joke as written** (pick: it is the satire) Y/N.
4. The judge: **an invented red-robed judge** (pick), not the real judge's face. Y/N.
5. The TV: **BBC News look with "BBC NEWS" lettering** (pick; parody) or an invented channel.
6. "everybody!" at the gates: **the same press pack waiting outside** (pick, reused) or an empty street.
7. "Usual attire" at the gates: **his trial look: dark jacket, open white shirt, crucifix, sunglasses, long white scarf, hair loose** (pick); prison: grey tracksuit, hair in the topknot from the sentencing sketch.
8. Line 1 tone: **sincere showman** (pick: believes his own performance, lowers the sunglasses, hand on heart) or a wink to camera.
9. Line 3 "doesn't feel very blessed": **quiet, to himself, deadpan** (pick) or said up to the judge.

## How Brand moves (before the scandal; one search pass, 11 Nov)
Sources: LA Times, Chris Lee, 14 Jun 2008 (Roxy show: "louche, preening British rock star", "Jagger-esque rock star
charisma", "exaggerated pantomime moves", "neurotic twitchiness", "looked up to face the capacity crowd"); The Comic's
Comic, 22 Jul 2008 (NYC debut: "slithering, crouching and twirling about onstage, his sprawling updo of hair flowing and
bouncing behind him"; walks out into the audience for crowd work; "I'm not Christ"); Guardian, Brian Logan, 20 Sep 2021
("charismatic and animated as ever", "sells it with brio"); The Times, Dominic Maxwell, 2021 ("does he believe he's the
Second Coming?", "he owns the stage").
1. **The swagger:** a rock-star strut, chest out, leaning back a touch, a loose sway of the head and shoulders over
   each step, a long easy stride. (Built: the 'swagger' walk, 108 steps a minute, with a head roll per step.)
2. **Big open-handed gestures:** whole arms, hands open, flung wide; pantomime, never small. (Built: arms open at
   shoulder height on "super"; up and open on "Blessed!".)
3. **The dip:** drops at the knees on the punchline and springs back up. (Built: on "super" and on "everybody!".)
4. **Goes to the crowd:** leans in close to people. (Built: leans in to the scrum on "mate", head tilted.)
5. **Preening:** chin up, looking up and out at the room. (Built: chin up on "super", "Blessed!" and each "blessed"
   in the oath.)
6. **The messiah joke:** arms out, palms open, the Second Coming. (Built: the gates' "Blessed!".)
7. **Twitchy underneath; hair bouncing:** not built (the hair has no bounce in our kit; small fidgets would muddy the
   held poses on phone-sized frames).
The showman is the arrival, the oath (held in: bolt upright, only the chin lifts) and the gates; prison has none of it.



## Where things stand before chat 3 of 8 (12 Nov)
- **Rules that bite next:** 67 (one full pre-flight, then the check sheet with the Hook Text frame), 13 (SET_FEET missing), 59.
- **Done (12 Nov, chat 2 of 8, Sonnet):** Bible bigger with a pale edge; ink-edged sleeve on the heart-hand; phone eyes open, looking down (new 'phone' mood). One full pre-flight run (9 min): picture checks clean; the rest is named below. Check sheet `notes/sheets/blessed-check-sheet.jpg` and Hook Text frame `notes/sheets/blessed-hook-frame.jpg` sent to Sam.
- **Needs Sam (12 Nov, he said YY):** chat 3 of 8 is Opus high: build the missing checks FIRST (see Next). Then Y or N for animatic 1 (about 5 min to render; needs `--faults-named`). Also a look at the jury clip and the movement clips.
- **Next: Opus, high effort.** Type: "Blessed: write the missing checks (SET_FEET and movers, scene(t) for the audit, LINE_SUBJECTS, pupils clipped to the eye, camera plan for the shots with none, newsreader mouth at 50.8 s); fix every fault they find; one full pre-flight; then the sheet." Animatic 1 waits for a new Y.
- **Read:** `guides/job-packs.md` Checks and animatic; this section.
- **Open rule requests:** none.
- **For Claude (chat 2):** named, not fixed (no speech-to-text here to re-time): subtitle timing off 0.4-0.8 s on lines 2, 4, 5; newsreader line 5 recording has ~3 more syllables than the script at 10.4 s (listen); newsreader mouth shut 50.8-51.7 s; six captions too fast (lines 2, 5); no SET_FEET/audits/LINE_SUBJECTS/scene(t) (template gaps); pupils not clipped (S5). Figure-guard arm lines are 'allowed'. Older notes: the --text run (48 faults) shows "SHOT CAST: never on screen" for every shot: the text mode draws no frames, so judge it from the full run. Named, not changed (hunt 2): the oath Bible is small at phone size; at the phone his eyes read shut (head down, tearful); hand-on-heart forearm merges with the jacket (same grey). Still open from chat 10: newsreader mouth still at 50.8 s ("stop overcrowding"), fast captions (lines 2, 3, 5), SET_FEET/movers/SET_CAM (rule 13), no court_jury rows in SET_BOXES/BENCHMARK (rule 83/3), pupils not clipped to the eye in blessed_cast (S5). Ledger fixed by hand: the hunt 2 pack reused folder r1-p1 and `record` overwrote hunt 1; both passes restored in notes/ledger/blessed.json. Hunt 2 spec in the scratchpad was not kept.

## Chat 3 (12 Nov)
- **Rules that bite next:** 59 (the 17 picture faults below are fixed or named before any animatic), 67 (one full pre-flight, about 15 min now), 85 (chat 3 stopped on budget: about 3.3% of a week against Sam's 1-1.5%).
- **Done (12 Nov, chat 3 of 8, Opus):** every missing check built and wired in (`blessed_checks.py`): where everyone stands in metres (collisions, who is on screen), each body alone over its frames (pieces, pops, frozen), line work, walking against the set's solid things in the three walking shots, a camera in the plan for every shot, eyes measured (pupils stay inside), tears and TV light as effects (HAS now has effects), the jury, van and gate sets in the overlap list, the jury box benchmarked. Faults they found, fixed: newsreader line 5 now ends where she is last heard (the "mouth shut at 50.8 s" and "3 extra syllables" faults were the faded part of the take); six too-fast subtitles given room (pieces up to 0.3 s early); stubbled jaws re-inked; a journalist moved off the gate sign's edge; jury SHOT_CAST is the ten jurors in frame (1 and 6 sit outside it). Kit: setcheck takes a set per shot (kittest `moving_figures_per_shot`) and its own `set_movers` (it clashed with viewchecks' `movers`). Quick check clean. One full pre-flight (14 min 46 s): 17 faults, none fixed (budget stop). Check sheet `notes/sheets/blessed-check-sheet.jpg`, Hook Text frame `notes/sheets/blessed-hook-frame.jpg`; full list `notes/ledger/blessed-preflight-chat3.txt`.
- **What the checks found (plain):** the earlier "picture checks clean" was not the whole film: with the checks switched on, 17 picture faults show. Hands: journalists' and Brand's hands hidden at times (van, press seen from behind), his hand off the Bible at the start and end of the oath, shoulder seams on his arms in the arrival, the officer's grip not listed as meant. The cot: he lies on his back, head away, so his face cannot be drawn right (rule 42). Cuts: arms drop back to rest just before three cuts (rule 72). The judge holds dead still 2.5 s in both oath shots. The famous-face size check never found Brand (name mismatch), and the turnaround sheet was skipped (no PEOPLE entry): two more checks not running.
- **Needs Sam:** Y to spend about 1.5% more to fix the 17 and render animatic 1 (my pick), or N to stop.
- **Next: Opus, medium effort** (fixes from a clear list). Type: "Blessed: fix the 17 pre-flight faults in notes/blessed.md Where things stand, then ONE full pre-flight, the check sheet with the Hook Text frame, and animatic 1. Read CLAUDE.md, then notes/blessed.md Where things stand."
- **Read:** `guides/job-packs.md` Checks and animatic; `guides/satire.md` "If a check fails"; this section.
- **Open rule requests:** none in the notes. (Sam's pre-flight "never clean while a check is skipped" change sits in the system audit job, `notes/system-audit-12-nov.md`.)
- **For Claude (chat 3):** the 17 (txt above): HANDS journalist R arm covered (arrive, gates2: from behind, likely name in an allow-list with why); Brand L arm holds hidden 2.00 s; rule 81 shoulder lines 2.17, 3.08; oath hand off the Bible 4.83 (1.1 hand-widths) and 13.75; van R hand covered (clasped); escort officer's hand over Brand (the grip: list it as a touch); POSE cot (lying.lie 'side' reads as back, head away: turn him to face the lens, COT_AT yaw); CUT rests 4.25 journalist L, 14.00 Brand L (oath arms-down plan), 48.50 journalist R (hold or CUT_RESTS_OK with why); FACES: FAMOUS=['brand'] but drawn name is 'Russell Brand' (kitchecks.faces); judge frozen (give put_seated judge small shifts or head life); turnaround sheet skipped: no PEOPLE entry. blessed.py is 1,182 lines (rule 61 warning: split the shots out). Sheets' Hook frame: frame_image(1.0) + hook_text.card. Cost read: costwatch.read_usage on this chat's transcript, $9.63 = 3.3%.

## Archived 12 Nov (chat 6)
- **Done (12 Nov, chat 4, Opus):** the 17 pre-flight faults answered; quick check clean. Fixed: the Bible now moves with his hand (it floated off it on the way up) and he holds the oath pose to the cut (rule 72); the judge shifts his weight and head (was dead still 2.5 s); FAMOUS uses the drawn name; each journalist has their own name (the cut check had pooled them all as one 'Journalist', the likely cause of 2 of the 3 cut faults) and a turnaround entry. The cot: lying curled from this camera drew his face upside down (looked at full size, rule 42; every lying angle tried was off the bed or out of frame), so he now SITS on the cot's edge, weeping at us, sobs heaving his shoulders. Named as meant (HANDS_OK, each looked at full size): journalists' hands under their raised kit (arrival, gates); his hand-on-heart sleeve edge; the shoulder "seams" are his hair over the shoulders; van hands clasped; the officer's grip.
- **Needs Sam:** at the check sheet: the cot change (Lost: curled up lying on it. Added: sitting on its edge, weeping at us).
- **Done (12 Nov, chat 5, Sonnet):** quick check clean; ONE full pre-flight run (12 min): 1 fault, HANDS: oath 4.83 s, Brand's left arm, the Bible hand is hidden (22% shows). The critique's second pass also fixed 6 faults itself (aviator lenses, wider gates, HM PRISON sign, phone gaze). No pass stamp, so no animatic yet.

## Where things stand (the ONE handover)
- **Rules that bite next:** 67 (one full pre-flight, about 15 min), 59 (every fault fixed or named before the animatic), 14 (the check sheet with the Hook Text frame, then wait for Sam's clear yes).
- **Done (12 Nov, chat 6, Sonnet):** oath hand fixed; animatic 1 rendered (full size by mistake: 31 min; rule now in guides/satire.md: animatics are always `--small`), finished at 1.1x and sent (`review/blessed-animatic-1.mp4`, 8.7 MB, off GitHub as a draft). Rules written (Sam's Y): no check sheet unless asked (CLAUDE.md); animatic = `--small` (satire.md); the pre-flight audit job is below. Sam's round-1 notes 11-26 logged in the table, none fixed yet.
- **Next: Opus, medium effort (chat opened 12 Nov): notes 11-24 and 26.** Order: the mouths first (13, 15: find why the judge has none and note 5's fix never reached him, rule 30), then the body faults (14, 16), front-on Brand (13, 17, 21, 26), the sets (12, 17, 20, 22, 24), the despair shot from above (18), the zooms (23). Clips of the changed moments (`final OUT --small --span T0 T1`), no full animatic until the clips look right; then a Sonnet chat for checks and the animatic. Note 25 (Walliams) waits for Sam.
- **Needs Sam:** 1 Walliams (note 25): B (pick) / A / C; 2 front-on scope (note 26): Y (pick) / N. Note 19: if his recording differs from "Yeah, love. I'm just not feeling very...blessed right now.", he re-records.
- **Spent:** stage animatic1 about 7.2% against 2% (Sam said Y to go on); round 1 of 2 notes rounds starts now.
- **Follow-up tool fix (not done):** `kitchecks.faces` on an incremental run must not report from partial frames (keep the last full run's best face size in blessed-frames.json). Audit job after Blessed's last round (below).
- **Read:** `guides/job-packs.md` Checks and animatic; this section.
- **Open rule requests:** none.
- **For Claude (chat 4):** cot = put_seated at COT_MARK/COT_YAW, cot_pose (blessed_checks.placed updated); oath: lift = _contact - OATH_BIBLE, dn0 = T['s3']+0.05; judge jj shifts; press_sp name 'Journalist N', turnhead.PEOPLE[who].sheet; HANDS_OK list after CUT_RESTS_OK. Stills checked at 4.75, 4.9, 13.95, 25.0. blessed.py over 1,100 lines (rule 61 warning, not a fault).



## Where things stand (chat 2 of notes round 1, archived 12 Nov)
- **Rules that bite next:** 30 (a repeated note: say why the first fix failed), 74 (moves against the acting list), 59 (every fault fixed or named before the animatic).
- **Done (12 Nov, notes chat 2 of 8, Opus medium, stopped on amber):** 16 van (clip sent; Sam laughed at the too-big seat on the way, fixed), 18 cot from above (clip sent), 19 line, 27 music built, 26 front-on in the stills (arrival, oath, cell stop, phone).
- **Next: Opus, medium (chat 3 of 8):** clip the front-on arrival/oath/phone (0-4.5, 4.5-7.2, 27-33); then 20 phone room, 23 zooms (+ the music clip, 40-47), 22 TV room, 12 and 24 press, 25 Walliams, 15 framing, 11 camera, 17 sigh and blanket. Then a Sonnet chat for checks and animatic 2.
- **Needs Sam:** nothing.
- **Not merged on purpose:** claude/audit-honest-checker (joins after animatic 2).
- **Spent:** chat 2 about 1.2% of a week; round 1 of 2.
- **Read:** `guides/job-packs.md` Notes round; this section; the Notes rows 11-27.
- **Follow-up tool fix (not done):** `kitchecks.faces` on an incremental run must not report from partial frames.
- **Open rule requests:** none.
- **For Claude:** van: `_seat` draws both legs then the seat (j['hide_legs']), views.leg j['knee_round']; cot: ST.cot_top / cot_top_front, cot_pose, _cam 'cot'; music(): MUSIC_SAD_END/MUSIC_PEAK; front-on = yaw 0 in shot code (oath, phone, arrive, escort). Pre-flight not yet run on these (new view cot_top: SET_BOXES may need it).



## Handover (12 Nov, before chat 5's Walliams build)
- **Rules that bite next:** 24 (round 1 is over its share: 3.99% against 2.5%; wait for Sam's Y), 30, 59.
- **Done (12 Nov, chat 4 of 8, Opus medium, amber):** 11, 12, 24 (press pack, flashes, arrival camera), 15 (dock framing), 17 (sigh, blanket) coded and pushed; NO clips yet (renders failed: two at once). Chat 5 (12 Nov) stopped before any work: Sam switching account; nothing changed.
- **Next (Sam said Y): Opus, medium, chat 5 of 8, on Sam's new account (attach github.com/SamKearns22/Animation-, main line):** clips ONE AT A TIME, --small, check each log as it starts: gates 47.0-52.9, arrival 0-8.9, dock+cell 14.0-25.0; then 28 (HM Prison officer: white shirt, epaulettes, black tie, keys on a chain). Then a Sonnet chat: checks and animatic 2.
- **Needs Sam:** nothing (Walliams set aside by Sam; another chat may be building it: pull first).
- **Read:** `guides/job-packs.md` Notes round; this section; Notes rows 11-28.
- **Open rule requests:** none.
- **For Claude:** ST.press_spots(bx, bd, rows, seed, cx, half); press(part=('behind'|'front', d)) drawn either side of him; _stills kit + flash; CREW_TOP/LEG; ARRIVE_CAM; OUT = Level(1.7, 1090, 1500); _cam dock Cam(1.2, 548, 1560); gates Cam starts 1.3; T['cot'] = cell + 3.9; escort sigh keys; ST._blanket. A 5pm reminder (trig_0162nUpu9SadML1ei9zrWBP7) resumes only on Sam's Y.
## Replaced 12 Nov (r2 chat 1 of 8)

## Where things stand (the ONE handover)
- **Rules that bite next:** 49 (a new likeness pack first), 30 (note 29 repeats 25: read why the first fix failed), 24 (round 1 at 5.8% vs 2.5%; Sam's Y covers 29-30 only, about 3%).
- **Done (12 Nov, chat 5 of 8, Opus, amber):** first Walliams head and a separate shot; Sam's notes 29 (not recognisable, new references) and 30 (in the background of gates2, not a new shot) recorded with fixes.
- **Next (Sam said Y, 12 Nov): Opus, HIGH, chat 1 of 8 (a new likeness build):** 29 then 30, then one clip of gates2 (--small --span 49.4 53.6). The held chat 6 (Opus medium) is not used. Then the round-1 clips/animatic 2 as Sam answers.
- **Needs Sam:** nothing (Y, 12 Nov: go on past round 1's share to fix 29 and 30, about 3% more).
- **Read:** `guides/job-packs.md` Build (people, critique); rule 49; Notes rows 25, 29, 30; this section.
- **Open rule requests:** none.
- **For Claude:** blessed_walliams.py (P4 'walliams', TUNE; MOODS scared/alarmed; FACE_HEADS hook). blessed.py: T['wal'], WAL_LEN, wal_* functions, _door_clip, parted, draw_walliams: re-use the grip and door clip inside gates2's drawing, remove the 'walliams' entries from SHOTS/VIEW/SHOT_CAST/_cam and set DUR back. Brand's gates2 mark: ST.STAGE['gates']['brand'] = _mark(GATE, 0.6, 7.6) and G2_FROM/G2_TO in blessed.py.

## Replaced 12 Nov (r2 chat 1, second)
## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (Walliams' new head has had no fresh-eye critique: one before animatic 2), 30 (note 28 the officer; 26's unclipped shots), 24 (round 1 well over its share).
- **Done (12 Nov, chat 1 of 8, Opus high, branch claude/blessed-notes-r2):** notes 29 (new likeness from Sam's 5 photos), 30 (Walliams in gates2's background, no shot of his own, film 53.57 s), 31 (gates2 pushes in on the pack); checks clean; clip blessed-r2-clip-gates2.mp4 sent.
- **Next (on Sam's Y to the clip): Opus, MEDIUM, a new chat (chat 2 of 8):** the fresh-eye critique of Walliams' head (rule 89), note 28 (HM Prison officer), note 26's clips (oath, phone, arrival) and note 27's music clip; then animatic 2 (Sonnet).
- **Needs Sam:** a look at the gates2 clip.
- **Read:** `guides/job-packs.md` Notes round; Notes rows 26-31; this section.
- **Open rule requests:** none.
- **For Claude:** blessed_walliams.py (new card, TUNE nose_long -1.5, beard() is now stubble, long_nose()). blessed.py: T['wal'] = gates2 + 0.5; G2_X -1.0, G2_PART, G2_PRESS (the pack opened left in gates2 only; ST.STAGE['gates']['brand'] kept, it places gates2's camera); _cam 'gates2' push; draw_walliams() drawn first in gates2. Photo sites are blocked in the Default environment (create/update_environment refused 12 Nov): ask Sam for photos.

