# Movement guide: how she should move

Read this (with `character-anatomy.md`) before animating any character. It collects what the research says about
real human movement, with the numbers we animate to, and how our pipeline will produce it.

## 1. The principles that make movement believable
From Disney's twelve principles (Thomas & Johnston, *The Illusion of Life*, 1981), the ones that matter most for
realistic characters:

- **Slow in, slow out.** Bodies accelerate and decelerate; nothing starts or stops at full speed. Use eased
  curves between poses, never straight-line interpolation (mechanical things are the exception).
- **Arcs.** Natural movement follows curved paths (a joint rotating). A hand moving in a straight line looks robotic.
- **Anticipation.** Before a big action, a small opposite one: the cleaver is lifted before it falls; the eyes
  move before the head turns.
- **Follow-through and overlapping action.** Parts move on their own timing. The torso leads; head, arms and
  especially **hair** follow, overshoot and settle ("drag"). Soft tissue moves more than bone.
- **The moving hold.** Even "still", a person breathes, sways and blinks. A frozen body looks dead.
- **Timing.** Heavy things react slower; the number of frames for an action sets its weight and mood.
- **Secondary action.** Small supporting motions (a breath, a glance, fingers settling) make a scene live,
  but must not distract from the main action; during a big movement the face is barely noticed, so put
  facial beats just before or after it.
- **No twins.** Left and right never move identically at the same moment.

## 2. Eyes (the biggest giveaway of "dead" CG)
- **Saccades** (the jumps between points of focus) are extremely fast: about 20–40 ms for small ones, with
  peak speeds around 300–500°/s (10° jump ≈ 250–350°/s; saturating near 500–650°/s for 40°). Duration grows
  roughly linearly with size (about 2–3 ms per degree plus ~20 ms). At 24 fps a small saccade is **one frame**:
  the eye should simply be in the new place, perhaps with one in-between for big jumps. Never ease a saccade
  slowly across many frames.
- **Reaction time** before a saccade is ~200 ms after something catches her attention.
- Between saccades the eyes **fixate** for ~0.2–0.6 s, with tiny drifts; a person looking at someone they love
  moves their eyes between the other person's eyes and mouth in small saccades.
- **Eye–head coordination.** For gaze shifts bigger than ~20° the head joins in. The **eyes move first**, then
  the head follows more slowly (a few hundred ms); as the head arrives, the eyes **counter-rotate** to stay on
  the target (the vestibulo-ocular reflex). For very large shifts (>~60°) the shoulders/torso turn too, last.
- **Blinks.** At rest 8–21 per minute (fewer when concentrating, e.g. on a task; more when talking or
  emotional). A spontaneous blink lasts ~100–400 ms, the lid closing faster than it opens (about 1 : 2).
  Blinks often happen **with** gaze shifts and head turns, and at the end of a thought. Irregular intervals.
  The upper lid follows the eye up and down (looking down lowers the lid).
