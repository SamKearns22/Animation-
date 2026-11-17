# Helper B: Craft-next Step 2

## Leak
The problem file passes on the adopted plan's branch ("a per-shot card sheet and its gate only"). I set it aside and judged it alongside the other options.

## Results
- 36 shot-design notes across 3 films: plan wrong or missing 20, Sam's late choice 11, drift 5. Could be seen on a still: 20. Only seen moving: 16 (craft-next.md, Step 1 results). The causes are one chat's judgment. Five rows rest on thin evidence.
- Cross-counts (I checked them against the table): still+plan 12, still+Sam 6, still+drift 2, moving+plan 8, moving+Sam 5, moving+drift 3.
- Rule 11's gate is a paper gate. It passes any dated line. Remakes logged its *built* check sheet as the "composition sheet". Blessed logged its sets sheet with no people placed (notes/remakes.md:85, notes/archive/blessed.md:35, preflight.py:230). On all three films, no picture of a planned shot with its people in it existed before building.
- rough.py draws each place through its own camera with 1.75 m outlines. It draws each move with **the person alone**, and in draft mode at a fixed mark (rough.py:163-224). Nothing combines the shot itself: camera, people at their positions and beats in order.
- Film costs: Remakes 36%, Blessed 62%, EPR about 101% of a week (notes/ledger). All three are far over 15%, and rounds of notes drive the cost.
- **Gap:** the record does not say whether notes Sam gives on a sheet *before building* count toward "3 per film". The number to beat needs this defined.

## The real decision
The real question is where in the film Sam first sees each shot's design, and in what form. Today that is the animatic, so every shot-design note becomes a rebuild. A card is only one way to move that point earlier. A bigger lever is making the pre-build picture the *real* shot (real camera, real people positions, beats in order) rather than a written description of it.

## Root cause
The plan is never shown as the shot. Places and people are approved separately, cameras are set in code (A10, Blessed 11, Remakes 49: "no reason"), and the gate accepts any sheet. So the first composed picture of a shot is the built film. F1 and A1 "passed stills" because those stills were place views and pencil roughs, not the shot with people at their real heights over time.

## Approaches weighed
1. **Written shot cards plus a sheet drawn from them** (the adopted branch). Reaches still+plan 12, at most. A card can be filled in on paper and still be wrong.
2. **Reframe: a shot board drawn by the kits.** rough.py gains `shots`: every shot through its real camera, its cast at their marks and true heights, at 3 moments on the draft clock (start, key beat, end), with the next shot's first frame beside it. The gate checks that the board's record covers every shot and was sent before the film's code existed. This reaches still+plan 12, plus the order/timing/cut rows that show up across 3 frames (F3, F7, F23, A31, Remakes 47): about 17 of 36. Sam's 6 still choices would arrive before building, where they are cheap.
3. **A moving stand-in rough before building.** It would reach most moving rows. Sam declined it on 16 Nov, and there is no new evidence strong enough to put it back.
4. **Learn first:** define how sheet notes count, and measure the board's cost on one film's existing data before any rule changes.

I chose 2, with 4's learning as the first step.

## Proposal
**Learn first (changes nothing, about 0.5% of a week, unchecked):** run the board on Remakes' story files (SHOT_CAST, 14 shots) and Blessed's. Count how many of their 22 still+plan notes the board visibly shows. Time the run. Agree the counting rule: notes given on the board are logged as "board notes", not film notes.

**Change 1 (only change, its own yes):** Rule 11 is rewritten so its sheet is the kit-drawn shot board, covering every shot. Enforcement: the pre-flight gate reads rough.py's record, not a typed line. It refuses if any shot in SHOT_CAST is missing from a sent board, or if the board was sent after the film's code was first committed. Build: one Opus chat, about 2-3% of a week once (unchecked). Per film: about 0.5% (unchecked).

**Number to beat:** plan-caused shot-design notes on the animatic at most 1 per film on the next two films (Step 1 average: 20/3 ≈ 6.7). None returned twice. Counted with census tags at each end-of-film review.

**Plainly for Sam:** this reaches about half the 36 at best, around 6 per film. It does not reach Sam's own late choices on moving shots (5), drift (5), or height felt only in motion (F1, A1). "At most 3 per film" needs a later change, chosen when two films' results show which of those remains largest.

What Sam would notice: one picture sheet of every shot, with people placed and three moments each, before anything is built; fewer camera notes on the animatic.

## Sam test
Q1 Expert: it fixes the gate that can be passed on paper and reuses the kits, which is what an expert would do first.
Q2 Best result: built on the 36-note census across 3 films. The census is one chat's judgment, as noted above.
Q3 Comprehensive: the gate reads the record, so a typed line cannot satisfy it. Root cause shown above. Success is measured by the census tags.
Q4 Most intelligent: four distinct approaches were weighed. Cards alone reach less.
Q5 Risk: one rule and one gate, undone alone. It is tried on past films before Sam's yes.
Q6 Checked: sources are named. Costs are marked unchecked.
Q7 Not cheap: it is sized to every shot with real people, not 3-4 pencil shots. Its honest shortfall is stated.
Q8 Nothing temporary: a permanent rule, reviewed at film end.

## Lost / Added
Lost: building waits for Sam's look at a fuller sheet, about 0.5% of a week per film.
Added: the shot board (every shot, real camera, people, 3 moments) and a gate that cannot be passed with a typed line.

## Unchecked
Build and per-film costs. Whether the 3-moment board shows F3/F23/47 (tested in the learning step). Whether the board works for flat-people films (Step 1 F5).
