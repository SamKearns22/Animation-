# Satire-style film: the one page to read

For a full Satire-style TikTok film (more than two people talking, or any action). For two people talking, use
`guides/quick-video.md` instead. Open `guides/best-practice.md` Part 2 only for a kind of scene this page doesn't cover.

## Start
1. Copy `source/satire_template.py` to `source/NAME.py`; set `NAME`, and change only its STORY section (title, cast,
   where people stand, who looks at whom, lines, shots, actions as beats). Everything else is already wired in.
2. Read Sam's brief (`prompts/_brief-skeleton.md` is the shape; `prompts/russiadent-evil-template.md` a finished one).
   Ask all questions in ONE message, each with a recommended answer. Notes go in `notes/NAME.md` (`notes/_template.md`).
3. `python3 source/NAME.py cast OUT.png`: the cast sheet. Sam approves it before anything moves.
4. `python3 source/NAME.py stills OUT_DIR T T ...`: one still per shot. Sam's notes come back in one batch.

## The look (all built in: `source/satire_style.py`)
Flat colour, one outline weight, no gradients or glows; lumpy, hand-cut shapes (`blob`, `rough`), never perfect ovals
or ruler-straight boxes; every copy different (colours, sizes, facing); circle hands with props laid over them; deadpan
faces; hard cuts; a close-up for the reaction that matters; Cranberry Title style for the title, on 2 s.

## Staging and acting (each is checked or has a tool)
- Everyone in a fight or a conversation looks at the other (`LOOKS_AT`; checked: eyelines).
- Nobody is ever frozen: listeners sway, background people each do one thing (checked: the audit).
- Every action as beats: set-up, action, contact, follow-through, settle, with a pace ('fast' into a hit, 'slow' out)
  (`filmkit.Beats`; every frame of the path is tested with `filmkit.check_joints`: joint limits, bone lengths, a hand
  never through a head).
- Plan big moves in the floor plan first: a fallen body is long; place action seen in two shots with
  `filmkit.visible_spots`.
- Anything that changes stays changed (a smear, a broken window): list it and probe it (`filmkit.probe_marks`).
- Anyone in a close-up must be seen in a wide shot.

## Before every render
`python3 source/preflight.py NAME OUT_DIR` (all cores; or `python3 source/NAME.py check` for the plan checks and audit
alone, seconds to minutes). It runs: the plan checks (mouths move for every phrase, the voice sits at least 6 dB above
everything else, subtitles printed as text: proofread them now), the general audit (each body alone: in pieces, popping,
stretching, frozen; actions; eyelines), and a contact sheet with the safe area. Fix every fault, or list a deliberate
one (`FAST_OK`/`allow`) with its reason.

## Render
- `python3 source/NAME.py final OUT.mp4 --small`: a quick look (540 x 960), only when a shot's movement changed.
- `python3 source/NAME.py final animations/NAME-vertical.mp4`: the final. Pictures are cached; captions and title go on last.
- Caption or timing note: `... final OUT --reuse` (no pictures re-rendered). Note on shot X: `... --reuse --redo X`.
- Sound note: rebuild the sound only and attach it to the finished picture (never a re-render).
- Say how long it will take; push notification when it ends; send the film in the chat; update `story/status.md`.

## If a check fails
| Message | Fix |
|---|---|
| `in N pieces` | A body part is detached (neck, head, limb): its base must sit inside the shape it joins. A stain on the floor is fine: list it in `allow`. |
| `pops` / `stretches` | A pose switches drawing or a limb flips between frames: add an in-between pose, or ease the beat. A body thrown on purpose: list it. |
| `frozen` | Give them a small action (sway, breathing, a glance). |
| `not looking at who they are dealing with` | Fix `LOOKS_AT` or the pupils' side. |
| `bends ... degrees` / `elbow folded` | Move that beat's target further from the shoulder or add a beat that swings wide. |
| `no mouth movement` | The words aren't spread over that phrase: check the line's recording and text. |
| `only N dB above the rest` | Turn the crowd, music or effects down under that line (or the line up). |
| `... is missing at` | A permanent mark isn't drawn in that shot: draw it from the list of permanent changes. |
| `never seen in shot 2 or 3` | Move that person, or show them in a wide shot. |
