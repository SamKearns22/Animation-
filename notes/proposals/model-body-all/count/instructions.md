# Sorting Sam's notes: would a "model body" have prevented this fault?

Each line of your batch file is: ID <tab> film <tab> file:line <tab> the note as written in the film's notes
(Sam's words, often quoted, followed by what Claude did about it). Sam directs cartoon satire films; our style is
FLAT 2D drawings (outlines, flat colour). Today most people are drawn as flat 2D pieces (torso, arm, leg shapes
drawn separately per view and layered), with hand-drawn heads (a few fixed views) and circle hands.

THE PROPOSAL: build every character's body as ONE solid 3D model body (like "Jason" in Grand Theft Autism shot 4):
a single posed 3D human body, rendered flat in the house style, so limbs are always joined, keep their length and
thickness, turn correctly at any angle, and are posed like a real body; one depth pass decides what is in front.
Clothes are painted on or pushed-out shells of the skin. Heads and hands stay hand-drawn (house heads, circle hands)
on top. Sets/furniture/props stay flat drawings unless also modelled.

For every line write one output line:  ID | KIND | CAT | PREVENT | CAUSE | why (max 12 words)

KIND: N = a note/fault Sam raised (or a fault from Sam's brief/notes that the film had to fix);
      X = not a Sam note (Claude's work log, a plan, a check result, a decision record, a file list, a status).
      Only N lines need the rest; X lines: `ID | X | - | - | - | -`.
CAT (the fault's subject, pick one):
  BODY    = the body's shape, proportions, limbs, joins, a limb missing/wrong length/sausage, body turning or changing
            drawing between angles or frames, a pose that looks broken/unnatural, sitting/standing/walking pose,
            body depth order (arm in front of/behind torso), back/side views of the body.
  CONTACT = where a body meets something else: hands on objects, feet on the ground, sitting on a chair, body
            through a car/door/desk/wall, gripping, leaning.
  HANDS   = the hands themselves (shape, fingers, grip drawing).
  FACE    = likeness, face, eyes, mouth, expression, head shape/turn, hair, beard.
  CLOTHES = garments, colours, costume details.
  MOVE    = timing, speed, acting choice, gesture choice, lip sync, a move that is missing or wrong in kind (not how
            the body is drawn while moving).
  SET     = places, furniture, props, vehicles, backgrounds, lighting, scale of things.
  CAMERA  = framing, cuts, shot choice, composition, crop.
  TEXT    = Hook Text, titles, captions, sign-off, sound, voices, music, file size/format.
  SCRIPT  = story, jokes, lines, who is in it, content.
  OTHER   = anything else.
PREVENT (would the model body, as described, have stopped this fault from happening?):
  Y = yes, the fault came from drawing the body as flat separate pieces (joins, lengths, turning, pose breaking,
      body depth order, a body passing through ITSELF).
  P = partly / only if the thing it touches is also solid 3D (most CONTACT with furniture, cars, doors), or it
      would reduce but not remove the fault.
  N = no (the fault is about something the model body does not change).
CAUSE: R if the model body could plausibly make THIS kind of fault worse or bring a new one (e.g. head views not
  matching a freely turning body, circle hands on a realistic arm, a 3D look against flat sets, clothes that must be
  real garments, a hard-to-draw back of head); else -.
Be strict and honest: P is not Y. Judge from the note's words only. Do not skip lines; one output line per input line,
in order. Write ONLY the output lines to the output file named in your task (no headings), then reply "done N lines".
