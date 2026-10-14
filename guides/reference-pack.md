# Reference pack: movement for the satire films

What every pose and movement in the satire package is built from (researched 14 Oct). Built to order: a movement is
only made when a script needs it, but when it is made it follows this page. Timings are in frames at our 12 frames a
second; "on twos" means each drawing is held for two of those frames' worth of film time at 24 fps, which is what our
12 fps already is.

## 0. The style target: limited animation, not realism
- **South Park** (the closest model): animator Lucas Walker describes every character rig as having "no less than four
  views: left, right, front, back", plus special poses done as **replacement animation**: "you can hit a slider that
  turns off one piece of geometry and turns on another" (South Park Public Library, *Animation Style Changes*). So a turn
  or a new pose is a swap to another drawing, never a squash or a bend of the flat one. Walks are minimal (a bob and a
  slide); only the video games animate their legs. Our films go a step further than the show (legs do walk), but keep
  its snap: hold, swap, hold.
- **Limited animation** (UPA, Hanna-Barbera): few drawings, strong poses, holds; walk cycles of a handful of drawings;
  only the parts that matter move. Realistic numbers below are used to keep poses *believable*, not to make motion
  smooth: we pick the key poses from them and draw those snappily.

## 1. Walking, strolling, pacing, running, sprinting
Sources: Richard Williams, *The Animator's Survival Kit* (2001), walks and runs chapters; Novacheck, *The biomechanics of
running*, Gait & Posture 1998; Tudor-Locke et al. 2019 (walking cadence, PMC6337834); Physiopedia, *Running
biomechanics*; Muybridge, *Animal Locomotion* (1887, public domain, on Wikimedia Commons: Category:Eadweard Muybridge).
- **Four key poses per step** (Williams): *contact* (heel just touching, legs at their widest, no weight yet), *down*
  (weight lands, knee bends, body lowest, arms swing widest), *passing* (free leg passes the standing one, body rising),
  *up* (pushing off, body highest). Make the contacts first, then the passing position; the passing position decides the
  walk's character (up = normal; down = a cartoony, heavy walk).
