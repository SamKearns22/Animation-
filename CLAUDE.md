# Working with me

I don't know how to code. Please:

- **Explain everything in plain English.** Avoid jargon, and if you have to use a technical word, say what it means.
- **Make choices for me rather than listing options.** Pick what you think is best, do it, and briefly tell me what you chose and why.
- **Always tell me where to find the finished file.** When you make or change something, tell me exactly where it is and how to open it.
- I only have an iPhone and this app, no computer. When an animation is finished, **send the file to me directly in the
  chat** so I can tap it and save it to my Photos. Never give me steps that need a computer.

# Files

- Every file **under 50 MB** (GitHub warns above 50, rejects over 100); aim for **a few MB per animation** (GitHub keeps
  every old version; the project stays well under 1 GB). Shrink or compress if needed and tell me the final size.
- Only the **finished version** goes on GitHub, in `animations/` with a clear name; drafts and test renders stay off.
- Default to **MP4**; a GIF only if I ask (short and small).
- The tools (Python with Pillow, NumPy, imageio, a bundled ffmpeg) install at session start (`.claude/hooks/setup.sh`).

# Asking me before you go on

- **Before any full render, offer me an animatic** (a quick, lower-quality version of the whole film) and wait for my
  Y or N. **Always ask before a final render and wait for a clear yes**; "fix this before the final render" is not a
  go-ahead (15 Oct).
- **Before every animatic render (re-renders too), show me the check sheet and wait for a clear yes**; a note in reply
  is not a yes (18 Oct). **No animatic while a shot is missing anyone the brief puts in it**: say so instead (25 Oct).
- **"Just go" (or any override of mine) skips waiting for my yes, never the checks (25 Oct):** pre-flight still runs,
  every fault is read and fixed or named before the render.
- **Unattended runs stop after one animatic (25 Oct):** if I leave you working (overnight), render one, send it, and
  wait; never stack rounds I haven't seen.
- **Notes on movement get a short clip (18 Oct):** render only the seconds around it, small
  (`final OUT --small --span T0 T1`, under a minute). Clips need no yes; a full animatic comes once the clips look right.
- **"Hold" means collect, don't act (16 Oct):** reply to each note with how you understood it and how you'll fix it,
  change nothing, do it all when I say go. **"Hold responses until all my notes are through" (24 Oct): no replies at
  all** until I say the notes are done.

# Rules are permanent

- **New rules and lessons are proposed to me first (16 Oct):** say what you would add and where; wait for my numbers.
- **When I say "I want a rule" (or "every film", "from now on", "always"), I mean a permanent rule for all future films
  (Sam, 25 Oct).** Reply with the exact wording and where it goes; on my yes, write it into the guide in that same chat,
  never "later" and never only in the film's notes. A note asking for a rule is not done until the rule is in a guide
  and listed in `guides/rule-register.md` with the check that tests it (or "by hand" on the check sheet).
- **Before every handover, search the film's notes for rule requests and proposals not yet in a guide** (rule, every
  film, from now on, proposed) and list them in the handover.

# Models and chats (to save money)

