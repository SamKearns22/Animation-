## Leak
yes: the file name "staging-stills" and its pointer to Milburn review lesson 3 ("draw two small stills, numbered, build the pick") carry a solution. V1 is exactly that solution; V2 and V3 named the leak and weighed it as one option.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 4 | 4 | 5 | 17 |
| V2 | 4 | 4 | 4 | 4 | 4 | 20 |
| V3 | 4 | 5 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes. An expert moves the existing board check (rule 11) to where building starts, so a framing cannot be built before Sam has seen it, instead of adding a new by-hand step.
Q2: Evidence is Milburn's record (three builds of the reverse, board 18 Nov 06:22 after 22 move blocks, checked in story/milburn-board-sent.txt) plus the census (19 framing notes, 3 repeats, craft-census.md line 58); the learning step widens it to four films before anything changes.
Q3: Root cause found and checked: board_gate (source/rough.py ~668-704) runs only at the animatic and only asks whether a shot was ever on a board; rule 87's "ask first / 2-3 options" is by hand and was skipped. The fix is a tool refusal, proved by replaying Milburn's chat 6 and chat 10 builds; success is counted at film end.
Q4: Yes: by-hand stills, a build gate, reading the brief literally, a taste record, and learning first were all weighed.
Q5: One change, made only if the learning shows it is needed; it can be switched off alone. Risk named: a night run waits on a still for that shot (other work carries on).
Q6: Facts checked: ledger figures 2.84/3.74/3.24/2.73% (the problem file's 1.9/2.5/2.17 are wrong); note 5's words (milburn.md line 233); the brief's "the 180 of shot 1" (line 165). Sam's chat 7 and 11 exact words and the staging share of cost are marked unchecked.
Q7: Sized to stop rebuilds (one avoided rebuild is ~3% of a week) against ~0.7% once; not the cheap message version.
Q8: Permanent, written in rule 11 with its check, reviewed at film end against the numbers below.
## Pick
V3
## Why
V1 is the leaked answer: it relies on a chat choosing to follow it (rule 87 already asks for 2-3 options on one still and was skipped), covers notes only (not new shots, where Milburn's first build went unseen), and both stills come from Claude's own taste, which on Milburn pointed away from what Sam wanted. V2 and V3 find the same root cause; V3 edges it with wider evidence (four films), a stated threshold for the change, the rule 87 and night-run findings, and the numbered framings on a re-stage. Taken from V2: removing rule 11's "never sent again" clause (else a re-stage board breaks the rule), and the brief's camera line as one of the numbered framings (V2's approach 3), so the choice is not only Claude's taste. Added by the judge: the board record already stores a picture fingerprint per shot, so "changed since the last board Sam saw" needs no new record.
## Faults in the pick
- F1 [fixed] V3 did not remove rule 11's "sent once, never sent again" clause, which a re-stage board would break (from V2).
- F2 [fixed] Both re-stage framings could be Claude's taste alone; one numbered framing now follows the screenplay's own camera line word for word.
- F3 [fixed] V3 bundled a new "record each shot's camera and seats" step; the board record already holds a fingerprint per shot, so it is dropped.
- F4 [named] On an unattended run a re-staged shot waits for Sam's number; other shots and stages go on, but that shot cannot be finished overnight.
- F5 [named] Sam's exact chat 7 and chat 11 words are not in the repository; the learning step reads the earlier chats to settle whether a framing board would have caught note 5.
- F6 [named] The problem file's chat costs are wrong (ledger: 2.84/3.74/3.24/2.73%); the staging share of each is unchecked.
## Final version
**Step 1, learn (changes nothing, ~0.4% of a week).** Over Milburn, Blessed, Protest Tiers and Patriots 4 (notes plus earlier chats' transcripts), list every framing or staging note: Sam's exact words, whether a board of that framing reached him before it was built, how many builds it took, whether it was a repeat. Also read Sam's Milburn chat 7 and 11 words. Result: the share of rebuilt framings that were built with no board seen first.

**Step 2, the change (only if 2 or more staging repeats were built before a board; else stop and report).** One yes:
- The board check moves from the animatic to building: the move and clip tools refuse a shot whose current picture fingerprint differs from the one on the last board Sam received (the board record already stores it).
- A note about framing or staging marks that shot's board out of date. The reply to the note is one still sheet with 2-3 numbered framings, one of them the screenplay's camera line taken literally; the chat waits for Sam's number on that shot and carries on with other work.
- Rule 11's "notes on it are acted on, never sent again" is replaced by "a re-staged shot goes on a new board before it moves". Rule 87's two-failures clause is now enforced by this gate.
- A kit test replays Milburn's record and must refuse chat 6's and chat 10's builds.
- Cost: ~0.7% of a week once, ~0.15% per re-stage board.

**Numbers to beat (film end, from the board record and repeat marks):** framings built before a board: Milburn 2, target 0; staging repeats: 1, target 0.
## For Sam
### Option 1: No shot is built before you have seen its framing
First a short look back over four films, to count how often a framing was built and rebuilt before you saw a picture of it. If that happened twice or more, the building tool itself refuses to animate a shot until you have seen its framing on the shot board. When you give a note about where people sit or how a shot is framed, you get one picture with 2-3 numbered framings (one exactly as the script describes), and you answer with a number. On Milburn this would have stopped the Cabinet Room shot being built three times.
Lost: a re-framed shot is no longer animated straight from your note; it waits for your number.
Added: one picture to pick from before each new or re-framed shot moves, and a tool that enforces it.
### Option 2: Two pictures per framing note
When you give a note about framing, the chat draws two small pictures of different framings and asks "1 or 2?", then builds your pick. Cheap and quick, but it relies on each chat remembering to do it (a similar rule was skipped on Milburn), it does not cover brand-new shots, and both pictures come from Claude's own taste.
Lost: nothing.
Added: one extra short message per framing note.
