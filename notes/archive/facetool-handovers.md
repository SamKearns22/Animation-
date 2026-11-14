
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

