# The chat's own idea (written before the helpers ran)

1. A big move is planned as KEY POSES, not as a path. For shot 4: about seven keys (seated; rising and turning; head and
   shoulders out; sat on the sill facing back; aimed; recoil; back in). Each key is a whole pose on the kit's 3D
   skeleton (views.py already poses hips, feet, shoulders, elbows, wrists in 3D), posed in the BODY's own frame (hands
   placed relative to his chest, not world targets), and drawn with the view drawing that fits its angle (front,
   three-quarter, side, three-quarter back, back). In-betweens blend the skeleton in 3D; the view drawing swaps only
   on a frame chosen by hand (fast, or hidden by the window frame).
2. Layered by hand, by parts: the figure is drawn as separate part layers (head, torso, each upper arm, forearm, thigh,
   shin, hand with gun). Each key has a small table saying which parts are in front of the door / window frame / roof
   and which behind; in-betweens take the table of the nearer key, and a per-part depth test along each bone (not three
   sample points) confirms it. The car's solids hide only the parts the table puts behind them.
3. A pose sheet before the shot: each key drawn alone at full size, and in the shot's frame at phone size, plus a strip
   of every third frame of the move with the person alone; the fresh-eye critique (rule 89) on that sheet before any
   clip; Sam sees it in the rule 8 build proposal.
4. The "is this a human body" check, every person, every frame, run by the clip and animatic gates (a fault stops the
   send): (a) every bone's 3D length within 6% of the rig; (b) elbows and knees bend the natural way (3D joint limits);
   (c) each arm drawn joined to its shoulder (the arm layer touches the torso layer); (d) seen from behind, the left arm
   is on the picture's left (the drawn side matches the 3D side); (e) the draw order of parts matches their depth
   unless the key's table says otherwise; (f) samples along every bone, not only joints, tested against solids;
   (g) a held gun's barrel within 15 degrees of its target while firing; (h) the person's picture alone is one joined
   shape. Proven by failing version 4 on Sam's frames (notes 2, 3, 4, 6, 7, 8, 11, 15) and passing shot 3 and the pose
   gallery.
5. Kept as kit: the part-layer drawing and the check go in views.py / viewchecks.py with kittests; new key poses that
   pass the critique go in the pose gallery (car climb, sill sit, aim from a sill) for reuse.
Cost guess: about one Opus chat to build parts + check, one to pose shot 4's keys and sheet; risk: views.py is used by
every film, so the part layers are an option that changes nothing unless asked for.
