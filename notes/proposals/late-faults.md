# Proposal: Faults made while building are found chats later, at the gate, and each costs a whole fix chat

Status: open

## Problem
Sam's aim (15 Nov): cut the cost of every stage of production as far as possible without harming quality. On
Protest Tiers (paused at ~53.6% of a week against ~20% planned, 33 chats), the chats that only critiqued, reworked,
re-rendered or chased tool crashes cost about 16% of a week, about 30% of the film. Traced through the archived
handovers, most of those faults were made in one chat and only found several chats later, when the round's gate
(the critique pack, the first quick pre-flight, the animatic render's picture checks) first looked. By then the
building chat had ended, so a new chat paid its start-up (reading notes, finding the code again) just to fix them,
and fixes made without the code fresh sometimes failed and came back (rule 30). Some of the faults were in the shared
tools, not the film: the film was the first thing to run them. Quality must not fall; every film is new (no content
reuse). The question is which change, to which rule, tool or check, would stop this at the lowest total cost.

## Facts
- Film totals (notes/proposals/learn/protest-tiers-costs.md, from notes/ledger/protest-tiers.json): 33 chats, 53.6%
  of a week; moves stage (both passes) 25.3% against a 7.6% plan; critique + rework + re-render + code-finding chats
  (ledger rows 13, 15, 17, 18, 19, 27, 28, 30) 16.0%. Opus chats 1.3-3.2% each; per-chat cost did not fall after the
  13 Nov fixes; the count of chats is the lever named by chat 2's Learn step.
- LIMIT: chats 9-32 (ledger sids 01Gzna...) cannot be opened from this account (get_session "not found", checked
  again by chat 3). Their causes below come from the archived handovers' own words, not from the chats' records.
- Chain 1, moves first pass (notes/archive/protest-tiers-handovers.md, chat 13-16 handovers): moves built in chat 13
  (stills only looked at). Critique hunt 1 (chat 14): 21 faults, 15 of them "does not read at phone size" (small,
  dark, hidden beats). Fixed in chat 15 (ledger 3.22%, the dearest Protest Tiers chat). Hunt 2 (chat 16): 16 more,
  mostly the same kind (too small, too dark, not reading); 4 named not fixed. Rule 24 already said Glimpses are judged
  at phone size; nothing measured it while building. Open lesson since chat 14, never written: "every Glimpse beat is
  checked at phone size before the moves pack"; chat 15's: "a Glimpse prop or effect is drawn about twice true size".
- Chain 2, first pre-flight after the moves (chat 16/17 handovers): 44 faults. Many were lists pre-flight needs that
  the film had never declared: EFFECTS, JOKE_PROPS, PROP_SIZES, OUTFIT, LINE_SUBJECTS, TOUCHES/ALLOWED/ORDER_SWAPS,
  solids(t), 'haze' in draw_order; plus pre-flight not reading the critique (ledger name protest-tiers vs code name
  protest_tiers). Chat 17 (~1.8%) filled them in. Pre-flight then crashed (head_view wrapping itself, only inside
  pre-flight's child after install_probes); chat 18 (1.6%) was spent on that crash.
- Chain 3, round 1 (chat 21-30 handovers): build chats 21-26 built steps 1-6, each sending rehearsal clips; chat 26
  wrote "Checks on T2/T3: clean (3 pops named)" (which checks it ran: unchecked). Chat 27 (2.18%) ran the critique.
  Chat 28 ran the round's first quick pre-flight (`preflight.py protest_tiers OUT --text`): 107 faults: 67 teleports
  (hands moving 90-120 cm in one 12 fps frame) in T3's back row and pushers (built chat 26) and T4's buyers, selfie
  and rioters (built chat 25); 9 front/back swaps; 11 pass-throughs 13-21 cm; 4 effect shapes. Chats 29 (2.24%) and 30
  (2.36%) fixed them. Of the 4 effect shapes, the check itself was at fault (its mask took every faint pixel of the fx
  layer, so it saw a "star" in the scatter: chat 29).
- Chain 4, a repeat fault (rule 30; chat 30/31 handovers): the throwing arm folding shut was worked round in chats
  13/14 and 25 by skipping the middle of the throw (`make_pose` jumped past u 0.42-0.57), a window sized to one build;
  blends later folded it again. The render turned each stopped drawing into a black frame and `--faults-named` let
  it through; Sam's note 1 on animatic 2: "There are frames missing." Chat 31 fixed it at the cause.
- Chain 5, shared-tool faults found by the film, not by their own tests (handovers chats 16-18, 28-30): critique.py
  numbered hunt 2 as pass 1 and overwrote hunt 1; the ledger's film name vs the code's module name broke pre-flight's
  critique reading, finish.py's --film and the quick pre-flight (needs `protest_tiers`); the pre-flight crash; the
  effect-shape mask; kittests `people_from_a_description` and `facehouse_whole_head` failing on the main line (chat 18).
- Rules in force (guides/film-quality-rules.md): 8 (rehearse the 3-4 riskiest moves as clips before building the
  rest), 19 (every check ends PASS/FAULT/COULD NOT TEST; one command per step), 24 (Glimpses judged at phone size),
  59 (no animatic without pre-flight passing on the code as it is now), 67 (one pre-flight per round: every fix, then
  the quick check until clean, then pre-flight once, then the render), 89 (one critique pack per stage, two hunts,
  after the stage is built), 30 (a repeated note: find why the first fix failed).
- Tools: a span clip (`final OUT --small --span T0 T1`, source/film_engine.py ~181-300) runs the picture checks
  (preflight.picture_faults) on the frames it draws; clipcheck (teleports, pass-throughs, order swaps;
  source/clipcheck.py) and audit (source/audit.py) run in pre-flight (source/preflight.py ~417-419). Whether a span
  clip also runs clipcheck/audit: unchecked. Chat 29 found a span check by hand: set `F.CLIP_SPAN=(t0,t1)`, then
  `clipcheck.run(F)` and `audit.run(F,t0,t1)`, about 5 s a tier.
- What a fix chat pays before fixing (notes/cost-diagnosis.md, 13 Nov): re-reading history is ~49% of an Opus chat;
  chats over 200k cost most. Protest Tiers chats 0-8 ended at 90-300k history. notes/proposal-route.md: chats 29 and
  31 ran page.py (the named code finder) 0 times and searched the code by hand 25 and 26 times.
- Blessed (the film before; notes/ledger/blessed.json) ran ~22 chats at 1.5-3% each, also with late fix rounds
  (unchecked by cause).

## Record
notes/archive/protest-tiers-handovers.md
notes/proposals/learn/protest-tiers-costs.md
notes/proposals/learn/asks-split.md
notes/ledger/protest-tiers.json
notes/ledger/blessed.json
notes/protest-tiers.md
notes/cost-diagnosis.md
notes/proposal-route.md
guides/film-quality-rules.md
guides/job-packs.md
guides/kit-catalogue.md
source/preflight.py
source/film_engine.py
source/clipcheck.py
source/audit.py
source/critique.py
source/kittests.py
