# One route to the current kit (tool job; Grand Theft Autism paused for it)

## Brief checklist (Sam's words, 20 Nov)
- [x] "there should be one route to the right kit, the best kit, the most updated kit" (measured; through the proposal route)
- [x] "you shouldn't be able to find all of the previous kits from previous films because they're done now" (Option 1, change 3)
- [x] "should the outdated things be completely isolated or deleted?" Answer sent: isolated, never deleted (recuts need them)
- [x] "should this be the case throughout the project?" Answer sent: yes, every kind of kit (people, places, sound, checks)
- [x] Sam's pick (20 Nov): "1" (freeze old films, then one clean kit; each change still gets its own yes)

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

## Where things stand (20 Nov, one-route-kit chat 3, Sonnet)
- Rules that bite next: the proposal route (one change per yes), 24 (cost watch), 30.
- Done: Change 1 (results above). Pushed with bookmarks.
- Next: Change 2 (one kit), Opus high, on Sam's own yes. Not started.
- Needs Sam: Y/N Change 2 (his priority, 20 Nov: continue Grand Theft Autism with the best tools only; he dislikes the small chips in the jury shoulders, picture in chat); Blessed's 1.92% drift is probably the same thing.
- Read: this file; notes/proposals/one-route-kit.md "Final version" Change 2; guides/job-packs.md Build.
- Open rule requests: none found.
- For Claude: freeze.py recut/check/count; branches claude/elegant-davinci-2anki0 (depth-check proposal files, not this job's) named, not merged; claude/blessed-c2-mics-wip as before.
