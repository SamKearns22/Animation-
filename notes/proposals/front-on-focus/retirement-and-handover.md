# Front-on focus: retirement candidates and Where things stand (job 1, 19 Nov)

## Retirement candidates (job 1's light survey; each its own Y later, archived not deleted; the judge's C5 confirms them from L2 and the ledger)
| # | what | who still uses it | if archived: Lost / Added |
|---|---|---|---|
| R1 | 3D MakeHuman stack (sdf3d, mother, daughter, shot, mhuman, graphite, hair, rig, kitchen, props, mh_lab, checks, character, clothes, horror_preflight, materials, concept_mother; ~4,300 lines) | no film file; no posted film found | Lost: the 3D look experiments (recoverable). Added: ~4,300 fewer lines for chats to wade through |
| R2 | hands3d.py (517) | none; guides/figure-rig.md line 137 already says "retired" | Lost: nothing used. Added: the guide and the code agree |
| R3 | `head: measured` (people_famous) | Blessed's finished frames (kittest people_from_a_description) | Lost: Blessed re-renders on the old head unless kept for it. Added: one head route for famous people. Keep for Blessed, marked "kept because" |
| R4 | `head: part walliams` (people_walliams, blessed_walliams) | Blessed (test only, its MAP says) | as R3: keep, marked, for Blessed only |
| R5 | people_turned.py (invented people turned) | Milburn, Protest Tiers (finished) | Lost: nothing new once C1/C2 are in (front-on default). Keep for the two finished films, marked |
| R6 | labs: trial_lineup, trial_link, ll_looks, ed_variants, protest_tiers_roughs, ai_tells_lab, horror_trailer_music (~5,000 lines) | no film; trial notes only | Lost: the studies' code (results kept in notes). Added: less noise |
| R7 | long-red kittests facehouse_whole_head, round_page | red since 15 Nov | fix, not retire (job 3 takes round_page; F5 above) |
Not tools: park.py, duel.py are finished film files and stay (corrections.md).

## Sam's answer (19 Nov, evening)
"Y to all. Do we have a plan for if we actually do need a 3/4 pose?" Read as: Y to L1-L3, C1-C5, and the retirement list (archive, never delete; R3-R5 kept, marked "kept for Blessed / Milburn / Protest Tiers"; R7 fixed, not retired). His 3/4 question was answered, not acted on: the real turn stays for walks, exits, backs and any shot with a written reason; a 10-15 degree turn comes free with C2; a true 45-degree turn still uses the face tool's turned head, which keeps the faults in famous-turned-now.jpg (thin far glasses, flat hair, long neck from behind). Proposed fix (needs its own Y): the first film that truly needs one fixes those three faults on the turned head, critiqued alone first (rule 89), and the 18 Nov three-quarter steps 2 (torso) and 3 (cast-sheet tile) are done with it.

