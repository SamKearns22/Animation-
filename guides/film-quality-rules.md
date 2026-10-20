# Quality rules for every film (approved by Sam, 21 Oct, after Power Crime Action)

Why: Power Crime Action took 51 notes from Sam; about 30 were things a check could have caught (things passing through each
other, thin places, people popping in and out, script and mouth mistakes). The old rules failed because they were written as
symptoms ("hands don't go through signs"), the checks only tested what we had already been burnt by, each room and shot was
built separately, "detailed enough" had no measure, stills can't show movement, nobody compared the script with the
recordings, and fixes stayed in one film's file. These rules are written as causes, so they apply to any film.
Rules marked [tool] need a tool that does not exist yet (see "Build list" in `story/status.md`); until it exists, do the
check by hand and say so.

1. **Draw the world once, in a plan.** Before any shot, write one plan in metres per film: every place (square, room,
   corridor), where each door and opening joins them, where each camera stands, which way each person faces. Every shot
   reads from that plan. Keep it in the film's notes file.
2. **See-through gaps are drawn from the neighbouring space.** A doorway or window shows the real next room, its lighting,
   floor and colours (from the plan), never a flat colour. [tool: a "portal" in the sets code]
3. **Reference benchmark before building any place.** List the 8-10 things that make it recognisable (landmarks, ground,
   kerbs, traffic, sky, clutter, scale). Put our first picture beside Sam's reference on one sheet and tick each item; build
   whatever is missing before Sam sees it. No references yet: stop and ask. Never draw from memory (the lion had a hole).
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

## Saving tokens and cutting rounds
- **Fix the cause once, in the shared kit.** Label each of Sam's notes "new kind" or "seen before". A new kind is fixed in
  the kit and gets a test in the automatic checks. Never fix the same kind twice.
- Run rules 5-7 before showing Sam anything; Sam should not find what a computer can find.
- Clips before animatics (a full animatic only once the clips are clean).
- Fresh chat with a handover at every stage switch; one combined sheet per check; never look at an unchanged picture.
- Opus for the plan, the tests and anything new; Sonnet for filing, rendering and sending.
- Log Sam's notes by group in the film's notes file, so we can see which group costs most and which test to add.
