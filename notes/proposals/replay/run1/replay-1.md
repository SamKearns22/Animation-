# Proposal: cut what it costs to make a film

Status: open (replay case 1)

## Problem
Sam wants the films to cost less to make without being worse. He has said the cost stops are only a warning; what
matters is "the cost of how the work is carried out in the first place". Two recent Protest Tiers chats were
measured step by step. Decide what change to make to cut the cost of making films.

## Facts
- Chat 29 cost $6.29 (92 tool calls); chat 31 cost $5.78 (117 tool calls); the split by kind of step is in the bills
  file (estimates from step counts, not metered).
- Protest Tiers has run 29 chats so far at roughly $3-8 each (the app's real figures, in the ledger).
- Each step re-reads the chat's whole history, so a step costs more the longer the chat (source: notes on cost in
  .claude/hooks/costwatch.py).
- Tools to find code already exist: a code MAP at the top of each film's code (rule 61) and `source/page.py`.
  Whether chats 29 and 31 used them: unchecked.
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/bills-29-31.md
notes/proposals/replay-record/sam-to-case1.md
notes/ledger/protest-tiers.md
notes/ledger/protest-tiers.json
CLAUDE.md
guides/job-packs.md
guides/film-quality-rules.md
guides/kit-catalogue.md
.claude/hooks/costwatch.py
source/page.py

## Verdict (the judge, word for word)
<!-- verdict-hash: b2a3a0c72743f2a4 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 7 found, 4 fixed, 3 named.

## Leak
yes: mild. The Facts list says the code-finding tools (the MAP, page.py) "already exist" and that whether chats 29 and 31 used them is "unchecked". That points a helper towards "make the chats use the existing tools". V1 took that line almost whole. V2 and V3 used the record to go past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 4 | 5 | 15 |
| V2 | 4 | 3 | 3 | 2 | 4 | 16 |
| V3 | 4 | 3 | 4 | 4 | 4 | 19 |
## Sam test
Q1: Yes. An agent-workflow expert cuts history × steps with one-call tools and blocks the costly habits with a hook. They would also extend the tools that exist (round.py, handover.py) before writing new ones, and the final version now does that.
Q2: Wide enough. It uses two whole metered chats, the code-tool count, all 32 ledger rows and page.py's code. The acceptance re-run of chat 29's job is the right evidence for the decision.
Q3: The hook blocks rather than advises, the per-step log shows any bypass, and the ledger columns show the result in every chat. Weak spot: a python read of code can slip past a pattern hook. The log catches it, but the hook does not stop it.
Q4: Five approaches were weighed (V3), and V2 weighed four. Only "lean main chat, enforced" cuts every later step without touching the films.
Q5: The tools are proven on chat 29's real job before Sam's yes, and the hook comes out by removing one settings entry. A wrongly blocked command costs one step, and the refusal names the right tool.
Q6: Most facts were checked: the $4.98 average (nine app figures, recomputed), 32 looks per chat, 0 page.py runs, the page.py name bug (confirmed in its code), and that no pre-tool hook exists today. Unchecked: the cost shares by kind of step, and the $3 target.
Q7: It is sized to halve a work chat, against a cost of about 3-4% of a week. About $2 saved on each of roughly 20 work chats is about 16% of a week per film, so it pays back within one film.
Q8: It is permanent once it passes the acceptance run, and it is reviewed against the next film's ledger when Sam declares the film complete. The acceptance run is a gate before the yes, not a trial.
## Pick
V3
## Why
V3 finds a real root cause that the other two missed. page.py cannot serve this film, because the code is `protest_tiers*.py` while the film's story files are `protest-tiers-*`, and no page was ever built. It enforces with a hook that blocks, not with more text. It sets a number to beat from the app's real figures, and it proves the tools on a real job before Sam is asked.
V1 relies on chats choosing a tool, which already failed twice. It has no target, and its chat 31 split is wrong: waiting, renders, saving and notes come to about 44%, not 30%.
V2's fixer helper depends on page.py, which is broken here and which V2 never checked. It also rests on an unchecked guess that the hook can tell a helper from the main chat, and its hand-offs add risk to the film's edits.
Taken from V2: the hook's repeat rule applies only when the file has not changed since the last run, the per-step log of tokens and kind of step, and reusing round.py instead of writing new tools.
## Faults in the pick
- F1 [fixed] V3's `run` and `fix` overlap round.py, which already checks, clips, makes a sheet and saves in one command. V3 never named it. They are now folded into round.py as new steps.
- F2 [fixed] Blocking "an identical command" would also block a correct re-run after an edit. It now blocks only when the files the command touches are unchanged (from V2).
- F3 [fixed] A render run in one blocking call would break on renders longer than the 10-minute command limit. Long renders now run in the background with exactly one wake.
- F4 [fixed] The page.py fix must handle both names (`protest_tiers` code, `protest-tiers` story files), not just one.
- F5 [named] The hook cannot see every way of reading code, for example a python script that prints a file. The per-step log shows any bypass, but nothing blocks it.
- F6 [named] "No more notes per round" cannot be measured yet. The ledger's notes column reads 0 for all 32 chats, so it must be filled before the acceptance run counts.
- F7 [named] The $3 target and the cost shares by kind of step are estimates. The problem says 29 chats, but the ledger lists 32, and three chats titled "Opus" are logged as Sonnet.
## Final version
**Aim:** a lean main chat. Every mechanical job takes one call with a short printout, and the costly habits are blocked by the app, not left to choice.

