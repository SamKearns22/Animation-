# Chat 8's own idea (written before the helpers ran)

Change `show` in source/page.py, one change, four parts, each aimed at one kind of miss:

1. **Module-level code on the page.** build() also lists every top-level assignment (NAME = ..., X['key'] = ...,
   P4.TUNE['brand'] = dict(...)) with its line, its target name and the keyword/dict keys and string words it holds
   (chin_long, shall). find() then scores these like defs. A table that spans many lines is listed once with its keys.
2. **The line, not the head.** When the best def is too long to show whole, show its first 3 lines plus the lines
   that hold the note's words, ranked by how many words each holds, with face/body synonyms folded (chin -> chin_long,
   ears -> ears_hidden by splitting names on _), so a one-line setting deep in a function surfaces.
3. **The shot as a word.** `show` takes `--shot NAME` and `--at SECONDS` (the round chat always knows both from the
   notes table). The shot name is added to the note's words; with --at, the shot is looked up from the film's T/shot
   table. Lines and defs naming the shot (def dock, `if shot in ('dock', ...)`, VIEW['dock']) score as if the note
   named them.
4. **New code.** When the best hit is weak (score under a threshold), say so and show where the nearest shot's code
   lives (its draw branch and its staging entry), so the chat adds the new code beside it rather than searching.

Replay: feed the shot and time from the notes table (as a round chat would), keep the target words fixed; aim >= 80%
strict and loose. Lost: nothing (old calls still work). Added: one flag the round chat passes per note.
