# milburn: the page a notes round reads (python3 source/page.py milburn; regenerate after any edit)

Read this, then only the lines a note points to (`page.py FILM find "note words"`).


## milburn.py (691 lines)
- 34: HERE (data)
- 42: B (data)
- 43: V (data)
- 48: NAME (data)
- 49: FILM (data)
- 50: NOTES (data)
- 51: HAS (data)
- 52: FPS (data)
- 53: LINES (data)
- 75: SHOTS (data)
- 80: CUTS_N11 (data)
- 83: DUR (data)
- 84: T (data)
- 92: _FOUR (data)
- 93: REVERSE (data)
- 94: ACROSS (data)
- 95: SHOT_CAST (data)
- 97: KEEP_CLEAR (data)
- 98: HOOK (data)
- 99: SHOT_MARKS (data)
- 102: `scene_of` 
- 110: `shot_of` 
- 115: PLAN (data)
- 130: BENCHMARK (data)
- 141: CAST (data)
- 142: FEET (data)
- 145: `scale_at` The kit's scale for someone drawn at pxm pixels per metre (their neck base sits at 0.84 of their height).
- 150: `person` Draw `who` standing on sole_y; their face and pose come from story/milburn-moves.txt (the moves kit) when the
- 164: MOODS (data)
- 196: `word_at` When line n reaches `words` (stand-in timing: the text spread evenly by letters over the line's span).
- 204: TRACK (data)
- 208: BLINKS (data)
- 211: HEAD_LIFE (data)
- 214: `head_life` Rule 74: Milburn's head tilts and nods on his voice (headlife, from the stand-in's loudness per drawing).
- 226: `face_sp` The moves kit's seam: who's build with the face for a mood, lips on their own lines, blinks.
- 239: _MOVES (data)
- 242: `moves` (the moves file, the film's side) for the kit, read once.
- 250: `acted` (face sp, joints) for who's block in shot at film time t (story/milburn-moves.txt).
- 262: _DESC (data)
- 263: _PAINT (data)
- 267: `cabinet` 
- 294: _RPAINT (data)
- 295: SEATS (data)
- 296: SPLIT (data)
- 299: `reverse` Andy and Pat across the table from Milburn's seat (places view `reverse`), seated as Milburn is in shot 1: the
- 332: `_table_layer` The front layer (table, folders, glasses, name card) on its own, to lay between Milburn's body and arms.
- 341: NEETS (data)
- 344: `shaft_shot` 
- 365: TINY (data)
- 368: `_tiny` 
- 377: `field_shot` 
- 385: FIELD3 (data)
- 388: PLINTHS3 (data)
- 392: `_hoist` 0 -> 1: the goth's crossbow from across her hips up onto her shoulder (lands on "arm themselves").
- 398: `_mix` 
- 402: `arming` (face sp, joints) for scene 3 (acting list row 3): the weapons in their hands, the moves on line 3.
- 450: YAW3 (data)
- 454: `field_level_shot` 
- 476: FOREST6 (data)
- 479: CLOSE6 (data)
- 480: HALT (data)
- 483: `_ramp` 
- 487: `walked` How far `who` has walked (m, across the screen) since the shot began: the camera's pace, stopping dead on
- 500: `_crouch` Lower the body `amt` person units with the feet kept on the floor (knees bend), leaning forward.
- 510: `forest_pose` (face sp, joints, firing) for scene 6 (acting rows 8 and 9): walking with their weapons, the jolt on the
- 574: `forest_shot` 
- 598: `picture` 
- 613: `frame_image` 
- 617: `cast` 
- 622: `_standin` A robotic stand-in for line i (espeak-ng), only for timing until Sam records: spoken at the rate that fills
- 645: `soundtrack` 
- 656: `final` 
- 667: `main` 
- 688: `caption_at` The subtitle on screen at t (finish.py burns them in; rule 62), from LINES.

## milburn_forest.py (496 lines)
- 29: HERE (data)
- 35: CAM (data)
- 37: YAW_VIEW (data)
- 38: V_EFF (data)
- 39: STOP (data)
- 42: `cam_x` The camera's travel (m, to the right) since the shot began: walking pace, then easing to a stop.
- 51: END_X (data)
- 54: HAZE (data)
- 55: CANOPY (data)
- 56: LEAF (data)
- 57: BARK (data)
- 58: BARK_D (data)
- 59: EARTH (data)
- 60: EARTH_D (data)
- 61: FLOOR (data)
- 64: `fog` Colour c at depth d: hazier and paler the further off (flat steps, not a gradient per pixel).
- 70: `_P` 
- 76: `items` Every piece of the forest in metres: (depth, kind, x, args, seed).
- 110: AHEAD_GUNS (data)
- 111: NOZZLE (data)
- 112: STAR_PIVOTS (data)
- 116: `_poly` 
- 120: `_blob` 
- 134: `trunk` 
- 161: `clump` 
- 174: `bush` 
- 188: `fern` 
- 217: `mark` 
- 243: `_backdrop` The deep, hazy green behind every trunk: darker up in the canopy (flat bands).
- 253: `_shafts` Shafts of light slanting down through the canopy (flat, pale, see-through).
- 264: `behind` Everything behind the four (RGBA, full size).
- 301: NEAR (data)
- 305: `in_front` The nearest layer at about 1.5 m (RGBA): the undergrowth just in front of the track, ferns and a trunk that
- 323: `class _FxCam` The level camera in prepper_fx's terms: points are (x, up, depth) in metres; px per metre as k.
- 338: `_fx` 
- 343: `gunfire` Flashes in the leaves ahead (screen right) from the gunfire on, one frame each, never all at once; tracers
- 364: `muzzle` A muzzle flash at a gun's mouth (screen X, Y; k px per metre there): the house's lumpy flash.
- 377: `flame` The flamethrower's blast (37.5): a jet whips out of the nearest bush ahead, left across the track at their
- 425: `star_at` (pivot X, Y, ball X, Y, radius px, k px/m) for morning star i at film time t, or None before it drops.
- 445: `stars` The two morning stars: spiked steel balls on chains swinging down out of the trees over their heads.
- 477: `sheet` 

## milburn_props.py (196 lines)
- 20: HERE (data)
- 29: `_rect` 
- 33: `_ell` 
- 37: `_spikes` 
- 48: SHAPES (data)
- 74: SCALE (data)
- 76: LENGTH (data)
- 79: `draw` The prop's parts turned `ang` degrees (0: along +x on screen, + clockwise as y runs down), k per metre.
- 89: `units_per_m` 
- 93: `in_hands` The prop held in hand `a` (its grip in that hand) pointing at hand `b` (or at `ang` degrees when b is None);
- 123: `j2_3` The 2D drawn joints as 3D points (depth 0) for grips.hand_centre.
- 132: `plinth` A grey plinth (1.0 m high, 0.5 m square) at (x, dep) seen by a level camera `cam` (cam.p(x, d, z) in
- 173: `sheet` 

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

## milburn-people.txt (7 people; a note on a person changes their lines)
- 6: milburn (Alan Milburn (Lead: speaks, straight to lens)): body: , shoulders , head x ; skin: hair: side, ; face: brow_high , nose_wide , brow_slope , nose_long , eye_tilt , chin_long , face_wide , lip_top , eye_size ; eyes: lips: brows: , width , thick ; glasses: , thick; outfit: suit navy, shirt white, tie , trousers navy, shoes
- 14: goth (The goth girl (NEET : big blue-purple hair, blooming black dress, pudgy nose, overweight)): body: , shoulders , head x ; skin: pale hair: shag, , big, streaks ; face: face_wide ++, jaw_wide ++, nose_wide ++, nose_long -, eye_size +; eyes: lips: brows: , width lashes piercings: brow, lip, nose; outfit: dress , dress , sleeves , trousers , shoes ; extras: skirt
- 22: rangy (The thin lad (NEET : Arabic, pencil moustache, grey sweatshirt and trackies)): body: , shoulders , head x ; skin: hair: crop, ; face: face_wide --, jaw_wide -, nose_long ++, chin_long +; eyes: lips: brows: , width ; beard: pencil ; outfit: jumper , shirt , no tie, trousers , shoes
- 30: swindon (The Swindon lad (NEET : stout, good build, Swindon Town home shirt, sports-casual)): body: , shoulders , head x ; skin: pink hair: crop, ; face: face_wide ++, jaw_wide ++, nose_wide +, eye_size -, brow_high -; eyes: lips: brows: , width ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: crest
- 38: waif (The shy girl (NEET : woollen jumper with flowers, glasses, very pale, nervous)): body: , shoulders , head x ; skin: hair: long, ; face: face_wide -, chin_long -, eye_size +; eyes: lips: brows: , width ; glasses: ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: flowers
- 47: andy (Andy Burnham, the Prime Minister (scenes : angry, pointing; Sam's finished face-tool head, unchanged)): head: house burnham, hair swept, look detail; outfit: suit , shirt white, no tie; body:
- 52: pat (Pat McFadden, Work and Pensions Secretary (scenes : patient, fingers steepled). Face tool pick B): head: house mcfadden, hair bald, look detail; outfit: suit , shirt white, tie ; body:

## milburn-places.txt (31 pieces; a note on a place changes its line: open that line)
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
- 25: tumbler (the left place's glass)
- 26: tumbler (the right place's glass)
- 27: his name card
### reverse (the 180 of shot 1
- 35: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): panels (the panelled wall behind them)
- 36: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): block (the picture rail)
- 37: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): block (the dado rail)
- 38: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): the marble fireplace behind the PM's chair
- 40: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (the empty chair, left)
- 41: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (the Prime Minister's chair)
- 42: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): chair back (Pat's chair)
- 43: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): table top (the green-baize table)
- 44: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Andy's red folder
- 45: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Pat's red folder
- 46: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): can (Andy's Vimto)
- 47: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): tall glass (Pat's sparkling water)
- 48: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): his name card
- 49: from Milburn's seat across the table to Andy and Pat; shots 5 and 7): Pat's name card

## milburn-moves.txt (122 lines; a note on a move changes its line: open that line)
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
- 72: R: fists
- 73: L: fists | jab Milburn Hunger | fists Hunger | jab aren't end
- 74: body: lean in Milburn
- 75: body: nod Milburn Milburn
- 76: body: nod aren't aren't
- 77: idle: roll shifts
### 4a (pat)
- 80: row: 4 (Pat) | patient, listening, eyes on Andy | fingers steepled, still; a slow blink
### a pat
- 81: stance: seated
- 82: face: patient
- 83: keys look:
- 84: both: steeple
- 85: body: nod Milburn Milburn
- 86: idle: roll shifts
### 4b (milburn)
- 89: row: 5 "This report has been long in the making. Would you care to hear the findings o
### b milburn
- 90: stance: seated
- 91: face: attentive | pleased interrupt
- 92: both: folder
- 93: body: tilt interrupt
- 94: body: nod making making
- 95: idle: roll shifts
- 96: idle: nod shifts
### 4c (pat)
- 99: row: 6 "I'd like to hear where this goes, Prime Minister" | patient; eyes sideways to Andy
### c pat
- 100: stance: seated
- 101: face: patient
- 102: keys look:
- 103: both: steeple
- 104: body: nod Prime Prime
- 105: idle: roll shifts
### 4c (andy)
- 108: row: 7 "Fine! Continue." | exasperated, then sulky; eyes and head go over to Pat (note 7:
### c andy
- 109: stance: seated
- 110: face: furious | exasperated Fine | sulky Continue
- 111: keys look: | Fine | Continue | Continue
- 112: keys head_yaw: | Fine | Continue | Continue
- 113: both: fists Fine | flung Fine Fine | fold Continue
- 114: body: lean back Continue
- 115: idle: roll shifts
### 6 (goth)
- 118: row: 8 "The NEETs will form a unit." | travelling with the four | walking in single file, 
### goth
- 119: code: forest_shot the walk the camera's travel the props are the film's code
### 6 (swindon)
- 122: row: 9 (gunfire, flame, morning stars) "And will encounter teams of their erstwhile col
### swindon
- 123: code: forest_shot the reactions are the film's code: timed the gunfire flame morning stars beats
### 7a (andy)
- 126: row: 10 "You fucker! You're pulling a Maze Runner-Squid Games-Fortnite on me!" | rage | f
### a andy
- 127: stance: seated
- 128: face: rage
- 129: both: fists
- 130: body: slam fucker fucker
- 131: L: fists Fortnite | jab Fortnite end
- 132: body: lean in fucker
- 133: idle: roll shifts
### 7a (pat)
- 136: row: 10 (Pat) | patient, eyes on Andy | steepled; a blink at "fucker"
### a pat
- 137: like: a.pat
### 7b (milburn)
- 140: row: 11 "I am sorry that you feel that way." | sorry-not-sorry: a small sympathetic fr
### b milburn
- 141: stance: seated
- 142: face: sorry
- 143: both: folder
- 144: body: nod feel feel
- 145: idle: roll shifts
### 7c (andy)
- 148: row: 12 "Are you or are you not sending NEETs to kill each other on live TV?" | despairin
### c andy
- 149: stance: seated
- 150: face: despair
- 151: both: fists sending | plead sending end
- 152: body: head shake live
- 153: idle: roll shifts
### 7c (pat)
- 156: row: 12 (Pat) | patient | steepled
### c pat
- 157: like: a.pat
### 7d (milburn)
- 160: row: 13 "My report is nuanced and multifaceted. I also suggest taking away PIP after t
### d milburn
- 161: stance: seated
- 162: face: attentive | pleased multifaceted | smug Blood
- 163: keys look: glance | glance | glance | glance
- 164: both: folder
- 165: body: nod multifaceted multifaceted
- 166: body: nod Blood Blood
- 167: idle: roll shifts
### 7e (andy)
- 170: row: (silent) | outrage, visibly cross (note 8): brows hard down, eyes narrowed, mouth op
### e andy
- 171: stance: seated
- 172: face: rage | gape gape
- 173: both: plead end
- 174: body: lean in
- 175: body: nod gape
### 7e (pat)
- 178: row: 14 "I think the backbenchers will like this one, sir." | patient, a small approving s
### e pat
- 179: stance: seated
- 180: face: patient | approving backbenchers
- 181: keys look:
- 182: both: steeple
- 183: body: nod like like
- 184: idle: roll shifts
