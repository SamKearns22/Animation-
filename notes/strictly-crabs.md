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

## References
| reference | what it shows | ours matches? |
|---|------|------|
| 1 velvet crab, white | brown velvety shell, red eyes, dark legs with blue lines, flat paddle back feet | shell texture from photo, paddles built |
| 2 velvet crab on weed | same species from above | - |
| 3 shore crab reared up | the threat pose: claws raised, orange underside | used for the final pose and his underside colour |
| 4 shore crab, black | olive-grey shell, olive-yellow legs, chunky claws | shell texture from photo |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|

Decisions made:
- She is the velvet crab (screen left), he is the shore crab (screen right), as in the reference couple.
- 136 bpm; first beat 9.30 s into the music. Routine in beats: A 0-8 shimmy, B 8-16 scuttle and hip rolls,
  C 16-24 her lunge, D 24-32 spins and she crosses in front, E 32-48 she hops onto his level claws, spin lift,
  down, F 48-56 rear-up final pose.
- Sam said "Go" (21 Oct) to building the crabs in this chat despite the effort-setting rule.

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
