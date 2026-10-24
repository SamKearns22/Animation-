# Working with me

I don't know how to code. Please:

- **Explain everything in plain English.** Avoid jargon, and if you have to use a technical word, say what it means.
- **Make choices for me rather than listing options.** Pick what you think is best, do it, and briefly tell me what you chose and why.
- **Always tell me where to find the finished file.** When you make or change something, tell me exactly where it is and how to open it.

# Making animations

- Every file must stay **under 50 MB** so it uploads to GitHub without problems (GitHub rejects anything over 100 MB and warns above 50 MB). Aim well below that: shorten, shrink or compress the animation if needed, and tell me the final size.
- Aim for **a few MB per animation**. GitHub keeps every old version forever, so big files add up fast; the whole project should stay well under 1 GB.
- Only upload the **finished version** of an animation. Keep drafts and test renders off GitHub.
- Default to an **MP4 video** (small and plays everywhere). Only make a GIF if I ask for one, and keep GIFs short and small.
- Put finished animations in the `animations/` folder with a clear name.
- **Before any full render, offer me an animatic** (a quick, lower-quality version of the whole film) and wait for my
  Y or N. Never assume either way.
- **Always ask me before starting a final render, and wait for a clear yes.** Notes like "fix this before the final
  render" are not a go-ahead (15 Oct).
- **Before every animatic render, including a re-render after notes, show me the check sheet and wait for a clear
  yes.** A note in reply is not a yes (18 Oct).
- **Notes on movement get a short clip, not stills or a full animatic (18 Oct).** When a note is about movement
  (timing, a trip, a crash, anything passing through something), render only the few seconds around it, small
  (`final OUT --small --span T0 T1`, under a minute), and send that. Clips need no yes first; a full animatic comes
  only once the clips look right, and still needs the check sheet and a clear yes.
- **Switching models to save money.** Each film moves through stages, and each stage has a model:
  - planning (reading the brief, staging the shots, questions for me): Opus, high effort;
  - building anything new (a new character, creature, set or tool): Opus, high effort;
  - reading my notes and deciding the fixes: Opus, medium effort;
  - building from a clear plan (drawing to a brief, applying my notes, sound): Opus, medium effort;
  - routine work (filing recordings, sheets, checks, renders, sending, saving): Sonnet.

  When the next stage needs a different model, stop before starting it, send me a push notification (for example
  "Time to switch to Sonnet: type /model") and wait for me to say I've switched. Never carry on into a stage that needs
  a stronger model without it. Group the work so there are usually only 3 or 4 switches per film. Quick videos keep
  their own rule (Sonnet, medium effort).
  **If I start a task on the wrong model, refuse and tell me it is on the wrong setting.** Then either let me change it,
  or offer me the option to override the advice.
- **Fresh chat at every stage switch (Sam, 20 Oct).** Every step re-reads the whole chat so far, so one long chat costs
  far more than several short ones (Power Crime Action: one chat of about 700 steps, about 375,000 tokens re-read per
  step, 73% of the weekly budget gone across three films). When a film moves to the next stage, write exactly where
  things stand (what is done, what Sam has asked for, what comes next, the files to open) into the film's notes file
  and `story/status.md`, commit and push, then tell me to start a new chat. The new chat reads only that and the guide
  for the film in hand, never the old history. Also: look at as few pictures as possible, and don't re-read the big
  source files; use `python3 source/codemap.py FILE.py` and read only the lines needed.
  **Post the handover in the chat too (Sam, 20 Oct):** whenever a new chat is needed, also paste the handover (where
  things stand, what comes next, what to type in the new chat) into the message, so Sam has it without opening files.
- **"Hold" means collect, don't act (16 Oct):** when I say hold, reply to each note with how you understood it and how
  you'll fix it, change nothing, and do everything in one round when I say go.
  **"Hold responses until all my notes are through" means no replies at all (Sam, 24 Oct):** stay silent, change
  nothing, until I say the notes are done.
- **New rules and lessons are proposed to me first, and added only once I approve them (16 Oct).** Say what you would
  add and where, and wait for my numbers.
- **Critique-fix rounds (19 Oct):** after each batch of Sam's notes, run up to three rounds on my own (render,
  critique, fix), sending a sheet or clip with a two-line summary each round. Stop early for any taste call, or for
  anything that would remove something Sam has seen.
- **Self-review before every send (18 Oct):** with every sheet, clip or animatic, list in a line or two what was
  checked (which checks ran, what was compared with the references) and anything I'm unsure of, so Sam knows where
  to look. Never send something a check has flagged without saying so.
- **The brief is a checklist (18 Oct):** before the first animatic, every detail in Sam's brief and notes (wording,
  asterisk and bleep counts, who stands where, colours, props) is copied into the film's notes file as a list and
  ticked off against the film; anything not done is named in the message.
- **Flag what a fix takes away (18 Oct):** if a fix removes or hides something Sam has already seen (a prop, a person,
  a joke, a landing in shot), name it in the message as a loss, so he can say no before it goes in. (Shocking
  Behaviour: fixing the pens sent the mug out of shot, and it was only mentioned in passing.)
- **Flag your own additions:** anything I didn't ask for (a sign, a reflection, a new joke, a sound) is named as your
  addition in the message, so I can say no before it costs a round.
- **Motion-led films (stunts, action): after the cast sheet, go to a quick animatic early**; stills can't show timing,
  camera moves or physics (Roadster: I asked to skip the stills and see it moving).
- **Test pictures are expensive, so look at as few as possible.** Check a change on one combined sheet (several small frames
  side by side) rather than one picture at a time; open a frame full size only for a detail a small one can't show; never
  look again at a picture that hasn't changed; and when a fix is simple and certain, trust it and check it with the rest
  at the end.
