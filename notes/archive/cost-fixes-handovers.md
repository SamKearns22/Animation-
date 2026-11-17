## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch), 24 (budget stop), the proposal route (`source/propose.py`).
- **Done (chat 10ea2689, Opus, 17 Nov):** cost audits read; chat size measured (42 Opus chats + Anthropic's prices:
  cheapest ~100 steps, flat 50-150); proposal `chat-size-and-model` judged; Sam's Y to option 2 amended
  (`notes/proposals/chat-size-and-model/sam.md`); why the model switch failed (`.../why-model-switch-failed.md`);
  code finder checked: barely used on 16 Nov (sam.md, last lines). Sam's Y (17 Nov) to 1, 2, 3 below.
- **Next, two chats side by side:**
  A. **Opus, medium (build from a clear plan):** build 1: rule 85 and `.claude/hooks/costwatch.py` amber 250k,
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
- **Open rule requests:** none unwritten (1 is A's job).
- **Settled:** handover check's UNROUTED line (07:54): that ask was later put through the route (verdict recorded).
- **Settled (chat B):** Sam's "Why not handover at 150 if the number doesn't matter at that stage" was answered by
  the amended option 2 (aim ~100, up to 150 to finish a stage; sam.md line 7).
- **For Claude:** stepcost kinds in ledger rows (`kinds`); show log `notes/logs/*-show.log`; get_session
  configured_model vs last_served_model for the model check.

## Chat A's version (merged 17 Nov)
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


## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 85 (cost watch), 24 (budget stop).
- **Done (chat A, Opus medium, 17 Nov):** job 1 built: rule 85 and costwatch amber 250k / red 370k with step counts
  (kittest `cost_watch_lines` passes); CLAUDE.md "Models and chats" has the Chat size lines; wording sent to Sam.
- **Done (chat B, Opus high, 17 Nov; red at 5.1%, 4.3 of it helpers):** three proposals routed. model-switch and
  finder-use: helpers, blind judge, verdict recorded (`propose.py show NAME` prints Sam's text). early-warning: both
  helpers written; judge NOT yet run.
- **Next (Opus, medium: route steps from a clear plan):** `propose.py judge early-warning`, start the one judge with
  the printed line, `record`, then ONE message to Sam: all three `show` texts (top two each, Lost/Added, Critiqued),
  numbered questions, his pick first. Then handover.
- **Needs Sam:** after that message, his numbers on the three. Also: a helper published its notes by mistake as a
  private page only Sam can see (claude.ai/artifact/BsPpuixgT8nQZy6h2LvMnn): ask Y/N to delete (Y recommended).
- **Read:** this section; `guides/proposal-route/` only if a step fails.
- **Open rule requests:** none unwritten. Branches named (not merged, waiting on Sam, as in notes/proposal-route.md):
  claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **Found here:** Sam's message log has saved nothing since 16 Nov (helper A: 19:02); its error output is thrown
  away. It is in the early-warning facts; not fixed (no building in job B).
- **For Claude:** proposals notes/proposals/{model-switch,finder-use,early-warning}.md; branch claude/cost-fixes-b-route.


## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 85 (cost watch), 24 (budget stop).
- **Done (chat C, Opus medium, 17 Nov):** early-warning judged (helper B picked, recorded). ONE message sent to Sam
  with all three proposals (model-switch, finder-use, early-warning), top two each, plus the Y/N on deleting the
  stray page. Nothing built.
- **Next (Opus, high: building new tools):** on Sam's numbers, build the chosen options in his order; delete the
  stray page only on his Y. Chain stopped here on a question for Sam; his answer comes back to this chat.
- **Needs Sam:** Q1 model-switch (1/2), Q2 finder-use (1/2), Q3 early-warning (1/2), Q4 order, Q5 delete page
  claude.ai/artifact/BsPpuixgT8nQZy6h2LvMnn (Y/N).
- **Read:** this section; `guides/proposal-route/` only if a step fails.
- **Open rule requests:** none unwritten. Branches named (not merged, waiting on Sam, as in notes/proposal-route.md):
  claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **Found earlier:** Sam's message log has saved nothing since 16 Nov; its error output is thrown away (in early-warning).
- **For Claude:** proposals notes/proposals/{model-switch,finder-use,early-warning}.md; verdicts recorded.

