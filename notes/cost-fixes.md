# Cost fixes (Sam, 17 Nov): chat size, the model switch, the code finder, an early warning

## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch), 24 (budget stop), the proposal route (`source/propose.py`).
- **Done (chat 10ea2689, Opus, 17 Nov):** cost audits read; chat size measured (42 Opus chats + Anthropic's prices:
  cheapest ~100 steps, flat 50-150); proposal `chat-size-and-model` judged; Sam's Y to option 2 amended
  (`notes/proposals/chat-size-and-model/sam.md`); why the model switch failed (`.../why-model-switch-failed.md`);
  code finder checked: barely used on 16 Nov (sam.md, last lines). Sam's Y (17 Nov) to 1, 2, 3 below.
- **Done (chat A, Opus medium, 17 Nov):** job A built: rule 85 row and costwatch amber 250k / red 370k, warning
  lines count steps and say aim ~100, up to 150, never mid-fix (kittest `cost_watch_lines` passes); CLAUDE.md
  "Models and chats" has the Chat size lines. Wording sent to Sam word for word.
- **Next, two chats side by side (A done, see above):**
  A. **(done) Opus, medium (build from a clear plan):** build 1: rule 85 and `.claude/hooks/costwatch.py` amber 250k,
     red 370k; CLAUDE.md "Models and chats": aim ~100 steps, up to 150 to finish a stage, never hand over mid-fix;
     no chat under ~40 steps except notes after an hour's gap or a whole routine stage on Sonnet; routine stages
     on Sonnet. Wording to Sam word for word after writing; kittest for the warning lines.
  B. **Opus, high (proposal route, no building):** three proposals, each `propose.py new/pack/judge/record`:
     (2) the model switch (facts: why-model-switch-failed.md); (3) chats use the code finder and it covers shared
     tools (facts: sam.md search check, notes/proposals/learn/search-cost.md); (4) Sam, 17 Nov: "an early warning
     system when important tools and systems don't work ... I can't see when they fail" (chat switching, the
     people kit, the code finder in one week). Then ONE message to Sam with all three, top two each.
- **Needs Sam:** nothing until B's message.
- **Read:** this section; for A, rule 85 row and costwatch.py's MAP; for B, `guides/proposal-route/` and the files named.
- **Open rule requests:** none unwritten (1 written by chat A). Branches named (not merged, waiting on Sam, as in notes/proposal-route.md): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **Settled:** handover check's UNROUTED line (07:54): that ask was later put through the route (verdict recorded).
- **For Claude:** stepcost kinds in ledger rows (`kinds`); show log `notes/logs/*-show.log`; get_session
  configured_model vs last_served_model for the model check.
