# Helper A: find out which rules and tools work

## Leak
None. The problem file states the problem and facts only.

## Root cause
The project has no record of what a rule or tool did. It only has what chats say about themselves, and they rarely say it.
- Outcome fields are typed in by chats, so they are empty. The Protest Tiers ledger shows "32 chats, 0 rounds, 0 notes, 0 repeated" (notes/ledger/protest-tiers.md). Yet round 1 notes exist, and a repeated note ("frames missing", rule 30) was fixed in chat 31 (notes/protest-tiers.md, Where things stand). Those fields fill only when a chat runs `ledger.py log --notes N` by hand (source/ledger.py MAP). Self-reported costs were 20-75% low (sam-to-case4.md). Three chats titled "Opus medium" are logged as sonnet (ledger), so the model column can't be trusted either.
- Use depends on a chat reading an instruction. The job pack names page.py, but chats 29 and 31 ran it 0 times and ran grep/sed 25 and 26 times (tool-use-29-31.md). No PreToolUse hook exists (.claude/settings.json). Only the cost watch, the handover log and the ledger run by themselves.
- 21 of the 54 numbered rule rows say "by hand" in their Check column (my count, guides/film-quality-rules.md). The rest name a tool, but nothing tallies, film after film, whether it ran or what it caught. That means CLAUDE.md's "remove a step only if it caught nothing in three films" has no data to act on.
- A rule is judged only by the chat that writes it. The critic found 8 faults in a "pillar" rule, but only after Sam asked (problem file).

## Approaches weighed
1. **One-off expert audit** of every rule by fresh critics. This finds badly written rules but measures neither use nor effect, and it decays.
2. **Turn every rule into code** (hooks and gates) and delete the prose. This fixes "followed", but not "helps".
3. **Controlled replays**, re-running past rounds with and without a rule. This is strong evidence for one rule but far too dear for about 170 items.
4. **A scorecard read from the record, with enforcement where the record shows skipping.** Use and catches come from transcripts and check files. Effect comes from tracing every one of Sam's notes back to the check that should have caught it. **Chosen:** it is the only one that answers both questions for every item, automatically.

## Proposal
**What it is.** Each rule and tool gets two short lines.
- **Signature:** what shows in a transcript when it is used (a command, a file written, a notes line).
- **Expected:** which stage or event calls for it.

`ledger.py auto` (the Stop hook, which already reads the transcript for free) records for each turn what was expected and what ran. `ledger.record` already saves every check's result into round files, so catches get tallied per check. Notes and repeats are counted from `notes/ledger/sam/` and the notes table, never typed in.

For each of Sam's notes, `handover.py start` makes the next chat name the rule or check that should have caught it, or "none exists". That is stored as a miss.

**How it is enforced.**
- When something expected is skipped and its use can be seen at the moment it happens, a new PreToolUse hook steers the chat to the tool. Example: grep/sed on film code in a notes round → "use page.py FILM find".
- Otherwise, `handover.py end` exits with a fault.
- A new rule or tool without a signature is refused. No chat has to choose to comply.

**Back-filled first** over the whole chats of Protest Tiers and the last two films, so the baseline is real.

**The decision, at each film's end:** one page lists every item with expected / ran / caught / missed notes.
- Needed but skipped → made automatic.
- Missed notes → its check is improved.
- Caught nothing in three films → a "Lost:" line for Sam's Y.

**Number to beat.** Protest Tiers' baseline from the back-fill: notes per round, repeated notes, notes a named check should have caught, and real cost (51.27% so far, ledger). It is measured on the next film's scorecard, from app costs and the logged notes.

**Cost.** Building it plus the back-fill is about the size of past tool jobs (6.4-7.0% each, notes/ledger cost-diagnosis, budget-job, preflight-audit): about 8-12% of a week, once. After that it is near 0% per chat (scripts, not model reading), plus one line per note.

**What Sam would notice.** One page per film saying which rules work. Fewer repeated notes. Tools that get used. "Lost:" lines backed by numbers.

## Sam test
- Q1 Expert: yes. Measuring from logs and steering at the moment of action is standard practice for agent workflows. Asking agents to report on themselves is not.
- Q2 Best result: whole chats of the last two films plus this one, back-filled, not a sample.
- Q3 Comprehensive: no chat can comply on paper. Data comes from transcripts and files, skipping is blocked by hooks, and every note gets traced.
- Q4 Most intelligent: four different approaches weighed. Only this one measures both use and effect.
- Q5 Risk: an over-broad hook could block real work. Each hook says why it blocked and can be removed. Lost lines still need Sam's Y.
- Q6 Checked: sources named. Cost range is an estimate (Unchecked).
- Q7 Not cheap: it covers every item and the back-fill. It is not a sample or a one-off audit.
- Q8 Nothing temporary: permanent hooks and records, reviewed when Sam declares each film complete.

## Lost / Added
Added: one PreToolUse hook; signature and expected lines on about 170 items; a per-film scorecard page; a "which check should have caught this" line for each note.
Lost: hand-typed `--notes`/`--repeat` (replaced by counts). Grep/sed on film code in notes rounds (steered to page.py).

## Unchecked
Item counts (54 numbered rows found; about 115 tools claimed). Whether old transcripts are on disk or need list_events for the back-fill. Which model the three "sonnet" chats really ran on. The cost range. The "After the film" ledger line (33.55%) disagrees with 51.27% spent; cause not traced.
