# milburn: the page a notes round reads (python3 source/page.py milburn; regenerate after any edit)

Read this, then only the lines a note points to (`page.py FILM find "note words"`).


## milburn.py (371 lines)
- 32: HERE (data)
- 40: B (data)
- 41: V (data)
- 46: NAME (data)
- 47: FILM (data)
- 48: NOTES (data)
- 49: HAS (data)
- 50: FPS (data)
- 51: LINES (data)
- 56: SHOTS (data)
- 57: DUR (data)
- 58: T (data)
- 61: SHOT_CAST (data)
- 62: KEEP_CLEAR (data)
- 63: HOOK (data)
- 64: SHOT_MARKS (data)
- 67: `scene_of` 
- 75: `shot_of` 
- 80: PLAN (data)
- 95: BENCHMARK (data)
- 106: CAST (data)
- 107: FEET (data)
- 110: `scale_at` The kit's scale for someone drawn at pxm pixels per metre (their neck base sits at 0.84 of their height).
- 115: `person` Draw `who` standing on sole_y; their face and pose come from story/milburn-moves.txt (the moves kit) when the
- 128: MOODS (data)
- 143: `word_at` When line n reaches `words` (stand-in timing: the text spread evenly by letters over the line's span).
- 151: TRACK (data)
- 155: BLINKS (data)
- 158: HEAD_LIFE (data)
- 161: `head_life` Rule 74: Milburn's head tilts and nods on his voice (headlife, from the stand-in's loudness per drawing).
- 173: `face_sp` The moves kit's seam: who's build with the face for a mood, lips on their own lines, blinks.
- 186: _MOVES (data)
- 189: `moves` (the moves file, the film's side) for the kit, read once.
- 197: `acted` (face sp, joints) for who's block in shot at film time t (story/milburn-moves.txt).
- 207: _DESC (data)
- 208: _PAINT (data)
- 212: `cabinet` 
- 238: `_table_layer` The front layer (table, folders, glasses, name card) on its own, to lay between Milburn's body and arms.
- 247: NEETS (data)
- 250: `shaft_shot` 
- 271: TINY (data)
- 274: `_tiny` 
- 283: `field_shot` 
- 290: `picture` 
- 299: `frame_image` 
- 303: `cast` 
- 308: `_standin` A robotic stand-in for line i (espeak-ng), only for timing until Sam records: spoken at the rate that fills
- 331: `soundtrack` 
- 342: `final` 
- 353: `main` 

## milburn_sets.py (413 lines)
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
- 399: `sheet` 

## milburn-people.txt (5 people; a note on a person changes their lines)
- 6: milburn (Alan Milburn (Lead: speaks, straight to lens)): body: , shoulders , head x ; skin: hair: side, ; face: brow_high , nose_wide , brow_slope , nose_long , eye_tilt , chin_long , face_wide , lip_top , eye_size ; eyes: lips: brows: , width , thick ; glasses: , thick; outfit: suit navy, shirt white, tie , trousers navy, shoes
- 14: goth (The goth girl (NEET : big blue-purple hair, blooming black dress, pudgy nose, overweight)): body: , shoulders , head x ; skin: pale hair: curly, , big, streaks ; face: face_wide ++, jaw_wide ++, nose_wide ++, nose_long -, eye_size +; eyes: lips: brows: , width lashes; outfit: dress , dress , sleeves , trousers , shoes ; extras: skirt
- 22: rangy (The thin lad (NEET : Arabic, pencil moustache, grey sweatshirt and trackies)): body: , shoulders , head x ; skin: hair: crop, ; face: face_wide --, jaw_wide -, nose_long ++, chin_long +; eyes: lips: brows: , width ; beard: pencil ; outfit: jumper , shirt , no tie, trousers , shoes
- 30: swindon (The Swindon lad (NEET : stout, good build, Swindon Town home shirt, sports-casual)): body: , shoulders , head x ; skin: pink hair: crop, ; face: face_wide ++, jaw_wide ++, nose_wide +, eye_size -, brow_high -; eyes: lips: brows: , width ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: crest
- 38: waif (The shy girl (NEET : woollen jumper with flowers, glasses, very pale, nervous)): body: , shoulders , head x ; skin: hair: long, ; face: face_wide -, chin_long -, eye_size +; eyes: lips: brows: , width ; glasses: ; outfit: jumper , shirt , no tie, trousers , shoes ; extras: flowers

## milburn-places.txt (17 pieces; a note on a place changes its line: open that line)
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

## milburn-moves.txt (32 lines; a note on a move changes its line: open that line)
### 1 (milburn)
- 12: row: 1 "The essence of my proposal is quite simple." | calm, reasonable, faintly please
### milburn
- 13: stance: seated
- 14: face: pleased | smug simple
- 15: both: folder
- 16: body: nod essence essence
- 17: body: lean close simple
- 18: body: nod simple simple
- 19: idle: roll shifts
- 20: idle: nod shifts
### 2a (goth)
- 23: row: 2 "Those not in education, employment or training..." | the goth: unimpressed, even 
### a goth
- 24: face: unimpressed | unimpressed up training | gaze eased training
- 25: body: look up training
- 26: idle: lean shifts
- 27: idle: roll shifts
### 2a (rangy)
- 30: row: 2 (the rangy lad) | mouth hanging open | looks up first, mouth falls wider
### a rangy
- 31: face: gormless | awe open training | gaze eased training
- 32: body: look up training
- 33: idle: roll shifts
### 2a (swindon)
- 36: row: 2 (the Swindon lad) | chest out, squinting | chest out the whole shot; squints up
### a swindon
- 37: face: proud | proud up training | gaze eased training
- 38: keys lean:
- 39: keys shoulders: # shoulders set back broad front on the chest out shows as width
- 40: body: look up training
- 41: idle: lean shifts
### 2a (waif)
- 44: row: 2 (the waif) | nervous, shrinking | shoulders up, gripping her sleeves; looks up las
### a waif
- 45: face: nervous | awe training | gaze eased training
- 46: keys shoulders:
- 47: both: sleeves
- 48: body: look up training
- 49: idle: roll shifts
### 2b (goth)
- 52: row: 2 cont. "...a unique opportunity to serve their country." | the aerial: tiny figures
### b goth
- 53: code: field_shot tiny figures a few pixels tall: no faces or limbs act this size
