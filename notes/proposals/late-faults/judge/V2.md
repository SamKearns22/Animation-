# The chat's own version (chat 3 of 8, written before the helpers ran)

**Check as you build: the gate's checks run on every step, in the chat that wrote it.**

1. One command ends every build step: `final OUT --small --span T0 T1` on the shots the step touched runs, besides
   the picture checks it already runs, clipcheck and audit on that span (the teleport / pass-through / order-swap
   checks pre-flight runs; ~5 s a tier, chat 29) and pre-flight's declarations check (EFFECTS, JOKE_PROPS, PROP_SIZES,
   LINE_SUBJECTS, TOUCHES, solids...). It prints PASS / FAULT / COULD NOT TEST (rule 19). A step is not done, and its
   handover may not say "built", while the span shows a fault not fixed or named. Rule 67 gains this sentence; the
   job pack "Build" names the one command.
2. Declarations at the plan stage: the film's file is started from a scaffold that already holds every list
   pre-flight reads (empty, with a one-line comment), and the plan chat runs pre-flight once on the empty film so
   crashes and name mismatches in the shared tools show on day one, not at the gate.
3. Phone-size read on every rehearsal clip (rule 24): the clip's sheet shows each beat's subject at phone size with
   its height in pixels; under a floor (e.g. 40 px for the subject of a beat) is a FAULT.

Number to beat: the round's first full quick pre-flight finds under 10 faults (Protest Tiers round 1: 107; moves pass
1: 44); fix-only chats per round 1 or fewer (round 1: 3, chats 28-30); moves stage cost within its plan +20%.
Cost to build: ~1.5-2% of a week (engine flag, scaffold, kittests). Undo: one flag and one rule sentence.
Lost: nothing Sam sees; each build step takes ~10-30 s longer. Added: a FAULT line during building.
