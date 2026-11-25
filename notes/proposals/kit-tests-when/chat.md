# The chat's own idea (written before the helpers)

1. One shared list of what is "the film's own": handover.py's film prefixes plus story/, notes/, references/,
   animations/. Anything else changed since the last finished kit run on the main line is "shared".
2. Start-up hook: instead of always starting the run, start it only if the main line has shared changes since the last
   recorded green run (a stamp file notes/logs/kittests-stamp.txt holding the commit it ran on, pushed with the
   handover).
3. handover.py end: if this chat changed a shared file (net diff from where it started), it needs a finished run on
   its own final code (run it then, if the start-up run predates the change); if it changed only film files, no run and
   no wait: the gate says "kit tests skipped: film files only".
4. finish.py (animatic and final): refuses to start unless a green run is stamped on the current shared code; if not,
   it runs the kit tests first (about 15 min) and says so.
5. A kittest proves the three cases: film-only change skips, shared change demands a run, finish without a stamp refuses.
Lost: the start-up safety net that catches a fault already on the main line from another chat. Added: shorter chats,
no wait on film-only rounds; animatics and finals always on tested code.
