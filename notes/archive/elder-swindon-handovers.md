
## Where things stand
- **Rules that bite next:** 8 (rehearse the dog and the zoom-out, the scroll reveal, the title burn as short clips first), 3 (roundabout benchmark against Sam's two photos), 39 (3D only for the scroll and can).
- **Done (8 Nov):** plan; answers 1-9; teaser stills; the Staffie added; composition sheet sent and approved (Sam: "Y to all": glowing burn-in on SWINDON, the man stays out cold, brindle Staffie); lying.py's `lie` mended.
- **Spent against the estimate:** 6.0 of 9.0 (ground 1.2, scroll 0.6, can and packet 0.4, face 0.5, dog 0.5, zoom-out 0.6, roundabout 1.1, traffic 0.7, title 0.4); nothing over yet.
- **Next:** build, Opus high, NEW chat: "Build Elder Scrolls Swindon – read notes/elder-swindon.md". Order: rehearsal clips (dog + zoom-out, scroll reveal, title burn), then the film from the template, check sheet, animatic offer.
- **Needs Sam:** nothing until the rehearsal clips.
- **Read:** this file (Plan, Showstopper, Brief); guides/satire.md (Start, One set, Render); kit-catalogue (Effects).
- **Open rule requests:** none.
- **For Claude:** comp `source/elder_swindon_comp.py` (cams `orbit`, `topcam`; props `lying_rev`, `scroll_mat`, `can_mat`, `packet`, `drool`, `dog`; `aerial`, `title`); ground `source/elder_swindon_ground.py`. Film: `source/elder_swindon.py` from the template, `HAS = {'people','effects','props'}`, sound `music/sentinel-teaser-audio.m4a` as is. Face close-up needed (lying.draw's face reads poorly face down). Can label reads "RT LAGER" at its end: fix the wrap.



## Handover before the merge (8 Nov)
- **Rules that bite next:** 8 (rehearse risky moves as short clips before building), 59 (no animatic or final without a clean pre-flight; Sam skipped it for animatic 1, the hang must be fixed first), 67 (one full pre-flight per round).
- **Done:** film built from the template (all six shots, traffic, title burn, dog, face close-up); rehearsal clips sent; animatic 1 sent (31.6 s, trailer's sound, Hook Text, sign-off, rendered with `--no-lock`); Sam's notes 1-11 on animatic 1 saved below.
- **Spent against the estimate (rule 55):** 6.0 of 9.0; nothing over yet. Sound: the trailer's sound stays; Sam's private test post on his own profile is his call (his question, 8 Nov).
- **Next:** Opus, medium effort, NEW chat: "Build Elder Scrolls Swindon – read notes/elder-swindon.md". Order: fix notes 1-11 in one round (clips first), fix the pre-flight hang, full pre-flight, check sheet, animatic 2 offer; wait for a clear yes.
- **Needs Sam:** Y/N early evening (notes 11); Y/N the scroll's gold glow (note 9, a deliberate house-style exception); the private test post result (decides the sound route).
- **Read:** this file (Where things stand, Brief checklist, Notes on animatic 1); guides/film-quality-rules.md (rules 8, 59, 67); guides/satire.md (Before every render, Render).
- **Lost / Added:** Lost: the CLOSING DOWN sign (note 1). Added: scroll glow, shopping bag, early evening (pending Y).
- **Open rule requests:** none.
- **For Claude:** `source/elder_swindon.py` (cam_for, man_at, face_close, dog_at, draw_dog, draw_packet, near_real, aerial_flat, _estate, traffic, title, burn, scene, checks); ground in `source/elder_swindon_ground.py`; composition in `source/elder_swindon_comp.py`. Animatic: `python3 source/elder_swindon.py final OUT.mp4 --small --no-lock`, then `source/finish.py`. Frames memoised in `~/.cache/filmcache/elder_swindon-memo/`. Pre-flight hang: workers freeze (futex, libgomp) after frame ~332 (gdb: idle semaphore waits); numpy linalg calls removed from the drawing, not yet fixed; try `OMP_NUM_THREADS=1` and a worker-free run first.



## Where things stand (8 Nov, before notes 1-18)
- **Rules that bite next:** 56 (a fault of a kind: every mini, every sign), 59 (no animatic without a clean pre-flight; fix the hang), 67 (one full pre-flight per round).
- **Done:** animatic 1 sent; Sam's notes 1-11, then 12-18 (shot-6 people and vehicles, framing, the sign) saved below. A duplicate build from another chat merged out (see "More notes").
- **Spent against the estimate:** 6.0 of 9.0 (plus about 1.4 for notes 12-16 if Sam agrees).
- **Next:** Opus, medium effort, NEW chat: "Fix Elder Scrolls Swindon notes 1-18 – read notes/elder-swindon.md". Order: notes 1-18 in one round (clips first), the pre-flight hang, full pre-flight, check sheet, animatic 2 offer.
- **Needs Sam:** Y/N early evening (note 11); Y/N scroll glow (note 9); Y/N people drawn up to 4 times real size in shot 6; budget about 10.4%.
- **Read:** this file (Where things stand, Brief checklist, both "Notes on animatic 1" sections); guides/satire.md (Before every render, Render).
- **Lost / Added:** Lost: the CLOSING DOWN sign. Added: scroll glow, shopping bag, early evening (pending Y); people up to 4x size (pending Y).
- **Open rule requests:** none.
- **For Claude:** `source/elder_swindon.py` (cam_for, aerial_flat, _estate, traffic, title, burn, scene, checks); shot-6 extras to port in `source/elder_swindon_extras.py`. Animatic: `python3 source/elder_swindon.py final OUT.mp4 --small --no-lock`, then `source/finish.py`. Pre-flight hang: workers freeze after frame ~332; try `OMP_NUM_THREADS=1` and a worker-free run first.
