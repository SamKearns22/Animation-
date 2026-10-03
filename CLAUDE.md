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
- For TikTok versions, follow `guides/tiktok-design.md` (size, title, safe areas, posting). Say how long each render will take, report how long it took, and send a push notification when it finishes.
- **Push notifications for anything long:** whenever a render or any other long process (animatic, storyboard, sound build, upload, research) finishes, fails, or stops to wait for my decision, send a push notification to my phone saying what is ready or what is needed (details in `guides/tiktok-design.md`, "Working").
- I only have an iPhone and this app, no computer. When an animation is finished, **send the file to me directly in the chat** so I can tap it and save it to my Photos. Never give me steps that need a computer.
- The tools (Python with Pillow, NumPy, imageio and a bundled ffmpeg) are installed automatically at the start of each session by `.claude/hooks/setup.sh`.

# Where things stand

- **Read `guides/best-practice.md` (the master file) before starting or changing any film.** Part 1 holds general animation principles from recognised references; the later parts hold rules for one kind of project only (the TikTok parody series, the coloured-pencil shorts, the horror trailer) and must not be applied to others. Add each new lesson to the right part as soon as it is learned.

- Read `story/status.md` at the start of every session: what is done, what is open, and how to work within the budget.

# Drawing people

- Before building or changing any character, read `guides/character-anatomy.md` and follow its checklist.
  Build people on the free MakeHuman human model (CC0) rather than sculpting bodies from scratch.
- Before animating anything, read `guides/movement.md` (timing of eyes, blinks, smiles, hair and body).
- Before making or changing a shot, read `guides/pipeline.md` (how shots are built from reusable parts and recipes).
- The story and the director's decisions for the animation test are in `story/animation-test.md`.
- The film's premise and hidden backstory are in `story/yuletide.md` (never reveal the backstory in the trailer).
- Compare every new shot against the approved frames in `lookbook/` so the look stays consistent.
- The trailer should evoke the style and quality of an A24 horror film (the craft, never the brand): read `guides/tone.md` before planning or changing any shot.
