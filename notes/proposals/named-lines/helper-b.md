# Helper B: named lines

## Leak
Small: the merged part leans toward "move the cleaned-takes fix into the shared tools" ("the fix lives in that film's code only"). Ignored here as an answer; weighed as one option.

## Results
- Pre-flight's carried lines grew 48 (chats 13, 15) to 60 (chat 18), then 61; none was settled (notes/archive/milburn.md lines 13, 20, and the chat 18 entries below them).
- The cost that matters: the real clipping fault ("clipcheck COULD NOT TEST") sat in that list and **reached Sam twice** as notes: Pat and Andy's name cards (chat 13, note c) and Milburn's card (chat 18) (milburn.md lines 13, 18). Both entries say the check never ran on this film.
- Picture checks: 28 to 31 per animatic, waved past as "same file as animatic 1" (milburn.md lines 13, 16, 20).
- Milburn cost 22% of a week against the 15% aim (milburn.md line 1). How much of that came from re-reading and re-naming the same lines: not in the record. That gap is a finding.
- How the waving-through works: one switch, `--faults-named`, lets the render go ahead however many faults there are (source/film_engine.py lock_fault; source/preflight.py near the end). No record says which lines were named, by whom, or since when, so a new line looks the same as an old one.
- Pre-flight's own rule says "COULD NOT TEST" stops the animatic (source/preflight.py: gate warnings containing it are moved to the stop list). But clipcheck's "COULD NOT TEST" is added as an ordinary fault instead, so the switch waves it through. That is the exact path the card fault took.
- The 60 false voice lines: the shared voice check measures the raw recording file whenever a film does not hand it the cleaned take (source/voices.py, prepared). Milburn's take joining and trimming lives only in milburn_voice.py, which no other film or the template uses (grep: nothing imports it; not in guides/kit-catalogue.md).
- Kit tests: notes/logs/broken.md (19 Nov 20:36) says facehouse_whole_head was fixed and round_page is "job 3's". The problem file says both still fail. One of the two is out of date.

## The real decision
This is not about Milburn's 61 lines. The question is how every film's pre-flight keeps each line meaning something across all its chats, so that a check that could not run, or a new fault, can never pass unseen. The bigger lever is the one switch that waves through a whole list. The size of the list matters less.

## Root cause
1. Naming is one switch over the whole list. Nothing remembers lines one by one, so every chat re-names everything and nobody owns a line.
2. "Could not test" is handled two ways. The gate stops on it, but clipcheck's version passes as a plain fault.
3. Checks guess their inputs. The voice check, the cast check (no scene(t)) and the house-style lists report false faults when a film does not hand them what they need. Fixes then go into film code, so the next film starts with the same false lines.
Earlier tries failed for these reasons. Chat 13 saw the card fault's cause and only wrote a proposal. Chat 11's ask to fix the stale tests was blocked by the guard because it had not gone through the proposal route, and nothing was routed afterwards.

## Approaches weighed
A. **Named per line, with an owner and an age (reframe).** Each named line is written once in the film's notes with its reason, like the existing exceptions table (source/waivers.py). A new line, or a line older than one animatic, stops the render.
B. **Clean the inputs at the source.** Shared voice, cast and style inputs go into the template and kit, and a kit test proves Milburn's false lines go to zero.
C. **Learn first.** Sort Milburn's 61 lines and Grand Theft Autism's current list into true fault, false line or could-not-test, and note where each cause lives (shared tool or film code). Replay whether a stop would have caught the cards before animatic 1.
D. **Show only what is new since the last run.** Rejected: it hides old faults, and Sam said no check is dropped.

## Proposal
C first, then A, B and the could-not-test fix as separate changes, each with its own yes.
- **Learn (changes nothing, about 1.5% of a week, Sonnet).** Sort both lists. Count the check fixes made in film code across Blessed and Milburn (from the code history). Settle which kit tests really fail.
- **Change 1: "could not test" always stops the animatic.** Kit test: replaying Milburn at animatic 1 must refuse on clipcheck. Number to beat: 0 of the 2 card notes would have reached Sam. About 1%.
- **Change 2: one record per named line, in place of the one switch.** The render refuses any unrecorded line, and any line older than one animatic without a fix or a question to Sam. Number to beat: the carried list starts the next film's first animatic under 10, and no line passes more than one animatic. Measured from pre-flight's own report. About 2.5%.
- **Change 3: shared inputs.** The cleaned-takes hand-over and the other false-line causes the learning step finds go into the template and shared checks, one cause per change. Number to beat: replaying Milburn gives 0 false voice lines (60 today). About 2% each.
- Total about 7 to 9% of a week, spread over tool chats outside a film. Set against the 15% per film, this is paid back if it saves one round of notes (Milburn's chats cost 2 to 3.7% each).
- What Sam would notice: shorter "Checks:" lines, and questions about specific old faults instead of a pile of them.

## Sam test
Q1 Expert: per-line ownership plus a stop on blind checks is standard practice for keeping alarms meaningful. Pass.
Q2 Best result: the learning step uses two films and the shared tools, not one chat. Pass.
Q3 Comprehensive: enforced by the render refusing, not by a chat reading something; each change has a replay test. Pass.
Q4 Most intelligent: four different approaches weighed; the root (the one switch) is fixed, not the symptom. Pass.
Q5 Risk: each change undoes alone. The risk is more refusals, which is the point. Pass.
Q6 Checked: sources named; the extras are under Unchecked. Pass.
Q7 Not cheap: fixes the switch and the inputs, not the list's length. Pass.
Q8 Nothing temporary: each change is permanent, with a kit test, and reviewed at film end. Pass.

## Lost / Added
Lost: the one switch that waves through the whole list (for any line older than one animatic). Added: a short notes table of named lines, and more refusals early on.

## Unchecked
Which of round_page and facehouse_whole_head fail now. Where the plan gaps and house-style lines come from. Whether Grand Theft Autism hands the checks cleaned takes. How much of Milburn's 22% came from naming.
