# The chat's own idea (written before the helpers)

Core: one solid body, not pieces. Jason becomes ONE skinned 3D body (the MakeHuman mesh the project already has, shaped
to his proportions and dressed as closed shapes for vest, shorts, hair) on a proper rig: a skeleton with IK (the hand or
foot is placed, the elbow and knee follow), joint limits, and the car as a solid 3D shape in the same world. The look is
made by drawing that body, not by assembling flat pieces: each pixel knows which part and colour it is (skin, vest,
shorts, hair, car) and how deep, so what hides what is decided by the 3D body, never by hand-made maps. Outlines are
drawn where parts or depths meet (silhouette and part borders, like Blender's Line Art), in the house line weight; fills
are the house's flat colours; the face stays the house's drawn face pinned to the head; the hands stay the house circle
hands, placed at the 3D wrist and hidden by whatever is in front of them.

Steps:
1. Test the tool: can Blender run here with no graphics card (Workbench or Cycles on the processor), or do we use our
   own renderer (mesh_sdf) for the part/depth picture. Pick by a one-frame test.
2. Test space: Jason seated, the car door and window only, shot 4's exact camera. Nothing else.
3. Style match first, no movement: the solid-body Jason in K1 beside the current flat Jason from shot 3; must be
   indistinguishable at phone size (a blind look test) before any move is made.
4. Learn moves in steps of difficulty, each passing before the next: turn the head; raise the arm; kneel up; head out;
   out to the waist; back in. Key poses set by IK goals on the car (hand on the door top, knee on the seat), in-betweens
   from the rig; acted reference first (a CMU motion or a reference clip of a person climbing out of a car window).
5. Checks built into the test space: no mesh passes through another (body vs car, body vs itself) measured in 3D every
   frame; hand style is circle hands every frame; the full-size frame look by a fresh critic; strips at phone size.
6. Only when the test-space move passes Sam, it goes back into shot 4, camera and beats untouched.
7. Written up as a kit piece (rig, solid-body drawing, collision check) for every later showstopper move.

Hands: put back the circle hands now in the notes as a lesson: no change to the house look without Sam's Y; fault lists
must quote Sam, not paraphrase him into a new request.
