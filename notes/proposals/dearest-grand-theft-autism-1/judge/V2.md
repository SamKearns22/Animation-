# The chat's own idea (written before the helpers)

Facts seen: every GTA chat starts at a floor of 91-95k tokens before its first step (ledger 'start.floor_k'), and that
floor is 22-24% of a typical chat's bill (base_pct), re-read at every step. Only about 5k of it is this project's own
words (CLAUDE.md 15 KB, job-packs 6 KB); the rest is the app's system prompt, the tool list and the instructions of
connected services the films never use (web-automation, web-scrape and documents connectors add their tool lists
and long instructions to every chat), the skills list, and the start hooks' printouts.

Idea: (1) measure the floor's parts once in a chat (count the tokens of each block in a fresh transcript's first
request); (2) ask Sam to switch off, for this project only, the connectors no film stage uses (he can do it on the
phone in the app's connector settings), keeping any a stage names; (3) cut the start hooks' printouts to the faults
only (branches list, watcher lines) and keep CLAUDE.md's size under a fixed cap with a check; (4) measure the floor
again on the next chat: number to beat, floor under 70k.
Lost: nothing a film uses (connectors the films never call). Added: one plain step for Sam on the phone; a size check.
