# Netan-Yahoo! old handovers

## Before planning (26 Oct)
## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **Done (26 Oct):** brief saved word for word; the kit checked for what can be reused. Nothing built, no pictures made, no render.
- **Next (stage, model, fresh chat):** PLANNING, Opus, high effort, new chat. Read this file, `prompts/netan-yahoo.md`,
  `guides/satire.md`, `guides/film-quality-rules.md`, `guides/kit-catalogue.md`. Send Sam the questions below in ONE message and
  ask for sound effects and references. Plan only; build nothing until Sam says go. Then BUILDING (new characters, new set,
  new effect): Opus, high effort, another fresh chat.
- **Already built (26 Oct, the Newsdesk building chat; merged from GitHub):** the Israeli news studio (`source/newsdesk_set.py`),
  the presenter (`newsdesk_cast.py`, `PRESENTER`), Netanyahu (`netanyahu_cast.py`), Darth Maul with the double-bladed lightsaber
  and four poses (`maul_cast.py`), the chairs (`newsdesk_props.py`). Details and Sam's photos: `notes/newsdesk.md`,
  `references/newsdesk/`, `references/maul/`. This film IS the Newsdesk film: the brief arrives here. NOT yet built: the
  leap-and-roll, the cuts (clean-sliced chunks), the lightsaber glow and cut effect, the hand-off of the presenter to "younger
  and more energetic" (a new variant of `PRESENTER`: say what changed), Hebrew screen text, sound.
- **Losses and my additions Sam should know about:** none yet. Proposed additions (Sam to say no): presenter glances at the
  camera (his, shot 4: kept); a studio "ON AIR" light and desk props; a stinger on the logo; steam hiss under the chunks.
- **Ambition estimate (rule 24-26, a guess to confirm at planning):** the people and set are built, so the cost is the action:
  a hard fast leap, roll and crouch, the slicing sequence with chunks, the saber effect, sound. About 12-18% of a week.
  Cheapest cuts: three strikes only, one wide shot for all the action, reuse the existing poses.
- **Rule requests and proposals not yet in a guide:** none in the brief or notes.
- **Files to open:** `prompts/netan-yahoo.md`, this file, `notes/newsdesk.md` (the built cast and set), `story/status.md` (Newsdesk section only).

## Planning, before building (26 Oct)
- **Done (26 Oct, planning chat, Opus):** questions sent in one message, all answered (below); sound effects and references
  asked for. "President" changed to "Prime Minister" in the brief and script (Sam). Nothing built, no pictures, no render.
- **Next:** wait for Sam's references and sounds (incoming). Then, still PLANNING in this chat: check the references
  (missing ones named), the plan in metres, the composition sheet (rule 11). Then BUILDING (presenter variant, leap-roll,
  cuts and pieces, saber glow, Hebrew screens, sound): Opus, high effort, fresh chat. Sam: "begin build once happy with
  references".
- **Already built (Newsdesk building chat):** the studio (`source/newsdesk_set.py`), the presenter (`newsdesk_cast.py`,
  `PRESENTER`), Netanyahu (`netanyahu_cast.py`), Maul with the double-bladed saber and four poses (`maul_cast.py`), the
  wooden armchairs (`newsdesk_props.py`). Details: `notes/newsdesk.md`. Sam has no notes on the Maul sheet.
- **Losses and my additions Sam should know about:** additions he approved: leap and landing thump, pieces hitting the
  floor, chair creak, steam hiss (sounds; my code); the steam wisps; the hood falling back in the roll. Set dressing: NONE
  (Sam: the real sets are very clean); no ON AIR light, no desk props, no news sting, no studio ambience.
- **Ambition estimate (rule 24, estimate):** cast and set built; the cost is the action. About 12-18% of a week. Sam took
  no trims.
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** `prompts/netan-yahoo.md`, this file, `notes/newsdesk.md`, `story/status.md` (Newsdesk section only).



# Handover replaced 26 Oct (building chat)
## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **Done (26 Oct, planning chat, Opus):** all questions answered ("Sam's answers" below); references packs 1-5 in
  (Maul movement, wounds, debate layout, Netanyahu faces; the cat dropped; the presenter left to me); the plan in metres
  and three versions of the composition sheet (`source/netan_yahoo_comp.py`); Sam: "let's build". "President" is
  "Prime Minister" everywhere. Nothing built yet.
