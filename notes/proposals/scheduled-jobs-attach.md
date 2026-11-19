# Proposal: scheduled-jobs-attach

Status: open

## Problem
On 19 Nov at 17:01 four timed jobs Sam queued fired and every one opened with no project attached, so none could work. The chat that queued them reported them as queued without anything checking they could run.

## Facts
- The four jobs (trig_0142kNie.., trig_018Pueb.., trig_01TwQ8fJ.., trig_01SVHnkT..) have last_run SUCCEEDED at 17:01 with no source repository in their record (list_triggers include_completed, 19 Nov).
- create_trigger has no repository or source field; create_session does (source_url, revision). Sessions made with create_session at 17:15-17:17 show the repository attached (get_session).
- The failure was seen only when Sam read it at 17:14 (notes/ledger/sam/7r62524n.md).
- Earlier timed reminders (Nov 11-18) bound to an existing session (persistent_session_id) ran fine.
- CLAUDE.md says a chat opening the next chat uses create_session with the project attached.

## Record
notes/ledger/sam/h3akq5qv.md
notes/ledger/sam/7r62524n.md
story/status.md

## Verdict (the judge, word for word)
<!-- verdict-hash: b13410e8c90e844a -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V1 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: small. "The chat that queued them reported them as queued without anything checking they could run" points toward adding a check at queue time or after firing. The Facts also set create_trigger (no repository field) beside create_session (has one), which hints at "start jobs with create_session". Both helpers still weighed reframes, so the anchoring was mild.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 5 | 5 | 4 | 4 | 5 | 23 |
| V2 | 4 | 4 | 4 | 3 | 4 | 19 |
| V3 | 3 | 3 | 4 | 3 | 4 | 17 |
## Sam test
Q1: Yes. One way to start any chat, enforced in the tool path, plus a health check after the start, is what an agent-workflow expert would do. Patched: the guard must be proven switched on (V2's finding), or it is a rule on paper.
Q2: Yes. The evidence is every timer on record (19 listed, all kinds), the fired chats' own records, and Sam's ledger, not one evening. The look-back adds the 14 and 16 Nov wake runs.
Q3: Root cause found with evidence: the fresh-chat timer kind carries no project, no login, no model (checked: job 2 ran on Sonnet, "no-git-repo", model field empty). Enforcement is a refusal, not reading; patched so a test proves the refusal fires. The after-start check catches failure kinds not yet seen.
Q4: Yes. Reframe, check at queue time, check after firing, learn first were weighed; V2's "pre-open the job chat, bind the timer to it" added as a second pattern for the test.
Q5: Low. Nothing changes until the test passes; each change has its own Y and is removed by deleting one guard line or one rule line. The one trust asked (that the safe path works unattended) is what the test shows first.
Q6: Mostly. Checked here: 4 jobs were fresh-chat kind, every earlier timer was a wake-existing-chat kind; job 2 cost $0.065, ran on Sonnet, no repository; the stop-guard file (modelguard) is not wired into the project settings. Unchecked and marked: jobs 1, 3, 4 run model; the 14 and 16 Nov wake outcomes.
Q7: Yes. The cheap warning-only option is rejected because no warning can give a fresh-chat timer a project or model.
Q8: Yes. Permanent guard and rule, reviewed at film end; the test is learning before the change, not a trial of it.
## Pick
V1
## Why
V1 is the only version that names all three things the fresh-chat timer loses (project, model, and with them the full brief), checks them against the fired chats' records, and keeps each change on its own Y behind a test that must pass first. It also adds the after-start check, which is what turns "Sam found it at 17:14" into "a chat found it within minutes".
V2 is strong on enforcement: its finding that the project's only stop-guard was built on 17 Nov and never switched on is checked and true, so V1's guard would risk the same fate. But V2 bundles the guard, the switch-on, and a handover-check addition into one yes, has no live test of the safe pattern before changing, and its look-back does not test the path unattended.
V3 is the idea in one line: right direction, no evidence, no test, no sizing.
Taken from V2: (a) the guard is switched on in the project's settings and its own test fires a refused call to prove it is blocked; (b) the guard also refuses opening a new chat without the project and main line; (c) the second safe pattern (open the job chat first with the project and model, then set a timer that wakes that chat), tried alongside V1's in the test so the numbers pick one. From V3: "queued" is only reported after the read-back.
## Faults in the pick
- F1 [fixed] V1's guard could be built and never switched on, as the existing stop-guard was. The guard is now wired into the project settings and tested by a call it must refuse.
- F2 [fixed] V1 tested only one safe pattern (the queuing chat wakes and starts the job). Waking a long, old chat re-reads its whole history and depends on that chat still existing; the pre-opened job chat is tested too, and the cheaper one that passes all four points is kept.
- F3 [fixed] "Queued" was still reportable on trust; it is now reported only after reading back the started chat (project, model, brief).
- F4 [named] The guard only works in chats that load this project's settings; a chat opened with no project loads none. That is why the queuing chat, which has the project, is the one guarded.
- F5 [named] The fired chats did have a tool to attach a project themselves; nobody used it, and it cannot fix the missing model. Not relied on.
- F6 [named] Run model of jobs 1, 3, 4 and the 14 and 16 Nov wake outcomes are unchecked; the look-back settles them.
- F7 [named] The cost in % of a week rests on Milburn's $32.40 = 22%.
## Final version
Problem: on 19 Nov four timed jobs started fresh chats with no project, no login, and no model (job 2 ran on the cheaper model); each was marked "succeeded" because that only means a chat was started. Sam found it himself 13 minutes later, and the hand restart nearly lost his additions to job 1's brief.

Learn first (changes nothing, about 0.5% of a week, Sonnet). Read the 14 and 16 Nov wake runs: did the chats they opened have the project? Then run two 2-minute tests: (A) a timer wakes the queuing chat, which opens the job chat with the project, main line, model, effort and the full stored brief; (B) the job chat is opened first with all of that, and a timer wakes it. Each passes only if: project attached, saving works, model and effort match, brief arrives word for word. Keep the cheaper one that passes all four; if neither passes, nothing below goes ahead and Sam is told why.

Change 1 (its own Y). Rule in CLAUDE.md, Models and chats: "Every chat starts with the project, main line, model, effort and full brief. A timed job never starts a chat by itself; it wakes a chat that already has them (the pattern the test chose)." A guard runs before every timer and every new chat: it refuses a timer that opens a fresh chat, and a new chat without the project or the main line, and says what to do instead. The guard is switched on in the project settings, and its own test makes a refused call and checks it was blocked. Number to beat: 0 timed jobs start without the project (19 Nov: 4 of 4), checked from the timer list at each film's end.

Change 2 (its own Y, after change 1 is in use). After any job chat is started, the starting chat reads it back (project, model, brief) and only then says "queued" or "started". On a failure it sends Sam one push saying what broke. Number to beat: a failed start found by a chat within 5 minutes, never first by Sam (19 Nov: Sam, 13 minutes).

Cost: about 2% of a week once, nothing per film. Reviewed against results at the end of the next film.
## For Sam
### Option 1: One safe way to start, tested first
Timed jobs stop opening blank chats. First a quick test tries two safe ways and keeps the one that works and costs least. Then a guard (an automatic block that stops a wrong step before it happens) refuses the broken kind of timer, and is proven to be switched on. Later, on its own yes, every started chat is checked, and if one fails you get one push saying so.
You would notice: queued jobs start on time with the project and the right model; "queued" means it was checked.
Lost: timers can't open chats on their own; queuing a job takes one extra step.
Added: every chat starts the same safe way; failures reach you from Claude within minutes, not by you finding them.
### Option 2: Block now, check later
Build the guard and switch it on straight away, with the rule, in one yes; a look through past timers decides whether a read-back check is needed later.
You would notice the same safe starts sooner, but the safe way is not tested unattended first.
Lost: the test before changing; changes come as one bundled yes.
Added: the guard works from the next chat on; a check that every guard is really switched on.
