# Proposal: Routine work keeps running on the expensive model

Status: open

## Problem
Routine work (animatics, splicing clips into the animatic, checks, sound, filing, sending) is meant to run on the
cheaper model (Sonnet) and keeps running on the expensive one (Opus). The check built on 15 Nov to catch this did not
fire once on 16 Nov, although several routine chats ran on Opus. Sam said Y (17 Nov) to "routine stages on Sonnet" as
part of the chat-size rule (built separately, chat A); this proposal is about why the switch does not happen in
practice and what makes it hold.

## Facts
- Why it stopped working, from the Protest Tiers notes' Next lines in git (notes/proposals/chat-size-and-model/
  why-model-switch-failed.md): (1) from 16 Nov 12:46 every Next line gave the Opus medium notes chat "clips with
  `final --span` ... splice fixed seconds into the animatic", so the animatic was made inside the Opus fix chat; on 15
  Nov 18:49 a Sonnet chat had made animatic 3 by splicing, cheaply and correctly. The check's ROUTINE word list skips
  `--span` on purpose and has no word "splice". (2) CLAUDE.md's "Models by stage" itself put clips and "building from
  ... sound" on Opus medium, so France chat 7 (look, check, clip) and chat 8 (sound) on Opus followed the rule as
  written. (3) The check (source/handover.py, `model`) reads only the film notes' first Next line, at start and end;
  it never sees the model a chat is actually opened on (create_session) nor what a chain does. 16 Nov's country
  chains (Albania, Germany, France) were opened from Sam's phone and passed work in their own prompts. (4) Before 15
  Nov 17:29 there was no check at all.
- The platform switch itself works: chats whose parent asked for Sonnet ran on Sonnet (get_session: configured and
  served claude-sonnet-5-5 for Startup reading chat 2 and Learn chat 2). France chats 7 and 8 configured and served
  Opus, medium (get_session, 16 Nov).
- Measured cost (notes/ledger/*.json): Sonnet chats of 8-17 steps cost 0.21-0.39% of a week, 64 steps 0.8%; Opus
  chats of 40-60 steps ~3.4% per 100 steps, 80-100 steps ~2.4% per 100 steps (chat-size-and-model.md Facts).
  Protest Tiers 16 Nov: 24 chats, 39.3% of a week in one day (notes/ledger/protest-tiers.json).
- Switching model inside a long chat re-pays its whole history (notes/cost-diagnosis.md, 13 Nov: $5.80 on Blessed).
- Sam's Y, 17 Nov (notes/proposals/chat-size-and-model/sam.md): aim ~100 steps, up to 150 to finish a stage;
  routine stages on Sonnet; a 40-step floor except notes after an hour's gap or a whole routine stage on Sonnet.
  Chat A builds that wording into CLAUDE.md and rule 85 now (notes/cost-fixes.md, Where things stand).
- Unchecked: how much quality Sonnet loses on the splice/clip/look/sound stages (the critic test on Remakes was to
  decide Sonnet for critique, notes/morning-report.md line 104); how many 16 Nov Opus steps were routine.

## Record
notes/proposals/chat-size-and-model.md
notes/proposals/chat-size-and-model/
notes/ledger/protest-tiers.json
notes/archive/protest-tiers-handovers.md
notes/cost-diagnosis.md
source/handover.py
CLAUDE.md
guides/job-packs.md
