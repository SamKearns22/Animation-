# Proposal: Checks that are always red or always "named" are noise, so real faults hide among them

Status: adopted (2026-11-22)

## Problem
Before every animatic, pre-flight (the checks run before an animatic) printed 48 lines on Milburn that chats "named"
(listed to Sam as known) instead of fixing, growing to 61; two kit tests (the automatic tests of the shared tools)
stayed failing for the whole film, and two "before Sam approves" tests were stale. A line that is always there is
never read: the real clipping fault (could-not-test) sat among them. Milburn review section 1 items 6 and 7, lesson 2.
Sam (19 Nov): no check is deleted; each old line is fixed, or dropped only under the three-films rule (CLAUDE.md: a
step is removed only if it caught nothing in three films, with Sam's Y on a "Lost:" line).

Merged in (22 Nov, same cause: false lines in the checks): On Milburn, chat 18 removed 60 false lines from pre-flight (the checks run before every animatic) by making the film's
own code hand the checks the cleaned voice takes. The fix lives in that film's code only, so the next film starts with
the same 60 false lines. False lines bury real faults: Milburn's real clipping fault sat among 48 to 61 named lines.
Milburn review lesson 4 and section 1 item 5; Sam put it third in the queue (19 Nov).

## Facts
- notes/archive/milburn.md line 20 (chat 15): 48 quick-check lines, "the same 48 as chat 13 (plan gaps, SHOT CAST
  'never on screen' for want of scene(t), house-style lists missing, two fast captions, the 'fucker' bleep waiting on
  Sam's recording, clipcheck COULD NOT TEST), none new; named to Sam ... not settled (each needs a build)".
- notes/archive/milburn.md line 13 (chat 18): 60 lines left named after 60 false ones were removed: the old 48, 12 more
  "too fast to read" captions, 2 syllable counts.
- Picture checks: 28-31 faults each animatic (HANDS 14-17, LAP 14), "file identical to animatic 1's: not new"
  (milburn.md lines 13, 16, 20).
- Kit tests round_page and facehouse_whole_head failing before and through the film
  (notes/archive/milburn-handovers.md lines 23, 33); `handover.py start` on 19 Nov still prints both as BROKEN, plus
  "cost_faults has no promise in the watcher".
- Chat 11 asked Sam to approve fixing the stale tests; the guard stopped the ask (notes/proposals/unrouted.md,
  2026-11-18 06:11); nothing was fixed.
- CLAUDE.md "Rules are permanent": remove a step only if it caught nothing in three films, with Sam's Y on a Lost line.

- notes/archive/milburn.md line 13 (chat 18): "milburn.py now hands the checks the cleaned takes (`_voice`,
  `_stretches`, `n` per line), which removed 60 false script/mouth lines; 60 lines left named".
- notes/proposals/milburn-review.md section 1 item 5: "Improved the film, not the tool ... only for this film".
- The shared checks: source/preflight.py (unchecked name; search), source/kitchecks.py, source/audit.py.
- The film template new films start from: source/satire_template.py (rule 75 names it).
- How many other check fixes went into film code instead of shared tools across Blessed and Milburn: unchecked.

## Record
notes/archive/milburn.md
notes/archive/milburn-handovers.md
notes/proposals/milburn-review.md
notes/proposals/unrouted.md
source/kittests.py
source/kitchecks.py
source/watcher.py
source/handover.py
CLAUDE.md
source/milburn.py
source/satire_template.py
source/audit.py
source/
guides/kit-catalogue.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 0a0a40d07b42a025 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 5 found, 3 fixed, 2 named.

