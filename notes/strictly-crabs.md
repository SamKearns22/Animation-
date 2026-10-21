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
