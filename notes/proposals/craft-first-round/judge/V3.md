# Helper B: craft lessons for a right first build

## Leak
None as a remedy. The facts lean towards "rules, tools or checks", which I treat as one option among several.

## Results
- **Sameness is the largest repeated craft fault.** I count 11 separate "all the same" notes: A17, A18, A22, F5, F15, F16, F19, G16, O4, O5, O7. Two of them came back a second time: F15 repeats O4 and F16 repeats F9 (notes/protest-tiers.md). Blessed had the bald-head fault too (O5).
- **Every variety fix was made inside this one film's code.** The variety pieces (CITY_MIX, marcher(), street_clothes()) exist only in source/protest_tiers_cast.py. The kit has no crowd builder (guides/kit-catalogue.md), and no rule mentions variety or sameness (searched guides/film-quality-rules.md). The next film starts with identical crowds again.
- **The shrug was already in the pose gallery but had never been looked at.** Its row says "tested by the check only; not yet looked at by eye", all 6 views (guides/pose-gallery.md line 48). The first build was side on, with a palm hidden behind the launcher. It failed twice (A12, A30). It also broke rule 38's front-on default, and nothing caught that.
- **The framing lessons F1-F12 were never written into the rulebook.** Rule 10 has no sentence about bands, eye level or focus. There is no squint check and no "twins" check (two copies of one figure moving in step) in rule 6 (guides/film-quality-rules.md; research/crowds-and-big-action.md, "only on Sam's numbers").
- **Cameras:** the France and Albania cameras passed the still framing check and the pencil roughs, then were reversed by Sam once he saw them move (notes/proposals/epr-lessons.md, judge). A moving rough was declined on 16 Nov.
- **Cost:** critique, rework and re-render chats came to about 30% of the cost of chats 0-32. The moves stage cost 25.3% against a 7.6% plan, spent as rounds fixing the same faults again (notes/proposals/learn/protest-tiers-costs.md). The film notes carry 10 rule-30 repeat lines (a note Sam had already given once).
- **Gap:** no record gives a cost for each craft area, or says which craft notes came from having no fixed composition. The ledger is kept per chat, not per note.

## The real decision
The decision is not "which lessons to write down". It is which faults the **film's first build** keeps making by default, and how to stop that for every film. The bigger levers than written lessons:
1. What the tools produce when nobody asks for anything else (their defaults).
2. Whether kit pieces that were never looked at at phone size are trusted.
3. Whether a fix goes into the generator, the shared code that makes every crowd, or only into the one instance Sam noticed.

## Root cause
- **Fixes go to the instance, not the generator.** O4 varied the acted rioters but not the crowd figures, so F15 came back. F9 changed only the timing of the throws, so F16 came back.
- **Checks test geometry, not how things read.** The current checks catch pops, overlaps, speed, and whether a pose is drawn, but not "does it read at phone size, in its shot". That is how the unviewed gallery shrug got in.
- **The research was never turned into rules or checks**, so it relies on a chat choosing to read it.
- The missing composition (Sam's caution) explains the length and camera reversals better than it explains sameness or the shrug. Those two would recur on any film.

## Approaches weighed
1. **A lessons rulebook:** write F1-F12 and the new lessons as rules. It is cheap, but it relies on chats reading and choosing to follow it (fails Q3).
2. **Reframe to defaults:** move craft into the kit, so the first build is varied, front-on and scaled by default, with a check that counts sameness.
3. **Learn first, a craft-note census:** sort every craft note from EPR, Blessed and Remakes by area, cause, repeat and fix cost, then rank which change would have prevented the most.
4. **A blind phone-size read before Sam:** a fresh helper judges each new pose, effect and crowd only inside its shot, at phone size. This overlaps with rule 89, and a moving version was declined.

I pick 3 then 2, one change at a time. Approach 1 alone does not change what gets built. Approach 4 waits for the census.

## Proposal
**Learn (changes nothing): the craft census.** About 1-1.5% of a week (unchecked estimate), done once.
- Covers every craft note in EPR, Blessed and Remakes. Each note is tagged with its area (crowd, set, person, pose, framing, effect, camera) and its cause (tool default, missing check, taste, or no composition). It also records whether it was a repeat, its fix cost from the ledger, and which existing check should have caught it.
- Output: a ranked list of changes, each with the notes and % of a week it would have saved. This also gives the per-area cost the record lacks.

**Change 1: variety by default.** This can go first because its evidence is already in: 11 notes, 2 repeats.
- Move the city mix, outfits, hats, builds and face sets out of the protest film's code into a kit crowd builder. Every group it makes is varied unless the plan says otherwise.
- Add a sameness count to the existing audit. It flags any single look, colour or hat on more than a set share of a group (gold hats were 70 of 147, 48%), and two copies moving in step side by side (this takes in F12).
- Enforced by the audit before every animatic.
- Number to beat: sameness notes on the next crowd film fall from 11 to 0 or 1.
- Cost: about 1-2% of a week once (unchecked), about 0% per film.

**Changes 2+**, each its own yes after the census. Likely candidates: gallery rows not looked at at phone size are refused (the shrug); effect sizes set from the set's metres; and the F1/F2/F10 sentence added to rule 10 with a check. Each change comes with its own count to beat from the census.

**Total:** about 2.5-3.5% once, against 15% per film. What Sam would notice: no crowd sameness notes, and one ranked list of lessons that each carry a number.

## Sam test
- Q1 (Expert): Yes. An expert fixes defaults and generators, then measures before adding rules.
- Q2 (Best result): Three films, not EPR alone, so the lessons are not set by one film built without a fixed composition.
- Q3 (Comprehensive): Change 1 is in the tool and the audit, not on paper. It is measured by its note count. Root cause shown: fixes went to the instance.
- Q4 (Most intelligent): Four different approaches weighed. Defaults beat rules because they do not depend on a chat reading something.
- Q5 (Risk): The census changes nothing. Change 1 can be undone alone. The other changes wait for evidence.
- Q6 (Checked): Sources are named. Costs and thresholds are marked unchecked.
- Q7 (Not the cheap version): Sized by 11 notes and 2 repeats, not by price. A rules-only list is the cheap trap, and it is rejected.
- Q8 (Nothing temporary): The kit builder and the check are permanent, and are reviewed when Sam declares the film complete.

## Lost / Added
- Lost: nothing. Plan-time crowd variety becomes the default rather than a per-note fix.
- Added: one census (about 1-1.5%), one kit crowd builder and a sameness check (about 1-2%), and later changes only on their own yes.

## Unchecked
- The cost estimates.
- The share threshold for the sameness check.
- Whether Blessed and Remakes have readable craft notes.
- Whether A30's three-quarter turn was listed under rule 38.
- The 11-note count is my own reading of the notes.
