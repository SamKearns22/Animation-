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
- **Test pictures are expensive, so look at as few as possible.** Check a change on one combined sheet (several small frames
  side by side) rather than one picture at a time; open a frame full size only for a detail a small one can't show; never
  look again at a picture that hasn't changed; and when a fix is simple and certain, trust it and check it with the rest
  at the end.
- For TikTok versions, follow `guides/tiktok-design.md` (size, title, safe areas, posting). Say how long each render will take, report how long it took, and send a push notification when it finishes.
- **Push notifications for anything long:** whenever a render or any other long process (animatic, storyboard, sound build, upload, research) finishes, fails, or stops to wait for my decision, send a push notification to my phone saying what is ready or what is needed (details in `guides/tiktok-design.md`, "Working").
- I only have an iPhone and this app, no computer. When an animation is finished, **send the file to me directly in the chat** so I can tap it and save it to my Photos. Never give me steps that need a computer.
- The tools (Python with Pillow, NumPy, imageio and a bundled ffmpeg) are installed automatically at the start of each session by `.claude/hooks/setup.sh`.

# Where things stand

- **Short two-person film ("quick video"): read only `guides/quick-video.md` and nothing else below.** Don't open other
  guides or the big source files. Use Sonnet at medium effort, and ask me for all my notes in one batch after the one
  stills sheet.
- **Satire-style film (the TikTok parody series, beyond two people talking): read `guides/satire.md` (one page) first**,
  start from `source/satire_template.py`, and open `guides/best-practice.md` Part 2 only for a scene that page doesn't cover.
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
