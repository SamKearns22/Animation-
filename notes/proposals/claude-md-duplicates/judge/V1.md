# Helper B: the five CLAUDE.md "duplicates"

## Leak
The title ("Merge the 5 rules") and the named guard (10-situation test, sentences.py allowance) presume the remedy; ignored.

## Results
- **Size is negligible.** The five second copies are 447 characters (counted: lines 25, 101-102, 115, 56, 19's clause), ~80 more for the shared sign-off clause: ~200 tokens, about **0.06% of a week a film** (learn.md: 1.6% per 5.47k tokens). The 4.8k beat needs ~470 characters off (handover.md).
- **One pair has caused a fault.** `notes/proposals/unrouted.md`, 16 Nov 12:55, chat 0007a586: "2 Y/N on the Hook Text rule" went to Sam with no proposal, after the hook blocked it once. Lines 56-57 still describe the old way ("say what and where; wait for my numbers"; "reply with the exact wording"); lines 67-70 (15 Nov, b6594f02) and the hook require the route. install-route.md F9 names this gap. Whether that chat followed line 56: unchecked.
- **The other four pairs: no recorded fault** (archive searched).
- **They are halves, not copies.** Pair 1: where the 3 lines go (25) vs what they say (101-102). Pair 2: the parent attaches the project (79-80); the new chat checks its own start (115): two actors (rulebook P13). Pair 3: animatics carry Hook Text and sign-off (36-37) vs the TikTok look (127-128); only the sign-off overlaps. Pair 5: a general rule (13) restated for back-end proposals, Sam's 16 Nov ask (19).
- **Gap:** no record of how chats read the four; the 10-situation test is unbuilt.

## The real decision
Not "save characters" (0.06% a film) but "does every rule tell every chat one thing?" The lever is the pair that contradicts the hook (blocked reply, unrouted ask reaching Sam), and why contradictions appear.

## Root cause
CLAUDE.md is ordered by moment; a new rule is written where its fault happened, and the older sentence on the same subject is not amended. The route (15 Nov) was added without changing lines 56-57 (10 Nov, ca204390). "Each rule is written once" (line 58) has no check: sentences.py guards loss, not contradiction.

## Approaches weighed
1. **Merge all five** (the file's frame): one bundled yes, 0.06% saved; drops pair 2's child-side check.
2. **Reframe: fix the one contradiction** (pair 4); keep the four halves, each with its reason.
3. **Learn first:** a fresh helper answers past situations each pair governs with today's CLAUDE.md; only pairs it gets wrong change.
4. **Prevent:** when CLAUDE.md gains a sentence, the handover check shows the nearest existing ones and asks "amends which?". Outside Half A; its own later proposal.

Pick: 3, then 2.

## Proposal
**Learn (changes nothing):** a fresh helper gets 10 past situations (the 12:55 Hook Text ask, a failed save, a chat without the project, a clip's sign-off) and today's CLAUDE.md; answers are scored against what Sam asked for. Built once, it stays as the guard for every later rewording. ~0.5% of a week (unchecked).

**Change 1 (pair 4, its own Y):** lines 56-57 become one bullet: "New rules and lessons, including when I say 'I want a rule' (or 'every film', 'from now on', 'always'), go through the proposal route first; the judged wording comes back with its place; on my yes, write it in that same chat." "Each rule is written once…" stays.
- Enforced: the hook already refuses an unjudged ask; sentences.py gains a rulebook table "Reworded in CLAUDE.md" (old | new | Sam's Y) so the loss check accepts it on purpose.
- Beat: unrouted rule asks, 1 on 16 Nov, 0 next film; the new text scores at least as well as the old on all 10 situations.
- Cost: build ~0.3% plus this route run (~1.3%, install-route F7): ~2% once, against 15% a film.

**Changes 2+:** only a pair the learn step catches, one at a time, each with its own number.
**Sam would notice:** rule requests arrive judged, never as a bare Y/N.

## Sam test
Q1: Yes; measure behaviour, fix the contradiction, not the character count.
Q2: Checked against every recorded rule ask (unrouted.md, install-route), not one chat.
Q3: Hook, allowance row and replay enforce it; the root cause is named, prevention flagged.
Q4: Four different approaches; 3 then 2 cuts faults most.
Q5: One bullet changes, undone by restoring its row; the learn step changes nothing.
Q6: Sources named; costs and the chat's motive marked unchecked.
Q7: The cheap merge hides the real fault among four harmless pairs; this is sized to the fault.
Q8: Permanent wording and test, reviewed at film end.

## Lost / Added
Lost: the 4.8k beat stays missed by ~0.2k (~0.06% a film) unless the learn step finds more.
Added: one merged bullet, a rulebook row, the 10-situation test.

## Unchecked
The learn step's cost; whether chat 0007a586 followed line 56; the token-to-cost ratio.
