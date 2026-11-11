# Budget job: old handovers

## Where things stand (11 Nov, 17:10 UTC; budget chat 1 handed over on amber)
- **Rules that bite next:** 85 (cost watch), 24 (the estimate: honest prices), 89 (critique: both hunts stay).
- **Done:** Remakes' 60% traced; trial 1 (Link, a Lead) measured; `source/costbreak.py` built (where a chat's cost
  goes by kind of step, helpers included). Trial 2 (the line-up five as Glimpses, `notes/trial_lineup.md`) stopped
  after 8 minutes when the usage limit ran out; restarted 17:10 on Sam's "try again".
- **The big new fact:** the critique helpers are NOT in the cost watch's figure. Link's true cost is about 3.2% of a
  week (chats 1.0 + 1.22, helpers 0.51 + 0.46), not 2.0%. Every film's helper cost has been invisible the same way.
  Breakdown: `notes/trial_link.md`, "Cost breakdown".
- **Next (Fable, high effort; Sam set Fable for this job):** read trial 2's Results and Cost breakdown in
  `notes/trial_lineup.md` (if empty, one check in 30 minutes, no more). Then write the stage-by-stage savings list
  with a measured figure on each, re-forecast Remakes, and send Sam every proposal in one message for Y/N.
  Nothing is written into the rulebook or tools before his yes.
- **Savings already seen in the breakdown (to price):** a helper's start-up is 0.16 of its 0.5; 60% of a helper's
  listed faults are repeats (its writing is 0.12-0.18); the build chat took 59 steps, 20 running tools, 12 shell,
  11 looking at pictures, 7 saving (draw and look in one step; save once); the cost watch and ledger must count
  helpers.
- **Sam's answers so far:** test = Remakes with its starting information; any spend; the animatic stays as clean as
  Remakes'; both critique hunts stay; chats stay short; acting in the first animatic is settled (no trial); tool
  improvements (script checks, reference tick-list, child poses in the kit) go in the proposals: Y; no Fable trial.
- **Needs Sam:** nothing until the proposals. Open: this chat's cost sits in the Remakes ledger (about 1.6%; the
  guard refused the move); the cost watch prices Fable as Opus.
- **Read:** this file; `notes/trial_link.md` Results and Cost breakdown; `notes/trial_lineup.md` Results.
- **For Claude:** trial sessions: session_01J1JB7XiZASWyXBqe8TwFbT (trial 2). Do not read their events (huge).


## Where things stand (11 Nov, 17:45 UTC; budget chat 2: both trials read, proposals sent, waiting for Sam)
- **Rules that bite next:** 24 (the estimate: honest prices), 85 (cost watch), 89 (critique: both hunts stay).
- **Done:** both trials read; the savings list, the re-forecast (about 26%; 30 before the two tool changes prove
  themselves) and proposals 1-11 are in "5. After both trials" below, and sent to Sam in one message.
- **Next (Fable, high effort; Sam set Fable for this job):** on Sam's numbers, write each yes ONCE: the rulebook
  (rules 24, 85, 89), CLAUDE.md, the Build pack's order, and the tools (`critique.py`, `costwatch.py`,
  `ledger.py`, the one-command draw-check-sheet). Type: "Budget job: write up my yeses" with the numbers.
- **Needs Sam:** Y/N on 1-11 (his "Do you need to test the sets too?" is number 9: my pick N).
- **Read:** this file's section 5 only; the rule, tool or pack section each yes names.
- **Open rule requests:** none beyond the proposals.
- **For Claude:** helper unit 0.48 (0.44-0.51, start-up 0.16-0.18 of it); a step 0.02; Remakes' helpers counted from
  `notes/ledger/remakes*.json` critique passes (cast 3, sets 9, animatic 2). The "before" row of the Remakes ledger
  is Sam's app figure, so helpers ARE in Remakes' 60%; the cost watch's own figures leave them out
  (`isSidechain`). This chat's cost sits in whichever ledger the hook picked; check before quoting it.


