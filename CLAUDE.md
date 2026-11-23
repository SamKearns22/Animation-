# Statement One: top quality, within 15% of a week (Sam, 22 Nov)

**Every film aims at the quality Sam's notes and the rulebook ask for, and costs no more than 15% of a week's
allowance. Quality is never cut to fit the budget. Cost comes down only by working smarter: reusing what's built,
catching faults before Sam sees them, and reading less. Every rule below serves these two aims.**

# Statement Two: be honest about what I can do (Sam, 21 Nov)

**Be honest. If something isn't currently within my capabilities, say so and suggest what I would first need to learn
or have, instead of trying to use the wrong tools to make something happen.** (A wrong-tool workaround that only looks
like it worked is worse than saying "I can't yet".)

# Fix the drawing, never the shot (Sam, 21 Nov)

**Sam's approved shots are locked: the script, the shot order and lengths, each camera and framing, and what happens in
each shot.** When a drawing is wrong, fix the drawing. Never change a camera, framing, shot or screenplay beat to hide
or avoid a fault, even if the view is hard to draw. If a view seems not to work, first say in plain words **what the
project would need to learn** to draw that shot or movement well (a new way of drawing, a tool, a reference, a test),
and start learning it; only then, if it still can't be done, ask Sam, with any alternative as a numbered question.
**Every handover has a "Locked by Sam" line** naming the cameras and beats that must not move.

# Seeing like Sam (read first, every chat; Sam's Y, 21 Nov)

**Sam should never have to teach a fault twice. Every note he gives is proof that a check failed to see something,
so fix the seeing as well as the frame.**

1. **Look as a viewer, not as a measurer.** Passing numbers prove nothing about how a frame looks. Before anything goes
   to Sam, watch it at phone size, then study every character and every point where two things meet (hands on
   objects, feet on the ground, a body against furniture or a wall) at full size, in every frame that moves. Ask of
   each: "Would a stranger believe this without effort?" If the answer isn't an easy yes, it is a fault.
2. **Every note becomes a lesson the checks keep.** Sam's words and marked-up pictures are saved as examples. A check is
   only finished when it would have caught that note on its own; new checks are tested against every earlier note
   before they are trusted.
3. **Before fixing a frame, ask why nobody saw it.** Name the check that should have caught it and improve that check,
   then fix the frame. A note given twice means the first fix only patched the picture.
4. **Choose views the drawing can carry** (for a NEW shot; never for a shot Sam has already approved: see "Fix the drawing, never the shot"). Our style is flat drawings; some camera angles and poses break them (very
   close, from behind, a limb pointing straight at the lens). Such a view is a fault in itself, ruled out before
   anything is drawn.
5. **Physical things behave physically.** Everything has weight, solidity and cause and effect. Nothing passes through
   anything. What is touched, pushed or struck responds in proportion; what rests on something sits on it; marks and
   objects attached to a surface move and turn with it. Every action gets a reaction that reads from this camera.

# Working with me

**Plain words, always.** Every message to me is in plain words. Any technical word is explained where it appears, or replaced by a simpler one. I can't follow code names, file names or jargon. Read this again before every message that asks me to decide something. (Sam, 19 Nov. If this isn't followed, the next step is a checker that sends a message back: notes/proposals/plain-check.md, option 1.)

I don't know how to code. **Explain in plain English** (say what any technical word means). **Make choices for me**:
pick what's best, do it, say briefly what and why. **Always say where the finished file is** and how to open it. I
have only an iPhone and this app: **send finished animations in the chat** so I can save them to Photos; never give
me steps that need a computer. The film rules are the rulebook, `guides/film-quality-rules.md`; what each stage reads
is in `guides/job-packs.md`.

# Messages to me
- **One message, never twice (Sam, 22 Nov):** if a checker stops a reply after Sam has seen it, the resend is only
  the changed line, never the whole message again.
- **Say only what matters.** If you need something, the first line says what ("Need: Y or N for the animatic"); if
  not, there is no first line. **Done / Needs you / Next appear only with something in them.** About 10 lines unless I
  ask for more.
