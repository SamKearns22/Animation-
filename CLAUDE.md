# Working with me

**Contents:** Working with me · Messages to me · Files · Asking me before you go on · Rules are permanent ·
Models and chats · Fresh chats and the handover · Reading little · Making the films. The film rules are in
`guides/film-quality-rules.md` (the rulebook).

I don't know how to code. Please:

- **Explain everything in plain English.** Avoid jargon; if you must use a technical word, say what it means.
- **Make choices for me rather than listing options.** Pick what's best, do it, and briefly say what you chose and why.
- **Always tell me where the finished file is** and how to open it.
- I only have an iPhone and this app, no computer. **Send finished animations to me in the chat** so I can save them
  to Photos. Never give me steps that need a computer.

# Messages to me
- **Say only what matters (Sam, 9 Nov).** If you need something from me, the first line says what ("Need: Y or N for
  the animatic"). If you need nothing, there is no first line. **Done / Needs you / Next appear only when they have
  something in them:** never an empty heading, "nothing needed" or "nothing was done". About 10 lines, unless I ask for more.
- **No code names or file internals.** Those go in the film's notes. Name only files I'll open (and send them).
- **One line per note:** "8: fixed – the whale now knocks the helideck away. Clip sent." Anything a fix takes away
  (a prop, a person, a joke, a landing in shot) and anything you add (a sign, a joke, a sound, set dressing) gets its
  own line, "Lost: …" / "Added: …", so I can say no before it costs a round.
- **Questions are numbered,** each answered by a number or Y/N, your pick first. **Every open decision goes in one message**
  (all jobs, not just the current one), so no chat is spent waiting on a single answer (Sam, 9 Nov).
- **A "Checks:" line only when a check slipped or was at risk:** "Checks: X slipped (looked: fine because …)". A clean
  result says nothing. Never send something a check flagged without saying so.
- **A note I've given before is a warning:** find why the first fix failed before changing anything, and tell me
  (rulebook 30).
- **The handover's 3 pasted lines always go at the bottom of the message** (Sam, 9 Nov).

# Files
- Every file **under 50 MB**; aim for **a few MB per animation**. Tell me the final size.
- Only the **finished version** goes on GitHub, in `animations/` with a clear name; drafts and test renders stay off.
- Default to **MP4**; a GIF only if I ask (short and small).
- The tools install at session start (`.claude/hooks/setup.sh`).

# Asking me before you go on
- **Before any full render, offer me an animatic** (a quick, lower-quality version of the whole film) and wait for my
  Y or N. **Ask before a final render and wait for a clear yes**; "fix this before the final" is not a go-ahead.
- **Every animatic carries the Hook Text and the CranbriJoos sign-off,** made the same way as the final
  (`finish.py` on the animatic's clean render), and the check sheet shows the Hook Text frame (Sam, 3 Nov).
- **Before every animatic (re-renders too), show me the check sheet and wait for a clear yes**; a note is not a yes.
  **No animatic while a shot is missing anyone the brief puts in it**: say so instead.
- **"Just go" (or any override) skips waiting for my yes, never the checks:** pre-flight still runs, and every fault is
  fixed or named before the render.
- **Unattended runs stop after one animatic:** render one, send it, and wait; never stack rounds I haven't seen.
- **Notes on movement get a short clip:** only the seconds around it, small (`final OUT --small --span T0 T1`). Clips
  need no yes; a full animatic comes once the clips look right.
- **"Hold" means collect, don't act:** reply to each note with how you understood it and how you'll fix it, change
  nothing, do it all when I say go. **"Hold responses until all my notes are through": no replies at all** until then.
- **Critique-fix rounds:** after each batch of my notes, up to three rounds on your own (render, critique, fix), each
  with a sheet or clip and a two-line summary. Stop early for a taste call or anything that removes something I've seen.
- **The brief is a checklist:** every detail of my brief and notes (wording, bleep counts, who stands where, colours,
  props) goes in the film's notes as a list, ticked against the film before the first animatic.

# Rules are permanent
- **New rules and lessons are proposed to me first:** say what you'd add and where; wait for my numbers.
- **"I want a rule" (or "every film", "from now on", "always") means a permanent rule for all future films.** Reply with
  the exact wording and where it goes; on my yes, write it in that same chat. Every rule is written once, in
  `guides/film-quality-rules.md` (the rulebook) with the check that tests it, or in this file if it's about working
  with me (and listed in the rulebook's last table).
- **Every new rule replaces or merges an old one, or turns a by-hand rule into an automatic check** (Sam, 9 Nov): the
  rulebook never gets longer, because every rule is re-read in every new chat.
- **Before every handover, search the film's notes for rule requests and proposals not yet written** and list them.

# Models and chats (to save money)
- Each stage has a model:
  - planning (the brief, staging, questions for me) and building anything new (a character, creature, set or tool):
    Opus, high effort;
  - **a round of my notes** (deciding the fixes, applying them, the clips): **Opus, medium effort**; building from a
    clear plan or sound: Opus, medium effort;
  - routine work (the pre-flight and other checks, the check sheet, the animatic render, filing recordings, a final
    render, sending, saving), quick videos, **status questions and quick answers**: **Sonnet** (Sam, 8 Nov: put back; once the fixes are made, the checks
    and the animatic go to Sonnet).

  **Chats chain themselves (Sam, 10 Nov):** at every handover (a stage's end, a round's end, amber or red) the chat I
  started opens the next chat itself (create_session: the right model and effort, the handover's line as its prompt),
  checks on it once per stage (send_later, under an hour) and tells me which chat to open; chats it starts cannot
  start chats, so they hand over and stop. A round of my notes chains too: once I say go, the notes chat (Opus medium)
  fixes, then opens the Sonnet chat for the checks and the animatic. **If I start a task on the wrong model, the chat
  opens the right one itself** and says which to open. Anything that needs my yes (an animatic, a final, a rule, a
  taste call) still stops and waits. Never carry on into a stage that needs a stronger model inside one chat.
- **One wait per render:** wait once for a render or long process to finish; never check on it repeatedly.
- **Push notifications** whenever a render or long process finishes, fails or needs my decision, and at every stage
  end. Say how long each render will take and how long it took.

# Fresh chats and the handover
- **Fresh chat at every round and every cost warning** (every step re-reads the whole chat). Each round of my notes (one
  animatic, or one batch of clips) ends with the handover, and the next round starts a new chat. Change model only by
  starting a new chat, never inside one.
- **The cost watch (rule 85) decides 'long':** on amber, finish the step and hand over; on red, hand over at once unless
  I type 'override'. If I come back after more than an hour to a chat on amber or red, the reply is the handover only
  (Sam, 9 Nov: two chats ran 18 and 22 hours and cost about 37% of a week).
- **The handover** is the film's ONE "Where things stand" section (old ones go to `notes/archive/NAME-handovers.md`),
  **15 lines at most**, in this order: Rules that bite next (3, by number); Done; Next (model and what to type in the
  new chat); Needs Sam; Read (which sections of which guide); Open rule requests. Code names go in a "For Claude" line
  at the end. Update `story/status.md` (3 lines), commit and push. **Paste only 3 lines into the chat** (at the bottom
  of the message): what's done, the model, and which chat was opened for it (what to type only if none could be). **Every handover, and every message that
  sends Sam to a new chat, names the model AND the effort level** ("Opus, high effort"), matching the build plan or the
  stage list above; a stage not listed gets my pick and one line of why (Sam, 9 Nov: a handover that said only "Opus"
  started Job E on medium).

# Reading little
- **Notes:** at each handover, finished notes move to `notes/archive/`; **a film's whole notes file moves there the day
  Sam says it's posted** (Sam, 9 Nov). The film's notes file keeps only the brief checklist, the estimate, open notes
  and 'Where things stand' (under 4,000 words).
- **Pictures:** one labelled sheet, full size only where it counts, never an unchanged picture again (rulebook 48, 79).
- **Code and guides:** a film's code starts with a short map and only the lines a note touches are read (rulebook 61);
  only the guide sections the handover names. Long check printouts are filtered so only the faults are read (rulebook 19).
- **Fewer rounds, not cheaper rounds:** before every animatic, the moves are checked against the film's acting list
  (rulebook 74) on the check sheet; a slip caught on a sheet costs a fraction of a re-render.

# Making the films
- **Every chat starts with the Animation- project selected** (Sam, 9 Nov): without it the cost watch and the tools never
  start. If a chat finds itself without it, add the project before any work and say so.
- **One main line of work:** `claude/create-claude-md-oe8z4g` (GitHub's default branch) holds everything. Start from
  the newest copy on GitHub, merge in any newer work from other branches, and push back at the end.
  **At the start of every chat, list every branch (`git fetch --all; git branch -r`) and look for newer work on the
  film or tool being worked on before building anything** (Elder Scrolls: Swindon, 8 Nov: a chat started from the
  main line, never saw the other chat's finished film and animatic, and rebuilt parts of it). **At the end of every
  chat, push to the main line as well as the chat's own branch,** so the next chat cannot start from an old picture
  (this file is Sam's standing permission for that). If the cloud session refuses the main-line push, say so, and the
  handover's first line names the branch with the newest work; the next chat's first step is to merge it (Sam, 9 Nov).
- **Quick video (short two-person film): read only `guides/quick-video.md`.** Sonnet, medium effort.
- **Satire-style film (the TikTok series, beyond two people talking): read `guides/satire.md`**, start from
  `source/satire_template.py` (always), and follow the rulebook, `guides/film-quality-rules.md`. **Reuse before
  building:** `guides/kit-catalogue.md`; build new only where nothing fits, and say so. `guides/best-practice.md` Part 2
  only for a scene satire.md doesn't cover.
- **Motion-led films (stunts, action): go to a quick animatic early** after the cast sheet.
- **Reference photos (Sam, 8 Nov):** Sam sends 2-3 photos with the brief when he has them to hand; otherwise Claude
  searches once, slowly, and keeps 3 photos per place at most. **One failed try per source, then stop** (a network that
  says it is connected may not be): give Sam one numbered list of what to find, which angle and why, to fetch by hand.
  At the start of each film, try the other sources (Geograph for UK places, Openverse, Pexels, Unsplash, Library of
  Congress, NASA) and note which work here (Sam, 9 Nov).
- **Flat cartoon people:** read `guides/figure-rig.md`; follow `guides/preflight.md` from the first brief. Hands are
  always a plain circle with props laid over it.
- **Yuletide horror trailer** (a separate experiment): read `guides/yuletide/yuletide-trailer.md`; next time it starts
  from the newest engine. Nothing in `guides/yuletide/` applies to the TikTok films.
- **Sound:** no sound effects unless the script names them or I ask; voices only by default. **I record every voice in
  these films; never ask who voices them.**
- **TikTok:** follow `guides/tiktok-design.md`. No title by default; Hook Text in TikTok's white-box caption style.
  **Every video ends with the CranbriJoos sign-off** (the beaver sipping from the carton, my slurp, 1.6 s): finish with
  `python3 source/finish.py CLEAN.mp4 animations/NAME-vertical.mp4 --film NAME` (or `["Hook Text"]` for a film with no `HOOK`) from the clean render in `source/data/`.
