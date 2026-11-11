# Remakes: trim the pace (handover to paste into a new chat)

**Model: Opus, medium effort.** Chat starts with the Animation- project selected; first merge origin/claude/create-claude-md-oe8z4g.

**Goal (Sam, 11 Nov):** make the Remakes animatic about 10% quicker (45 s to about 41 s) by trimming gaps and holds,
NOT by speeding the whole film (a plain 1.1x file was sent for comparison; its caption times get tight: "I don't think I"
is 0.9 s for 4 words already). Voices, subtitles and the action beats (snap, gate blast, Navi's strike, wall slams) must keep their
current speed and pitch.

**Do, in order:**
1. Read notes/remakes.md "Where things stand" and the MAP at the top of source/remakes.py (lines and timing: `_L` rows, the
   "gap before" column; shots and BEATS follow from the lines; PIECE_FIX holds line 13's subtitle times).
2. Trim, in this order of preference: (a) the gap before each line (now 0.15-0.6 s; cut 0.05-0.2 s each, never below 0.1 s,
   never touch the 0.25 s after the execution move: Sam's note 66); (b) long holds with nothing happening (the reaction shots S4, S6,
   S9, S11 and the end hold, DUR = last line + 0.7 s); (c) nothing inside a voice take, a bleep or an action beat.
3. Re-check what depends on time: PIECE_FIX (line 13) and any other fixed times, the bleep spans, the effects' ducking under the
   voices, R1/R2 flash times, caption lengths (rule 62; keep every caption at 0.9 s or more).
4. `python3 source/remakes.py check`, then clips of every trimmed join (`final OUT --small --span T0 T1`) and send them
   (no yes needed for clips).
5. Quick pre-flight `python3 source/preflight.py remakes OUT --text` (fix or name every fault; earlier named faults:
   syllable counter on "R1"/"9"/"Ok?", PROP TURN on Malon and Saria, critique round 3 pass 2 open).

**Needs Sam's yes before the animatic:** this changes timing he has approved, so send the clips and wait for his Y.
Then render animatic 4 (`final source/data/remakes-clean.mp4 --small`, then `finish.py ... --film remakes`), watch and listen once,
send it, and wait for his look. No final without his clear yes.

**Report in one line per change** ("gap before line 6: 0.25 s kept; line 9: 0.6 to 0.4 s") and any "Lost:" (anything
removed from what he has seen). Update the Where things stand handover (15 lines at most), story/status.md, commit and push to the
main line and the chat's own branch.
