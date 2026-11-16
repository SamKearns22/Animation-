# Proposal: Craft lessons from EPR to get crowds, sets, people, poses, framing, effects and cameras right in a first build

Status: adopted (2026-11-16)

## Problem
Sam (16 Nov), after the end-of-film lessons proposal for European Protests Ranked (EPR) was declined, because EPR was
built piece by piece without a fixed composition: "I would be interested in any lessons about building crowds, sets,
individuals, posing (such as the problematic shrug at the end), shot framing, effects and camera perspective. Anything
that would make those aspects easier for you or more effective in a first round build." Then: "I am interested in all of
the above, what would you propose to do." EPR cost 101.3% of a week against a first plan of 21.5%, most of it after the
first animatic, and its notes repeatedly returned to the same craft faults: sameness in crowds, set elements wrong
against the camera, poses that did not read at phone size, effects mis-scaled, cameras that passed still checks but
were changed on seeing them move. The decision is which craft lessons, if any, should become permanent rules, tools or
checks so that the first build of a crowd, set, person, pose, shot, effect or camera is right more often, for every
film, ordinary or unusual, and what to do first. Sam says some of this film may not be a good example to learn from
because he had no composition in mind; the evidence must be read with that in mind. Every film is new: no lesson may
mean less joke, worse films or reused content (reuse means means, never content).

## Facts
- The shrug (notes/protest-tiers.md, A11, A12, A30, A35): the first version failed twice. Recorded reason for A12:
  "side on, one palm hidden behind the launcher, a small shoulder lift: nothing read at phone size." A30's fix turned him
  three-quarter to camera, raised the shoulders, lifted the launcher clear; A35 held it longer and softened the head
  shake. Rule 38 in guides/film-quality-rules.md says front on by default and a three-quarter view only as a last
  resort, listed with its reason. Whether the A30 fix used that listing: unchecked.
