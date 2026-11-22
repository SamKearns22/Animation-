## Leak
The problem file gives away a remedy ("capped the moods there", Sam's Y to "the brow limit enforced by the kit"). Ignored: the answer below starts from the record.

## Results
- One fault reached Sam: Milburn note 1 (18 Nov), Andy's angry brows in scene 7 tipped into steep slashes through his glasses. Cause found by chat 13: rage 0.16, gape 0.22 (notes/archive/milburn.md line 10). Fixed by setting both to 0.14 by hand in the film's own mood table (source/milburn.py lines 169-175).
- Cost: chat 13 was 2.25% of a week for this note plus four others (notes/ledger/milburn.md line 38). The brow note's own share is unchecked.
- "Rule 56" does not exist. It was merged into rule 89 on 10 Nov (guides/film-quality-rules.md line 126). So chat 13 wrote its limit against a rule that is gone. Nothing in the code or the rulebook holds 0.14.
- The 3/4-parts rule is already enforced. A kit test exists (source/kittests.py `turned_parts_kept`), and so does a pre-flight refusal for every film (source/preflight.py line 206, `lost_parts`). Only the rulebook line naming them is missing. The problem file is wrong to say it "lives only in Milburn's notes".
- The brow pull is not one number across the kit. In the shared face code (source/faces.py `brow_uv`, used by facehouse, people_parts and people_famous) it is a fixed drop of the brow's inner end. The turned head copies the same formula (source/turnhead.py `brows`), and so does source/patriots4_cast.py. Other films use other scales (traitors.py frown 1.0-1.4; press_secretary.py in degrees). How steep 0.14 looks therefore depends on each head's eye width and brow slope, and on whether it wears glasses. On other heads it is unchecked.
- Brow faults are a class, not a one-off: "eyebrows too high on all characters" (grand-theft-autism-notes.md line 51); "brows really far from her eyes" (facetool-handovers.md line 140); "eyebrows look weird as they change" (ad-vanced-notice.md line 178). One steep-brow note so far.
- Gap: nobody has measured what angle the drawn brow makes on each head at each mood. Without that, the limit can't be set honestly.

## The real decision
The decision is not "write 0.14 down somewhere". It is how a face fault Sam finds once gets caught on every head, every view and every film, before he sees it. The lever is measuring the drawn brow, not capping a typed number. A second, bigger lever: why the critique before the animatic let the steep brows through.

## Root cause
1. The fault lives in the drawing: how steep the brow is against the eye and the glasses. But the only guard was a typed input, and it was set in one film's own file. Rule 13 says checks live in the kit.
2. The same input draws a different angle on every head (fixed drop, different eye widths), so a fixed cap is a stand-in and would pass or block the wrong faces.
3. No check measures a drawn face at its strongest moods. Critique (rule 89) looked at people as a whole, so an extreme mood was first seen full size by Sam.

## Approaches weighed
1. **A number cap in the kit** (refuse a brow pull over 0.14). Cheap. It misses moods drawn by other brow code, it is wrong on heads with other eye widths, and it may block a strong look that works.
2. **Measure the drawn brow (reframe).** The shared brow code reports the angle it actually drew and whether it crosses the glasses or the eye. Pre-flight refuses any frame past the limit, on every head and view.
3. **A mood sheet:** every mood a film uses, on every head that uses it, at full size, looked at before the animatic. It catches all face faults, but it depends on a chat looking.
4. **Learn first:** replay every mood on every head on record and measure the angles. The number comes from the faults and the approved looks, not from one head.

Chosen: 4, then 2. The 3/4-parts part needs only its rulebook line.

## Proposal
**Learn (changes nothing, about 0.5% of a week, Sonnet):** draw every mood in every mood table on record on every head that used it, front and turned. Record each brow's drawn inner angle, and whether it crosses the glasses or the eye. Mark which are known-bad (Milburn rage 0.16, gape 0.22) and which Sam approved (Milburn furious in scene 4, the angry Blessed jurors, the flying-whales animals). Result: one angle that separates the bad faces from the approved ones, or the finding that no single angle does.

**Change 1, its own yes (about 1.5%, Opus medium, one chat):**
- The shared brow code (faces.py, turnhead.py) measures the angle it draws.
- Pre-flight refuses any frame where a brow is past the measured angle, or crosses the glasses or eye, unless the film writes down a reason.
- Written once in the rulebook with its kit test.
- The kit test must flag Milburn at 0.16 and 0.22, and pass 0.14 and every approved look.
- Number to beat: zero steep-brow notes from Sam on the next three films. Also, the replay flags the old note on its own.

**Change 2, its own yes (about 0.1%):** the rulebook gains the 3/4-parts line, naming the test and pre-flight refusal that already exist.

Sam would notice: nothing on screen, and no repeat of the slash-brow note.

## Sam test
- Q1 Expert: measures the drawn result on every head, not a typed proxy; yes.
- Q2 Best result: the evidence is every mood on record, all heads, not one film.
- Q3 Comprehensive: a refusal, not something to read; it is proven against the old note and the approved looks.
- Q4 Intelligent: four different approaches weighed; the measured one fits rule 13.
- Q5 Risk: each change undoes alone. Nothing is trusted until the replay shows it catches the note.
- Q6 Checked: sources named; the rest marked unchecked.
- Q7 Not cheap: the number cap is the cheap trap and is rejected. Total about 2.1%.
- Q8 Nothing temporary: permanent kit check, reviewed against the next film.

## Lost / Added
Lost: brows steeper than the measured limit, unless a film gives a reason. Added: one kit measure and pre-flight line, and two rulebook lines.

## Unchecked
The brow note's share of chat 13's cost. Whether 0.14 looks right on other heads. Whether the glasses sit where the brow meets them on all heads. Whether one angle separates the bad faces from the approved ones (that is the learning step's job).
