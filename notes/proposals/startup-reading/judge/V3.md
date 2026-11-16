# The chat's own idea (written before the helpers)

1. CLAUDE.md rewrite, same rules, ~1,300 words: drop dates and "replaces/was" histories (they move to
   notes/archive/claude-md-history.md); one rule per bullet in terse imperative wording; merge overlaps (the three
   places about fresh chats/handovers; "ask before" items); move rarely used parts (My accounts, YouTube, TikTok
   finish command details, reference-photo search order) to the packs that use them, leaving a one-line pointer.
   Rules a tool enforces (handover.py, propose.py hook, finish.py) become one line naming the tool.
2. Branch listing replaced by a quiet check: setup.sh (already fetching) prints only branches with commits newer
   than the main line that touch the film or tools, max ~5 lines; CLAUDE.md's "list every branch" becomes "read the
   setup note". Optionally Sam's Y to delete branches already merged.
3. Packs: trim each stage's named sections to a "must-know" summary at the top of each guide section (a few lines),
   detail below read only when a note or fault names it; critique-checklist's "Came from" marked skip.
4. Enforce notes under 4,000 words in handover.py end (it may already).
5. Test: a fresh helper given only the new CLAUDE.md answers 10 situations from past chats (e.g. "Sam says fix this
   before the final", "hold", a repeat note); must match what the old one gives. Measure the ~90k start footprint
   before and after on the next film's first chats.
Estimated saving: ~5-8k tokens per chat, ~2-3% of a week per film.
