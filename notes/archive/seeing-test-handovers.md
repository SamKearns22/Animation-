
## Where things stand (27 Nov, seeing test chat 1, red)
- Rules that bite next: 93 (advice only), Statement Two (say what can't be done), "Messages to me" (one plain table).
- Done: seeing.py built, kit test green; 16 cases rendered from the versions Sam saw; all five blind judges' answers
  saved (findings/). First read (unscored): judges found GTA's door fault (note 8) in every arm; most others found by
  no arm; only who-is-where and movement judges said their view (not the plain frame) showed them anything.
- Next: Opus, medium effort (scoring needs judgment, from a clear plan). A fresh scorer helper gets ONLY key.md and the
  five findings files relabelled A-E (shuffled; not which tool) and marks each finding caught / other real / wrong,
  and each key note caught or missed; then one plain table for Sam (one line per tool, plus the plain-frames
  baseline), Lost/Added lines, and his yes/no on each winner one at a time (touching, then movement).
- Needs Sam: the chain stopped (this chat is at the chat-chain depth limit, 8, and cannot open chat 2). Sam starts
  chat 2 with the text in notes/seeing-test/next-prompt.md.
- End check, named (not this chat's): STOP RULE: CLAUDE.md's "Never tell me my chats are long (Sam, 26 Nov)" came
  in from the main line with no rule_proofs.json entry (another chat added it); chat 2 adds its proof or names its owner.
- Read: this file; notes/seeing-test/key.md; findings/; CLAUDE.md "Messages to me".
- Open rule requests: none.
- For Claude: worktrees for re-rendering: `git worktree add /scratch/wt-COMMIT COMMIT`; then
  `python3 source/seeing.py render CASE --film MOD --span T0 T1 --src WT/source` and `seeing.py views CASE`.
  Models fetched on demand into source/models/ (not on GitHub).


## Where things stand (27 Nov, seeing test chat 2)
- Rules that bite next: Statement Two (no tool beat plain frames: say so), 93 (advice only), "Messages to me".
- Done: blind scoring (notes/seeing-test/scores.md). Of 14 notes Sam gave: plain frames 2, pose 2, movement 2 (with
  6 false alarms), who-is-where 1, cut-out 1. Every arm caught GTA note 8 (door); none caught the other 11. No
  tool beats the plain frames, so no winner is adopted.
- Next: chat 3, Opus, high effort (building something new). Sam said Y (27 Nov): drop the four views as checks; build
  the watch-the-clip test. Honest limit: the model sees pictures, not video, so "watching" means short runs of
  consecutive frames side by side (every frame, a few seconds), each person outlined; scored blind on the same 16
  cases against plain frames, same scorer method (scores.md). Also settle c10 (posted GTA, door) on a real frame.
- Needs Sam: nothing until chat 3 scores the new test.
- Open, unverified: all five arms flag Jason through the door in c10 (posted GTA final); not matched to a frame.
- Read: this file; notes/seeing-test/scores.md; key.md.
- Open rule requests: none.
- For Claude: re-render: `git worktree add /scratch/wt-COMMIT COMMIT`; `seeing.py render CASE --film MOD --span T0 T1
  --src WT/source`; `seeing.py views CASE`. Letter map in scores.md.

