# Quality rules for every film (rules 1-11 approved by Sam 21 Oct, after Power Crime Action; 12-31 on 25 Oct, after Prepper Minister)

Why: Power Crime Action took 51 notes from Sam; about 30 were things a check could have caught (things passing through each
other, thin places, people popping in and out, script and mouth mistakes). The old rules failed because they were written as
symptoms ("hands don't go through signs"), the checks only tested what we had already been burnt by, each room and shot was
built separately, "detailed enough" had no measure, stills can't show movement, nobody compared the script with the
recordings, and fixes stayed in one film's file. These rules are written as causes, so they apply to any film.
Rules marked [tool] need a tool that does not exist yet (see "Build list" in `story/status.md`); until it exists, do the
check by hand and say so. (25 Oct: every [tool] in rules 1-31 is built; the tools are named in each rule.)

1. **Draw the world once, in a plan.** Before any shot, write one plan in metres per film: every place (square, room,
   corridor), where each door and opening joins them, where each camera stands, which way each person faces. Every shot
   reads from that plan. Keep it in the film's notes file. [tool: the film's `PLAN`, checked by `source/plan.py`
   (pre-flight); `python3 source/plan.py FILM sketch OUT.jpg` draws it]
2. **See-through gaps are drawn from the neighbouring space.** A doorway or window shows the real next room, its lighting,
   floor and colours (from the plan), never a flat colour. [tool: `sets.house` draws it, the real next room clipped
   to each opening; `sets.portal_faults` (pre-flight) fails an opening showing one flat colour]
3. **Reference benchmark before building any place.** List the 8-10 things that make it recognisable (landmarks, ground,
   kerbs, traffic, sky, clutter, scale). Put our first picture beside Sam's reference on one sheet and tick each item; build
   whatever is missing before Sam sees it. No references yet: stop and ask. Never draw from memory (the lion had a hole).
   [tool: the film's `BENCHMARK`; `python3 source/benchmark.py FILM OUT.jpg` makes the sheet; pre-flight fails a blank
   item, a missing reference or fewer than 8 items]
4. **Every set has layers and life.** Foreground, middle, background; a textured ground; something moving or lived-in.
   A flat empty area fails.
5. **One automatic collision test.** Every person and prop gets a simple solid shape; test every frame, including the area
   swept by anything that moves (doors, arms, ropes, thrown things, a tipping hem). Anything overlapping that is not on the
   film's "allowed contacts" list is flagged. This replaces symptom rules. [tool: `source/audit.py`, built 21 Oct: the
   film's `scene(t)` and `ALLOWED_CONTACTS`; see `guides/satire.md`]
6. **One automatic pop-in test.** Compare each frame with the next: anyone or anything that appears, vanishes or changes
   drawing away from the frame edge is flagged. Keep a list of who is in each shot. [tool: `source/audit.py`, built
   21 Oct: also flags a jump (a step far longer than the frames either side); `ALLOWED_POPS`; it prints the list]
