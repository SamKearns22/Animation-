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