- Each stage has a model:
  - planning (reading the brief, staging the shots, questions for me): Opus, high effort;
  - building anything new (a new character, creature, set or tool): Opus, high effort;
  - reading my notes and deciding the fixes: Opus, medium effort;
  - building from a clear plan (drawing to a brief, applying my notes, sound): Opus, medium effort;
  - routine work (filing recordings, sheets, checks, renders, clips, sending, saving): Sonnet.

  When the next stage needs a different model, stop, send me a push notification ("Time to switch to Sonnet: type
  /model") and wait for me to say I've switched. Never carry on into a stage that needs a stronger model. Usually only
  3 or 4 switches per film. Quick videos: Sonnet, medium effort. **If I start a task on the wrong model, refuse and tell
  me**; let me change it, or offer me the option to override.
- **Fresh chat at every stage switch (20 Oct).** Every step re-reads the whole chat (Power Crime Action: about 700 steps
  in one chat, 73% of a week across three films). Write where things stand into the film's notes file (its ONE "Where
  things stand" section, overwritten each time; old handovers go to `notes/archive/`) and `story/status.md`, commit and
  push, **paste the handover into the chat too** (what's done, what's next, what to type in the new chat), and tell me
  to start a new chat. The new chat reads only that and the film's guide.
- **Read little:** look at as few pictures as possible (one combined sheet, full size only for a detail, never an
  unchanged picture again; trust simple certain fixes and check them at the end); use `python3 source/codemap.py FILE.py`
  and read only the lines needed; read only your film's section of `story/status.md` (`grep -n '^## ' story/status.md`).
- **Push notifications** whenever a render or other long process finishes, fails or needs my decision, and at every
  stage end and handover, saying what is done and what to do next (`guides/tiktok-design.md`, "Working"). Say how long
  each render will take and report how long it took.

# Sending work to me

- **Self-review before every send (18 Oct):** list in a line or two which checks ran, what was compared with the
  references, and anything you're unsure of. Never send something a check flagged without saying so.
- **Critique-fix rounds (19 Oct):** after each batch of my notes, up to three rounds on your own (render, critique,
  fix), each with a sheet or clip and a two-line summary. Stop early for a taste call or anything that removes
  something I've seen.
- **The brief is a checklist (18 Oct):** every detail of my brief and notes (wording, asterisk and bleep counts, who
  stands where, colours, props) goes in the film's notes file as a list, ticked against the film before the first
  animatic; anything not done is named.
- **Flag what a fix takes away (18 Oct)** as a loss (a prop, a person, a joke, a landing in shot), and **flag your own
  additions** (a sign, a reflection, a joke, a sound, set dressing), so I can say no before it costs a round.
- **A note I've given before is a warning (25 Oct):** if a new note repeats an earlier one, find why the first fix
  failed before changing anything, and tell me.

# Making the films

- **One main line of work:** `claude/create-claude-md-oe8z4g` (GitHub's default branch) holds everything. Start from
  it, merge in any newer work from other branches (`git branch -r`), and merge back at the end. Never leave a tool or
  lesson only on a side branch.
- **Quick video (short two-person film): read only `guides/quick-video.md`**, nothing else. Sonnet, medium effort; all
  my notes in one batch after the one stills sheet.
- **Satire-style film (the TikTok parody series, beyond two people talking): read `guides/satire.md` first**, start
  from `source/satire_template.py` (always: it carries the house style and the checks), and open
  `guides/best-practice.md` Part 2 only for a scene that page doesn't cover. Follow best-practice Part 1 sections 1.2
  and 1.3 (contact and continuity). **Reuse before building:** check `guides/kit-catalogue.md` (every set, person,
  prop and effect already built) and the kit tools; build new only where nothing fits, and say so.
- **Motion-led films (stunts, action): after the cast sheet, go to a quick animatic early**; stills can't show timing,
  camera moves or physics (Roadster).
- **Every film (not quick videos): follow `guides/film-quality-rules.md`.** Rules marked [tool] need a tool still to
  be built (`story/status.md`, "Build list"); do the check by hand until it exists, and say so.
- **Flat cartoon people:** read `guides/figure-rig.md` before building or animating anyone; follow `guides/preflight.md`
  from the first brief (`python3 source/preflight.py FILM OUT_DIR` before every animatic; `python3 source/voices.py
  FILES` as soon as recordings arrive). Hands are always a plain circle with props laid over it.
- **Yuletide horror trailer:** read `guides/yuletide-trailer.md`. **Any other film:** `guides/best-practice.md` (Part 1
  is general; later parts are for one kind of project only). Add each lesson to the right guide as it is learned.
- **Sound:** no sound effects unless the script names them or I ask; voices only by default.
- **TikTok:** follow `guides/tiktok-design.md`. No title by default (the cranberry title only when asked); Hook Text
  (the line introducing the joke) in TikTok's white-box caption style. **Every video ends with the CranbriJoos
  sign-off** (the beaver sipping from the carton, with my slurp, 2 s; the one standing sound effect): finish with
  `python3 source/finish.py CLEAN.mp4 animations/NAME-vertical.mp4 ["Hook Text"]` from the clean render in
  `source/data/`.
