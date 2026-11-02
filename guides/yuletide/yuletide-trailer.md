# Yuletide horror trailer: a separate experiment (not finished)

Everything for Yuletide lives in this folder, `guides/yuletide/`. It never applies to the TikTok films, and nothing
in it changes them.

## When we next work on Yuletide (Sam, 2 Nov): use the newest engine
Yuletide was last worked on in early October, on an older engine (`source/shots/`, `horror_preflight.py`,
`lookbook_check.py`, the MakeHuman bodies). The main engine has moved on a long way since (the plan in metres,
`preflight.py` and its shared checks, the render lock, `sheet.py`, clips with `--span`, the rulebook).
- **Start from the current engine, the way a remake does:** bring over the story, the look, the score, the shot
  list and what was learned, never the old code as it is. Plan the first session as a short "port" stage (Opus
  high): decide which current tools carry over (the plan, pre-flight and its checks, the render and its lock, the
  sheets, the clips) and what the graphite 3D look needs that they don't have yet. Say what that costs before
  building.
- The old code stays as a reference for how the look was made (the graphite drawing, the hair, the MakeHuman bodies).
- The rulebook (`guides/film-quality-rules.md`) applies, except rules about the flat Satire look (circle hands,
  flat colour, front-on faces, the Satire style kit): Yuletide keeps its own look.

## What there is (October)
- The story and premise: `story/yuletide.md` (never reveal the hidden backstory in the trailer); the animation test:
  `story/animation-test.md`; the finished test: `animations/yuletide-animation-test.mp4`.
- The look: `lookbook/`, `tone.md` (the A24 craft, never the brand), `best-practice-yuletide.md`.
- People and movement: `character-anatomy.md` (MakeHuman bodies; its checklist), `movement.md` (eyes, blinks,
  smiles, hair, body).
- The old pipeline: `pipeline.md` (shots from parts and recipes); `python3 source/horror_preflight.py` before a render;
  `shot.py sequence ... --reuse`; `python3 source/lookbook_check.py OUT_DIR` against `lookbook/`.
- Still open from October (the wrist in the chop, the girl's neckline, the hair speed, the crown parting, the trailer
  shot list timed to `music/horror-trailer-score.m4a`): `story/status.md`, "Yuletide".
