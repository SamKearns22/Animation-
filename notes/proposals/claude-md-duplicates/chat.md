# Chat 8's own idea (written before the helpers)

1. One copy per rule, kept where a chat looks for it; anything only the removed copy said is merged into the kept one:
   - Handover lines: keep line 25 (Messages to me), merged: "The handover's 3 lines go at the bottom of the message:
     what's done and what's next; "what to type" only when the chain has stopped for good (no save); never a request
     to start a chat myself." Lines 101-102's sentence goes.
   - Project attached: keep line 115, merged with 79-80: "Every chat starts with the Animation- project attached
     (source_url of the repo, revision the main line); without it, add it before any work and say so, and the reply
     lists it before I'm told the chat is working." Lines 79-80 go.
   - Hook Text and sign-off: keep 36-37 (animatic) and 127-128's TikTok style; 127-128 says only "Hook Text in
     TikTok's white-box style; sign-off command in guides/job-packs.md, Checks and animatic" (the "every video ends"
     part folded into 36-37: "Every animatic and video carries...").
   - New-rule proposals: line 56 goes; the proposal-route bullet gains "(new rules and lessons too; wait for my
     numbers)". Line 57-59 ("I want a rule") stays: it is about Sam's words, not the route.
   - Code names: line 19 drops "No code names;" (line 13 holds it).
2. sentences.py allowance: a "Merged in CLAUDE.md" table (in the rulebook, beside the dates table): removed sentence |
   first words of its kept twin. A removed sentence passes only if its row exists AND the twin is still in CLAUDE.md;
   kittest covers a row whose twin was later deleted (must refuse).
3. Guard, the 10-situation test: a script picks 10 past situations from earlier chats (one or two per duplicate,
   rest random), writes two packs (old CLAUDE.md / new), two fresh helpers answer "what do you do / what does the
   message say", the script compares the answers' decisions; any difference refuses the merge.
4. Beat: ~0.15-0.25k tokens saved (to ~4.8k), no meaning lost, no rule written twice in these five.
