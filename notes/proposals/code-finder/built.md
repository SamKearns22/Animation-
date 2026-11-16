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
