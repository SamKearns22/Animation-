# Helper A: named lines

## Leak
Mild: the merged part says the fix "lives in that film's code only, so the next film starts with the same 60 false lines", which points at "move it to the shared tool" (the review's lesson 4). Ignored as an answer.

## Results
- Milburn's last saved pre-flight (notes/ledger/milburn/checks.jsonl, 20 Nov) holds 62 lines, by check: SHOT CAST 21, plan 15, captions 14, house style 4, script/mouth 2, and one each for camera feel, effect shapes, readability, clipcheck "COULD NOT TEST", collisions "did not run". Checked.
- Sorted by what they mean: **30 say the check could not see the film** (SHOT CAST wants scene(t); the five single lines; house style "has no audits"); **15 are plan gaps** (no camera in the plan, rooms overlapping); **14 are real but chosen** (Sam speaks fast); **2 wait on Sam's ears**. So about 45 of 62 are blindness, not faults. Checked (the line texts).
- Cost in faults: the name card clipped and reached Sam **twice** (chats 13 and 18) because clipcheck could not test and its line was carried as "old" (milburn.md line 13). Blessed had the same failure: "newsreader mouth shut 50.8-51.7 s" was named, not fixed, and came back as Sam's note 45, marked REPEAT (blessed-handovers.md line 161; blessed-notes-animatics-1-2.md line 47). **Two films, three Sam notes** from faults that were already printed.
- Inconsistency in pre-flight itself: a "COULD NOT TEST" coming from a warning stops the animatic (preflight.py line 457), but clipcheck's own "COULD NOT TEST" is added as an ordinary line (line 488). Same words, opposite treatment. Checked.
- The 60 false voice lines: the template already hands the checks the recording (satire_template.py lines 124-129), but only the raw file; when a film plays trimmed, joined, levelled takes (milburn_voice.py), the shared voice check falls back to the raw file without saying so (voices.py `prepared`). Checked.
- Kit tests round_page and facehouse_whole_head red through the whole film (milburn-handovers.md lines 23, 33). Their cost: unchecked.
- Gap: no record anywhere of which named lines each chat read, so the reading cost per chat cannot be measured.

## The real decision
Not "fewer lines", but: **must a check that cannot see a film be allowed to pass as a line?** The unit is the whole film from its first build chat: blindness is cheap to cure while the film is being built and costly at the animatic. Bigger lever than cleaning up lines: the film's code not handing the shared checks what they need.

## Root cause
Pre-flight mixes four kinds of line in one list with one treatment ("name it"): blind, false, chosen, real. Nothing records which kind a line is or whether it is new, so the list grows every chat, every line "needs a build", a Sonnet routine chat cannot build, and naming is the only move left. The first try (naming in the Checks line, `--faults-named`) failed because naming is permission to go on, not a decision.

## Approaches weighed
1. **Triage and cap:** label each line fix or retire; under 10 before an animatic. Easy to meet on paper by blanket labels.
2. **Show only new lines** against the last run. Would have hidden the name card for good: rejected.
3. **Reframe, blindness stops:** a check that cannot read its input stops pre-flight in the build chat, naming the one thing the film must hand it; the template and kit hand all of them, voice takes included.
4. **Learn first:** sort every pre-flight line of the last three films into the four kinds and match each Sam note to an earlier printed line.
Chosen: 4, then 3, then one decision per remaining line.

## Proposal
**Learn (changes nothing, about 1% of a week, Sonnet):** sort Milburn's, Blessed's and Remakes' saved lines (checks.jsonl, preflight records) into blind / false / chosen / real, and list every Sam note that was already a printed line. Result decides which changes go ahead.
**Change 1 (about 1.5%):** any shared check that cannot read its input stops pre-flight, naming what is missing (one shared rule, fixing the line-457/488 mismatch). Enforced in pre-flight code, not by reading. Must beat: replayed on Milburn's code it stops on all 30 blind lines and on the name card; replayed on Blessed it catches the shut mouth.
**Change 2 (about 2.5%, after 1):** the template and a shared voice-takes kit piece (built from Milburn's take cleaning as a means) hand every check its input, and the voice check says so when it is reading a raw file the film does not play. Must beat: the next film's first pre-flight has 0 blind lines and 0 false voice lines.
**Change 3 (about 1%, after 2):** each line left gets one written decision, using the existing exceptions table (reason, where looked); pre-flight prints only undecided lines, and a decided line returns if its numbers change. Must beat: under 10 undecided lines before every animatic, and 0 Sam notes that were already a printed line.
**Change 4 (about 1%):** the two red kit tests are repaired, not deleted; a kit test red at two handovers in a row stops the handover. Must beat: 0 red tests at the next film's start.
One-off total about 7% of a week, outside any one film; each film should save Sam's repeat notes and a long list read in every chat. What Sam notices: shorter Checks lines, fewer "seen before" notes.

## Sam test
Q1 Expert: input contracts and "unknown is not pass" are standard practice. Q2 Best result: three films' records, not one. Q3 Comprehensive: enforced in pre-flight code; the root (mixed kinds) is named; each change has a number. Q4: four different approaches weighed. Q5 Risk: each change separate and removable; Change 1 may stop a film until its hooks exist (that is the point). Q6: sources named; gaps marked. Q7: sized to stop the repeats, not a cap on paper. Q8: permanent changes, reviewed at film end.

## Lost / Added
Lost: nothing a check catches; no check deleted (Sam, 19 Nov). Added: build chats must hand the checks their inputs (some minutes per film); one written decision per chosen line.

## Unchecked
Cost figures; Remakes' lines; the kit tests' cause; whether Blessed's shut mouth was blindness or a real fault named.
