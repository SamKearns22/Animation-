# Proposal: Statement One lessons from building European Protests Ranked (EPR)

Status: declined (2026-11-16)

## Problem
Sam (16 Nov): "Acknowledging that EPR was a non standard film that required research, new crowd technique, and was
built on a speculative screenplay rather than a final one, what Statement One lessons can we learn from the build
process of this film?" EPR is European Protests Ranked (the "Protest Tiers" job): a 4-tier, 43 s satire film of real
protests (Spain, Germany, France, Albania). Statement One (CLAUDE.md, Sam 13 Nov) is the three aims every stage works
to: high quality, fewer notes and faults, a film within 15% of a week. The film finished at about five times its
first plan in cost and with long rounds of notes. The decision is which lessons from how this one was built are real
(shown by the record), which are specific to its unusual kind, and which of them should change how future films,
including ordinary ones, are built, one change at a time, each shown to cut cost or notes without lowering quality.
Sam wants lessons for the build process, not a cost post-mortem alone. Every film is new; no lesson may mean less
joke, worse films or reused content.

## Facts
- Cost (notes/ledger/protest-tiers.json, .md; app figures for most chats): 61 chats, 101.29% of a week spent; first plan
  21.5% (notes/protest-tiers.md "First plan"); the ledger's later estimate 63.51%. By stage at the end (spent when each
  stage closed): plan 0.7 planned; unplanned plan extras (research) 10.08; cast 2.09 planned, 16.04 cum; sets 3.7 planned,
  20.78 cum; moves 3.07 planned, 32.08 cum; animatic 1 at 34.21; round 1 moves 4.45 planned, 53.21 cum; round 2 0.865
  planned, 100.78 cum (about 47.6% of a week); final 0.16 planned, 101.29. Chats by day: 12 Nov 6, 13 Nov 1, 14 Nov 6,
  15 Nov 24 (42.0%), 16 Nov 24 (39.3%).
- Kind of film: new crowd technique and research (Learn/Protest-tiers notes: notes/framing-research.md, references/
  protest-tiers/, ledger "plan extras"); the brief of 12 Nov is a 4-tier screenplay with second-by-second beats
  (notes/archive/protest-tiers-brief.md). The brief was re-staged after research (notes/archive/protest-tiers-plan-r0.md;
  "re-staging" at line 378 of notes/protest-tiers.md); how much of it was speculative and later changed: for the helpers
  to measure from the notes (unchecked here).
- Notes and faults: the film's notes file lists rounds: Round 1 (animatic 1), Round 2 (animatic 2, 16 Nov, film
  reopened), per-city Albania rounds 3, 4, 5 and France rounds 3, 4, 5 on single clips, Germany G12-G23, Albania A4-A39,
  France F4-F24 items (notes/protest-tiers.md; counts for the helpers to take, unchecked). The ledger rows' own notes and
  repeats fields read 0 for every chat (unrecorded).
