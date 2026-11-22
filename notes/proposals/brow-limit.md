# Proposal: The brow limit learnt on Milburn lives only in that film's notes

Status: open (un-parked 22 Nov, Sam: "Milburn: begin all"; his 19 Nov words below still stand)

## Problem
On Milburn, Sam noted that scene 7's angry faces looked wrong: the brows tipped into steep slashes through the
glasses. Chat 13 found the cause: past a brow pull of about 0.14 the brows go too steep, and capped the moods there.
That limit and the 3/4-parts rule (from the three-quarter-people work) are written only in Milburn's notes, so the
next film can break them again. Milburn review lesson 9; Sam (19 Nov): yes, the brow limit enforced by the kit
(the kit: the shared drawing code for people).

## Facts
- notes/archive/milburn.md line 10 (chat 13): "scene 7's moods pushed the brow pull past scene 4's (rage 0.16, gape
  0.22 + brows lowered); past ~0.14 the brows tip into steep slashes through the glasses. Now rage and gape use
  furious's 0.14 ... Rule 56: no other mood anywhere above 0.14."
- Rule 56 in guides/film-quality-rules.md: check what it says about brows (unchecked).
- The moods live in source/people.py and source/people_famous.py (e.g. 'showman' brow 0.03); where rage and gape
  are defined: unchecked (search "rage", "gape").
- Whether the 0.14 limit holds on every head (house head, famous heads, turned heads) or only Milburn's with glasses:
  unchecked.
- The 3/4-parts rule: notes/proposals/three-quarter-people.md (adopted 18 Nov); whether it is in the rulebook:
  unchecked.
- Rule 12 in the queue (Sam Y): no rule without a working check.

