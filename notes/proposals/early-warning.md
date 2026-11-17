# Proposal: Sam cannot see when a tool or system stops working

Status: open

## Problem
Sam, 17 Nov, word for word: "Is there a way you can have an early warning system when important tools and systems
don't work? Chat switching, the people kit, the code finder are all examples from the last week alone. As you are the
one building these things, I can't see when they fail." Tools and systems that Claude builds stop working, or never
start working, without anyone noticing until Sam spots the result days later. Sam uses only an iPhone and does not
read code, so he cannot see a failure himself.

## Facts
- Chat switching (routine stages on Sonnet): the check (handover.py `model`, built 15 Nov) did not fire on 16 Nov
  although routine chats ran on Opus; causes in notes/proposals/chat-size-and-model/why-model-switch-failed.md
  (word list missed "splice"; reads notes, not the model a chat actually runs on).
- The people kit: Sam said Y to it for films on 14 Nov (notes/morning-report.md line 104, "people kit approved (Y)");
  the catalogue line kept "NOT for films until Sam approves it" until 16 Nov (guides/kit-catalogue.md line 44 now
  reads "APPROVED FOR FILMS by Sam, 16 Nov"; notes/proposals/craft-first-round.md line 45 quotes the old line). A kit
  test failed on it meanwhile (notes/archive/facetool-handovers.md ~line 372: people_from_a_description fails because
  protest_tiers_cast.py imports the kit before approval).
- The code finder: 23 uses on 16 Nov against hand searching ~46 times its cost; its handover flag never fired
  (notes/proposals/finder-use.md Facts).
- Found while writing this (17 Nov): Sam's messages in chat 10ea2689 (07:54-08:07, including the one above) are not in
  notes/ledger/sam/ (the message log hook, handover.py `log`); its last save is 16 Nov 22:17 (git log). `handover.py
  start` said "no saved log" and fell back to the chat record. Why it did not save: unchecked.
- What runs automatically now (.claude/settings.json): at session start setup.sh; on each message costwatch.py and
  handover.py log; after each tool costwatch.py; at each reply's end ledger.py auto and propose.py hook. kittests.py
  ("each shared-kit check tested against the film fault that taught it") runs only when a chat calls it; nothing
  calls it automatically (grep of setup.sh and handover.py).
- Sam is told things only in chat replies and push notifications (CLAUDE.md "Push notifications").
- Unchecked: how many other tools have silently failed or gone unused; how many days each failure lasted before it
  was seen, beyond the three above.

## Record
notes/proposals/chat-size-and-model/
notes/proposals/finder-use.md
notes/proposals/craft-first-round.md
notes/morning-report.md
notes/archive/facetool-handovers.md
notes/logs/
notes/ledger/
.claude/settings.json
.claude/hooks/
source/handover.py
source/kittests.py
guides/kit-catalogue.md
