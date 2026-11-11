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