- **No code names or file internals** (they go in the film's notes). Name only files I'll open, and send them.
- **One line per note:** "8: fixed – the whale now knocks the helideck away. Clip sent." Anything a fix takes away or
  you add gets its own "Lost: …" / "Added: …" line, so I can say no before it costs a round.
- **Back-end proposals are explained plainly.** Anything I propose that you can't see (a
  check, a tool, a rule, a change to how the films are built): the problem in one or two plain sentences, then what's
  proposed as numbered steps, then why, what you'd notice, and the other option. One "Lost:" / "Added:" line each. No
  code names; any technical word is explained where it appears. This may run over the 10-line limit; never skipped.
- **Questions are numbered,** each answered by a number or Y/N, your pick first. **Every open decision, across all
  jobs, goes in one message.**
- **A "Checks:" line only when a check slipped or was at risk** ("Checks: X slipped (looked: fine because …)"). Never
  send something a check flagged without saying so (the checks print that line ready).
- **A note I've given before is a warning:** find why the first fix failed before changing anything, and tell me (rule 30).
- **The handover's 3 lines go at the bottom of the message** (never a request to start a chat myself, see Models and chats).

# Files
Every file **under 50 MB**, aiming for a few MB per animation; tell me the size. Only the **finished version** goes on
GitHub, in `animations/` with a clear name; drafts stay off, **except the latest animatic and its clean render**, kept in
`animations/drafts/` (finish.py saves them; push them; emptied when the film is posted). **MP4** by default; a GIF only if I ask. The tools install
at session start (`.claude/hooks/setup.sh`).

# Asking me before you go on
- **Before any full render, offer an animatic** (a quick, lower-quality whole film) and wait for my Y or N. **Ask
  before a final render and wait for a clear yes**; "fix this before the final" is not a go-ahead.
- **Every animatic carries the Hook Text and the CranbriJoos sign-off**, made as the final is (`finish.py` on its
  clean render); a check sheet, when I ask for one, shows the Hook Text frame.
- **No check sheet before an animatic unless I ask**: once the checks pass (every fault fixed or named),
  render the animatic and send it; my notes come on the animatic itself.
  **No animatic while a shot is missing anyone the brief puts in it**: say so instead.
- **"Just go" (or any override) skips waiting for my yes, never the checks or the hand-over:** every fault is fixed
  or named first; at red the chat opens the next one, which carries on without asking.
- **Unattended runs stop after one animatic:** render, send, wait; never stack rounds I haven't seen.
- **Notes on movement get a short clip** of just those seconds (`final OUT --small --span T0 T1`); clips need no yes;
  a full animatic once the clips look right.
- **A question about the film is answered, not acted on**: reply with the answer and the plan (what I'd
  change and how), then wait for his Y before changing anything.
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
- **Every stage aims at Statement One (top of this file), with fewer notes and faults; its checks are made smarter, improved and condensed toward them. Something new? First improve the check that missed it; then merge overlapping checks; remove a step only if it
  caught nothing in three films, with my Y on a "Lost:" line.** It stays if the next film is cheaper or gets fewer notes.
- **The channel is topical, absurdist news-of-the-week satire; every film is new.** Every idea for cost or
  speed makes new things better, cheaper or faster: smarter tools, faults caught before Sam sees them, reading less.
  Never suggest doing less, making it worse, trimming the joke, or repeating old characters, places or material. Reuse
  means the means (rig, hands, poses, house look, checks), never the content.
- **The proposal route:** "Every change to
  rules, tools, checks, kits or how films are built that is put to Sam goes through the proposal route first (helpers,
  blind judge, top two in plain English with Lost/Added and Critiqued). The guard refuses an unjudged ask. Changes made
  without asking are listed and judged in the end-of-film review against the film's results." (`source/propose.py`)
- **Before every handover, search the film's notes for rule requests not yet written** and list them.

# Models and chats
- **Models by stage:** planning (brief, staging, questions) and building anything new: **Opus, high effort**. A round
  of my notes (deciding, fixing, clips) and building from a clear plan or sound: **Opus, medium effort**. Routine work
  (checks, check sheet, animatic, filing, final render, sending, saving), status questions: **Sonnet**.
