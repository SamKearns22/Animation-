# The proposal route (Sam, 15 Nov): build brief

## Where things stand (the ONE handover)
- **Rules that bite next:** 30 (find why the first fix failed), 85 (cost watch), 89 (fresh-eye helpers).
- **Done (15 Nov, chat 1, session ...MBu, stopped at red):** built `source/propose.py` (steps 1-6: new, pack, judge
  blind and shuffled, record with hash, show, Stop `hook`, review, mark, lock) and the fixed prompts
  `guides/proposal-route/` (helper.md, judge.md, sam-test.md: Sam's 8 pushes word for word, glosses kept generic so
  they never carry a replay case's answer). Kittest `proposal_route_hook` written: 2 sub-checks FAIL ("valid verdict
  + Critiqued line blocked", "mark made the verdict stale"), not yet debugged. The five replay cases are written
  (problem + facts as before each push, chat.md = the parent chat's own first answer, word for word) in
  `notes/proposals/replay/`; all 10 helper answers are written and saved there (with each case's state.json). NOT switched on: the
  hook is not in `.claude/settings.json`, no LOCK.
- **Next: Opus HIGH (building something new):** (1) fix the 2 kittest failures (debug `verdict_ok` after `record`
  in a temp PROPS); (2) rebuild the clean replay tree: `git worktree add --detach SCRATCH/replay-tree 5a670b0`
  (the main line at 19:44, before the brief existed: no leak), copy `guides/proposal-route/`, `source/propose.py`
  and `notes/proposals/replay/*` into its `notes/proposals/`; (3) for each case `propose.py judge replay-N` in the tree,
  one NEW judge per case (all five in one message), then `record`; (4) compare each pick
  with the "Better" answers below (case 3 passes if the pick covers 6+ of its 8 faults and does not rely on naming a
  tool in a pack); pass = 4 of 5; on a fail, rule 30, fix prompts, rerun once; (5) on a pass: add `python3
  source/propose.py hook` to the Stop hooks, `propose.py lock`, catalogue row, rule wording to Sam; report one plain
  line per case. Budget: helpers cost ~0.4% of a week each (chat 1: 4.3% on 10 helpers): run them from a FRESH chat,
  never a long one.
- **Needs Sam:** nothing until the replay result.
- **Read:** this file only (plus `source/propose.py` MAP and the kittest).
- **Open rule requests:** the route itself becomes a rule (with its check) only once the replay passes.
- **For Claude:** correction from the parent chat: the paused job's commit 1787a2f IS wired in (job-packs Notes round,
  rule 61, its catalogue row, handover.py start; kittest round_page passes). Leave it; it is the route's first real
  review once the route passes. Replay limit to tell
  Sam: the judge's questions are Sam's own past pushes, so the replay shows the route asks them for him; it cannot
  show it catches a new kind of push.

## The problem (evidence from this chat, 15 Nov)
Claude's proposals are a first plausible idea, sized small and cheap, anchored on that idea; they only got better
when Sam pushed. Sam cannot code and cannot be the system's critic. In one chat Sam pushed five times, each giving a
better answer (these are the replay cases):
1. Code-finding fix proposed (looking at code is ~30% of a chat's steps). Push: "Is this what you would suggest as an
   AI efficiency expert?" -> Better: the fix is modest; the number of chats, start-up reading and bookkeeping (~30% of
   chat 31) are bigger levers; measure across the film before tuning one chat.
2. Bill check of the cheapest and dearest chat proposed. Push: "What would get us the best result? ... or just this
   film" -> Better: this film (newest tools), a spread across every kind of work, not extremes.
3. A "pillar" rule (fixes aim for the biggest result). Push: "Critique that rule and make sure it will
   comprehensively deliver" -> 8 faults: vague "thorough", no root cause, "used" is not "worked", no numeric target,
   a lesser option invites half-fixes, unchecked claims told to Sam, only after failures, no enforcement.
   Further: naming a tool in a pack already failed (`guides/job-packs.md` notes round names `page.py`; chats 29 and
   31 ran it 0 times, and searched code by hand 25 and 26 times).
4. A full audit of all ~64 rules and ~115 tools (8-12% of a week). Push: "Is this the most intelligent thing to do
   and the best way to adhere to statement 1?" -> Better: results first (the film's cost by stage and Sam's notes,
   catchable vs taste), trace only those to the rules/tools that should have stopped them, and make measuring
   automatic at every handover (free, from the chat's own record); ~3-5%.
5. Push: "Saying yes to anything now carries huge risk" -> Better: split learning (read-only, safe) from changing
   (one change at a time, with evidence and a number to beat).
Also: Claude told Sam "the tools weren't used" before checking (it was true, but unchecked).

## The route (Sam's Y; step 6 is Sam's own wording)
Scope by KIND, never by the chat's own cost estimate: any change to rules, tools, checks, kits or how films are built
(not animatics, renders, clips or film notes).
1. The chat writes the problem and the raw facts, NO solution, to `notes/proposals/NAME.md`.
2. Two fresh helpers, each from a fixed prompt file the chat does not edit, each given only the problem file and the
   paths to the raw record (never the chat's idea), write their own approach.
3. A third fresh helper, the judge (fixed prompt file), scores every version, the chat's included, on a fixed list:
   high quality, fewer notes and faults, cost against 15% of a week, risk, can it be undone; answers the Sam test
   (Sam's pushes above, word for word, 8 questions at most, merged not added); picks one; writes its verdict into the
   proposal file, word for word, with the file's hash.
4. Enforced where the work happens: a Stop hook blocks any reply that asks Sam to approve a change while
   `notes/proposals/` holds no matching verdict for it. Detect by the proposal file (written this turn, or named in
   the reply), not by wording alone. Must honour `stop_hook_active` (no endless loop) and never block routine Y/N
   questions (animatic, final render).
5. Sam sees the top two options in plain English, with Lost/Added lines, and "Critiqued: N found, N fixed, N named"
   counted from the file.
6. **No trials, nothing temporary (Sam, 15 Nov).** When Sam declares a film complete, Claude reviews every change made
   since the last film against that film's results (Sam's notes, faults he caught, cost from the ledger). Any change
   that needs changing goes through steps 1-5.
Measure (automatic, in the end-of-film review): how often a proposal is later replaced, notes and cost per film.
Not "how often Sam pushes" alone (it falls if Sam tires).

## Replay test (it must pass before the route is switched on)
For each of the five cases, write only the problem and facts as they stood BEFORE Sam's push, run steps 1-3, and
compare the judge's pick with the "Better" answer above. Pass: the route reaches the better answer (or one the judge
shows is better still) in at least 4 of 5 without Sam's push. Report each case to Sam in one plain line. On a fail,
find why (rule 30), fix the prompts, rerun once; then report either way.

## Build notes
- **Kittest fixes (15 Nov, chat 2; rule 30, why):** (a) `record` wrote `open(f,'w').write(problem_text(name)...)`:
  Python opens (truncates) the file before reading it, so every recorded proposal lost its problem and read as stale.
  Fixed by reading first. (b) `verdict_ok` hashed the raw verdict, not the copy in NAME.md, so an edit below the
  verdict went unseen; it now checks the copy is word for word. kittest `proposal_route_hook` passes.
- Reuse: rule 89's critic helper (`.claude/agents/critic.md`, `source/critique.py`) for how helpers are started
  and their reports saved; handover.py's .jsonl reading; the Stop hook list in `.claude/settings.json`.
- Kittests for the hook (blocks a change proposal without a verdict, passes one with it, passes a routine animatic
  Y/N, honours stop_hook_active). Catalogue row. MAP at the top of any new file.
- After it is on, the next jobs go through it: the paused code-tool job, the results-first review of Protest Tiers,
  the automatic per-chat measuring. Sam: "the entire system could benefit".
