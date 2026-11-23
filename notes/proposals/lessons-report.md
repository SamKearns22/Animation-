# The Milburn lessons: what changed, and how it should behave (Sam's ask, 22 Nov ~23:10 UK)

Sam: "Please report back on all changes rules and what the difference you have made is, and how it should behave in
the future." One entry per lesson, written by the chat that builds it. The chat that builds brow-limit (the last of
chain B) sends the whole page to Sam in plain words.

## 1. staging-stills: no shot is built before Sam has seen its framing (built 22 Nov, chain B chat 1)

**The look back first (step 1).** Over four films (Milburn, Patriots 4, Blessed, European Protests Ranked), 5 framings
Sam had to give a note on twice were all built and sent as clips before he saw any picture of them. Milburn's Cabinet
Room shot was built three times; its weapon-picking shot needed "still poorly composed". The one time a still came
first (Patriots 4's wide view), his "no" cost a picture, not a round. So the change was made.

**Rules changed: rule 11 and rule 87**, written 23 Nov on Sam's "Y to all" (05:51 UK), word for word as shown to him:
- Rule 11, before: "Each is sent once: notes on it are acted on, never sent again." Now: "Each is sent once; a
  shot whose framing changes (a note about framing or staging) goes on a new board before it moves: first a sheet of
  2-3 numbered framings, one of them the screenplay's camera line taken literally, then Sam's number, then the shot as
  built on the board." Check column adds: the clip and animatic refusals (staging tool) and their two tests.
- Rule 87, before: "A fix that fails twice stops rendering: the next send is one still sheet of 2-3 options for Sam to
  pick from." Now adds: "A note about framing or staging gets that sheet at once, not after two failures (rule
  11)." Check column: "framing notes: the staging tool (rule 11)".

**Tools added (on Sam's option 1).** A new check runs every time a clip or animatic is drawn. It refuses any shot
that (1) has never been on a shot board Sam received (new shots included), (2) is held by a framing note until Sam
has picked a number from 2-3 framings and the shot, built to his pick, has been on a board, or (3) has a note whose
words read as framing that nobody has routed yet. Before, the board check ran only at the animatic and asked only
whether a shot had ever been on a board, so clips of unseen framings went to Sam freely.

**Difference made.** Measured on the record: replaying Milburn, the check refuses chat 6's first build of the Cabinet
Room shot and chat 10's re-stage (the two builds Sam then re-noted), and lets shot 1 through. The note-finder finds all
29 framing notes in the four films and flags 52 of 205 notes (a wrong flag costs one line to clear). On a real film:
**not measured yet**: measured at the end of the next new film from the hold record: framings built before Sam saw
them (Milburn 2, target 0) and staging notes given twice (Milburn 2 by the look back, target 0).

**Verified working (23 Nov).** A made-up film was taken through every step with the real clip command: refused
at each stage it should be, rendering once Sam's number and the new board were recorded; a real Milburn clip still
renders normally; all six related tests pass.

**How it should behave from now on.** When Sam gives a note about where people are or how a shot is framed, his reply
is one picture of 2-3 numbered framings (one exactly as the script describes, and "0: none of these, say what
instead"); he answers with a number; that shot then waits while every other shot carries on. The shot is built to his
number, shown on the board as one still, and only then animated. A new shot never reaches him first as a clip. On an
overnight run a held shot waits for his number; the rest of the work goes on. If he says "just build it", that is
recorded with his words and the shot is released. Not covered: a chat re-framing a shot on its own with no note, and
Grand Theft Autism (its own renderer; Sam overruled its checks).

## 2. named-lines: every warning gets an answer, and "couldn't look" stops the line (learned 23 Nov, chain B chat 2)

**The look back first (the learning step; changed nothing).** Milburn's checks printed the same 61 warnings at every
animatic. Sorted: 37 were the checks being blind (the film never handed them what they need to see it), 8 were plain
wrong about the film (plus 60 more wrong voice warnings that a fix inside Milburn's own code removed), 14 were real but
chosen (captions too fast because Sam speaks fast), 2 were never settled, and none was a real fault on its own. But one
blind warning ("could not test" for things passing through each other) hid the name-card fault Sam noted twice.
Blessed shows the other side: once its checks were handed what they needed, 99 warnings, mostly noise, became 17 mostly
real ones, all fixed or answered within two chats. Sam notes that were already a printed warning: 3 (Milburn's name
cards, Blessed's newsreader mouth, likely Blessed's cot pose). 10 check fixes were made inside one film's own code in
three films, so each new film starts without them. Shared-tool tests failing now: 4 of 112 (2 can't run here because a download is blocked, 2 real; the one the proposal named, round_page, is already repaired).

**Rules changed (Sam's Y Y Y, 23 Nov).**
- Rule 59, before: "faults Sam has been told about need `--faults-named`, and each is listed once: the film keeps a
  named-faults list and pre-flight shows only faults not on it." Now (written): "every fault left needs its own written
  answer in the film's exceptions list (chosen or real; why; where it was looked at full size; who fixes it), or the
  render refuses; a fault whose check could not see the film cannot be answered, only cured by handing the check what
  it needs; an answered fault comes back if its numbers change; pre-flight prints how many are answered and every
  unanswered one in full." Its check column names the new tool and two kittests.
- Change 1 ("could not test" stops the animatic): built once, by the could-not-test chat (already in the render lock).
- Change 2 BUILT (chain B chat 2): the one switch is gone everywhere it waved a list through: pre-flight's pass, the
  render's picture checks (a held video is released by answering each line, no second render), the body check (one
  reason for the whole list is refused; GTA's 11-at-once naming can't happen again) and finish.py's Hook Text and
  readable checks. Not changed: the critique gate (rule 89), whose faults already go to Sam one by one in the Checks line.
- Change 3 BUILT (chain B chat 3, 23 Nov): **the shared kits hand every check what it needs, read from the drawing
  itself.** Before: a check saw a film only if that film's own code built its inputs (Blessed did, in 7 places;
  Milburn did not, so 37 of its 61 warnings were checks that could not see it). Now one shared step draws the film
  about 4 times a second and records who the people kit draws where, which way they face, which places view is
  painted, and every piece with words on it. From that the checks get, only where the film gave nothing: who is in
  each shot, pop-ins, a camera per shot, facings, the camera's movement measured from the frames, the props with
  words (measured on screen), the real sizes of places pieces, each person drawn alone for the line check, and their
  hems for the clothes check. People with no places view get their distance from how big they are drawn. Three plan
  checks were wrong for every film and are fixed in the shared check: places with no doorway between them are
  separate places; a floor-flat platform is stood on, not stood inside; a tilted camera says where it looks.
  Voices: Milburn's take cleaning is now a shared tool; the voice check hears the cleaned take the film plays, and
  says so out loud when it would read a raw file the film does not play.
- **The "move to shared" stop (built, chain B chat 3):** a check fix written inside one film's code (a film with its
  own renderer, like Grand Theft Autism, counts) stops the handover until it is moved to the shared tools, or Sam
  says it stays (an Exceptions row with his Y). It is the check for Sam's 23 Nov words below.
- Change 4 BUILT (chain B chat 3), on chain A's handover gate: a kit test red at two handovers in a row, or one that
  could not run, stops the handover (closed: never named away). Red once is a plain line. Each handover's red tests
  are kept (notes/logs/kittest-reds.log), so "two in a row" is counted, not remembered. The long-red sentence test is
  fixed: it now knows the sentences Sam himself rewrote (Statements One and Two) are not "lost".

**Difference made.** Measured on Milburn's saved lines (kittest named_lines_each_answered): all 61 now stop the render
until answered (before: all 61 passed with one switch); the 37 blind ones cannot be answered at all, including the
"could not test" line that hid the name cards; an answered caption comes back the moment its timing changes. On a real
film: not measured yet (at the next film's first animatic). The numbers to beat, from the look back:
Milburn's replay with changes 2 and 3 should leave at most the 16 chosen or unsettled lines, each answered (today 61
named in a bunch plus 60 removed by hand); the next film: under 10 unanswered lines before every animatic, 0 blind
lines at its first pre-flight, and 0 Sam notes that were already a printed line (3 in the last two films).

**Difference made by changes 3 and 4 (measured 23 Nov, chain B chat 3).** Replaying Milburn with today's checks and
no film code: its quick check went from 68 lines to 36. Of its 37 blind lines, 31 are cured; 6 stay, each named for
what is missing: shot 2b's four tiny figures (drawn by Milburn's own set code, not the people kit, so no shared tool
can see them: the cure is a far-figure piece in the people kit), no camera for shots 3 and 6 (hand-drawn places, no
places view), and the "each body alone" audit (needs the render's drawing pass to keep each person's own drawing).
Its 8 false plan lines: 0. Voice: with Milburn's own hand-over taken away, 2 lines (the two never-settled syllable
counts), 0 false; reading the raw files gives 85. Now that the checks can see Milburn, they found new lines the old
list never showed: line weights on the kit's people, and a fireplace 2 m wide against a real 1.3 m (to judge on the
next film, as the kit's people are every film's people). The move-to-shared stop catches all 10 film-code fixes the
look-back found (Blessed 7, Milburn 1, Grand Theft Autism 2) and no shared file. On the next film: not measured yet;
the bar is 0 blind lines at its first pre-flight, judged at its first animatic. Cost: the shared survey adds about 50
seconds to each pre-flight (drawing the film 4 times a second); it replaces the film code each film used to need.

