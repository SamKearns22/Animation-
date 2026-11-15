# Proposal: cut what it costs to make a film

Status: open (replay case 1)

## Problem
Sam wants the films to cost less to make without being worse. He has said the cost stops are only a warning; what
matters is "the cost of how the work is carried out in the first place". Two recent Protest Tiers chats were
measured step by step. Decide what change to make to cut the cost of making films.

## Facts
- Chat 29 cost $6.29 (92 tool calls); chat 31 cost $5.78 (117 tool calls); the split by kind of step is in the bills
  file (estimates from step counts, not metered).
- Protest Tiers has run 29 chats so far at roughly $3-8 each (the app's real figures, in the ledger).
- Each step re-reads the chat's whole history, so a step costs more the longer the chat (source: notes on cost in
  .claude/hooks/costwatch.py).
- Tools to find code already exist: a code MAP at the top of each film's code (rule 61) and `source/page.py`.
  Whether chats 29 and 31 used them: unchecked.
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/bills-29-31.md
notes/proposals/replay-record/sam-to-case1.md
notes/ledger/protest-tiers.md
notes/ledger/protest-tiers.json
CLAUDE.md
guides/job-packs.md
guides/film-quality-rules.md
guides/kit-catalogue.md
.claude/hooks/costwatch.py
source/page.py
