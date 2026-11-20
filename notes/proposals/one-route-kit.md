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

## Verdict (the judge, word for word)
<!-- verdict-hash: 30197d4a36257fd5 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V2 (helper A). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes: mild. No remedy is named, but the facts are built around the load map and the two constraints (recuts must work, the kit test replays Blessed), which points the helpers at "cut the kit's links to film files, keep recuts" before they weigh anything else.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 3 | 4 | 19 |
| V2 | 5 | 3 | 4 | 4 | 4 | 20 |
| V3 | 3 | 3 | 2 | 2 | 3 | 13 |
## Sam test
Q1: Yes. Freezing each released film at its saved version and keeping one live library with a boundary check is what an expert would do; the improved pick adds a "numbers may not rise" check at once, so the mess cannot grow while it is fixed.
Q2: Right scope: every finished film (one frame each from its saved version, against the posted video) and every kit file, not one cast sheet. Gap named: only two cross-film breaks are on record, so how often this hurt earlier films is unknown.
Q3: Root cause found with evidence (films rewrite shared drawing steps when they load; finished films re-render from the same live code, so their patches can never leave). Enforced by a check at the start and end of every chat and in the kit tests, not by a chat choosing to read. Known to work when the counts reach 0 and 41 of 41 films re-render.
Q4: Five approaches weighed across the versions (delete/hide, freeze by version, load wall, judge by the rules, learn first, numbered kits per film); freeze-then-wall is the best and the only one that keeps recuts.
Q5: Each change is its own yes and undone alone (all in git). The freeze is proven on all films before any kit step is moved; nothing is removed before the sheet shows what it does. Sam is not asked to trust anything unshown.
Q6: Checked here: 0 bookmarks (tags) in the project; local history is shallow (86 saves); people_parts loads ad_vanced_notice_cast, midterminal_cast and ed; the sleeve lines; Milburn's broken match; 123/102 files load burnham/ed by direct search; ledger 12.72% spent, 63.3% forecast. Unchecked: 12 of the 15 swaps, whether old saves re-render, all costs, 41 films (48 videos in animations/).
Q7: Sized by the result (kit-to-film loads 52 to 0, swapped steps 15 to 0, old films reached 40 to 0, catalogue film entries 67 to 0), about 12-14% of a week, honestly stated; no cheap trap such as patching the one sleeve.
Q8: Permanent; each posted film is frozen and moved out that day; reviewed at the next film's end against its notes and cost.
## Pick
V2
## Why
V2 is the only version that answers Sam's actual question for the whole project (old films isolated, one route to the current kit, the catalogue cleaned) in the right order: learn on all films, freeze, then cut. V1 proves only 3 of 41 films before cutting the kit (risk to recuts) and leaves the catalogue listing 67 old-film entries, so the "many routes" Sam saw stay. V3 fixes the one sleeve first (the symptom), moves patch behaviour into the kit as-is instead of rebuilding to the rules, and pins films only after it has started deleting their overrides, so finished films could break (as Milburn already did); it costs about 20%.
Taken in: from V3, the census as a "never rise" check at chat start and end, the most-used steps first (arm, person, torso, leg) so Grand Theft Autism can restart soonest, and finished films' files leaving the live folder (Sam's "isolate"). From V1, the reference cast (a man, a woman, short sleeves, a jacket) as the kit's proof against the rules, replacing "redraws Blessed exactly".
## Faults in the pick
- F1 [fixed] V2's guard refused only kit-to-film loads; a new film could still load an old film's file. Now any new work is refused.
- F2 [fixed] Old films' files stayed findable in the live folder; Sam asked for isolation. They leave it once frozen and no longer loaded.
- F3 [fixed] Nothing stopped new links forming during the work; the "never rise" count runs from the first change.
- F4 [fixed] Grand Theft Autism's wait was not addressed; the people steps go first and it restarts after them.
- F5 [named] The inherited sleeve was one of five causes of the cast sheet's faults; the main one (faults closed as "house style", body checks never run on cast sheets) is a separate proposal. This alone will not stop all body faults.
- F6 [named] Local history is shallow and no film has a bookmark; whether old saves re-render at all is unknown until the learning step.
- F7 [named] Costs and 12 of the 15 swaps are unchecked; the count of 41 films is the problem file's.
- F8 [named] A recut uses the kit as it was; later kit fixes must be carried across by hand.
## Final version
**Learn (changes nothing; Sonnet; about 1.5%).** Fetch the full project history. For each finished film, find the save its final came from, re-render one frame from that save in a separate copy, compare with the posted video. One labelled sheet of the 15 swapped drawing steps: each marked rule-meeting or one film's patch.
**Change 1, freeze (own yes; Sonnet; about 1.5%).** A bookmark per finished film and one recut command that draws it from that saved copy. The Blessed test reads its frozen copy. A count (old-film files loaded, steps swapped) runs at every chat's start and end; new work may never raise it. Beat: 41 of 41 match, exceptions named.
**Change 2, one kit (own yes after Change 1 passes; Opus high; about 8-9%).** Remove the 52 kit-to-film loads, most-used first (arm, person, torso, leg, head), each borrowed step rebuilt in the kit to the rules or dropped, with a before/after sheet. Grand Theft Autism restarts once the people steps are done. The kit test draws a reference cast (man, woman, short sleeves, jacket) and runs the hand, seam and body checks on it. The load-map check then refuses any new file loading a finished film's file or overwriting another file's step. Beat: loads 0 (from 52), swaps 0 (from 15), old films reached 0 (from 40).
**Change 3, one route (own yes; about 1-2%).** Finished films' files leave the live folder (kept at their bookmark); the catalogue lists only kit parts, each finished film once as "frozen, recut only". Posting a film freezes and moves it that day. Beat: catalogue film entries 0 (from 67).
Total about 12-14% of a week, once, filed as tool work; reviewed at the next film's end.
## For Sam
### Option 1: Freeze old films, then one clean kit
Each finished film gets a saved snapshot it can always be recut from, proven on every film first. Then the drawing kit stops borrowing pieces from old films: each piece is rebuilt to the body rules or dropped, and a check refuses anything new that reaches for an old film. Old films leave the working shelf and the kit list shows only current parts. You would notice cast sheets drawn only from current, rule-checked parts, and recuts still working. About 12-14% of a week, in three yeses; Grand Theft Autism restarts after the people parts.
Lost: a recut of an old film uses the kit as it was then; later improvements are carried across only if you ask.
Added: one current kit, a snapshot per finished film, a check that stops old pieces creeping back.
### Option 2: Spot-check three films, then cut and check bodies
Same idea, cheaper to start: prove recuts on three films only (Blessed, Milburn, the oldest), cut the kit's links to old films, and run the body checks on every cast sheet. The kit list still names old films' files. About 8-10% of a week.
Lost: the other 38 films' recuts are unproven before the kit changes; old films stay findable in the kit list.
Added: one kit free of old films; body checks on every cast sheet.
