## Leak
Mild: no remedy is stated, but the facts are chosen around the load map, pointing at "cut the kit's links to film files".

## Results
- Fault that reached Sam: Grand Theft Autism's cast sheet broke the body rules (sleeves, shoulders, taper, Lucia's box body). The sleeve is Midterminal's Epstein-only patch (midterminal_cast.py 454-475, checked), switched on for every "sleeves short" person (people.py 496-498, checked). (notes/grand-theft-autism.md, Diagnosis.)
- The coupling runs both ways. A Grand Theft Autism kit addition made the finished film Milburn stop drawing identically (kittest focus_front_heads; same notes, line 164). Earlier: Protest Tiers' early load broke a kittest (notes/next-jobs.md 29). catalogue.py's header: each entry draws in its own process because "films patch the shared drawing code differently".
- Scale (reach.py re-run, matches): 52 of 117 kit files load a film file; each main kit reaches 40 old film files; 15 drawing steps are swapped at run time (problem file, unchecked).
- Cost: the cast chat spent 3.99% (notes/ledger/grand-theft-autism.md); the patch's share is unchecked. Film forecast: 60-63% against 15%.
- Gap: no record of which commit each finished film was rendered from (0 tags), so nobody knows yet if a finished film re-renders from its past version.

## The real decision
Not "delete old files" but: where is the boundary between one live kit and finished films, for every film and chat? The bigger lever is how finished films stay re-renderable: frozen in their own past version, not kept live inside the kit.

## Root cause
Films extend the kit by overwriting kit functions when they load (midterminal_cast wraps views.arm), and later kit files load those film files to get the result. Nothing ever moves a film's addition into the kit through the rule checks, and nothing freezes a finished film, so old films must stay live to re-render, which keeps their patches live too. Deleting files fails: the kit loads 40 of them. The catalogue's one-process-per-entry workaround hid the symptom.

## Approaches weighed
1. Archive or delete finished films' files (Sam's wording). Breaks the kit and every recut; rejected.
2. Reframe at quality: run the body-rule checks on cast sheets and stop "house style" waivers. Patches and load-order effects stay; a separate proposal.
3. Freeze, then one kit: each finished film re-renders from its own saved version; then the kit loads no film file, each borrowed step rebuilt to the rules or dropped, enforced by a check. Chosen.
4. Learn-first only: measure which borrowed steps meet the rules, and whether old films re-render from their past versions. Kept as step 1.
5. Numbered kit versions per film: heavier than 3, same result.

## Proposal
**Learn (no yes needed; Sonnet; about 1.5%).** For each of 41 finished films find its final's commit; re-render one frame from it in a separate copy; compare with the posted video. For each of the 15 swapped steps, one labelled sheet: rule-meeting or one film's patch.
**Change 1 (own yes, about 1.5%).** Freeze: a list of each finished film and its commit; one recut command that draws it from that saved copy. Beat: 41 of 41 match (exceptions named). Enforced: posting a film adds its line, checked at handover.
**Change 2 (own yes, after change 1 passes; Opus, about 8%).** One kit: the 52 kit-to-film loads removed, each borrowed step rebuilt in the kit to the rules or dropped, one at a time; kit tests check rule sheets, and Blessed's replay moves to its frozen copy. Beat: kit-to-film loads 0 (from 52); swapped steps 0 (from 15); old films reached 0 (from 40). Enforced: the load-map scripts become a kittest and handover check refusing any kit-to-film load or run-time overwrite.
**Change 3 (own yes, about 1%).** The catalogue lists only kit parts; finished films appear once each, as "frozen, recut only". Beat: kit entries naming a film file 0 (from 67).
Total about 12% of a week, once, as tool work, not a film's 15%. Sam would notice: cast sheets built only from current parts; recuts still work.

## Sam test
Q1: yes; freezing released versions apart from the live library is standard. Q2: scope is every film and kit file, not one cast sheet. Q3: root cause named; enforced by a check, not by reading. Q4: five approaches weighed. Q5: freeze proven before anything is removed; each change undone alone. Q6: sources named; gaps marked. Q7: sized to remove all coupling, not one sleeve. Q8: permanent; reviewed at the next film's end.

## Lost / Added
Lost: kit steps that exist only as one film's patch (each rebuilt or named first). Added: a frozen copy per finished film, a recut command, a kit boundary check.

## Unchecked
The 15 swaps; the cost share; whether past commits re-render (shallow copy); size estimates.
