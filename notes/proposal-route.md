# The proposal route (Sam, 15 Nov): build brief

## Where things stand (the ONE handover)
- **Rules that bite next:** 30 (find why first), 85 (cost watch), 89 (fresh-eye helpers).
- **Done (15 Nov, chat 3 cd5f898 = prompt fix; chat 4 = this, amber):** helper.md and judge.md fixed (results first,
  question the frame, size both ways, learn then change; judge may write V0). Replay run 2: clean tree from 5a670b0,
  10 NEW helpers all written; `propose.py judge` run for all five (blind V1-V3 shuffled, key in state.json). All saved
  in `notes/proposals/replay/run2/` (replay-N.md, replay-N/ with chat.md, helper-a/b.md, judge/V1-3.md, state.json).
  Helpers ran 800-1300 words (asked under 800): named, not fixed (the prompt is fixed until this run is scored).
- **Next: Opus MEDIUM (running a clear plan; the judges are opus helpers):** (1) clean tree again: `git worktree add
  --detach SCRATCH/clean 5a670b0`; copy `guides/proposal-route/*.md` and `source/propose.py` in; copy
  `notes/proposals/replay/replay-record` to clean `notes/proposals/`, and run2's replay-N.md and replay-N/ to clean
  `notes/proposals/`. Do NOT run `judge` again (it reshuffles); write each judge line by hand as propose.py prints it
  (root = the clean tree; versions judge/V1-V3; out judge/verdict-raw.md). (2) 5 NEW judges in one message (~2%).
  (3) `propose.py record replay-N` each; copy back to run2; score each pick against "The problem" Better answers above
  (blind; one plain line per case). (4) pass = 4 of 5: hook into `.claude/settings.json` Stop list, `propose.py lock`,
  catalogue row, rule wording to Sam (Opus high for the hook-up). Fail: report to Sam, route stays off, why (rule 30).
- **Needs Sam:** nothing yet (the rerun is the approved plan).
- **Read:** this file only; `guides/proposal-route/judge.md`; the run2 verdicts.
- **Open rule requests:** the route becomes a rule (with its check) only once a replay passes.
- **For Claude:** replay-record/ files hold Sam's messages up to each case, never its own push (checked chat 2).

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
