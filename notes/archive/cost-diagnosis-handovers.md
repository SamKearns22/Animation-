
# Handover replaced 13 Nov (cost job chat 1)
## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch: it measures a chat, never a film), 24 (estimates from real costs), 74.
- **Done (13 Nov, diagnosis chat, Sonnet then Opus):** found that the cost record is wrong and the process has grown
  (facts below). Sam: Y to rebuilding the record; NO to "a film cap": "recording and alarming is useful but doesn't
  solve the problem: how do we make each step cost-efficient and high quality."
- **Next: chat 1 of 8, Opus high (building new tools and a new plan).** Jobs A, B, C below, in order.
- **Needs Sam:** nothing until the proposals (job C).
- **Read:** this file only; then the parts named in each job.
- **Open rule requests:** none.
- **For Claude:** real per-chat cost = `get_session(...).external_metadata.usage.cost_usd` (list $), plus
  `modelUsage` in the last `result` event (`list_events kinds=["result"]`) for the split by model. WEEK_USD 290 in
  `.claude/hooks/costwatch.py` is the yardstick (an estimate).

