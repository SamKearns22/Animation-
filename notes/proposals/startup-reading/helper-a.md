# Helper A: start-up reading

## Leak
Small: the title and the ask ("condense the text") already name the remedy, and the Facts point at the branch listing
and CLAUDE.md's dated tags. Weighed below as one approach, not taken as given.

## Results
- Its token figures are about 40% too low. The problem file counts 4 characters a token, but this project's text is
  measured at **2.35 characters a token** (notes/job-e-measurements.md §1). Recounted: CLAUDE.md 12,857 chars = **~5.5k
  tokens**; branch listing 9,171 chars = **~3.9k**; job-packs 4,558 = **~1.9k**; notes/elder-swindon.md 31,452 =
  **~13.4k**; notes/protest-tiers.md 25,037 = **~10.7k** (counted here with wc).
- At ~$0.023 per 1k start-up tokens per Opus chat (the problem file's own sum: write plus 78 re-reads), about 0.3% of
  a week per 1k tokens per 32-chat film: CLAUDE.md ~1.6%, branch listing ~1.2%, film notes **~3-4%** (when read
  whole), Build pack (~12.7k tokens) ~1.4% across ~12 build chats. Derived, unchecked against a chat.
- **The film notes are the biggest piece the project controls, and they already break a rule:** CLAUDE.md caps them at
  4,000 words; Elder Swindon is 5,965 and Protest Tiers 4,531 (wc). Nothing enforces the cap.
- A typical round reads **40-55k tokens** of guides and notes on top of the app's 80k (job-e-measurements §1). The app's
  80k cannot be changed by this project.
- Protest Tiers: 33 chats, 53.6% of a week; per-chat cost did not fall after the 13 Nov fixes
  (notes/proposals/learn/protest-tiers-costs.md).
- **Gap:** no record says what each chat actually reads at start-up, item by item. The "15%" is one fitted split
  (notes/cost-diagnosis.md Job B); whether chats read packs only, or more, is unmeasured. Chats 9-32 are on an
  account this repo's chats cannot open.

## The real decision
Not "how short can CLAUDE.md be" but: which tokens enter every chat of a film before work, who chooses them (the chat
or a tool), and what stops them growing back. Bigger levers than CLAUDE.md wording: the film notes (2x CLAUDE.md, over
their cap) and whether reading is picked by a tool or by the chat's judgment.

## Root cause
Text grows by accretion: each fault adds a rule, and dated histories ("replaces 14 Nov", "was 8 in a row") stay
inline. Only one size limit exists (notes, 4,000 words), and it is written, not checked, so both recent films broke it.
What a chat reads is left to it, following prose (packs, "list every branch"); the branch step predates the hook's
own main-line check (setup.sh, audit A14, 2 Nov) and prints all 252 branches when only those with newer work matter.
The same "named in a pack but not done" failure is on record (page.py run 0 times, chats 29 and 31).

## Approaches weighed
1. **Rewrite the prose shorter** (the problem's frame). One-off, saves ~1-2%, risks dropping the wording a fault
   needs, and regrows.
2. **Reframe: a tool does the start-up reading.** `handover.py start` prints the stage's pack sections, the notes'
   open part only and branches with newer work; size limits are checked at handover. Reading becomes fixed, small and
   measurable, not chosen.
3. **Layer by use:** move rarely used text (My accounts, dated histories, "Came from") out of always-loaded files to
   the pack or archive where it bites. Nothing deleted.
4. **Learn first:** measure each start-up item's tokens in the readable chats of the last two films, rank by tokens x
   chats, then change in that order.

Chosen: 4, then 2 and 3 as separate changes in measured order. 1 only where a measured item stays big.

## Proposal
**Learn (changes nothing):** one Sonnet chat reads the start of every readable chat of Elder Swindon and Protest Tiers
(list_events) and records, per chat, each start-up item and its tokens, and the history size when work begins.
Output: a ranked table. Cost ~1-1.5% of a week.

**Then one change at a time, each its own yes, in the table's order (expected):**
1. **Notes cap enforced:** `handover.py end` refuses a handover while the notes exceed 4,000 words, moving finished
   items to the archive. Beat: notes under 9.6k tokens in every chat of the next film.
2. **Branch step by tool:** the start-up hook prints only branches with work newer than the main line; CLAUDE.md's
   line points to it. Beat: under 200 tokens, with no missed newer work.
3. **CLAUDE.md layered:** dated histories to `notes/archive/`; rare sections moved to the pack that uses them; a
   kittest checks every rule still appears in exactly one place. Beat: ~5.5k to under 3.5k tokens, no rule lost.
4. **Pack reading printed by `handover.py start`** (sections only). Beat: start-up tokens per chat down by a third
   from the learned baseline.

Each change: about 0.5-1% of a week to build and test. Every change is held to two numbers at the film's end review:
start-up tokens per chat (from the chats' own history sizes), and Sam's notes plus repeat faults, which must not rise
against the last two films.

Sam would notice: nothing in the films; each yes comes with its own number, and chats cost a little less.

## Sam test
- Q1: Yes; an expert measures first, then makes reading fixed by tools and size-checked, rather than editing prose.
- Q2: Scope is both last films, all readable chats, and the gap is named.
- Q3: Root cause found (unchecked growth, reading by choice); enforced by checks and tools, not by chats choosing.
- Q4: Four different approaches weighed; the reframe chosen after measurement.
- Q5: Learning changes nothing; each change is single and undoable; a kittest guards against rule loss.
- Q6: Sources named; derived money marked unchecked.
- Q7: Sized by the result (the largest measured items, enforced), not a prose trim.
- Q8: Each change is permanent and reviewed at the film's end; no trials.

## Lost / Added
Lost: none of the rules; dated histories leave CLAUDE.md (kept in the archive). Added: a notes-size check, a filtered
branch printout, a rule-placement kittest, a reading printout. Each comes as its own yes.

## Unchecked
Money per item (derived); what chats actually read at start-up; savings figures; whether chats 9-32 followed packs.
