# Check repairs (Sam, 21 Nov: "Everything else needs step by step checking, fixing, testing, and reporting back to me")

## Brief checklist
- [x] Budget tracker: stages never marked and chats never logging notes. Handover check now flags both (LEDGER, STAGES);
      GTA stages opener..animatic1 marked afterwards from the chat order (approximate). The cost line then showed real
      overruns: board 2.3% against 0.5% planned, moves 19.2% against 11.3%. The budget stop works when tested, but
      Sam paused all budget alarms on 18 Nov (ledger.py ALARMS_PAUSED) "until system fixed": his call to switch back on.
- [x] Renders not handed to Sonnet: the model guard (.claude/hooks/modelguard.py, Sam's Y 17 Nov) was never wired
      into .claude/settings.json, so it never ran. Wired now; the watcher flags any promised hook left unwired.
      In GTA the whole-film animatics did go to Sonnet; Opus chats rendered their own clips, which the rules allow.
- [x] Notes over 4,000 words and handovers over 15 lines: no check existed. size_faults in handover end now
      (also requires the "Open rule requests" line).
- [x] Chat 26 told Sam "I sent you a short clip" but the send was refused (the body check's send gate: faults not
      named). Refused sends no longer count as sent; wider "sent" wording. Chat 27 told to re-send.
- [x] No push notification at handovers: push_faults in handover end.
- [x] kittest handover_status_checks; watcher_catches_last_weeks_four passes again (promises added).
- [ ] The 11 other failing kit tests (below).
- [ ] Sam, 21 Nov: "Why are tools built then not enabled? Keeps happening. Please ensure that doesn't happen again."
      Why: (1) the watcher finds systems by reading the wiring (settings.json hooks, handover end calls, job packs), so
      a tool that never got wired is invisible to it; (2) each tool's kittest calls the tool directly (modelguard
      test "OK, 11 cases"), proving it works when called, never that anything calls it; (3) a job is ticked done when
      the file and its test exist, not when it has been seen running in a real chat. Fix to build (chat 2):
      a) the watcher also finds tools from the files themselves (every .claude/hooks file, every source tool an
         adopted proposal names) and lists any that nothing switches on, at every chat start, until wired or named;
      b) every tool's kittest gets a switched-on half (it is in a hook, called by handover end, or in a job pack);
      c) a built tool is ticked only after its own log shows it ran in a real chat (as modelguard.log now does);
      d) test it against the 17 Nov guard (settings.json as it was before 21 Nov must be flagged).
- Plain words, one wait per render, repeat notes (rule 30): looked at chat 26's last message and waits; followed.
  Rule 30: the arm note came a fourth time; the chat said why the earlier fix failed (camera fix covered only the
  shooting). The ledger never counted repeats: LEDGER fault now makes each chat log them.

Handover check on this chat (named): three NOT SENT lines are this chat reporting OTHER chats' sends (a status
chat's words; the wider wording catches talk about sending: watch for false flags on film chats); COST: a back-end job
has no estimate; RECORD "pre-flight ran on gta": only test text naming preflight.py, nothing ran; PUSH: sent at the end.

Changes made without a proposal (for the end-of-film review): every item above, all on Sam's 21 Nov instruction.

## Budget tracker audit (Sam, 21 Nov: "I need to know that the budget tracking tool has worked as promised. The idea was to
audit every last thing done in order to find the most expensive things and run it through the proposal route to
discover how it can be made more compliant with statement one.")
- Works: every GTA chat has a row (27, 53.3% of a week), each with its cost split by kind of step and part of the
  bill; the estimate matches the app's real figure (chat 26: 2.45% estimated, $9.07 = 2.48% real).
