# One route to the current kit (tool job; Grand Theft Autism paused for it)

## Brief checklist (Sam's words, 20 Nov)
- [x] "there should be one route to the right kit, the best kit, the most updated kit" (measured; through the proposal route)
- [x] "you shouldn't be able to find all of the previous kits from previous films because they're done now" (Option 1, change 3)
- [x] "should the outdated things be completely isolated or deleted?" Answer sent: isolated, never deleted (recuts need them)
- [x] "should this be the case throughout the project?" Answer sent: yes, every kind of kit (people, places, sound, checks)
- [x] Sam's pick (20 Nov): "1" (freeze old films, then one clean kit; each change still gets its own yes)
- [ ] Sam (20 Nov 11:38, chat Vqz9UpsK): "Please inform me once the kit produces our best quality product (represented by the models in Milburn, aside from the 3/4 pose tools that have been produced since then) so I can continue with the film." Test: the kit redraws Milburn's people as the posted Milburn (people.py replicate milburn, from its bookmark), plus the 3/4 tools.
- [ ] Sam (20 Nov 11:38): "I don't like those tiny chips in the shoulders that are throughout the jury picture." (Blessed jury; the live code differs from posted Blessed by up to 1.92%: drift-baseline.json.) Fix in the kit's shoulder join, checked on the reference cast.

## Estimate
Whole job about 12-14% of a week once, as tool work (judge's figure, unmeasured). This proposal chat: about 3%.

## Measured (proposal chat 1, 20 Nov; scripts in notes/proposals/one-route-kit/measure/)
52 of 117 kit files load an old film's file; the people and places kits reach 40 old films' files; Grand Theft
Autism's cast loads 12 at start and 15 basic drawing steps (arm, person, head, body, leg, hair, mouth) are run by old
films' code; 67 of 108 catalogue entries are one film's file; all 41 finished films' code still loads. The reverse harm
too: Grand Theft Autism's kit additions made Milburn's frame stop matching (kittest focus_front_heads).

## Learn step results (chat 2, 20 Nov, Sonnet)
Full history fetched (3,448 saves; it was shallow). For each posted video, its save = the last save that changed that video file; one frame re-drawn from that save in a separate copy at 40% of the film, compared with the posted video (sheet: notes/sheets/one-route-kit-recut-check.png).
- 32 films compared. 27 draw the same picture (differences only captions, mouth shape, small timing).
- 5 differ, all look like time-mapping or a later edit, not broken code: halo-no-no (different shot at that time), remakes (different shot), protest-tiers (same scene, crowd placed differently), poker-mon (same scene, different pose), press-secretary (same picture; the re-draw carries a time label). Not proven; one frame each only.
- Could not re-draw: bayeux and strictly-crabs (their working data folders are not saved to GitHub: gitignored, so a save alone cannot recut them); king-in-the-north (only storyboard stills, no timed frame); channel-trailer, bingo-bingo, yuletide test, dam/flying-whales/prepper variants and story-size copies (no single-frame tool found; not tried).
- Finding for Change 1: bookmark alone is not enough for bayeux and strictly-crabs; their data folders need saving first. Also several videos' last save is a re-title (9707503c, 26 Sep, five early films): the save is a proxy.
- 15 swapped steps (notes/sheets/one-route-kit-15-swapped-steps.png): 4 meet the rules (turned head, limbs arm, limbs legs, circle hands); 11 are one film's patch or drawing (Ad-Vanced Notice arm/torso, MidTerminal wings, Patriots 3 boots, Patriots 4 back hair, Mossad's six face/body steps).
- Cost: about 1.5%, as estimated. Changed nothing in the kit or any film.

