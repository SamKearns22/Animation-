# The chat's own idea (written before the helpers)

Reading of the facts: the article's biggest lever (a slimmer CLAUDE.md) is small here in money: all of CLAUDE.md is
about 0.04% of a week a chat, ~1.3% a film. Re-reading the app's own 80k and long work histories cost far more, and
the project already has stage packs (the article's "load only when used"). So most of the article is already done in
another form; the real gaps are small and two are unmeasured.

1. Change A: move word for word (sentences.py allows it) the stage-only parts of CLAUDE.md into the packs that use
   them: the chain mechanics in "Models and chats" (create_session details, chat size numbers) into a "Handover and
   next chat" pack; the proposal-route paragraph and rule-writing mechanics of "Rules are permanent" into the
   proposal pack; "Files" details into Final and posting. Keep in CLAUDE.md a one-line pointer for each. Aim: about
   a third less (~2,200 tokens), ~0.4% of a week a film. Check: sentences.py already refuses a lost sentence; add a
   kittest that each pointer names a pack section that exists.
2. Change B: a short "If this chat is shortened, keep:" section (locked shots, open notes and their numbers, the
   brief checklist, any Override and its one ask, the next step). About 50 words. No chat has been shortened yet
   (max 414k of 1M), so this is insurance; check: a kittest that the section exists and names the four items.
3. Change C: a five-line "daily commands" list (render, checks, finish.py, handover start/end) with the quiet flag
   each takes, in the Checks pack, not CLAUDE.md.
4. Learn (no change yet): (a) from the ledger, cost per finished stage against chat length in steps, to set the
   step numbers by measurement; (b) run the saved name tests with the namer on Sonnet; switch only if it matches
   Opus on every saved case. (c) measure what the hooks print per step from one chat record.

Lost: a chat must open a pack to see chain mechanics (risk a chain step is missed). Added: ~50 words of insurance.
