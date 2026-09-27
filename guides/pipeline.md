# How a shot is made

Read this before making or changing any shot. It describes the parts the film is built from and how a
recipe turns them into drawings.

## The parts (in `source/`)
| File | What it is |
|---|---|
| `materials.py` | Every material (skin, knit, steel, ham glaze...) and the renderer's default settings. The drawing also uses it to know which things are characters, props, or kept in colour. |
| `kitchen.py` | The kitchen set and its lights. It never moves. |
| `props.py` | Things the characters handle: `Board`, `Ham` (cut from one end, slices lying about), `Cleaver` (placed by the middle of its edge and its orientation). Each can be moved frame by frame and measured against. |
| `rig.py` | Any character's body: MakeHuman's measured human with its real skeleton. For each pose the skin is bent by the skeleton (smooth elbows and shoulders, no seams). Arms are posed by *inverse kinematics*: you say where the hand goes, it works out the shoulder and elbow. |
| `mother.py` | The mother: her shape and face, her jumper and trousers made over her bent body for each pose, her MakeHuman head (smiling), her hands (closed round the cleaver, pressing the ham), her hair. `solve(spec)` works out a whole pose from a short description; `build()` puts her in the scene. |
| `character.py`, `mhuman.py`, `mesh_sdf.py` | MakeHuman loading, the grip solver, and turning meshes into shapes the renderer draws. |
| `checks.py` | The automatic whole-body checks. They run on every frame; any failure stops the render and says what is wrong, in millimetres. |
| `shot.py` | Builds, checks, renders and draws a frame from a recipe; renders whole shots. |
| `graphite.py` | Turns the render into the pencil drawing (coloured pencil on food, plants, decorations). |
| `cache.py` | Slow pieces (head, hands, a jumper or hair for a given pose) are kept on disk and only ever made once. |

## Recipes (in `source/shots/`)
A shot is a short file with `DURATION` (seconds) and `frame(t)`, which returns, for any moment:
`camera` (position, target, field of view), `mother` (her spec: where she stands, lean, where she looks,
smile, what each hand holds), and the props. Everything is in metres; the floor is y = 0; the island top is
at 0.92 m. The daughter will get her own module like `mother.py` built on `rig.py`.

Keep continuity in the recipes: the ham's cut position and the slices lying about carry from shot to shot.

## Making drawings
- One frame: `python3 shot.py still shots/s1_chop.py OUT_DIR` (1920x1080 by default).
- A whole shot: `python3 shot.py sequence shots/s1_chop.py OUT_DIR`. It draws on twos (12 drawings a
  second). The first drawing is made whole. After that a quick quarter-size render finds exactly where the
  picture changed (the moving things, their shadows, their reflections), and only those patches are
  rendered and redrawn, and pasted over the first. A redrawn window comes
  out stroke for stroke identical to the whole drawing, so there are no seams. The set's shadows are made
  once per shot.

## Costs (4-core machine, 1920x1080)
- Head and hands: once, a few minutes, cached. The set's shadows: once, cached.
- First drawing of a shot: about 3-5 minutes (rendered and drawn whole).
- Each later drawing: about 100 s - the jumper for the new pose (~35 s), the moving things' shadows
  (~27 s), a quick quarter-size render to find what changed, then only the changed patches rendered
  (~10-15% of the picture) and redrawn. Checked against drawing the whole frame: identical to the eye.
- Hair: rebuilt only when her head, neck or shoulders move (~70 s; to be replaced by the hair simulation).

## Rules
- Never hand-place a limb: say where the hand goes and let the arm solve, within natural joint ranges.
- Every contact needs visible proof (a dent, a cut, fingers wrapping); nothing meant to be apart may look
  touching from the camera.
- Run a fresh-eyes review of the whole picture after any change, not just the part changed.
