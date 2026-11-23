# The chat's own idea (written before the helpers)
1. Sam's message containing the word Override (a whole word, any case) as its own word opens a one-ask pass: a small
   record (time, chat, film, Sam's words) in notes/logs/overrides.log, written by the UserPromptSubmit hook the moment
   he types it. It lasts until his next message.
2. Every guard (send guard, finish.py's route stop, the proposal Stop hook, handover check, cost watch) reads one shared
   function: "is there an Override from Sam in this chat newer than his last other message?" If yes it passes, prints
   "Checks: skipped by Override: <what>", and logs what it skipped.
3. Never skipped: Locked-by-Sam shots, deleting files/history, pushing to someone else's branch, secrets. Override skips
   checks, not Sam's own locks.
4. Kittest: replays chat 47 (send refused without, passes with a logged Override; a chat-written "override" without
   Sam typing it still refused, handover's OVERRIDE fault kept).
5. Locked by Sam: kept in the notes (guards later chats), removed from the bottom 3 lines and from every message to Sam;
   CLAUDE.md wording changed; message checker flags "Locked by Sam" in a reply.
