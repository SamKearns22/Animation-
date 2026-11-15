## Leak
Hints: add "every film"/"from now on"; drop "reword". Ignored.

## Results
- Probe, re-run (probe.py): 9 of 12 change asks missed, 1 of 10 routine asks stopped.
  - 6 misses: a routine word wins first (render, clip, animatic, voice, sheet ×2).
  - 3 misses: no change word at all (subtitles, fps, house look).
  - The wrong stop: "hook" in "hook text".
  - The probe's questions are synthetic, written by the guard's own chat (problem file).
- **Real asks are not seen as asks.** Seven real system-change asks went through `reply_faults`; `questions()` found 0 asks in all 7.
  - Sources: morning-report.md lines 43, 71, 76, 82, 94; blessed-handovers.md line 66; protest-tiers.md line 13.
  - Forms: "Decide:", "- **Needs Sam:**", Y/N with no "?".
  - These are the notes' copies; the reply wording is unchecked.
- The morning report carries decisions to Sam (overnight-run.md line 14), but the Stop hook never reads it.
- Kittest uses only "Need: Y or N" asks (kittests.py 2519 on); no unrouted.md yet.
- Changes are frequent: 50 commits to the rulebook, catalogue or CLAUDE.md, 12–15 Nov (install-route.md; not rechecked).
- A route run costs about 1.3% of a week (install-route.md). The cost of a wrong stop is unchecked.
- Gap: there is no labelled set of real asks.

## The real decision
Can an unjudged change reach Sam, or get built, in a whole film? Three levers are bigger than the lists:
- what the guard reads (replies only, not files);
- what counts as an ask;
- a check where changes are written.

## Root cause
The guard judges wording at two layers, ask and change, both with word lists. But a change is defined by its effect: it outlasts this film and is written into system files. The chat being guarded controls the wording. The lists were tested on one format only, and the routine veto runs first.

## Approaches weighed
1. **Patch the lists.** Cheap, but it chases wording.
2. **Reframe: guard the point of change.** Flag any write to system files without a verdict, excluding film files as `review()` does. Complete by design, but it comes after Sam is asked.
3. **Model classifier.** A small model judges what each ask means. Unchecked here.
4. **Learn first.** Build a labelled set of real asks and measure every option on it.

Choice: 4 first, then one change at a time.

## Proposal
**Learn (changes nothing).**
- A Sonnet chat collects every decision put to Sam: notes/, archive/, the morning report, and the Protest Tiers and Blessed chats (`list_events`).
- A blind helper labels each one change or routine.
- The set becomes a kittest fixture, split into a build half and a test half.
- Today's guard and approach 3 are measured on it.
- Cost: about 2% of a week (unchecked).

**A (evidence in hand): the refusal names the route only.**
- Enforced by: the kittest.
- Beat: no reworded repeat of a blocked ask in unrouted.md.

**B (evidence in hand): the ask detector reads every decision form**, including files sent to Sam.
- Beat: 100% of fixture asks detected, with no new routine stops.

**C (after learning): the classifier**, approach 1 or 3, whichever wins on the test half.
- Beat: 0 change asks missed (test half plus the probe's 12); at most 1 in 50 routine asks stopped.
- Enforced by: the kittest.

**D (after the first step-6 review): approach 2**, only if the review lists an unjudged system commit.
- Beat: 0 such commits per film.

Each change gets its own Y, can be undone alone, and is reviewed at the film's end.

Cost: about 5% of a week in total, built once and spread across films (unchecked), against 15% per film. The running cost is near zero, unless the model classifier wins.

Sam would notice: every back-end ask, the morning report included, comes with its explanation and "Critiqued:". Routine questions pass.

## Sam test
Q1: Yes: measure on real asks; enforce at the effect.
Q2: The scope is the real asks plus two films' chats, not 22 synthetic questions.
Q3: The root cause is named. Kittests and the backstop enforce it, not a chat's choice.
Q4: Four different approaches were weighed. The evidence picks.
Q5: Each change can be undone alone and is tested on the fixture first.
Q6: Sources named; costs unchecked.
Q7: Not the list patch: it also closes ask detection and the file route.
Q8: Every change is permanent and is reviewed against the film's results.

## Lost / Added
Lost: nothing Sam sees. Added: an ask fixture, a wider ask detector, the morning report under the guard, and possibly a check on writes.

## Unchecked
How the replies were worded; the costs; prompt hooks; the 50-commit count.
