# Proposal: Craft-next Step 2: what to change, given Step 1's causes

Status: open

## Problem
Sam gives 8-13 notes per film about shot design: where the camera sits, how big people are, where the eye goes, what
matches across cuts. The aim Sam agreed is at most 3 per film on the next two films, none returned twice, every film
new, without trimming the joke or reusing content. Step 1 (changes nothing) has now sorted the 36 such notes from the
last three films by cause and by whether a still picture could have shown the fault. The decision is the ONE change put
to Sam for his yes now, in what form, and saying honestly how much of the 36 it can reach and what it leaves.

## Facts
- Step 1 results, notes/proposals/craft-next.md, "Step 1 results" (one chat's reading; counts exact, causes judged):
  cause: plan wrong or silent 20, Sam's late choice or changed mind 11, build drifted from a right plan 5.
  Seen: on a still 20, only when moving 16 (44%).
- Cross-count from that table (this chat, from the rows): still + plan 12 (F13, A10, Blessed 7, 11, 12, 15b, 22, 42,
  Remakes 32, 49, 56, 67a); still + Sam 6 (A3, Blessed 30, 33, 37, Remakes 33, 71); still + drift 2 (Remakes 61, 75);
  moving + plan 8 (F1, F3, F7, F23, A1, A31, Blessed 32, Remakes 47); moving + Sam 5 (F4, A4, A7, Blessed 18,
  Remakes 63); moving + drift 3 (G12, Blessed 17a, 46).
- Moving-only by kind (Step 1): camera height or distance judged right on stills and wrong when moving (F1, A1: both
  passed the framing research and pencil roughs); timing and order (F23, A7, F3, F4, A4, A31, F7); cuts and drift in
  time (17a, 46, 47, 63, 18, 32, G12).
- By film: EPR 13 (moving-only 10; Sam: EPR was built with no composition in mind), Blessed 13 (moving-only 4),
  Remakes 10 (moving-only 2).
- The adopted craft-next plan (Sam's Y, 17 Nov) said Step 2 takes its form from Step 1: if build drift is a third or
  more, a measuring check against agreed frames; if plan faults dominate, a per-shot card sheet and its gate only.
  Drift is 5 of 36, so the measuring branch is not triggered. That plan's judge named three open faults: per-film cost
  unmeasured (F4), measuring people's positions in flat-people films unverified (F5), EPR partly Sam's late choices (F6).
  The adopted plan also said: if more than a third are movement-only, Sam is told plainly that a still-only change
  cannot reach the number.
- Rule 11 today (guides/film-quality-rules.md:23): one rough composition sheet of the 3-4 key shots before building;
  pencil-style sketch; its gate (preflight.gates, source/preflight.py ~230) passes on any dated "Composition sheet
  sent:" line. Remakes logged its built film's check sheet (notes/remakes.md:85); Blessed its sets sheet
  (notes/archive/blessed.md:35). Rule 10 (line 22): framing and timing planned up front; its check is eyelines
  (LOOKS_AT) and holds (critique M2).
- source/rough.py already draws each new place through its own camera with 1.75 m outlines at people's depths, and
  each move's person at its key moments on a draft clock (the order of beats, timing waiting for the voice).
- Shots per film: Blessed 17+ (source/blessed.py:182), Remakes 14 (source/remakes.py:141, with SHOT_CAST per shot).
- Sam declined (16 Nov) a moving rough before building and a note-sorting chat (notes/proposals/epr-lessons.md); its
  judge found the France and Albania cameras failed only when seen moving. CLAUDE.md: movement notes get short clips
  (no yes needed); an animatic is offered before any full render.
- Framing lessons F1-F12: research/crowds-and-big-action.md (tall frame in bands, eye level first, focus near centre
  at cuts).
- Per-film cost of any added planning step: unmeasured (a planning chat in the ledger runs about 0.4% of a week,
  notes/ledger; unchecked for this task). Budget aim: a film within 15% of a week.

## Record
notes/proposals/craft-next.md
notes/proposals/craft-census.md
notes/proposals/craft-census/notes.tsv
notes/proposals/epr-lessons.md
notes/proposals/craft-first-round.md
research/crowds-and-big-action.md
guides/film-quality-rules.md
guides/preflight.md
source/rough.py
source/preflight.py
notes/archive/protest-tiers.md
notes/archive/blessed-notes-animatics-1-2.md
notes/archive/blessed.md
notes/remakes.md
notes/ledger
CLAUDE.md
