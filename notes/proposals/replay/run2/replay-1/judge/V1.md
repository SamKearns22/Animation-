# Helper B: cut what it costs to make a film

## Leak
A mild one. The facts point at the code-finding tools (MAP, `page.py`), and "decide what change to make" asks for one change before the results are in. I set both aside.

## Results
- **The whole film:** Protest Tiers has spent 51.27% of a week over 32 chats, against the 15% aim, so 3.4 times over. Its own estimate was 63.51%, already 4.2 times the aim (ledger `protest-tiers.md`). The "After the film" line says 33.55%, which does not match. It may leave out research and tool work under the "costs by kind" part of rule 24: unchecked.
- **By stage** (from the ledger's "spent at its end"): the unplanned extras in plan cost 10.08. Cast cost 5.96 against 2.09 planned, sets 4.74 against 3.7, moves 11.30 against 3.07 and animatic 1 2.13. In round 1, cast cost 3.66, sets 1.30 and moves 14.04 against 4.45. **Moves alone cost 25.3, about half the film.**
- **Per chat:** about 1.6% on average. The chats' names show a run of fix chats in moves: 14, 16, 18 (pre-flight crash), 29 (pre-flight faults), 30 and 31 (black frames).
- **Chats 29 and 31** (bills file): code looks were 27-35% of steps, checks 4-23%, waiting on renders 14% in chat 31 and bookkeeping 9-12%. At start-up, each chat read notes, guides or CLAUDE.md 11 to 19 times. Neither chat used `page.py` or `codemap.py`; each ran 25-26 grep/sed calls on code (tool-use file). These shares are **guesses from keywords and call counts, not metered**, and these two chats are about 10% of the film's spend.
- **The fixed cost of every chat:** a fresh chat starts at about 90k tokens (`FRESH` in `costwatch.py`), and every step re-reads the whole history.
- **Gaps:** the ledger shows "0 rounds, 0 notes, 0 repeated", so notes and rework are not recorded. Nobody has split the film's cost into first build vs fixing its own faults. `source/costbreak.py` already meters a transcript step by step (re-read, new material, writing), but the bills did not use it.

## The real decision
The real question is not how one chat finds code more cheaply. It is why one film takes 32 chats and 51% when the aim is 15%, and which cause of that spend to remove first. Two levers are bigger than code lookup: rework in moves (about half the film) and the fixed cost each chat pays to start up and hand over, multiplied by the number of chats.

## Root cause
- **First cause (strong evidence):** faults found late and fixed in new chats. Moves overran 3.7 times in its first pass and 3.2 times in round 1, and the chats are named after faults: crashes, pre-flight faults and black frames. A fault caught after a build costs a fresh chat (90k tokens and 11-19 reads) plus a long history of fixing.
- **Second cause:** there is no metered bill per film, so earlier audits chose fixes from two-chat keyword counts. That is how Sam came to hear that what was built "could in fact be more expensive".
- **Third cause:** the code tools exist but nothing makes a chat use them. Rule 61's check is only a pre-flight warning, and `protest_tiers.py` is 2,283 lines against the 1,000-line split.

## Approaches weighed
1. **Enforce code lookup:** a hook pushes `page.py find` before grep/sed on film code. This aims at about 30% of two chats, so at most about 3-5% of the film.
2. **Reframe to fewer, fuller chats:** cut the start-up and handover cost per chat, so a stage takes 2 chats, not 6.
3. **Reframe to rework:** catch moves faults (crashes, black frames, pre-flight faults) while the moves are being built, so no fix chat is needed.
4. **Learn first:** run a metered bill of the whole film, split into start-up, code finding, building, checks, fixing its own faults, waiting on renders and bookkeeping. Then pick.

**Choice: 4 first, then the one change the bill shows is biggest** (most likely 3, then 2). It meets all three aims. It does not cut quality, it removes rework where faults come from, and it aims the change at the share that actually stops 15% being reached.

## Proposal
**Step 1, learn (changes nothing).** Extend `costbreak.py` (edit, not a new tool) with two new kinds of step: "start-up" (every step before the first build or edit) and "fix of own fault" (a step that follows a failed check or render, or a chat named as a fix). Run it on all 32 Protest Tiers chats and on one earlier film (Remakes) to compare. The output is one table, the film's % by kind and by stage, written into the ledger by `ledger.py` so every future film gets it automatically.
- Cost: about 1-1.5% of a week, one Opus-medium chat, filed under tool work and not against the film.
- Unchecked: whether the old transcripts can be read locally. If they must be paged through in a chat, that cost could double, and the chat says so before it starts.

**Step 2, change (one at a time, each on its own yes).** Only the biggest share from step 1 gets a change, with its own number to beat:
- **If rework is biggest:** a moves gate inside the build that renders every shot's first, middle and last frame and the crash and black-frame checks after every edit, and refuses the handover while one fails. To beat: moves' share of the film down from about 50%, and fix chats per stage from about 4 to 0-1.
- **If start-up is biggest:** `handover.py start` prints the named pack's sections itself, so a chat makes no guide reads of its own. To beat: start-up reads from 11-19 to 3 or fewer, and start-up share down by half.
- **If code finding is biggest:** a hook that blocks grep/sed on film code until `page.py find` has run in that chat. To beat: code-look share down from about 30% of a chat.

Each change is enforced by a hook or check, not by a chat choosing to follow it. Each is measured by the same bill on the next film and reviewed against the ledger when Sam calls the film complete.

**What Sam would notice:** one table showing where his money went. Then one change at a time, each with "this should cut X% to Y%". Over time, fewer "fix" chats in the chain.

## Sam test
- **Q1 Expert:** yes. An expert profiles the whole workload with a meter before optimising, and goes after rework first.
- **Q2 Best result:** the evidence is all 32 chats plus one earlier film, not two chats.
- **Q3 Comprehensive:** the root cause rests on the ledger. Each change is enforced by a hook or gate, and the bill shows whether it worked.
- **Q4 Most intelligent:** four different approaches were weighed. The bill decides which change comes first.
- **Q5 Risk:** step 1 changes nothing. Each change can be undone on its own.
- **Q6 Checked:** every number names its source. The gaps are marked.
- **Q7 Not the cheap version:** it is sized to the biggest share of the film, not to the quickest tool tweak.
- **Q8 Nothing temporary:** the bill becomes a permanent ledger feature, and each change is permanent, reviewed when the film is complete.

## Lost / Added
- Lost: nothing.
- Added: two kinds of step in `costbreak.py`, a per-film bill in the ledger, and later one enforced change per yes.

## Unchecked
- Whether the 32 transcripts are readable locally.
- Why the "After the film" figure (33.55%) does not match the ledger's spend (51.27%).
- Ledger model labels: chats 27, 30 and 31 are marked "sonnet" but named "Opus medium".