## Change 1 results (chat 3, 20 Nov, Sonnet)
- Built source/freeze.py + source/data/freeze/films.json: `tag` (bookmarks `film/NAME`, 39 films + extra bookmarks for variant videos, 61 in all), `recut NAME` (draws from the saved copy in a separate folder), `check` (redraw vs posted video), `count` (baseline in count-baseline.json: old-film files loaded 12, steps swapped 15, kit files loading a film file 52, old films reached 40; may never rise). Count and bookmark check run in handover.py start and end; kittest finished_films_keep_their_bookmark.
- Registry: 39 films with a posted video in animations/ (the "41" was a loose count). Not in it: Shocking Behaviour (video never on GitHub, Sam 18 Oct); Grand Theft Autism (not finished).
- Five early films (Dam, The Salt, Andrew, Sam, Listening & Learning): bookmark is on the true source save (the last save that changed the raw video, 24-26 Sep), not the re-title 9707503c.
- Bayeux and Strictly Crabs: their data folders exist nowhere (gitignored, lost with old containers), so nothing to save. Both rebuild exactly from files in the repo; the rebuild steps ("regen", "fixups" for tool paths) are in films.json and run on each recut (Bayeux about 2.5 min, Strictly Crabs about 3 min). Both now redraw and match.
- Result: 38 of 39 redraw from their saved copy and match the posted video (sheets notes/sheets/one-route-kit-freeze-check-1/2.jpg). Exception named: channel-trailer (a cut of other finals plus clips redrawn from other films' copies; draws no picture of its own).
- The 5 that differed in the Learn check (Halo No No, Remakes, Protest Tiers, Poker-Mon, Press Secretary), at 4 times each (sheet one-route-kit-freeze-five-films.jpg): all match. The earlier "differences" were the posted video being sped up (Halo ~1.3x, Remakes 1.1x) plus captions; Poker-Mon pose differences were one frame, same pose in the other three.
- Blessed test: now draws the film's picture from its saved copy and reports how far the live code is from the posted film. FINDING: live Blessed differs from the posted film by up to 1.92% of pixels (jacket shoulder shading, since the moves-kit saves of 14 Nov). Not loosened; the number may not rise (drift-baseline.json). The places test is untouched (it already failed before: milburn.py uses the kit).
- Not done: places replicate still reads live film code. Next time Change 2 touches it.

## Change 2 results, part 1: the people steps (chat 4, 20 Nov, Opus high)
- Three new kit files hold every step a person is drawn with, each step in one place: `ink.py` (line and shading
  helpers, from An Honest Chat's ed.py), `body.py` (camera, pen, body and outfits, arm poses, the plain test head, head
  tilt, the head/torso/hair-behind hooks HEADS, TORSOS, HAIR_BEHIND; house limbs and circle hands installed once), and
  `faces.py` (the measured face layout from The Patriots 4's cast, the eye and clip from The Traitors', ears, tufts and
  the house mouths from Ad-Vanced Notice's, vance_mouth renamed house_mouth). views.py now owns the arm with short
  sleeves (from MidTerminal) and one list of turned-head kits (TURNED_HEADS) instead of four files rewrapping head_view.
- Dropped (old films' own, stay at their bookmarks): Hope Again's armour, swords, crowns, hall; Mossad's apron, coat,
  tee and extra brows/mouths/hair; Patriots 3 boots, gaiters, cargo, patches; Prepper's rolled/torn sleeves; Vance's
  own torso and arm; MidTerminal's Satan wings and Epstein head; Romesh/Bash/Claudia measures.
- Proof: the people kit redraws every person in five people files (Grand Theft Autism 9, Milburn 7, Blessed 27,
  facetool 2, Protest Tiers 11) at five turns: PIXEL-IDENTICAL to before (hash per film). GTA's cast sheet and opener
  frames (2.0 s, 6.0 s): identical. Script: notes/proposals/one-route-kit/measure/refcast.py.
- Count: GTA cast loads 0 old-film files (from 12), 0 steps swapped (from 15), also 0 after the cast is set up;
  kit files loading a film file 20 (from 52: every kit file now uses body.py, not burnham.py); old films reached 40
  (people.py's Blessed replicate, places, tools).
- Kit tests (full run vs an untouched copy): the same 7 fail as before (round_page, people_from_a_description,
  places/moves (milburn's Y), outfit_every_view (passes alone), focus_front_heads, watcher). 2 NEW, named:
  lopsided_invented_only and turned_heads_for_anyone test Ad-Vanced Notice's own man, Vance and driver through the live
  kit; their heads were that film's hooks, which the kit no longer carries. Next chat moves both onto the reference
  cast (an invented person drawn uneven; a turned head from a front design), or onto the film's frozen copy.
- Also changed: milburn.py and protest_tiers_cast.py (finished, frozen) one line each (V = PPt.V), so kit tests that
  draw them live still run; mouths.install and satire_style.install_circle_hands do nothing on body (built in).
- Not done yet (next chat): the other 20 kit loads (kittests 19 films, places/blessed_sets, people.py replicate,
  ai_tells_lab, checks, signoff/voices/satire_template (mossad_audio, burnham_film), subtitles, reel...), the 2 tests
  above, the catalogue rows for body/ink/faces, old films reached,
  the reference-cast kit test (man, woman, short sleeves, jacket; hand, seam, body checks; people file
  story/kit-reference-people.txt), the load-map check, the before/after sheet of the steps (pictures are identical, so
  a table of moved/dropped steps with one reference row), Sam's Milburn-look test and the jury shoulder chips.

## Where things stand (20 Nov, one-route-kit chat 4, Opus high)
- Rules that bite next: the proposal route (one change per yes), 24 (cost watch), 30.
- Done: Change 2 part 1, the people steps (above): GTA's cast loads no old film and nothing overwrites a step.
- Sam (20 Nov, "Y to all hurry", read as my pick 1): chat 5 FIRST fixes the shoulder chips (kit shoulder join,
  checked on the reference cast and the jury) and runs the Milburn-look check (people.py replicate on Milburn's
  bookmark), tells Sam, then goes straight to Grand Theft Autism's characters. The tool tidying waits till after the film.
- Later (after GTA): Change 2 part 2 (the other 20 kit loads, the 2 named tests, reference-cast test, load-map check, sheet,
  Milburn-look test, jury shoulder chips); then GTA restarts.
- Needs Sam: nothing. Open: Y/N bookmark Shocking Behaviour (answered 'later').
- Read: this file; notes/proposals/one-route-kit.md "Final version" Change 2; guides/job-packs.md Build.
- Open rule requests: none found.
- For Claude: handover.py end finished after chat 5 opened: its 69 items are QUICK CHECKs of the three films whose files this chat touched by one line (milburn.py, protest_tiers_cast.py: finished, frozen; satire_template.py: imports only). They are those films' own old staging faults (plans, mouths, poses, collisions), not from the kit move; named here, nothing to fix for GTA. body/ink/faces/views.TURNED_HEADS; refcast hashes in Change 2 results; kittests compared against an
  untouched copy (scratch); freeze.py count --lower done at 0/0/20/40.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 3.8% of 15%; forecast not yet planned (2026-11-20)
