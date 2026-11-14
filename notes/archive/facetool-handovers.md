
## Face tool, where things stand (chat 5 of the face chain, 14 Nov; ~0.3%, stop 0.9%: the asked list done)
- **Rules that bite next:** 49 (likeness: the replay's faults), 86 (kittests written; check column on Sam's Y), 85.
- **Done:** Walliams replay: 1 run, 3 min (+ a 14 s redraw), all three heads pass the check, 1st of 14 (A 85%, B 87%,
  C 81%), against his five hand-made chats (18.6% of a week). Sheet: `notes/morning/facetool-walliams-replay.jpg`
  (photos, the hand-made head, A/B/C). Fixed: the beard read only the first photo (his is shaven: stubble lost, redraw
  crashed): each photo now leads in turn, fullest kept; photo paths stored from the top folder (Burnham's held
  '../': redraw only ran from source/). Kittests: facepick_extras_after_the_check, facepick_beard_from_any_front,
  agelines_by_measure_and_age (all pass, ~25 s).
- **Faults the replay found (the hand-made head still reads more like him):** 1 the beard a solid dark brown band
  (his is light grey stubble: the hand-made one blends 22-32% grey into the skin); 2 eyes A and B read shut (lids
  over a smile-squint); 3 chin_long stays timid in all three (hand-made stretched the lower face x1.15: his 98th
  centile); 4 hair a rounded cap, not swept up off the forehead; no grey sides found.
