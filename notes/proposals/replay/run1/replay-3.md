# Proposal: stop half-effort fixes and tools that are built and then not used

Status: open (replay case 3)

## Problem
Sam (his messages are in the record): the first proposals he gets are sized to what is cheap, not to what gives the
best result, and better ones come only when he pushes. Tools built to cut cost were then not used. Saying "I should
have proposed that first" does not stop it happening again. Fixes to the project need to deliver huge results.
Decide what permanent change to how Claude works stops this, for good.

## Facts
- Chats 29 and 31 ran the code-finding tools (codemap.py, page.py) 0 times, and searched film code by hand (grep -n
  or sed -n) 25 and 26 times (record: tool-use file).
- In this chat Claude first proposed a 2-chat measurement, then (after Sam asked) an 8-chat one; it also told Sam the
  tools "weren't used" before it had checked (the check later confirmed it).
- The rulebook is guides/film-quality-rules.md; CLAUDE.md holds the rules about working with Sam, including
  "Rules are permanent" and "Back-end proposals get a plain explanation".
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case3.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
CLAUDE.md
guides/film-quality-rules.md
guides/job-packs.md
guides/kit-catalogue.md
source/handover.py
.claude/settings.json

## Verdict (the judge, word for word)
<!-- verdict-hash: 8f4cae44a69e6e88 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V1 (helper B). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes: mild. The Facts point at CLAUDE.md's "Rules are permanent" and "Back-end proposals" sections, which hints that the answer is a written rule in CLAUDE.md (V3 took exactly that path). No mechanism is given away.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 5 | 4 | 4 | 3 | 4 | 20 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 2 | 2 | 3 | 4 | 5 | 16 |
## Sam test
Q1: Yes. An agent-workflow expert enforces in the harness (hooks that act at the moment of the action) and measures adoption from transcripts. They do not add more wording, which is what has already failed (the Notes round pack already says "page.py, never whole film files").
Q2: The evidence is every call of two whole chats (tool-use and bills files), the live settings.json wiring and the rulebook's rule 61 check. The counters then cover every future chat, and the end-of-film review covers the whole film.
Q3: Root cause, checked: rule 61's only check is a warning about files, not behaviour, and no PreToolUse hook exists. propose.py's Stop hook is written but not wired (the Stop list holds only ledger.py). Paper compliance through the `# need` escape is closed: each use is listed at handover, and more than 3 in a chat is a handover fault that must be answered.
Q4: Four approaches were weighed: wording, a judge route alone, always using Opus, and enforce-plus-measure. Wording and the route alone already exist and failed. Chat 29 was Opus and still searched by hand 25 times.
Q5: A hook could refuse real work or stall an unattended chat. Each refusal hands back the answer, so the chat carries on, and it never blocks twice. One settings.json line undoes it. Before Sam's Y, it is replayed on chats 29 and 31 so he sees it work, not a promise.
Q6: Facts are checked with sources. The page file story/protest_tiers-page.md is absent, rule 61's check is a warning, settings.json has no PreToolUse hook, and the ledger shows 2.57% and 2.36%. Chat 31's model and the per-round saving are marked unchecked.
Q7: It is sized to make every change land in every chat, not to patch one tool. Its cost (about 3% of a week, once) is stated, and it is weighed against hand looks costing ~27-33% of two chats.
Q8: It is a permanent rulebook rule with its check, nothing on trial. It is reviewed at film end by `propose.py review`.
## Pick
V1
## Why
V1 is the only version that closes both halves of the problem with a mechanism. The code hook refuses every hand search, not just the first, so the count can actually fall from 25 to 3. The proposal route refuses any proposal without an "Enforced by" line and a "Measure" line. A start-up check catches any change marked enforced that is not wired, which is exactly how propose.py's Stop hook slipped. V2 shares the root cause and is well checked, but it refuses only the first hand search, so a chat could still make 24 more. Its target of at most 5 is not enforced. V3 is a written rule in CLAUDE.md, the very thing that failed. It has no root cause and nothing that makes it happen.
From V2: build the page on the first hand search if it is missing; frame the rule as "built means wired" plus a replay test; count proposals replaced after a push from the Stop hook as well as at handover. From V3: plain wording that the first proposal is the full-result version and any smaller one is labelled the lesser, put into the rule text.
## Faults in the pick
- F1 [fixed] V1 named the page story/protest-tiers-page.md. The film is protest_tiers, so the page is story/protest_tiers-page.md (page.py line 58; NAME in protest_tiers.py).
- F2 [fixed] The `# need` escape let a chat comply on paper. Each use is now listed at handover, and more than 3 in a chat is a fault to answer.
- F3 [fixed] V1 did not say where the rule lives. It is now rulebook rule 90 with its check, next to rule 61 (the closest one, whose warning becomes a fault for new files).
- F4 [fixed] V1 did not build the page when it was missing. Taken from V2.
- F5 [named] A refusing hook in an unattended chat could cost turns. Each refusal is one small turn carrying the answer. It is undone by one settings line.
- F6 [named] Wiring the Stop hook may block a routine message that mentions "tool" or "check". It never blocks twice and logs to notes/proposals/unrouted.md.
- F7 [named] "Full-result first" cannot be forced in a chat's head. It is enforced by the route's refusal and measured by the pushes counter (baseline 5 in one chat, target 0).
- F8 [named] Unchecked: chat 31's model (the ledger says sonnet, the title says Opus) and the real saving per round (27-33% is a call-count estimate).
## Final version
**Rule 90, "Built means wired, measured, reviewed"** (rulebook, beside rule 61; Sam, 15 Nov). A rule, tool or check counts as done only when:
- (a) **Wired:** it runs where no chat chooses (a settings.json hook, or a step in handover.py, preflight or finish).
- (b) **Measured:** it has a number to beat, counted from the transcripts and printed by `handover.py end` in every chat.
- (c) **Replayed:** a real past case is run through it before Sam's Y.
- (d) **Reviewed:** it is checked at film end by `propose.py review`.

