# The chat's own idea (chat 3, written before the helpers)

Three separate changes, asked as three numbered Y/Ns, in this order (cheapest and safest first):

1. Branch step by tool (~0.5% a film): setup.sh (already fetching) prints only branches with a commit not on the main
   line made since the main line's last handover commit (or the last 2 days), at most ~8 lines, each with its age and
   the film or tool files it touches; CLAUDE.md's "list every branch" line points to it, the merge rule unchanged.
   Check: at film end, the full listing is compared with what was printed; any newer work missed fails it.
   Lost: the full 254-line branch list at start (still one command away). Added: a short list printed by the hook.

2. Start printout of the notes (~0.7% a film): `handover.py start --film NAME` prints the film notes' "Where things
   stand" and the open notes (rows not ticked) only, capped at ~60 lines; the pack says read only what it names.
   A chat reads more only when a note or fault names a section. Check: the start's existing carried() test still runs
   against the whole notes file, so no open note is missed. Lost: chats skimming the notes' headings by habit.
   Added: one printout.

3. CLAUDE.md layered (~0.6% a film), last and guarded: dated tags and "replaces/was" histories move to the rulebook's
   last table / notes/archive/claude-md-history.md; rarely used parts (My accounts, finish command, photo search
   order) move to the pack sections that use them with a one-line pointer. Guards: a rule-sentence check (every rule
   sentence before is found after, word-matched) and a fresh helper answering 10 past situations with old and new,
   which must match. Built switched off as a candidate file first, shown, then asked.
   Lost: dates and histories in every chat (kept in the archive). Added: the sentence check and the situations test.

Optional: recompute the ledger's stale stored "33.55% ... 0.5x" line (53.56%, 0.8x).
