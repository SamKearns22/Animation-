# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## Quick videos (about 5% of a week)
- `guides/quick-video.md` is the whole recipe for a short two-person film (one brief file `prompts/NAME.json`,
  `source/quick.py check | sheet | final`; copy `prompts/quick-example.json`). One sheet, one final, no animatic.

## Done: "Russiadent Evil" (TikTok, `prompts/russiadent-evil.md`)
- **Finished 7 Oct:** `animations/russiadent-evil-vertical.mp4` (28.6 s, 1080 x 1920, 5.0 MB). Sam's voice from
  `source/audio/russiadent-peskov.m4a` (recorded outdoors: cleaned in `rec_lines`). Title on 2 s; circle hands.
- Peskov calmly denies the Irkutsk plague-lab death; behind the camera a zombie outbreak tears through his press
  conference. Code: `source/russiadent.py` (`sheet`, `stills OUT_DIR T...`, `times`, `animatic`, `final`). One plan
  for the press room drawn by perspective cameras in the plan (`PCam`): shot 2's 180 is the same room. Placeholder
  timing at Sam's pace (`LINE1`, `LINE2`, `T`); all sounds made in code (screams, roars, crunch, splats, slap).
- Director's decisions: no hint before the 180 except the hand slapping onto the podium edge (~5 s); English website
  line under a Russian "Ministry of Health" header (no emblem, `health.gov.ru`); the severed arm holds a microphone;
  a 0.6 s beat after "Any more questions?"; title RUSSIADENT / EVIL on two lines (no slash), gone by 1 s; real terror
  on the reporters' faces (wide eyes, pinprick pupils, screams with the corners pulled down, drained skin); more
  zombies: packed several deep at every window, back and side doors burst open; Peskov's reference photo (press
  agency) used but not stored in the project.
- **Hands:** close-up hands are built on MakeHuman's real hand and drawn flat (`source/hands3d.py`; see figure-rig
  5c): the phone grip (shot 4), the hand on the podium (shot 1), the fist round the microphone (shot 5).
- Next: Sam's notes on the animatic; his recordings `01 peskov.m4a`, `02 any more.m4a` (run voices.py), then the
  final render as `animations/russiadent-evil-vertical.mp4`.

## Done: "DLC" (The Bayeux Tapestry Season Pass) (TikTok, `prompts/bayeux-season-pass.md`)
- Sam's references in `references/bayeux/` (list and the swap rule in its README: each original weapon deleted
  completely, the new one stitched in the same hand and place).
- Proof-of-concept animatic sent 5 Oct 2026 (15.3 s, 1080 x 1920, 24 fps, 11.3 MB; render 70 s on 4 cores, not saved
  in `animations/`): gallery and title (gold BAYEUX / TAPESTRY, each Y two flaming arrows, SEASON PASS in fire),
  NEW WEAPONS, then the pan along the tapestry: rifle, ice claw, ghost pistol (ghost + WOOOOOO!!), stapler (riser,
  huge reveal, one flat click), title slam, hard cut. No voice yet (Sam to record); text slams carry the words.
- Code: `source/bayeux_stitch.py` (traces a reference into the tapestry's wools and re-stitches it: laid-and-couched
  fills, outlines, linen weave), `source/bayeux_weapons.py` (erase masks and the four new weapons; `build` stitches
  every scene into `source/data/bayeux/`, not on GitHub, ~1 min), `source/bayeux.py` (`stills`, `animatic`, `final`).
  Fonts: Cinzel Decorative Black and Cinzel (OFL) in `source/fonts/`.
- Concept v3 sent 5 Oct (18.9 s, 14.5 MB, render 92 s): the room rebuilt as the London 2026 exhibit (Sam's
  `london-2026-exhibit-*.jpg`: tapestry lying almost flat in long low glass cases, black wall with glowing blue line
  drawings and captions, warm floor light strip); title held 2 s longer (`D` in bayeux.py); after the stapler's reveal
  the glory fades (`STAPLER_FADE`) and it fires one staple into the messenger's forearm (`STAPLER_CLICK`, `STAPLE_HIT`).
