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