1. **Fix page.py** so it finds a film's code whether the name uses a hyphen or an underscore (`protest_tiers*.py` beside `protest-tiers-*.txt`). Pre-flight and the handover rebuild the page, and the handover check fails if the page is missing or empty.
2. **A pre-tool hook** (none exists today) that refuses three things, each with a one-line pointer to the right tool:
   - shell reads of more than 60 lines of film or engine code (point: `page.py FILM find`);
   - re-running a command whose files have not changed since its last run;
   - checking a render more than once.
3. **Extend round.py.** A new `--edits` step applies a list of edits and then runs the checks, printing only the faults. A new `render` step runs the render; a long one runs in the background with one wake, and prints the verdict and the faults.
4. **Extend `handover.py end`** to do the status update, the ledger, the commit and the push to both branches in one call. Extend `handover.py start` to print one start sheet in place of 11-19 reads.
5. **Measure.** The cost watch logs each step's tokens and its kind of step. The ledger gains three columns per chat: steps, final history size, and Sam's notes per round (filled, not 0).

**Number to beat** (app figures): work chats 22-31 average $4.98, and chats 29 and 31 took 92-117 steps and ended at 229-252k tokens. The target is under $3, 50 steps and 130k tokens per work chat, with no more notes per round.

**Acceptance before Sam's yes:** re-run chat 29's job from its starting commit with the new tools. They are kept only if the run costs half or less and the result passes the same checks.

**Cost:** about 3-4% of a week (one Opus high build chat plus about 1.2% for the re-run), filed as tool work. It pays back within one film.

**Reviewed** against the next film's ledger when Sam declares it complete.

Lost: the main chat can no longer print whole code files, repeat an unchanged command or keep checking a render.
Added: the page.py fix, one hook, two new round.py steps, a one-call handover and start sheet, the per-step log and three ledger columns.
## For Sam
### Option 1: Lean chats, enforced
Most of a chat's cost is the same growing history being re-read at every step. The chats took 92-117 steps, a third of them hunting through code. The tool meant to stop that could not even find this film's code, because of a naming slip, and nothing made the chats use it anyway. This fixes the tool, makes each routine job (fix, check, render, save, hand over) a single step, and has the app itself refuse the wasteful habits. It is proven first by redoing chat 29's real job: it is kept only if that costs half or less. You would notice cheaper chats (aim: under $3, against about $5 now) and the same films.
Lost: chats can't browse whole code files or keep re-checking a render.
Added: one guard, a few one-step tools, a test run on chat 29's job (about 1% of a week), and a cost-per-step record.
### Option 2: Helper chats do the fixing
The main chat keeps talking to you and judging the work. Each note's fix goes to a small, fresh Sonnet helper that finds the lines, edits them, checks them and hands back the clip. Small helpers mean short histories, so each step is cheaper. The risk is more hand-offs, so more chances of a wrong edit reaching the checks. It also depends on the same broken code-finding tool being fixed first. You would notice cheaper rounds, with clips arriving from helpers.
Lost: the main chat can't read code in big chunks; it relies on the helpers' edits.
Added: a fixer helper, a guard, and a cost-per-step record.