**How it should behave from now on (on Sam's yeses).** A warning is never waved through in a bunch. If a check could
not look at the film, the animatic stops until the film or the shared tools give it what it needs. Every other warning
left gets one written line: why it stays, where it was looked at full size, and who fixes it; if its numbers change it
comes back. Sam's "Checks:" line gets short: a count of answered warnings and only the unanswered ones in full. A check
fixed inside one film is flagged until it is moved into the shared tools, so the next film starts with it.

**Sam's words on this (23 Nov): "I would have expected the change on Blessed to apply to all films in the future —
rules need to be constructed that they work in this way, they are not film specific."** Proposed wording (asked 23
Nov), CLAUDE.md "Rules are permanent": "**Every rule and fix is for all films (Sam, 23 Nov):** a fix made because of one
film's fault goes into the shared tools, template, rulebook or checks so every later film gets it; a fix that can only
live in one film's code gets a 'move to shared' line in that film's notes, and the handover check stops until it is
moved or Sam says it stays." Its check: the "move to shared" handover stop (named-lines change 3).
Sam said Y with "needs testing" (23 Nov); chain B chat 2 wrote it in CLAUDE.md "Rules are permanent". Chat 3 built the
stop and tested it as asked: on the saved code it stops on all 10 film-code fixes of the last three films, never on a
shared file, and lets through one Sam has said may stay. The rule now counts as proven (kittest
move_to_shared_catches_film_fixes). Building it found and fixed one fault in the stop itself: it crashed on a film
whose notes are archived (Blessed). **Sam: "Y but
needs testing" (23 Nov). Written** in CLAUDE.md "Rules are permanent" (before: no such line; fixes often stayed in one
film's code). Not proven yet: it counts as a working rule only when the stop catches Blessed's 7 film-code check fixes,
Milburn's voice takes and GTA's solids on the saved code (chain B chat 3 builds and tests it). From now on: a fix made
for one film's fault is made in the shared tools; anything that can only live in a film's code is listed and stops the
handover until moved or kept on Sam's say.

