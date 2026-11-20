# Proposal: One route to the current kit

Status: open

## Problem
Sam (20 Nov, his words): "there should be one route to the right kit, the best kit, the most updated kit, and you
shouldn't be able to find all of the previous kits from previous films because they're done now ... it worries me
when you're using things that are outdated. So is it a case that the outdated things should be completely isolated or
deleted now? And should this be the case throughout the project, not just in this case?"

What went wrong: Grand Theft Autism's cast sheet broke the body rules (stuck-on short sleeves, square shoulders, tops
not tapering, Lucia on a man's box body). One cause: the short sleeves were MidTerminal's one-person patch for
Epstein's polo (a rectangle laid over a bare arm), live inside every kit person because loading the people kit loads
old film files, which replace the kit's own drawing steps. A chat building a new film cannot tell, from the kit,
which parts are the current, rule-meeting way and which are one old film's patch. Two constraints: every finished
film must still be able to re-render (Sam may ask for a recut), and the kit's tests replicate finished films (Blessed)
to prove the kit still draws them.

## Facts
Measured 20 Nov by this chat (scripts and import map in notes/proposals/one-route-kit/measure/: graph.py builds the
map from every `import` in source/, reach.py follows it, patches.py finds files that overwrite another file's parts).
- source/ holds 266 code files (93 MB with sound and data). By name, 153 belong to one film, 117 are tools or kit.
- 52 of the 117 kit/tool files load a film's file directly. The two most-loaded files in the project are finished
  films: burnham.py (the film "Hope Again", loaded by 124 files) and ed.py ("An Honest Chat", 110). Others used as
  kit: mossad.py and mossad_audio.py (Mossad), peepee.py (The Patriots), burnham_film.py, traitors_cast.py,
  midterminal_cast.py, ad_vanced_notice_cast.py, patriots3_cast.py, patriots4_cast.py, prepper_cast.py.
- Following the loads, the people kit (people.py), the places kit (places.py), figure.py and views.py can each reach
  113 files, 40 of them old films' files. Grand Theft Autism's code reaches 43 old films' files.
- What actually loads when Grand Theft Autism's cast file starts (checked by running it): ad_vanced_notice_cast,
  burnham, burnham_film, ed, midterminal_cast, mossad, mossad_audio, patriots3_cast, patriots4_cast, peepee,
  prepper_cast, traitors_cast.
- Run time check (gta_cast loaded, then each kit function compared with where it now comes from): 15 of the kit's
  basic drawing steps are replaced by old films' code while a Grand Theft Autism person is drawn:
  views.arm -> ad_vanced_notice_cast.arm; views.person -> midterminal_cast.person; views.head_view ->
  turnhead.head_view; views.torso_view -> ad_vanced_notice_cast; views.leg -> patriots3_cast._leg; burnham.head /
  face / mouth / torso / hair_front / beard -> mossad; burnham.hair_back -> patriots4_cast; burnham.arm and legs ->
  limbs; burnham.gesture_hand -> satire_style. Each replacement keeps the one before and adds to it (a chain):
  e.g. midterminal_cast.py lines 454-498 keep the old views.arm and add Epstein's short sleeve, and people.py lines
  496-498 switch that sleeve on for "sleeves short" (added for Grand Theft Autism, 20 Nov).
- 117 files overwrite at least one part of another file when they load (233 overwrites; most are one setting,
  burnham.SS, the drawing scale). So what a kit function does depends on which film files happen to have loaded,
  and in what order.
- All 41 finished films' main files still load without error (import test, 20 Nov). Unchecked: whether each still
  re-renders identically.
- kit-catalogue.md: 108 entries name a file; 67 of those files are one film's file. 7,481 words.
- kittests.py: 3,495 lines, about 100 tests; some import 20 film files (e.g. patriots3_cast, remakes_sets,
  traitors_cast) and replicate Blessed (`K.replicate('blessed', ...)`).
- Grand Theft Autism is paused until this is decided (chat 7 waits on Sam).

## Record
notes/grand-theft-autism.md
notes/proposals/one-route-kit/measure
guides/kit-catalogue.md
guides/job-packs.md
guides/film-quality-rules.md
source/people.py
source/people_parts.py
source/views.py
source/midterminal_cast.py
source/ad_vanced_notice_cast.py
source/kittests.py
source/catalogue.py
source/branches.py