## Where things stand (11 Nov, 18:20 UTC; budget chat 2: Sam said Y to my picks; rules written, tools half built)
- **Rules that bite next:** 24 (stage-share stop), 89 (two hunts, each fault once), 85 (helpers counted).
- **Done:** Sam's "Y" (taken as my picks: no sets trial, no further cuts yet). Written: rule 24 (tiers, the brief's
  must-haves, starting units, the moves' share, the stage-share stop, budget by size), rule 89 (Glimpses in the shot;
  two hunts a stage, one helper each, each fault once, no third hunt), rule 85 (helpers counted, Fable priced). Built
  and tested: the cost watch counts helpers and prices Fable at twice Opus (so the ledger does too).
- **Next (model waits on Sam's answer to question 1: Opus high is my pick, Fable high if he says N):** build the
  three tool changes the rules now promise: (a) `critique.py`: the helper lists each fault once; `status` not blocked
  by CAN'T TELL; one pack per stage; no third pass. (b) `ledger.py auto`: stop when a stage reaches its share (now
  only a quarter over the estimate); update rule 24's check column. (c) one command that draws, runs the checks and
  builds the sheet (look in the kit first, rule: reuse before building). Kittests for each. Type: "Budget job:
  build the three tool changes".
- **Needs Sam:** question 1 (the builds on Opus high, half Fable's price) and 2 (at the brief, name any new
  character an existing one could play, with the saving).
- **Read:** this file's section 5; `critique.py` and `ledger.py` MAPs, then only the functions named.
- **Open rule requests:** none.
- **For Claude:** Fable 5.2 lists at $8/$40 a million (Opus 5.5 $4/$20), re-reading the same; the cost watch's
  fable row is its opus row doubled except the re-read. The Build pack in `guides/job-packs.md` still says "drawn
  alone and critiqued" for every new thing: add the Glimpse exception when (a) is built.


## Where things stand (11 Nov, 18:45 UTC; budget chat 2 handed over on amber: rules written, the tool build is next)
- **Rules that bite next:** 24 (stage-share stop), 89 (two hunts, each fault once), 85 (helpers counted).
- **Done:** Sam's Y to proposals 1-11 (my picks: no sets trial, no further cuts). Rules 24, 85, 89 rewritten. The cost
  watch counts helpers and prices Fable at twice Opus (tested; the ledger follows).
- **Sam, 11 Nov (binding):** this job stays on Fable (a one-time experiment); N to naming kit stand-ins at the brief
  (a weekly satire always needs new people). **"Cost savings have to come from background processes becoming more
  efficient and intelligent."** So: no proposal that asks Sam to change what he writes or how he works.
- **Next (Fable, high effort):** build, each with a kittest, cheapest first, measuring this chat's cost at each:
  (a) `critique.py`: the helper lists each fault ONCE (60% of its lines were repeats); `status` not blocked by CAN'T
  TELL; one pack per stage, never per set; no third pass. Add the Glimpse exception to the Build pack.
  (b) `ledger.py auto`: stop when a stage reaches its share (today: only a quarter over); fix rule 24's check column.
  (c) ONE command that draws, runs the checks and builds the sheet, printing only faults (look in the kit first):
  a fixing chat ran 59-70 steps at 0.02 each, 27 of them tool runs, 16 shell, 12 looks.
  (d) the helper's start-up is 0.17 of its 0.48: time a one-line helper of each kind the Agent tool offers, and
  make `critique.py pack` name the lightest that still sees pictures. If none is lighter, say so.
  (e) the three improvements Sam okayed earlier and chat 2 left out of the proposals: script checks for the
  critique lines that catch the most (cast P2 25, A2 22, A1 17, P6 14; sets A2 22, A1 21, S3 20, O3 20, S1 19:
  `notes/ledger/remakes_*.json`, `guides/critique-checklist.md`), only where a script can truly test them; the
  reference tick-list filled by a tool before a hunt; the trials' child body and poses into the kit.
  Then one message to Sam: what each should save, measured where it can be. No film work. Hand over on amber.
- **Needs Sam:** nothing.
- **Read:** this file's section 5; the MAPs of `critique.py`, `ledger.py`, `costbreak.py`; only the functions touched.
- **Open rule requests:** none.
- **For Claude:** Fable 5.2 lists at $8/$40 a million (Opus 5.5 $4/$20), re-reading the same. Helper records sit
  beside the chat's own (`costwatch.helper_files`). Do not read the trial chats' events.