## Chat 2 record (19 Nov, Opus high)
- C1 built: pre-flight reads the drawn angle on every film (posecheck.set_marks now in install_probes, so the animatic's drawing pass checks it too; before, it was never set during a render); three frames per marked shot drawn before any animatic; a CAST key matches the drawn name; head turns count. Milburn: all four in scenes 3 and 6 flagged at 40 degrees, plus Andy at 29 in 4c. Clean and matched: ad_vanced_notice, midterminal, patriots4, terfwarts. halo_no_no: COULD NOT TEST (Musk not drawn by name through the kit). Kittest drawn_angle_every_film.
- C2 built: focus.py (focus -1..+1, focus_tilt, focus_turn, focus_eyes) in facehouse._head and people_parts._front_head; the far eye and lens stop at the outline (Andy's glasses); acting.py `keys focus` (eyes lead 0.17 s). focus 0 identical (kittest focus_front_heads: Andy, Kemi, Milburn 5 s and 32 s, Protest Tiers 3 s).
- Critique (rule 89), two hunts, no third: both said the look does not read at phone size in a whole-body medium shot. Hunt 1 at 60% of a real turn; raised to 85% with stronger pupils; hunt 2 still "barely". Named to Sam with the sheet (focus-sheet.jpg). Not focus faults (existing designs, named): goth's short neck and black sleeves, crop at the shins.
- Kittests: facehouse_whole_head green again (re-held: both heads changed only at 594f94ba, Sam's 14 Nov shadow removal). places_from_a_description and moves_from_the_acting_list fail only because milburn.py uses those kits without a recorded Y (named in the watcher).
- Start check settled: the 17:18 cross-session correction (chat 1's brief was in a scheduled task) and Sam's 17:36 "simple communication tool isn't working, not following your explanations" were chat 1's; the plain-words rule now at the top of CLAUDE.md answers the second.

## Where things stand (job 1, 19 Nov, chat 2 end)
- Rules that bite next: 38 (front on: the drawn-angle check now refuses), 89 (critique), 13 (exceptions listed).
- Done: C1 and C2 built and tested; sheet focus-sheet.jpg sent to Sam with the phone-size fault named.
- Next: chat 3, Sonnet medium: L1 (Milburn and Protest Tiers turned seconds), L2 (blind route-pick test), L3 (the goth on both heads, now with focus; sheet to Sam). Then Opus: C3, C4 from their results; archive R1, R2, R6 after a last search.
- Sam (20 Nov): "Show 1" = show him option 1 (a stronger look: eyes, nose and mouth move further) as a sheet before any change is kept; his Y to keep it comes after. Opened chat 2b (Opus medium) for it.
- Needs Sam: his Y or N on the stronger look once chat 2b sends the sheet. RESERVE JOB "Fix the half-turn heads" (Sam, 19 Nov: keep in reserve): the turned head's three faults (thin far glasses, flat hair, long neck from behind), critiqued alone; about 2-3% of a week, Opus high; starts only when Sam says "Fix the half-turn heads".
- Read: job pack "A tool job"; notes/proposals/front-on-focus.md "Final version"; this file's chat 2 record.
- Open rule requests: none found.
- For Claude: focus.py MAP; posecheck.turn check in preflight.turn_sample; kittests drawn_angle_every_film, focus_front_heads. Main-line branch claude/create-claude-md-oe8z4g; this chat's branch claude/front-on-chat2. Branches named, not merged: claude/aim-check-study-oe8z4g (another chat's), claude/blessed-c2-mics-wip (stays off). The shared proposal-route ledger has no estimate, so no cost line (named, not this job's to set); this chat about 2% of a week.


## Chat 2b (20 Nov, Opus medium): option 1 shown
- Built behind a switch that is OFF (focus.py: sp['focus_strong'], STRONG_K 1.7, STRONG_LOOK 1.4; `focus.py compare OUT.jpg`). Under it, when the far-side room limit holds the far eye/lens, the near side keeps today's spacing so glasses keep their shape (first try squashed Andy's glasses).
- Sheet sent: stronger-sheet.jpg (0.2 MB). Kemi reads clearly; Andy less (his glasses hold the far side). kittest focus_front_heads passes.
- Rule 30: first strength fell short because it was 85% of a real 15-degree turn, and at whole-body phone size the face is about 50 points wide, so the slides were a few points.
- Named (handover start): the message saver missed 1 of Sam's messages in chat 2 ("Show 1", 20 Nov); its words are recorded here and in Where things stand.
- Needs Sam: Y (keep stronger as the default) or N. On Y: make focus_strong the default (or set STRONG on), re-run kittest, push.
- Sam (20 Nov): "The stronger look is not good. The facial features have slid over so far that they no longer look human. Keep the original". Done: the stronger setting and its sheet code removed from focus.py; today's strength kept (a comment there records the refusal). Lesson: past about 85% of a 15-degree turn, sliding features inside a fixed outline stops looking human; any future fix for reading at phone size must move something other than the features (option 2's body lean, untried).
- Fault named (not this job's): kittest focus_front_heads fails on 'milburn 5' on the main line since the Grand Theft Autism kit additions (people.py + people_parts.py together; restoring both to d732ceea passes). Told GTA chat 7 (session_01J1JB7ZbCDC2svB5sx76FTn) to fix it.
