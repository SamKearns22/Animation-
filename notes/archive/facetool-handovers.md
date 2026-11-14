
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