- Earlier cost work: notes/cost-diagnosis.md (re-reading history ~49% of an Opus chat); notes/proposals/learn/
  protest-tiers-costs.md (chats 0-8 measured, chats 9-32 from handover wording; critique + rework + re-render +
  code-finding chats about 30% of that span; moves 25.3% against 7.6% planned; fix rounds on hunt lists, a pre-flight
  crash, black frames); notes/proposals/*.md (history-and-search, startup-reading, late-faults, estimates,
  startup-fixes, code-finder, guard-holes, install-route, claude-md-duplicates) each treat one cause; their verdicts and
  state (adopted / declined) are in each file's Status line.
- Process events in the film's notes: stage-stop (budget) hook fired repeatedly; Sam overrode it ("continue here until
  done"; "X1: no budget talk this film"); round 2 work was split into Germany, back-half (France) and Albania chat lines;
  a chat's unpushed work was lost and redone (Germany chat 6 -> 6b); two code-search and hand-over-cost effects named in
  other proposals. Parallel chat lines merged into one main line.
- Limit: chats 9-32 of the early record cannot be opened from this account (learn/protest-tiers-costs.md); cost by
  cause for them is title-level only. Whether the end-of-film review (propose.py review) has been run for EPR:
  unchecked. EPR is the first film built after the proposal route and the 13 Nov fixes.

## Record
notes/ledger/protest-tiers.json
notes/ledger/protest-tiers.md
notes/ledger/protest-tiers
notes/protest-tiers.md
notes/archive/protest-tiers-handovers.md
notes/archive/protest-tiers-brief.md
notes/archive/protest-tiers-plan-r0.md
notes/archive/protest-tiers-reporting.md
notes/framing-research.md
notes/archive/framing-research-handovers.md
notes/proposals/learn/protest-tiers-costs.md
notes/proposals/learn/code-search-count.md
notes/cost-diagnosis.md
notes/proposal-route.md
notes/proposals/history-and-search.md
notes/proposals/estimates.md
notes/proposals/late-faults.md
notes/proposals/startup-reading.md
notes/proposals/startup-fixes.md
notes/proposals/code-finder.md
notes/proposals/guard-holes.md
notes/proposals/unrouted.md
guides/film-quality-rules.md
guides/job-packs.md
guides/kit-catalogue.md
CLAUDE.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 848fda94fb5cd8f4 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = chat, V3 = helper A. Picked: V2 (chat). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
none (the problem's "one change at a time, each shown to cut cost or notes" is the route's own rule, not an answer; it names no remedy)
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 4 | 5 | 4 | 4 | 4 | 21 |
| V3 | 3 | 3 | 3 | 3 | 4 | 16 |
## Sam test
Q1: Yes: an expert locks length, cameras and pacing on a rough moving version (pre-visualisation) before building, and measures which notes cost most before choosing; the pick does both, in that order.
Q2: Widened from V2's one film to three (EPR, Blessed, Remakes, as V1 does), so the gate is not set by one unusual film; the evidence is the ledger by stage plus every note, the right evidence for "where does the money go after the first moving picture".
Q3: Root cause shown in the record: F1 (France camera, planned 0.8 m) and A1 (Albania, planned 3 m) were reversed on moving clips after passing the framing research and the still pencil roughs; length grew 16 s to 43 s at animatic 1 (R4, R2). Enforced by the handover check refusing cast without Sam's recorded Y on the clip, not by a chat choosing to; a number to beat says whether it worked.
Q4: Five approaches weighed (learn first, moving blocking pass, per-second pricing, automatic repeat/clipping/sameness checks, push guard), plus V3's "kind of film" flag; the blocking pass is the only one aimed at the 66% spent after animatic 1 without cutting the joke.
Q5: The learn step changes nothing. The blocking pass is one yes, made only if the learn step's threshold is met, and is undone by removing one gate line and one rule sentence. Weak point named: its cost per film is not yet measured (F2).
Q6: Checked here: 101.29% / 21.5% / 34.21% at animatic 1 (ledger), 16 s planned (plan-r0 line 153), 43 s final (notes), F1/A1/R2/R4/G4 wording (notes lines 189, 192, 206, 208, 181), Blessed 21.02 of 62.21 at its animatic (ledger), "After the film" 33.55% (ledger line 118). Note counts (~104) and classes are the helpers' own counts: unchecked.
Q7: Sized by the 66% it targets, not by price; the 1.5-3% per film is stated honestly as unchecked; no cheap trap (the pass is at real cameras and real length, not another still sheet).
Q8: Nothing provisional: either a permanent part of rule 11 with its gate, or not built; reviewed when Sam declares each of the next two films complete.
## Pick
V2
## Why
V2 has the sharpest root cause, and it is in the record: the cameras Sam reversed had already passed two still checks (the framing research and the pencil roughs), so another still sheet would not have caught them; only a moving version at real camera and length would. Its remedy goes straight at the measured result (two-thirds of the cost after animatic 1, round 2 at 47.6% against 0.865% planned) and cuts no joke. V1 reaches nearly the same place but proposes the existing still pencil kit "timed", which is the tool that already missed F1 and A1. V3 is the chat's own pre-helper guess: it rests on unchecked facts ("speculative script" as the driver; the record shows Sam's own length and camera notes on moving pictures drove the overrun), and its main change, a bigger estimate for unusual films, prices the overrun rather than preventing it.
Taken from V1: the three-film learn scope (Blessed's 66% after its animatic shows this is not EPR-specific), the broken "After the film" figure, and the sameness check as a later separate yes. Taken from V3: Sam's actual question asks for lessons sorted into "this kind of film" and "every film"; the learn step now writes that list. Added by the judge: the moving pass becomes part of rule 11 (merge, not a new rule), per CLAUDE.md's "merge overlapping checks".
## Faults in the pick
- F1 [fixed] V2's learn step looked at one film; widened to EPR, Blessed and Remakes so the threshold is not set by an unusual film.
- F2 [named] The blocking pass's cost per film (1.5-3%) is a guess; the first film it runs on measures it.
- F3 [named] Much of the length growth was Sam's own taste (R4, R2, G1, A2); a moving pass brings those notes earlier and cheaper but cannot promise fewer of them.
- F4 [fixed] V2 put the ledger tool change (counting notes) inside the "changes nothing" learn step; split out: the learn step fills counts by hand, the tool fix is its own later yes with the "After the film" bug.
- F5 [fixed] The learn step needs judgement on what kind each note is; Opus medium, not Sonnet.
- F6 [fixed] Sam asked for lessons, not only a change; the learn step's output is a lessons list sorted "this kind of film" / "every film".
- F7 [named] Lost unpushed work (Germany chat 6 to 6b) and the parallel chat lines are real lessons but small; listed, not built now.
- F8 [named] Stand-in figures for people not yet drawn may read differently from the finished crowd; density notes may still come later.
## Final version
**Step 1, learn (changes nothing; about 1.5% of a week; one Opus medium chat).**
- Sort every note from EPR, Blessed and Remakes into: length or camera, new direction, added scope, fault, repeat. Give each kind its share of the round costs (each fix's chat cost from the ledger).
- Write the lessons list Sam asked for, each with its source: which belong to new-technique, research-led films only (the 10.08% framing research; crowd technique), which hit every film (decisions seen only once moving; repeats; lost unpushed work; history re-reading, already treated by adopted proposals).
- Fill EPR's note and repeat counts in its notes by hand; name why the ledger's "After the film" reads 33.55% not 101.29%.
- Output: one table and the list, shown to Sam. It decides whether step 2 goes ahead.

**Step 2, one change, only if length-or-camera notes are at least 30% of after-animatic cost in at least 2 of the 3 films.**
- Rule 11 gains: after the still roughs and before the cast, a moving blocking pass: the whole film at its real length and real cameras, ready-made crowd figures and plain shapes for people not yet drawn, sent to Sam as a small clip.
- Enforced: the handover check refuses to open the cast stage without Sam's recorded Y on that clip.
- Cost: about 1.5-3% per film (unchecked; measured on the first film).
- Number to beat: share of cost after the first animatic under 35% (EPR 66%, Blessed 66%) on the next two films, with at most 2 length or camera notes after it. Reviewed when Sam declares each film complete; if missed, the rule line and gate come out.

**Later, each its own yes, only on step 1's evidence:** the ledger counts notes and repeats and its "After the film" is fixed; an automatic "they all look and move the same" check (9 such EPR notes by one helper's count); a guard against ending a chat with unpushed work.
## For Sam
### Option 1: Learn, then a moving rough before building
First, one chat sorts every note from this film and the last two by kind and by what it cost, and writes the lessons list you asked for. If notes about length and camera turn out to be the big cost, every film then gets a quick moving rough (whole length, real camera angles, simple stand-in figures) that you see and approve before any characters are built. On EPR the France and Albania cameras were changed only after you saw them moving, though they had passed the still sketches.
You would notice: one early grey clip per film; your "higher, longer" notes land there instead of after weeks of building.
Lost: about 1.5% of a week for the sorting chat; building waits for your Y on the rough.
Added: a lessons list; if approved, one early clip and one Y per film (about 1.5-3% each, a guess until measured).
### Option 2: Learn, then a timed pencil rough and a sameness check
The same sorting chat, then the existing pencil sketches are held to the beats at full length as a clip, and later an automatic check catches crowds where everyone looks and moves the same before you see them.
You would notice: pencil clips instead of still sheets; fewer "they're all the same" notes.
Lost: about 1.5% for the sorting chat; building waits for your Y on the pencil clip.
Added: a pencil clip per film (about 1-2%), and later a sameness check (about 2% once).
