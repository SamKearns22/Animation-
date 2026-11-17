# Cost fixes (Sam, 17 Nov): chat size, the model switch, the code finder, an early warning

## Sam's answers (17 Nov, chat C)
- [ ] model-switch: Option 1 (look back, then a guard that STOPS an expensive chat doing routine work). Sam: "this guard
  should already exist, we have used it plenty, it just vanished." Found: nothing that stops was ever deleted (no
  PreToolUse hook in git history). What existed and still exists: handover.py MODEL flag (15 Nov), which only reads
  the Next line's words; costwatch knows the real model but only prices it. Tell Sam this plainly; build on both.
- [ ] finder-use: Option 1 (per-chat search record + one-line reminder at the moment of hand searching).
- [ ] early-warning: Option 1 (look back, then watcher of real results, daily "all held"), PLUS Sam: "it needs to
  adapt to new systems we build too": every new hook/check/tool must register its expected result with the watcher,
  and the watcher flags any system with no entry (a kittest for that).
- Order (Claude's pick, Sam didn't answer Q4): model guard, finder reminder, watcher last so it checks the other two;
  the message-log save fault is fixed first inside the watcher's look-back.
- Q5 (delete stray page claude.ai/artifact/BsPpuixgT8nQZy6h2LvMnn): unanswered; re-ask, delete only on Y.

## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 85 (cost watch), 24 (budget stop).
- **Done (chat C, Opus medium, 17 Nov):** early-warning judged; all three sent; Sam picked 1, 1, 1 (see answers above).
- **Next (Opus, high: building new tools):** build in order: model guard, finder reminder, watcher (adapts to new
  systems). Kittest each; "Added/Lost" per piece in the message. Fix the message-log save fault early.
- **Needs Sam:** Y/N delete the stray page (re-ask once in the next message).
- **Read:** "Sam's answers" and this section; the three proposal files; `guides/proposal-route/` only if a step fails.
- **Open rule requests:** none unwritten. Branches named (not merged, waiting on Sam, as in notes/proposal-route.md):
  claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** proposals notes/proposals/{model-switch,finder-use,early-warning}.md; handover.py MODEL flag,
  .claude/hooks/costwatch.py fam(); settings.json has no PreToolUse hook yet.