- **No sound effects unless the script specifies them or I ask for them.** Voices only by default.
- For TikTok versions, follow `guides/tiktok-design.md` (size, title, Hook Text, safe areas, posting). No title by default (Sam, 15 Oct): the cranberry
  title stays available, used only when asked for; Hook Text (the line introducing the joke) is TikTok's white-box caption style, for readability. Say how long each render will take, report how long it took, and send a push notification when it finishes.
- **Every TikTok video ends with the CranbriJoos sign-off** (the profile beaver sipping from the carton, with Sam's
  slurp, 2 s; Sam, 15 Oct: brand identity is worth a small dip in completion). Finish every film with
  `python3 source/finish.py CLEAN.mp4 animations/NAME-vertical.mp4 ["Hook Text"]`, from the clean untitled render kept
  in `source/data/`; it adds the Hook Text and the sign-off. The slurp is the one standing sound effect.
- **Push notifications for anything long:** whenever a render or any other long process (animatic, storyboard, sound build, upload, research) finishes, fails, or stops to wait for my decision, send a push notification to my phone saying what is ready or what is needed (details in `guides/tiktok-design.md`, "Working").
  **Also at every major stage end and every handover (Sam, 24 Oct, all films):** when a film's stage is finished (planning,
  building, stills, animatic, final...) or a new chat is needed, send a push notification saying what is done and what
  to do next (for example "Building done: cast sheet and clips ready. Start a new chat on Opus medium").
- I only have an iPhone and this app, no computer. When an animation is finished, **send the file to me directly in the chat** so I can tap it and save it to my Photos. Never give me steps that need a computer.
- The tools (Python with Pillow, NumPy, imageio and a bundled ffmpeg) are installed automatically at the start of each session by `.claude/hooks/setup.sh`.

# Where things stand

- **One main line of work:** `claude/create-claude-md-oe8z4g` (GitHub's default branch) holds everything. Every chat
  starts from it; before starting, check `git branch -r` for newer work on other branches and merge it in; at the end,
  merge back into it. Never leave a tool or lesson only on a side branch (the new limbs once were, 14 Oct).

- **Short two-person film ("quick video"): read only `guides/quick-video.md` and nothing else below.** Don't open other
  guides or the big source files. Use Sonnet at medium effort, and ask me for all my notes in one batch after the one
  stills sheet.
- **Satire-style film (the TikTok parody series, beyond two people talking): read `guides/satire.md` (one page) first**,
  start from `source/satire_template.py` (always: it carries the house style and the checks; Shocking Behaviour
  didn't, and lost rounds to boxy limbs and a missing audit), and open `guides/best-practice.md` Part 2 only for a
  scene that page doesn't cover. **Also follow best-practice Part 1 sections 1.2 and 1.3 (contact and continuity)
  for every film** (19 Oct: Poker Mon skipped them, and its table emptied between shots and its chips slid untouched). **Reuse before building:** the plan names which kit part does each person,
  movement and prop (`guides/satire.md`, Movement); build new only where nothing fits, and say so.
- **Every film (not quick videos): follow `guides/film-quality-rules.md` (Sam approved all 11 rules, 21 Oct).** Plan the world
  once, benchmark against references, run the collision, pop-in and script audits before showing Sam anything, rehearse
  the risky moves as clips, and fix each kind of note once in the shared kit. Rules marked [tool] need a tool still to be
  built; do the check by hand until it exists.
- **Any other film:** read `guides/best-practice.md` (the master file) before starting or changing it. Part 1 holds general
  animation principles; the later parts hold rules for one kind of project only (the TikTok parody series, the
  coloured-pencil shorts, the horror trailer) and must not be applied to others. Add each new lesson to the right part
  as soon as it is learned.
- Read only the section of `story/status.md` for the film in hand (list the sections with `grep -n '^## ' story/status.md`),
  not the whole file.

# Drawing people (not for quick videos)

- Hands are always a plain circle at the end of the arm, with props laid over it (South Park style).
- Satire-style films: everything (style kit, cast sheet, checks, audit, picture cache) is in `guides/satire.md`. Big film file?
  read its code map first (`python3 source/codemap.py FILE.py`; `guides/russiadent-map.md` is the biggest film's).
- For the flat cartoon films (the TikTok parody series), read `guides/figure-rig.md` before building or animating any
  person, and follow `guides/preflight.md` from the first brief: run `python3 source/preflight.py FILM OUT_DIR`
  before every animatic, and `python3 source/voices.py FILES` as soon as recordings arrive.
- **Yuletide horror trailer only** (skip these for the TikTok films):
  - before building or changing any character, read `guides/character-anatomy.md` and follow its checklist; build people on
    the free MakeHuman human model (CC0) rather than sculpting bodies from scratch;
  - before animating anything, read `guides/movement.md` (timing of eyes, blinks, smiles, hair and body);
  - before making or changing a shot, read `guides/pipeline.md` (how shots are built from reusable parts and recipes);
  - the story and the director's decisions for the animation test are in `story/animation-test.md`;
  - the film's premise and hidden backstory are in `story/yuletide.md` (never reveal the backstory in the trailer);
  - before rendering, run `python3 source/horror_preflight.py` (every pose of every frame, about a minute); render with
    `shot.py sequence ... --reuse`; check every new drawing with `python3 source/lookbook_check.py OUT_DIR` against `lookbook/`;
  - the trailer should evoke the style and quality of an A24 horror film (the craft, never the brand): read
    `guides/tone.md` before planning or changing any shot.