- Concept v4 sent 5 Oct (26.3 s, 23 MB, render 121 s): NEW SKINS added after the staple (William: PARTY SUIT,
  Harold: SHARK WARRIOR, Edward: ELECTRIC MOUSE; `SKINS` in bayeux_weapons.py: each figure's face and hands copied
  back over the new costume ('show'), club/arrow/sceptre redrawn in front). Sam's rock track
  (`source/audio/bayeux-rock.mp3`, a Pixabay-style download Sam supplied: confirm its licence before posting) plays
  from the moment SEASON PASS ignites, drops out for the stapler's silence and returns for NEW SKINS.
- Concept v5 sent 5 Oct (37.7 s, 30.6 MB draft, render 162 s): opens straight on the title (`START` trims the
  first 0.85 s; INTRODUCING removed); bigger gold names on the skins; Edward's whole face shows through the hood;
  the shark costume solid to the feet with his shield stitched on top. NEW STORY CHAPTER / BAYEUX: ENDLESS CONQUEST:
  three new stitched scenes (`source/bayeux_story.py`, `build` ~40 s): 1066 coronation (William in his party suit
  with a crown, guards with rifle and ghost pistol, Saxon houses burning), 1069 Durham (claw and ghost riders storm
  the gate, the bishop's palace burns over sleeping Normans, two run away), 1086 Domesday (William, the book, three
  tax collectors with staplers, staples everywhere, villagers, sheep, ox). Sam's chapter message was cut off at
  "You must render the fll": ask what the rest said.
- Concept v6 sent 6 Oct (45.3 s, 23.6 MB draft, render 3 min): chapter slowed (`CH_LEN` 5.4 s a scene, the logo held
  2.5 s); ENDLESS CONQUEST in fire like SEASON PASS (`burn_text`); movement: William dances (a separate stitched sprite,
  `draw_sprites`/`dance`), tax collectors jolt with each shot and staples fly and land, plasma bolts into the houses,
  ghosts fired from the pistols (`SHOTS`, `chapter_action`), each with its sound. Stitching repaired by hand on the
  ghost-pistol and ice-claw riders (`REPAIRS` in bayeux_weapons.py). White flash at the start fixed: the shake wrapped
  the picture's bright left edge round to the right (`shove` now repeats the edge instead).
- Concept v7 sent 6 Oct (45.3 s, 23.5 MB; plus a Discord copy 720 x 1280, 9.4 MB, two-pass, for Discord's 10 MB
  limit): chapter figures cut out by their own shape (`cut` in bayeux_story.py: seed points, joined stitching
  only, small gaps kept), no slicing and no leftovers; the Ice Claw rider redrawn whole, charging right with the
  claw thrust forward (`charging_claw_rider`); Domesday crowded with the country's resources (two fields of
  people, pigs, goats, sheep, oxen, a cow, a horse, hives, a cart, barrels, a mill, a plough), staples on all of
  it; border repeats joined at their plainest columns. Still open: Sam may send a real tapestry tree to replace
  the invented divider tree (`tree_image` in bayeux.py).
- Concept v8 sent 6 Oct (50.3 s, 24.7 MB; Discord copy 9.4 MB): new ending after the title slam (`end_card`):
  AVAILABLE NOW, 1,066 CROWNS, a stitched "M / MEDIEVAL" rating box with "Mild Pillaging / Fantasy Ghosts /
  Excessive Stapling", TAPESTRY SOLD SEPARATELY; then a hard cut to the silent gallery where one staple pings off
  the glass (`final_staple`, tink), then black. Everything drawn now looks hand-sewn (`wobble` in
  bayeux_weapons.py: edges nudged, thread width varies). Sam: no voice, keep the length; he will send a real
  tapestry tree for the divider.
- Series title added 6 Oct (51.0 s, 25.0 MB; Discord copy 9.4 MB): DLC in the standard cranberry title
  (`series_title`, burnham.title_lines, capitals 148 px, top 395) over the quiet gallery for the first 0.8 s, then
  the gold logo crashes in (`START` 0.15, `T_DLC_OUT`). Cover: about 0:00.4 (DLC over the gallery).
- Real tree 6 Oct (51.0 s, 25.0 MB): the invented flower-tree replaced by Sam's real tapestry tree
  (`references/bayeux/tapestry-trees.jpg`, traced and stitched, 72% of the band, never squashed; scene gap DIV 330).
  Sam: no more Discord copies unless asked.
- Cover frame 6 Oct (24.7 MB): DLC now appears on frame 0 only (`cover_frame`, 1/24 s) so the film still opens
  straight into the logo; choose the very first frame as the TikTok cover.