## Record
notes/archive/milburn.md
source/people.py
source/people_famous.py
source/
guides/film-quality-rules.md
notes/proposals/three-quarter-people.md
source/kittests.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 2f7c2381daa5d0cf -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper B, V3 = helper A. Picked: V3 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the problem file says chat 13 "capped the moods" at 0.14 and quotes Sam's Y to "the brow limit enforced by the kit", which points straight at a number cap in the kit (V1 took it as given).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 3 | 2 | 4 | 13 |
| V2 | 4 | 4 | 4 | 4 | 4 | 20 |
| V3 | 5 | 4 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes for the pick: it guards the drawn result (the brow's angle on the actual head) rather than a typed number, and proves the guard against the old note and against approved looks before trusting it.
Q2: Evidence is every mood table on record on the heads that used it, front and turned, plus two films' notes (Milburn note 1; Ad-Vanced Notice 36c, where a plain cap at 0.13 made anger stop showing). Wide enough; brow code outside faces/turnhead (traitors, press_secretary) is named as not covered.
Q3: Enforced by pre-flight refusal, not by reading. Root cause found with evidence: the input "frown" draws a different angle per head (faces.py brow_uv adds it on top of each head's slope), and the only guard was a number in one film's file against a rule (56) merged away on 10 Nov. Success is measured: replay flags the old note on its own; zero steep-brow and zero "anger doesn't show" notes over the next three films.
Q4: Four approaches weighed (cap, measure drawn angle, mood sheet, learn first); measuring the drawn result fits the "checks live in the kit" rule. The plain cap is rejected on evidence (36c).
Q5: Learning changes nothing; each change has its own yes and undoes alone. Weak spot: the "crosses the glasses or eye" test is new geometry not yet shown to work; it is only trusted once the replay shows it flags the old note and passes the approved faces.
Q6: Checked here: milburn archive line 10, milburn.py lines 170-175, rule 56 merged into 89 (rulebook line 126), faces.py brow_uv line 196, turnhead.py brows, preflight.py line 206 lost_parts, ad_vanced_notice_cast.py frown cap 0.13. Unchecked: brow share of chat 13's 2.25%; the replay's real size.
Q7: Not the cheap clamp. Honest cost about 2.1% once; the replay's cost is an estimate and is capped (see Final version).
Q8: Permanent kit measure, pre-flight refusal and rulebook lines; reviewed at the next film's end.
## Pick
V3
## Why
V3 and V2 share the right reframe (limit the drawn angle, learn the number first), but V3's facts are better: it found that the 3/4-parts rule is already refused on every film by pre-flight (preflight.py line 206, lost_parts on the film's cast), so V2's Change 2 (make that test follow the film) mostly rebuilds something that exists, and V2's "kit tests block nothing" is true of the kit test but misses that refusal. V3 also calibrates against approved angry faces, not only against the bad one, so the limit cannot be set so low it kills the anger. V1 is the cheap cap the record already shows failing (Ad-Vanced Notice 36c) and bundles three changes in one yes.
Taken from V2: the anger guard. When a mood reaches the brow limit, pre-flight names it and the animatic's Checks line says its anger is carried by squint, lids and mouth, and the kit test checks that a stronger mood still draws a visibly different face from a weaker one (the 36c fault). Also from V2: the learning sheet is looked at at phone size beside Sam's note picture, not only measured.
## Faults in the pick
- F1 [fixed] No guard against the opposite fault (anger stops showing once the brow stops, Ad-Vanced Notice 36c); added from V2.
- F2 [fixed] The replay "every mood on every head on record" had no size limit; now capped to moods with a brow pull above zero, front and one turned view, on the shared face code only, about 0.5%, stopped and reported if it runs past 1%.
- F3 [fixed] "Pre-flight refuses any frame": pre-flight draws sample frames, not every frame; now pre-flight checks each mood on each head once (the angle depends on mood and head, not time), which covers every frame.
- F4 [named] Brow code outside the shared face code (traitors.py, press_secretary.py, a film's own drawing) is not covered; a film that draws its own brows must route them through the shared code or is listed in its notes.
- F5 [named] The "unless the film writes down a reason" escape could be used to skip the limit; every use shows on the Checks line for Sam.
- F6 [named] The learning may find no single angle separates bad from approved faces (glasses may matter); then Change 1 is re-sized from that result before it is built, not built anyway.
## Final version
**Learn first (changes nothing; about 0.5% of a week, stopped and reported past 1%; Sonnet).** Draw every mood with a brow pull above zero from every mood table on record, on each head that used it, front and at one turned view, through the shared face code (faces.py, turnhead.py). Print each brow's drawn inner angle and whether it crosses the glasses or the eye. Mark the known-bad faces (Milburn rage 0.16, gape 0.22) and the approved ones (Milburn furious in scene 4, the angry Blessed jurors, Ad-Vanced Notice anger 6). One labelled sheet, looked at at phone size beside Sam's note picture. Result: the angle (or angle per head kind, with and without glasses) that separates bad from approved, or the finding that none does.

**Change 1, own yes (about 1.5%, Opus medium, one chat), sized from that result.**
- The shared brow code measures the inner angle it draws on the head being drawn.
- Pre-flight checks each mood on each head the film uses, front and turned, once: it refuses a brow past the learned limit or crossing the glasses or eye, unless the film writes a reason (shown on the Checks line).
- Anger guard: a mood held at the limit is named on the Checks line ("rage: brow at its limit; anger from squint, lids, mouth"); the kit test checks that a stronger mood still draws visibly differently from a weaker one.
- Kit test: flags Milburn's 0.16 and 0.22, passes 0.14 and every approved look, gives the same limit angle on a kit head and a famous head.
- Written once in the rulebook with that test.
- Number to beat: zero steep-brow notes and zero "anger doesn't show" notes over the next three films.

**Change 2, own yes (about 0.1%).** The rulebook gains the 3/4-parts line, naming the kit test and the pre-flight refusal that already exist.

Total about 2.1% once; nothing per film after. Reviewed at the next film's end.
## For Sam
### Option 1: Measure the brow, then guard it on every face
First a quick test sheet: every angry face from past films, on every head, to find exactly how steep a brow can go before it looks like the slashes you marked on Milburn, while keeping the angry faces you approved. Then the drawing tools measure each brow as they draw it and refuse a slash before you ever see it, on any character, front or turned. If a face hits the limit, its anger is pushed into the eyes and mouth instead, and the check note says so. About 2% of a week, once.
Lost: brows can't go steeper than the limit unless a film writes down why (you'd see that in the check note).
Added: one short test sheet, a brow check on every film, and two lines in the rulebook (the brow limit and the turned-people rule).
### Option 2: Fixed brow cap in the drawing tools
The drawing tools simply refuse any brow pull above Milburn's 0.14, and the rulebook records it. Cheapest and quickest (well under 1% of a week), but the same number draws a different slope on different heads, and a cap like this on Ad-Vanced Notice made stronger anger look the same, which cost you a repeat note.
Lost: stronger anger past the cap looks the same as the cap; other heads may still get slashes or lose anger.
Added: a one-number cap and two rulebook lines.