- Crowd and people sameness notes, each a separate item: Albania A17 (hat colours: gold was 70 of 147 hats), A18 (police
  identical), France F5 (police all the same model), F19 and Germany O4 (rioters one face and skin tone; each city's mix),
  O5 and O7 (too many bald heads; hats added), notes/protest-tiers.md. An older note from Blessed also had bald heads
  (O5). Count of "all the same" type notes in the film: one helper's count was 9 (unchecked here).
- Sets and effects items in the notes: Albania bank window glow too big, RPG craters too big and star-like, surf near
  the left edge, bank Molotov fires large (Albania chat 3 "seen at a glance"); France car smoke columns and lone puffs
  read as rocks (back-half chat 7); Germany shop front, placard on the door, glass impacts over the shutter (G23). Set
  measurements re-done after camera changes (SET_BOXES t3, ALLEY_CAM F). All in notes/protest-tiers.md.
- Cameras and framing: research/crowds-and-big-action.md holds lessons F1-F12 (tall 9:16 frame stacks layers in bands of
  the safe area; eye level chosen first; one focus per beat with a squint test; one value and one change per crowd; light
  plan with backlight; watchers point the eye; lines lead in; emptiness is scale; chaos from diagonals in the action with
  a level still camera; focus near the centre at fast cuts; screen direction fixed per side; three bands for crowds). They
  were written as "proposals" 12 Nov and the film's notes say "write nothing until Sam's numbers" (rule 86); whether and
  which were written into the rulebook: unchecked here (rule 10 and rule 89 mention framing and critique; the helpers
  must check). Notes/framing-research.md. The France and Albania cameras passed the still framing research and pencil
  roughs and were reversed by Sam on seeing them moving (round 3-5 France and Albania notes, R4 tier lengths 4/6/8/10 s).
- Existing tools (read their headers before proposing anything like them): source/posegallery.py (poses drawn and tested
  once from every view; rules 41, 42; guides/pose-gallery.md); source/posecheck.py (every pose taken from the kit is
  checked as drawn); source/rough.py (rule 11: one rough sheet of every new person, place and move, drawn by the kits
  themselves); source/protest_tiers_roughs.py (the hand-made pencil roughs); source/camfeel.py (rule 72: fast or
  un-eased camera moves flagged); the people kit (guides/kit-catalogue.md line 44, "NOT for films until Sam approves it");
  rule 83 (no painted overlaps unless listed); rule 18 (joke props at least 40 px of 1920 at phone size); rule 89
  (critique before every send); rule 74 (acting list before the animatic).
- Cost context: EPR 61 chats, 101.29% of a week; round 2 about 47.6% against 0.865% planned; the ledger's own earlier
  Learn work (notes/proposals/learn/protest-tiers-costs.md) puts critique, rework, re-render and code-finding chats at
  about 30% of chats 0-32's cost. Per-chat cost has not fallen after the 13 Nov fixes (same file).
- Sam's earlier proposal on this film (a moving rough before building and a note-sorting chat) was declined on 16 Nov
  (notes/proposals/epr-lessons.md); its judge's finding that the France and Albania cameras passed stills and only
  failed on moving pictures is recorded there and is the record to use.
- Limits: chats 9-32 of EPR are unreadable from this account; the film's script was speculative and built piece by piece,
  so some faults would not recur on a film with a fixed composition (Sam's own caution).

## Record
research/crowds-and-big-action.md
notes/protest-tiers.md
notes/archive/protest-tiers-handovers.md
notes/archive/protest-tiers-plan-r0.md
notes/framing-research.md
notes/proposals/epr-lessons.md
notes/proposals/epr-lessons/judge
notes/proposals/learn/protest-tiers-costs.md
guides/film-quality-rules.md
guides/kit-catalogue.md
guides/pose-gallery.md
guides/job-packs.md
source/posegallery.py
source/posecheck.py
source/rough.py
source/camfeel.py
notes/ledger/protest-tiers.json
CLAUDE.md

## Verdict (the judge, word for word)
<!-- verdict-hash: b7ade03ab302f24c -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 2 fixed, 4 named.

## Leak
none. The decision line names "rules, tools or checks", which leans toward writing lessons down, but gives no remedy; all three versions saw this and two looked past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 3 | 3 | 3 | 4 | 16 |
| V2 | 4 | 4 | 3 | 4 | 5 | 20 |
| V3 | 4 | 5 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes, as amended: an expert puts the fix into the shared tools (the crowd maker, the pose check) where the evidence is already in, and measures before building the rest.
Q2: Sameness and the shrug rest on EPR plus Blessed's bald-head note and would recur on any film (Sam's caution applies to cameras and length, not to these); sets, framing and cameras wait for the three-film census because EPR alone cannot separate them from "no composition".
Q3: Root causes are in the record: the variety code lives only in the EPR cast file (checked), the copies check flags only exact twins (checked, kitchecks header), the shrug row was never looked at by eye (checked, pose gallery line 48), and EPR had no shot marks so the front-on check never ran (checked). Each fix is a pre-flight refusal, not reading; worked = sameness and pose notes counted on the next two films.
Q4: Rules-on-paper, defaults-in-the-kit, learn-first and a blind phone-size reader were all weighed; defaults plus refusals win because they do not rely on a chat choosing to read.
Q5: Each change is its own numbered yes and comes out alone; the census changes nothing. Weak point named: the census resembles the declined sorting chat (F2).
Q6: Sources named; the note counts (11 vs 16 by two readers), costs and share limit are unchecked.
Q7: Sized by 11+ sameness notes with 2 repeats and a twice-failed pose; the rules-only list (the cheap trap) is rejected.
Q8: Every change permanent or not made; reviewed when Sam declares the next film complete.
## Pick
V3
## Why
V3 is the only version that acts now where the evidence already exists (sameness, 11+ notes, two repeats, and a fault shared with Blessed) instead of making every change wait for a census, and it finds the real root cause: fixes went into one film's code, not the shared maker, so the next film starts with identical crowds again. V2 has the same checks but gates all of them behind a census that resembles the sorting chat Sam declined on 16 Nov. V1's "look plan" is a document a chat must read and follow, the failure both other versions document, and its facts are unsourced.
Taken from V2: the rule-38 finding (no front-on listing in any EPR file) and the effect real-size check in metres as a named candidate. Added by the judge: the crowd variety goes into the existing people kit's crowd lines rather than a new builder, and the pose change is made concrete from the record (the front-on check is skipped silently when a film has no shot marks).
## Faults in the pick
- F1 [fixed] V3's "kit crowd builder" duplicated the people kit's existing crowd lines (kit catalogue line 44, awaiting Sam's approval); the variety now goes there, so there is one way to make a crowd.
- F2 [named] The census is close to the note-sorting chat Sam declined on 16 Nov; it is now narrower (craft notes only), gates only the areas without evidence, and is offered as its own yes.
- F3 [fixed] V3 left poses to "after the census" though the shrug's cause is in the record; pose change now offered with evidence.
- F4 [named] Note counts are one reader's each (11 vs 16 sameness); cost estimates and the share limit are unchecked.
- F5 [named] Using the people kit for crowds needs Sam's approval of that kit for films; the variety change cannot go in without it.
- F6 [named] Cameras get nothing now: the record shows they failed only when moving, and the moving rough was declined; the census must say whether that changes.
## Final version
Three separate yeses, each a pre-flight refusal, each reviewed at the next film's completion. Order: 1 and 2 now, 3 after.
1. Crowds varied by default (evidence in: 11+ sameness notes, F15 and F16 repeats, Blessed's bald heads). Move EPR's city mix, outfits, hats, builds and faces into the people kit's crowd lines, so any crowd made from it is varied unless the plan says otherwise. Widen the copies check: refuse a group where one hat, hair, skin or colour passes a set share of heads (gold was 70 of 147), where skins miss the place's listed mix, or where neighbours move in step. Needs the people kit approved for films. About 1-2% once. Number to beat: at most 2 sameness notes, none repeated, on the next two crowd films.
2. Poses read at phone size (evidence in: the shrug failed twice; its gallery row was never looked at; EPR had no shot marks so the front-on check never ran). A film with people and no shot marks is refused instead of told; a gallery pose not yet looked at by eye is refused until its sheet is viewed at phone size in its shot's own angle, with any held prop. About 0.5-1% once. Number to beat: no pose note returned twice on the next two films.
3. Craft census (changes nothing, about 1-1.5%): craft notes only, EPR, Blessed and Remakes, each tagged by area, cause (tool default, missing check, taste, no composition), repeat and fix cost. Output: a ranked list for sets, effects, framing and cameras, each with notes it would have saved; the likely next yeses (effect sizes checked in metres against the nearest person; framing lessons F1, F2, F10 into rule 10 with a check) come from it, one at a time.
Lost: nothing in the films. Added: two refusals and one sorting chat.
## For Sam
### Option 1: Fix crowds and poses now, sort the rest first
Two changes now, each its own Y: every crowd comes out varied by default (skins, hats, clothes, builds set by the city, with an automatic check that refuses "all the same"), and every pose is checked at phone size in its own shot before you see it (the shrug was never looked at, and the front-on check never ran on this film). Then one chat sorts the craft notes of this film and the last two to rank what to fix for sets, effects, framing and cameras.
You would notice: no "they all look the same" notes; poses that read the first time.
Lost: about 1.5% of a week for the sorting chat; crowd variety needs your Y on the people kit first.
Added: two automatic refusals (about 2-3% once) and a ranked list for the other areas.
### Option 2: Sort first, then fix in order
One chat sorts every craft note from this film and the last two by area, cause and cost, and the fixes (crowd variety, pose check, effect sizes, framing) come one at a time in the order it finds.
You would notice: the same fixes, but a round later; nothing changes until the sorting is done.
Lost: about 1.5% for the sorting chat, and the next film may still get crowd and pose notes.
Added: a ranked list, then each fix on its own Y.
