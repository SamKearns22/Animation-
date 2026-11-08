# Sitting kit (plan 7 Nov; part 1 built 8 Nov, part 2 built 8 Nov)

Sam, 7 Nov: "the full gamut of sitting animation": sit down, seated acting, stand up, feet up on a desk, lean back,
cross legs, perch, slump. Sam said yes to all eight questions ("Y go", 7 Nov).

## Where things stand
- **Rules that bite next:** 80 (front on: knees and lap show; no head dip on a rise), 78 (resting arms show weight), 42 (poses tested from every view).
- **Done (8 Nov): part 2 built and checked** (`source/sitting.py`): cross legs both kinds, feet up and down (and a caught-out snap), perch on a chair's edge and on a desk's corner, slump (slow and a collapse), the swivel turn with the desk staying put; the through-things, back-on-the-chair and feet-on-their-surface checks (`sitting.py audit`: clean). Part-2 sheet, photo comparison and a moves video sent to Sam. The whole sitting kit is built.
- **Next:** Sam's look at part 2 and his two questions (below, "Part 2: questions") (the rule 78 check is built: `kitchecks.rests`).
- **Needs Sam:** a look at the part-2 sheet and moves video; questions 9-10.
- **Read (next time):** `guides/figure-rig.md` s.4 (sitting line) and s.8; `source/sitting.py` MAP.
- **Open rule requests:** none.
- **For Claude:** part-2 hooks: spec keys `ankle` {side: (x, height, chair z)}, `on`, `knee_pole`, `toe`, `foot_yaw`, `foot_roll`, `sole`, `hip_dy`, `cross`, `contact`, `roll` (chair travel), `give` (how much the chair back follows), `tail`, `head_lean`, `swivel`, `legs_over`; views: `shoe_frame`, j['cross'] (top leg drawn last and over the lap), j['legs_over'] (+ `legs_over_views`), j['arms_under'] (hands under a desk), j['head_lean'] (side views only; front uses head_dy); a leg folded tight on screen is drawn as thigh + shin + round knee (was inside out). `Desk(turn, x, z)`, `Desk.xf` (+inverse), `Desk.boxes`; `Seat('desk')`. Clips: `sitting.py clips2 OUT.mp4`; `sitting.py sheet OUT 2`, `refs OUT 2`.

## Sam's list (the brief, ticked when built and tested)
| # | item | what it means here | built? | tested from every view? |
|---|---|---|---|---|
| 1 | sit down | from standing in front of the seat, down onto it, settled | part 1, 8 Nov | yes (front, side clips; poses 5 views) |
| 2 | seated acting | talking, gesturing, reacting from a seat; the moving hold | part 1, 8 Nov | yes (front, side clips; poses 5 views) |
| 3 | stand up | from seated to standing, ready to walk | part 1, 8 Nov | yes (front, side clips; poses 5 views) |
| 4 | feet up on a desk | leaning back, heels on the desk top | part 2, 8 Nov (and feet down, caught-out snap) | yes (front, side clips; pose 5 views) |
| 5 | lean back | trunk back against a reclining chair back | part 1, 8 Nov | yes (front, side clips; poses 5 views) |
| 6 | cross legs | one leg over the other | part 2, 8 Nov: knee over knee, ankle on knee; cross and uncross | yes (front, side clips; poses 5 views) |
| 7 | perch | sitting on the very edge (of a chair; of a desk: question 3) | part 2, 8 Nov: chair edge (and the scoot to it); desk corner (see question 9) | yes (front, side clips; poses 5 views) |
| 8 | slump | sliding down in the seat, deflated | part 2, 8 Nov: slow (1.5 s) and collapse (0.4 s) | yes (front, side clips; pose 5 views) |
| + | swivel turn | question 5 (Y): the villain's reveal | part 2, 8 Nov (0.8 s; the desk stays put, the head leads) | yes (front clip; the desk-still check) |

## What we have now (drawn on the sheet sent 7 Nov)
- **One seated pose:** upright on a plain knee-height office chair, thighs level, feet flat, hands on the thighs.
  Every seated person in every film so far (Oval Office, the newsroom, the poker table, the journalists, Gran) used it,
  and most films drew their own chair round it.
- **Stand up / sit down:** a 4-phase rise (1.6-2 s, the trunk leaning 35 degrees forward first); sitting down is the
  rise played backwards.