- Both eyes **converge** on the same point (the distance she's looking at), not parallel.

## 3. The smile (onset, apex, offset)
- Measured smiles (Cohn & Schmidt 2004, 81 people): the **onset** (lip corners rising) averages about
  **0.5 s** (0.52 s ± 0.32 spontaneous); earlier work gives ~0.7 s on average.
- **Genuine smiles are smaller and smoother**; their size and duration are tightly linked (a bigger smile takes
  longer) - like other automatic movements. Posed smiles are bigger for their duration and irregular.
- **Fast onset and abrupt offset read as fake**, untrustworthy and less attractive (Krumhuber & Kappas 2005;
  Krumhuber et al. 2007). A warm smile grows over ~0.5–1 s and fades over a second or more.
- The parts don't arrive together: facial actions reach their peak **asynchronously**. The mouth corners
  lead; the cheek lift and eye narrowing (the Duchenne part) build a little after.
- Muscle activity starts ~0.23 s before the movement is visible, so the change should start gently.
- A felt smile also shows subtle lip-corner movement that is smoother than in social smiles.

## 4. Hair
- Real hair is simulated as **strands or clumps of mass-and-spring chains**: each lock is a chain of points
  joined by stiff springs (keep its length), with bending stiffness (keeps its shape), damping (air drag and
  hair-on-hair friction make it settle within one or two swings), gravity, and **collisions** with head,
  shoulders and body (Selle, Lentine & Fedkiw, *A Mass Spring Model for Hair Simulation*, SIGGRAPH 2008).
  Productions usually simulate guide locks and fill in between them (Petrovic et al. 2005); that is exactly
  how our hair is built (about 110 locks round a volume), so we simulate our locks and re-sculpt per frame.
- Behaviour to expect: when the head turns, the roots move at once, the ends **lag**, then swing past and
  settle (follow-through). A 30 cm fall of hair swings at roughly 1 cycle per second and is heavily damped.
  Hair resting on the shoulder slides and pivots over it.

## 5. The body
- **Standing still** is never still: the body sways a few millimetres to a centimetre, slowly (well under
  1 Hz), and breathing (12–20 breaths per minute at rest, about 4 s per breath) lifts the chest and shoulders
  slightly; breathing even perturbs balance. Concentrating on a task reduces sway and breathing depth.
- **Weight** shifts before any reach: to reach forward she moves hips/torso first, then the arm.
- **Chopping**: anticipation (lifting the cleaver, ~0.3–0.5 s, eased), a fast downswing (~0.1–0.15 s,
  accelerating - gravity plus force), impact with a small recoil and a jolt through the wrist and arm, then
  settle. The free hand steadies the food and reacts to the impact. The eyes normally watch the blade just
  before impact (in our story she doesn't - that's the horror).
- Joints move within their ranges; elbows and knees never bend backwards; wrists flex up to ~60–70°.

## 6. The look of movement in our style
- Waltz with Bashir was done largely in **Flash cut-out** animation over a filmed reference, with classic
  hand animation where needed; its director said **slow movement was the hardest thing** to make look good in
  that technique - fast action hides a lot. Our 3D-then-drawn pipeline handles slow, subtle movement well,
  which suits this film (smiles, glances, breathing).
- Hand-drawn animation is often shot **"on twos"** (12 new drawings per second at 24 fps). It suits a pencil
  look, halves render time, and fast actions can go "on ones" (every frame).
- Pencil "boil": if the stroke texture changes randomly every frame the drawing flickers. Keep the stroke
  pattern tied to the surfaces (or change it only on each new drawing) so it lives without shimmering.

## 7. How our pipeline will do it
1. **Pose to pose**: key poses (like an animator's key drawings) for body, head, hands and face units; in
   between them eased curves (slow in/out) along arcs.
2. **Layers with offsets**: torso → head → eyes → hair each with its own delay and follow-through; eyes
   saccade on single frames; blinks scheduled irregularly, tied to gaze shifts.
3. **Face**: MakeHuman's face units animated over time (the smile's onset ~0.5–1 s, parts arriving in
   sequence, slightly different on each side).
4. **Hair**: each lock simulated as a damped chain with collisions against the MakeHuman body, then the hair
   volume re-sculpted for each drawing.
5. **Rendering budget**: a full frame currently takes ~6–10 minutes at 2560 wide. For animation: render at
   1280×720, draw on twos, re-render only what moves (the kitchen is drawn once), and reuse the hands'
   shapes as rigid pieces when only the arm moves.

## Sources
- Thomas & Johnston, *The Illusion of Life* (1981), via Wikipedia's summary of the twelve principles.
- Cohn & Schmidt, "The timing of facial motion in posed and spontaneous smiles" (2004).
- Krumhuber, "The temporal dynamics of facial expressions", *Emotion Researcher* (2016), summarising Krumhuber &
  Kappas 2005, Krumhuber et al. 2007/2009.
- Paul Ekman Group, "Fake smile or genuine smile?" (Duchenne markers).
- Saccade figures: Tobii's eye-movement notes (20–40 ms typical saccade) and clinical normal ranges; blink
  figures: *Review of Ophthalmology* (8–21/min at rest), clinical summaries (100–400 ms).
- Eye–head coordination: Freedman & Sparks (1997); McCluskey & Cullen (2007): eye, head, body move in sequence;
  the head contributes beyond ~20°.
- Selle, Lentine & Fedkiw, "A Mass Spring Model for Hair Simulation" (SIGGRAPH 2008).
- Joe Strike, "Waltz with Bashir: Animation and Memory", AWN (2008), interview with Ari Folman.
