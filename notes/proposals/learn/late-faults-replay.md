# Late faults: replay (read-only; Sonnet, 16 Nov)

What I did: ran today's quick pre-flight (`preflight.py protest_tiers OUT --text`) on the film code as each Protest
Tiers building chat left it (branches claude/protest-tiers-c13, c15, c16, c17, c21 to c26), today's tools on every
run, today's notes. Nothing changed outside notes/proposals/learn/. Counts are the check's own lines (a line can
stand for several, "[4 like it]"); that is how the 44 and 107 were counted at the time.

## Table: faults the check lists on the code as the chat left it
| chat (what it built) | faults | pass-through | teleport | front/back swap | resting hand | effect shape | undeclared list / shot cast / other | run time |
|---|---|---|---|---|---|---|---|---|
| c13 (moves built) | 58 | 30 | 0 (could not test) | 8 | 4 | 0 | 16 | 6 s |
| c15 (hunt 1 fixes) | 50 | 21 | 0 (could not test) | 10 | 3 | 0 | 16 | 4 s |
| c16 (hunt 2 fixes) | 42 | 21 | 0 (could not test) | 10 | 3 | 0 | 8 | 4 s |
| c17 (lists declared) | 70 | 5 | 56 | 0 | 0 | 2 | 7 | 36 s |
| c21 (round 1 plan, build start) | 13 | 2 | 0 | 0 | 0 | 2 | 9 | 58 s |
| c22 | 13 | same as c21 | | | | | | 58 s |
| c23 | 13 | same as c21 | | | | | | 63 s |
| c24 | 13 | same as c21 | | | | | | 79 s |
| c25 (T4 Albania gags, melee) | 73 | 19 | 31 | 7 | 0 | 4 | 12 | 83 s |
| c26 (Germany/France extra seconds) | 107 | 19 | 62 | 10 | 0 | 4 | 12 | 87 s |

## Against the real gates
- Gate 1 (first full pre-flight after the moves, chats 16/17: 44 faults): the check on c16's code lists 42 (c13's:
  58, then the fix chats took it down). So 42 of 44 (95%) were already listed on the code as the building chat left it.
- Gate 2 (chat 28, first quick check of round 1: 107 faults): on c26's code the check lists 107, the same number. All
  107 were visible at the end of the last building chat. By who made them: 13 already listed from c21 on, 60 first
  listed at c25's end, 34 first listed at c26's end. Each chat's own faults were visible at its own end.
- Together 149 of 151 (about 99%) visible at build end. The proposal's bar for change 1 was 60%: passed.
- Not in the replay: eye-only faults (phone-size reading, chain 1) have no machine check; named in the verdict (F4).

## Hidden behind COULD NOT TEST
- Yes, one check hid a lot: clipcheck (teleports, drawing order) printed "COULD NOT TEST: no solids(t)" on c13, c15
  and c16, then on c17 (lists declared) found 56 teleports + 5 pass-throughs. 56 of the 70 on c17 were hidden until
  the list existed. The 107 at gate 2 held 62 teleports; those were not hidden (the lists existed by then).
- The touch check said COULD NOT TEST on c21 to c25 (the T4 melee people not yet in the scene): checked nothing, hid
  nothing found later. So change 3 (lists from day one) is supported by the clipcheck case only.

## Shared-tool faults that reached the film
- Effect-shape "stars": 2 on c17, 4 on c26 (4 of the 107, 4%): the check's own mask (chat 29 found it).
- Not replayable because today's tools already carry the fixes: the film-name mismatch (protest-tiers vs protest_tiers,
  which stopped pre-flight reading the critique and the quick check running until chat 28) and the head_view crash
  that cost chat 18. Counted from the handovers, not rerun: 2 more shared-tool faults, 3 chats touched (17, 18, 28).
- kittests on today's main line: `people_from_a_description` FAILS ("films using the kit before Sam approves it:
  protest_tiers_cast.py"; a policy line, not a drawing fault); the full run did not finish in 280 s (the other kit
  tests I saw passed). So kittests is slow (over 4.5 minutes) and not clean: a handover step that runs it every
  time would be too slow; run it only when a shared tool changed (change 2) and keep it to the tests that tool touches.

## Limits (honest)
- Today's tools on old code: the check is stricter or looser than it was then; the match on counts (42 vs 44, 107 vs
  107) says it is close, not item by item.
- Blessed's last build chats: not replayed (kept to ~1%; its code would need finding branch by branch). Protest
  Tiers alone has two gates that agree.
- c18 to c20, c27 to c31 were fix, critique and render chats, not builds: not replayed.
- Run times are on this machine, one run each.

## Answer for change 1
At least 60% visible at build end: yes (about 99%). Run time at a handover: 4 to 90 s for the quick check. Gate-only
fix chats it would have removed: the four on this film (17, 18, 29, 30; 8.0% of a week), if every fault is fixed
before the building chat hands over; chat 18 (the crash) was a tool fault and falls under change 2.
