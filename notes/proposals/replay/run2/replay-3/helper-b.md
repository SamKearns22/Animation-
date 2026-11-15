# Helper B: replay 3

## Leak
No solution stated. The frame leans: "a permanent change to how Claude works" invites a behaviour rule, and the only facts given are tool counts.

## Results
- Chats 29 and 31 ran codemap.py/page.py 0 times; hand `grep -n`/`sed -n` on film code 25 and 26 times (tool-use-29-31.md).
- Code looks were ~33% and ~27% of those chats' estimated cost (bills-29-31.md; call-weighted guesses, not metered).
- Chat 29 cost 2.57%, chat 31 2.36% of a week (ledger protest-tiers.md). The film: 51.27% spent over 32 chats against the 15% aim. The same ledger's "After the film" line says 33.55%: the record disagrees with itself.
- `story/protest-tiers-page.md` does not exist: page.py was never run on this film, though the notes-round pack says to (job-packs.md, Notes round).
- `source/protest_tiers.py` is 2,283 lines; rule 61 says split at ~1,000, and its check only warns (film-quality-rules.md 61; preflight.py gate_warnings).
- No hook counts which tools a chat ran (.claude/settings.json: costwatch, handover log, ledger auto only).
- Proposals: 2-chat first, 8-chat only after Sam pushed (problem file; Sam 19:48-19:51, sam-to-case3.md).
- Gap: nobody has tested whether `page.py find` points to the right lines on this film. Nobody has measured whether it costs less than grep. The saving cannot be sized yet.

## The real decision
How does any change (tool, rule, check, proposal) get from "written" into every chat by default, with a number that shows it worked, across a whole film? It is not about one chat or one tool. Bigger levers than grep against page: 32 chats with 230-250k-token histories, and a 2,283-line film file.

## Root cause
Both symptoms come from one cause: everything depends on a chat reading text and choosing to follow it. Nothing puts the tool in the chat's path, and nothing counts whether it ran. Nothing checks a proposal's size before Sam sees it. Evidence: the hooks list; rule 61 only warns; the page instruction sits in a pack. Each tool proves it works (kittest) but never proves it is used. "I should have proposed that first" failed because it was a promise inside one chat, and the next chat never sees it. Grep is also the default habit and looks like the cheaper single call.

## Approaches weighed
1. **Enforce at use:** a hook that catches hand grep/sed on film code and answers with `page.py find` (building the page if missing).
2. **Reframe: "built means wired and counted."** A new tool, rule or check is finished only when (a) something already on every chat's path calls it, and (b) its use is counted per chat automatically. `ledger.py auto` already reads every transcript at Stop. `handover.py end` flags a stage that skipped its tool.
3. **Learn first:** count tool use per stage across all 32 Protest Tiers chats against the packs. Replay chat 31's notes through `page.py find` and score whether it lands on the lines the chat actually edited.
4. **Reframe: less to look up.** Enforce rule 61's split as a block, not a warning, so every lookup is smaller.
5. **Wire the proposal route:** `handover.py end` refuses a handover that carries a rule or tool proposal not run through `propose.py`.

Chosen: 3, then 2, then 1 and 5 one at a time, each only if the evidence calls for it. Approach 2 is the permanent cure: it catches every future unused tool, not only these two.

## Proposal
**Learn (changes nothing):** one helper, Sonnet, reads the 32 chats' transcripts and returns two things: tool use by stage, and a `page.py find` hit rate on 10 real notes from chats 29 and 31. Cost ~2-3% (unchecked; similar to the bills helper).
**Then, one change per yes:**
- **A. Counted use** (edit `ledger.py auto` + `handover.py end`). Every ledger row gets "code tools N / hand searches M". The handover is refused while a stage's named tool shows 0 without a written reason. Number to beat: from the first chat on, every row carries the count. ~2%, Opus medium.
- **B. The hook**, only if the learn step finds page hits the edited lines in at least 8 of 10 notes. Number to beat: hand searches on film code at most 3 per chat (from 25-26), measured by A. Notes-round chat cost below 2.4%. ~1.5%.
- **C. Proposal gate.** Number to beat: no proposal reaches Sam without its helper and judge files. ~1%.
Total ~7% once, against 15% per film. Saving per film: unchecked until the learn step. If page cuts code looks by a third across ~15 code chats, roughly 3-4% per film (estimate).
**Sam would notice:** each film's ledger shows whether its tools ran. Proposals arrive already tested against his pushes. Notes-round chats should get cheaper. Every rule ends up in the repository as a check, never only in a chat's text.

## Sam test
- Q1 Expert: yes. Experts make tools the default path and measure adoption; they don't rely on promises.
- Q2 Best result: the learn step reads all 32 chats, not 2. The page's accuracy is scored before anything is enforced.
- Q3 Comprehensive: A and C are enforced by handover.py/ledger.py on every chat, not by reading. A counts whether it worked.
- Q4 Intelligent: five different approaches weighed; one cause addressed.
- Q5 Risk: each change undoes alone. B waits for proof the tool finds the right lines.
- Q6 Checked: sources named; estimates and the ledger clash marked.
- Q7 Not cheap: sized to fix every future tool, not to patch two.
- Q8 Nothing temporary: each change is permanent once yes'd, and reviewed when the film is declared complete.

## Lost / Added
Added: a count on every ledger row; a handover refusal; (if earned) a hook that answers grep with page lines; a proposal gate.
Lost: a chat can no longer hand off having silently skipped its stage's tool.

## Unchecked
Learn-step cost; per-film saving; which ledger total is right (51.27% or 33.55%); whether page.py works on Protest Tiers' files.