- **Getting into and out of a car, and driving** (seated at the wheel).
- **Checks:** hips on the seat (`check_seated`); arms keep their length (the arm guard); a hand shows in every view
  (rule 41); feet don't slide (walks only).

**Faults seen on the sheet and in past notes:**
1. **Front on, the seated man reads as a short standing man:** his thighs point straight at us and vanish under the
   jacket, so no knees and no lap show. Front on is our default view (rule 38), so this matters most.
2. **Front on, the lean before rising reads as sinking:** the head drops towards us and shrinks. Sam's Islamocommunism
   note 10 ("Rise: no lean and sink first"); that film skipped the lean.
3. **The rise is too slow:** Sam's note 18 asked for it 50% faster (1.6 s to about 1.07 s).
4. **Sitting down is the rise backwards:** a real sit-down is a controlled lowering, bottom first, slowing before the
   seat, then a settle; it is not a stand-up reversed.
5. **"Slumped" is a standing slouch** (head down a touch); there is no seated slump.
6. **One chair, one height, fixed upright:** it can't recline, swivel or be a sofa, stool or desk edge, and the chair
   doesn't lean with the person.
7. **No leg checks:** nothing stops a leg stretching, a knee bending backwards, a foot floating above the floor or
   sinking into a desk, or a crossed leg passing through the other.

## The design
### A. The seat is measured, the pose fits it
Every seat pose takes the seat from the film's set plan (one place, rule 35): seat height and depth, whether it has a
back (and how far it reclines), arms, and the desk height if there is one. Defaults: office chair 0.45 m seat, desk
0.74 m (standard heights). Seats in the kit: office chair (swivels, reclines), armchair or sofa (low, deep; the body
sinks a little into the cushion), stool or bench (no back), desk edge. The chair follows the person: it reclines
with a lean back and turns with a swivel. Films that already draw their own chair hand its numbers in.

### B. Front on first
- **Knees and lap show:** the thighs come at us, so the knees are drawn as two rounded shapes in front of the jacket's
  hem, the jacket falls open over the lap, the shins drop to the floor below. This is the front-on fix every other
  pose builds on.
- **Rising and sitting front on:** feet drawn back under the seat first (people really do this: it lets them rise
  with less lean; Janssen 2002), then only a small lean (about 15 degrees front on, the full 30 side on), the hips
  lifting early. The head never drops below its seated height on the way up.

### C. The poses (each tested from all five views, rule 42; avoid-views listed)
| pose | the body | what it says (Navarro; Pease) | contacts checked |
|---|---|---|---|
| upright (exists, redrawn) | back straight, feet flat, hands on thighs or desk | neutral, formal | hips on seat, soles on floor |
| hands folded on the desk | forearms on the desk edge, hands clasped (Vance, line 1) | composed, presenting | forearms on the desk top (rule 78) |
| leaning in on the elbows | elbows on the desk, chin on a fist or hands together | interested, scheming | elbows on the desk, never through it |
| lean back | trunk 15-25 degrees back, chair reclined, hands behind the head (elbows out) or on the armrests | relaxed, smug, in charge | back on the chair back |
| feet up | lean back plus both heels on the desk, ankles crossed; front on we see the soles of his shoes | ownership, contempt | heels on the desk top, calves clear of the edge |
| cross legs, knee over knee | thighs together, the top calf hanging over the lower knee | prim, closed, careful | top leg rests on the lower knee, never through it |
| cross legs, ankle on knee | the "figure four", the top knee out wide | cocky, dominant, at ease | ankle on the lower knee |
| perch (chair edge) | hips on the front third of the seat, trunk forward, hands on the knees or gripping the seat edge, feet back | eager, nervous, about to go | hips on the seat's front, back clear of the chair back |
| perch (desk edge) | one hip on the desk corner, one foot on the floor, the other dangling | casual boss, "let's chat" | hip on the desk, standing sole on the floor |
| slump | hips slid forward, back rounded against the chair, shoulders down, head forward, arms limp in the lap or off the armrests, legs out | defeated, bored, sulking | lower back on the seat edge, shoulders on the chair back |

