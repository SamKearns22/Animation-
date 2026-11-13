# Where things stand (project, 13 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/overnight-q-handover-check` and `claude/face-tool-c2` (both on the main line).
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 30 (a repeated note: find why first).
- **Done (overnight chat 1, Job Q, Opus medium, ~2.2%):** `source/handover.py` (MAP; catalogue row; kittest
  `handover_drops` passes on Blessed's real chat 5 messages and notes files). The `log` hook (UserPromptSubmit) saves
  Sam's typed messages to `notes/ledger/sam/CHAT.md` and pushes. `end` / `start PARENT --film F` flag his asks not
  carried by a notes line written after he spoke, unanswered messages, unsent clips, an override he never typed.
- **Face tool (item 2): Sam, 13 Nov: "another 100% to the budget. Continue"** (stop now 7.5% of a week; spent ~5.6%
  in chats 1-2). Burnham's A/B/C pass the check (68/77/71%, first of 14) but read young and round.
  **Next: face chat 3, Opus high:** 1) age lines from the photo (cheek folds, crow's feet; no kit piece, new), re-run
  Burnham (a look change can drop a pass: re-run after each), name test (namer helpers) on A/B/C; 2) Badenoch (braids:
  hair mask down past the jaw); 3) Walliams replay (w06, w07, w01, w02; tries vs his five chats); 4) kittest
  (eyes swapped for the average fail `verdict`, the tuned head passes; `_others` finds 13+); 5) send Sam the 3 sheets.
- **Next: overnight chat 2, Opus medium: the critic bench (ranking item 3, `notes/ranking-list.md`).** Test on Blessed.
- **Needs Sam:** morning report: Y to the CLAUDE.md line that makes chats run `handover.py end`/`start` (pick Y);
- **OVERNIGHT RUN (Sam, 13 Nov 23:25 UTC): read `notes/overnight-run.md` first.** Order Q, critic bench, rounds-read-a-page,
  then people, places, moves, rough command; test only on Blessed (never Protest Tiers); each job may reach 150% of its
  estimate, then hard stop, `notes/morning-report.md`, next job.
- **Read:** this section; `guides/job-packs.md` "A tool job"; the job's own section.
- **Open rule requests:** none.
- **For Claude:** face tool state in `source/facepick.py` MAP (tune() is a search judged by `verdict()`, as check
  judges; 2.5 min a person); its next steps are in the morning report.
## Job Q, the handover check (Sam: Y, 13 Nov; Opus medium, ~1.5%; beside the face tool)
Why: Blessed's handovers dropped things (notes 8-11 sat unread when chat 5 broke before writing them and chat 6 read
only the notes file; Walliams' face, open in note 47, fell out of two handovers; chat 5 read "don't stop for any Y" as
a cost override). Closest: CLAUDE.md "Fresh chats and the handover", rule 30, `ledger.py`; nothing checks a handover.
One tool, two moments (Statement 1: quality, fewer notes and faults, cost; kittested; about $0.10 a chat to run):
- **End of a chat, before it hands over:** list every message Sam sent in that chat (`list_events kinds=["user"]`,
  filtered); flag any with no fix or reply, any open note the handover does not carry, any "clip sent" with no file.
- **Start of the next chat:** read Sam's messages in the chat before, to catch one that broke before handing over.
Saves about 2-4% on any film where a chat breaks or drops a note. Lost: nothing. Reads: `guides/job-packs.md` "A tool job".

## Logged 13 Nov (Sam: log for now; not started). The one aim: films at 15% of a week, or as close as honestly possible
- **Job O, true weekly figure (Sonnet, ~0.5%).** Sam: Blessed spent 80% of a week; our ledger counted 50.92% (WEEK_USD
  290). Set `WEEK_USD` in `.claude/hooks/costwatch.py` so Blessed's recorded dollars read 80% (first check the ledger
  has every Blessed chat: 11 Nov rows are estimates); restate every film's ledger and every quoted % with it.
  **DONE 13 Nov (chat 1 of 8, Sonnet):** found Blessed's record missed two chats (chat 5 of 8, $5.08, and chat 6 of 8,
  $2.11: added to `app-costs.tsv`) and carried five duplicate transcript-estimate rows for chats the app already
  showed (dropped by `ledger.py app`). Real Blessed = $100.79 from the app + $36.05 estimated (six 11 Nov chats
  the app cannot show, kept) = $136.84. `WEEK_USD` 290 -> **171** so that reads 80.02%. Every film's estimate rows were
  rescaled x290/171 and app rows recomputed: Blessed 80.02%, Remakes 51.54%, Protest Tiers 14.44%, Link trial 1.9%.
  Film estimates and stage plans (Blessed 19%, Remakes 14.5%) are NOT rescaled: they were guesses on the old ruler;
  Job N redoes them. Rule 85's 3%/5% chat limits are unchanged in % (now $5.13/$8.55, tighter than before): Sam to say
  if he wants them kept in dollars ($8.7/$14.5 = 5.1%/8.5%). Kittest `estimate_forecast_and_alarm` passes.
- **Job N, honest fit at planning (Opus high, ~1-2%).** Widen rule 24: before any building, the plan states whether the
  script fits 15% (from KNOWN vs NEW and real past costs on the true ruler); if not, why (people, places, likeness
  faces), and which tool improvements would bring it closer (never trimming the joke or reusing
  old content: CLAUDE.md, Sam 13 Nov). Blessed (7 people, 8 places, one
  likeness face) is the test case: the plan should have said "about 25-35%, here is why, and these tools would close the gap".
- **Job P, the ranking job: DONE 13 Nov (chat 2 of 8, Opus high): `notes/ranking-list.md`.** Order: 1 roughs of
  every new thing (rule 11), 2 likeness in one sitting, 3 critique test bench and Sonnet critic, 4 people from a
  description (tested on Protest Tiers' cast), 5 places, 6 rounds read a page, 7 moves; N at the next new film's plan.
  All built ~29%; a Blessed-sized film then ~20-26%, a typical one ~15-18%. Sam's numbered message sent. The entry as logged:
- **Job P (as logged, Opus high, ~2-3%).** One chat; output one ranked list of jobs to bring
  films toward 15%, from the real record (every note, every fault caught or missed, every chat's cost, stage cost vs
  plan, on the true weekly figure, Job O). Headings: catch faults before Sam sees them; better tools that work less hard;
  making new people, places and moves faster and surer; reading less. Each job: build cost, saving per film (measured),
  films to pay back, "Lost:" line. Ends with what a Blessed-sized film would cost if all were done. Never: trimming the
  joke or repeating old content (CLAUDE.md). **Headline item: describe, don't code.** Blessed needed ~5,500 lines of its
  own code (cast 1,144, sets 1,491, film 2,050, others); a new person, place or common move should be a short description
  the engine draws from tested parts (figure kit, likeness, set painter joined up). Price it honestly, what it would have
  saved on Blessed and the last 10 films, and a staged plan, people first.
  **Also on the list (Sam: Y, 13 Nov):** (a) a rough of every new person, place and move sent to Sam before its build
  (widens rule 11 from 3-4 key shots to every new thing); (b) test Sonnet as the critique helper (rule 89, now Opus,
  ~a quarter of a build chat) against past films' faults; switch only if it catches as much. (Parallel build chats
  dropped: already how we work.)