## Leak
yes: the merged part says the voice fix "lives in that film's code only, so the next film starts with the same 60 false lines", which points straight at "move it into the shared tools". It anchors one remedy (V3's second half copies it), but it does not hint at the bigger lever (how naming works), so the leak is mild.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 5 | 5 | 4 | 4 | 4 | 22 |
| V3 | 3 | 3 | 3 | 2 | 4 | 15 |
## Sam test
Q1: Yes. An expert on alarms that people stop reading would do this: a check that "could not test" counts as a failure, not a pass, and every alarm that is waved through has a written owner and reason. That is what the pick does. Waving the whole list through with one switch is the textbook way alarms stop being read.
Q2: The learning step covers Milburn, Blessed and the film now being made (Grand Theft Autism), plus the shared tools. It also matches each Sam note to a line the checks had already printed. Two films each had a repeat note from a printed line (Milburn's name cards twice, Blessed's newsreader mouth, note 45 marked REPEAT). Checked. The evidence is wide enough to decide.
Q3: The rule is enforced by the render refusing to go on, not by a chat reading and choosing. Two ways to meet it on paper are named and blocked: blanket reasons (each reason must say where it looked, and a decided line comes back if its numbers change) and hiding old lines (rejected). The root cause comes with evidence (preflight.py line 457 against line 488; the one switch at line 593). Each change has a replay test and a number to beat.
Q4: Four approaches were weighed: per-line records, cleaning the inputs at the source, a cap, and showing only new lines. Showing only new lines was rejected because it would have hidden the name card for good. The cap (V3) was dropped because it can be met by marking lines decided.
Q5: Each change gets its own yes and can be undone by itself. What can go wrong: more refusals early in a film. That is the point, and it is named. Nothing is asked of Sam on trust: the learning step and the Milburn replay show it works before the next film relies on it.
Q6: Facts checked: milburn.md lines 13, 18 and 20; the ledger's 62 lines; preflight.py lines 457, 488 and 593; Blessed note 45; broken.md (facehouse_whole_head fixed 19 Nov, round_page still open). Still unchecked: the cost figures, and how much of Milburn's 22% went on naming.
Q7: It is sized by the result: no animatic lets a blind check through, 0 false voice lines, and 0 Sam notes that were already printed lines. It is not sized to a cap on paper. Honest cost: about 7 to 9% of a week, once, outside any film.
Q8: Every change is permanent, with a kit test (an automatic test of the shared tools), and is reviewed when Sam calls the next film complete. The learning step is a measurement, not a trial.
## Pick
V2
## Why
V2 finds the deepest cause: a single switch, `--faults-named`, waves the whole list through. Because no line is remembered on its own, every chat names all of them again. V2 also found the "could not test" mismatch the card fault went through. V1 found the same mismatch and has better evidence: the ledger's 62 lines sorted into four kinds (about 45 of them are the checks being blind, not faults), and the Blessed repeat note, which shows this is a habit across films and not only Milburn's. V2 alone noticed that the problem file's kit-test fact is out of date (broken.md: facehouse_whole_head fixed 19 Nov). V3 starts from a cap and "show only new lines". A cap can be met by marking lines decided. Its new-lines-only view is the move that hid the name card. It also has no learning step and lumps its changes into one go.
Taken from V1: the four kinds of line (blind, false, chosen, real), used for sorting and in the refusal. The Blessed evidence. The rule that a kit test red at two handovers in a row stops the handover (Change 4). The rule that a decided line returns if its numbers change.
Taken from V3: a red kit test blocks the handover, and every film-code check fix gets a "move to shared" line that the end-of-film review lists.
## Faults in the pick
- F1 [fixed] V2 says "nothing imports" milburn_voice. In fact milburn.py and milburn_forest.py import it; what is true is that no other film or the template uses it. Corrected in the final version.
- F2 [fixed] V2 had no step for the red kit tests. Change 4 is added from V1, with round_page as the only one known to be red (from broken.md).
- F3 [fixed] V2's "older than one animatic stops the render" would refuse lines Sam chose on purpose (his fast speech). Final version: a written decision with where it looked counts as settled, and the line comes back if its numbers change.
- F4 [named] Cost figures (7 to 9% of a week) are estimates and not checked against past tool chats.
- F5 [named] Four changes, each with its own yes. Sam still has to decide four times, and changes 2 and 3 wait on what the learning step finds.
## Final version
**Learn (changes nothing, about 1.5% of a week, Sonnet).** Sort every pre-flight line of Milburn (ledger checks.jsonl), Blessed and Grand Theft Autism into four kinds: blind (the check could not see the film), false, chosen (real but chosen on purpose), real. Match every Sam note to any line printed earlier: Milburn's cards twice, and Blessed's note 45 so far. Count the check fixes made in film code (from the code history). Find out which kit tests really fail: round_page, per broken.md. The results decide what changes 2 and 3 cover.
**Change 1: "could not test" always stops the animatic (about 1%).** One shared rule in pre-flight: clipcheck's "COULD NOT TEST" (line 488) is treated like every other one (line 457), and it names what the film must hand the check. Must beat: replaying Milburn at animatic 1 refuses on clipcheck, and replaying Blessed catches the shut mouth (if the learning step shows that was a blind check).
**Change 2: one record per named line, in place of the one switch (about 2.5%).** Each line left gets a written entry in the existing exceptions table (waivers.py): kind, reason, where looked, owner. The render refuses any line without an entry. A recorded line comes back if its numbers change. Pre-flight prints the count of recorded lines and every unrecorded line in full. Must beat: under 10 unrecorded lines before every animatic of the next film, and 0 Sam notes that were already a printed line.
**Change 3: shared inputs (about 2% per cause).** The template and kit hand every check what it needs: cleaned voice takes (built from Milburn's take cleaning as a means), scene(t) for the cast check, and the house-style lists. The voice check says so when it reads a raw file the film does not play. Any check fix made in film code gets a "move to shared" line that handover.py end flags. Must beat: replaying Milburn gives 0 false voice lines (60 today), and the next film's first pre-flight has 0 blind lines.
**Change 4: kit tests (about 1%).** round_page is repaired, not deleted. A kit test red at two handovers in a row stops the handover.
No check is deleted (Sam, 19 Nov). Each change is permanent and reviewed at the next film's end. What Sam notices: shorter Checks lines, no "seen before" notes from faults already printed, and questions about one old fault at a time instead of a pile.
## For Sam
### Option 1: Every warning gets an answer, and "couldn't look" stops the line
At the moment one switch lets the whole warning list through, so the same 48 to 61 warnings were waved past every time. Your name card fault sat among them twice. First, a short study of the last three films sorts every warning into kinds and finds each of your notes the checks had already flagged. Then, as separate yeses: a check that couldn't look at the film stops the animatic; each warning left needs its own written answer or it stops the render; the shared tools hand every check what it needs, so new films don't start with 60 false warnings; and broken tests get fixed. You'd notice short Checks lines and no repeat notes from faults we'd already seen.
Lost: the one switch that waves the whole list through.
Added: about 7 to 9% of a week of tool work, once; more early stops while a film is being built.
### Option 2: Sort the old warnings and cap the list
One sitting now sorts Milburn's warnings by cause. Each cause is fixed in the tools or dropped under the three-films rule. From the next film, an animatic is refused while more than 10 warnings are named, and only new warnings are shown in full. Cheaper and quicker, but a warning can be "named" just to get under the cap. Showing only new warnings is how the name card hid.
Lost: old warnings shown in full.
Added: a cap of 10 named warnings per animatic.
