# Proposal: Measure what each new chat costs before its first real work, and set chat size from it

Status: open

## Problem
A film is a chain of about 15 chats. Every new chat pays to load the app's own instructions, CLAUDE.md, the
handover, the stage's pack and the film's notes before it does any work, and then pays to re-read all of that at
every later step. Longer chats pay that start once but re-read an ever larger history at every step. The chat-size
rules (about 100 steps, up to 150 to finish a stage, none under about 40) were set by judgement, and Sam has been
told different things at different times. Nobody has measured a chat's start-up cost directly, so the trade-off
between more, shorter chats and fewer, longer ones is not known on real numbers.

## Facts
- Milburn (notes/ledger/milburn.json): 15 chats, 1,281 steps (mean 85), 32.4% of a week by estimate, 22.0% on
  Sam's app at posting. Steps per chat: 68, 92, 130, 59, 136, 92, 71, 14, 91, 98, 123, 122, 40, 117, 28.
- 47 Opus chats with step counts across notes/ledger/*.json (all transcript estimates; counted 19 Nov). Cost per 100
  steps (% of a week) by length: under 40 steps 4.13 (7 chats, ending ~126k history); 40-69: 3.36 (22, ~191k);
  70-99: 2.82 (11, ~230k); 100-129: 2.74 (4, ~226k); 130+: 2.68 (3, ~301k). Linear fit: cost = 0.58 + 0.0225 x
  steps. Quadratic fit: 0.86 + 0.0146 s + 0.0000451 s^2, so cost per step is lowest near sqrt(0.86/0.0000451) ~138
  steps. The fixed term (0.58-0.86% a chat; x15 = 9-13% of a Milburn-sized film) is noisy and confounded: short
  chats are often different work (routine, fixes, failed starts).
- notes/proposals/chat-size-and-model.md (open, verdict picked helper A, not yet decided by Sam): the same kind of fit
  on 42 chats, minimum near 106 steps; 11 Nov "a chat start measured 0.15-0.3% of a week". Sam's brief: a 20-hour
  gap costs about 0.2% of a week.
- This chat (19 Nov): 83k tokens in context at its first step, before reading anything (app instructions and tools,
  CLAUDE.md, hook output). notes/proposals/startup-reading.md: near-empty chats end at ~90-100k.
- The ledger keeps per chat: steps, end history (hist_k), kind shares; not the context at step 1, the cost up to
  the first real work, or what the start read (handover, pack, notes). No marker of "first real work" exists.
- Prices (.claude/hooks/costwatch.py): Opus re-read $0.18/M, write $8/M, output $25/M; WEEK_USD 245 (provisional).
  The prompt cache lasts one hour; a chat resumed after longer re-writes its whole history at the write price.
- Cost watch (rule 85; CLAUDE.md): amber at 200k history or 3% a chat, red at 300k or 5%; a fresh chat for every round
  and every cost warning; chats never hand over mid-fix.
- The 15 Milburn transcripts are no longer in the container; ledger.py auto runs stepcost on every chat at its end.

## Record
notes/ledger/milburn.json
notes/ledger/milburn.md
notes/ledger/protest-tiers.json
source/stepcost.py
source/ledger.py
.claude/hooks/costwatch.py
notes/cost-diagnosis.md
notes/proposals/startup-reading.md
notes/proposals/chat-size-and-model.md
tests/stepcost-transcript.jsonl
