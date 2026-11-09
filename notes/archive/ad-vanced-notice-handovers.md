# Ad-Vanced Notice: old handovers

## Where things stand
- **Rules that bite next:** 51 (Vance likeness pack before drawing), 40 (showstopper list approved before building), 74 (acting list)
- **Done (7 Nov):** plan and Sam's answers; the network now allows Wikimedia (I fetch photos myself); cast sheet sent (Vance passes the likeness check; the driver; anger scale 1-6).
- **Next:** Sam's yes on the cast and his anger number; then place photos (Musandam cliffs, tankers, gas station, pickup, study) and the composition sheet (rule 11).
- **Needs Sam:** the rest of the script (reworked for an earlier joke); Vance cartoons he likes; Hook Text wording later.
- **Read:** `guides/satire.md` (Start; Getting it right first time), `guides/kit-catalogue.md` (Flying Whales sea and effects).
- **Open rule requests:** none (rule 77, the beard tool first, written 7 Nov on Sam's yes).
- **For Claude:** cast `source/ad_vanced_notice_cast.py` (sheet / faces / head); likeness card `references/ad-vanced-notice/vance-card.json`; Wikimedia: API with a User-Agent, 1 request per ~6 s (429s otherwise); kit: `views.leg` takes `leg_k` (heavier legs). Film will be `source/ad_vanced_notice.py` (from `source/satire_template.py`). Reuse: `flying_whales_sea.py` (sea painting, re-lit for a hazy noon), `flying_whales_fx.py` (fireball, Puff smoke, fire tongues, splashes, chunks, holes), `flying_whales_wreck.py` (pieces thrown, falling, splashing; freeze and jolt on the hit).

## The film so far (the script continues; about 24 s so far)
1. **Study, front on, medium** (about 4 s). Vance behind the desk, sincere and confident. Bookcases behind, fireplace crackling on the right, crystal glass of water on the desk, US flag draped over the desk's left side. Line 1.
2. **Omani cliffside over the Strait of Hormuz, locked wide** (about 11 s, the showstopper included). The strait to the horizon, far shore a grey smudge, a flotilla of still tankers; the nearest one sails to the right with a wake. Vance walks calmly towards the camera, eyes to the lens. Line 2.
3. **Showstopper, same camera** (Sam, 7 Nov: answer 5 = 2): the cliff shot holds; Vance keeps walking towards the lens, unaware, as the missile hits the tanker behind him. No line.
4. **Close-up of Vance** (about 3 s), the burning wreck on the sea over his right shoulder (screen left). Line 3.
5. **Midwest gas station** (about 7 s). The big man by his 4x4, pump in hand, glaring up at the price board (Diesel $6.15). Vance walks in from the right, arm round him. Lines 4-6.

**Jokes early (tiktok-design):** the first laugh lands at about 11 s (the explosion, then "None of this is my fault"), later than the 5 s aim. The Hook Text and the sincere "Hello, America" carry the opening; question 2 offers a trim.



## Where things stand (archived 8 Nov, before the arms job)
- **Rules that bite next:** 3 (each place's list ticked against our set, `benchmark.py`), 39 (flat paintings, one per camera, no 3D), 40 (showstopper list ticked at the first rehearsal clip)
- **Done (7 Nov):** composition approved (Sam: 1-4 yes); shirt check runs to every edge (note 12); prices set to peak war prices (note 13).
- **Next:** fresh chat, Opus high effort. Type: "Ad-Vanced Notice: join the arms to the shoulders (note 14, all films), then build the sets. Read notes/ad-vanced-notice.md".
- **Needs Sam:** his number on rule proposal R1 (arms one piece with the body); the rest of the script; the Hook Text wording later.
- **Read:** this file (notes 12-14, answers, references, composition); `guides/figure-rig.md` (arms); `guides/kit-catalogue.md` rows for sets.py, the Flying Whales sea and effects.
- **Open rule requests:** R1 (below the notes), not yet written.
- **For Claude:** arms: `burnham.arm` (old tube), `limbs.py` (`install`, the one-outline shoulder: no effect on these figures, find why), torsos via `patriots4`/`TC.TORSOS`; test `review/adv-arms.jpg` (top: off, bottom: on). Sets: one module `source/ad_vanced_notice_sets.py`; cliff reuses `flying_whales_sea` re-lit (patch SKY/SEA/CLOUDS/CAM, sun off frame, `_caps` off; camera 61.6 m up, pitch -8, focal 1400, horizon about y 760, plateau edge 12 m out, Vance's mark 2.6 m, near tanker 1.2 km); comp layout and the `PLACES` lists in `source/ad_vanced_notice_comp.py`; BENCHMARK and PROP_SIZES go in the film file (from `satire_template.py`).


## Where things stand (archived 8 Nov, before the arms job)

## Where things stand (archived 8 Nov, after the arms job)
- **Rules that bite next:** 3 (each place's list ticked against our set, `benchmark.py`), 39 (flat paintings, one per camera, no 3D), 40 (showstopper list ticked at the first rehearsal clip)
- **Done (8 Nov):** arms joined to the shoulders in the shared kit, every film (note 14); side-view legs stand straight (15); relaxed elbows bend a touch outward, matched to Sam's rest photos (16, 17); no tufts inside a lifted, bent elbow (18). Before/after sheet sent in chat (kept off GitHub, as a test picture).
- **Next:** fresh chat, Opus high effort. Type: "Ad-Vanced Notice: build the sets. Read notes/ad-vanced-notice.md".
- **Needs Sam:** any notes on the before/after sheet; the rest of the script; the Hook Text later.
- **Read:** this file (Where things stand, references, composition); `guides/kit-catalogue.md` rows for sets.py, the Flying Whales sea and effects; `guides/figure-rig.md` 2-3 only if Sam has arm notes.
- **Open rule requests:** none (R1 written as rule 81, 8 Nov).
- **For Claude:** sets: one module `source/ad_vanced_notice_sets.py`; cliff reuses `flying_whales_sea` re-lit (patch SKY/SEA/CLOUDS/CAM, sun off frame, `_caps` off; camera 61.6 m up, pitch -8, focal 1400, horizon about y 760, plateau edge 12 m out, Vance's mark 2.6 m, near tanker 1.2 km); comp layout and the `PLACES` lists in `source/ad_vanced_notice_comp.py`; BENCHMARK and PROP_SIZES go in the film file (from `satire_template.py`). Arms: `limbs._who` (unwraps Lean/Tilted/Mirrored; body kept in screen pixels), `limbs._fillet`, `views.standing`, `views.knee_of` lock; sheet script was a scratch file (4 casts x front, side, arm lifted; old code from a git worktree).

## Handover before the showstopper (8 Nov)
- **Rules that bite next:** 3 (each place ticked against its photos: `benchmark.py ad_vanced_notice_sets`), 40 (showstopper list ticked at the first rehearsal clip), 54 (only deck pieces and the funnel top break off; the hull stays whole)
- **Done (8 Nov):** arms joined to shoulders in the shared kit (notes 14-18, another chat; rule 81). All four sets built as flat paintings at real size, plus the tanker and pickup props (notes 19-20); Sam's first set notes fixed (21-25: shot 2 35% closer, headland and tree out, road to the edge, chair glitch, grain bins). Sheets and clip re-sent.
- **Next:** fresh chat, Opus high effort (the showstopper is new building). Type: "Ad-Vanced Notice: build the showstopper. Read notes/ad-vanced-notice.md".
- **Needs Sam:** nothing on the sets (Y, 8 Nov: notes 20-25 stand; the thorn tree is in reserve, its code is in commit eab160d, `_thorn_tree`); any notes on the arms sheet; the rest of the script; the Hook Text later.
- **Read:** this file (Where things stand, the showstopper list, notes 19-26); `guides/kit-catalogue.md` rows for the Flying Whales effects and the Ad-Vanced Notice sets.
- **Open rule requests:** none (R1 written as rule 81, 8 Nov).
- **For Claude:** sets in `source/ad_vanced_notice_sets.py` (MAP at the top; `BENCHMARK`, `PROP_SIZES`, `SHOTS`, `picture(t)` there for benchmark.py/sheet.py; the film file imports them). Study: `study_back(t)`, `study_pose(j)` (no kit chair or desk; desk top drawn between body and arms), `study_front()`, Vance at `STUDY_VANCE`. Strait: `strait(which, t, near=('sail'|'wreck', x), fx=fn)` (fx draws effects between the ships and the cliff top), `near_x(t, t_hit)`, `X_HIT`, `place_cliff`, `cliff_shadow`, cameras `CAMS`. Gas: `gas_back()`, `gas_front()`, `place_gas`, `MAN_X`/`VANCE_X`, `gas_points()` (filler, hose_from, board box for KEEP_CLEAR). Effects: `flying_whales_fx`.



## Where things stand
- **Rules that bite next:** 40 (street elements: wait for Sam's yes before building), 83 (the street's SET_BOXES), 74 (line 9's acting)
- **Done (8 Nov):** note 44: Vance's turned faces from his own front design (`turnhead.py`), the swivel's turning frames back; street elements approved and questions 21-25 answered (no SUV, shopfronts, snow).
- **Next:** fresh chat, Opus high: references (Lake Street shopfronts in snow, ICE raid gear) ticked as lists, then build the street (set, SUV, four officers, the curled man via `lying.py`, the beating via `moves.punch`/`kick`, blood, push in); then the check sheet and animatic 3 (Opus medium).
- **Needs Sam:** OK on the made-up shop signs; recordings of lines 1-9.
- **Read:** this file (Where things stand, note 44, Street elements, Acting line 9, Sam's answers 21-25); `guides/kit-catalogue.md` people rows (Met officers in `power_crime_cast.py`, `lying.py`); rulebook 40, 74, 83.
- **Open rule requests:** none.
- **For Claude:** Vance's turned heads: `ad_vanced_notice_cast.vance_turned` + `VANCE_PROFILE` (hooked into `V.head_view`); sheet `ad_vanced_notice_cast.py turn OUT`; the film's `study_j` uses the kit swivel again. The street goes in `ad_vanced_notice_sets.py` (new place) and `ad_vanced_notice.py` (shot after `gas`).

