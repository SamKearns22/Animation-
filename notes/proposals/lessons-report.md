# The Milburn lessons: what changed, and how it should behave (Sam's ask, 22 Nov ~23:10 UK)

Sam: "Please report back on all changes rules and what the difference you have made is, and how it should behave in
the future." One entry per lesson, written by the chat that builds it. The chat that builds brow-limit (the last of
chain B) sends the whole page to Sam in plain words.

## 1. staging-stills: no shot is built before Sam has seen its framing (built 22 Nov, chain B chat 1)

**The look back first (step 1).** Over four films (Milburn, Patriots 4, Blessed, European Protests Ranked), 5 framings
Sam had to give a note on twice were all built and sent as clips before he saw any picture of them. Milburn's Cabinet
Room shot was built three times; its weapon-picking shot needed "still poorly composed". The one time a still came
first (Patriots 4's wide view), his "no" cost a picture, not a round. So the change was made.

**Rules changed: none yet.** Two wording changes are waiting for Sam's yes (asked 22 Nov):
- Rule 11, before: "Each is sent once: notes on it are acted on, never sent again." Proposed: "Each is sent once; a
  shot whose framing changes (a note about framing or staging) goes on a new board before it moves: first a sheet of
  2-3 numbered framings, one of them the screenplay's camera line taken literally, then Sam's number, then the shot as
  built on the board." Check column adds: the clip and animatic refusals (staging tool) and their two tests.
- Rule 87, before: "A fix that fails twice stops rendering: the next send is one still sheet of 2-3 options for Sam to
  pick from." Proposed adds: "A note about framing or staging gets that sheet at once, not after two failures (rule
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

**Rules changed: none yet.** Each change needs its own yes (Sam's option 1), asked 23 Nov:
- Change 1 (a check that "could not test" stops the animatic): not asked again. It is the same fix as the
  could-not-test lesson, which Sam has approved and which is being built in its own chat; built once, there.
- Change 2, rule 59, before: "faults Sam has been told about need `--faults-named`, and each is listed once: the film
  keeps a named-faults list and pre-flight shows only faults not on it." Proposed: "every fault left needs its own
  written answer in the film's exceptions list (chosen or real; why; where it was looked at full size; who fixes it),
  or the render refuses; a fault whose check could not see the film cannot be answered, only cured by handing the check
  what it needs; an answered fault comes back if its numbers change; pre-flight prints how many are answered and every
  unanswered one in full." Check column adds: the render lock reads the exceptions list per line (its kittest).
- Change 3 (shared inputs, starting with the places and moves tools Milburn was built on): no rule wording; a
  "move to shared" line for every check fix made in film code, flagged at the handover.
- Change 4 (kit tests): round_page is already repaired. The rest: a shared-tool test red at two handovers in a row stops the handover (one is red at two today), and a test that could not run counts as red. No rule wording beyond rule 13's check column naming the handover check.

**Difference made.** Nothing changed yet, so nothing to measure in a film. The numbers to beat, from the look back:
Milburn's replay with changes 2 and 3 should leave at most the 16 chosen or unsettled lines, each answered (today 61
named in a bunch plus 60 removed by hand); the next film: under 10 unanswered lines before every animatic, 0 blind
lines at its first pre-flight, and 0 Sam notes that were already a printed line (3 in the last two films).

**How it should behave from now on (on Sam's yeses).** A warning is never waved through in a bunch. If a check could
not look at the film, the animatic stops until the film or the shared tools give it what it needs. Every other warning
left gets one written line: why it stays, where it was looked at full size, and who fixes it; if its numbers change it
comes back. Sam's "Checks:" line gets short: a count of answered warnings and only the unanswered ones in full. A check
fixed inside one film is flagged until it is moved into the shared tools, so the next film starts with it.
