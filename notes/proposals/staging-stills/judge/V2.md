# Helper B: staging notes take several rounds

## Leak
The file name ("staging-stills") and its pointer to milburn-review lesson 3 ("draw two small stills, numbered, build the pick") carry a solution. Weighed below as one option, not assumed.

## Results
- The reverse (shots 4a-4c, 7a-7e) was built three times: chat 6 (Andy and Pat level, side by side), chat 10 (lens 1.02 m, Andy 2.0 m, Pat 2.42 m, staggered), chat 11 (equal and centred, same depth 2.2 m, camera 1.2 m "like Milburn's") (notes/archive/milburn-handovers.md lines 63, 101; notes/archive/milburn.md line 7).
- Sam's first note was vague: "the scene composition in scene 4 as proposed is poor" (milburn.md line 233). Chat 9 decided for itself what was poor, and named "two equal busts side by side, dead centre" as a fault (handovers line 91). Sam's final answer was equal and centred. So the second build went the opposite way to what Sam wanted. The first build was close, and its real faults were probably the empty baize, the cut name cards and the arm under the table (unchecked: Sam's exact chat 7 and chat 11 words are not in the repository).
- The screenplay already said "the 180 of shot 1" (milburn.md line 165), which is a mirror of Milburn's level, centred shot. Chat 10's lower, staggered camera left that.
- No shot board of the reverse reached Sam until 18 Nov 06:22, after 22 move blocks and both builds (story/milburn-board-sent.txt). Chats 6 and 9 each pushed the board on to the next chat (milburn.md lines 240, 246).
- Chat costs from the ledger's app figures: chat 6 2.84%, chat 9 3.74%, chat 10 3.24%, chat 11 2.73% (notes/ledger/milburn.md). These do not match the problem file's 1.9/2.5/2.17. How much of each went on staging: unchecked. Film: 22% against the 15% aim (milburn.md line 1). The reverse was 1 of the film's 4 repeats (milburn-review.md line 7).
- Across earlier films, "a composition for each shot, agreed before building" would have saved 19 framing notes (3 repeats), the largest group in the census (notes/proposals/craft-census.md line 58).

## The real decision
The question is not "how do staging notes land faster" but this: is every shot's framing agreed with Sam on a picture before it is built, both when the shot is new and when a note re-stages it? The bigger lever is the shot board that already exists (rule 11). Its check sits in the wrong place, and it has a hole.

## Root cause
1. Rule 11's check only runs at the animatic. `rough.board_gate` (source/rough.py line 668) refuses an animatic for a shot that is on no board. It only checks that the *first* board came before movement. Shots added later can be built, and rebuilt, before their board is sent. Chats 6 and 9 did exactly that.
2. Rule 11 says "notes on it are acted on, never sent again". A re-stage after a note is therefore built straight away, with no picture.
3. A vague note was read by Claude's own taste, not by the screenplay's camera line or by asking Sam. That is a taste call, and CLAUDE.md says to stop for those.

## Approaches weighed
1. **Two numbered stills per staging note** (lesson 3). Cheap, but Claude picks both options from its own taste. On Milburn that taste pointed away from Sam's choice, so both stills could miss. It also covers notes only, not new shots.
2. **Reframe: put the existing board check where building starts.** A shot cannot get movement, or be re-staged, until its current framing is on a board Sam has received. A staging note marks that shot's board out of date.
3. **Read the brief literally.** The board row quotes the screenplay's camera line, the drawing follows it, and any departure becomes a numbered question.
4. **Learn first.** Measure every framing or staging note in Milburn and Grand Theft Autism: was the shot on a board Sam had seen before it was built, and did the note land first time?

Chosen: 4, then 2. Approach 3 waits for 4's result.

## Proposal
**Learning (changes nothing, about 0.5% of a week).** From both films' notes and their earlier chats' transcripts, list each framing or staging note with three facts: was a board delivered before the build (yes or no), how many builds it took, and Sam's exact words. Result: the share of re-builds that came on shots with no board seen first. If most did, change 1 follows. If notes still came back wrong on shots Sam had already seen on a board, approach 3 becomes the next separate change.

**Change 1 (one yes).** The board check moves from the animatic to building, and the rule 11 "never sent again" clause is removed.
- What changes: the moves tool and the build step refuse a shot whose current framing (camera, places, who sits where) is not on a delivered board. A note tagged staging or framing marks that shot's board out of date, and the shot's new board still is the reply to the note.
- How it is enforced: in the tool, not by a chat choosing to follow a rule. A kit test proves it refuses Milburn's chat 6 and chat 10 builds.
- Number to beat: Milburn built the reverse 3 times. Target: no shot built more than twice (once after its board, once from a note on it), and no framing note on a shot that had no board first. Measured from the notes table's "seen before" marks and the board record, in the end-of-film review.
- Cost: about 0.8% of a week once (the gate and its test), then about 0.2% per board still. One avoided rebuild saves about 2-3% (one chat), set against the 15% film.
- What Sam would notice: a still of each new or re-staged shot before it moves, answered with a note or a number. Fewer clips that come back.

## Sam test
- Q1: An expert puts the check at the point it protects, before the build, rather than adding a new step.
- Q2: The evidence spans two films plus the census of three earlier films. The learning step widens it before any change.
- Q3: A tool refusal, not a reading choice. It is tested on Milburn's real failures.
- Q4: Four different approaches were weighed. The chosen one fixes the cause, not the symptom.
- Q5: One change, which can be undone alone. Its risk is one still's wait per staging note.
- Q6: Sources are named. The figures that do not match, and the staging share, are marked.
- Q7: It is sized to stop rebuilds, not as a cheap message.
- Q8: It is permanent, and reviewed when the film is complete.

## Lost / Added
Lost: building a re-stage straight from a note, without waiting for a still. Added: one board still before every new or re-staged shot moves.

## Unchecked
Sam's exact chat 7 and chat 11 words. What chat 6 "proposed" (a clip or a still). The staging share of each chat's cost. Grand Theft Autism's staging notes. Why the problem file's chat costs do not match the ledger.