## 3. guard-film-questions: a stopped message is corrected in one line, never sent again (built 23 Nov, chain B chat 4)

**The look back first (the learning step; changed nothing).** The guard (the checker that reads each reply after you
have already seen it, and stops one that asks you to approve a change to how films are made before helpers and a judge
have looked at it) stopped 51 replies between 15 and 23 Nov. Each was read and sorted. Only 12 could be read in full:
the chats behind the other 39 (15 to 21 Nov) have been deleted, so those were sorted from the logged question alone.
- Right to stop: 18 (11 named a judged proposal but left out its "Critiqued" count line; 7 asked you to approve a
  change nobody had judged). 8 of the 11 are not certain, because the deleted chats can't show whether the count was
  there in other words.
- Wrong to stop: 33. 7 were about the film itself (a recording, a shot, the effects, Hook Text options); 7 asked
  whether to start, queue or restart a chat; 10 asked whether to START the judging process; 3 had the right count in
  other words; 4 took a file that is not a proposal for one; 2 only asked what you meant.
- Whole replies sent to you again after a stop: at least 3 of the 12 that could be read (22 Nov 17:03, which you saw
  three times; 22 Nov 23:17, after which you said "You keep sending me messages twice"; 23 Nov 03:34).
- The guard's old practice test still misses 9 of 12 real change asks and stops 1 of 10 film questions.

**Rules changed.** No wording changed. Your rule "One message, never twice" (CLAUDE.md, 22 Nov, your pick "2" in the
Statement One chat) had no working check; it now has one. Before: when the guard stopped a reply it said "reword the
question", so chats sent the whole reply again; and only a second stop was written down, cut to 120 characters. Now:
- Every stop is written down in full, the first one too, with what was sent after it and how long it was.
- The stop tells the chat you have already read the reply, and asks for ONE line starting "Correction:": the missing
  count line, or "ignore question 2, it is withdrawn", or "question 2 is not a change, it only asks about ...".
- Only what is sent after the stop is judged. A right one-line correction clears it. A whole reply sent again is
  counted as a repeat and listed at the handover, and stops the next animatic until it is settled.
- The rulebook's "Messages to me" row names the check. The rule now counts as proven on your own 22 Nov double message
  (partly: the daily watcher line can still ask for a resend; that part waits on your pick, see below).

**Difference made.** Measured on your 22 Nov example: the old guard asked for a reworded resend and got 2,300
characters again; the new one names question 2 and accepts a one-line answer. On real chats: not measured yet. The
number to beat, counted from the full log at the end of the next film: whole replies sent to you again after a stop,
from at least 3 in two days to 0; every stop cleared by one line.

**Not built yet: Change 2 (its own yes).** Retune what the guard stops, tested on the 51 sorted stops and the practice
test: questions about the film, about chats, and about starting the judging process pass; "every film", "from now on",
"always" mark a real change ask; the count line passes in any wording with the right numbers; file names that are not
proposals stop being read as proposals. To beat: 0 wrong stops on the list (21 when replayed today), 0 real asks missed
(2 replayed today), practice test 9 of 12 missed to 0.

**How it should behave from now on.** You read each reply once. If a checker objects after you've seen it, you get at
most one extra line beginning "Correction:". The full log shows every stop and every repeat, so a chat that sends a
reply twice is caught the same day.