- 6 Oct: the Ice Claw arm in 1069 swings back and forth from the shoulder (`claw_arm` drawn as its own sprite,
  `drawn_sprite` with a pivot); 1066 archer and ghost-pistol rider cut out whole (wider outlines, `nots` to drop
  the old bowstring and spear, the horse's rump closed by hand).
- TikTok version 6 Oct (49.3 s, 24.4 MB, 3.3 min): rendered with a 1 s shorter title hold: `BX_HOLD=1.0 python3 source/bayeux.py
  final OUT.mp4` (default 2.0 is the full version; every later time moves with it, `E` in bayeux.py). Simply
  cutting a second out of the finished film made the picture jump (camera drift and flames skip), so never do that.
- FINAL 6 Oct: `animations/bayeux-season-pass-vertical.mp4` (TikTok version, 49.3 s, 1080 x 1920, 24 fps,
  10.0 MB two-pass copy of a 24.3 MB render; render 3.2 min: `BX_HOLD=1.0 python3 source/bayeux.py final OUT.mp4`).
  Sam reverted my wider pass of fixes and kept only four: William grounded (sways and dips about his hooves), the
  1066 horse's back half, the Ice Claw rider's torso redrawn (face kept), and the new party suit (tapered leg,
  flared jacket, cowboy boot, fluffy boa). Everything else as in the version before. Cover: the very first frame (DLC). Hashtags discussed: #bayeuxtapestry #historytok #gamingmemes
  #animation #parody. Check the rock track's licence before posting.
- Posted 6 Oct 2026, 5:35pm. After ~2.5 h: 175 views, average watch 7.3 s of 49 (15%), 3.8% to the end, 8 likes,
  8 comments (all from one person), 0 shares, 1 save, 0 new followers. People Sam showed it to personally rated it
  his best film. Likely cause: the first ~5 s are a convincing game-logo sequence (reads as an advert, swiped
  before the first swap at ~5.5 s; stapler payoff at ~13 s). Sam decided to move on rather than re-cut it.
- Electric mouse: kept generic (Edward's own face, our wools, no name or copied artwork); Sam's character picture
  deliberately not stored in the project.

## Done: "The Patriots 2" (TikTok, the letter to the RNLI, `prompts/patriots-2.md`)
- Posted Mon 5 Oct 2026 at 1pm, the day of another RNLI/small-boat protest (Gosport). Cover around 0:05. Check the
  retention graph next day (watch the 12 s opening shot and the doctor's speech).
- After ~1.5 h: 255 views, average watch 14.8 s of 60 (25%), 14% to the end, 15 likes (~6%), 6 comments, 0 shares.
  Likely causes: #Smallboats (sensitive topic, limits reach; was on the avoid list), the 60 s length with the first
  laugh at ~23 s (TikTok rule: 15-30 s, first payoff by 8-10 s). Advice: no re-post; remove #Smallboats if editing is
  offered; check the retention graph next day; a 30-35 s cut is possible for a later post.
- DONE 4 Oct 2026: `animations/the-patriots-2-vertical.mp4` (59.5 s, 8.3 MB, 1080 x 1920, 12 fps). Animatic about 4 min,
  final render 20 min on 4 cores. Checked against the safe-area guides (title, widest caption, busiest frames).
- To post: cover around 0:05 (him lit by the screen, mid-letter, title gone). Avoid #heartattack and #NHS (they give
  away the turn) and #smallboats, #migrants, #illegalimmigration (strictest moderation, limited reach).
- All code in `source/patriots2.py` (`stills`, `sheet`, `animatic`, `final`, `times` prints the timeline). Shots: his
  room (one unbroken push-in, title over the dark room), lifeboat, dinghy, his room from the screen (collapse), ambulance,
  rushed through the A&E doors, pushed fast into the ward ("heart attack, Doctor"), the doctor's speech (the ward camera
  moved in: one shared ward set, `WARD_TX` / `WARD_DOC`), alone on the trolley (same ward), hard cut to black.
- Sam's recordings: `source/audio/patriots2-*.m4a` (protester-1 Dear RNLI, -2 courage, -3 people I don't like, -4
  traitors, -gurgle; paramedic-1 taxi, -2 heart attack; doctor-1 the whole speech; protester-choke his strangled noise as his eyes cross). Cleaned and levelled with `mossad_audio.line`; `REC` in patriots2.py says which stretch
  plays and where each caption piece starts (on Sam's pauses). Every sound of a voice is Sam's own.
- Director's decisions: no keyboard insert (the push-in runs through); legs on everyone always; urgent rush through the
  doors into the ward before the deadpan; the doctor redesigned so he doesn't resemble Andy Burnham (cropped sandy hair,
  short beard, round face, thin dark glasses); doctor's line "This man's life is clearly in serious danger".
