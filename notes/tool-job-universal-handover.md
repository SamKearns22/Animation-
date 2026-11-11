# Tool job: make the 11 Nov rules hold for every film (handover to paste into a new chat)

**Model: Opus, high effort.** Animation- project selected; first merge origin/claude/create-claude-md-oe8z4g.
**Rule 86:** this is a tool job with its own estimate, outside any film's budget. **Send Sam the estimate first and
build nothing until his yes.** Sam has said Y to the job itself (11 Nov).

**The rules (written 11 Nov, guides/film-quality-rules.md):** 62 (captions: Remakes style for every film), 70
(1.1x delivery), 75 (Hook Text planned at the first animatic, covers nothing important, pops at 0.5 s), S5 (eyes on
every cast). S6 retired.

**The job, each piece with its check:**
1. Captions: the Remakes style (Montserrat Black, white, black outline and shadow, at most 5 words a piece, never
   joined; `remakes.draw_subtitle` and `_pieces`) becomes the kit default (subtitles.py / finish.py), the template
   uses it; finish.py refuses a film with no captions (no more opt-in SUBTITLES_AT_FINISH); finished films untouched.
2. 1.1x in finish.py, pitch kept, after captions; the sign-off still 1.6 s and the Hook Text pop still 0.5 s on the
   delivered file; the caption readability check run at 1.1x. A kittest for each.
3. Hook Text: finish.py/hookcheck refuses a film with HOOK but no KEEP_CLEAR (today it skips quietly); preflight
   names the Hook Text plan as an animatic gate.
4. S5: KG's owl eye (remakes_creatures `_kg_eye`) cut to its outline; a kit eye helper every new cast uses, and a
   critique line.
5. Rule 13: the camp check (`remakes.camp_paths`, `RS.SET_FEET`) moved into the shared kit (setcheck.py) as a
   moving-figure-against-the-set check any film with SET_BOXES gets; Remakes calls the kit.
6. Delete source/quick.py, prompts/quick-example.json and preflight's quick-video exception (guide already gone).
Run the kittests and `remakes.py check` at the end; Remakes' picture must not change (bar KG's eye).

## Estimate (11 Nov, sent to Sam; waiting for his Y, rule 86)
About 2.5% of a week, one build chat (Opus, medium: the plan above is clear), cap 3.5%.
Stages: captions 0.5, 1.1x 0.4, Hook Text 0.2, eyes 0.6, camp check 0.5, quick.py removal 0.1, kittests and
`remakes.py check` 0.2. Pieces 1, 2, 3 and 5 touch finish.py or remakes.py, so the build starts only once
animations/remakes-vertical.mp4 is on the main line. Sam's answer: Y (11 Nov, "override my yes, proceed").

## Where things stand (11 Nov, build chat)
- Rules that bite next: 86, 13, 85.
- Done (free pieces, pushed): 6 (quick.py, its example and preflight's exception gone; hutt and polanski take their
  hands and captions from satire_parts.py, frames identical); 4 (eyekit.py, KG's eye cut to the outline, house-style
  S5 check, critique P14; Remakes frames identical at 29 times); 3 (hookcheck refuses HOOK without KEEP_CLEAR,
  pre-flight's rule 75 gate); 5's kit half (setcheck.moving_faults, run by pre-flight on SET_FEET). Kittests all pass.
- Next: Opus, medium effort, this chat, once `git fetch` shows animations/remakes-vertical.mp4 on the main line:
  1 (captions default), 2 (1.1x), and Remakes' half of 5 (camp_paths calls setcheck.moving_faults; give remakes
  SET_FEET/movers/SET_CAM/MOVE_SPAN), then kittests and `remakes.py check`. One send_later check is set.
- Needs Sam: a look at the KG eye sheet (review/kg-eye-sheet.png, sent in chat) at the end.
- Read: job-packs "A tool job"; this file; source/kittests.py (new tests: eyes_cut_to_the_outline,
  hook_text_planned, moving_figures_against_the_set).
- Open rule requests: none.
- For Claude: ledger name tool-job-universal-handover.