7. **Script and mouth audit before any picture.** For every recording compare syllable count and length with the script
   text and the subtitles; flag mismatches (the missing "terrorist" sentence). Check the mouth opens once per syllable and
   shuts in silence unless the brief says otherwise. [tool: `python3 source/voices.py --film FILM`, built 21 Oct: the
   film's `mouths_seen(t)` and `ALLOWED_MOUTHS`; see `guides/satire.md`]
8. **Rehearse the risky moves as clips in the planning stage.** Pick the 3-4 hardest moments (a throw, a door, a lunge, a
   crowd running in) and render each as a 2-3 second clip before building the rest of the film.
9. **Every group has a plan for every phase.** For crowds, police, any group: write what each person does while arriving,
   stopped and leaving (no pacing after the action stops; no formation walking). Put it in the plan.
10. **Plan the framing up front, hook text included.** Mark the empty area of each shot for the Hook Text; list the key
    beats and give each its own minimum hold time (about 0.3 s per readable stage) and camera distance; no diagonal cameras
    unless the models hold up.
11. **Show one rough composition sheet before building:** the 3-4 key shots, so Sam approves layout and joke first.
    (`sets.house` with the plain painter draws any plan's rooms and things as blocks for it; pre-flight refuses to run
    until the notes say "Composition sheet sent: DATE, FILE", rule 14)

## Rules 12-31 (approved by Sam, 25 Oct, after Prepper Minister)
Why: Prepper Minister took 64 notes and 25% of a week; about 45 notes were mechanical. Several broke rules we already
had, because a check was copied per film (and wasn't), only looked at what the film handed it, or didn't exist.
**Lesson: a rule only holds if a check enforces it.** Every rule is listed in `guides/rule-register.md` with its check.

**Checks**
12. **Checks run on everything by default.** Every person, prop, wall, door frame and piece of furniture in the set is
    a solid in the collision audit, given automatically by the set builder; a film lists only what to leave out, each
    with a reason, never what to include. (Prepper: the audit never saw a wall, note 47.) [tool: `sets.solids`, added
    to every frame by `audit.py` from the film's `PLAN`; `SET_EXCLUDE = [(name, why)]`; door leaves at `door_angles(t)`]
13. **Every check lives in the shared kit and pre-flight runs it on every film;** never copy a check from a film file.
    Move in: contact and hands-seen and resting-hand clearance (Poker Mon), head-and-body facing, marks on real
    surfaces, one sound per hit in frame (Prepper). (The bean tin, note 60: Poker Mon's contact check never copied.)
    [tool: `source/kitchecks.py`: `TOUCHES`, `FREE_MOVES`, resting hands (inside the audit), facing (pre-flight's
    drawing pass), `all_marks()`, `SOUND_SOURCES`]
14. **Pre-flight refuses to run** while the brief checklist has a blank "done?" row, or before the composition sheet
    (rule 11) has been sent. [tool: `preflight.gates`; and a shot missing anyone in `SHOT_CAST` fails]
15. **Effect shapes are checked:** each effect is listed with its shape; a star, a regular spike or a motion line
    fails (the off-style list, `guides/satire.md`). (Prepper's star flashes, note 20.) [tool: `viewchecks.shape_faults`
    on the film's `EFFECTS`]
16. **Direction holds across a cut:** anything moving keeps its screen direction and its side of a person across a
    cut unless the plan says it swaps. (The plasma through Wes's head, note 57.) [tool: `viewchecks.direction_faults`
    on `movers(t)`; `DIRECTION_SWAPS`]
17. **Every figure in front of an effect hides it** (robots and creatures too, not only people). (Note 13.) [tool:
    `viewchecks.hide_faults` on `effect_points(t)` and `EFFECT_SWITCH`]
18. **Readability sheet:** every prop a joke depends on, at phone size, with its height on screen; under about 40 px
    (of 1920) it is made bigger or brought nearer before Sam sees it. (Crossbow, Alexa, coaster, sparks: notes 2, 27,
    41, 46.) [tool: `viewchecks.readability_faults` on `JOKE_PROPS`; the sheet: `python3 source/viewchecks.py FILM
    SHEET.jpg`]
19. **Checks print a short summary** (counts and the first few faults); the full list goes to a file. [tool:
    `source/report.py`; pre-flight writes `OUT_DIR/NAME-preflight.txt`, the audit `review/FILM-audit.txt`]

**Building**
20. **Held things aim in 3D with the holder's body**, never at a fixed screen angle; a prop that draws its own fists
    still counts as held. The prop test turns each person through every view and fails a prop drawn across their
    back. (Machete, minigun, crossbow: notes 11, 12, 16, 45, 48.) [tool: `viewchecks.turn_faults`, on pre-flight's
    drawing pass]
21. **A limb pointing at the lens is drawn foreshortened** (wider as it nears us, the sole or palm facing us), drawn
    over the body. (Wes's kick, note 42; the reach, note 39.)
22. **My set dressing is shown on the cast or composition sheet,** kept clear of every spot where action happens, and
    is in the collision audit. (The lemons sat where the Alexa explodes, note 19.)
23. **A film file over about 1,000 lines is split, one file per group of shots,** so a note opens only its shots.

**Planning**
24. **Ambition estimate:** the plan lists the new builds and the risky moves and says roughly what share of a week
    the film will cost; Sam can trim before building starts. (Prepper: 12 shots, a 3D house, a robot, five weapons,
    a full effects set, a 360-degree loop.)
25. **Eyelines and holds per shot:** for each shot, where each person looks and how long each key beat holds; the
    checks compare the film with it. (Notes 21, 30, 35, 59, 61, 62.)
26. **Every sound effect is listed at planning** (what, which moment, when it's needed), asked for in one message;
    placeholders are named in every send.
27. **A bleep: ask whether the word was said or a gap was left,** at recording; then place the bleep from the sound
    itself (where the words and gaps are), never from the script. (Notes 33 and 54.)
28. **Reuse first:** check `guides/kit-catalogue.md`; every new set, person, prop or effect built for a film is added
    to it when the film's building stage ends (`source/catalogue.py`'s list too: `python3 source/catalogue.py OUT.jpg`
    draws the lot on one sheet).

**Notes and review**
29. **Every review copy (clip, animatic) shows the film time and the shot number in a corner,** so Sam's times point
    straight at the frame. [tool: `film_engine.render` stamps every `--small` or `--span` render]
30. **The notes table stays short:** one line of what was done per note, no "Was:" text (git keeps the history). Label
    each note "new kind" or "seen before"; a "seen before" note means a check is missing: add it.
31. **Clips, renders, filing and sending stay on Sonnet;** Opus only for planning, new builds and deciding fixes.

## Rules 32-37 (approved by Sam, 26 Oct, after Netan-Yahoo!)
32. **Pieces, rubble and parts of things settle properly.** Anything that falls and lies on the ground (cut-off pieces,
    debris, broken parts) settles on its broadest side (lowest centre of weight), never overlaps or rests on another
    piece, and casts a shadow only where it touches the floor. Any saved ("cached") drawing records which camera it was
    drawn for, so it can never be reused in a shot with another camera. (Netan-Yahoo! notes 4, 6, 11.)
33. **Test anything that falls or piles up on a short close clip before the animatic** (`final OUT --small --span T0 T1`
    on the landing): look for floating, overlap, balancing on a point, the wrong camera's drawing. Clips need no yes.
34. **Mirror test:** before showing a cast sheet, put each tile next to its source drawing and check nothing is squeezed
    or flipped; before an animatic, check every shot (wide shots too) for a mirrored face, lettering or prop, and that
    every glance goes the way the plan says. (Netan-Yahoo! notes 2 and the wide-shot glance.)
35. **Lock the layout in the planning pass:** ask in the first questions who sits or stands where, the gap between
    chair and desk and what must be in frame; run the plan file's true-gap check before building; a layout change after
    building is named as a cost.
36. **Say at planning when a tool is slow here** (3D pieces without numba, 5 s a body) and ask Sam once to allow
    pypi.org (claude.ai Settings, Capabilities).
37. **Files kept off GitHub (sounds, big references)** are listed in the first line of the handover with "ask Sam to
    re-attach them", so the next chat asks at once.

## Rules 38-39 (approved by Sam, 27 Oct, Patriots 3)
Why: weekly usage was climbing film by film, mostly from new 3D builds; and our people look best facing the camera.
38. **Front on by default.** Our people look best facing the camera: stage every shot so each person faces the lens
    (within about 25 degrees). A three-quarter (or side or back) view only where the shot demands it (seen from behind,
    walking across the frame, a wide where they face someone else), each listed with its reason. [tool: `plan.py`
    (pre-flight) from the plan's `SHOT_MARKS` {shot: [marks]}; the film's `THREE_QUARTER_OK = [(shot, mark, why)]`]
39. **Build in 3D only when it is needed; 2D everywhere else.** A set, prop or effect is built in 3D only when the film
    needs it: the camera moves round it or through it, it is seen from three or more angles and things in it must stay
    put between them, or someone turns it in their hands. Everything else is 2D: one flat painted picture per camera,
    in layers (back, middle, front), drawn to the plan's measurements. The plan in metres (rule 1) stays for every
    film. 3D pieces already built are reused as they are. The ambition estimate (rule 24) lists each 3D build with its
    reason, so Sam can say no before it is built.

## Saving tokens and cutting rounds
- **Fix the cause once, in the shared kit.** Label each of Sam's notes "new kind" or "seen before". A new kind is fixed in
  the kit and gets a test in the automatic checks. Never fix the same kind twice.
- Run rules 5-7 before showing Sam anything; Sam should not find what a computer can find.
- Clips before animatics (a full animatic only once the clips are clean).
- Fresh chat with a handover at every stage switch; one combined sheet per check; never look at an unchanged picture.
- Opus for the plan, the tests and anything new; Sonnet for filing, rendering and sending.
- Log Sam's notes by group in the film's notes file, so we can see which group costs most and which test to add.