- Could be shortened by tightening Sam's longest pauses (about 3-4 s) if the retention graph asks for it.

## Done: "Mossad" (TikTok coffee-shop parody, `prompts/mossad.md`)
- DONE 3 Oct 2026: `animations/mossad-vertical.mp4` (30.1 s, 2.2 MB, 1080 x 1920, 12 fps; final render 14 min on 4
  cores, animatic 3 min). Checked against the safe-area guides (title, widest caption, the bang).
- All code in `source/mossad.py` (`stills`, `sheet`, `animatic`, `final`, and `resound SRC OUT` to put a new
  soundtrack on an existing render in seconds). Cleaning and levelling of Sam's lines: `source/mossad_audio.py`
  (hum and hiss reduced by at most 10 dB, every line at the same loudness, nothing else). Timeline, captions and
  cuts: `LINES` / `SHOTS` at the top of mossad.py. Recordings: `source/audio/mossad-*.m4a`.
- Captions follow Sam's words: "can I please order a latte with caramel syrup", "Of course you can",
  "Errm... excuse me?", "actually doing a promotion at the moment with Mossad", "my drink is ready".
- Director's decisions: October 7th and 9/11 written plainly; explosion a real shock in the flat style, not Looney
  Tunes (flash, ragged fireball, dark smoke, plastic bits, a jolt; cut three-quarters through with the sound);
  customer 2 neutral, glancing about; the pager is a small upright café pager ("17"); Coffee Queens on the apron and
  menu board; patron 2 sips just before the bang; no flags in the customer's shots, only behind the cashier;
  12 oz cups stacked wide end down; everyone has legs; camera on the customer right at the counter; no café
  murmur or street rumble at all (only clinks, typing, machine, steam, one car, buzzer, bang); the cashier acts with
  her face (serious on "defend itself", wide-eyed on "did you know", hand on heart for "my opinion"); the barista
  pours milk in shot 2, steams frantically in shot 4.
- Posted 4 Oct 2026, 9:02am. After 6 hours: 6,906 views, average watch 17.1 s of 30 (57%), 37.3% watched to the end,
  272 likes (~4%), 7 comments, 19 shares, 17 saves, 9 new followers. The opening rules work (first posts: 3.6-4.6 s).
  Weak spots: few shares and comments; many leave mid-film, probably in the 16 s single shot on the cashier
  (0:11-0:27). Check the retention graph to confirm.
- To post: cover around 0:04.5 (the cashier mid-smile, flag cups behind her). Avoid #oct7, #october7, #911,
  #pagerattack, #pagers and #explosion: they give away the ending and draw the strictest moderation.

## In progress: TikTok versions of the rap battles (SAM and ANDY)
- Director's decision (2 Oct): TikTok versions of `animations/sam.mp4` (title SAM) and `animations/andrew.mp4`
  (title ANDY), with the same title and look as the other TikTok films.
- `source/rap_vertical.py andy|sam stills OUT_DIR T...` or `render OUT.mp4`: draws the widescreen picture clean
  (no old subtitles), enlarges it by a third into 1080 x 1920 with edge-glow pads, and draws the standard title
  (first second), captions (700 px, centred) and UNINTELLIGIBLE flashes fresh. Every caption checked to fit.
  Next: look at stills, then render both (about 0.7 s a drawing: roughly 25 min for ANDY, 18 min for SAM).

## In progress: "The Patriots" (TikTok, file name pee-pee)
- TV street interview at a Dover border blockade; masked protester, reporter with a BBQ mic flag; his arm badges
  "PP" and a felt-tip doodle (the other PP). Hope Again look, vertical. All code in `source/peepee.py`
  (`animatic OUT.mp4` about 3 min; `final OUT.mp4`). Timeline and captions: `LINES` / `SHOTS` at the top.
- Director's decisions: title THE PATRIOTS (small, gone by 2 s); mic flag BBQ (like BBC); protester thick-set with a
  belly, same height as the reporter; the childish line captioned in plain italics; no blurred version needed;
  storyboard skipped (low on usage). Ends on the two-shot hold (her slow blink, a distant horn), hard cut to black.
