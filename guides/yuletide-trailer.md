# Yuletide horror trailer: what to read and run (moved from CLAUDE.md, 25 Oct)

For the Yuletide horror trailer only; never apply these to the TikTok films.

- Before building or changing any character, read `guides/character-anatomy.md` and follow its checklist; build people
  on the free MakeHuman human model (CC0) rather than sculpting bodies from scratch.
- Before animating anything, read `guides/movement.md` (timing of eyes, blinks, smiles, hair and body).
- Before making or changing a shot, read `guides/pipeline.md` (how shots are built from reusable parts and recipes).
- The story and the director's decisions for the animation test are in `story/animation-test.md`.
- The film's premise and hidden backstory are in `story/yuletide.md` (never reveal the backstory in the trailer).
- Before rendering, run `python3 source/horror_preflight.py` (every pose of every frame, about a minute); render with
  `shot.py sequence ... --reuse`; check every new drawing with `python3 source/lookbook_check.py OUT_DIR` against
  `lookbook/`.
- The trailer should evoke the style and quality of an A24 horror film (the craft, never the brand): read
  `guides/tone.md` before planning or changing any shot.
