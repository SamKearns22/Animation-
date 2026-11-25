## Leak
None. The file frames the question as the article's five points, which narrows it (see The real decision).

## Results
- **Every measured film overran 15%:** Remakes 24.07%, Milburn 32.85%, Protest-tiers 34.48%, Brexit 41.97%, Blessed 48.63%, Grand Theft Autism 108.34%; 17 to 58 chats a film (notes/ledger/FILM.md headers).
- **CLAUDE.md costs about 1.3% of a week a film** (arithmetic re-done: 6,800 tokens x $8/M once + 78 re-reads x $0.18/M = $0.15 a chat, 0.04%; x ~32 chats). It grew from ~5k to ~6.8k tokens in 9 days (job-e-measurements s1; problem file). Helper loads: unchecked.
- **Shortened (compacted) chats: none in 85 records;** largest 414k of a 1M limit, 2 Opus chats over 300k (app-costs.tsv). Loss so far: zero.
- **Long chats:** already governed (cost watch, chat-size rule). Blessed chat 5, bundled stages and a model switch: $27.73, 9.6% (cost-diagnosis Job B).
- **Biggest measured cost: rework of faults that came back, ~15% of a week on Blessed** (cost-diagnosis Job B); GTA had 4 repeated notes, Brexit 3 (ledgers).
- **Work history (code reads, printouts, pictures) ~25% of a median chat;** printouts alone are not split out (cost-diagnosis). Gap.
- **Helper models:** critic Sonnet, namer Opus (.claude/agents), proposal helpers Opus by design (propose.py). Sonnet ~2x cheaper a word (cost-diagnosis). Namer on Sonnet: unchecked.

## The real decision
Not "do we follow the article" but "which of its points moves a whole film toward 15%, and by how much". All five together touch perhaps 2-4% of a film; the overrun is 9 to 93 points. Bigger levers lie outside it: repeated faults (~15%), bundled stages (~10%). So Sam gets a ranking, and only a measured saving earns a change.

## Root cause
The article targets long, drifting chats; this project already curbed those (cost watch, packs, reading layers, handover). Left uncontrolled: (a) printout volume, never measured by command, and (b) CLAUDE.md growth, with no ceiling. Compaction protection and cheaper helpers answer risks the record does not show.

## Approaches weighed
1. **Adopt the article wholesale:** move CLAUDE.md sections to on-demand skills, add compaction instructions, a command list, cheaper helpers. Under 1% a film; binding rules moved out load only if a chat chooses: a quality risk.
2. **Reframe:** answer the article in one ranked table and put the effort into repeated-fault rework, the largest measured cost. Right ranking; another route's work.
3. **Learn first, then single enforced changes:** measure the two real gaps, change only what clears a threshold, inside the tools, not as prose.
Chosen: 3, with 2's ranking as the reply to Sam.

## Proposal
**Learn (changes nothing), Sonnet, about 1-1.5% of a week:** from the chat records of Milburn and Protest-tiers (list_events), measure (a) tokens each tool printout added, grouped by command, top ten; (b) cost per finished stage against chat length; (c) helper runs per film and their cost; (d) name tests (nametest.py) re-run on Sonnet against the saved Opus answers; (e) any compaction event.

**Then, one yes each, only if its number clears:**
- **C1, quiet printouts by default** in the commands that top (a), built into the tools, not a list to read. Only if those commands cost at least 1% of a week a film. Beat: their printout tokens halved at the next film, same measure. About 0.5%.
- **C2, CLAUDE.md ceiling:** the handover check refuses a handover if CLAUDE.md passes 16,023 characters; room is made by moving text word for word to the rulebook or a pack (sentences.py). Its saved example: the 5k to 6.8k growth. Beat: never above the ceiling. About 0.3%.
- **C3, namer on Sonnet** only if (d) matches Opus on every saved test. Critic and proposal helpers stay as they are.
- **No compaction section:** none has happened; (e) and the ledger keep watching, and the handover already holds the locked shots and open notes.

**Sam would notice:** one plain table (done / small gap / not worth it) per point, then at most three Y/N questions once measured. Films look the same.

## Sam test
- Q1 Expert: measures where tokens go before trimming.
- Q2 Best result: two whole films' chats, not one chat; the film is the unit.
- Q3 Comprehensive: changes live in tools and checks, not prose; each has a number.
- Q4 Most intelligent: three approaches weighed; bigger levers named.
- Q5 Risk: each change undoes alone.
- Q6 Checked: sources named.
- Q7 Not cheap: quality roles keep Opus.
- Q8 Nothing temporary: each change is permanent or not made; reviewed at film end.

## Lost / Added
Lost: nothing until a yes. Added: one measuring job (~1-1.5%); up to three enforced changes.

## Unchecked
Helper runs that load CLAUDE.md; printout tokens by command; namer quality on Sonnet; whether 32 chats a film is still typical.
