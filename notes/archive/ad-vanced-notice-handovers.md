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
