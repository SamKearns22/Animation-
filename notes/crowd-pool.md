# Crowd pool (shared people kit; Sam, 26 Nov)

Sam: "Please ensure that the builders in OpenWinds are using the crowd pack. Open up the crowd pack to all of the
combinations that we've used before across all cities. So if we have generic people in any of our films, you can just
make them from a generic pooled crowd pack."
Also Sam, 26 Nov: the bald heads "definitely" came before the crowd packs (the old default head); never use it again.

## Brief checklist
- [x] Open Wounds' builders (crowd 'worker', story/brexit-is-done-people.txt) drawn from the crowd pack in the film: one
      still from the film's own picture at a worker, full size (hard hat, hair, face, hi-vis); no old default head
      (check people.head_faults, kittest crowd_head_installed). Chat 27 is changing Open Wounds' code: touch only its
      people file, and only if needed, and tell chat 27 (session_01U3pKR29EmmteJgw6u577Ng).
- [x] A generic pooled crowd pack: every combination used before across all cities and films (story/*-people.txt
      crowd lines and people.py's mixes: haircuts, hair colours, skins, face pushes, builds, tops, hats, glasses,
      stubble), one pool any film's generic people come from (e.g. `mix: pool`), still varied by place where a film
      names one, the sameness check still on; kit catalogue entry updated; its own kit test.
- [x] One labelled sheet of about 12 pooled people for Sam (full size, house look), sent in the chat.

Locked by Sam: every posted film's crowds as drawn; Open Wounds' shots, cameras and movements.

## What was found and built (chat 1, 26 Nov)
- Open Wounds' builders: all five workers are the crowd pack (hard hats, haircuts, faces, hi-vis); film stills at 9 s and
  13 s looked at full size; head_faults clean for every worker. The lying worker's bare head is the film's staging (his
  hat flies off at the hit). Nothing changed in Open Wounds' people file or code; chat 27 told.
- The pool: `people.py` POOL_* and pool_varied(); default for every new film's crowds; `mix: pool PLACE` opts an old
  one in; `people.pooled(i, place)` for test scenes. Posted films and Open Wounds stay as drawn (BEFORE_POOL).
- Seen on the first sheets and fixed: too many grey heads (4 of 12; greys now about 1 in 10); a turned ponytail drawn
  over the cheek (now hangs from the head's back edge, new films only: `pony_edge`, people_turned.py); hats too few to
  pass the sameness check in small crowds (share now over the whole crowd; colours one step round per member).
- Kit limits named, not built (learn first): Milburn's big curls are big from the front only (left out of the pool);
  the turned short sleeve keeps a square corner on the far shoulder (as GTA's walkers; short sleeves only in warm places).
- Checks run (why): kittest crowd_pool (new; caught 9 missing tops, 2 greys and a hat clash before passing),
  crowds_varied, crowd_heads_hung, crowd_head_installed, people_from_a_description and kit_people_never_generic
  (shared people code changed): all pass. Blessed's pixel-for-pixel redraw unchanged.

## Sam's words from pose-test chat 1 (carried by the handover check; settled there)
- "this is just taking far too long ... a practice clip ... half an hour" / "diagnose why so much time" / "this middle
  ground is hopeless": settled in pose-test chat 1 (practice clips: no body check or kit tests; checks advised).
- "No, I don't think we need to run it through the proposal step" / "It doesn't have to be perfect": the proposal
  route is now on request only; checks advised (CLAUDE.md, 26 Nov).
- "the bald head ... our art style has advanced ... no longer fit for purpose": this job (never the old default head;
  the pool; kittest crowd_head_installed).
- "How long until Kemi, Tony and May are updated in the new style?" / "why are you rendering them again? we've already
  seen them and I said they were fine": no re-render; Open Wounds chat 27 carries them as Sam passed them.

## Kit test rule: where a film starts and ends (Sam, 26 Nov, this chat)
Sam: "The beginning of the film is when I give you the screenplay and title. The end of the film is when I ask for any
lessons on the film that need to be learned." Done: kitfilm.py begin FILM / lessons FILM; a job with no screenplay
(this one) never starts the run; a final no longer waits for kit tests; CLAUDE.md, rulebook row 90 and the Plan pack
say so; kittest kit_tests_per_film covers it (saved example: this job's first chat started all 81 tests). This job's
wrong start row removed. Lost: the kit tests before a final (they now run at the lessons instead).
Reds from the stopped background run, not this job's (named, not fixed): seated_r7_look and womens_builds (May seated:
knees and bottom; rule S12 shows BROKEN) are Open Wounds chat 27's seated work, told; places_from_a_description
(Blessed's room paintings about 1% off) predates this chat (places kit untouched here).

## Where things stand (crowd pool chat 1, 26 Nov, session_01U3pKQz4KnhPvQAepNUUdMg)
Rules that bite next: people in tests are the crowd pack or grey; reuse before building; 90 (kit tests: screenplay and title to lessons).
Done: Open Wounds' builders checked (crowd pack, clean); the pooled crowd pack built, tested and the default for new films; sheet of 12 sent; kit test start and end defined. HALTED by Sam ("good enough, not priority").
Next: none (halted). Any notes on the sheet: Opus medium.
Needs Sam: nothing.
Read: guides/kit-catalogue.md row 45 (the pool sentence); source/people.py "the pooled crowd pack".
Open rule requests: none.
For Claude: people.POOL_*, pool_varied, pooled, BEFORE_POOL; people_turned pony_edge; kitfilm begin/lessons/begun; kittests crowd_pool, kit_tests_per_film.


## Branches named at the start (not merged here)
- claude/open-wounds-chat27: Open Wounds chat 27's own live work; it merges its own.
- claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: Grand Theft
  Autism (posted) leftovers, logs and one draft each; not this job's work.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 2% of 15%; forecast not yet planned (2026-11-26)
