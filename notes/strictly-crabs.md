# Notes for Strictly Crabs Dancing (one file, numbered; mark each done as it is fixed)

Files: refs in `refs/strictly-crabs/` (music, ident recording, routine reference, 4 crab photos).
Titles: `source/strictly_crabs_titles.py` (Come -> Crabs on the ident, 0-9 s of the music, fade at 8.3-9.0 s);
output `animations/strictly-crabs-dancing-titles.mp4` (kept off GitHub until the film is finished).
Dance: `source/strictly_crabs/` (prep.py cuts the photo textures; scene.js = crabs, routine, cameras, clipping
checks; render.mjs drives headless Chromium: `node render.mjs stills|video|check ...`). Needs
`npm install --no-save three@0.170.0 playwright-core` in that folder each new session.

## The brief as a checklist
| # | from the brief or a note | done? |
|---|------|------|
| 1 | First 9 s of the music, fading out at the end so the drop isn't too sheer | yes (titles) |
| 2 | Ident copied frame by frame; "Come" replaced by "Crabs" | yes (titles; font is a plain bold italic, flagged) |
| 3 | Dance covers only the remaining seconds of the music (9.0-33.9 s, 24.9 s) | built to 24.9 s |
| 4 | Two crabs fluidly recreate the routine (reference: side-by-side Latin moves, she lunges low, spins, overhead spin lift, final pose) | routine planned in scene.js, bars A-F |
| 5 | No BBC logo, no Strictly title in the dance | yes |
| 6 | Crabs not cartoony at all; as close to the 4 photos as possible | textures cut from photos 1 (velvet, her) and 4 (shore, him); 3D shapes are approximations |
| 7 | Clothing optional, only if logical and seamless | not added (could not see a seamless way that stays realistic) |
| 8 | Most important: crabs are dancing and are not clipping | clipping audit in scene.js (check mode) |
| 9 | The stage | blurred ballroom from the routine's wide shot behind a polished floor |
| 10 | Shot J1 (21 Oct): Craig Revel Horwood alone, flamboyant, droll, exaggerated: "I don't really understand the joke, darling, but I'm having an amazing time." (`craig-amazing-time.m4a`, 6.8 s, speech 1.36-6.33) | planned, waiting on Sam's answers |
| 11 | Shot J2: all four judges at the table, eyes on the crabs as they spin past; eyes follow them | planned |
| 12 | Shot J2: Anton, excited, over-enthusiastic, thrusts a scoring paddle reading 290 in the air: "290!" (`anton-290.m4a`, 4.2 s, speech 0.98-3.04; measured ~13 syllables, "two hundred and ninety" is 7: ask Sam) | planned |

## References
| reference | what it shows | ours matches? |
|---|------|------|
| 1 velvet crab, white | brown velvety shell, red eyes, dark legs with blue lines, flat paddle back feet | shell texture from photo, paddles built |
| 2 velvet crab on weed | same species from above | - |
| 3 shore crab reared up | the threat pose: claws raised, orange underside | used for the final pose and his underside colour |
| 4 shore crab, black | olive-grey shell, olive-yellow legs, chunky claws | shell texture from photo |
| judges-ref-01, 02 | Craig: slicked-back dark hair, high forehead, arched brows, red jacket with black flower pattern (01) or burgundy velvet (02), black bow tie, white shirt with black studs, pen in hand | - |
| judges-ref-03 | all four promo, left to right Shirley, Anton, Craig, Motsi | - |
| judges-ref-04, 06 | Anton: short grey-brown hair, big toothy grin; gold paisley jacket (04) or black tux (06), black bow tie | - |
| judges-ref-05, 07, 12 | the table: glittery pink/purple/silver bands, round glitter-ball emblem in the middle; seating left to right Craig, Motsi, Shirley, Anton; blue light-beam backdrop | - |
| judges-ref-08, 09 | Shirley: dark wavy bob, big earrings and rings, black with silver swirls (08) or white ruffles (09), expressive hands | - |
| judges-ref-10, 11 | Motsi: hair up in a bun, big gold or drop earrings, yellow ruffled one-shoulder dress (10) or sequinned black (11) | - |
| judges-ref-12 | paddles: white round paddles with big black numbers, held up beside the face | - |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|

Decisions made:
- She is the velvet crab (screen left), he is the shore crab (screen right), as in the reference couple.
- 136 bpm; first beat 9.30 s into the music. Routine in beats: A 0-8 shimmy, B 8-16 scuttle and hip rolls,
  C 16-24 her lunge, D 24-32 spins and she crosses in front, E 32-48 she hops onto his level claws, spin lift,
  down, F 48-56 rear-up final pose.
