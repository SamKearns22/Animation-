# Helper B: one route to the current kit

## Leak
None from the writing chat. Sam's "isolate or delete" is weighed below as one option.

## Results
- The kit is partly made of old films. people_parts.py loads ad_vanced_notice_cast, midterminal_cast and ed (source/people_parts.py 15-17). 110 files load ed.py; about 123 load burnham.py (problem file: 124).
- Checked by running: after gta_cast loads, views.arm comes from ad_vanced_notice_cast, views.person from midterminal_cast, views.leg from patriots3_cast. Epstein's sleeve is in midterminal_cast.py 454-498, and people.py 496-498 switches it on. The other 12 swaps are unchecked.
- Harm runs both ways. Old into new: GTA's cast sheet got the one-person sleeve. New into old: GTA's additions made Milburn's 5 s frame stop matching (notes/grand-theft-autism.md 75-86, 164-167).
- The GTA diagnosis gives a bigger root cause: the critic named the faults twice and they were closed as "house style". The inherited sleeve was one contributor of five, and body checks never run on cast sheets (same lines).
- Cost: GTA spent 12.72% of a week over 7 chats, is paused, and is forecast at 63.3% (notes/ledger/grand-theft-autism.md). The sleeve's share of that is unmeasured.
- Gap: only these two cross-film breaks are on record. How often this happened in earlier films is unknown.

## The real decision
The real question is what sets the kit's drawing today, not where old kits are kept. Today it is set by whichever film files loaded, and in what order. The kit's only proof is "redraws Blessed exactly", never "meets the body rules". Bigger levers: cut the live kit loose from old films while keeping recuts possible, and prove the kit against the rulebook.

## Root cause
1. Films swap shared drawing steps for their own when they load (patching). Loading an old film is the cheapest reuse, and nothing refuses it.
2. Finished films re-render from the same live code, so their patches can never leave the kit.
3. The kit's tests check "same as before", never "meets the rules".

## Approaches weighed
A. Delete or hide old films. This breaks recuts, and 52 kit files load film files.
B. Reframe by version: pin each finished film to the saved project version it was finished on (git keeps every version). A recut runs from that version, so the live kit is free to change.
C. Import wall: kit files may not load film files and no file may swap another's step. Shared basics move into the kit, and a load-map check enforces it.
D. Judge by the rules: a kit-drawn reference cast, with the body checks run on every cast sheet.
E. Learn first: measure what each swap changes, and whether old films re-render from their version.
Chosen: E, then B, C, D, each its own yes. B makes C safe, and D proves C.

## Proposal
- **Learn (changes nothing, about 1%, Sonnet):** find each film's version (the save that added its MP4). Re-render Blessed, Milburn and the oldest film from their versions and compare frames. Draw GTA's cast with each swap removed, on one labelled sheet.
- **Change 1, pin by version (about 1.5%):** a film-to-version list and a recut command. Number to beat: 3 of 3 frame-identical. The Blessed test reads the pinned version.
- **Change 2, import wall (about 4-6%, Opus high):** move the basics into the kit. Each swap the sheet shows matters is rebuilt to rule 41 or left in its film. A load-map check in pre-flight and kittests enforces it. Numbers to beat: 52 kit files loading films down to 0, and 15 swaps on a new person down to 0.
- **Change 3, reference cast (about 1.5%):** a man, a woman, short sleeves and a jacket; hand, seam and body checks on every cast sheet. Number to beat: zero body faults reaching Sam on the next cast sheet.
- Total about 8-10% of a week, filed as tool work. It is reviewed at the next film's end against its notes and cost. The "house style" closure is a separate proposal.

## Sam test
Q1: separates what old films need (pinned versions) from the kit now (rule-tested).
Q2: covers the whole kit and all 41 films; the frequency gap is named.
Q3: enforced by checks, not by a chat choosing to read.
Q4: five approaches weighed.
Q5: each change is undone alone; versions are proven before anything moves.
Q6: sources named; rest under Unchecked.
Q7: removes the cause (52 to 0), not just a label.
Q8: permanent; reviewed at film end.

## Lost / Added
Lost: recuts use their old version, so later kit fixes need carrying across. Added: one kit, the same whatever loads first, proven against the rules.

## Unchecked
12 of the 15 swaps; whether old films re-render now; all costs; the count of 41 films; earlier films' frequency.
