# The chat's own idea (written before the helpers)
Rewrite rule 17: "Anything nearer the camera hides whatever is behind it: people, props, cars, effects and parts of the
set, in every shot, practice clips included. The only overlaps allowed are ones the scene means (a hand holding
something, someone inside a car, see-through glass or smoke), each listed in that film's file with a reason. The check
compares every object with every other, never just certain kinds."
Build: widen viewchecks.hide_faults from effects-vs-figures to every listed object pair (a film/rehearsal lists its
objects with position and size; the check redraws without the far object and compares); rehearsal files give the same
lists (scene(t), objects with switches); an ALLOWED list of (a, b, reason) per film. Run on both GTA rehearsal clips;
expect the shot 2 hydrant flagged; fix by depth-sorting the hydrant with the cars. Lost: the narrow rule 17. Added: about
a minute per clip, and each film's short allowed list.