Every proposal opens with the version sized to the result it must deliver. A smaller one appears only as a labelled "Lost:" line. Any claim about use cites a count.

**Checks:**
- `propose.py record` refuses a proposal without an "Enforced by: FILE, point" line and a "Measure: baseline → target" line.
- A session-start check fails if anything the kit catalogue marks enforced is missing from settings.json.

**Applied now:**
1. **Code reading.** A PreToolUse hook on Bash and Read refuses a grep or sed across a film or engine file, or a whole-file Read of one.
   - On the first such call it builds the page if it is missing (story/FILM-page.md), and every refusal returns the `page.py FILM find` answer for the same words.
   - Reads of 80 lines or fewer pass. A `# need: reason` suffix passes, and each use is listed at handover. More than 3 in a chat is a handover fault.
   - `handover.py start` builds the page. Rule 61's warning becomes a fault for new films.
   - Number to beat: hand searches per chat, from 25 and 26 down to 3 or fewer, with at least 1 page lookup in every chat that touches film code.
2. **Proposals.** Wire propose.py's Stop hook. Count proposals marked "replaced" after a push, at handover and from the hook. Baseline 5 pushes in one chat; target 0.
3. **Replay** both hooks on chats 29 and 31 and show the counts before Sam's Y.

**Cost:** one Opus high tool chat, about 2.5-3% of a week, once (chats 29 and 31 were 2.57% and 2.36%). Hooks cost nothing unless they refuse; a refusal is one small turn. Against that, hand looks took ~27-33% of those chats' estimated cost.

**Sam notices:** a handover line like "Code looked up by hand: 2 (target 3)". Proposals arrive full-sized first, with what enforces them and the number they must beat.

**Lost:** free grep and whole-file reads of film code (allowed with a stated reason, listed).
**Added:** rule 90 and its check, two wired hooks, a start-up wiring check, two required proposal lines, one handover line.
## For Sam
### Option 1: Nothing counts as done until it is switched on and measured
A new rule: any tool or rule I build only counts once the system runs it for me, every chat, without me choosing to. Each chat's handover then shows a number proving it was used.
Applied now, if I search the film's code by hand, the system stops me and hands me the answer from the code-finding page instead. Any proposal I bring you must say what makes it happen and what number it has to beat, and the biggest-result version comes first.
You'd notice: proposals arrive full-sized without you pushing, the handover shows "looked up by hand: 2 (target 3)", and cheaper rounds. Building it costs about 3% of a week, once. I'd show it working on two past chats before you say yes.
Lost: chats can no longer freely read film code by hand (still allowed with a stated reason, which you'll see listed).
Added: one rulebook rule with its check, two automatic stops, one start-up check, one handover line.
### Option 2: A gentler version that stops only the first slip
The same idea, but the system stops only the first hand search in each chat. After that it just counts. Proposals still go through the judge before reaching you, and the handover shows the count.
It's less likely to get in the way, but a chat could still do most of its searching by hand, as chats 29 and 31 did (25 and 26 times).
Lost: nothing that works now; the extra hand searches still cost what they did.
Added: one rulebook rule, two automatic checks (one stops only once), one handover line.
