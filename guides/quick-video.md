# Quick video (about 5% of a week). Read only this page: nothing else is needed.

For a short TikTok film with two people talking, made by `source/quick.py` from one brief file. It already uses
the series' look (flat shapes, black outlines, plain circle hands), Sam's recordings, the standard title and
captions, and the pre-flight checks. **Do not open** `burnham.py`, `russiadent.py`, `patriots2.py` or other guides.

## 1. Ask Sam, in ONE message (skip what he already sent; pick the rest yourself and say what you chose)
- The script: who says what (A or B), the exact words, short lines (a caption is at most 2 rows of 42 characters).
- His recordings, one file per line, saved as `source/audio/NAME-1.m4a`, `NAME-2.m4a`... in script order.
- Title (1-3 words, never gives the joke away), background (`room cafe office street` or a colour `#88aadd`).
- For A and B: skin (`pale pink olive brown deep`), hair (`crop side bald bob long swept wisps blonde`), hair and
  jacket colours, outfit (`suit jumper dress blouse`), glasses yes/no.
- Any gag: a face (`angry shock happy`), a gesture (`point shrug wave hips talk`), a sound (`thud ding whoosh bang`).
Estimate the length (words / 3.3 a second, plus pauses) and say plainly if it will pass 30 s. First payoff by 8-10 s.

## 2. Steps (maximum: one sheet, one final; no animatic, no storyboard)
1. Copy `prompts/quick-example.json` to `prompts/NAME.json` and change the values (the `_help` line lists every
   option). Give each line a `start` in seconds; its end comes from the recording. Leave `"end": "end"` on the last shot.
2. `python3 source/quick.py check prompts/NAME.json` (2 seconds). Fix every FAIL (table below), run it again.
3. `python3 source/quick.py sheet prompts/NAME.json /tmp/sheet` (about 3 s per second of film). It checks every
   body (arms, legs, hands) and makes ONE contact sheet, `/tmp/sheet/quick-preflight.jpg`, with the safe area
   drawn on. It must say `0 problem(s)`. Look at the sheet once; if it is wrong, fix the brief and run step 3 again.
4. Tell Sam what you chose and the render time (about 3 minutes per 20 s of film); get his notes in ONE message and
   apply them all at once.
5. `python3 source/quick.py final prompts/NAME.json animations/NAME-vertical.mp4` in the background; send a push
   notification when it ends. Check `ls -l`: 1-4 MB expected, never over 8 MB.
6. Send the file in the chat, suggest a cover (the frame at 0:00.5), add 3 lines to `story/status.md`, and commit
   only the video, the brief and the recordings. Sam writes the post text himself.
Test any change cheaply first: `final ... /tmp/t.mp4 --scale 0.5 --secs 3` (10 seconds).

## 3. If a check fails
| Message | Fix |
|---|---|
| `starts before line N ends` | Move its `start` just after line N's end time (printed by `check`). |
| `caption has ... rows` | Shorten the text, or split it into two lines at a pause. |
| `recording not found` | The file must be in `source/audio/`; ask Sam once. |
| `same take` | Two files are the same recording: ask Sam which is right. |
| `head leaves the safe area` | Use a smaller `zoom` (1.6) on that shot. |
| `shots have a gap` / `shots end at` | Each shot starts where the last ended; the last has `"end": "end"`. |
| `first line starts at` | Make the first `start` 0.2. |
| `hand cannot reach` / `figure check` (sheet) | Change that line's `gesture` to `talk` or `rest`. |
| `too fast to read` (note) | Add 0.5 s before the next line. |
| `no recording` (note) | Fine only if Sam meant a silent line. |
If anything still fails twice, or the fault is inside `quick.py`, stop and tell Sam in plain words: do not rewrite it.

## Added 8 Oct: the Satire checks run here too
- The `sheet` step now also runs: mouths move for every phrase, the voice sits at least 6 dB above the effects, the
  subtitles printed as text (proofread them there), each person drawn alone over the whole film (in pieces, popping,
  stretching, frozen), and the eyelines (A and B look at each other). It must still say `0 problem(s)`.
- Backgrounds are drawn in Satire style (hand-cut corners, flat colour); listeners sway slightly (never frozen).
- After a caption or timing note: `final ... --reuse` (no pictures re-rendered, about a minute).
| Message | Fix |
|---|---|
| `frozen` | Give that line a `gesture` or a `react` face. |
| `only N dB above the rest` | Lower that sound effect's `gain`. |
| `no mouth movement` | The recording and the text don't match: ask Sam. |

