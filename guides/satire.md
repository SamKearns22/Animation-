# Satire-style film: the one page to read

For a full Satire-style TikTok film (more than two people talking, or any action). For two people talking, use
`guides/quick-video.md` instead. Open `guides/best-practice.md` Part 2 only for a kind of scene this page doesn't cover.

## Start
1. Copy `source/satire_template.py` to `source/NAME.py`; set `NAME`, and change only its STORY section (title, cast,
   where people stand, who looks at whom, lines, shots, actions as beats). Everything else is already wired in.
   **A remake** of an older film starts from the template too (bring over only the story, recordings and timing, never
   the old code), and keeps the original's camera angles, shot order and timing unless Sam says otherwise.
2. Read Sam's brief (`prompts/_brief-skeleton.md` is the shape; `prompts/russiadent-evil-template.md` a finished one).
   Ask all questions in ONE message, each with a recommended answer. Notes go in `notes/NAME.md` (`notes/_template.md`).
   Remind Sam: leave about a second of silence after each line before stopping the recording, and turn off the
   iPhone's Voice Isolation mic mode (takes stopped mid-hiss, chopped by the phone's clean-up, crackled in Cry Minister).
   In code, look lines up by their number, never their position, so cutting a line never breaks the shots after it.
3. `python3 source/NAME.py cast OUT.png`: the cast sheet. Sam approves it before anything moves. It shows **every view**
   each character appears in (from above, a close-up, mid-action), not only the default one; and for the film's key
   reaction, a **numbered strength sheet** (1 = slight, 6 = huge) for Sam to pick a number from.
4. `python3 source/NAME.py stills OUT_DIR T T ...`: one still per shot. Sam's notes come back in one batch.

## The look (all built in: `source/satire_style.py`)
Flat colour, one outline weight, no gradients or glows; lumpy, hand-cut shapes (`blob`, `rough`), never perfect ovals
or ruler-straight boxes; every copy different (colours, sizes, facing); circle hands with props laid over them; deadpan
faces; hard cuts; a close-up for the reaction that matters; Cranberry Title style for the title, on 2 s.
No blank surfaces: every building, wall and window in view gets windows, doors, signs, drainpipes or posters (a blank
flat wall reads as unfinished or computer-made); signs and posters carry a joke tied to the film where they can.

## Staging and acting (each is checked or has a tool)
- Everyone in a fight or a conversation looks at the other (`LOOKS_AT`; checked: eyelines).
- Nobody is ever frozen, and nobody wobbles: idle life is a held pose with a quick small shift now and then
  (`filmkit.shifts`), a blink or a glance; never a looping sway or tremble. A dead-still hold that is the joke (a
  stunned stare) is listed in `allow` (checked: the audit).
- Eyes **jump** to each new thing on one frame, and the head turns on the same frame (`filmkit.glance`); only following
  something that moves is smooth. An eased look reads as woozy, not alert.
- Background people and animals behave normally (pecking, chatting, walking) with relaxed, friendly faces. Nobody looks
  at the camera or reacts unless the script says so.
- One of each facial feature: when a face part is drawn over the library's face (a shocked mouth, raised brows),
  switch the library's own off (`mouth`, `brows`), or the face shows two. A drawn mouth (gritted teeth, a grimace) goes
  on only when the library mouth is 'hidden': call `satire_style.own_mouth(sp)` first (it stops with an error otherwise).
- Selfie shots: the arm holding the phone runs out of the frame towards the lens, raised for an over-the-shoulder view
  and never under the on-screen text; we never see a phone in that hand. When the threat is behind him, he glances back
  over his shoulder towards its side of the screen.
- A small or distant person reacting to the story uses the whole body (stops dead, hands on hips, a big slow head shake,
  then holds), placed where nothing in front hides them. A face-only reaction is for close shots.
- Every action as beats: set-up, action, contact, follow-through, settle, with a pace ('fast' into a hit, 'slow' out)
  (`filmkit.Beats`; every frame of the path is tested with `filmkit.check_joints`: joint limits, bone lengths, a hand
  never through a head).
- Plan big moves in the floor plan first: a fallen body is long; place action seen in two shots with
  `filmkit.visible_spots`.
- Anything that changes stays changed (a smear, a broken window): list it and probe it (`filmkit.probe_marks`).
- Anything thrown or dropped falls under gravity, scatters unevenly (each piece its own size and speed), lands, and
  stays where it lands.
- The title never covers anyone (checked). It sits no higher than 310 px (TikTok's buttons); one line sits highest
  (`TITLE_AT` in the template).
- Sound effects are placed by when they really start (`filmkit.place`), not by the start of their file.
- Anyone in a close-up must be seen in a wide shot.

## Sound (all in `source/mossad_audio.py`)
- Never squash the voice to make it loud: `MA.master` evens out loud stretches gently (down over 30 ms, back over
  300 ms), masters at -16 LUFS and limits by 3 dB at most (checked: `MA.limit_check`). Phone takes peak about 20 dB over
  their average; squashed 8 dB to reach -14 LUFS, they crackled on a phone.
- Every line's tail is cleaned (`MA.smooth_tail`, built into `MA.line`): the real "s", "z" or "k" is kept, then the hiss
  only fades. The phone's clean-up chops final hisses into bursts and thumps, which the extra volume makes obvious.
- Lines recorded in one go and played back to back with no gap stay ONE unbroken piece of sound, split only for the
  mouths (as in `cryminister._voices`); never fade, treat separately or space out pieces cut mid-sound.
- When Sam reports a bad sound, first make a short clip of the original recording and the film's version of that moment
  at the same volume, to learn whether the fault is in the recording or our processing. Send each sound fix as a
  sound-check file (the soundtrack over one still) before any render.

## Before every render
`python3 source/preflight.py NAME OUT_DIR` (all cores; or `python3 source/NAME.py check` for the plan checks and audit
alone, seconds to minutes). It runs: the plan checks (mouths move for every phrase, the voice sits at least 6 dB above
everything else, subtitles printed as text: proofread them now), the general audit (each body alone: in pieces, popping,
stretching, frozen; actions, including elbows staying on their own side; eyelines; the title clear of everyone), and a
contact sheet with the safe area. Fix every fault, or list a deliberate one (`FAST_OK`/`allow`) with its reason.
It also prints **QUESTIONS FOR SAM** about the sound (deep wind rumble, dead silence, a jump in volume at a cut). They may
be meant: put each to Sam with a recommended answer, and change nothing until he answers.

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
| `frozen` | Give them a held pose with small quick shifts (`filmkit.shifts`), a blink or a glance; never a sway loop. A hold that is the joke: list it in `allow`. |
| `crossed the middle of the body` | The elbow bends the wrong way (usually `'down'`): bend it `'out'` or use a relaxed `'depth'` arm. If the action really crosses (arms folded, reaching across), list it; ask Sam if unsure. |
| `the title covers` | Raise it (no higher than 310 px), make it one line, or make it smaller (`TITLE_AT`). |
| `not looking at who they are dealing with` | Fix `LOOKS_AT` or the pupils' side. |
| `bends ... degrees` / `elbow folded` | Move that beat's target further from the shoulder or add a beat that swings wide. |
| `no mouth movement` | The words aren't spread over that phrase: check the line's recording and text. |
| `only N dB above the rest` | Turn the crowd, music or effects down under that line (or the line up). |
| `... is missing at` | A permanent mark isn't drawn in that shot: draw it from the list of permanent changes. |
| `never seen in shot 2 or 3` | Move that person, or show them in a wide shot. |
