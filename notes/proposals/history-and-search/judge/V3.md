# The chat's own idea (written before the helpers ran)

Root cause: tools reach a chat only as text it may ignore, and nothing limits what one step pulls into history.
Telling chats to use page.py (pack, rule 61, handover start line) has failed three times; only a refusal at the
moment of the search changes behaviour, and only a count proves it.

1. A PreToolUse hook (new, `.claude/hooks/codelook.py`) on Grep, Read and Bash:
   - A Grep, a whole-file Read, or a grep/sed/awk/cat of a film file (source/FILM*.py) before this chat has run
     `page.py FILM show` once is refused, with the exact show command for the film in the reply. After a show, a
     Read with offset/limit up to 80 lines, or a `sed -n A,Bp` of up to 80 lines, passes (reading the lines show
     pointed to). A whole-file Read of any .py over 300 lines is refused at any time (offset/limit instead).
   - Shared tools: `page.py tools show "words"` over the MAP headers of source/*.py (each tool's MAP already
     exists), so the same one step finds tool code too; the hook points there for source/ files that are not a film's.
   - Escape: `# codelook: ok <reason>` in the command, logged, so a miss never blocks work.
2. Every chat's counts written automatically into its ledger row by the Stop hook: steps, page.py runs, hand
   searches, refusals, escapes, history at end. Free; makes the effect visible at the end-of-film review.
3. Not now (separate yes, after 2 has numbers): handing over earlier (amber at 150k instead of 200k), since shorter
   chats pay less re-reading but each new chat pays its ~80k start-up again; the trade needs the counts first.

Number to beat: hand searches from 30% of steps to under 10% in the next film's round chats; median round chat
history at end under 200k; round chat cost below Protest Tiers' 1.3-3.2% of a week. Cost to build: ~1% of a week
(one Opus medium chat with tests replayed on two old commands lists). Undo: remove one hook line in settings.json.
Risk: a wrong refusal slows a chat for one step (escape exists); show missing the code (then `find`, then escape).
