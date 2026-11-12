# Working with me

I don't know how to code. **Explain in plain English** (say what any technical word means). **Make choices for me**:
pick what's best, do it, say briefly what and why. **Always say where the finished file is** and how to open it. I
have only an iPhone and this app: **send finished animations in the chat** so I can save them to Photos; never give
me steps that need a computer. The film rules are the rulebook, `guides/film-quality-rules.md`; what each stage reads
is in `guides/job-packs.md`.

# Messages to me
- **Say only what matters.** If you need something, the first line says what ("Need: Y or N for the animatic"); if
  not, there is no first line. **Done / Needs you / Next appear only with something in them.** About 10 lines unless I
  ask for more.
- **No code names or file internals** (they go in the film's notes). Name only files I'll open, and send them.
- **One line per note:** "8: fixed – the whale now knocks the helideck away. Clip sent." Anything a fix takes away or
  you add gets its own "Lost: …" / "Added: …" line, so I can say no before it costs a round.
- **Questions are numbered,** each answered by a number or Y/N, your pick first. **Every open decision, across all
  jobs, goes in one message.**
- **A "Checks:" line only when a check slipped or was at risk** ("Checks: X slipped (looked: fine because …)"). Never
  send something a check flagged without saying so.
- **A note I've given before is a warning:** find why the first fix failed before changing anything, and tell me (rule 30).
- **The handover's 3 lines go at the bottom of the message.**

# Files
Every file **under 50 MB**, aiming for a few MB per animation; tell me the size. Only the **finished version** goes on
GitHub, in `animations/` with a clear name; drafts stay off. **MP4** by default; a GIF only if I ask. The tools install
at session start (`.claude/hooks/setup.sh`).

# Asking me before you go on
- **Before any full render, offer an animatic** (a quick, lower-quality whole film) and wait for my Y or N. **Ask
  before a final render and wait for a clear yes**; "fix this before the final" is not a go-ahead.
- **Every animatic carries the Hook Text and the CranbriJoos sign-off**, made as the final is (`finish.py` on its
  clean render); the check sheet shows the Hook Text frame.
- **Before every animatic (re-renders too), show me the check sheet and wait for a clear yes**; a note is not a yes.
  **No animatic while a shot is missing anyone the brief puts in it**: say so instead.
- **"Just go" (or any override) skips waiting for my yes, never the checks:** every fault is fixed or named first.
- **Unattended runs stop after one animatic:** render, send, wait; never stack rounds I haven't seen.
- **Notes on movement get a short clip** of just those seconds (`final OUT --small --span T0 T1`); clips need no yes;
  a full animatic once the clips look right.
- **"Hold" means collect, don't act:** reply to each note with how you understood it and how you'll fix it, change
  nothing, do it all when I say go. **"Hold responses until all my notes are through": no replies at all** until then.
- **Critique-fix rounds:** after each batch of notes, up to three rounds on your own (render, critique, fix), each with
  a sheet or clip and a two-line summary; stop early for a taste call or anything that removes something I've seen.
- **The brief is a checklist:** every detail of my brief and notes goes in the film's notes as a list, ticked against
  the film before the first animatic.

# Rules are permanent
- **New rules and lessons are proposed first:** say what and where; wait for my numbers.
- **"I want a rule" (or "every film", "from now on", "always") means a permanent rule for all films:** reply with the
  exact wording and place; on my yes, write it in that same chat. Each rule is written once: in the rulebook with its
  check, or here if it's about working with me (listed in the rulebook's last table).
- **Every new rule replaces or merges an old one, or turns a by-hand rule into a check:** the rulebook never grows.
  **Before suggesting anything** (rule, tool or idea), search the rulebook and `guides/kit-catalogue.md`; each
  suggestion names the closest rule or tool and says what is new, or is dropped (Sam, 12 Nov).
- **Before every handover, search the film's notes for rule requests not yet written** and list them.

# Models and chats
- **Models by stage:** planning (brief, staging, questions) and building anything new: **Opus, high effort**. A round
  of my notes (deciding, fixing, clips) and building from a clear plan or sound: **Opus, medium effort**. Routine work
  (checks, check sheet, animatic, filing, final render, sending, saving), status questions: **Sonnet**.
