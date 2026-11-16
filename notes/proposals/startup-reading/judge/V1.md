# Helper B: start-up reading

## Leak
Mild: the title and ask already name the remedy ("condense the text"). Set aside; the problem is the cost of what enters every chat before work, not the wording.

## Results
- Start-up reading is ~15% of a median Opus chat (~$0.84 of ~$5.6); the app's own 80k is ~25% (notes/cost-diagnosis.md, Job B). Which text that 15% is made of was never measured per chat: the split by source does not exist. That gap is the main finding.
- The rework of returned faults costs ~15% of a week a film (Blessed, cost-diagnosis.md): a cut rule that lets one fault back costs more than all start-up savings.
- Repo text that enters chats (checked): CLAUDE.md 2,192 words (wc); job-packs 707 words; remote branches 252 (`git branch -r`); notes/elder-swindon.md 5,965 words and protest-tiers.md 4,531, against a 4,000 cap. handover.py has no word-count check on notes (grep: none), so the cap is prose only.
- Price per 1k tokens read at start, per 32-chat film: ~0.3% of a week (problem file, derived; unchecked). So the branch listing (~2.5k, zero rules) ~0.8%; notes over cap (~2-3k extra) ~0.7%; CLAUDE.md ~1%.
- Film size disagrees in the record: protest-tiers ledger "33.55% of a week" vs protest-tiers-costs.md "~53.6% spent". Unresolved; every saving in % depends on it.
- Naming a tool in a pack failed once (page.py run 0 times, chats 29 and 31; notes/proposal-route.md line 60): text alone does not change behaviour.

## The real decision
Not "how short can the guides be" but: across a whole film's ~32 chats, which text enters each chat's history that its stage does not use, and can that be stopped by a tool rather than by rewording rules. Bigger levers than wording: printouts with no rule in them (branch listing), notes over cap (no check), and dated histories inside rules. Rewording working rules is the smallest and riskiest lever.

## Root cause
Text grows only by adding. Each fault adds a rule with its dated history (10 dated tags, 3 "replaces/was" in CLAUDE.md); notes grow by appending, and the cap has no check; the branch step was written when there were few branches and now prints 252. Nothing measures what a chat reads, so nothing flags growth. Evidence above.

## Approaches weighed
1. Hand-condense every guide and CLAUDE.md (the named frame). Large, and each rewording risks a returned fault; saving unmeasured.
2. Reframe: stop non-rule text reaching chats by tools: filtered branch check, enforced notes cap, dated histories moved to the rulebook's log. No rule wording touched.
3. Learn-first: measure, from the transcripts reachable, every chat's start-up tokens by source, then rank.
4. Turn prose rules into checks so CLAUDE.md keeps one line per enforced rule. Right long-term, but per rule and slow.
5. Fetch stage sections on demand by a tool instead of reading them up front. Failed before as text (page.py).

Chosen: 3, then 2, one change at a time, in the order the measurement ranks them; 4 later, rule by rule, through the route.

## Proposal
**Learn first (changes nothing).** One Sonnet chat reads the reachable transcripts (Protest Tiers chats 0-8 and the current film's chats, list_events) and, per chat, counts tokens that entered before the first work action, by source: CLAUDE.md, pack, named sections, film notes, branch listing, hook, handover start. It settles the 33.55 vs 53.6 figure. Output: a ranked table and, per source, the number a change must beat. Cost ~1.5% of a week (unchecked estimate).

**Then one change at a time, each its own yes, likely order:**
- C1 Branch check by tool: handover.py start prints only branches holding commits not on the main line (expected under ~10 lines). The CLAUDE.md line points to it; the merge-newer-work rule is unchanged. Enforced: it runs in the start step every chat already does. Must beat: listing ≤300 tokens (from ~2.5k) and zero missed merges, checked by comparing with the full list at each film end.
- C2 Notes cap enforced: handover.py end refuses a handover while the film's notes are over 4,000 words, naming finished sections to move to notes/archive/. Must beat: every handover under 4,000 words; no note Sam gave lost (archive keeps all).
- C3 CLAUDE.md histories out: dated tags and "replaces/was" moved to the rulebook's last table; rule sentences kept word for word. Enforced by a script listing every rule sentence before and after: any missing sentence refuses the change. Must beat: zero rule sentences lost, size down by the measured history share.

Each is reviewed at film end: Sam's notes and repeated faults not above the last two films (Protest Tiers, Blessed), and start-up tokens per chat against the learn-step table. Cost of C1-C3 ~0.5-0.7% of a week each, once; saving ~2-3% of a week per film (derived, unchecked until the learn step).

Sam would notice: nothing in the films; one learn-step table, then three separate questions.

## Sam test
- Q1 Expert: measure context by source before cutting, remove non-rule text by tools; yes.
- Q2 Best result: all reachable chats of two films, not one chat.
- Q3 Comprehensive: root cause is growth with no check; each change is enforced by a refusal, not by reading.
- Q4 Most intelligent: five approaches weighed; rule wording left alone.
- Q5 Risk: no rule removed; each change undone alone; nothing asked on trust before the measurement.
- Q6 Checked: sources named; money figures and the film total marked unchecked.
- Q7 Not cheap: sized to the measured result; the cheap trap (cutting rule words) refused.
- Q8 Nothing temporary: each change permanent, reviewed when Sam declares the film complete.

## Lost / Added
Lost: the full branch list in every chat; dated histories in CLAUDE.md (kept in the rulebook). Added: one learn chat; a filtered branch check; a notes-cap refusal; a rule-sentence guard.

## Unchecked
The ~0.3%-per-1k price; the 15% start-up share by source; the film total (33.55 vs 53.6%); whether every chat actually runs the branch listing; savings figures.
