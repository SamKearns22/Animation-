# Helper A: women drawn on a man's body

## Leak
Mild: the facts lean toward kit parts (`build woman`, a shoe, a suit cut). Weighed as one approach only.

## Results
- **Repeat across films.** GTA, 20 Nov: "Lucia on a man's box body". The critic named it twice; it was closed as "house style" until Sam pushed (notes/archive/grand-theft-autism-notes.md 122-139). Brexit, 23 Nov: the same fault on May and Kemi (notes/sam-notes/brexit-cast-v2/notes.md).
- **The fix reached one person.** Only Lucia has `build woman`. These women don't: GTA's "her", Milburn's goth and waif, Protest Tiers' wife, May, Kemi (story/*-people.txt). Crowd women (45%) get the man's body (people.py 268-271).
- **No check.** "woman" has 0 hits in the rulebook. The hips and hems rule S6 was retired 11 Nov (rulebook line 130).
- **The ledger missed the repeat.** It counts repeats only within a film. Brexit's "1 repeated" is Blair (notes/ledger/brexit-is-done.md).
- Cost: Brexit's cast chat 1.85%, film 4.32% so far (ledger). GTA's rebuild cost: unchecked.

## The real decision
The kit's default person is a man, so every woman in every film is drawn as one unless a chat opts in. No check reads a body the way a viewer does.

## Root cause
1. The build is opt-in. A named person has no field saying she is a woman. A crowd member's `woman` flag never reaches the body.
2. The GTA fix went into one cast line, against "every fix is for all films".
3. No check reads a body as a viewer would, so the critic could close it as style.
4. There is one man's suit cut (lapels) and one house shoe. Whether the woman's build still reads as a man in them is unchecked.

## Approaches weighed
1. **Patch the cast lines** (May, Kemi). Already failed once.
2. **Reframe:** every person carries `woman` or `man`, which sets the build and defaults. Pre-flight refuses a cast line without it.
3. **Learn first:** draw the woman's build in every view, seated, and in each outfit at phone size. Compare with generic figure templates, not photos of real women.
4. **A viewer's check:** a blind judge (a fresh model that hasn't seen the cast lines) says man or woman for each person on the sheet at phone size. A mismatch is a fault.

Chosen: 3, then 2, then 4, then clothes only where 3 shows the need.

## Proposal
**Learn (changes nothing; about 1.5%).** Draw May and Kemi on the woman's build at five turns, seated and standing, in their outfits, at phone size. List what still reads as a man, and list every woman in the cast files.

**Change 1 (its own yes; about 2%).** Every person carries `woman` or `man`, enforced by pre-flight and a kittest. `woman` turns on the build; crowds pass their flag through. Finished films stay as drawn. To beat: women on the man's body in live cast files, now 7 named plus all crowd women, down to 0.

**Change 2 (its own yes; about 1.5%, then about 0.2% a film).** The viewer's check runs in pre-flight on every cast sheet. It is trusted only once it flags both saved n5 pictures. To beat: 2 of 2 caught, and 0 notes from Sam on women's bodies over the next three films.

**Change 3 (its own yes; about 2-3%; only what the learn step lists).** Women's clothes in every view: for example a jacket without a man's lapels, and a court shoe or flat. To beat: 0 mismatches from the check across the reference cast.

Total about 7% once, for all films. Carried by Brexit, that is about 11% of 15% before animating, so change 3 may wait for the next film. Sam would see a cast sheet v3 where May and Kemi read plainly as women in every view.

## Sam test
- Q1: Yes. It fixes the default and adds a check, not a patch.
- Q2: Evidence covers every cast file and two films.
- Q3: Pre-flight enforces it; measured by the check and the next three films.
- Q4: Four different approaches were weighed.
- Q5: Each change is undoable alone. The check isn't trusted until it catches the saved notes.
- Q6: Sources are named; the gaps are listed below.
- Q7: It skips the cheap patch, which already failed.
- Q8: Permanent, and reviewed at the film's end.

## Lost / Added
- Lost: a cast line must say who the person is.
- Added: the field, the check (about 0.2% a film), and women's clothes if needed.

## Unchecked
- How Lucia looked to Sam.
- The GTA cost.
- Which Blessed jurors are women.
- Whether seated suits carry the build.
- Whether a blind judge can read a body's sex reliably at phone size.