- **Chats open the next chat themselves (create_session), with no count:** each gets the
  handover's model, effort and its place ("chat 3"); first it checks it can save to GitHub, else it stops and tells me.
  **The Animation- project is always attached** (`source_url` of the repo, revision the main line), and the reply must
  list it before I'm told the chat is working.
  **The chain stops only at the budget stop (rule 24), a question for me, a failed save, or a chat that pushed no new work
  on its job. I never start a chat or type a prompt unless it failed to save.** When a chat ends on a question
  for me, my answer comes back to that chat, which (or the chat it opens, if it is on amber or red) carries straight on;
  the chain then goes on. A chat on the wrong model for its next stage opens one on the right model, never
  carries on, up or down: an Opus fix ends by opening the Sonnet chat for the animatic, finish.py and sending.
  **Chat size:** a chat aims at about 100 steps, up to 150 to finish a stage, and never hands over mid-fix. No chat
  ends under about 40 steps, except notes after more than an hour's gap or a whole routine stage on Sonnet;
  routine stages always go on Sonnet.
  No scheduled check-ins unless I ask. A message never says "start a new chat" or "type ...": it says what
  is done and what I'm needed for.
- **One wait per render;** never check on it repeatedly. **Push notifications** when a render or long job finishes,
  fails or needs me, and at every stage end. Say how long each render will take and took.

# Fresh chats and the handover
- **A fresh chat for every round and every cost warning;** change model only by starting a new chat
  (switching a long chat's model re-pays its whole history; for Sonnet, I say "hand over to Sonnet"). **The cost watch
  (rule 85):** amber, finish the step and hand over; red, hand over at once unless I type 'override'. Back after more
  than an hour to a chat on amber or red: the reply is the handover only.
- **The handover** is the film's ONE "Where things stand" (old ones to `notes/archive/NAME-handovers.md`), **15 lines at
  most**, in order: Rules that bite next (3, by number); Done; Next (model, effort, what it does); Needs Sam; Read
  (the pack in `guides/job-packs.md`, and any extra sections); Open rule requests; a "For Claude" line for code names.
  Update `story/status.md` (3 lines), commit and push. **The handover check:** `python3 source/handover.py end
  --film NAME` before every handover; first thing in a chat, `handover.py start PARENT_SESSION --film NAME`; every
  fault it lists is fixed, written in the notes or answered first. **The 3 lines at the bottom** say what's done and what's
  next; "what to type" only when the chain has stopped for good (no save). **Every handover names the next
  chat's model AND effort**; a stage not listed above gets your pick and one line why.

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
- **One main line:** `claude/create-claude-md-oe8z4g` holds everything. **At the start, merge or name (in the notes) every
  branch the start lists (only branches with work not on the main line; `source/branches.py scan`) before building. At the end, push to the main
  line as well as the chat's own branch** (this file is my standing permission). If the main-line push is refused,
  say so; the handover's first line names the branch with the newest work, and the next chat merges it first.
- **Which film, which guide** (satire film, motion-led, flat people, Yuletide): `guides/job-packs.md`,
  "Film types". **Reuse before building** (`guides/kit-catalogue.md`); build new only where nothing fits, and say so.
- **Reference photos:** the search order is in `guides/job-packs.md`, Plan.
- **Earlier chats can be read** (`list_sessions`, `list_events`): before asking me anything I may have answered
  already, or when a handover is unclear, look in that film's earlier chats first and say what you found.
- **Sound:** voices only, no sound effects unless the script names them or I ask. **I record every voice; never ask
  who voices them.**
- **TikTok** (`guides/tiktok-design.md`): no title by default; Hook Text in TikTok's white-box style. **Every video
  ends with the CranbriJoos sign-off**: the command is in `guides/job-packs.md`, Checks and animatic.
- **My accounts** (CranbriJoos, TikTok first, YouTube Shorts second): `guides/job-packs.md`, Final and posting.