- **Tempo** (Williams' beat, frames per step at 24 fps -> steps a second): 16 = stroll (1.5); 12 = natural, businesslike
  walk (2); 8 = brisk "cartoon" walk or slow run (3); 6 = run (4); 4 = very fast run, sprint (6). At our 12 fps a natural
  walk is 6 frames a step, which gives exactly contact, down, passing, up plus two in-betweens.
- **Real cadence** (checks only): about 100 steps a minute = a moderate walk, 130 = a vigorous one (Tudor-Locke); runners
  170-180 (elite 180+); sprinting up to about 220. Comfortable walking speed about 1.3-1.4 m/s.
- **Walk vs run** (Williams; Novacheck): in a walk one foot is always on the ground; in a run both leave it ("float") for
  one or more drawings, and the faster the run, the longer the float and the shorter the foot's time on the ground
  (stance is under half the cycle). Hip about 50 degrees forward at a running footfall.
- **Arms**: opposite to the legs, widest on the down. In a very fast run, pump the arms on their own faster beat, or
  stretch them forward (Williams: "not enough time to swing the arms around violently").
- **Feet**: pick up slowly, put down fast; a planted foot never slides. Vary a fast run's drawings so it doesn't read
  as a loop; take several steps before repeating.
- **Personality**: an angry walk hits the foot down fast; a sneak leans back as the foot reaches, forward as it takes
  the weight; head and hands counteract the body (Williams).
- **Pacing** = walking a line, turning at each end with the turn method below, then walking back.
- **Facing**: the body faces the way it travels; the head may look elsewhere, but no more than about 90 degrees from the
  body. **Angles** come from the four or more views (front, side, back, and three-quarter in between).

## 2. Turning
Sources: South Park (above); the industry turnaround (front, front three-quarter, profile, back three-quarter, back:
Domestika, *What is a turnaround*); Toon Boom Harmony's drawing substitution in cut-out rigs.
- A turn swaps view by view: the eyes first (one drawing), the head a drawing later, the body a drawing after that,
  each view held one or two drawings; the feet take small steps round. A half turn is about 4-6 drawings.
- One quick smear or a cut on the action can hide the middle (the live-action trick; Bingo Bingo uses the cut).

## 3. Standing styles
Sources: the classical *contrapposto* (weight on one leg: hips tilt one way, shoulders the other) as taught in figure
drawing (Andrew Loomis, *Figure Drawing for All It's Worth*; George Bridgman); Williams on weight.
- Relaxed standing puts the weight on one leg; the hip over it rises, the shoulders tilt the other way; the free knee
  bends a little. People shift weight every few seconds (our `filmkit.shifts`).
- Attitudes come from silhouette: arms folded (closed, sceptical), hands in pockets (casual), hands behind the back
  (formal, royal, politician), leaning on something (casual, weary), slumped (head forward, shoulders down, chest
  hollow), chest out with hands on hips (confident).

## 4. Sitting, standing up, sitting down
Sources: Schenkman et al., *Whole-body movements during rising to standing from sitting*, Phys Ther 1990; Kinematic
analysis of sit-to-stand in healthy young adults, Medicine 2021 (PMC8183776).
- Standing up has four phases: (1) **flexion momentum**: the trunk leans forward (ends about 18% of the way through);
  (2) **momentum transfer**: the hips leave the seat and the body rotates forward over the feet (to about 40%);
  (3) **extension**: the legs and trunk straighten, the longest phase (to about 91%); (4) **stabilisation**: settle
  upright. Feet come back under the knees first. Sitting down is roughly the reverse, with the hands often reaching for
  the chair. An unhurried rise takes about 1.5-2 s (18-24 drawings).
- Seated: hips on the seat, thighs forward, the jacket ending at the lap so the seat's edge shows (A Professional);
  leaning forward puts the elbows on the knees or the table.

## 5. Talking gestures
Sources: David McNeill, *Hand and Mind* (1992) and the McNeill Lab's gesture classification.
- Four kinds: **iconic** (draws the thing: a big circle for "huge"), **metaphoric** (shapes an idea: offering it on an
  open palm, weighing two options), **deictic** (pointing, at a person or an imagined place), **beat** (small up-down
  strokes on the stressed words). Beats land on stressed syllables: our lip-sync track knows those, so beat gestures
  can be timed automatically.
- Politicians' stock set: the open palm, the chopping hand ("let me be clear"), the point, the hand on heart, the shrug.
- **Circle hands can't do finger gestures** (counting, precision grip, a thumb pressed on a fist): stage those with the
  whole arm or a prop instead. The finger guns are our one named exception.

## 6. Holding things
Sources: ergonomics (UK Health and Safety Executive on neutral wrists); our own lessons (best-practice Part 1).
- Held in front: the upper arm hangs, the forearm comes forward, the wrist stays near neutral; the prop turns to suit the
  arm. A phone to the ear: elbow up and out, the phone over the circle hand at the ear. Papers in two hands at chest
  height; a mug at the chest when sipping, by the side otherwise. Picking up: reach, the circle touches, the prop moves
  with the hand from then on.

## 7. Combat and falls
Sources: Williams (timing of hits and weight); stage-combat practice (Weapons of Choice, *The Textbook of Stage Combat*:
strikes, knaps and reactions); our Russiadent Evil lessons (best-practice Part 2).
- **The blow**: wind-up (anticipation; animation exaggerates it where stage combat hides it), a fast strike that lands
  in one or two drawings, a held impact drawing, follow-through. One clear blow beats flailing.
- **The reaction**: the victim moves only after the contact (stage rule: only after the knap is heard), in the direction
  of the force, sized to the blow; the striking hand drops down and away rather than flying on.
- **Sightline**: the blow reads best across the camera's line of sight; the impact sound lands on the contact drawing.
- **Falls** come in stages (knees, hips, shoulder, head), never a plank tipping over; the body's length on the floor is
  planned first; then it settles and stays.
- **Swords** (laid over the circle hand): wind-up, the swing along an arc with a one-drawing smear, contact or parry,
  follow-through.

## 8. Cars (to order; the car itself is designed per film)
Sources: Crizzle et al., *A systematic review of driver ingress and egress* (Journal of Ergonomics 2014); senior drivers'
ingress/egress strategies (Vehicles 2023, MDPI).
- **Getting in** has three phases: open the door; the *adaptation* (the near leg lifts in, head ducks under the roof, or
  the person turns, sits and slides across first and then swings both legs in); seated, both feet on the floor; then
  the door closes. Common strategies: lateral slide (sit, then swing the legs in) or leg first (one leg in, duck, sit).
- **Getting out**: open the door, near leg first (or both legs swung out together), a hand on the frame, head forward
  under the roof, stand, step clear, close the door.
- **Driving**: seated, hands on the wheel, small steering moves; the body sways a little with turns while the scene
  outside slides past.

## 9. Perspective (built before anything walks towards or away from the camera)
Sources: Loomis, *Successful Drawing* (perspective); our own `series.Room` (A Professional).
- One camera in metres over a flat floor: everything's size follows its distance, and every foot meets the floor. With
  the camera at eye height, every standing adult's eyes sit on the horizon line, whatever their distance: a quick check
  that people are on the same floor.
- Walking towards the camera: the figure grows and its feet move down the frame; away, it shrinks and rises towards the
  horizon; across, constant size.
