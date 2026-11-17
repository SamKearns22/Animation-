# Helper A: routine work keeps running on Opus

## Leak
None in the problem file itself. It points to `why-model-switch-failed.md`, which only diagnoses. I did not read this proposal's chat.md.

## Results
- The model rule has never held on its own. Before 15 Nov there was no check, and "the model-by-stage rule never fired; Sam switched chats 4 and 5 to Sonnet himself" (notes/cost-diagnosis.md:112). The 15 Nov check fired zero times on 16 Nov (problem file; why-model-switch-failed.md).
- 16 Nov, Protest Tiers: 24 chats cost 39.3% of a week. 19 were Opus: 35.18%, 1,305 steps. In those Opus chats, renders cost 0.88% and looking at pictures 1.07% (my sum of the ledger's per-kind shares, notes/ledger/protest-tiers.json). That is the visible routine floor. The routine steps around them (splicing, finish.py, filing) are not split out: **gap**.
- Sonnet costs about 0.6x Opus per token (.claude/hooks/costwatch.py PRICE). Moving only the visible 1.95% saves about 0.8% a day. Whole routine chats on Opus (France 7 look/check/clip, France 8 sound) add to that by an unchecked amount.
- The plan said Sonnet, but the action stayed on Opus. On 16 Nov the Next line gave the Germany fixes to Opus and the front-half animatic (`--span 0 14.5`, finish.py) to Sonnet (archive handovers line 348). The splice still happened in the Opus chat (why-model-switch-failed.md 1).
- The ledger's model labels and the chat titles disagree on 15 Nov. "Chat 19: animatic 1 (Sonnet)" is logged as Opus. Chats 27, 30 and 31, titled "(Opus medium)", are logged as Sonnet. So neither titles nor notes are a reliable record of the served model: **gap**.
- Switching model inside a chat re-pays its history: $5.80, 2% (cost-diagnosis.md:75). The fix is always a new chat, never a switch.
- No fault reached Sam because of the model. The cost is money only. Sonnet's quality on clips and sound is unchecked.

## The real decision
Sam has already said Y to routine work on Sonnet. The decision is how to tie **the model a chat is actually served to the actions it actually runs**, across every chat of a film, including chains opened from the phone. The bigger lever is named but not bundled: Opus rework steps (1,305 steps in a day) cost far more than the routine share. That needs its own route.

## Root cause
The model is chosen in words (a Next line, a chat prompt) and checked in words, by a word list on one line of the notes. Nothing compares the served model with what the chat runs. So:
1. Any new wording ("splice", "sound", a chain's own prompt) slips past.
2. The rule's own wording put clips and sound on Opus.
3. Splitting off a Sonnet chat for a few steps looks wasteful, so a fix chat keeps the routine tail. The last proposal even endorsed this (chat-size-and-model.md F4).

Every earlier fix (the rule, then the word check) was more words, which is why each one failed.

## Approaches weighed
1. **Widen the word check** (add "splice" and "sound", and reword CLAUDE.md). This is the same family that failed twice, and it still misses chains' own prompts.
2. **Reframe: guard the action, not the plan.** A hook (an automatic step the app runs before every command) already knows the served model (costwatch reads it from the chat's record). On Opus, it refuses routine commands (a whole-film `final` render, finish.py, splicing into the drafts animatic, filing) and replies: "open the Sonnet chat with create_session". A second hook on create_session refuses a model that doesn't match the job named in the prompt. Both run in every chat that has the repository, including phone-opened chains.
3. **Make the Sonnet tail cheap.** Build one command that splices, runs finish.py and saves the animatic, so a Sonnet chat finishes in about 8 steps (about 0.21%, ledger). Then nobody is tempted to keep the work on Opus.
4. **Learn first.** Measure each Protest Tiers chat's served model, its routine steps and their cost, and correct the ledger labels.

Chosen: 4, then 2. Approach 3 waits: it is needed only if the learning shows split-off Sonnet chats costing more than they save.

## Proposal
**Learn (changes nothing; Sonnet, about 0.5% of a week):** for every 16 Nov Protest Tiers chat, record the served model (get_session), steps by job (fix, build, look, check, clip, splice, sound, render, finish.py, filing) and the cost of each. Correct the ledger's model labels. Outputs: the % of a week spent on routine work on Opus, and which commands carry it. That list becomes the gate's list.

**Change 1, the action gate (one yes, after the learning):**
- It runs as two hooks in `.claude/settings.json` (Bash, and create_session), on the served model, not on any text a chat wrote. It applies in every chat, and no chat can choose to skip it.
- Clips with `--span` stay allowed on Opus, so a fix can be checked in its own chat. The splice into the animatic does not.
- Every refusal is logged, so the end-of-film review sees each one.
- Number to beat: routine work on Opus under 0.5% of a week per film, measured from the served model in the hook log and the ledger, against the figure the learning finds.
- Build: Opus medium, about 1% of a week.
- This replaces `model_faults`' word list. That check is removed only once the gate has caught everything the list caught.

**Change 2 (only if the learning shows split chats costing more than they save): the one-command Sonnet tail.** It gets its own evidence and its own yes.

Total: about 1.5% of a week, once, against 15% per film. It saves about 0.8% or more a day on a 16 Nov-sized day.

What Sam would notice: animatics always arrive from a Sonnet chat, and the model never needs his correction again.

## Sam test
- Q1: An expert enforces at the point of action, using the system's own truth (the served model), not prose.
- Q2: Its scope is every chat of the film. The evidence is the ledger and served models, not one chat's notes.
- Q3: The root cause is found (words checked by words). It is enforced by hooks with no reading. The refusal log shows whether it worked.
- Q4: Four different approaches were weighed. The gate is the only one that does not rely on wording.
- Q5: Each hook is undone alone. A wrongly refused command prints why and names the chat to open.
- Q6: Sources are named. The gaps are marked.
- Q7: Sized to the real waste. The gate covers phone chains, which the cheap word fix does not.
- Q8: Permanent, and reviewed against the film's results at completion.

## Lost / Added
Lost: Opus chats making the animatic, finish.py or filing. The word-list model check goes once the gate replaces it.
Added: a look back at one day (about 0.5%), two automatic gates with a refusal log, and corrected ledger model labels.

## Unchecked
- The routine share of the 16 Nov Opus steps beyond renders and pictures.
- Sonnet's quality on clips, sound and looks.
- That a hook can match create_session's tool name and read its model field.
- Why the 15 Nov ledger labels and titles disagree.