### D. The moves and their timing (at 12 drawings a second)
| move | time | how (key moments) | source |
|---|---|---|---|
| stand up | 1.1 s normal (13 drawings); 0.7 s jumping up; 1.6-2 s weary or old | feet back (0.15 s), small lean, hips off the seat at a quarter of the way, legs straighten, a small settle | Sam's note 18 (1.07 s); healthy young adults rise in about 1-1.5 s (Janssen 2002 review) |
| sit down | 1.3 s normal; 0.5 s a "plonk" (tired, defeated); 2 s careful | a glance or a hand back to the seat (optional), bottom leads back and down, trunk leans forward to balance, slows just above the seat, lands, a 2-3 drawing settle | stand-to-sit is slower and controlled at the end (Jeon 2024); Williams, *The Animator's Survival Kit* (weight and settle) |
| lean back | 0.6 s | shoulders go first, the chair gives, a small rock forward-back as it settles (0.3 s) | anticipation and follow-through (figure-rig s.6) |
| feet up | 1.5 s | lean back, one leg swings up (0.4 s), the other lands on it crossed at the ankle (0.3 s), heels settle | |
| feet down | 0.8 s; 0.4 s "caught out" snap | reverse, legs first, then sit up | |
| cross legs | 0.7 s; uncross 0.5 s | weight shifts to one hip, the knee lifts, swings over, settles | |
| scoot to perch | 0.4 s | two small hip shuffles forward | |
| slump | 1.5 s slow deflate, or 0.4 s collapse (comic) | an exhale, shoulders drop first, hips slide forward, head last | overlapping action (Williams) |
| swivel turn | 0.5-1 s | the chair and body turn together, head leads a beat; the classic "reveal" turn | eyes lead (figure-rig s.6) |
| seated acting | the line's own timing | the standing gestures (open palm, point, chop, shrug) on top of any seated pose; leaning in on a point, back on a punchline | the gesture library (moves.pose) |
| moving hold | always | breathing every ~4 s and blinks (exist); a small weight shift every 4-8 s; never a frozen statue | figure-rig s.6 |

### E. The checks (code unless marked; every frame, every view)
| check | stops the render when | new? |
|---|---|---|
| hips on the seat | the hips are off the seat (perch: not on its front third) | extend the existing one |
| feet on their surface | a foot floats over or sinks into the floor, desk or other knee, or slides while planted | new for seats (walks have it) |
| leg guard | a thigh or shin is drawn longer or shorter than the rig, or a knee bends backwards or folds too tight | new (the arm guard has this, the legs don't) |
| legs and body through things | a leg passes through the seat, the desk or the other leg | new |
| back on the chair back | lean back or slump with a gap behind the back, or the back through the chair | new |
| no sink on a rise | front on, the head goes lower than its seated height while rising or sitting (Sam's note) | new |
| balance on a rise | the hips leave the seat before the shoulders are over the feet (side on) | new |
| the chair follows | the chair's recline or turn doesn't match the person's lean or facing | new |
| hands and resting arms | rule 41 (a hand in every view) and rule 78 (forearms on the desk show weight, never sink) | exist / rule 78 check built 8 Nov (`kitchecks.rests`) |
| no twins | two seated people shift or blink in the same drawing | by hand on the check sheet |

Proof for Sam: one labelled sheet of every pose from all five views (plus the chair types), and a short small clip
of each move, sent in the chat; the pose gallery and kit catalogue get their rows once each passes.

### F. References
- Timing: Janssen et al. 2002, "Determinants of the sit-to-stand movement: a review" (Physical Therapy 82:866); Jeon
  et al. 2024 on stand-to-sit speed and smoothness (PMC11112120); Sam's Islamocommunism notes 10 and 18.
- Animation: Richard Williams, *The Animator's Survival Kit* (weight, the bottom leading a sit, settles, overlapping
  action); Preston Blair, *Cartoon Animation* (sitting and slumping silhouettes); figure-rig s.6.
- Meaning of each pose: Joe Navarro, *What Every Body Is Saying* (feet and legs, leaning back, perching ready to leave);
  Allan and Barbara Pease, *The Definitive Book of Body Language* (leg crosses, the figure four, feet on the desk).
- Photos: one photo per pose in `references/sitting/` (question 7), checked side by side with ours on the sheet (rule 76).

### G. Build order (recommended: two halves)
- **Part 1 (what Ad-Vanced Notice needs now, and the base for the rest):** the measured seat and chair types, the
  front-on knees and lap, upright, hands folded on the desk, leaning in, lean back; stand up and sit down rebuilt;
  seated acting and the moving hold; the leg guard, feet, no-sink and balance checks. Then the sheet and clips to Sam.
- **Part 2:** cross legs (both), feet up and down, perch (both), slump, swivel turn; the through-things and
  chair-back checks. Then the sheet and clips.
- Cost: each half is building, Opus high. Budget asked for after part 1 (rule 44).

## Questions for Sam (7 Nov; answers go here)
**Sam, 7 Nov: "Y go": yes to all eight.** Rule 80 written. Building part 1 now.

1. Stand up in about 1.1 s with only a small lean front on (your Islamocommunism notes)? Y/N
2. Cross legs: both kinds, knee over knee (prim) and ankle on knee (cocky)? Y, or 1 = knee over knee only, 2 = ankle on knee only
3. Perch: both, on a chair's front edge (eager) and on a desk corner (casual boss)? Y, or 1 = chair only, 2 = desk only
4. Feet up, front on: we see the soles of his shoes, hands behind his head? Y/N
5. Add the swivel-chair turn (the villain "reveal")? Y/N
6. Build in two halves, the first being what Vance needs now? Y/N
7. Reference photos: I find free photos of each pose; you send any you'd rather use? Y/N
8. New rule 80, in the rulebook: "Anyone seated front on shows knees and lap, and rising or sitting never makes the head dip below its seated height." Y/N

## Part 2 (8 Nov): what was built, and the choices made
- **Knee over knee** (prim): the top thigh lies on the lower one just past its knee, the top calf hangs over the lower knee,
  the top foot off the floor; both hands on the top knee. Front on the top leg is drawn over the lap.
- **Ankle on knee** (the figure four, cocky): the top ankle on the lower thigh behind its knee, the top knee out wide,
  the foot turned across, its sole forward; one hand on the raised shin, one on the lower knee.
- **Feet up**: the chair pushed back 9 cm and reclined, hands behind the head, the left heel on the desk top, the right
  ankle crossed over it; front on the soles face us. Our people's legs are short for a desk this high, so the knees stay
  up a little to keep the calves clear of the desk's edge (the photo's legs are straight).
