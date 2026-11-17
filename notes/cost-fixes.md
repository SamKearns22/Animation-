# Cost fixes (Sam, 17 Nov): chat size, the model switch, the code finder, an early warning

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
