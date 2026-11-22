# The chat's own idea (written before the helpers)

Facts seen: memory lapses (the app forgets a chat's cached history after about an hour idle, so the next step
re-pays the whole history at the write price) cost 3.11% of a week on GTA, in 8 chats. They come from long waits:
renders, Sam replying hours later, and chats resumed rather than handed over.

Idea: (1) before any wait expected over 50 minutes (a long render, a question to Sam at night), the chat writes its
handover first, so the answer lands in a small fresh chat, not a big stale one; (2) when Sam's answer comes back to
a chat that has gone cold and is over about 120k words, it hands over at once (CLAUDE.md already says this at amber
or red; extend it to any cold big chat); (3) the ledger names each lapse with its cause (render wait / Sam's reply),
so the next film shows which kind was cut.
Lost: nothing on screen; Sam's answer may go to a new chat rather than the one that asked. Added: a handover before long waits.