- **Perch on the chair's edge** (eager): hips on the seat's front third, leaning in, feet drawn back, hands on the knees;
  the back clear of the chair back. **Scoot to perch**: two hip shuffles (0.4 s).
- **Perch on the desk's corner** (casual boss): see question 9. Built as: standing beside the desk's front end, the left
  thigh up along the desk top, the knee just past its end, the shin hanging in front of it; the right leg standing; left
  hand flat on the desk, right hand on the raised knee.
- **Slump** (defeated): hips slid forward and down onto the tailbone, the back leaning against the chair (shoulders on
  it, the lower back off it), the chair back giving less than the trunk leans, the head forward and down, hands limp
  in the lap, legs out and splayed (the splay is what makes it read front on). Slow 1.5 s (breath out, shoulders drop
  first, hips slide, head last) or a 0.4 s collapse with a bounce off the chair back.
- **Swivel turn** (0.8 s): back to us, a small wind-up, he and the chair turn together through the drawn views, the head
  a beat ahead, a lean-in settle facing us, fingers steepled. The desk stays put on screen (checked every drawing).
- **Checks added** (every drawing of every pose and move): each foot on what it rests on (floor, desk top, the other
  knee or shin, or clear of everything when dangling); no leg or shoe through the seat, the desk or the other leg (a
  thigh may press the seat's front edge a little); the back resting on the chair back where the pose says (lean back,
  feet up, slump, armchair), clear of it on a perch, never through it; a perch on the seat's front third; a slide down
  the seat no deeper than the thigh allows; the chair back following the lean by the pose's amount; knees bending the
  right way (now tested on the knee's hinge, so a raised or turned-out knee is judged fairly); the desk still in a swivel.
- **Drawing fixes for every film:** a leg folded tight on screen (a figure four seen three-quarter) was drawn inside out
  (a hollow outline); now thigh, shin and a round knee. Soles can be drawn (lighter, with a heel) when they face us.
  Hands in the lap behind a desk are now under the desk, not over its front.
- **Photos (rule 76):** feet up (two), ankle on knee (from behind), the desk-edge perch, the armchair crossed leg; none
  found for the slump or a chair-edge perch (Wikimedia rate-limited the slump engraving).

## Part 2: questions for Sam (8 Nov)
9. Perch on a desk: our desk is higher than our people's hips (it's sized for seated arms), so sitting a bottom on its
   edge would make him taller than when standing. I built it as one thigh up along the desk and the other leg standing
   (it reads as perched side on, less so front on). Keep it? Y, or 1 = lower the desk for this pose only (a meeting table
   height), 2 = I'll send a photo of what I want.
10. Feet up: the knees stay a little bent (short legs, high desk). Fine? Y/N
