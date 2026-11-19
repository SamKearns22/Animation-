# Helper A: scheduled-jobs-attach

## Leak
None. The problem file states a problem and facts only.

## Results
- 19 Nov: Sam queued jobs at 08:36-09:01 for 17:01 (`notes/ledger/sam/h3akq5qv.md`). Four fired at 17:01 with no project attached, so none of them did anything (the problem file; Sam at 17:14, `notes/ledger/sam/7r62524n.md`). The project lost about 8 hours of queued work. The money lost was small: empty chats (unchecked, there is no ledger row for them).
- The fault reached Sam. He found it himself and then asked three follow-ups: "you error or me error", "you hadn't attached it to the new four either?", "how do we prevent" (`7r62524n.md`). That is 4 messages of his attention on a fault no film caused.
- The relaunch lost the brief as well. A correction had to be sent at 17:18 telling Job 1 that its real brief was the stored text of the failed job, not the short summary it had been given (`notes/ledger/sam/yah6eyjt.md`). So moving the jobs to working chats by hand nearly lost Sam's additions (a)-(f).
- Bound reminders (timed messages sent into a chat that already has the project) worked 11-18 Nov (the problem file; unchecked by me). Two earlier timed chats, 12 Nov at 1:01 (`notes/archive/blessed-handovers.md`:86) and 15 Nov (`notes/archive/protest-tiers-handovers.md`:191, Sam: "the chat did not appear correctly under the scheduled list"), have no record of whether they had the project attached. A gap: the record cannot say whether fresh-chat timers have *ever* worked here.
- The one stopping-guard in the project, `.claude/hooks/modelguard.py`, is written as a check that runs before a tool call. It is not wired into `.claude/settings.json`, and the settings history on every branch shows it never was. So a "stop" guard built on 17 Nov has never stopped anything (git log -S PreToolUse).

## The real decision
This is not only about one tool's missing field. The decision is: **every time a chat hands work to a chat that doesn't exist yet (timed, next-in-chain, or a sibling), does the new chat get the project and the full brief, and does something check before the handover is reported as done?** The bigger levers are (1) a hard block in the tool path rather than a rule to read, and (2) checking the launch, not trusting the report.

## Root cause
- The scheduling tool, when it opens a fresh chat on each firing, cannot be given a project. CLAUDE.md covers project attachment only for "create_session". So a chat that queued jobs on fresh-chat mode was not breaking any rule: no rule or tool stops it.
- Nothing checks a launch. The queuing chat reported "queued", and the first check was Sam reading the result.
- Rules here get followed on paper while their guards stay unwired (modelguard above). A new written rule alone would fail the same way.

## Approaches weighed
1. **Rule in CLAUDE.md:** "timed jobs must bind to a chat with the project attached." Cheap, but it relies on being read. Rejected (Q3).
2. **Block the bad call (chosen):** a guard that runs before the tool call refuses a fresh-chat timer and any new chat opened without the project. The safe pattern is to open the job's chat first, with the project attached and its full brief, then set the timer to wake *that* chat. This is the pattern that already worked 11-18 Nov.
3. **Reframe, verify the launch:** after any timer or new chat is made, the chat reads it back (get_session or get_trigger) and reports "queued" only if the project and brief are there. A timer with nothing to read back counts as not queued.
4. **Learn-first:** go through the record for every timed or fresh chat since 1 Nov: whether it had the project, whether it ran, whether its brief arrived whole. That settles whether anything beyond this one tool needs fixing.

## Proposal
**Step 1, learn (changes nothing):** a Sonnet chat lists all timers (list_triggers with completed jobs included) and the chats they started since 1 Nov. For each it records: project attached Y/N, ran Y/N, brief whole Y/N. Cost about 0.5% of a week. Output: a table in the film's notes. It decides whether Step 3 also has to cover briefs.

**Step 2, change one: the launch guard.** A check that runs before the scheduling and session-opening tools. It refuses (a) a timer set to open a fresh chat each time, and (b) a new chat with no project attached or not on the main line. The refusal says what to do instead: open the chat with the project attached, then bind the timer to it. To make sure the guard really runs, its own test fires a refused call and checks it was blocked. In the same change, the guard is wired into `.claude/settings.json` (the place that makes the project's hooks run), with a check in the handover check that every guard file is wired there. Number to beat: 0 jobs fire without the project (now 4 of 4 on 19 Nov). Cost about 1.5% of a week once, then nothing per film.

**Step 3, change two, only if Step 1 shows brief loss beyond 19 Nov:** the read-back. "Queued" may be reported only after the new chat has been read back with the project and the full brief text in it. Number to beat: 0 briefs re-sent by correction.

What Sam would notice: timed jobs simply start working. A "queued" message means it was checked.

## Sam test
- Q1: An expert puts the block in the tool path, not in prose. Yes.
- Q2: The evidence covers every timer since 1 Nov (Step 1), not just this night.
- Q3: It can't be complied with on paper, because the call is refused. The wiring check covers the unwired-guard failure.
- Q4: Four different approaches weighed. The block plus the proven pattern wins.
- Q5: Undoable: remove one hook line. It relies only on a pattern already proven 11-18 Nov.
- Q6: Sources named. The 12 and 15 Nov launches are marked unchecked.
- Q7: Sized to zero failures, not a cheap rule.
- Q8: Permanent guard, reviewed at film end.

## Lost / Added
Lost: fresh-chat-per-firing timers (each job needs its chat opened first: one extra step when queuing).
Added: guaranteed attached timed jobs; a wiring check that catches guards built but never switched on (modelguard now).

## Unchecked
Bound reminders 11-18 Nov working; the 12 and 15 Nov timers' attachment; the cost of the four empty chats; whether modelguard is wired outside the repo (user settings).
