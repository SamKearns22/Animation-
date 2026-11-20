# Proposal: Clipping checks: anything nearer the camera hides anything behind it, practice clips included

Status: open

## Problem
In Grand Theft Autism's swerve practice clip (shot 2), the police cars and the getaway car are drawn over a fire hydrant
that stands nearer the camera than they do, so they look as if they drive through it. Sam saw it; no check did. Sam
(20 Nov): "'Anything against anything' should be the rule across all clipping checks in this project, otherwise we will
always encounter the same problem every time we build any new prop or setting." Some overlaps are meant (a hand on a
held gun, people inside a car, see-through windscreen glass, smoke), so a check that compares everything will meet
deliberate overlaps as well as faults.

## Facts
- source/gta_rehearse.py shot2(): the hydrant is drawn with the street layer, before the cars, whatever the depth;
  shot 4 in the same file sorts hydrant, cars and props by distance (fx_items) and is correct.
- guides/film-quality-rules.md rule 17: "Every figure in front of an effect hides it." Check: viewchecks.hide_faults.
- source/viewchecks.py hide_faults (line ~296): needs film.effect_points and film.scene; compares effects against
  figures with a body or head only; redraws the frame with the effects switched off to confirm a cover. Returns []
  silently when a file has no effect_points/scene (as every rehearsal file has none).
- Rehearsal clips are sent under rule 8 before the moves stage; the shot 2 clip was sent in chat 5 with only the car
  sheet critiqued (notes/archive/grand-theft-autism-handovers.md, chat 5), and re-sent 20 Nov (this chat) for music.
- Sam asked to reuse the existing check, not build a new one (this chat, 20 Nov), and said Y to doing so.
- Other overlap-related checks (unchecked for scope): handcheck.py (hands meeting props, props hidden), kittests.

## Record
source/viewchecks.py
source/gta_rehearse.py
source/audit.py
source/handcheck.py
guides/film-quality-rules.md
notes/grand-theft-autism.md
notes/archive/grand-theft-autism-handovers.md
CLAUDE.md
