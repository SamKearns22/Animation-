# MidTerminal handovers

## Where things stand
- **Rules that bite next:** 27 (bleep both swears, from the sound), 38/68 (front on, no three-quarters), 11 (shot list below is the approved staging)
- **Done (4 Nov, Opus):** cast, set, key shots approved; rules 68, 27 written. Moving parts built and passed by Sam after 5 test clips (door into the room with thickness, hiding Trump till it opens; cut on the slam; Trump in from frame RIGHT, front-on, pointing; Satan float; ghost with upward flames on an ember bed; skin melting over a head-sized house-style skull). Notes 22-28 in the checklist.
- **Spent against the estimate (rule 55):** cap 10% (stop at 84% on Sam's meter; 74% at the brief). Plan 9%; moves about 4%: ask Sam for his meter at the start of the build.
- **Next:** the film file from `source/satire_template.py` once Sam's recordings arrive (Opus, medium effort). New chat, type: "MidTerminal: build the film from the handover in notes/midterminal.md".
- **Needs Sam:** the lines (shot list 1-10), the door slam and a gentle fire sound, as voice memos in the chat.
- **Read:** guides/satire.md 'Start', 'Movement', 'Before every render'; notes/midterminal.md (this file).
- **Lost / Added:** Added: our own simplified seal; generic portraits; a door slam and a gentle fire sound (Sam's files); a cream corridor with a red runner seen through the door.
- **Open rule requests:** none.
- **For Claude:** cast `source/midterminal_cast.py`; set `source/midterminal_set.py` (`render`, `put(lift=)`, `ghost()`, `to_cam`, `COMP`, shot 4 camera moved for Epstein on the left); moves `source/midterminal_moves.py` (`door_items(door_curve(t,...))`, `trump_item(t, d, sp)` with `path_length()`, `satan_item`, `epstein_item(t, sp, fade, melt)`, `test_timeline`, `ENTRY`, `SLAM`/`CUT`: line 2 starts on CUT). Still to build in the film: shrug, point, chuckle, Epstein's silly-ghost arm wave, Trump's mocking line 10.

## Where things stand
- **Rules that bite next:** 27 (bleep both swears, from the sound), 62 (subtitles readable: re-time from the takes), 14 (check sheet, then Sam's yes, before the animatic)
- **Done (4 Nov, Opus, build):** the film file, every shot drawn with estimated timings (shrug, point, chuckle, zoom out, ghost wave, melt, mock); quick pre-flight clean except 6 subtitle speeds (estimates). Meter 77% at the start (stop 84%).
- **Next:** file Sam's takes (lines 1-5, 7-10, slam, fire) as `source/audio/midterminal-N.m4a`, place both bleeps from the sound, set line 10's `mock_end`, quick pre-flight, check sheet with the Hook Text frame, wait for Sam's yes, animatic (Opus, medium; same chat if short, else type: "MidTerminal: time the film to my recordings, from the handover in notes/midterminal.md").
- **Needs Sam:** the recordings (2:30-3 pm, 4 Nov).
- **Read:** guides/satire.md 'Before every render', 'Render'.
- **Lost / Added:** Added: Trump's hands on hips through line 8; the door opens later if line 1 runs long (his voice heard through it first).
- **Open rule requests:** none.
- **For Claude:** `source/midterminal.py` (MAP at the top): LINES est -> takes; timeline T; CAMS adds 'satan', 'trump' singles; PORTAL_OK and THREE_QUARTER_OK reasons; previous handover in notes/archive/midterminal-handovers.md.

## Where things stand
- **Rules that bite next:** 27 (bleep both swears, from the sound), 56 (a fault of its kind: every point hand, every U-shaped arm pose, every ghost layer), 14 (check sheet and Sam's yes before the animatic)
- **Done (4 Nov, Opus):** film built; test animatic (silent, est timings) sent; Sam's notes 31-43 logged (Notes table); proposals for 35, 40, 42 and the skeleton question sent to Sam.
- **Next:** a round of notes (Opus, medium): Sam's answers, then fix 31-43, clips for the moves, file his recordings when they come (lines 1-5, 7-10, slam, fire), bleeps, check sheet, animatic. New chat, type: "MidTerminal: notes 31-43 from the handover in notes/midterminal.md" plus the answers.
- **Needs Sam:** answers 1-5 (sent 4 Nov), his meter, the recordings (2:30-3 pm).
- **Read:** guides/satire.md 'Movement', 'Before every render'; guides/kit-catalogue.md 'Effects' (burst, smoke, flash).
- **Lost / Added:** Added: camera flashes, a corridor in depth, the burst of flames and smoke, flames on Epstein, a skeleton under the melt (all Sam's). Lost: the zoom out (Sam).
- **Open rule requests:** "when a character points, give him a pointing finger" (note 33): proposed to Sam as a rule.
- **For Claude:** `source/midterminal.py` (MAP); audit artefact: audits() takes int(a*FPS), the frame before each cut: start at ceil. Point hand: MV._install_point_finger. Skull: MV.epstein_item draws `under` straight onto im (not through MS.ghost). Pocket square: check V.snap around 13.58 (Satan's yaw in the 'two'/'three' blend). Shrug: replace moves.pose 'shrug' arm targets (U shape) with shoulders up.


## Where things stand (4 Nov, before the notes 31-43 round)
- **Rules that bite next:** 56 (a fault of its kind: every point hand, every U-shaped arm pose, every ghost layer), 27 (bleep both swears, from the sound), 14 (check sheet and Sam's yes before the animatic)
- **Done (4 Nov):** film built; test animatic (silent, estimated timings) sent; Sam's notes 31-43 logged in the Notes table; his answers in (below); meter 78% (stop 84%).
- **Sam's answers:** note 35 = palms flung up and out on "Yeah, because Bibi told me to", lean in and jab twice on "I thought he was one of yours!?" (yes). Note 40 = narrow eyes on "I know it's you", NO finger wag, arms folded with a smug sneer on "reflecting pool". Note 42 = Trump copies Epstein's silly ghost wave, smaller and floppier, pout, raised brows, head waggling (yes). Skeleton: no reference, draw from standard anatomy in the house style (yes).
- **Next:** Opus, medium effort, one chat: fix notes 31-43, short clips for the moves (`final OUT --small --span T0 T1`: shrug, breath-and-point, flame burst, melt), then file Sam's recordings when they arrive, place the bleeps, full pre-flight, check sheet, wait for Sam's yes. New chat, type: "MidTerminal: notes 31-43 from the handover in notes/midterminal.md".
- **Needs Sam:** the recordings (lines 1-5, 7-10, door slam, gentle fire sound), 2:30-3 pm 4 Nov; a clear Y/N that "T" meant Y on the pointing-finger rule.
- **Read:** guides/satire.md 'Movement', 'Before every render'; guides/kit-catalogue.md 'Effects' (burst, smoke, flash); only the lines each note touches in `source/midterminal*.py`.
- **Lost / Added:** Lost: the zoom out (note 38). Added (Sam's): a corridor in depth, camera flashes, flames and smoke on Epstein's entrance, flames on his body, a burning skeleton under the melt, Trump's breath and arm gestures.
- **Open rule requests:** "when anyone points, the hand shows a pointing finger" (note 33; Sam's 5th answer came as "T", read as Y, ask once to confirm, then write it in the rulebook with its check and list it in the last table).
- **For Claude:** film `source/midterminal.py` (MAP at top); audit "pops" at 2.17, 14.50, 15.58, 30.25 are the frame before each cut (audits() uses int(a*FPS); start at ceil). Point hand: `MV._install_point_finger`, `MV.point_at`. Skull: `MV.epstein_item` draws `under` straight on `im`, not through `MS.ghost`; its head box is measured with arms down. Pocket square: check `V.snap` near 13.58. Shrug: `moves.pose 'shrug'` U-shape; the film's `satan_j`. Door/corridor: `MV.door_open`, `CORRIDOR`. Wings: `MC.wings`. Flag and books: `midterminal_set.py`. Quick pre-flight: `python3 source/preflight.py midterminal OUT --text`.


## Where things stand (4 Nov, animatic 1 sent)
- **Rules that bite next:** 14 (check sheet and Sam's yes before every animatic), 27 (bleeps from the sound), 59 (pre-flight before every render; `--faults-named`)
- **Done (4 Nov):** notes 31-43 fixed; Sam's takes filed (his 6 = line 7 ... 9 + 10 = line 10), his wording, bleeps, door slam, fire breath; Q1 Trump cutaway; voiced animatic sent (60.6 s, 7.4 MB, Hook Text and sign-off).
- **Next:** Sam's notes on the animatic: a new round, Opus medium, this chat if short; then his yes for the final.
- **Needs Sam:** notes or a yes on the animatic; Q3: he checks the subtitles of lines 4, 7, 10 against his takes.
- **Read:** guides/satire.md 'Before every render'; only the lines a note touches in `source/midterminal*.py`.
- **Lost / Added:** Lost: the zoom out (38); line 2 no longer on the cut (32); the gentle fire bed (fire breath instead). Added: corridor, flashes, breath, burst and smoke, body flames, burning skeleton, end two-shot, Trump cutaway.
- **Open rule requests:** none.
- **For Claude:** named faults (on the stamp): syllable counts on lines 4, 7, 9 (wail), 10; two quick captions; Epstein shot 42.6-50.9 is 8.3 s. Animatic clean render `source/data/midterminal/animatic-clean.mp4` (small, upscaled; gitignored). Cutaway `T['away'/'back']`. Timeline helpers `word_at` (snaps to stretches), `jab`, `lift_shoulders`, `CLEAR`.


## Where things stand
- **Rules that bite next:** 36 note (a cut waits for the subtitle to clear, with note 47's halved gaps), 14 (check sheet and Sam's yes before the animatic), 59 (pre-flight before every render)
- **Done (4 Nov):** voiced animatic 1 sent (60.6 s); Sam's notes 44-50 logged in the Notes table with the planned fixes (no questions open).
- **Next:** Opus, medium effort, new chat: fix notes 44-50, clips for the moves (walk-in point, eye roll, Satan's cut), full pre-flight, check sheet with the Hook Text frame, wait for Sam's yes, animatic 2. Type: "MidTerminal: notes 44-50 from the handover in notes/midterminal.md".
- **Needs Sam:** nothing until the clips.
- **Read:** only the lines each note touches in `source/midterminal*.py` (MAP at the top of each); guides/satire.md 'Before every render'.
- **Lost / Added:** Lost (Sam's notes): the stop and breath (32), the smug fold (40), the end two-shot with the jab and flinch (43).
- **Open rule requests:** none.
- **For Claude:** timeline T in midterminal.py ~100 (CLEAR, T['stop'/'angry'], cut11/flinch to remove); trump_sp/trump_j (word_at, jab, lift_shoulders); satan_sp/satan_j (flinch block to re-use for the end single); wings `midterminal_cast._wing` (scale s); captions tail in `subtitles.line_caption`/caption_at (0.45). Animatic clean `source/data/midterminal/animatic-clean.mp4` (small, upscaled to 1080 x 1920 before finish.py, which needs full size).