- **Chats may open the next chat themselves, up to 8 in a row (Sam, 12 Nov):** each gets the handover's model and
  effort and its place ("chat 3 of 8"); first it checks it can save to GitHub, else it stops and tells me. Anything
  needing my yes stops the chain; once I answer, the count starts again at 1. After chat 8 or any stop, I start the
  next by hand. No scheduled check-ins unless I ask. The handover's bottom lines say what to type, the model, the
  effort and any file to attach. **A task started
  on the wrong model** says so and gives what to type. Anything needing my yes stops and waits. Never carry on into a
  stage that needs a stronger model inside one chat.
- **One wait per render;** never check on it repeatedly. **Push notifications** when a render or long job finishes,
  fails or needs me, and at every stage end. Say how long each render will take and took.

# Fresh chats and the handover
- **A fresh chat for every round and every cost warning;** change model only by starting a new chat. **The cost watch
  (rule 85):** amber, finish the step and hand over; red, hand over at once unless I type 'override'. Back after more
  than an hour to a chat on amber or red: the reply is the handover only.
- **The handover** is the film's ONE "Where things stand" (old ones to `notes/archive/NAME-handovers.md`), **15 lines at
  most**, in order: Rules that bite next (3, by number); Done; Next (model, effort and what to type); Needs Sam; Read
  (the pack in `guides/job-packs.md`, and any extra sections); Open rule requests; a "For Claude" line for code names.
  Update `story/status.md` (3 lines), commit and push. **Paste up to 3 lines at the bottom:** what's done, the model, and
  what to type in the next chat (left out while Next waits on my look or my yes). **Every handover and every message sending me to a new
  chat names the model AND the effort level**; a stage not listed above gets your pick and one line why.

# Reading little
- **Three layers:** this file; the one pack in `guides/job-packs.md` the handover names (only its sections); a rule,
  kit piece or guide section looked up only when it is named. Long printouts filtered to the faults (rule 19).
- **Notes:** finished notes go to `notes/archive/` at each handover; a film's whole notes file the day I say it's
  posted. A film's notes keep only the brief checklist, the estimate, open notes and Where things stand (under 4,000
  words). **Pictures:** one labelled sheet, full size only where it counts, never an unchanged picture again (rule 48).
  **Code:** a film's code opens with a MAP; read only the lines a note touches (rule 61).
- **Fewer rounds, not cheaper rounds:** before every animatic, moves are checked against the acting list (rule 74).

# Making the films
- **Every chat starts with the Animation- project selected**; without it, add it before any work and say so.
- **One main line:** `claude/create-claude-md-oe8z4g` holds everything. **At the start, list every branch (`git fetch
  --all; git branch -r`) and merge any newer work on the film or tool before building. At the end, push to the main
  line as well as the chat's own branch** (this file is my standing permission). If the main-line push is refused,
  say so; the handover's first line names the branch with the newest work, and the next chat merges it first.
- **Which film, which guide** (satire film, motion-led, flat people, Yuletide): `guides/job-packs.md`,
  "Film types". **Reuse before building** (`guides/kit-catalogue.md`); build new only where nothing fits, and say so.
- **Reference photos:** I send 2-3 when I have them; otherwise search once, slowly, 3 per place at most. **One failed
  try per source, then stop** and give me one numbered list of what to find, which angle and why. At the start of each
  film, try the other sources (Geograph, Openverse, Pexels, Unsplash, Library of Congress, NASA) and note which work.
- **Sound:** voices only, no sound effects unless the script names them or I ask. **I record every voice; never ask
  who voices them.**
- **TikTok** (`guides/tiktok-design.md`): no title by default; Hook Text in TikTok's white-box style. **Every video
  ends with the CranbriJoos sign-off** (the beaver sipping from the carton, my slurp, 1.6 s): `python3
  source/finish.py CLEAN.mp4 animations/NAME-vertical.mp4 --film NAME` (or `["Hook Text"]` for a film with no
  `HOOK`), from the clean render in `source/data/`.

# My accounts (Sam, 26 Oct)
- Channel and brand name on every platform: **CranbriJoos**. TikTok (main platform): `www.tiktok.com/@cranbrijoos`.
- YouTube Shorts is the second platform: same name and profile picture (`profile/cranbrijoos-tiktok-1080-eyes-open.png`,
  the beaver's face); every Short's description and pinned comment points back to the TikTok link.
