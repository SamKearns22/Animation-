# Where things stand (project, 7 Nov; the last film is finished)

- **Rules that bite next:** 78 (resting arms show weight, never sink), 79 (full-size looks before "looks right"), 74 (acting list: shot and why, meaning questions first, no limit).
- **Done (7 Nov):** the touch check prints COULD NOT TEST when it finds no hand or object (`audit.py`, `kitchecks.py`); rules 74, 78, 79 written; two tips in `guides/figure-rig.md` s.4; reference photo `references/body-weight/leaning-on-table-forearm-forward.jpg`. Hook Text rule dropped. All on the main line.
- **Next job A, sitting kit: part 1 BUILT 8 Nov** (`source/sitting.py`, notes `notes/sitting-kit.md`); sheet and moves video sent to Sam. Part 2 after his look: Opus, high effort, new chat. Type: "Build the sitting kit, part 2, from notes/sitting-kit.md".
- **Job B, rule 78 check: BUILT 8 Nov** (`kitchecks.rests`, run by pre-flight; films list resting arms in `RESTS`; tested on the sitting kit's desk and armchair poses and planted faults).
- **Needs Sam:** a look at the sitting kit's sheet and moves video.
- **Read:** `guides/figure-rig.md` s.2 body, s.3 limbs, s.4 contacts, s.6 movement; `guides/pose-gallery.md`; `source/kitchecks.py` (touches, resting); rule 78 and 32 and L1 in the rulebook.
- **Open rule requests:** none (rule 80 written 7 Nov). New rules from A or B are proposed to Sam first.
- **For Claude:** existing seat support is only `check_seated` (hips on the seat) and the desk-seated note in figure-rig s.4; no stand-up, feet-up or seat-change poses exist yet. Check `source/moves.py`, `posegallery.py`, `figure.py` before building.

## Efficiency rules: Sam's answers (9 Nov), to write in a fresh chat
Background: the 7-9 Nov weekend used about 90% of a week (Ad-Vanced Notice about 55%, Elder Scrolls Swindon about 27%, tools about 12%);
the cause was long chats re-read at every step. Rules 31, 44, 55, 85 and the "Fresh chat" rule are already written. Still to word
(show Sam the exact wording; write on his yes):
1. **Each film: 12% of a week at most; aim 8-12%** (two films last week came in at 8-12%). The plan's estimate warns Sam in
   advance of anything inescapably expensive, with its cost and a cheaper option. Each handover adds up the film's measured total
   (`costwatch.py --report` per chat, rule 44); the first line to Sam warns as soon as the total is on course to pass 12%.
2. **Rounds went wrong because fixes missed the request, or new ideas came.** Proposal to word: before fixing, each note is
   restated in one line with the plan (and a still where it's visual) and fixed only once understood; a fix that fails twice
   stops rendering and goes to a still sheet of 2-3 options. New ideas are welcome, but each one gets its cost said first.
3. **Tools get their own chats and their own estimates**, separate from any film's 12%; estimate first, build only on Sam's yes.
4. **Streamline and condense the rules and guides without losing film quality**: merge duplicates, drop dead rules, contents
   list at the top of each guide, handovers name sections to read. Its own chat (Opus high), estimate first (about 1-2%).
5. One check sheet per round; re-checks in words with no picture unless something visible changed.
6. Calibrate the cost watch (WEEK_USD in `.claude/hooks/costwatch.py`) the next time Sam gives his weekly % figure.
