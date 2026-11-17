## Leak
yes: the title asks for "one definitive rule", and the facts put "Fit minimum near 106 steps" up front. Together they steer a helper towards a single chat-length number. The problem also says "the check meant to catch that did not" catch routine work on Opus, but the rule as written sends clips and sound to Opus. Both nudges show in V3.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 4 | 4 | 4 | 17 |
| V2 | 4 | 2 | 4 | 4 | 4 | 18 |
| V3 | 2 | 2 | 3 | 2 | 3 | 12 |
## Sam test
Q1: Yes, with the fixes below. An expert would measure which model each chat was actually served, by job, before changing anything. They would route by job when a chat is opened, and they would say that chat length is the smallest of the three levers.
Q2: The learning reads every chat it can open from the last two films (Protest Tiers and Blessed). That is wider than one day and is the evidence the model decision needs. The size decision rests on 32 Opus chats with step counts, but only 5 of them ran past 80 steps (named).
Q3: Root causes are shown. CLAUDE.md itself puts clips and sound on Opus, and the check only matches words in the next-chat line. The model is enforced in code twice: when a chat is opened and when it starts. Each change has a number to beat.
Q4: Four approaches were weighed: a fixed length, model by job, learn first, and fewer steps. Fewer steps is the biggest lever and is named as its own route, not bundled in.
Q5: The learning changes nothing. The model change and the size change are separate yeses, each undone on its own. The model change waits for its evidence.
Q6: Wrong numbers are corrected: 32 Opus chats, not 42, and Sonnet-labelled 72-79-step chats at 2.6-4.1, not 2.2-2.6. Anything unchecked is marked.
Q7: It is sized by the result. It does not claim that chat size gets a film to 15%. The size saving is stated as small (about 1-6% of a week on a day like 16 Nov).
Q8: Both changes are permanent once made. Each is reviewed against the next film's ledger when Sam calls the film complete.
## Pick
V2
## Why
V1 and V2 make the same core move: learn first, then a model change and a size change as separate yeses, with the rework lever sent to its own route. V2 wins on three points:
- Wider evidence: two films and every readable chat.
- It checks the model each chat was actually served, not the words in its prompt.
- It gives the size rule teeth: a flag on chats that end under 40 steps without a reason.

From V1 I took the gate when a chat is opened, so a wrong-model chat is never started (V2 alone pays a wasted start before it refuses). I also took V1's arithmetic that the best length saves only about 1.2% on 16 Nov, which keeps the size saving honest.

From V3 I took one point: a clip made straight after a fix stays in the fix chat, because a ~10-step Sonnet chat costs 0.21-0.39 and saves nothing.

V3 bundles five changes into one yes and makes them before any learning. It raises amber to 250k against the 13 Nov evidence. It also allows one chain per film, but 16 Nov's three chains ran side by side and that slows the film without cutting cost.
## Faults in the pick
- F1 [fixed] V2 says Sonnet-labelled 72-79-step chats cost 2.2-2.6. The ledger says 2.6 (Protest Tiers) and 4.11 (morning report).
- F2 [fixed] V2's "quadratic minimum near 11 steps" was not shown and conflicts with the fit's own cost-per-step minimum near 106. Dropped. What stands is that only 5 chats ran past 80 steps.
- F3 [fixed] V2's start check refuses only after a wrong chat has already paid its start. Added V1's gate when a chat is opened. The start check stays as the backstop and the measurement.
- F4 [fixed] V2 moved every clip to Sonnet. A clip made straight after a fix now stays in the fix chat (from V3).
- F5 [fixed] The size line keeps the existing gap rule: back after more than an hour on amber or red means hand over only, because a cold cache re-writes the whole history.
- F6 [named] The problem file says "42 Opus chats". The ledger has 42 step-counted chats: 32 Opus and 10 Sonnet.
- F7 [named] The biggest lever is 1,479 steps in one day, mostly rework. This proposal does not cut it; it needs its own route.
- F8 [named] Unchecked: the learning's cost (~1% of a week); whether a gate can read create_session's model field; whether get_session can read every chat. The size saving runs from about 1.2% (V1's fit) to 4-6% (V2's buckets) of a week on a 16 Nov-sized day; the learning settles it.
## Final version
**Learn (changes nothing, one Sonnet chat, ~1% of a week, unchecked):** for every Protest Tiers and Blessed chat it can open, record the model it was served (get_session), its job (fix, build, look, check, clip, sound, render, filing), its steps and its history size. Outputs:
- the % of a week spent on routine jobs run on Opus;
- the true model labels in the ledger, with the mislabelled rows corrected;
- the cost per 100 steps by length band, with the long bands filled in where the data allows.

**Change 1, model by job (one yes; only if the learning shows over 2% of a week a film on the wrong model):**
- CLAUDE.md's model lines become one job-to-model table. Fixing, building and deciding go on Opus. Checks, looks, sound to a plan, clips-only, renders, finish.py, sending and filing go on Sonnet.
- A clip made straight after a fix stays in the fix chat. The fix chat then opens the Sonnet chat for the rest.
- Enforced twice in code. (a) When a chat opens the next one, a gate compares the model asked for with the job named and refuses a mismatch. (b) `handover.py start` compares the chat's served model with the table. On a mismatch it opens the right chat and stops.
- Number to beat: under 1% of a week a film on the wrong model, read from the served models. Build: ~1-2% of a week.

**Change 2, one size rule (one yes; after Change 1, using the learned curve):**
- One line replaces "a fresh chat for every round": "A chat runs to amber or the end of its stage. It ends sooner only for a model change, a question for Sam, or red. Back after more than an hour on amber or red: hand over only."
- The handover check flags any chat that ended under 40 steps without one of those reasons.
- Amber and red change only through the route, on ledger evidence.
- Number to beat: under 15% of a film's chats under 40 steps, and Opus cost per 100 steps at or under 2.7. Build: ~0.5%.

**Named, not bundled:** cutting the steps themselves (rework rounds) is the largest lever and goes through its own proposal.

Both changes are reviewed against the next film's ledger when Sam calls it complete.
## For Sam
### Option 1: Measure first, then fix the model and give one chat-size answer
First, one cheap chat looks back over the last two films. It works out how much was wasted by running routine jobs (checks, sound, clips, renders) on the dearer Opus model, and how chat length really affects cost. Only if the waste is real do the next two steps happen, each as its own yes:
1. Routine jobs move to the cheaper Sonnet model, enforced automatically when a chat opens and again when it starts.
2. One permanent answer on chat size: run to the cost warning or the end of the stage, never shorter without a reason.

You'd notice fewer, fuller chats, routine work on Sonnet, and the size advice never changing again.
Lost: "a fresh chat for every round", and Opus doing clips-only and sound work.
Added: a look back at two films (~1% of a week), an automatic model check, one chat-size line, a flag on short chats.
### Option 2: Change it all now in one go
A fixed set of changes made straight away, with no measuring first:
- Hand over at about 100 steps.
- Raise the cost warnings to 250k and 350k.
- No chat under about 40 steps.
- One chain of chats per film at a time.
- Routine stages on Sonnet.

Quicker to switch on, but all five ride on one yes before anyone knows which ones pay. Running one chain per film would slow films that now run several in parallel.
Lost: handing over at 200k, and running a film's chains side by side.
Added: a 40-step minimum, one chain per film, higher cost warnings.
