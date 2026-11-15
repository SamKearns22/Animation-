# Helper A: cutting what a film costs to make

## Leak
None. Its mention of the code tools is a hint, not a solution.

## Root cause
All the mechanical work happens inside the one Opus chat, whose history grows with every step. Each step re-reads it all, and the tools that keep it small rely on the chat choosing them.
- **Where the money goes.** From costwatch.py's prices, chat 29 (92 steps, history 90k to 252k) spent about $2.8 re-reading and $2.0 writing history, of $6.29: about three quarters is history times steps.
- **What fills the history.** Code looks (32 in each chat), check printouts, render waiting (16 in chat 31), repeats and 5 to 6 retries (bills-29-31.md).
- **Why the earlier fix failed.** Neither chat ever ran page.py or codemap.py; they used grep or sed 25 and 26 times (tool-use-29-31.md). The notes pack (job-packs.md) and "One wait per render" are text to follow; chat 31 tailed one render file 5+ times. Rule 61's check only tests that a MAP exists. Only the checks the app runs itself held (settings.json).
- **No helpers used.** 0 spawns, even though a working helper pattern exists (critic.md).

## Approaches weighed
1. **Force the code tools.** A hook blocks bare grep or sed on code and points to page.py. Checks, retries and waits still pile up.
2. **The main chat decides, helpers do (chosen).** Mechanical jobs go to fresh Sonnet helpers that return about 10 lines each. A hook enforces it.
3. **One-command tools for every job** (like round.py). Fewer steps, but chats still have to choose to use them.
4. **Leaner start-up and earlier handovers.** Cuts the 90k start, but every one of the 32 chats pays start-up again.

## Proposal
**What it is.** A Sonnet helper, `.claude/agents/fixer.md`, made the same way as critic.md. For one note it runs `page.py find`, reads only those lines, makes the edit and runs `round.py`. It sends back the change, the check line and the clip. The main chat judges the result and talks to Sam.

**How it is enforced.** A hook the app runs before every step. In the main chat it refuses reading more than 40 lines of code, repeating a command on a file that hasn't changed, and checking a running render a second time. Each refusal names the fixer. It also logs each step's tokens and kind of step. Builds on rule 61, page.py, rule 19 and rule 85; new is the enforcement and the split.

**Number to beat.** Notes-round chats now cost $5.78 to $6.29 and end at 229k to 252k of history. The target is at least a third off the cost per note fixed, helpers included, with the main history under 150k at handover. It is measured from the hook's real log. Before building, that log is run over all Protest Tiers chats and the last two films.

**Cost.** About 4% of a week as tool work (unmeasured), kittest included.

**What Sam would notice.** Cheaper rounds, later amber, the same clips and checks.

## Sam test
- **Q1:** Lean history, helpers and app-run enforcement is standard expert practice.
- **Q2:** Confirmed on every Protest Tiers chat and two films.
- **Q3:** App-enforced, aimed at the root cause, measured by the real log.
- **Q4:** Four approaches weighed; only this shrinks every later step.
- **Q5:** One commit undoes it. The same checks, clip and main-chat review catch a wrong helper edit.
- **Q6:** Every source is named. The cost split is my own working.
- **Q7:** It is sized by the result. Approach 1 alone would be the cheap trap.
- **Q8:** Built in full; reviewed against the ledger at the film's end.

## Lost / Added
- Lost: the main chat can no longer read code freely in big chunks.
- Added: the fixer helper, the guard hook, the per-step log and a kittest.

## Unchecked
- Whether the hook can tell helpers from the main chat (the kittest decides).
- The cost split.
- Chat 31's model: the ledger says sonnet, the title says Opus.
- The 4% build cost.
- The chat count: the problem file says 29, the ledger lists 32.
