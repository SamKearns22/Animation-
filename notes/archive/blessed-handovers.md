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
