## Leak
None.

## Root cause
A change counts as done once written or built; nothing makes chats use it or measures whether they did.
- Chat 31 was pointed to the "Notes round" pack (notes/protest-tiers.md), which says use `page.py` (guides/job-packs.md). Chats 29 and 31 still ran codemap/page 0 times and grep/sed 25 and 26 times (tool-use-29-31.md). Chat 29 was Opus (ledger).
- There is no `story/protest-tiers-page.md` (checked).
- Rule 61's check only warns. The film's files run to 2,283, 1,666 and 1,564 lines, and the MAP has no line numbers (source/protest_tiers*.py).
- The tools were "proven" by a kittest (kit-catalogue line 138). It proves the tool works, not that chats use it.
- .claude/settings.json has no PreToolUse hook. `propose.py hook` (a Stop hook) is not wired in either. Same failure.
- Proposals: nothing makes a first answer state its result target and how it will be enforced. It sizes itself by price and improves only under push (sam-to-case3.md, 19:45-19:51). "Weren't used" was said before any count existed (problem file).

## Approaches weighed
1. A written rule ("best first, use page.py"). Exists (pack, rule 61); failed.
2. Fresh helpers and a judge (propose.py). Better ideas, not tool use; its hook is unwired.
3. Always Opus high. Chat 29 was Opus.
4. **Chosen:** the harness enforces each change, and the transcripts measure it.

## Proposal
**"Wired, measured, or not done."** A rule, tool or check change counts only when:
- **(a) Wired:** runs where no chat chooses (a settings.json hook, or a step in handover.py, preflight or finish).
- **(b) Measured:** a number to beat, computed from transcripts and printed by `handover.py end` every chat.
- **(c) Reviewed:** against the film's results when it is complete (`propose.py review`).

`propose.py record` refuses any proposal without an "Enforced by: FILE, point" line and a "Measure: baseline → target" line. A check at session start fails if anything the catalogue marks "enforced" is missing from settings.json. It catches the unwired Stop hook.

Applied now:
1. **Code reading.** A PreToolUse hook on Bash and Read refuses a grep across a film file or a whole-file read of one. Its refusal gives the `page.py find` answer. Reads of 80 lines or fewer pass. A `# need: reason` suffix passes and is counted. `handover.py start` builds the page. Rule 61's warning becomes a fault for new files.
   - Number to beat: hand searches per chat, from 25 down to 3 or fewer.
2. **Proposals.** Wire the Stop hook. Each proposal opens with the version sized by the result it must deliver. Smaller versions only as "Lost:" lines. A claim about use cites a count.
   - Number to beat: Sam's pushes before his Y, counted at handover and by `propose.py mark replaced`. Baseline five in one chat (propose.py's note). Target 0.

**Cost:** about 2-3% of a week, once (one Opus tool job, about a chat 29/31's size: 2.57%, 2.36%, ledger). Hooks cost nothing unless they refuse. Hand looks were ~27-33% of their estimated cost (bills-29-31.md).

**Sam would notice:** a handover line like "Code looks by hand: 2 (target 3)"; proposals arrive full-sized with a number to beat.

## Sam test
- Q1: An expert enforces in the harness and measures adoption.
- Q2: Evidence: every call of two whole chats plus the wiring; the review covers the whole film.
- Q3: Hooks don't rely on reading; the measure shows whether it worked.
- Q4: Four different approaches were weighed. Rejected ones already fail.
- Q5: The hook could block real work: the `# need` suffix lets it through, and one settings.json line undoes it. Replayed on chats 29/31 before Sam's Y.
- Q6: Facts sourced; gaps below.
- Q7: Sized to enforce every change, not patch one.
- Q8: Permanent, and reviewed when the film is complete.

## Lost / Added
Lost: free grep and whole-file reads of film code (`# need` still allows them, counted).
Added: a PreToolUse hook, a start-up wiring check, two proposal lines, one handover line.

## Unchecked
- Chat 31's model (ledger: sonnet; title: Opus).
- The saving per round.
- Whether the Stop hook was wired after this tree was copied.
- When page.py was built relative to chats 29/31.
