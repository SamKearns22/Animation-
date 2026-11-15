# Proposal: Is installing the proposal route the right thing to do?

Status: open

## Problem
Sam (15 Nov, chat 6), word for word: "Is installing this tool the right thing to do? Use the tool to answer".
The "tool" is the proposal route (notes/proposal-route.md, "The route"): any change to rules, tools, checks, kits or
how films are built goes to two fresh helpers and a blind judge before Sam sees it, and a Stop hook refuses a reply
that asks Sam to approve such a change without a judge's verdict. Chat 6 has wired the hook into the Stop list (it
loads from the next chat), locked the prompts and added a catalogue row; the permanent rule is not yet written (Sam's
numbers pending). The question is whether this, as built, should be switched on and made permanent: is it the right
thing for the project's results (fewer notes, fewer faults, lower cost per film, better films), or is some other
course better (in any shape: as built, changed, narrower, wider, undone, or something else). Sam cannot code and
cannot be the system's critic; whatever is chosen must hold without him checking it. Sam has said "No trials,
nothing temporary" (15 Nov) and that "saying yes to anything now carries huge risk".

## Facts
- Why the route exists: in one chat (15 Nov) Sam pushed five times and each push produced a better answer than
  Claude's first; Claude's proposals were "a first plausible idea, sized small and cheap" (notes/proposal-route.md,
  "The problem", cases 1-5).
- Replay run 1 did not pass; prompts were fixed; replay run 2 PASSED 4 of 5 (case 2 a miss: judge added two older
  films and picked the dearest chats). Every pick was a helper's; the chat's own version scored lowest in all five
  (10-14 of 25 against 20-22) (notes/proposal-route.md, "Replay run 2 scores"; notes/proposals/replay/run2/).
- The replay's judge and helpers are the same model family as the chat being judged (Agent general-purpose, opus;
  source/propose.py HELPER/MODEL). The "Better" answers were known to the person who wrote the prompts (chat 3-4),
  so the prompts may be tuned to these five cases (unchecked).
- Helpers ran 800-1300 words when asked for under 800 (notes/proposal-route.md, For Claude).
- Cost to build so far: 6 chats in notes/ledger/proposal-route.md, 21.7% of a week in total (chat 6 not yet counted).
  Run 2's 10 helpers cost about 4.4-4.8% and 5 judges 2.12% of a week, so one route run is roughly 1.3-1.5% of a week
  (estimate from those two chats). For scale: Protest Tiers took 33 chats, 53.6% of a week; Blessed 24 chats, 62.2%
  (notes/ledger/protest-tiers.md, notes/ledger/blessed.md).
- Protest Tiers is ON HIATUS at animatic 3 until the route is built and proven (story/status.md).
- The hook (source/propose.py `hook`, `reply_faults`): finds lines with a Y/N or choice marker; flags a change by
  word lists (CHANGE_RE: rule, tool, check, kit, hook, guide, .py ...; ROUTINE_RE passes animatic, render, clip,
  sheet, voice ...). Tested chat 6: blocks all 5 original replies from the five cases, passes routine animatic and
  final-render questions, never blocks twice (stop_hook_active: logs to notes/proposals/unrouted.md, which
  `handover.py end` now flags). A change made without asking Sam a Y/N question is not seen by the hook (unchecked
  how often that happens). Kittest proposal_route_hook passes.
- Rules Sam asks for himself ("I want a rule") also need a route run before the wording reaches him once the hook is on.
- Step 6 (end-of-film review of every change since the last film) is written (`propose.py review`) but has never run
  on a real film.
- Queued behind the route: a paused code-finding tool job, a results-first review of Protest Tiers, automatic per-chat
  measuring (notes/proposal-route.md, Build notes).
- The rulebook must never grow; every new rule replaces, merges or turns a by-hand rule into a check (CLAUDE.md,
  "Rules are permanent"). The closest existing rules: CLAUDE.md "Before suggesting anything, search the rulebook and
  kit catalogue" (12 Nov, by hand); "Back-end proposals get a plain explanation" (14 Nov); rule 89 (fresh-eye critic
  helpers, for pictures).

## Record
notes/proposal-route.md
notes/proposals/replay/run2
notes/proposals/replay/replay-record
source/propose.py
guides/proposal-route
notes/ledger/proposal-route.md
notes/ledger/protest-tiers.md
notes/ledger/blessed.md
CLAUDE.md
guides/film-quality-rules.md
guides/kit-catalogue.md
story/status.md
