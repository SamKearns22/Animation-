# Helper B: routine work keeps running on Opus

## Leak
No solution stated. It does carry the earlier chat's diagnosis (why-model-switch-failed.md) as fact; I checked it and do not assume it is the whole cause.

## Results
- Protest Tiers spent 101.29% of a week against a 63.51% estimate; round 2 alone went from 53.21% to 100.78% against 0.865% planned (notes/ledger/protest-tiers.json, stages).
- 16 Nov: 24 chats, 39.3%. Opus 19 chats, 35.18%, 1,305 steps; Sonnet 5 chats, 4.12% (same file, summed).
- Opus cost on 16 Nov by kind (same file, weighted): renders 0.88%, pictures 1.07%, film-file search 6.65%, tool search 3.22%, "other" 23.12%. Measured render steps are under 2% of a week. How much of "other" was routine (splicing, checks, sound, sending) is not in the record: **a gap**.
- The stated model and the model that actually ran disagree. The app record (notes/ledger/app-costs.tsv) shows chat 19, "animatic 1 (Sonnet)", **ran on Opus**, and chats 27, 30 and 31, titled "Opus medium", **ran on Sonnet**. Nothing compares the two.
- Sonnet is not cheap when long: chats 27, 30 and 31 cost 2.18–2.36% each at 211–229k history (app-costs.tsv). Price per step is roughly half of Opus (.claude/hooks/costwatch.py PRICE).
- The cost watch hook already reads each chat's real model from its own record at every step (costwatch.py, `st["model"]`). handover.py `model` reads only the words of the Next line (source/handover.py lines 312–332).
- What Sam saw: none of this reached him as a fault (no notes logged against it, ledger "notes" 0); he paid for it in budget.

## The real decision
The question is not "make the Next line say Sonnet". It is: does every chat in a film run on the model its job needs, checked against the model it **actually** runs on, however it was opened (chain, Sam's phone, a prompt)? Larger levers sit beside it: round 2 overran by about 47% of a week, and Opus search alone cost about 9.9% on one day. Model choice can save a few % per film, but by itself it cannot bring a film to 15%.

## Root cause
1. **The check reads words, not facts.** It reads what the notes say the next chat should be and guesses "routine" from a word list. "splice" was missing, so it never fired. Chats opened from Sam's phone never pass through it. And chat 19 shows a chat labelled Sonnet still ran on Opus.
2. **Stages are free prose.** Any Next line can fold routine steps into a fix chat ("clips … splice into the animatic"), so no split is ever forced.
3. **The rule contradicts itself.** CLAUDE.md "Models by stage" puts clips and sound on Opus medium and the animatic on Sonnet. Splicing clips is both, so France chats 7 and 8 followed the rule.

## Approaches weighed
1. **Check the real model at the source:** the hook that already knows the live model compares it with the job's model from a fixed list of stages, and stops the chat before work on a mismatch. This reframes the problem from "what the notes say" to "what is running".
2. **Make the routine tail one command:** splice, finish and send as a single step. That costs a few steps whatever the model, needs no extra chat and no history reload.
3. **A Sonnet helper inside the Opus chat** for routine steps. It avoids a new chat, but whether helpers here can take a model choice is unchecked.
4. **Learn first:** measure from the 16 Nov transcripts which steps were routine and what they cost, and reconcile the intended and served model for all 61 chats.

I choose 4 first, then 1, then 2 only if 4 shows the routine tail is large. Approach 1 fixes the cause, because it does not rely on anyone writing the right words.

## Proposal
- **Learn (changes nothing), Sonnet, about 0.5–1% of a week:** read the ledger's session list and step records for Protest Tiers. For each chat, find the model it should have used (from its stage) and the one it served, and the cost of its routine steps. Output: the mismatch count and the routine share of Opus spend. If the transcripts cannot be read, say so and do not go on to change 2.
- **Change 1 (alone):** a closed list of stage names (plan, build, fix, clips, sound, animatic, final, filing), each with one model. The handover names one stage from that list, not prose. The cost watch hook compares the live model with that stage's model, and a mismatch stops work with a message to open the right chat. The step-up rule (switching needs a fresh chat) still holds. Enforced by the hook, which runs every step whoever opened the chat. Number to beat: 0 mismatched chats in the next film, against 4 of 24 app-recorded chats on 15 Nov. Build cost about 1.5–2% of a week (Opus medium), once.
- **Change 2, only after the learn step and its own yes:** settle whether clips and sound are Sonnet or Opus work. That is a rule change for Sam, with the measured routine share as its evidence and the number of notes on Sonnet-made clips as its number to beat.
- What Sam would notice: an occasional "wrong model, opening the right chat" line, and a smaller Opus share on the ledger.

## Sam test
- Q1 Expert: it enforces at runtime what is actually running; an expert would not trust a label.
- Q2 Best result: it uses the whole film's 61 chats, not one day's.
- Q3 Comprehensive: a hook, not a reading habit; it covers phone-opened chats; success is measured as a mismatch count.
- Q4 Intelligent: four different approaches weighed; the root fix is chosen and the routine tail is sized by data.
- Q5 Risk: a false stop only costs a reopened chat, and the hook line can be removed alone.
- Q6 Checked: sources are named; the gaps are marked below.
- Q7 Not cheap: it fixes the cause rather than adding another word to the list.
- Q8 Nothing temporary: a permanent check, reviewed at the film's end.

## Lost / Added
Lost: free-prose stage names in the Next line. Added: one stage list, one hook check, one learn step.

## Unchecked
Routine share of the "other" bucket; whether the app's model field is the configured or the served model; whether old transcripts can be read; whether helpers can run on Sonnet; Sonnet quality on clips and sound.
