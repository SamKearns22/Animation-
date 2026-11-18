# milburn: the page a notes round reads (python3 source/page.py milburn; regenerate after any edit)

Read this, then only the lines a note points to (`page.py FILM find "note words"`).


## milburn.py (804 lines)
- 34: HERE (data)
- 42: B (data)
- 43: V (data)
- 48: NAME (data)
- 49: FILM (data)
- 50: NOTES (data)
- 51: HAS (data)
- 52: FPS (data)
- 53: LINES (data)
- 84: _FOUR (data)
- 85: REVERSE (data)
- 86: ACROSS (data)
- 87: SHOT_CAST (data)
- 89: KEEP_CLEAR (data)
- 90: HOOK (data)
- 91: SHOT_MARKS (data)
- 94: `scene_of` 
- 102: `shot_of` 
- 107: PLAN (data)
- 122: BENCHMARK (data)
- 133: CAST (data)
- 134: FEET (data)
- 137: `scale_at` The kit's scale for someone drawn at pxm pixels per metre (their neck base sits at 0.84 of their height).
- 142: `person` Draw `who` standing on sole_y; their face and pose come from story/milburn-moves.txt (the moves kit) when the
- 156: MOODS (data)
- 190: `word_at` When line n reaches `words`: its syllables spread over where the recording really speaks.
- 199: TRACK (data)
- 204: BLINKS (data)
- 207: HEAD_LIFE (data)
- 210: `head_life` Rule 74: Milburn's head tilts and nods on his voice (headlife, from the stand-in's loudness per drawing).
- 227: `face_sp` The moves kit's seam: who's build with the face for a mood, lips on their own lines, blinks.
- 241: _MOVES (data)
- 244: `moves` (the moves file, the film's side) for the kit, read once.
- 252: `acted` (face sp, joints) for who's block in shot at film time t (story/milburn-moves.txt).
- 264: _DESC (data)
- 265: _PAINT (data)
- 269: `cabinet` 
- 296: _RPAINT (data)
- 297: SEATS (data)
- 298: SPLIT (data)
- 301: `reverse` Andy and Pat across the table from Milburn's seat (places view `reverse`), seated as Milburn is in shot 1: the
- 336: `_table_layer` The front layer (table, folders, glasses, name card) on its own, to lay between Milburn's body and arms.
- 345: NEETS (data)
- 348: `shaft_shot` 
- 369: TINY (data)
- 372: `_tiny` 
- 381: `field_shot` 
- 389: FIELD3 (data)
- 391: PLINTHS3 (data)
- 395: `_hoist` 0 -> 1: the goth's crossbow from across her hips up onto her shoulder (lands on "arm themselves").
- 401: `_mix` 
- 405: `_picked` 0 -> 1: how far `who` has lifted their weapon off the plinth (0: it still lies there, their hands on it).
- 417: ON_PLINTH (data)
- 420: `arming` (face sp, joints) for scene 3 (acting list row 3): the weapons in their hands, the moves on line 3.
- 475: YAW3 (data)
- 479: `field_level_shot` 
- 502: FOREST6 (data)
- 505: CLOSE6 (data)
- 506: GOTH_SHOTS (data)
- 507: SKY_SHOT (data)
- 511: `_sky` 0 -> 1 -> 0: the goth's crossbow jerked up skyward on the first gunfire, then lowered again.
- 514: HALT (data)
- 517: `_ramp` 
- 521: `walked` How far `who` has walked (m, across the screen) since the shot began: the camera's pace, stopping dead on
- 534: `_crouch` Lower the body `amt` person units with the feet kept on the floor (knees bend), leaning forward.
- 544: `forest_pose` (face sp, joints, firing) for scene 6 (acting rows 8 and 9): walking with their weapons, the jolt on the
- 638: `forest_shot` 
- 687: `picture` 
- 702: `frame_image` 
- 706: `cast` 
- 711: DUCK_TO (data)
- 712: SFX_GAIN (data)
- 713: _SFX (data)
- 716: `_sfx` One of Sam's sound effects (source/audio/milburn-sfx-NAME.mp3), as supplied.
- 724: `sfx_cues` [(effect, film second it starts, seconds it may run or None, fade out)]: where each effect lands (Sam, 18 Nov:
- 740: `soundtrack` Sam's recordings, cleaned and matched, each where its line starts (the swear bleeped), then the effects at 60%
- 769: `final` 
- 780: `main` 
- 801: `caption_at` The subtitle on screen at t (finish.py burns them in; rule 62), from LINES.

## milburn_forest.py (497 lines)
- 29: HERE (data)
- 35: CAM (data)
- 38: YAW_VIEW (data)
- 39: V_EFF (data)
- 40: STOP (data)
- 43: `cam_x` The camera's travel (m, to the right) since the shot began: walking pace, then easing to a stop.
- 52: END_X (data)
- 55: HAZE (data)
- 56: CANOPY (data)
- 57: LEAF (data)
- 58: BARK (data)
- 59: BARK_D (data)
- 60: EARTH (data)
- 61: EARTH_D (data)
- 62: FLOOR (data)
- 65: `fog` Colour c at depth d: hazier and paler the further off (flat steps, not a gradient per pixel).
- 71: `_P` 
- 77: `items` Every piece of the forest in metres: (depth, kind, x, args, seed).
- 111: AHEAD_GUNS (data)
- 112: NOZZLE (data)
- 113: STAR_PIVOTS (data)
- 117: `_poly` 
- 121: `_blob` 
- 135: `trunk` 
- 162: `clump` 
- 175: `bush` 
- 189: `fern` 
- 218: `mark` 
- 244: `_backdrop` The deep, hazy green behind every trunk: darker up in the canopy (flat bands).
- 254: `_shafts` Shafts of light slanting down through the canopy (flat, pale, see-through).
- 265: `behind` Everything behind the four (RGBA, full size).
- 302: NEAR (data)
- 306: `in_front` The nearest layer at about 1.5 m (RGBA): the undergrowth just in front of the track, ferns and a trunk that
- 324: `class _FxCam` The level camera in prepper_fx's terms: points are (x, up, depth) in metres; px per metre as k.
- 339: `_fx` 
- 344: `gunfire` Flashes in the leaves ahead (screen right) from the gunfire on, one frame each, never all at once; tracers
- 365: `muzzle` A muzzle flash at a gun's mouth (screen X, Y; k px per metre there): the house's lumpy flash.
- 378: `flame` The flamethrower's blast (37.5): a jet whips out of the nearest bush ahead, left across the track at their
- 426: `star_at` (pivot X, Y, ball X, Y, radius px, k px/m) for morning star i at film time t, or None before it drops.
- 446: `stars` The two morning stars: spiked steel balls on chains swinging down out of the trees over their heads.
- 478: `sheet` 

## milburn_props.py (197 lines)
- 20: HERE (data)
- 29: `_rect` 
- 33: `_ell` 
- 37: `_spikes` 
- 48: SHAPES (data)
- 75: SCALE (data)
- 77: LENGTH (data)
- 80: `draw` The prop's parts turned `ang` degrees (0: along +x on screen, + clockwise as y runs down), k per metre.
- 90: `units_per_m` 
- 94: `in_hands` The prop held in hand `a` (its grip in that hand) pointing at hand `b` (or at `ang` degrees when b is None);
- 124: `j2_3` The 2D drawn joints as 3D points (depth 0) for grips.hand_centre.
- 133: `plinth` A grey plinth (1.0 m high, 0.5 m square) at (x, dep) seen by a level camera `cam` (cam.p(x, d, z) in
- 174: `sheet` 

## milburn_sets.py (491 lines)
- 28: HERE (data)
- 33: SS (data)
- 36: `mix` 
- 40: `ease` 
- 45: `_poly` 
- 52: `_line` 
- 57: `class LevelCam` A level camera: height `up` m, horizon row, lens px; x across, d forward from the lens, z up (metres).
- 69: SHAFT_CAM (data)
- 70: R_SHAFT (data)
- 71: C_BACK (data)
- 72: RISE (data)
- 73: CONCRETE (data)
- 74: CONCRETE_LIT (data)
- 75: DECK (data)
- 78: `wall_pt` A point on the shaft wall at angle phi (0 = straight ahead) and height z above the deck -> screen.
- 84: `light_line` The lit edge's height above the deck (m) as the light sweeps down the wall: from high above the frame at t0
- 90: `shaft` The shaft at time t (seconds into the rise): returns an RGB image. `lit_z`: the lit edge's height (m).
- 183: `class TiltCam` A camera `h` m up, `back` m behind the middle of the world (x across, y away, z up), pitched down `pitch` deg.
- 212: FIELD_CAM (data)
- 213: R_RING (data)
- 214: GRASS (data)
- 215: FOREST (data)
- 218: `_peak_range` A range of peaks `dist` m away, up to `top` m high, as one ridge polygon with snowcaps.
- 240: `_tree` One tree standing at screen (X, Y) (its foot), s px per metre: a conifer (stacked tiers) or a round crown.
- 260: `_field_layers` The still parts, drawn once: (back RGB: sky, peaks, hills, the forest beyond the ring) and (front RGBA: the
- 302: `_ground_grid` 
- 309: `meadow` The grass inside the ring at time t: three flat greens; gusts run across it from the left and far side.
- 324: `deck_z` The platform's height (m, 0 = level with the grass) at share u of the rise: up from 9 m down, easing to a stop
- 329: `mouth` The shaft's mouth at the middle of the field and the platform `z` m below the grass, seen from above.
- 365: `tiny_people` Tiny people standing on the deck (z m), seen from above (F8: a few pixels each): `figures` is a list of
- 381: `field` The whole field picture at time t with the platform at height z; `figures`: the tiny people (tiny_people).
- 393: `field_point` World metres in the field -> screen (X, Y) and px per metre there.
- 400: LEVEL_CAM (data)
- 401: R_AHEAD (data)
- 404: `class _Level3` LevelCam in TiltCam's terms (p -> X, Y, depth; horizon) so the peaks and trees draw with the same code.
- 418: `_level_back` Sky, two ranges of peaks, foothills and the forest's edge 150 m ahead (rows of trees), for the level camera.
- 453: `_level_grid` 
- 462: `field_level` Scene 3's ground: the meadow with the same long gusts as the aerial, seen level (RGB).
- 477: `sheet` 

## milburn_voice.py (176 lines)
- 22: HERE (data)
- 23: SR (data)
- 24: LUFS (data)
- 27: TAKES (data)
- 31: GAP (data)
- 32: FUCK (data)
- 33: ORDER (data)
- 36: `_trim` The take with hum and hiss out, cut to the speech (50 ms before, 80 ms after); also where it started.
- 45: `_match_tone` Make the takes sound like one session: each line's tone nudged towards the average, at most 4 dB, no echo.
- 65: `_build` 
- 89: DUR_OF (data)
- 92: `bleeped` The sound of line n: where Sam swears, a 1 kHz tone goes over the word (rule 26).
- 104: `_timeline` Film seconds for every line, shot cut and beat. Gaps between lines are the old film's (dead air already
- 121: LINES_TIMED (data)
- 129: FOREST (data)
- 132: `word_times` [(word, film seconds it is reached)] for line n: the words' syllables spread over where the line speaks.
- 153: `_after` When line n reaches the first word of `find` (a snippet of its text).
- 160: `shots_and_beats` (SHOTS, T, forest times, DUR) from the lines. texts: {n: the line's text}.

## milburn-people.txt (7 people; a note on a person changes their lines)
- 6: milburn (Alan Milburn (Lead: speaks, straight to lens)): body: , shoulders , head x ; skin: hair: side, ; face: brow_high , nose_wide , brow_slope , nose_long , eye_tilt , chin_long , face_wide , lip_top , eye_size ; eyes: lips: brows: , width , thick ; glasses: , thick; outfit: suit navy, shirt white, tie , trousers navy, shoes
- 14: goth (The goth girl (NEET : big blue-purple hair, blooming black dress, pudgy nose, overweight)): body: , shoulders , head x ; skin: pale hair: shag, , big, streaks ; face: face_wide ++, jaw_wide ++, nose_wide ++, nose_long -, eye_size +; eyes: lips: brows: , width lashes piercings: brow, lip, nose; outfit: dress , dress , sleeves , trousers , shoes ; extras: skirt
- 22: rangy (The thin lad (NEET : Arabic, pencil moustache, grey sweatshirt and trackies)): body: , shoulders , head x ; skin: hair: crop, ; face: face_wide --, jaw_wide -, nose_long ++, chin_long +; eyes: lips: brows: , width ; beard: pencil ; outfit: jumper , shirt , no tie, trousers , shoes
- 30: swindon (The Swindon lad (NEET : stout, good build, Swindon Town home shirt, sports-casual)): body: , shoulders , head x ; skin: pink hair: crop, ; face: face_wide ++, jaw_wide ++, nose_wide +, eye_size -, brow_high -; eyes: lips: brows: , width ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: crest
- 38: waif (The shy girl (NEET : woollen jumper with flowers, glasses, very pale, nervous)): body: , shoulders , head x ; skin: hair: long, ; face: face_wide -, chin_long -, eye_size +; eyes: lips: brows: , width ; glasses: ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: flowers
- 47: andy (Andy Burnham, the Prime Minister (scenes : angry, pointing; Sam's finished face-tool head, unchanged)): head: house burnham, hair swept, look detail; outfit: suit , shirt white, no tie; body:
- 52: pat (Pat McFadden, Work and Pensions Secretary (scenes : patient, fingers steepled). Face tool pick B): head: house mcfadden, hair bald, look detail; outfit: suit , shirt white, tie ; body:

## milburn-places.txt (36 pieces; a note on a place changes its line: open that line)
### cabinet (Milburn across the table, straight to lens)
- 11: panels (the panelled wall)
- 12: block (the picture rail)
- 13: block (the dado rail)
- 14: the tall window
- 15: the left curtain
- 16: chair back (Milburn's chair)
- 17: chair back (the empty chair, left)
- 18: chair back (the empty chair, right)
- 19: table top (the green-baize table)
- 20: Milburn's red folder
- 21: the left place's folder
- 22: the right place's folder
- 23: papers (a paper)
- 24: tumbler (Milburn's water glass)
- 25: tumbler (the right place's glass)
- 26: his name card
### reverse (the 180 of shot 1
- 38: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): panels (the panelled wall behind them)
- 39: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): block (the picture rail)
- 40: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): block (the dado rail)
- 41: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): the marble fireplace behind the PM's chair
- 44: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): the first-minister portrait over the fireplace
- 45: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): the bracket clock, middle of the mantel
- 46: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): candlestick (gilt candelabrum, left end)
- 47: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): candlestick (gilt candelabrum, right end)
- 48: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (the empty chair, left)
- 49: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (the Prime Minister's chair)
- 50: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (Pat's chair)
- 51: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): table top (the green-baize table)
- 52: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Andy's red folder
- 53: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Pat's red folder
- 54: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): his name card; Sam 18 Nov: forward on the table, clear of his hands
- 55: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Pat's name card; Sam 18 Nov: forward, clear of his arms
- 57: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): coaster (under Andy's Vimto: front-left of him, chat 11)
- 58: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): can (Andy's Vimto, note 10; chat 11 nearer him)
- 59: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): coaster (under Pat's water: front-left of him, chat 11)
- 60: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): tall glass (Pat's sparkling water, note 10; chat 11 nearer him; Sam 18 Nov: no lemon slice)

## milburn-moves.txt (124 lines; a note on a move changes its line: open that line)
### 1 (milburn)
- 21: row: 1 "The essence of my proposal is quite simple." | calm, reasonable, faintly please
### milburn
- 22: stance: seated
- 23: face: pleased | smug simple
- 24: both: folder
- 25: body: nod essence essence
- 26: body: lean close simple
- 27: body: nod simple simple
- 28: idle: roll shifts
- 29: idle: nod shifts
### 2a (goth)
- 32: row: 2 "Those not in education, employment or training..." | the goth: unimpressed, even 
### a goth
- 33: face: unimpressed | unimpressed up training | gaze eased training
- 34: body: look up training
- 35: idle: lean shifts
- 36: idle: roll shifts
### 2a (rangy)
- 39: row: 2 (the rangy lad) | mouth hanging open | looks up first, mouth falls wider
### a rangy
- 40: face: gormless | awe open training | gaze eased training
- 41: body: look up training
- 42: idle: roll shifts
### 2a (swindon)
- 45: row: 2 (the Swindon lad) | chest out, squinting | chest out the whole shot; squints up
### a swindon
- 46: face: proud | proud up training | gaze eased training
- 47: keys lean:
- 48: keys shoulders: # shoulders set back broad front on the chest out shows as width
- 49: body: look up training
- 50: idle: lean shifts
### 2a (waif)
- 53: row: 2 (the waif) | nervous, shrinking | shoulders up, gripping her sleeves; looks up las
### a waif
- 54: face: nervous | awe training | gaze eased training
- 55: keys shoulders:
- 56: both: sleeves
- 57: body: look up training
- 58: idle: roll shifts
### 2b (goth)
- 61: row: 2 cont. "...a unique opportunity to serve their country." | the aerial: tiny figures
### b goth
- 62: code: field_shot tiny figures a few pixels tall: no faces or limbs act this size
### 3 (goth)
- 65: row: 3 "Each NEET must arm themselves..." | the goth: pleased | hoists the heavy crossbow 
### goth
- 66: code: field_level_shot scene 's moves are drawn by the film's code: props held in both hands
### 4a (andy)
- 69: row: 4 "God damnit, Milburn. You're pulling a Battle Royale slash Hunger Games on us, are
### a andy
- 70: stance: seated
- 71: face: furious
- 72: keys head_yaw: | Milburn | Battle | Hunger | aren't # head life chat rule : the head works the rant
- 73: R: fists
- 74: L: fists | jab Milburn Hunger | fists Hunger | jab aren't end
- 75: body: lean in Milburn
- 76: body: nod Milburn Milburn
- 77: body: nod aren't aren't
- 78: idle: roll shifts
### 4a (pat)
- 81: row: 4 (Pat) | patient, listening, eyes on Andy | fingers steepled, still; a slow blink
### a pat
- 82: stance: seated
- 83: face: patient
- 84: keys look:
- 86: both: steeple
- 87: body: nod Milburn Milburn
- 88: idle: roll shifts
### 4b (milburn)
- 91: row: 5 "This report has been long in the making. Would you care to hear the findings o
### b milburn
- 92: stance: seated
- 93: face: attentive | pleased interrupt
- 94: both: folder
- 95: body: tilt interrupt
- 96: body: nod making making
- 97: idle: roll shifts
- 98: idle: nod shifts
### 4c (pat)
- 101: row: 6 "I'd like to hear where this goes, Prime Minister" | patient; eyes sideways to Andy
### c pat
- 102: stance: seated
- 103: face: patient
- 104: keys look:
- 106: both: steeple
- 107: body: nod Prime Prime
- 108: idle: roll shifts
### 4c (andy)
- 111: row: 7 "Fine! Continue." | exasperated, then sulky; eyes and head go over to Pat (note 7:
### c andy
- 112: stance: seated
- 113: face: furious | exasperated Fine | sulky Continue
- 114: keys look: | Fine | Continue | Continue
- 115: keys head_yaw: | Fine | Continue | Continue
- 116: both: fists Fine | flung Fine Fine | fold Continue
- 117: body: lean back Continue
- 118: idle: roll shifts
### 6 (goth)
- 121: row: 8 "The NEETs will form a unit." | travelling with the four | walking in single file, 
### goth
- 122: code: forest_shot the walk the camera's travel the props are the film's code
### 6 (swindon)
- 125: row: 9 (gunfire, flame, morning stars) "And will encounter teams of their erstwhile col
### swindon
- 126: code: forest_shot the reactions are the film's code: timed the gunfire flame morning stars beats
### 7a (andy)
- 129: row: 10 "You fucker! You're pulling a Maze Runner-Squid Games-Fortnite on me!" | rage | f
### a andy
- 130: stance: seated
- 131: face: rage
- 132: keys head_yaw: | fucker | Maze | Squid | Fortnite # head life chat
- 133: both: fists
- 134: body: slam fucker fucker
- 135: L: fists Fortnite | jab Fortnite end
- 136: body: lean in fucker
- 137: idle: roll shifts
### 7a (pat)
- 140: row: 10 (Pat) | patient, eyes on Andy | steepled; a blink at "fucker"
### a pat
- 141: like: a.pat
### 7b (milburn)
- 144: row: 11 "I am sorry that you feel that way." | sorry-not-sorry: a small sympathetic fr
### b milburn
- 145: stance: seated
- 146: face: sorry
- 147: both: folder
- 148: body: nod feel feel
- 149: idle: roll shifts
### 7c (andy)
- 152: row: 12 "Are you or are you not sending NEETs to kill each other on live TV?" | despairin
### c andy
- 153: stance: seated
- 154: face: despair
- 155: both: fists sending | plead sending end
- 156: body: head shake live
- 157: idle: roll shifts
### 7c (pat)
- 160: row: 12 (Pat) | patient | steepled
### c pat
- 161: like: a.pat
### 7d (milburn)
- 164: row: 13 "My report is nuanced and multifaceted. I also suggest taking away PIP after t
### d milburn
- 165: stance: seated
- 166: face: attentive | pleased multifaceted | smug Blood
- 167: keys look: glance | glance | glance | glance
- 168: both: folder
- 169: body: nod multifaceted multifaceted
- 170: body: nod Blood Blood
- 171: idle: roll shifts
### 7e (andy)
- 174: row: (silent) | outrage, visibly cross (note 8): brows hard down, eyes narrowed, mouth op
### e andy
- 175: stance: seated
- 176: face: rage | gape gape
- 177: both: plead end
- 178: body: lean in
- 179: body: nod gape
### 7e (pat)
- 182: row: 14 "I think the backbenchers will like this one, sir." | patient, a small approving s
### e pat
- 183: stance: seated
- 184: face: patient | approving backbenchers
- 185: keys look:
- 187: both: steeple
- 188: body: nod like like
- 189: idle: roll shifts