- Notes after the animatic (all done): captions centred on the frame (700 px wide); doodle filled with a Union Jack
  with a yellow stream; officer relaxed (hands clasped), clear of the protester; one small brown wheelie case with a
  front pocket (the left case removed); big title like Dam / L&L (720 px, gone by 1.6 s); reporter given lipstick,
  lashes and blush. Sam's recordings: `audio/pp-protester-1.m4a`, `pp-protester-2.m4a`, `pp-reporter.m4a`.
- Continuity fix (1 Oct): one shared set for both cameras; the reporter's single is the two-shot camera zoomed in
  (`CAMS` in peepee.py), so the officer, reporter, family and case, protester and mates keep the same order in every
  shot; the officer stands with his arms at his sides so his lettering never crosses them. Re-render 21 min.
- DONE 1 Oct 2026: `animations/pee-pee-vertical.mp4` (19.2 s, 1080 x 1920, 12 fps). Final render 16.5 min on 4
  cores. Captions use the script words; check against the recordings if Sam changed any. Cover: around 0:00.5
  (him mid-line, thumb out) with THE PATRIOTS as cover text.

## In progress: "Hope Again" (TikTok parody, `prompts/king-of-the-north.md`)
- Conference speech that turns into the "King in the North" scene, 11 shots, 43 s, Listening & Learning look,
  made vertical. Pictures: `source/burnham.py` (cast, armour, shots, storyboard sheet). Timeline, sound and
  render: `source/burnham_film.py` (`animatic OUT.mp4` about 8 min at half size; `final OUT.mp4`).
- Sam's recordings: `source/audio/burnham-line.m4a` (the speech), `source/audio/king-shouts.m4a` (four shouts:
  1st lowest = old knight, 2nd highest = young woman, 3rd = Miliband, 4th = Sikh knight). Crowd, swords,
  drums and horn are made in code; no show music.
- Director's decisions: title HOPE AGAIN; the only emblem is Manchester's bee; knights keep conference
  lanyards; standing ovation in waves (one, a few, all); Miliband stays seated then stands and bellows;
  all five ministers (Streeting, Rayner, Miliband, Mahmood, Healey) in varied armour in the front-on sword shot;
  ends on a slow push-in on Burnham's face with war drums, hard cut to black. Captions must be accurate.
- Notes applied after animatic 1: voices play exactly as recorded (gain only, no echo, no pitch change);
  captions follow Sam's actual words ("they were the ones who gave it away...", "KING OF THE NORTH!");
  clapping only (no crowd murmur); ending music made in code (original, ominous and regal: D minor strings, brass, low choir, timpani; replaced the battle sounds);
  Andy gestures (points, air quotes, wagging finger, hand on hip); knights each salute differently;
  the king is royal (crown, dark fur, gold chain, gilded breastplate); title centred on the frame.
- Later notes: mouths follow each voice; no bobbing fists or sword sounds; natural clapping; chant carries on
  under the close-up; lanyards on every audience member; two great bee banners in the turned hall.
- DONE 30 Sep 2026: `animations/king-in-the-north-vertical.mp4` (38 s, 4.3 MB, 1080 x 1920, 12 fps), checked
  against the safe-area guides. Recut to the new TikTok opening rules: title at the standard size (as Dam and Listening & Learning) on the
  opening frame, gone by 1 s, over a tilt down from the backdrop to Andy; speech from
  the first frame, pauses tightened (`PIECES` in burnham_film.py), first knight at 15.6 s. The king grows
  harrowed (rings, bags, heavy lids) through the final push-in. Full render about 32 min on 2 cores.
- To post: cover around 0:09 (Andy pointing) with HOPE AGAIN as cover text. Avoid Game of Thrones hashtags:
  they spoil the turn. Sam writes the post text and pinned question himself.

