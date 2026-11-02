# The Yuletide horror trailer: lessons (moved out of best-practice.md, 2 Nov)

Read with `guides/yuletide/yuletide-trailer.md`, which says how the next round starts.

# Part 4. The Yuletide horror trailer (3D world drawn in graphite)
The guides for this project are `tone.md`, `character-anatomy.md`, `movement.md` and `pipeline.md`, and
they apply to this project:
- the A24 craft (dread over shock, restraint, patient camera);
- graphite with colour only on food, plants and decorations (and later blood);
- MakeHuman bodies, measured contacts and automatic checks;
- the animatic-first workflow.

Specific lessons recorded there include:
- the cleaver held with a near-straight wrist, the blade turning with the forearm and coming square only
  in the cut;
- the chest following the spine only;
- eyes clamped with lids following the gaze;
- slices that fall differently;
- a full redraw whenever the camera moves.

**Checks and speed (horror trailer, 8 Oct)** (details: `guides/yuletide/pipeline.md`, last section)
- Run `horror_preflight.py` before every render: the whole skeleton over every frame in about a minute. Fix every fault first.
- Render with `--reuse`; check every new drawing against the lookbook with `lookbook_check.py`; keep title cards last.
- The Satire rules (circle hands, flat colour, the Satire style kit) never apply here: the trailer keeps its own look.
