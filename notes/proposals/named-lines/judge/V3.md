# The chat's own version (written before the helpers ran)

1. One sitting now: list every line pre-flight named on Milburn and every red kit test, grouped by cause (about 10
   causes for the 61 lines).
2. Each cause gets "fix in the tool" (and is fixed, one at a time, each tested) or "drop under the three-films rule"
   (only if it caught nothing in Blessed, Milburn and one more film, each going to Sam as a Lost line).
3. From the next film: pre-flight shows named lines as a count and the new ones in full; an animatic is refused while
   more than 10 lines are named.
4. A red kit test blocks the handover unless a fix is under way in that chat.
Lost: a short job at the start of the next film. Added: a short list where a new fault stands out.
Other option: leave them and keep naming.

Merged from shared-check-fixes (its own version, written 19 Nov before helpers):
1. Move the cleaned-takes hand-over from milburn.py into the shared pre-flight, so every film hands its checks the
   cleaned voice takes with no film code.
2. Re-run pre-flight on Milburn's final code with the shared version: the 60 false lines stay gone.
3. Any check fix made in film code gets one line in the film's notes, "move to shared", and handover.py end flags any
   that are still open at the end of the film.
4. The end-of-film review lists them.
Lost: nothing. Added: fewer false lines on every film.
Other option: leave each fix in its film.