- Sam said "Go" (21 Oct) to building the crabs in this chat despite the effort-setting rule.

## Judges shots (added 21 Oct, chat 2, planning)
Sam sent 12 judge photos (`refs/strictly-crabs/judges/`) and two recordings (`refs/strictly-crabs/`), checked with
voices.py. Questions sent to Sam in one message, with recommended answers; build starts once he answers.
Plan: one animatic of the whole film (titles, dance, judges) once the judges are built, instead of a dance-only one.
Sam's answers (21 Oct): 1 Satire house style for the judges, crabs stay real-looking; 2 the music carries on at a
lower volume under the judges (the track is only 33.9 s, so a loop of its closing bars, beat-matched, checked with
musiccheck); 3 all four follow the crabs with their eyes, then Anton does his bit once they have passed; 4 outfits:
Craig red flower jacket, Motsi yellow ruffle, Shirley black with silver swirls, Anton black tux; 5 Anton says
"Two hundred and ninety!"; 6 no caricature: Craig flamboyant, extravagant movements; Anton shoots up with the paddle
like an extremely formal yet excited puppy, a big smile. Then: "Give Motsi hair!" (done: sleek updo, side sweep,
big bun; refs incl. `judges/motsi-hair-refs.png`).
Built: `source/strictly_judges.py` (1280 x 720; `cast OUT.jpg`). Cast sheet 1 sent 21 Oct; waiting on Sam's notes.
Next after approval: J1 and J2 movement, crabs rendered alone (transparent) from scene.js spinning past the table,
sound, then the whole-film animatic (check sheet and a yes first).

## Where things stand (handover, 21 Oct, end of chat 1)
Done: titles (0-9 s, Come -> Crabs, 5.7 MB, in Sam's chat; the file in `animations/` is git-ignored so it may be gone
in a new session: rebuild it from `refs/strictly-crabs/ident-recording.mov` with `source/strictly_crabs_titles.py`,
whose paths point at an old scratchpad and need fixing, or ask Sam to resend it). Dance scene built and audited;
cast sheet sent. Sam has NOT yet answered Y/N on the animatic, only asked for the new chat to start with it.
Next: (1) animatic of the dance, then join after the titles with the music (see below); (2) send with check
sheet and self-review; (3) Sam's notes; (4) final render only after a clear yes; (5) TikTok version and sign-off
per CLAUDE.md (not yet decided with Sam: widescreen 1280x720 now, vertical later).
Setup each session: `cd source/strictly_crabs && npm install --no-save three@0.170.0 playwright-core && python3 prep.py`
Render: `node render.mjs video OUT.mp4 640 360 24 0 24.9` (dance seconds; 0 = 9.0 s into the music; ~6-8 min).
Clipping audit: `node render.mjs check OUT.json 30` (about 4 s), summarise with an.py-style script (inter, floor, self, reach).
Join: titles video + dance video, then add `refs/strictly-crabs/music.mp3` 0-33.9 s with fade out over the last 0.7 s
(the music is 33.93 s; titles 9 s + dance 24.9 s = 33.9 s).
Known leftovers from the audit: front leg brushes claw arm by 2-3 cm (about 50 frames), 3-4 frames of 3 cm shell-on-claw
as she slides off his claws, 12 frames with a foot slightly off the floor.
My additions to flag again: lift staged as hop onto level claws (no shoulders), no costumes, camera cuts.

## Chat 2 progress (21 Oct): judges built, animatic being assembled
- Titles rebuilt (tool paths fixed: `source/strictly_crabs_titles.py extract|track|render`, working files in the
  git-ignored `source/data/strictly-crabs/titles/`). The recording is only 3.2 s, so the titles play it at real speed
  then hold the last frame to 9 s with the fade at 8.3-9.0 (my choice, flag to Sam). The small BBC logo from the
  recording is still top left in the titles (brief said none in the dance; ask Sam).
- Judges: `source/strictly_judges.py` (`cast`, `stills`, `final OUT [--small]`), crabs' spin-past rendered see-through by
  `node render.mjs pass OUT_DIR 1280 720 12 26.77 36.0`, composited on the desk. Judges run 15.3 s: Craig 6.2 s,
  all four 9.1 s. Film total 49.2 s plus the 2 s sign-off later.
- Music: loops back 12 bars at beat 55 (film 33.9 s onward), 21 dB down under the judges, faded out over the last 0.8 s.
- People kit: smooth arms and arm checker now always on in `source/burnham.py` (Sam, 21 Oct).
- Still to add before the final: the template's clothes, line-work, size and clipping checks for the judges.
- Sam said "Proceed straight to animatic" (21 Oct), waiving the check-sheet-first step this once.
