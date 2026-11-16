## Built (chat 8, 16 Nov, Sam's 1)
- Learn: `notes/proposals/learn/replay-show.py` frozen (shot + time from the notes table; loose 26 / strict 14 targets fixed;
  note 18 scored on the nearest like shot 'cot'); kittests `code_finder_replay` (bar 23/26, 12/14, under 45 lines).
- Change 1 in `source/page.py`: `show --shot --at` (shot names from the film's SHOTS list, cached in story/FILM-shots.json,
  and `shot ==`/`in` lines); the shot's count kept apart from the words; an unknown shot falls to the shot at --at or the
  nearest name, said in a `note:` line; the shot's own lines shown before a def's head; every answer under 45 lines (best
  def 16, runners-up 5, at most 3 FILE:LINE); bookkeeping words (Sam, Nov, note, chat, animatic...) ignored; each call
  logged to notes/logs/FILM-show.log; `handover.py end` flags a film-code change with no show call; `start` prints --shot/--at.
- Replay, 26 Blessed notes: before 18/26 loose, 7/14 strict (52-60 lines). After: **23/26 (88%) loose, 12/14 (86%) strict,
  41-44 lines**. Without the shot (words only, same split): 21/26, 10/14; so the shot adds 2 each.
- Still missed: 2 (chin_long in a TUNE table), 9 (ears_hidden, one line in a long def), 24 (flash). Change 2 (tables and
  long-def lines) targets 2 and 9; not built: it is its own yes, asked only after it is shown working on the replay.
- Still to do: the held-out set from the next film's first round, frozen before any tuning (targets: lines edited, from git).

## Built (change 2, chat "code finder change 2", Opus medium, 16 Nov; Sam said proceed; ADOPTED 16 Nov, Sam: "Switch it on")
- Why the two notes missed (rule 30, looked first): note 2's chin_long sits in a module-level `P4.TUNE['brand'] = dict(...)`
  line, never on the page; note 9's ears_hidden is in `press_person` (blessed_cast.py:663-671), a SHORT def whose
  docstring has none of the note's words, so it was never a candidate; its one line ("hair over the ears: none drawn on
  top of it") holds four. The plan's "long def" guess was wrong: the cause was the candidate pool, not the cut.
- In `source/page.py`, behind `show.deep` (off; `FINDER_DEEP=1` turns it on): module-level assignments are units like
  defs; every def and table whose best single line holds 2+ of the note's words joins the hits (+2 per word on that
  line); a note with a more-or-less word (SIZE: big, long, wide, dark...) lifts tables whose keys name its thing
  (+3 each); the best line and its neighbours are shown before the head. Off: answers identical to change 1.
- Also on now (speed only, answers unchanged, made without asking; listed for the end-of-film review): each file is
  parsed once and kept until it changes; the 26-note replay ran 52 s, now 0.5 s.
- Replay (`notes/proposals/code-finder/change2-replay.py`): before 23/26 loose, 12/14 strict; **after 25/26, 14/14**,
  41-44 lines; words only 21/26, 10/14 -> 23/26, 12/14. kittest code_finder_replay passes either way.
- Named: note 2's answer shows six chin settings (Brand's is third, labelled `P4.TUNE['brand']`); SIZE is a hand list
  tuned on one note; still missed 24 (flash). Proof on a new film is the held-out set at the next film's first round.
- Sam's 16 Nov question (separate job or part of the rule-location one?): answered by his "proceed" as its own job.

## Weak spots (Sam, 16 Nov: "Switch it on. And can you address the weak spots?")
- Switched on: show.deep defaults on (FINDER_DEEP=0 turns it off); kittest code_finder_replay bar 25/26, 14/14, <45 lines.
- Hand list of more-or-less words: dropped (show.gate False). Without it the replay is the same 25/26, 14/14 and the top
  answer is the same on all 26 notes; on 11 notes another settings table appears among the runner-ups.
- Brand's chin line third of seven: `--who` added (the notes table's who column; a def or table named for them +2 per
  word). With it: second (first is Walliams's `outline`, whose docstring says "big face ... long, broad, rounded chin");
  scores unchanged. handover.py start and the FINDER fault now print --who. change2-replay.py prints all three runs.
- Note 24 (flash): not a finder miss. The flash code (`_stills`, blessed.py:476, "note 24" in its docstring) was written
  by that fix; the answer shows press_sp/press_pose/press, where the clothes and cameras went. Tried folding -ing/-ed
  endings: no change on the replay, not kept.
- The next film's test: cannot be run before there is a next film. Protest Tiers has no round notes with fixes in git
  (its round 1 was a re-staging), so no held-out set exists yet; it is frozen at the next film's first round as planned.
