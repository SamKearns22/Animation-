# The chat's own idea (written before the helpers run)
1. Split every notes round at one fixed seam: the Opus chat ends when the code fixes are made and committed (with the
   clip command lines written into the notes); a Sonnet chat renders the clips, splices, runs finish.py and sends.
2. The check moves from words to facts: at `handover.py end`, read the Next line AND the create_session call the chat
   is about to make (its model field), and refuse when routine words (render, splice, finish.py, send, file, sound
   placement) go to Opus or fix/build words go to Sonnet. Add "splice", "--span render", "sound" to the routine list.
3. A start check: `handover.py start` compares get_session's served model with the stage the notes name; on a
   mismatch it prints "wrong model: open the right chat" before any work.
Cost: ~1% of a week to build; saves an estimated 2-4% a film (4-6 routine Opus chats moved to Sonnet).
