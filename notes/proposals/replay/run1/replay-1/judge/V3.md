## Leak
The problem names the code-finding tools (MAP, page.py), hinting "use them". Treated as evidence only.

## Root cause
Cost ≈ steps × history re-read per step (costwatch.py). The main chat does every mechanical job itself, step by step:
- **Code looks: 32 per chat, about 27-33% of the cost** (bills). page.py could not help. `page.py protest-tiers` finds no files, because the code is named `protest_tiers*.py`, with an underscore (I checked). No protest-tiers page exists.
- **Repeats and polling:** scripts were re-run 2-3 times, with 5-6 retries. A render's output was tailed 5+ times, and 16 steps went on waiting for renders (bills). The rule "one wait per render" was ignored.
- **Bookkeeping and git:** 14 steps in chat 29 and 23 in chat 31 (bills).
- **Start-up:** 11-19 reads of notes and guides in each chat (bills), and there were 32 chats (ledger).

**Why earlier fixes failed:** rule 61, the MAP and page.py are advice that nothing enforces, and page.py was broken here. The cost watch measures dollars, not how the work is done.

## Approaches weighed
1. **Fewer, longer chats.** Saves start-ups; each step re-reads more.
2. **A cheaper model.** This is the cheap-but-worse trap.
3. **Fresh helpers for the looking and editing.** Small histories, but hand-offs risk faults; broad hunts only.
4. **Fewer rework rounds.** Big (chats 18, 29, 31 fixed faults) but separate, and already a rule.
5. **Chosen: a lean main chat, enforced by hooks and one-call tools.**

## Proposal
**What it is.**
- (a) **Fix page.py's name bug.** Pre-flight and handover rebuild the page.
- (b) **A hook that runs before each tool call** (none exists today). It refuses three things, each with a one-line pointer to the right tool:
  - shell reads of more than 60 lines of film code;
  - repeating an identical command;
  - polling a render.
- (c) **`run`** renders in one blocking call and prints the verdict and the faults.
- (d) **`fix`** applies a list of edits and runs the checks in one call, printing the faults only.
- (e) **`wrap`** does the handover check, status, ledger, commit and the push to both branches in one call.
- (f) **`handover.py start`** prints one start sheet instead of 11-19 reads.

**Enforced by:** the hook, which blocks. The ledger also gains two columns per chat, its steps and its final history size.

**Number to beat.** From the app's real figures in the ledger:
- Work chats 22-31 averaged $4.98 (my sum of nine figures).
- Chats 29 and 31 took 92-117 steps and ended at 229-252k tokens.
- Target: under $3, 50 steps and 130k tokens per work chat, with no more notes per round.
- **Acceptance test before Sam's yes:** re-run chat 29's job from its starting commit. The tools are kept only if that run costs half or less.

**Cost:** about 3-4% of a week. That is one Opus high build chat (similar chats cost 1.3-3.2%) plus about 1.2% for the re-run. Filed as tool work.

**Sam notices:** cheaper chats, fewer per stage, same films.

## Sam test
- Q1 Expert: small history and one call per job are the standard levers, both enforced.
- Q2 Best result: two whole chats' bills, all 32 ledger chats, the tool's code.
- Q3 Comprehensive: the hook blocks; ledger columns show every chat's result.
- Q4 Most intelligent: five approaches weighed; only this cuts both without touching quality.
- Q5 Risk: proven on chat 29's job first; removable (one settings entry).
- Q6 Checked: sources named, gaps listed.
- Q7 Not cheap: sized to halve a chat, with an acceptance test.
- Q8 Nothing temporary: permanent, reviewed against the next film's ledger when Sam declares it complete.

## Lost / Added
Lost: the main chat can no longer dump whole code files or repeat identical commands.
Added: one hook, three one-call tools, a start sheet, two ledger columns.

## Unchecked
- The cost shares by kind of step (the bills are estimates).
- The 90k-token fresh base and how much of it is tool definitions.
- Whether chats 29 and 31 tried page.py.
- The ledger lists chats titled "Opus" as Sonnet.
- The $3 target is my own arithmetic.