## Done
- **The Salt for TikTok** (1 Oct 2026): `animations/the-salt-vertical.mp4` (11.6 s, 6.7 MB, 1080 x 1920, 12 fps,
  drawn natively at full size; render about 1 minute on 4 cores: `python3 source/salt.py vertical OUT.mp4`).
  salt.py now uses `source/pencil_cartoon.py` (the 24 Sep version of pencil.py, restored under its own name;
  beaver_asteroid.py and rap.py still import the old names from pencil.py and would need the same switch).
  Tightened timeline: her line from 0.32 s, cut to him 3.4 s, "Of course!" 3.8 s, 1.1 s deadpan, whip 6.05 s,
  slap 8.9 s, crash 11.0 s (pats, wind-up and slap keep their old rhythm). Full-size title (letters ~200 px tall, the same as Dam, at Sam's request) on screen for the first second only; captions
  wrapped and balanced inside the safe area. Fixes: coat of arms redrawn (pewter shield, crossed pickaxes,
  salt cube, coronet, ribbon), candle flames sit on wicks, wrought-iron chandelier, shelf brackets, no seams
  in floor/ceiling/ramp, rug/curtains/window toned down, wide shot reframed so the crash is inside the safe
  area (camera close to the original framing so the floor still ends just behind her chair; her face sits on the bottom edge of the safe area during the crash). Cover: her mid-line at about 0:01.6 with the full-size title. Director skipped the stills and
  animatic sign-offs for this one.
- **Animation test (6 s + 1.5 s black):** Shots 1-3 of `story/animation-test.md`, rendered and assembled
  with the trailer score (THUD on the cut to black). Recipes: `source/shots/s1_chop.py`, `s2_daughter.py`,
  `s3_closeup.py`. Sound: `source/animation_test_audio.py`. Joining drawings into video: `source/assemble.py`.
  Finished video: `animations/yuletide-animation-test.mp4`.
- **Look book** (`lookbook/`), **tone guide** (`guides/tone.md`), **premise and title cards**
  (`story/yuletide.md`).
- **Hair simulation** (`hair.Sim`, switched on by `hair_t` in the mother's spec): works, not yet used in a
  finished shot.

## Open
- **FIRST: the mother's right wrist is bent unnaturally in almost every chop** (director's note). Measured
  over every drawing: Shot 1 bends 30-45 deg up/down all the time and sits at the 25 deg sideways limit in
  14 of 32 drawings (every impact and the rest after); Shot 2 35-50 deg; Shot 3 50 deg at the start, fine
  (10 deg) only in the raised hold, where the blade was allowed to tip and turn with her arm
  (`raised_cleaver` in `s3_closeup.py`). A natural chop keeps the wrist within about 20 deg (more only when
  cocked back at the top of a lift) and never at its sideways limit.
  Cause: every recipe fixes the cleaver's angle and the hand's grip on the handle, so the wrist takes up
  all the difference. Fix: in every frame, turn the cleaver (tilt about its edge, pitch, turn about the
  vertical) to suit her forearm so the wrist stays near straight, keeping the edge square across the ham at
  each impact so the slices stay clean; tighten `checks.py` to about 30 deg up/down and 15 deg sideways for
  the chopping hand. Then re-render Shots 1-3 (animatic first) and rebuild
  `animations/yuletide-animation-test.mp4`.
- The girl's neckline reads as a square neck (after trimming her head piece so her shoulder skin no longer
  shows through her top and hair); a round crew collar band would be nicer.
- A check in `checks.py` for skin poking through clothes (a first attempt could not tell it from the
  throat above a collar).
- Speeding up the hair grid build (~90 s per drawing).
- The parting at the mother's crown reads as a squared-off patch, and a faint bright line runs along her
  hairline, when the camera looks down on her hair.
- Next (director): lock a full trailer shot list timed to the finished score
  (`music/horror-trailer-score.m4a`) before building more.

## Working within the budget (director's Claude plan)
- The plan is charged for Claude's work, not render time. Keep sessions short: one piece of work per
  session, then a fresh session.
- Always make a quick animatic (quarter size, no drawing pass) before a full render; look at few images.
- Render in the background and report once at the end.

## Tooling added 8 Oct (for future Filmcow films)
- `source/filmkit.py` (general body/movement audit, `Beats`, joint rules, permanent-marks probe, visible spots), `source/filmcow.py`
  (style kit, used by `park.py`), `source/codemap.py`, `notes/_template.md`, `prompts/_brief-skeleton.md`. Russiadent Evil: pre-flight is
  parallel and runs the audit; the render caches pictures and puts captions and the title on last. Details: `guides/preflight.md`.
- Found by the audit in the finished Russiadent Evil: the zombie that falls through the window pops from lying flat to crawling
  (about 15.6 s). Not fixed (film is finished).
