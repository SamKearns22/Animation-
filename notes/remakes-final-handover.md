# Remakes: the final render (handover to paste into a new chat)

**Model: Sonnet, medium effort.** Animation- project selected; first merge origin/claude/create-claude-md-oe8z4g.

**Sam's clear yes (11 Nov):** the final render, with the new subtitles and every fix in. **No check sheets.** The
checks still run (rule 59): every fault fixed or named first.

**In the film already (on the main line):** the barrel fix (Link runs round the barrels, camp check), the stone-wall
thump (full on the first push, softer on the re-slams), the captions in Montserrat Black with outline and shadow.

**Do, in order:**
1. `python3 source/remakes.py check`, then pre-flight (the "Checks and animatic" pack in guides/job-packs.md); faults
   already named are in notes/remakes.md (render with `--faults-named`; say any NEW fault to Sam before sending).
2. Full-size clean render in the background: `python3 source/remakes.py final source/data/remakes-clean-final.mp4
   --faults-named` (no --small). Say how long it will take; one wait, push notification when done.
3. Finish: `python3 source/finish.py source/data/remakes-clean-final.mp4 SCRATCH/remakes-finished.mp4 --film remakes
   --faults-named --signoff-speed 1.136` (1.136 so the sign-off is 1.6 s AFTER the 1.1x step below).
4. 1.1x (rule 70, pitch kept): `ffmpeg -i SCRATCH/remakes-finished.mp4 -filter_complex
   "[0:v]setpts=PTS/1.1,fps=24[v];[0:a]atempo=1.1[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset slow -c:a aac
   -b:a 160k -movflags +faststart animations/remakes-vertical.mp4`. Then measure: sign-off about 1.6 s; the Hook Text
   pops at 0.45 s (named, not a fault: the tool job builds 1.1x into finish.py so it lands at 0.5 s); the shortest
   caption still at least 0.8 s / 1.1 (name it if not).
5. Watch and listen once (frames sheet for yourself only, not sent), size under 50 MB, send the file to Sam with its
   size, length and render time. Commit `animations/remakes-vertical.mp4`, update Where things stand and
   story/status.md, push to the main line and the chat's branch.

**Next after it:** wait for Sam to say it's posted (then the film's notes go to the archive).