- **Sam's answers (14 Nov, after the replay):** "Not identifiable as him at all"; worried we drift from the house style.
  Plan 1 chosen: rebuild the tool ON THE HOUSE HEAD (Ad-vanced Notice, Blessed): hair, beard and clothes from the
  house's drawn pieces (people kit), not traced off the photo; caricature his 2-3 standout features; judged by the
  blind name test (namer), the likeness check kept only as the "nothing the wrong way" guard. Sam: "there is a lot of
  great detail in these tests that you should try to retain ... the Kemi in particular is amazing. We just need to
  blend it into our existing style somehow, improving the style without losing it artistically." Tests: Andy
  (Burnham) and Kemi (Badenoch), then Walliams. Age lines KEPT ("important for some characters"), drawn in house
  style, per character. Budget: "don't limit yourself on budget as this is important and I have spare" (no % stop;
  rule 85's cost watch still hands over between chats).
- **Next: face chain chat 6, Opus HIGH (new building):** design the blend first (one sheet: Burnham C and Badenoch C as
  picked vs the house versions, details kept named one by one: Kemi's plaits, Burnham's eyes and glasses, the age
  lines), then build; done when the namer names each blind and Sam says the style is ours.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facepick.py` MAP; rule 49.
- **Open rule requests:** rule 49's check column naming the face-tool tests: asked, unanswered (Sam answered the plan instead); ask again with chat 6's sheet.
- **For Claude:** replay: `facepick.py walliams OUT w06 w07 w01 w02 (references/blessed/likeness/) --tq w09 --says
  "glasses=no, age=55, hair=plain"` (no beard=no: chat 5 said it and had to redraw). Hand-made head:
  `blessed_walliams.py head OUT.png` (beard() 115, colours 97-111, LOW 81). beardkit.analyse returns sheet None when no
  hair is found.



## Face tool, where things stand (chat 6 of the face chain, 14 Nov; amber at ~2.4%: handed over after the sheet)
- **Rules that bite next:** 49 (likeness: the name test is the judge now), 86 (facehouse needs its kittest), 85.
- **Done:** design step of plan 1. New `source/facehouse.py`: the face tool's pick drawn ON THE HOUSE HEAD (people kit
  body and clothes, house outline, ears, eyes, brows, nose, lips at the house head size) with house pieces: `swept`
  hair (Walliams' hand-made hair made general), `braids` (middle parting, crown lines, two curtains of plaits that
  hug the face, chevrons per plait), the measured glasses in house ink, age lines redrawn as the hand-made smile
  folds and crinkles. Two looks: 1 house (house skin tones, strong lines only), 2 house + detail (skin near the
  photo, socket shade, every line, more plaits). Sheet sent: `notes/morning/facehouse-design.jpg`.
- **Blind name test (namer, step 1 only):** Burnham 1: 8% (named Starmer first, 10%: the glasses pull to him);
  Burnham 2: 12%; Badenoch 1: 30%; Badenoch 2: 35% (her plaits carry her; the face reads generic). Answers kept
  locally only (review/ is not saved). Fault found in the check: the pack's folder is named after the person and two
  namers said it nudged them: name packs neutrally (fix in nametest.py's pack paths).
- **Next (chat 7, Opus HIGH: new building):** K1 and K2 first (a clip-size sheet of Kemi: pick C beside look 2
  before and after; find why her shape was lost: house outline vs C's outline_uv, the layout at the house size), then push the likeness until the
  namer names each blind (neutral folder names, line-up step too): Burnham's heavy dark brows over deep-set eyes,
  longer face, the wide smile with deep folds (his usual expression), thick wavy hair pushed up; Badenoch's high
  rounded forehead (namer: the cap reads as a fringe), wide-set big eyes, full lips, the gap-tooth smile. Keep the
  likeness check as the 'nothing the wrong way' guard. Then: facehouse in people.py (`head: house NAME`), turned
  views (turnhead), kittest, catalogue row, facepick's sheet drawing its heads with facehouse; then Walliams.
- **Sam's answers (14 Nov, after the sheet):** "2 is great" (look 2, house + detail, is the look). Andy: "looks 90%
  correct, great job". Kemi, two notes: **K1** "we lost the face shape ... Kemi just needs her proportions back" (the
  pick C's face shape and proportions; "we are allowed to play with face shapes in the house style"); **K2** "her
  plaits go all the way to the top ... always the way she keeps her hair. You would need to learn how to draw her top
  plaits too" (plaits from the parting over the crown, not a sleek cap; the namer also read the cap as a fringe).
- **Needs Sam:** rule 49's check column naming the face-tool tests (Y/N, asked twice).
- **Sam's words kept:** "Please don't limit yourself on budget as this is important and I have spare." (no % stop;
  rule 85 still hands over between chats). Age lines stay, house style, per character.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP; rule 49.
- **Open rule requests:** rule 49's check column (asked again with chat 6's sheet).
- **For Claude:** `python3 source/facehouse.py sheet OUT.jpg [burnham badenoch]` (~10 s); `head NAME LOOK OUT.png`;
  per-person lines in facehouse.CAST (hair piece, quiff, hairline, brow_thick, outfit); looks in LOOKS. The sheet's
  photo tile prints a harmless mediapipe shutdown traceback. nametest packs: scratchpad (lost); rebuild them.


## Face tool, where things stand (chat 7 of the face chain, 14 Nov; amber at ~3.1%: handed over after the sheet)
- **Rules that bite next:** 49 (likeness: the blind name test is the judge), 86 (facehouse needs its kittest), 85.
- **Done:** K1: Kemi's face was already pick C's (outlines match); the guessed hair cap made her head a head taller and
  narrower. Hair now measured off the pick's picture (`pick_hair`), plus her ears (as in C) and a wider neck. K2: plaits
  from the parting over the whole crown, one rope each down to the tips. Sheet sent: `notes/morning/facehouse-kemi-k1k2.jpg`.
  Name test now uses neutral folders (`nametest.py`). facepick and agelines kittests pass; Andy unchanged (0 pixels).
- **Name test, neutral folders (the honest baseline; chat 6's 8-35% were nudged by the folder name):** Kemi look 2:
  not named (Ketanji Brown Jackson 30%), line-up 6th of 8 ("a generic template ... needs her own features: face shape,
  nose and mouth"). Andy look 2: named 3rd at 5% (Starmer 15%), line-up 3rd. Both FAIL.
- **Next (chat 8, Opus HIGH: new building): the likeness push** until each is named blind (neutral packs, line-up
  step too): Burnham's heavy dark brows over deep-set eyes, longer face, the wide smile with deep folds, thick wavy
  hair pushed up; Badenoch's high rounded forehead, wide-set big eyes, full lips, the gap-tooth smile (exaggerate:
  "we are allowed to play with face shapes in the house style"). Keep the likeness check as the 'nothing the wrong
  way' guard; don't undo K1/K2. Then facehouse in people.py (`head: house NAME`), turned views, kittest, catalogue
  row, facepick's sheet drawing with facehouse; then Walliams.
- **Needs Sam:** (1) Kemi's ears showing, as in pick C (her photos hide them): Y keep / N hide. (2) rule 49's check
  column naming the face-tool tests (Y/N, asked three times).
- **Sam's words kept:** "Please don't limit yourself on budget as this is important and I have spare." (no % stop;
  rule 85 still hands over between chats). Age lines stay, house style, per character. Look 2 is the look.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP; rule 49.
- **Open rule requests:** rule 49's check column.
- **For Claude:** `python3 source/facehouse.py head NAME detail OUT.png`; per-person lines in facehouse.CAST (ears,
  neck_w new). `nametest.py pack KEYDIR BIG.png --lineup "..."` now writes the helper's files to review/np/RANDOM;
  `score KEYDIR NAME` finds them. Packs used: Kemi line-up Badenoch, Abbott, Butler, Patel, Harris, Obama, de Cordova,
  Ribeiro-Addy; Andy line-up Burnham, Starmer, Streeting, Miliband, Sunak, Hunt, Gove, Khan.



## Face tool, where things stand (chat 8 of the face chain, 14 Nov; amber at ~3%: handed over after Sam's notes)
- **Rules that bite next:** 49 (likeness: the blind name test is the judge), 86 (facehouse needs its kittest), 85.
- **Done:** the likeness tools in facehouse (caricature push, lashes, eye size, brow arch/raise, the house mouths with
  colours, forehead, plait size; MAP "LIKENESS"). Round 1 (push 1.3, Andy's grin, Kemi gap-tooth/smirk) scored no
  better: Andy named 3rd at 6%, line-up 4th; Kemi not named (Ketanji Brown Jackson), line-up 5th and 6th (namers
  match her plaits to Ribeiro-Addy, de Cordova). Round 2's tests died on the usage limit. **Sam's notes (chat 8):**
  "Kemi may need individually bigger braids, slightly slightly bigger. Not too much." "Her pupils are massive compared
  to Andy's." "Careful, you're straying too hard into caricature territory." Done: push held back to 1.15, plaits
  1.2x, her pupils smaller, her lips trimmed; Andy keeps a gentle grin, lashes, heavier brows, burgundy tie (his
  photo). Sheet sent: `notes/morning/facehouse-likeness-c8.jpg`. facepick and agelines kittests pass.
- **Sam's notes on the sheet (chat 8, 14 Nov evening):** "I prefer the before in both (Andy's grin is poorly drawn
  with stray lines, is too shit-eating, his eyelashes are too much), except for Kemi's braids and eyes. But even then
  the eyes are wide and startled. I think before Andy is finished. Kemi is still not quite right especially in face
  shape and I think looking at your face on references would help." So: (F1) Andy back to chat 7's head exactly (no
  push, grin, lashes, tie; the brows as before): **Andy is finished.** (F2) Kemi keeps plait_k 1.2 and the new
  eyes' smaller pupils, but calmer: not wide or startled (less white, eye_scale near 1, a heavier upper lid). (F3)
  Kemi's face shape: drawn from her FRONT-ON reference photos (k01, k02, k03), outline laid over the photo, not
  the push; everything else back to the before (no push, mouth, brow raise, forehead lift).
- **Next (chat 9, Opus HIGH):** F1, F2, F3; a sheet (before / now / her front photo with the outline over it), then
  her blind name test (neutral pack, line-up step). Then facehouse in people.py, turned views, kittest, catalogue row;
  then Walliams.
- **Needs Sam:** (1) Kemi's ears showing, as in pick C: Y keep / N hide. (2) rule 49's check column naming the face-tool
  tests (Y/N, asked four times). (Andy's grin and tie: answered N, F1.)
- **Sam's words kept:** "Please don't limit yourself on budget as this is important and I have spare." Age lines stay,
  house style, per character. Look 2 ('detail') is the look. Not too far into caricature. Andy is finished (chat 7 head).
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (LIKENESS); rule 49.
- **Open rule requests:** rule 49's check column.
- **For Claude:** CAST holds the new lines. `nametest.py pack KEYDIR BIG.png --lineup "..."` (quote the list: "de
  Cordova" has a space); line-ups as chat 7. AV.vance_mouth and P4.brows took new keyword options; defaults unchanged.


## Face tool, where things stand (chat 9 of the face chain, 14 Nov; amber 3.2%: stops on a question for Sam)
- **Rules that bite next:** 49 (the blind name test is the judge), 86 (facehouse needs its kittest), 85.
- **Done (chat 9):** F1 Andy = chat 7's head pixel for pixel: **finished**. F2 Kemi: plaits 1.2x; eyes calm (iris
  0.98, pupil 0.28, iris_c a shade lighter, upper lid 0.24). F3 her outline traced off her 3 front photos
  (`facehouse.py trace`): rounder, slightly longer chin. Ears hidden (Sam). **Sam's notes on the sheet:** "Try the
  eyebrows" (Y) and "look closely at the neckline": brows now thin, arched, tapered (0.032, arch 0.03, taper 0.6);
  her open collar redrawn (`open_collar`: the skin runs down into a V, collar flaps over the lapels; the old foot had
  a step, white bars at the sides and a floating skin triangle). Smile: not answered, not done.
  Sheets: `notes/morning/facehouse-kemi-c9.jpg`, `-c9b.jpg`. facepick and agelines kittests pass.
- **Name tests (neutral pack, chat 7's line-up):** not named in any of 3 runs (Cori Bush / Ketanji Brown Jackson);
  line-up 5th, 5th, then 7th with the new brows. Namers keep calling her face generic and matching the plaits and
  navy suit to Ribeiro-Addy.
- **Sam on c9b:** "Neckline is so much better." "Her eye brows are really far from her eyes?" (a question: answered
  with the plan, waits for his Y). Why: the face tool measured her brows high (brow_high 0.80 vs 0.59 average,
  landmark 52, likely thrown by her arch), and chat 9's arch lifted them more; laid over her photo, the drawn brows
  sit above her real ones. Plan: set the brows' height from the drawing laid over her front photos (tune brow_high
  down until they sit on hers), peak where hers peaks; a close-up of the eyes with the photo beside it.
- **Sam answered (chat 9):** brows: Y, fix them AND "investigate why the tool made that judgement" (why the face
  tool measured her brows so high: landmark 52 vs her arch? the photos? the brow_high measure itself?); the fix and
  the finding go in likeness/facehouse so the next face does not repeat it. Smile: N ("I don't see a problem with her
  mouth"): mouth stays as it is. Neckline: kept.
- **Next (chat 10, Opus medium):** the brow investigation and fix; a close-up sheet (eyes and brows, drawing beside
  her photo, and the drawing laid over it) with a Checks line; her name test; then facehouse in people.py, turned
  views, kittest, catalogue row; then Walliams.
- **Needs Sam:** nothing open.
- **Sam's words kept:** "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far
  into caricature. Andy is finished. Kemi: bigger plaits, small pupils, calm eyes, face from photos, ears hidden.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (LIKENESS); rule 49.
- **Open rule requests:** none.
- **For Claude:** CAST badenoch: plait_k, iris_r, pupil_r, iris_c, lid, shape, brow_arch/taper (new: iris_c, lid,
  shape; the trace is 'outline' in her pick JSON). open_collar only in the braids path (Andy's base torso untouched).

## Face tool, where things stand (chat 10 of the face chain, 14 Nov; stops on a question for Sam)
- **Rules that bite next:** 49 (the blind name test is the judge), 86 (facehouse's kittest), 85.
- **Done (chat 10):** Kemi's brows lowered onto her own (sheet `notes/morning/facehouse-kemi-c10-brows.jpg`: before,
  now, her photo, now laid over it). **Why the tool put them high:** its height was honest (on her sharp photo the
  brow point sits on her brow; her brows ARE a little high), but three things stacked: the pick's push (0.68 -> 0.80),
  chat 9's arch lifting the WHOLE brow (about 0.2 eye widths) and the heavier lid lowering the lid line. Her two small
  photos (eyes 18-24 px) put the point mid-brow and read higher still. **Fixed in the tool:** the arch bends the ends
  down; brows move with a heavier lid; `facehouse.py brows NAME OUT.jpg` measures the brow and its peak in the
  pixels (small photos only when nothing sharper), saves them in the pick, draws the brows at her height (0.57 eye
  widths above the lid) and peak, and lays the drawing over each photo. New kittest facehouse_brows_sit_on_hers;
  facepick and agelines pass. Andy pixel for pixel unchanged. Mouth and neckline untouched.
- **Name test (neutral pack, chat 7's line-up):** not named (Dawn Butler 12, Ayanna Pressley 10, Diane Abbott 8);
  line-up 5th of 8 (Ribeiro-Addy first). Namer: "fairly generic"; braids and navy suit fit several MPs.
- **Sam (chat 10):** "Kemi is right." Build on: "Yes, what is left to do on the kit"; asked whether the Walliams test
  is still required. Answered with the plan (kit list 1-5, Walliams as the end-to-end proof, my pick keep it).
- **Sam: Y** to the plan: 1-5 then Walliams.
- **Needs Sam:** nothing open.
- **Next (chat 11, Opus medium):** 1 facehouse in the people kit (people.py: `head: house NAME` from a people file,
  not only CAST); 2 turned views (three-quarter, side) for house heads; 3 facehouse whole-head kittest (Andy and
  Kemi held); 4 facepick's pick sheet draws its heads with facehouse; 5 catalogue row: ready for films (look
  'detail'). Then Walliams end to end from his photos (`facehouse.py brows` on him), blind name test. Andy and Kemi
  stay pixel for pixel unless Sam says.
- **Sam's words kept:** "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far
  into caricature. Andy is finished. Kemi: bigger plaits, small pupils, calm eyes, face from photos, ears hidden,
  mouth as it is, neckline kept.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (LIKENESS, brows); rule 49.
- **Open rule requests:** none.
- **For Claude:** CAST badenoch unchanged (brow_arch 0.03 now bends ends); pick JSON gained 'brow' {high 0.568, peak
  0.42}; P4.brow_uv/brows took `peak`; facehouse.face_layout, _brow_gap, LID0, SHARP. Andy's pick has no 'brow'
  (do not run browcheck on him: it would move his finished brows). Name pack key in this chat's scratchpad only.


## Face tool, where things stand (chat 11 of the face chain, 14 Nov; handed over at amber)
- **Rules that bite next:** 49 (the blind name test is the judge), 86 (every tool gets a kittest), 85.
- **Done (chat 11):** 1 people kit: a people file can say `head: house NAME, hair PIECE, look LOOK` and `house: ...`
  (`story/facetool-people.txt` holds Andy and Kemi). 2 turned views (three-quarter, side, both behinds) for house
  heads; sheet `notes/morning/facehouse-turned-c11.jpg`, sent to Sam. 3 kittest facehouse_whole_head: Andy and Kemi
  held pixel for pixel, the people file builds the same faces, no turned view falls back to the plain head. facehouse
  and people kittests pass.
- **Seen, not fixed (taste, for Sam's look):** from behind the neck reads long (the people kit's old turned heads do
  the same); turned brows are turnhead's plain brows (no arch); Andy's dark top from behind is a plain shape.
- **Next (chat 12, Opus medium):** 4 facepick's pick sheet draws its heads with facehouse; 5 catalogue row: ready for
  films (look 'detail'), naming `turns` and the people lines. Then Walliams end to end from his photos
  (`references/blessed/likeness/` w06, w07, w01, w02 fronts, w09 three-quarter; facepick make, `facehouse.py brows`,
  his lines in the people file), blind name test, and send Sam a sheet of the Walliams head (with a Checks line).
- **Needs Sam:** nothing open.
- **Sam's words kept:** "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far into
  caricature. Andy and Kemi finished: do not change their heads.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (IN THE PEOPLE KIT, TURNED).
- **Open rule requests:** none.
- **For Claude:** people.py `_house`, head kind 'house', 'house' line -> house_kw; facehouse HAIR, TURN_PROF,
  _swept_shapes/_swept_strokes (swept split, pixels unchanged), _turned_braids, _outside, _turn_person (crown rows
  extended: the house outline's few rows notched the skull), install_turned, turns(); kittest held md5s are the
  chat-10 heads. kittests allowlist gained facehouse.py (a kit, not a film).


## Face tool, where things stand (chat 12 of the face chain, 14 Nov)
- **Rules that bite next:** 49 (the blind name test is the judge), 86 (every tool gets a kittest), 30 (a repeated note).
- **Done (chat 12):** Sam's note "our 3/4 front poses simply don't work and look gaunt and weird" fixed for every
  turned head (turnhead): the three-quarter is now 30 degrees on a flat face plan, both eyes and brows show (the far
  one narrowed, never under half). Why it failed: at 45 degrees the muzzle-shaped plan hid the far eye and hollowed
  the far cheek. Side and behind unchanged pixel for pixel. Sheet `notes/morning/threequarter-c12.jpg` sent (Andy,
  Kemi, Vance, before and now). Kittest turned_heads_for_anyone now holds side/behind and counts both 3/4 eyes.
- **Seen, not fixed:** Kemi's near jaw has a small notch where the plaits meet the neck (there before); the far eye
  sits close to the far outline (cartoon-normal; for Sam's look).
- **Next (chat 13, Opus medium):** 4 facepick's pick sheet draws its heads with facehouse; 5 catalogue row: ready for
  films (look 'detail'), naming `turns` and the people lines. Then Walliams end to end from his photos
  (`references/blessed/likeness/` w06, w07, w01, w02 fronts, w09 three-quarter; facepick make, `facehouse.py brows`,
  his lines in the people file), blind name test, and send Sam a sheet of the Walliams head (with a Checks line).
- **Needs Sam:** his look at the three-quarter sheet (a no comes back as a note; the chain does not wait on it).
- **Sam's words kept:** "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far into
  caricature. Andy and Kemi finished: do not change their front heads.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (IN THE PEOPLE KIT, TURNED).
- **Open rule requests:** none.
- **For Claude:** turnhead YAW['three'] 30, TurnFace.three, PLAN3/KFAR/KMIN (3/4 only); VANCE_TURNED_MD5 now yaws
  90-180. Kittests critique_helper_kind and round_page fail on the main line before this change too (not face work).


## Face tool, where things stand (chat 12 of the face chain, 14 Nov)
- **Rules that bite next:** 49 (the blind name test is the judge), 86 (every tool gets a kittest), 30 (a repeated note).
- **Done (chat 12):** Sam's note "our 3/4 front poses simply don't work and look gaunt and weird" fixed for every
  turned head (turnhead): the three-quarter is now 30 degrees on a flat face plan, both eyes and brows show (the far
  one narrowed, never under half). Why it failed: at 45 degrees the muzzle-shaped plan hid the far eye and hollowed
  the far cheek. Side and behind unchanged pixel for pixel. Sheet `notes/morning/threequarter-c12.jpg` sent (Andy,
  Kemi, Vance, before and now). Kittest turned_heads_for_anyone now holds side/behind and counts both 3/4 eyes.
- **Done, round 2 (Sam's notes on the sheet):** the three-quarter outline smoothed (bumps and corners, Kemi's chin hooks:
  the chin's width jumped from the face's); the neck's top corners no longer poke out under the jaw; the three-quarter
  jacket fitted (rounded shoulders, no hard shadow panel or seam, the shirt V nearer the middle: it read as a ridge);
  Kemi's open collar now carries round to three-quarter (was the plain buttoned shirt). Sheet
  `notes/morning/threequarter-c12b.jpg` sent. Sam: the far temple stays bare skin (line of sight hides it): do not add hair there.
- **Next (chat 13, Opus medium):** 4 facepick's pick sheet draws its heads with facehouse; 5 catalogue row: ready for
  films (look 'detail'), naming `turns` and the people lines. Then Walliams end to end from his photos
  (`references/blessed/likeness/` w06, w07, w01, w02 fronts, w09 three-quarter; facepick make, `facehouse.py brows`,
  his lines in the people file), blind name test, and send Sam a sheet of the Walliams head (with a Checks line).
- **Needs Sam:** his look at the three-quarter sheet (a no comes back as a note; the chain does not wait on it).

## Face tool, where things stand (chat 13 of the face chain, 14 Nov)
- **Rules that bite next:** 49 (the name test cannot judge Walliams: calibrated), 86 (every tool gets a kittest), 30.
- **Done (chat 13):** 4 facepick's sheet draws A, B, C the house way (facehouse `src`/`variant`); 5 catalogue rows: the
  house head READY for films (look 'detail', people lines, `turns`). Walliams end to end from w06 w07 w01 w02 (+w09):
  three heads 85/87/81%, line-up first each; pick B saved (references/faces/walliams/pick, `picked_by` Claude: Sam to
  confirm); brows measured; lines in facehouse.CAST (swept, smirk, cocked brow 0.025, push 1.1). Faults found and
  fixed in the tools: beardkit only ran on the face finder's hint (his grey stubble read 0): now always, kept over
  BEARD_MIN 0.2; the house head had no beard: `stubble()` (Blessed's made general, measured colour and coverage);
  smiling photos tuned his eyes shut (0.08 open): EYE_OPEN_MIN 0.2; swept sides stood off his narrower temples (white
  sliver): laid onto the face edge where over 0.015 off. Andy and Kemi held pixel for pixel. Kittests pass.
- **Name test:** new head not named (Hegseth/Newsom, low), 2nd of 10 in the line-up (after Cowell); a cocked brow and
  push 1.15 changed nothing. Calibration: Sam's approved Blessed head also not named, 9th of 10. Sheet sent:
  `notes/morning/walliams-facetool-c13.jpg` (photos, Blessed head, new head, turned).
- **Seen, not fixed:** the stubble is drawn front-on only (turned views bare); his eyes read smaller and more tired
  than the Blessed head's.
- **Next (chat 14, Opus medium):** stubble carried round the turned views (turnhead's beard path, as Vance's goatee);
  then Sam's notes on the Walliams sheet, if any.
- **Needs Sam:** Y/N on the new Walliams head (the chain does not wait on it).
- **Sam's words kept:** the far temple of a three-quarter stays bare skin (chat 12b). "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far into
  caricature. Andy and Kemi finished: do not change their front heads.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (TURNED) and `stubble`.
- **Open rule requests:** none.
- **For Claude:** facehouse.load(name, src, variant); CAST['walliams']; stubble() after age_lines; facepick
  BEARD_MIN, _beard_word (pick 'beard' is now a dict). Scratch run: `facepick.py walliams OUT w06 w07 w01 w02 --tq w09
  --says "glasses=no, age=55, hair=plain"` (~3 min). Chat 12b: turnhead YAW["three"] 30, TurnFace.three, PLAN3/KFAR/KMIN, _smoothed, chin ease (3/4 only); views three torso (open_curve top, v_at 0.24, neck to -130); facehouse open_collar_three; VANCE_TURNED_MD5 now yaws
  90-180. Kittests critique_helper_kind and round_page fail on the main line before this change too (not face work).


## Face tool, where things stand (chat 14 of the face chain, 14 Nov)
- **Rules that bite next:** 49 (the name test cannot judge Walliams: calibrated), 86, 30.
- **Done (chat 14):** Walliams' stubble carried round his turned views (three-quarter, side; a sliver on the far jaw
  from three-quarter behind; none from behind), drawn by the front's own `stubble` on the turned face, as Vance's
  goatee. Andy and Kemi held pixel for pixel (front and turned rows unchanged). Kittest facehouse_beard_turns; the
  face and turn kittests pass. Sheet sent: `notes/morning/walliams-turned-c14.jpg`. No notes from Sam on c13's sheet yet.
- **Seen, not fixed:** side view: the stubble's top edge ends in a straight step behind the jaw (as the front's top
  edge); his eyes read smaller and more tired than the Blessed head's.
- **Next (chat 14, in hand):** Sam's two jobs below; then Sam's notes on the Walliams sheets, if any.
- **Sam, 14 Nov (to chat 12), two jobs (chat 14 doing them):** (a) Y: background people on the generic head
  (views.head_view) move onto the new three-quarter turned head. (b) "clothes remain consistent no matter the pose, as
  that was the source of the Kemi problem": the outfit described once and every view (front, three-quarter, side,
  behind) draws it; nothing outfit-like hides in a hair piece (Kemi's open collar sits in the braids code: make it the
  outfit's own choice, e.g. `outfit: suit ..., open collar`). A kittest draws each outfit from every view and fails
  when a view drops a piece the front has (rule 86).
- **Sam on the Walliams sheet (14 Nov, a N):** "I would recognise the original as Walliams a lot more ... Just
  doesn't look like him. Very different head shape too." Why (chat 13's read): the face tool tuned the inner face to
  likeness.py's measures off a smiling photo, but the head's OUTLINE is the house's from those measures: narrow
  temples, long, tapering, where his (Blessed, Sam: "That's him") is a broad box, jaw as wide as the cheeks, long heavy
  lower face (blessed_walliams.outline, LOW 1.15); the eyes also came out small and tired. Plan for chat 14 (after Sam's
  two jobs): `facehouse.py trace walliams` (his outline off his photos, `shape`, as Kemi's) and check it against the
  Blessed outline; bigger, livelier eyes as the Blessed head's; one sheet, Blessed vs new side by side, to Sam. The
  name test is no judge for him (calibrated); Sam's eye is. Lesson to propose: the face tool's sheet puts a head Sam
  already knows (any hand-made one) beside A, B, C, and traces the outline by default.
- **Sam's words kept:** the far temple of a three-quarter stays bare skin (chat 12b). "Please don't limit yourself on budget." Age lines stay. Look 2 ('detail'). Not too far into
  caricature. Andy and Kemi finished: do not change their front heads.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (TURNED) and `stubble`.
- **Open rule requests:** none.
- **For Claude:** facehouse._turn_face calls stubble(ink=False) (turnhead inks the outline); facehouse.load(name, src,
  variant); CAST['walliams']. Older code names: notes/archive/facetool-handovers.md (chat 13).



## Face tool, where things stand (chat 14 of the face chain, 14 Nov)
- **Rules that bite next:** 86 (every tool gets a kittest), 30 (Walliams is a repeated note: say why it failed), 49.
- **Done (chat 14):** Walliams' stubble goes round his turned views (front's `stubble` on the turned face, as Vance's
  goatee); Andy and Kemi pixel for pixel; kittest facehouse_beard_turns; sheet `notes/morning/walliams-turned-c14.jpg`.
  Job (a) checked: all 29 people in the 3 people files (crowds included) already turn on turnhead's 30-degree
  three-quarter (people_turned, famous, house); only the test-only hand-made Walliams part (HEAD_PARTS) does not.
  Kittest kit_people_never_generic holds it for every people file.
- **Next (chat 15, Opus high: new building):** (b) one outfit, every view. Found: the kit's torso extras (robe,
  officer, open shirt, crucifix, scarf, zip; people._extras) run only in the FRONT torso (traitors_cast.torso via
  B.torso); turned views draw views.torso_view's plain clothes, so every extra drops when a person turns. Kemi's open
  collar lives in the braids code (front `braids_behind`, three `_turned_braids`), none at side/behind. Build: the
  open collar as an outfit choice (`outfit: suit ..., open collar` in people.py, drawn by the torso, out of the hair
  code, Kemi's lines carry it: her pixels held); each extra drawn in three, side, three_back, back; a kittest drawing
  every extra and outfit from every view that fails when a turned view drops a piece the front has. Then Walliams'
  head shape (below). One sheet to Sam: the extras turned, and Blessed Walliams vs new side by side.
- **Sam on the Walliams sheet (14 Nov, a N):** "I would recognise the original as Walliams a lot more ... Just
  doesn't look like him. Very different head shape too." Why (chat 13's read): the inner face was tuned off a smiling
  photo, but the OUTLINE is the house's: narrow temples, long, tapering, where his (Blessed, "That's him") is a broad
  box, jaw as wide as the cheeks, long heavy lower face (blessed_walliams.outline, LOW 1.15); eyes small and tired.
  **Sam's direction (replaces the lesson chat 13 offered):** "I think it just needs to be able to draw the face shape
  from the reference a lot more intelligently": the face tool reads the head's whole shape off the photos itself
  (temples, cheeks, jaw, chin, crown with the hair), for every face, not a house outline from a few measures; also
  bigger, livelier eyes as the Blessed head's. A new build at Opus high, judged on Walliams beside the Blessed head
  Sam knows (Sam's eye is the judge; the name test is calibrated out). Andy and Kemi's front heads held.
- **Seen, not fixed:** side view: the stubble's top edge ends in a straight step behind the jaw.
- **Needs Sam:** nothing open (the Walliams N is being worked).
- **Sam's words kept:** the far temple of a three-quarter stays bare skin (chat 12b). "Please don't limit yourself on
  budget." Age lines stay. Look 2 ('detail'). Not too far into caricature. Andy and Kemi finished: do not change them.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP; people.py `_extras`,
  views.py `torso_view`.
- **Open rule requests:** none.
- **For Claude:** facehouse._turn_face calls stubble(ink=False); open_collar / open_collar_three (facehouse 680/691);
  PF.open_shirt/crucifix/scarf/zip_top, PP.robe_torso/officer_torso; views.torso_view(img, p, sp, view). Older code
  names: notes/archive/facetool-handovers.md.


## Face tool chat 15 handover (archived by chat 16, 14 Nov)
- **Rules that bite next:** 30 (Walliams is a repeated note: say why it failed), 86 (every tool gets a kittest), 49.
- **Done (chat 15):** (b) one outfit in every view. Every extra (robe, officer, open shirt, crucifix, scarf, zip) and
  Kemi's open collar (now an outfit choice, `outfit: ..., no tie, open collar`, out of the hair code) is drawn
  turned: the front's drawing wrapped round the turned body, its own back where it goes round (belt, sash, scarf at
  the neck, the top's collar); the judge's wig turns with his head. Andy and Kemi front pixel for pixel; Kemi's
  three-quarter unchanged, her side now keeps the collar. Blessed's frames still match (new turned pieces scored
  apart). Kittest outfit_every_view (34 piece-views; fails on the old code). Sheet `notes/morning/outfit-every-view-c15.jpg`.
- **Next (chat 16, Opus high: new building):** Sam's face-shape build (below), judged on Walliams beside the Blessed
  head; one sheet to Sam with this chat's outfit sheet.
- **Sam on the Walliams sheet (14 Nov, a N):** "I would recognise the original as Walliams a lot more ... Just
  doesn't look like him. Very different head shape too." Why (chat 13's read): the inner face was tuned off a smiling
  photo, but the OUTLINE is the house's: narrow temples, long, tapering, where his (Blessed, "That's him") is a broad
  box, jaw as wide as the cheeks, long heavy lower face (blessed_walliams.outline, LOW 1.15); eyes small and tired.
  **Sam's direction:** "I think it just needs to be able to draw the face shape from the reference a lot more
  intelligently": the face tool reads the head's whole shape off the photos itself (temples, cheeks, jaw, chin, crown
  with the hair), for every face, not a house outline from a few measures; also bigger, livelier eyes as the Blessed
  head's. Judged on Walliams beside the Blessed head Sam knows (Sam's eye is the judge). Andy and Kemi's front heads held.
- **Seen, not fixed:** side view: the stubble's top edge ends in a straight step behind the jaw. Kittest
  people_from_a_description fails on one thing not this job's: `protest_tiers_cast.py` imports the people kit before
  Sam approved it for films (protest-tiers chat's work); Blessed's frames themselves pass.
- **Needs Sam:** nothing open (the outfit sheet is to look at; the Walliams N is being worked).
- **Sam's words kept:** the far temple of a three-quarter stays bare skin (chat 12b). "Please don't limit yourself on
  budget." Age lines stay. Look 2 ('detail'). Not too far into caricature. Andy and Kemi finished: do not change them.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (the traced outline, `trace`).
- **Open rule requests:** none.
- **For Claude:** views.WrapPen/torso_outline/TORSO_EXTRAS; people.turned()/pieces()/kit_torso_view, FILM_TURNED,
  DREW; PP.robe_back/officer_back/open_collar(_three)/collar_torso; PF.scarf_back/zip_back; people_turned 'wig';
  facehouse sp['neck_redrawn'] (braids re-lay the collar). Older code names: notes/archive/facetool-handovers.md.


## Face tool, where things stand (chat 16 of the face chain, 14 Nov)
- **Rules that bite next:** 30 (Walliams is a repeated note: the photos' shape alone did not give his box, below), 86, 85.
- **Done (chat 16):** the face tool now reads each head's whole shape off the front photos (face edge with ears cut,
  hair-and-skin silhouette, crown, hairline, side hair) and draws the face outline, the swept hair's cap and sides and
  bigger eyes from it (on by default; Andy and Kemi held pixel for pixel). Walliams measured. New check sheet
  `notes/morning/walliams-head-shape-c16-wip.jpg` (not sent: not good enough yet). Kittest facehouse_head_from_photos
  (fails on the old outline). Sent nothing to Sam this chat.
- **Why it is not his head yet (rule 30):** drawn true to his photos, the head reads as a light bulb: wide temples,
  the chin rounding in. The photos say his jaw is only a little wider than average (about as Kemi's, against Andy's);
  Blessed's box (jaw as wide as the cheeks, face half width 0.50 against his photos' 0.44, the lower face stretched
  1.15, mouth and eye spacing pushed) is a caricaturist's exaggeration the photos do not show. Pushing the outline
  from the average face x3 barely moved it (his differences are small) and made the hair a mushroom (capped since).
- **Next (chat 17, Opus high: still new building):** make the push work on the head's proportions, not its absolute
  rows: (a) the face's width against its features (Blessed: big face, small features; P4's face_wide push is not yet
  applied to the measured outline), (b) the jaw-to-cheek ratio and chin squareness pushed against the three faces'
  middle, (c) the beard's edge counted as jaw. Then judge on Walliams beside Blessed with the compare sheet (one
  extra critique round), carry the measured widths into the turned views (still the house outline's: unchecked),
  and send Sam ONE sheet with chat 15's outfit sheet (`notes/morning/outfit-every-view-c15.jpg`, not yet sent).
- **Seen, not fixed:** the side view's stubble edge ends in a straight step behind the jaw. Kittest
  people_from_a_description fails on protest-tiers' early import (not this job's).
- **Needs Sam:** nothing yet.
- **Sam's words kept:** the far temple of a three-quarter stays bare skin. "Please don't limit yourself on budget." Age
  lines stay. Look 2 ('detail'). Not too far into caricature. Andy and Kemi finished: do not change them.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facehouse.py` MAP (WHOLE HEAD).
- **Open rule requests:** none.
- **For Claude:** FH.measure_head/_head_rows/drawn_head/_swept_measured/_Squeeze/compare/STRONG, SHAPE_PUSH, SKIN_BIAS,
  HEAD_EYES, EYE_OPEN_HEAD; pick key 'head', lines `head`, `shape_push`; `facehouse.py compare OUT walliams blessed:walliams`.