- **Next: BUILDING, Opus high effort, fresh chat.** In order: (1) start `source/netan_yahoo.py` from
  `source/satire_template.py` with the PLAN, cameras, `SHOT_CAST`, `BENCHMARK` from the plan below; (2) the younger
  presenter (answer 2: a `PRESENTER` variant, say what changed); (3) eye direction (`sp['look']`) on the Netanyahu and
  Maul heads; Netanyahu's surprised and impressed faces (pack 5) and a 1-6 strength sheet; (4) remove the chairs' blue pools in the set (`newsdesk_props.pool`, Sam); the big Hebrew screen
  caption 'עימות לראשות הממשלה 2026' and the hook "Israeli Prime Ministerial Debate"; (5) Maul's moves from pack 1: ready
  stance, ignition, leap-flip (hood falls back), crouch landing, three strikes and follow-through, spring onto the chair,
  territorial crouch with head snaps (answer 11); (6) the cuts: flare, sparks, flat smoke, orange rims cooling, four
  pieces falling into a pile, steam (answers 8-9, pack 2; no blood); the presenter's reactions (hands up, then the arch);
  (7) the saber glow (answer 10). Then the cast sheet; then, motion-led, early clips of the risky moves (rule 8): the
  leap-flip and landing, the three strikes and pieces, the spring onto the chair.
- **FIXED (building chat, 26 Oct): the chairs and the desk.** Cause, measured: every chair (round, reach 0.345 m)
  sat 1.75 m from the disc's centre, only 0.06 m inside the desk's inner edge, so at phone size it read as touching;
  all three chairs, not just Netanyahu's. Fix: all three people 0.1 m nearer the disc's centre (1.05 m); every chair
  now 0.15 m clear (rule: 0.1 m). The plan now lives in `source/netan_yahoo_plan.py` (sheet and film read the same
  numbers): the desk is 24 solid blocks, the chairs round solids with `clear=0.1`; `plan.py` now measures true gaps and
  catches the old spots (checked). The desk draws in 12-degree pieces, each sorted on its own (`newsdesk_set.desk_items`),
  so the sheet's draw-order cheat is gone. Kit fix found on the way: the collision audit turned angled things the
  wrong way (mirrored, `sets._thing_solid`). Sheet v7 sent; waiting for Sam's look.
- **Waiting on Sam:** the saber sounds (ignition, hum, three swings, a sizzle per cut; kept OFF GitHub); the recordings
  (later today; "Prime Minister" in the line; "shit" said in full, S heard, rest bleeped).
- **Already built:** studio `source/newsdesk_set.py`, presenter `newsdesk_cast.py`, Netanyahu `netanyahu_cast.py`, Maul
  `maul_cast.py` (saberstaff, 4 poses), chairs `newsdesk_props.py`. Reuse: sparks, flat smoke, steam (`prepper_fx.py`),
  falling pieces (Poker Mon's `launch`), lying pieces (`lying.py`).
- **Watch out:** this planning session could not install `numba` (pypi.org blocked), which `lying.py` needs. If the
  building chat hits it, Sam can allow pypi.org in claude.ai Settings, Capabilities.
- **Losses and my additions Sam should know about:** everyone 0.1 m nearer the disc's centre (the chair fix; Maul's leap about 0.1 m shorter); the horseshoe from his sketch (the photo's straight line dropped); chairs angled to centre-audience; blue pools removed; the flip is
  mostly upwards (about 1 m of travel); shot 4 is now front-left, so the presenter is nearest (the photo had the right end
  nearer); Netanyahu leaves the frame during shot 4's push-in. Additions he approved: thump, pieces landing, chair creak,
  steam hiss (sounds, my code), sparks and smoke at the cuts, steam wisps, hood falling back. No set dressing.
- **Ambition estimate (rule 24, estimate):** about 12-18% of a week; the action is the cost.
- **Rule requests and proposals not yet in a guide:** none.
- **Files to open:** this file, `prompts/netan-yahoo.md`, `notes/newsdesk.md` (the built cast and set),
  `guides/satire.md`, `guides/film-quality-rules.md`, `guides/figure-rig.md`, `story/status.md` (Newsdesk section only).

