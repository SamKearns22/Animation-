## Leak
none
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 3 | 3 | 5 | 15 |
| V2 | 4 | 4 | 4 | 4 | 4 | 20 |
| V3 | 4 | 4 | 4 | 3 | 4 | 19 |
## Sam test
Q1: Yes. An expert keeps a guard that has already stopped the known failure (the hook blocks all 5 replay replies), measures before tuning, and tests the filter instead of trusting it. Tests show the hook's holes, so those are closed first.
Q2: The unit is the whole film and every system change made during it. The evidence is the replay, hook tests run here, the ledgers, git counts (50 commits to the rulebook, catalogue or CLAUDE.md from 12 to 15 Nov) and film costs of 54-62%. Two gaps are named: changes per film and asks per film.
Q3: Root cause: Claude's own idea has no outside critic, and no results are recorded (every ledger reads "0 rounds, 0 notes"). Enforcement comes from the hook, a kittest and the step-6 review, never a chat choosing to comply. The dodge (change without asking) goes to the step-6 review, which lists every system commit. Its notes count stays blind until C2: named.
Q4: Five different approaches were weighed: as built; undo for a by-hand rule; reframe; learn-first; route only "large" changes. The reframe, with learn-first as its first job, is the best of them.
Q5: Risks: the time Sam waits, and about 1.3% of a week per routed change. The replay is weak proof: the prompts encode cases 1, 4 and 5. Each change can be undone alone. Sam trusts real film results at step 6, not the replay.
Q6: Every figure was checked against its file, with sources named. Asks per film, the cost of C2-C4, and bias from a judge of the same model family are marked unchecked.
Q7: Not the cheap "as built": it closes the known holes and makes the measure work. Its honest cost could reach about 13% of a week per film at 10 asks. That is why C4 exists.
Q8: Permanent from the first Y, with no trial. Every change is reviewed against the film's results when Sam calls the film complete.
## Pick
V2
## Why
V2 and V3 both see the real decision: how system changes come to make whole films better and cheaper. Both see that the "as built" route has a blind measure and a leaky guard. V2 wins on honesty. Its rule says what the hook really enforces (changes put to Sam), and changes made unasked go to the end-of-film review. V3 keeps the rule as sent ("any change, however small"), which promises Sam more than the hook checks. V1 takes the replay at face value. It does not see that the route's own success measure reads zero notes, misses the tested bypasses, and guesses 3-6 changes per film against 50 rulebook commits in four days.
Taken from V3: (a) the hook's refusal tells the chat to "reword the question", which invites a dodge V2 missed. (b) More test questions: a routine word overriding a change word, and "gate" not being listed. (c) The learning step is the already-queued results-first review of Protest Tiers, plus the first real run of step 6. (d) C4, one route run per problem rather than per edit, used if changes per film are many. (e) The 50-commit count, which I checked; V2's 101 rests on subject text.
My own changes: the hook fix (C3) goes first, because its evidence is already in hand (the tests run here) and it needs no learning. Resuming Protest Tiers is put to Sam as its own question, not bundled into the route's Y.
## Faults in the pick
- F1 [fixed] V2's measure was "0 pushes after a verdict", but the route's own notes say pushes fall when Sam tires. It is replaced by the replaced-rate, notes per film and cost per film.
- F2 [fixed] The hook's refusal advises "reword the question" (source/propose.py reply_faults). It goes in C3.
- F3 [fixed] The hook fix waited behind the learning step though its evidence is in. It is now the first routed job.
- F4 [fixed] V2's "101 commits" was counted from subject text. Replaced by a checked 50 (rulebook, catalogue, CLAUDE.md, 12-15 Nov).
- F5 [fixed] Ending the hiatus was bundled into the route's Y (V3). It is now a separate question.
- F6 [named] The replay is weak proof. helper.md encodes the answers to cases 1, 4 and 5, and judge and helpers are the same model family as the chat. Real proof comes only at step 6 on a real film.
- F7 [named] The route's cost per film is unknown. At about 1.3% a run, 10 asks cost about 13% of a week, close to the whole 15% target. C4 is the remedy, if the count shows it is needed.
- F8 [named] Changes made without asking Sam are judged only at film end. Until C2, step 6 reads 0 notes.
- F9 [named] Sam's own "I want a rule" wording waits one route run each, about 1.3%.
## Final version
**Change 1 (Sam's Y, permanent).** Keep the hook on. The rule is written in CLAUDE.md "Rules are permanent". It replaces the 12 Nov "Before suggesting anything" bullet, so the rulebook does not grow, and gets a last-table row with the check `propose.py hook`. Wording: "Every change to rules, tools, checks, kits or how films are built that is put to Sam goes through the proposal route first (helpers, blind judge, top two in plain English with Lost/Added and Critiqued). The guard refuses an unjudged ask. Changes made without asking are listed and judged in the end-of-film review against the film's results." Measure: proposals later replaced (`propose.py mark replaced`), Sam's notes per film, % of a week per film.

**Separate question (Sam's Y): resume Protest Tiers now.** The route can only be proven on a real film. Film work stays outside the route.

**Then one change at a time, each through the route with its own Y:**
- **C3, first: close the hook's holes.** Today a routine word (render, clip) overrides a change word, "gate" is unlisted, and the refusal says "reword the question". Beat: a kittest blocks "Shall I change the render tool so it reuses cached frames? Y/N" (a real change, 15 Nov), "Y or N to add a new check before every animatic?", "tighten the gate" and the 5 replay replies, and passes routine animatic, render and clip Y/Ns. The refusal names the route only.
- **Learn (read-only, no Y, about 2-3%, unchecked).** This is the queued results-first review of Protest Tiers. It counts from transcripts and git: Sam's notes and repeated notes per round, faults a check should have caught, each chat's cost by cause, system changes per film (asked and silent), how many were replaced, and asks per film. Then it runs `propose.py review protest-tiers` (step 6's first real run). This sets the baseline.
- **C2: the ledger records notes and faults at each handover.** Beat: matches the hand count from Learn, and no ledger reads 0 notes for a film that had notes.
- **C4, only if Learn shows many asks per film:** one route run per problem, not per edit. Beat: route spend per film below the film's system-change spend in Protest Tiers.
- **C5, only if Learn shows silent changes are replaced more often than asked ones:** silent changes are routed too. Beat: the replaced rate.

**Cost.** About 1.3% of a week per route run (ledger: helpers 4.41% and judges 2.12% for 5 cases). Learning is 2-3%. C2-C5 are about 1.3% each plus their build (unchecked). Films now run 54-62%.

**Undo.** Each piece alone. The hook is one entry in the Stop list. The rule wording goes back through the route.

**Sam notices:** back-end questions arrive with two judged options and a "Critiqued" line. He gets a results line at each film's end, and real note counts in the ledger.
## For Sam
### Option 1: Switch it on, fix its holes, measure it on the film
Every change to how the films are made is checked by two fresh helpers and a blind judge before it reaches you. A guard stops me asking you to approve one that wasn't. I tested the guard and found ways past it. Closing those is the first job. Next, a read-only count of your notes and costs on Protest Tiers, so we can see whether the films get better. The film can restart now (separate Y).
Lost: about 1.3% of a week per change, and a short wait before you see wording for rules you ask for.
Added: two judged options behind every back-end question, real note counts, and a results check when you call a film finished.
### Option 2: Switch it on exactly as built
The same helpers, judge and guard, made permanent today with no fixes. It is cheaper and faster. But the guard misses some questions that use words like "render" or "clip", and the results check at film end would read "0 notes", so we couldn't tell whether it worked.
Lost: the holes stay, and there's no working measure of whether films improve.
Added: the same judged options, one fewer round of building before the film restarts.
