# Helper B: scheduled-jobs-attach

## Leak
Small: "without anything checking they could run" points toward adding a check. Not leaned on. (A search result also showed one line of `chat.md`, the chat's idea; I did not open the file and worked from the record.)

## Results
- All four 17:01 jobs were set as "start a fresh chat when fired" (persist_session false, created_kind ROUTINE). Every earlier timed job (10-18 Nov, 15 listed) was a reminder that woke an existing chat (persist_session true, created_kind REMINDER), and all of those ran. So this was the first use of the fresh-chat kind, and it failed 4 times out of 4 (list_triggers, checked).
- The fired chat got no project, **an invalid GitHub login**, and **no model**: the trigger's model field was empty, so job 2 ran on Sonnet, not on the model its brief named (job 2 transcript, list_events, checked). Jobs 1 and 4 asked for Opus high in their wording, which the trigger cannot carry (their run model is unchecked). So three things were lost, not one.
- Each run still reads "SUCCEEDED": that status only means the chat was started. Job 2 stopped correctly after 10 seconds and sent a push (transcript, checked).
- Money: job 2 cost $0.065 (transcript). Four runs come to about $0.26, roughly 0.2% of a week if Milburn's $32.40 = 22% (job 4 prompt and story/status.md). The other three runs are unchecked.
- The real cost was elsewhere. Sam found it himself at 17:14, it took 4 of his messages (7r62524n.md), and the work started 14-16 minutes late (child sessions 17:15-17:17, checked; job 3 attached to the main line, get_session, checked). The restart also lost part of a brief: job 1 got a short summary and had to be corrected at 17:18 to use the stored prompt with Sam's additions (a)-(f) (yah6eyjt.md). That is a second fault from the same cause.
- Gap: nothing records whether a woken reminder that then calls create_session works every time. The 14 and 16 Nov wake prompts did ask for that, but whether those chats opened is unchecked.

## The real decision
This is about how a chat gets started, for every film, not one tool's missing field. The rulebook has one safe way to start a chat (create_session: project, main line, model, effort, full brief). The fresh-chat timer is a second way that can carry none of those. The decision: should any chat ever start by a route other than create_session? And how do we find out about a start that failed before Sam does?

## Root cause
CLAUDE.md asks for create_session "when a chat opens the next chat". The queuing chat did not treat a timer as opening a chat, so it chose the timer kind that starts chats itself. The project requirement sat only in the prompt ("must be attached"), and a prompt cannot attach a project. Nothing checked the choice when the timer was made, and nothing checked the result when it fired; "SUCCEEDED" hid the failure. It depended on a chat reading a rule and applying it to a case the rule does not name.

## Approaches weighed
1. **One way to start a chat (reframe).** Timers are only ever reminders that wake an existing chat. The woken chat starts each job with create_session, passing the full stored brief. A guard refuses the fresh-chat timer kind.
2. **Check at queue time.** Keep the fresh-chat timers, and warn when one is made. This falls short: nothing a check does can give that chat a project, a login or a model.
3. **Check after firing.** The woken chat confirms each job chat is attached, can save and is on the right model, then reports a failure straight away. This catches every way a start can fail, including ones we haven't seen yet.
4. **Learn first.** Before anything changes, test one bound reminder that opens one test chat with create_session, and read the old wake runs, to show the safe path works when nobody is watching.

Chosen: 4, then 1, then 3, as separate yeses.

## Proposal
**Learn (changes nothing, about 0.5% of a week, Sonnet):** look back at the 14 and 16 Nov wake runs and check whether their create_session calls produced chats that were attached. Then set one 2-minute reminder in a chat that opens a test chat. Check: the project is attached, saving works, the model and effort match, and the brief arrived word for word. Number to beat: 1 test out of 1 passing on all four points. If it fails, nothing below goes ahead and Sam is told why.

**Change 1, its own Y:** "Every chat is started with create_session (project, main line, model, effort, full brief). A timed job is a reminder that wakes the queuing chat, and that chat starts the job." This goes into CLAUDE.md, Models and chats. It is enforced by a guard that runs before every timer is made and refuses the fresh-chat kind, so it does not rely on a chat remembering to apply the rule. Number to beat: 0 timed jobs starting without the project (now 4 of 4). Measured from list_triggers at each end-of-film review.

**Change 2, its own Y, after change 1 is in use:** after it starts each job, the woken chat runs a start check on every chat it opened. It confirms the project is there and the model is right. It sends Sam one push only on a failure, and it records "started: attached, model, brief" in the notes. Number to beat: a failed start is found by a chat within 5 minutes and never first by Sam (now found by Sam after 13 minutes).

Building both: about 1.5% of a week (Opus medium) on top of the 0.5% look-back, about 2% in all. That is a one-time cost, not one paid on every film, and set against 15% of a week per film it is small. What Sam would notice: queued jobs start on time with the right brain. A failure reaches him as one plain push saying what broke, not something he has to find himself.

## Sam test
Q1: Yes. Experts give a system one way to start a job and check its health after it starts, rather than warn about a broken path.
Q2: The evidence is all 19 timers plus the transcripts, not one evening. The look-back fills the one gap.
Q3: A guard enforces it, not reading. The after-start check catches failures we haven't thought of. Results are reviewed at the end of each film.
Q4: Four kinds of approach were weighed (reframe, check at queue time, check after firing, learn first).
Q5: Each change undoes on its own. Nothing goes ahead until the test passes.
Q6: The sources are named above. The gaps are listed below.
Q7: The cheap option (a warning only) is rejected because it can't fix what the timer can't carry.
Q8: Permanent changes, reviewed at film end. The test is a step to learn from before changing, not a trial run.

## Lost / Added
Lost: timers can no longer start chats on their own. The queuing chat must still exist to be woken. Each timed job takes one extra step to start.
Added: every chat starts the same safe way, with project, login, model and the full brief. A failed start is reported by Claude within minutes.

## Unchecked
Run model and cost of jobs 1, 3, 4. Whether the 14 and 16 Nov wakes opened attached chats. Whether a woken old chat always has the tools to call create_session. The %-of-a-week rate (worked out from Milburn).
