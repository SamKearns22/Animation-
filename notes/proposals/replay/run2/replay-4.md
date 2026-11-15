# Proposal: find out which rules and tools work

Status: open (replay case 4)

## Problem
Sam: "This then is a systemic issue that could apply to every rule, test, kit and process ever written into the
project." We do not know which of the project's rules and tools are followed, or which of them actually help (fewer
notes, fewer faults reaching Sam, lower cost). Decide how to find out, and what to do with what is found.

## Facts
- About 64 rules (guides/film-quality-rules.md plus CLAUDE.md) and about 115 tools and kits (guides/kit-catalogue.md);
  counts unchecked.
- Only a few act on their own, as hooks in .claude/settings.json: the cost watch, the handover log and the ledger
  (check the file); others (pre-flight, checks) run only when a chat runs them.
- The notes-round section of guides/job-packs.md already tells a chat to use page.py; chats 29 and 31 still ran it 0
  times and searched code by hand 25 and 26 times (record: tool-use file).
- Earlier failures named in this chat: cost stops fed chats' own cost figures that were 20-75% too low; the critic
  found 8 faults in a "pillar" rule only after Sam asked for a critique.
- Protest Tiers' ledger holds every chat's real cost; its notes file holds Sam's notes; the handover check can read a
  chat's own record for free (source/handover.py).
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case4.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
notes/ledger/protest-tiers.md
notes/protest-tiers.md
CLAUDE.md
guides/film-quality-rules.md
guides/kit-catalogue.md
guides/job-packs.md
source/handover.py
source/ledger.py
.claude/settings.json