- Fails the promise: (1) 69% of the film's cost (36.6 of 53.3) is filed as "other": the record cannot say what the
  most expensive things were; (2) nothing takes the dearest things to the proposal route: only a hand-run end-of-film
  review does (Milburn's); (3) notes and repeats were never counted (fixed tonight: LEDGER fault); (4) no real (app)
  figures imported for GTA yet. Known parts: tool search 11.3, carried history 14.5, start-up floor 11.5, renders 2.0.
- Sam, 21 Nov: "I would like them suggested to me before I approve them to send through proposal route as the
  route itself is expensive. Please fix the 'other' problem and the notes problem, test in a real chat, and once
  done report back with your five suggestions." So: fix "other" and automatic notes counting, test on real records,
  then five plain suggestions to Sam; the route runs only on the ones he picks.
- [x] (superseded by Sam's line above where they differ) Cost audit chat (Opus high): split "other" into named things (writing code, thinking, edits, reading notes,
      critique helpers...) on GTA's real records; then a standing step that, at each film's end (and weekly), ranks
      the five dearest things and opens each as a proposal through propose.py against Statement 1 (quality first,
      then fewer notes and faults, then cost). Test it on GTA and Milburn; report the top five to Sam in plain words.
      Done 21 Nov (cost audit chat, session_01GznaAVLcaYKAag7e6Ap2Nx):
      - Every dollar of a chat is now named (stepcost.split -> 'named': thinking (exact, from the usage), writing
        code, writing notes, commands, messages to Sam, helper and chat prompts, reading notes / guides / film code /
        kit code / chat records, pictures, renders, checks and tools, git, start-up and handover tools, critique /
        name-test / proposal helpers, start-up reading, memory lapses, messages and reminders). Adds up to the bill;
        on this chat and the 6b test chat 0% is left unnamed. Rows from now on carry it (the ledger stores the split).
      - GTA's gta_*.py now counts as the film's own code (the record filed it as kit code).
      - source/dearest.py ranks the dearest named things per film and per week. Per Sam's later line, nothing opens on
        its own: the five are SUGGESTED to Sam (numbered); `dearest.py FILM --open 1,3` opens only his picks
        ("not split" gaps never). Switched on: propose.py review (film end) prints the five to suggest; handover.py
        end flags DEAREST when the weekly ranking is over 7 days old. kittest dearest_things_named; catalogue row.
      - Notes problem: the Stop hook now counts Sam's notes from his own typed messages (numbered items each count;
        yes/no/go/number answers and one-line questions do not) onto the row, and flags possible repeats (60% of the
        words of a line already in the film's notes); handover.py end shows them as REPEAT?. On the saved messages:
        301 notes in 287 messages, 13 possible repeats (e.g. GTA's "the gun is not pointing at his target").
      - Real-chat test: this chat's own row carries the named split (0% unnamed) and its note count (0: no message
        from Sam in it). A chat with Sam's notes: tested on his saved messages, not yet live.
      - GTA top five on its own record (51.5% of a week): Claude's own writing 22.3 (older rows cannot split it; on the
        two full records thinking was 39-48% of it, writing code 32-38%), start-up reading 11.0, searching and reading
        code and notes 7.9 (kit code 2.8, film code 2.0, other 1.7, notes 0.8), messages and reminders 3.3, memory
        lapses 2.9 (7 chats). Milburn: no split was ever recorded (17-18 Nov): cannot be ranked.
      - The app's own records for GTA chats 1-25 and Milburn 1-7 can no longer be read (their old ids give "not
        found" and they are not listed); only chat 26 can, and its copy lacks thinking and true output counts. The
        ledger rows (made from each chat's full record at the time) are the only record left.
      - Put to Sam (21 Nov): which of five go through the route (my pick 1, 2, 3): 1 start-up reading, 2 Claude's
        thinking and code writing, 3 memory lapses, 4 looking at pictures, 5 searching code. His answer comes back here.
        Ideas given with them (unrouted, his pick first): 1 a smaller fixed start, only what that chat needs; 2 more
        built from ready kit pieces, less new code per note; 3 hand over before a long wait instead of resuming;
        4 small labelled crops of what changed; 5 a map of where each part of the film lives in the code.
        22 Nov 02:00, Sam's 2am reminder ("go on with your own stated pick"): picks 1, 2, 3 go ahead, listed to Sam.
- [x] Cost audit chat 2 (Opus medium): `python3 source/dearest.py grand-theft-autism --open 1,2,3`, then the route
      (pack, helpers, judge, record) on #1 first with its cost measured (ledger row), then #2 and #3; show Sam the
      verdicts (propose.py show) with Lost/Added. Then the 278% week check and Sam's Sonnet-render note.
- Cost audit chat 2 (22 Nov, session_01GznaASKWmDUJAWLniVGoiV) found:
  - Numbering slipped: the list put to Sam (1 start-up reading, 2 Claude's thinking and code, 3 memory lapses) was
    hand-written; dearest.py's own numbers put "messages and reminders" at 2, so `--open 1,2,3` opened the wrong
    thing. Fixed by hand (proposal 2 rewritten to Sam's pick). Still open: the list Sam sees must be the tool's
    own printout, numbers and all (dearest.py should save what it showed and --open read that).
  - Verdicts (propose.py show dearest-grand-theft-autism-1/2/3), each option 1 = measure first: (1) start-up block
    measured per chat, then unused add-ons switched off by Sam; (2) tag rework of rejected shots, then stills must
    pass checks before movement if rework is half or more; (3) time each memory lapse's cause, then one fix. Sam
    picks option 1 or 2 for each.
  - The route's cost, measured on proposal 1: about 1.2% of a week (two helpers + judge 1.1%, the chat's own steps
    about 0.1). All three: about 2.6% (9 helpers and judges 2.2%, so about 0.7-1.1% each).
  - Week 15-21 Nov: 126 rows add to 234% as filed. The rows use two different week sizes (before 19 Nov $290, after
    $366: the 36 app-figure rows hold $160 but say 54.7%); at one size ($366) the week is 205%, still twice a week.
    2 chats filed under two jobs. The app's own figures for these chats can no longer be read ("not found"), so
    the estimates cannot be checked against them. Likeliest cause left: the week size itself is too small (set from
    Milburn's 22 meter points = $80, but other chats ran at the same time, so the points cost more). Needs one meter
    reading from Sam (the % his usage page shows and when it resets) to set it from all chats in the same window.
- [ ] The week's record adds to 278% of a week over 149 chats (219 of it estimates, 3 chats filed twice; 42 chats
      filed under proposal-route). That cannot all be real if the weekly limit holds: check the estimates against the
      app's figures for the chats that can still be read, and how chats are filed to jobs (Opus medium).
- [x] (done in cost audit chat 2) On Sam's picks: `dearest.py grand-theft-autism --open N,N`, then the route on each; its cost per proposal is
      unmeasured, so measure the first before the rest (Opus medium).
- [x] Sam's note 3 in the status chat (21 Nov): "I had noticed that renders were not being handed off to sonnet models
      like you used to." Not yet carried anywhere: find why (handover model line, modelguard) and fix.
      Done in the status chat: modelguard.py was never wired; wired 21 Nov, watcher flags unwired hooks (see the top).

## Where things stand (22 Nov, cost audit chat 2, Opus medium)
- Rules that bite next: the proposal route (Sam picks only from judged options), 85 (cost watch), 30.
- Done: Sam's picks 1-3 routed and judged (see "Cost audit chat 2 found"); the route costs about 1% of a week per
  proposal; week check: 205% at one week size, cause most likely the week size; dearest_faults promise listed.
- Next: on Sam's answers, Opus medium builds the options he picks (each option 1 is a measuring step first).
- Needs Sam: an option (1 or 2) for each of the three; one reading of his usage meter (% and reset day).
- Read: this file's "Budget tracker audit" only; `propose.py show dearest-grand-theft-autism-N`.
- Open rule requests: none.
- For Claude: still open, dearest.py numbering (save the shown list; --open reads it). Watcher BROKEN saver line
  (20 Nov 03:29) is named in notes/proposal-route.md. claude/check-repairs-2 left alone (another chat's live work). Handover
  flags named: SENTENCE (CLAUDE.md's "Choose views" line still there, now with Sam's 21 Nov aside), COST (no estimate set for this job).

