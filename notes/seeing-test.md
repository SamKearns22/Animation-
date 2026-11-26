# Seeing test (shared tools job; proposal notes/proposals/seeing-five-candidates.md, Option 1, Sam's Y 26 Nov:
"1. Y but lose option 5")

Kind: tool job (no film). Locked by Sam: no film's shots, cameras or beats are touched (old versions are only
re-drawn in throwaway copies); rule 93: every view is advice, never a lock.

## Brief checklist
- [x] Test set: Sam's movement and touching notes, Brexit Is Done 13, 14, 15, 19, 22, 23.1, 23.3, 23.4 and GTA v5
      2, 3, 4, 5, 6, 8, each re-drawn from the version Sam saw (commits in notes/seeing-test/key.md), plus five moves
      he passed (c03, c05, c07, c10, c15). 16 cases.
- [x] Four ways of looking built in one shared tool, source/seeing.py: (1) who-is-where flat-colour copy drawn by our
      engine, (2) frame-to-frame movement measure (OpenCV DIS optical flow), (3) picture cut-out (MediaPipe multiclass
      person segmenter + u2netp through onnxruntime), (4) body-pose finder (MediaPipe pose landmarker full + hand
      landmarker). Baseline: the plain frames alone.
- [x] Installs: OpenCV 5.1, MediaPipe 1.2.3, onnxruntime 1.29 were already here. Downloads all worked (26 Nov):
      pose_landmarker_full.task, hand_landmarker.task (Google's model store), u2netp.onnx (rembg's GitHub release),
      magic_touch.tflite (point-click cut-out; not used: it needs someone to say where to look). Nothing faked.
- [x] Option 5 (video-watching model): dropped by Sam; not attempted.
- [x] Kit test: seeing_views_see_a_vanish (a made-up film's square vanishes mid-frame; the item wrapper records the
      layers, who-is-where names the vanish, the movement measure flags that frame, sheets saved): PASS.
- [ ] Fresh judges, one per view (blind to the notes), write what they see per case; a separate scorer with the
      key counts caught / missed / wrongly flagged.
- [ ] One plain table for Sam, one line per tool; his yes/no per winner, one at a time.
- Not duplicated: check-knows-intent option 1 (R8, notes/check-audit.md) is about intent lists for the picture
  checks; this job only adds ways of looking.

## Branches the start listed
- claude/brexit-chat39 (0 h): Open Wounds' live chat 39, left for that chain (film work, pushed by its own chat).
- claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: GTA's, named
  and left by earlier chats (notes/check-audit.md, notes/next-jobs.md); nothing this job needs.

## Open
- The who-is-where copy sees only what is drawn through the engine's layer recorder (cover.py: places pieces, the
  people kit's people, arms and heads) or a sorted item list (GTA's street). At these versions it could NOT see the
  wolves (drawn by their own code) or the people/arms of GTA's 3D Jason separately from the car's inside; those show
  as faint grey picture. A film that wants this view needs its own-drawn things wrapped (cover.thing).
