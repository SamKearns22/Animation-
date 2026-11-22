# Helper A: which model works Sam's notes rounds

## Leak
The problem file leans to "text, timing and sound rounds go to Sonnet". Set aside.

## Results
- Rounds run (notes/ledger/milburn.json, $ at 366 USD a week): Opus chat 9 $9.16 (2.5%, 98 steps), chat 10 $7.94 (2.17%, 123), chat 11 $6.68 (1.82%, 122). Chat 13 $5.51 (1.5%, 117) is "sonnet" in the ledger but "Opus medium" in notes/archive/milburn.md line 10. Chat 18 (Sonnet) $4.65 (1.27%), steps unrecorded. The review's "2.3%" matches neither (unchecked).
- Per step: Opus $0.055-0.093; Sonnet chat 12 $0.029; chat 13 $0.047. Long "Sonnet" chats are not cheap: 72-79 steps cost 2.6-4.1% (notes/proposals/chat-size-and-model.md).
- "No repeats" is false on the record. Chat 13 judged Milburn's name card "already clear" by eye, and Sam gave the note again in chat 18 (milburn.md line 15). Chat 18's own fixes drew 2 more notes on the ambush clip (its grin for the goth, Swindon's leftover bob). Opus repeated too: note 3 (repeat of note 1), note 5 (the reverse staged three times).
- Confound: Opus got looks and re-staging; Sonnet got mostly text. One film cannot compare the models.
- Gap: the ledger's notes and repeated columns are 0 on every film, and the served model is in doubt (chat 13; chat 11 was planned Sonnet and ran Opus, milburn-handovers.md line 103). The record cannot yet say which model repeats more.

## The real decision
How a whole film's notes rounds get the fewest repeats for their cost. One repeat costs a round (1.3-2.5%). The model swap saves at most about 1-1.5% a film, so one extra repeat wipes it out. The bigger lever, fewer notes reaching Sam, is a separate decision.

## Root cause
1. The rule picks a model by stage, not by step. A round mixes judgement (what Sam means, why the check missed it, the new pose) with many carrying-out steps (edits, renders, clips, finish.py). Either Opus pays for the carrying-out, or Sonnet makes the judgement calls.
2. Notes land in the chat that sent the animatic, which is Sonnet by rule. Nothing checks the model when a round starts, so chat 18 broke the rule unnoticed.
3. No record ties notes and repeats to the served model.

## Approaches weighed
1. Split by note kind (text and sound to Sonnet). Rounds are mixed (chat 18's nine included a retreat move and a card placement), and the case rests on one confounded film.
2. Reframe, split by step. Opus medium decides the round and writes each fix exactly, with its phone-size look-check. Sonnet carries it out, renders, clips and sends. This extends CLAUDE.md's existing seam ("an Opus fix ends by opening the Sonnet chat").
3. Learn first: measure notes, repeats, cost and served model per round over three films.
4. Fewer notes reach Sam (better checks before the animatic). Biggest lever; its own route.

Chosen: 3, then 2 only if its numbers win.

## Proposal
**Learn (changes nothing; Sonnet, about 1% of a week).** For every notes round in Milburn, Blessed and Protest Tiers, read the chat's own record (events, served model). Per chat, record steps, cost, each note (its kind, whether it returned, and whose fix failed) and the cost share of judgement versus carrying-out steps.

**Change, one yes, only if (a) carrying-out is over half of an Opus round's cost and (b) Sonnet's carried-out fixes repeat no more than Opus's.** The round splits at a written plan. Opus medium ends when every note has its exact fix and look-check. Sonnet does only what is written; anything unwritten goes back to Opus, never guessed. Enforced by the handover check. It reads the served model from the chat itself, and refuses a Sonnet notes round with no Opus plan, or a Sonnet change to a look or pose the plan does not name.

**Numbers to beat** (end-of-film review): repeats per note at or below the Opus-only rate measured; cost per note at least 25% below Milburn's Opus rounds.

Cost: learning about 1%, the check about 0.5% once; the saving is about 1-1.5% a film (unchecked), against the 15% aim. Sam would notice one plan line per note before clips, and slightly cheaper rounds.

## Sam test
Q1: An expert routes by step and measures the served model first.
Q2: Three films, every round, from the chats' own records.
Q3: Enforced by the handover check; judged on repeats.
Q4: Four different approaches; the biggest lever is named separately.
Q5: The learning changes nothing; one check, removable alone.
Q6: Sources named; the review figure and chat 13 are marked.
Q7: Opus keeps all judgement; no cheap split by note kind.
Q8: A permanent rule or none, reviewed at the film's end.

## Lost / Added
Lost: nothing until the learning; after it, Opus stops running renders and clips.
Added: one learning chat, one check, a written plan per round.

## Unchecked
- The review's 2.3%.
- Chat 13's model.
- Chat 18's steps.
- Sonnet's true price per step.
- Whether lesson 5 (counting notes) is built elsewhere.
