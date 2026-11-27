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
- [x] Fresh judges, one per view (blind to the notes), wrote what they saw per case (27 Nov, chat 1):
      notes/seeing-test/findings/{plain,whereis,motion,cutout,pose}.md. Each tool's own printout per case:
      notes/seeing-test/printouts/ (cNN-VIEW.txt; cNN-truth.json = the movement measure beside the engine's own
      layer movement: median error under 3 px on still-camera Brexit cases, 10-50 px on GTA's moving camera; the
      means are inflated by layers sharing one name, e.g. every 'worker'). Sheets were in the chat's scratchpad only
      (re-made by `seeing.py render` + `views` from notes/seeing-test/cases.tsv).
- [x] A separate scorer with the key (notes/seeing-test/key.md) counts caught / missed / wrongly flagged per view.
      Done blind (chat 2): notes/seeing-test/scores.md.
- [ ] One plain table for Sam, one line per tool; his yes/no per winner, one at a time.
- Not duplicated: check-knows-intent option 1 (R8, notes/check-audit.md) is about intent lists for the picture
  checks; this job only adds ways of looking.

## Branches the start listed
- claude/brexit-chat39 (0 h): Open Wounds' live chat 39, left for that chain (film work, pushed by its own chat).
- claude/upbeat-dirac-w16tn9 (0 h): a live chat's plain-words log and waiting-list archive; not this job's, left for it.
- claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: GTA's, named
  and left by earlier chats (notes/check-audit.md, notes/next-jobs.md); nothing this job needs.

## Open
- The who-is-where copy sees only what is drawn through the engine's layer recorder (cover.py: places pieces, the
  people kit's people, arms and heads) or a sorted item list (GTA's street). At these versions it could NOT see the
  wolves (drawn by their own code) or the people/arms of GTA's 3D Jason separately from the car's inside; those show
  as faint grey picture. A film that wants this view needs its own-drawn things wrapped (cover.thing).

## Where things stand (27 Nov, seeing test chat 2)
- Rules that bite next: Statement Two (no tool beat plain frames: say so), 93 (advice only), "Messages to me".
- Done: blind scoring (notes/seeing-test/scores.md). Of 14 notes Sam gave: plain frames 2, pose 2, movement 2 (with
  6 false alarms), who-is-where 1, cut-out 1. Every arm caught GTA note 8 (door); none caught the other 11. No
  tool beats the plain frames, so no winner is adopted.
- Next: none until Sam answers (Opus, medium on his answer). Plan if he says Y: the faults all arms missed are
  hands-on-things, through-the-scenery and too-quick moves; the next try is the model watching the actual clip
  (motion, not stills) with each person's outline, tested on these same 16 cases.
- Needs Sam: Y/N on dropping the four views as Sam-facing checks and trying the watch-the-clip idea.
- Open, unverified: all five arms flag Jason through the door in c10 (posted GTA final); not matched to a frame.
- Read: this file; notes/seeing-test/scores.md; key.md.
- Open rule requests: none.
- For Claude: re-render: `git worktree add /scratch/wt-COMMIT COMMIT`; `seeing.py render CASE --film MOD --span T0 T1
  --src WT/source`; `seeing.py views CASE`. Letter map in scores.md.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 149.56% of a week (2026-11-27)
