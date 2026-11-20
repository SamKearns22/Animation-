# Learn step results (chat 17, 20 Nov; changes nothing)

(a) Fresh cold critique of version 4 (12 frames, critique.py pack gta-shot4-learn, Sonnet helper, before any fix;
pack in source/data/critique/gta-shot4-learn/r1-p1). Of the 8 cause-A notes (2, 3, 4, 6, 7, 8, 11, 15):
caught 2 (3: "a stubby tube arm with no clear shoulder join", "a straight rubber tube"; 7: "from behind the passenger's
arms are missing or start inside the chest"); half-caught 3 (6, 15: same P8 line spans the frames but not the tangle;
8: "the gun is lost or unclear", not its direction); missed 3 (2, 4, 11: body through bonnet, door, door frame).
It also caught notes 9 (no driver hit), 13 (hydrant never seen), 16 (no acting) and part of 14. It would have stopped
version 4 being sent (faults found), but it cannot be trusted alone for clipping through the car.

(b) Version 4's Jason poses turned into the 3D skeleton (lying.Body, built from jason_layer's own joints through
fig_to_world; scratch script, not kept) at 0.6, 1.0, 1.4, 2.0, 2.92, 5.3 s: bone lengths within 6% of the rig and
lying.body_faults (neck, arm on its own side as seen) found NO fault at any of the six. So the skeleton was human;
the inhuman pictures came from drawing it as one flat figure at one turn angle with the arm drawing order of that view
and the three-point masks. A check on the skeleton alone would have missed notes 6 and 7: the human-body check must
test the DRAWN pieces (each arm joined to its own shoulder in the picture, on its own side as drawn), as the verdict's
Change 1 says.

(c) Look sheet: notes/shot4-case-study/v5-test-skeleton-vs-v4.jpg. The same poses drawn with lying_flat.draw (the
house pieces on the skeleton, nearer over farther), still hidden by version 4's masks: arms join the shoulders from
behind, no arm out of the back at 2.0 and 2.92 s; reads as a person.

(d) Missing upright (to build with Change 2): the held gun (lying_flat draws no props: grips.held on the skeleton
route); the neck (head sits on the shoulders, also in version 4); hiding by the car piece by piece instead of
three-point masks; the face's mood and squint carried to lying_flat's head; key poses for the written lean-out.
