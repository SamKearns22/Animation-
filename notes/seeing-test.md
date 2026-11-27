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
- [x] Watch-the-clip test (Sam's Y 27 Nov) built and scored blind: notes/seeing-test/scores-watch.md.
- [ ] Check the watch test's flags in passed moves at full size (real or misread), then one plain table for Sam,
      one line per tool; his yes/no per winner, one at a time.
- Not duplicated: check-knows-intent option 1 (R8, notes/check-audit.md) is about intent lists for the picture
  checks; this job only adds ways of looking.

## Branches the start listed
- claude/brexit-chat39 (0 h): Open Wounds' live chat 39, left for that chain (film work, pushed by its own chat).
- claude/upbeat-dirac-w16tn9 (0 h): a live chat's plain-words log and waiting-list archive; not this job's, left for it.
- claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: GTA's, named
  and left by earlier chats (notes/check-audit.md, notes/next-jobs.md); nothing this job needs.

## c10 settled (chat 3, 27 Nov)
Posted GTA vertical matched to the c10 re-draw frame by frame (posted = c10 time minus 1.85 s). At full size, at the
three moments every judge named (posted 19.17, 19.67, 20.08 s), Jason's legs stay hidden behind the door: his
trousers show only in the open window above the door's top edge; his arm hangs over the outside as it should. In the
version Sam flagged (c06, 21.33-22.75 s) the trousers bulge out below that edge. Picture: notes/seeing-test/c10-door.jpg
(top: c06, Sam's note 8; bottom: posted). So the c10 door flag is a FALSE ALARM from the small six-frame pictures.

- claude/lucid-pasteur-qol4oi, claude/jolly-ramanujan-2lcl2o (chat 3 end): live chats' plain-words logs and a
  cost-spike proposal; not this job's, left for them.
- Kit change (chat 3): only seeing.py gained the watch sheets (new functions; nothing old changed but vehicles left
  out of the new outlines) and kittests.py gained seeing_watch_shows_every_frame. Both seeing tests run green; the
  full kit check waits for the next film's end, as CLAUDE.md sets (kit tests at a film's start and end).

## Open
- The who-is-where copy sees only what is drawn through the engine's layer recorder (cover.py: places pieces, the
  people kit's people, arms and heads) or a sorted item list (GTA's street). At these versions it could NOT see the
  wolves (drawn by their own code) or the people/arms of GTA's 3D Jason separately from the car's inside; those show
  as faint grey picture. A film that wants this view needs its own-drawn things wrapped (cover.thing).

## Where things stand (27 Nov, seeing test chat 3)
- Rules that bite next: Statement Two (say plainly what the test can't do), 93 (advice only), "Messages to me".
- Done: watch sheets built (seeing.py watch: every frame, 8 a sheet, people outlined, close-up of the busy part;
  kittest seeing_watch_shows_every_frame PASS). Blind score (scores-watch.md), same brief both arms: watch caught 6
  of Sam's 14 notes vs plain 3, but flagged 17 things in the 5 passed moves (plain 5) and 46 extras (plain 12).
  c10 settled: no door fault in the posted film (false alarm from small pictures; c10-door.jpg).
- Next: chat 4, Opus, medium effort (deciding from a clear plan). Look at full size at the 17 passed-move flags and
  a dozen extras (scores-watch.md lists them): which are real faults Sam let pass, which are misreadings. That
  decides if the watch test is noise or a real gain; then the plain table for Sam with one numbered question.
- Needs Sam: nothing until chat 4 has checked the flags.
- Read: this file; scores-watch.md; findings/watch.md (only the flagged lines); key.md.
- Open rule requests: none.
- For Claude: re-render as chat 2 (git worktree per commit; seeing.py render CASE --film MOD --span T0 T1 --src
  WT/source), then `seeing.py watch CASE`; GTA cases ~14 min each, run 4 at once; render c01 alone first (it
  downloads the body model). Old commits' GTA code races that download if two start together.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 4.1% of a week (2026-11-27)
