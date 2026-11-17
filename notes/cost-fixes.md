# Cost fixes (Sam, 17 Nov): chat size, the model switch, the code finder, an early warning

## Sam's answers (17 Nov, chat C)
- [x] model-switch (built chat D: .claude/hooks/modelguard.py, routine kind in stepcost): Option 1 (look back, then a guard that STOPS an expensive chat doing routine work). Sam: "this guard
  should already exist, we have used it plenty, it just vanished." Found: nothing that stops was ever deleted (no
  PreToolUse hook in git history). What existed and still exists: handover.py MODEL flag (15 Nov), which only reads
  the Next line's words; costwatch knows the real model but only prices it. Tell Sam this plainly; build on both.
- [x] finder-use (built chat D: .claude/hooks/finderwarn.py, stepcost.search_record, handover end per chat): Option 1 (per-chat search record + one-line reminder at the moment of hand searching).
- [x] early-warning (built chat D: source/watcher.py, Stop hook, start lines, kittests in the background): Option 1 (look back, then watcher of real results, daily "all held"), PLUS Sam: "it needs to
  adapt to new systems we build too": every new hook/check/tool must register its expected result with the watcher,
  and the watcher flags any system with no entry (a kittest for that).
- Order (Claude's pick, Sam didn't answer Q4): model guard, finder reminder, watcher last so it checks the other two;
  the message-log save fault is fixed first inside the watcher's look-back.
- Q5 (delete stray page claude.ai/artifact/BsPpuixgT8nQZy6h2LvMnn): unanswered; re-ask, delete only on Y.

## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 85 (cost watch), 24 (budget stop).
- **Done (chat D, Opus high, 17 Nov):** the three builds, each with a kittest (all pass): the model guard (stops
  finish.py, a whole-film render, a splice into animations/ on Opus/Fable; clips allowed; GUARD_OK escape logged);
  the search reminder (one line at a chat's first hand search of film code with no show; per-chat search record on
  every ledger row; handover end names the chat, not the day); the watcher (a promise per system, checked at every
  Stop, standing list notes/logs/broken.md, daily alive line, flags any new hook / handover check / pack tool with no
  promise, and any promise naming a missing kittest). Message saver fixed (the app now stamps typed messages "human";
  any stamp read as a robot; nothing saved since 16 Nov 19:02). Watcher's first catch: the kit list said places and
  moves kits "NOT for films" though Sam said Y on 14 Nov: lines corrected.
- **Learn step, honest:** only 1 of 4 checked 16 Nov chats can still be opened (list_events: not found), so the
  look-back used the ledger and the notes' Next lines; the guard's command list comes from those (F6/F7 named).
- **Live proof (first Opus chat after this, step 1; in chat D the search reminder and watcher ran live, the guard did not load mid-chat):** run `python3 source/finish.py /none.mp4 /tmp/x.mp4 --film none`:
  it must be refused with MODEL GUARD (hooks load at chat start, so chat D could only prove it on its own record).
  If not refused, the watcher flags "guard" at that chat's Stop.
- **Next:** nothing queued: the chain stops for Sam's answer below. Broken list (notes/logs/broken.md) holds 2 kittests failing before chat D (round_page, facehouse_whole_head): the next code-finder or face-tool chat owns them.
- **Needs Sam:** Y/N delete the stray page claude.ai/artifact/BsPpuixgT8nQZy6h2LvMnn (asked again, chat D).
- **Open, own route later:** whether clips and sound are routine (Sonnet) work (model-switch F5): through propose.py
  with the guard's log and the routine figures, not asked unjudged. Finder later changes wait for Learn's numbers.
- **Read:** this section only.
- **Open rule requests:** none unwritten. Branches named (not merged, waiting on Sam, as in notes/proposal-route.md):
  claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** guard .claude/hooks/modelguard.py (routine(), _runs()); finderwarn.py; source/watcher.py PROMISES
  (a new system adds its entry + kittest); handover.py TYPED/ROBOT; kittests model_guard_stops_routine_on_opus,
  message_saver_keeps_typed_messages, finder_reminder_per_chat, watcher_catches_last_weeks_four. Old handovers
  notes/archive/cost-fixes-handovers.md.
