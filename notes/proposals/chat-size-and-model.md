# Chat size and model switching: the measured answer (17 Nov, for Sam's "definitive answer")

## Problem (Sam, 17 Nov)
Advice has swung between more/fewer/longer/shorter chats. Model switching is failing: renders and clips run on Opus.

## Facts (measured, ledger rows with steps, 42 Opus chats, % of a week)
- Fit: chat cost = 1.04 + 0.0063*steps + 0.0000934*steps^2 (fixed start-and-handover cost ~0.5-1.0, noisy).
- Cost per 100 steps by chat length: <40 steps 4.2; 40-60 3.4; 60-80 2.7; 80-100 2.4; 100+ 3.0 (history 280k).
  Cheapest at ~100 steps (s* = sqrt(a/c) = 106), history ~220-260k. Flat between 60 and 150 steps.
- Protest Tiers 16 Nov: 24 chats, 1,479 steps, 39.3% of a week in one day; 10 chats under 60 steps.
  Same steps in ~15 chats of ~100: fit says ~15% cheaper (about 6% of a week). Steps themselves are the big lever.
- Earlier advice reconciled: "short chats" (13 Nov) came from 300-414k chats (chat 5, $27.7) -> true above ~300k;
  "fewer chats" (11 Nov, budget job) -> true below ~40 steps. Both are the two ends of the same U-curve.
- A fresh chat after Sam's notes come back hours later is still right: the 1-hour cache has expired, so the old
  chat re-pays its whole history at write price.

## Model switching: why it "fails"
1. CLAUDE.md puts clips on Opus ("A round of my notes (deciding, fixing, clips): Opus medium"), and
   handover.py ROUTINE deliberately skips `final --span` (clips). Clip renders on Opus are by the rule.
2. handover.py model_faults only reads the film notes' Next line; ROUTINE lacks "check", "look", "sound", "clip".
   16 Nov: "back-half chat 7 (France round 4 look, check, clip)" and "chat 8 (France sound)" were created on
   Opus medium (get_session configured_model claude-opus-5-5); nothing flagged them.
3. When a parent names Sonnet in create_session it works (Startup reading chat 2, Learn chat 2: configured and
   served Sonnet). The platform switch is not broken; the choice is.
4. A Sonnet chat for a ~10-step job pays a full chat start (~0.5-1%), more than it saves; so a separate Sonnet
   chat pays only for a whole routine stage (animatic, final, finish.py, sending, filing), not a clip.

## Proposed (to go through the proposal route before Sam's Y)
- Hand over at ~100 steps or ~250k history (amber 250k, red 350k); never open a chat for under ~40 steps of
  work except: notes after a gap of more than an hour, or a whole routine stage on Sonnet.
- One chain per film at a time (16 Nov ran Albania, Germany and France chains side by side, each paying starts).
- Model check: routine = animatic, final, finish.py, sending, filing, check sheet; a clip stays with the Opus fix
  chat. The check also runs on the create_session prompt (model vs job), not just the notes' Next line.
