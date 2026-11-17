# Proposal: Chat size and model switching: one definitive rule

Status: open

## Problem
Sam has been told, at different times, to use more chats, fewer chats, longer chats and shorter chats; he wants one
answer that holds. Separately, routine work (renders, clips, checks, sound) is running on Opus when it was meant to
run on Sonnet, and the check meant to catch that did not.

## Facts
- 42 Opus chats with a step count (notes/ledger/*.json, rows with `steps`, % of a week). Least-squares fit:
  cost = 1.04 + 0.0063*steps + 0.0000934*steps^2 (the fixed term is noisy; a linear fit gives 0.42 + 0.0235*steps).
- Cost per 100 steps by chat length: <40 steps 4.2 (6 chats, history ~134k); 40-60 3.4 (11, ~181k); 60-80 2.7 (10,
  ~215k); 80-100 2.4 (3, ~226k); 100+ 3.0 (2, ~281k). Fit minimum near 106 steps.
- Protest Tiers, 16 Nov (notes/ledger/protest-tiers.json): 24 chats, 1,479 steps, 39.3% of a week in one day; 10
  chats under 60 steps; Albania, Germany and France chains ran side by side (list_sessions, 16 Nov 14:50-16:18).
- 13 Nov (notes/cost-diagnosis.md): Blessed chat 5 ran to 414k history, $27.73; splitting it into chats of 200k or
  less estimated to save ~$11. Model switches inside a chat re-paid the whole history ($5.80).
- 11 Nov (notes/budget-job.md): ~25 Remakes chats; "too many chats, too many small steps"; a chat start measured
  0.15-0.3% of a week then (corrected figure).
- Cost watch (rule 85): amber at 200k history or 3% a chat, red at 300k or 5%. CLAUDE.md: a fresh chat for every
  round and every cost warning. The prompt cache lasts one hour; a chat resumed after longer re-writes its history.
- Models (CLAUDE.md "Models by stage"): "A round of my notes (deciding, fixing, clips): Opus, medium"; routine
  (checks, check sheet, animatic, filing, final render, sending, saving): Sonnet.
- source/handover.py model_faults (built 15 Nov after chat 30 rendered on Opus) reads only the film notes' Next line;
  its ROUTINE pattern matches finish.py, `final` without --span, final render, animatic render, sending the
  animatic/final, filing. It does not match check, look, sound or clip, and clips (--span) are deliberately excluded.
- 16 Nov, get_session: "back-half chat 7 (France round 4 look, check, clip)" and "back-half chat 8 (France sound)"
  configured and served claude-opus-5-5, medium. Chats whose parent asked for Sonnet ran on Sonnet (Startup reading
  chat 2, Learn chat 2: configured and served claude-sonnet-5-5). The platform switch works.
- Measured Sonnet chats (ledger): 8-17 steps cost 0.21-0.39; 64 steps 0.8; two labelled Sonnet at 72-79 steps cost
  2.6-4.1 (the label is doubted in notes/proposals/learn/protest-tiers-costs.md).

## Record
notes/ledger/protest-tiers.json
notes/ledger/proposal-route.json
notes/cost-diagnosis.md
notes/budget-job.md
notes/proposals/learn/protest-tiers-costs.md
notes/proposals/learn/search-cost.md
notes/job-e-measurements.md
source/handover.py
.claude/hooks/costwatch.py
guides/film-quality-rules.md
CLAUDE.md
