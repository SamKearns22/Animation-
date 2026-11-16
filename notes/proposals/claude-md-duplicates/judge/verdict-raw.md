## Leak
yes: the title says the answer ("Merge the 5 rules"), and the Facts hand over the guard as already agreed (the 10-situation test, an allowance in the sentence check). Both anchor toward merging all five. The Facts also call the drift risk "unchecked" without saying that the record holds one real contradiction (unrouted.md, 16 Nov 12:55).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 3 | 3 | 3 | 3 | 4 | 16 |
| V3 | 2 | 2 | 3 | 2 | 4 | 13 |
## Sam test
Q1: Yes. An expert would measure how chats behave under the rules, fix the one place they disagree, and not edit wording to save about 0.06% of a week a film.
Q2: The evidence is the whole record: every rule ask that skipped the route (unrouted.md, install-route F9), all 42 CLAUDE.md commits (V2's history), and the archive search. That is wider than one chat.
Q3: The root cause is named: a new rule gets added where its fault happened, and the older sentence on the same subject is never changed (the route came on 15 Nov, but lines 56-57 still date from 10 Nov). The hook already enforces the route in every chat. The behaviour test gives proof. Stopping it happening again is outside Half A, and that is named.
Q4: Four approaches were weighed: merge all, fix the contradiction, learn first, and a check when a rule is written. Learning first and then fixing the one contradiction cuts faults most.
Q5: The test changes nothing. The one changed bullet is undone by its own row and commit. Sam is not asked to trust any unshown merge.
Q6: Facts are checked against the record (unrouted.md 12:55; b6594f02 and ca204390 dates; 0cb979ae; 06e62819; flying-whales-handovers line 274). Costs are marked unchecked.
Q7: The cheap trap is the five-way merge, which hits the character beat and hides the one real fault. This is sized to the fault, and its cost is stated.
Q8: The test and the wording are permanent and are reviewed at film end.
## Pick
V1
## Why
V1 is the only version that found the measured fault. Lines 56-57 still describe the pre-route way of doing things ("say what and where; wait for my numbers"). On 16 Nov a chat sent Sam a bare rule Y/N after the hook had blocked it once. Merging all five (V2, V3) saves about 130-200 tokens (0.04-0.06% of a week a film) and puts that fault among four harmless pairs.

The record shows the other four are halves, not stale copies. Two of them were added because the general wording failed:
- the 1 Nov animatic went out "with no sign-off" before "Every animatic carries..." was written (V2's find, checked: 06e62819, flying-whales-handovers line 274);
- the parent-side project rule (51846b42) came after the start-side one (P13).

V3's merge of pair 2 drops the parent's duty: a new chat cannot set its own source_url. That would lose a guard.

Taken from V2:
- the history evidence for keeping pairs 2 and 3;
- two of the test situations (note 5, where Sam was asked to type a prompt; the 1 Nov animatic without its sign-off);
- the must-beat (10 of 10 on today's wording, any miss reported to Sam);
- one numbered Y per later change;
- the drift V2 found outside CLAUDE.md (rulebook row 99 still says "Nothing needed"; "P17" names two rules), named for a separate fix.

Taken from V3: the sentence-check allowance refuses a row whose kept twin was later deleted.
## Faults in the pick
- F1 [named] The 4.8k-token beat stays missed by about 0.2k (about 0.06% of a week a film), unless the test shows another pair needs merging.
- F2 [named] Whether chat 0007a586 actually followed line 56 is unchecked. The fault is proven, its cause is inferred.
- F3 [named] Nothing yet stops the next rule from contradicting an older one (the cause). That is outside Half A, and the next proposal could be a check when a rule is written.
- F4 [fixed] V1's test situations were thin on pairs 2 and 3. V2's real situations have been added.
- F5 [fixed] An allowance row could outlive its kept sentence. The row now needs the new bullet present (from V3).
- F6 [named] The build cost (about 2% of a week once, including this route run) is unchecked.
- F7 [named] Rulebook row 99 and the double "P17" are drift outside Half A. They are listed, not fixed here.
## Final version
**1. The situation test (changes nothing).** A Sonnet chat builds a permanent test of 10 past situations, two per pair. Each situation comes with Sam's recorded right answer:
- the 16 Nov 12:55 Hook Text rule ask;
- note 5 (Sam asked to type a prompt);
- the 1 Nov animatic without its sign-off;
- a chat started without the project;
- a back-end proposal with code names;
- and so on.

A fresh helper answers all 10 using today's CLAUDE.md. Must beat: 10 of 10. Each miss is reported to Sam as a fault in today's wording. The test stays as the guard for every later rewording: old and new wording must give the same answers, except where a change is meant to fix a miss.

**2. One change (pair 4, its own Y).** Lines 56-57 become one bullet: "New rules and lessons, including when I say 'I want a rule' (or 'every film', 'from now on', 'always'), go through the proposal route first; the judged wording comes back with its place; on my yes, write it in that same chat. Each rule is written once: in the rulebook with its check, or here if it's about working with me (listed in the rulebook's last table)."
- Enforced by: the hook already refuses an unjudged ask.
- The sentence check gains a rulebook table "Reworded in CLAUDE.md" (old sentence | new bullet's first words | Sam's Y and date). The check accepts a removed sentence only if its row exists AND the new bullet is still in CLAUDE.md. A kittest covers both cases.
- Must beat: the new wording gets the 12:55 situation right and matches the old wording on the other nine; next film, 0 unrouted rule asks (1 on 16 Nov).

**3. The other four pairs stay as written.** Each is a half with its own reason: where the 3 lines go versus what they say; parent versus new chat; animatic versus TikTok look; the general rule versus back-end proposals. A pair changes only if the test misses on it. Then it goes as its own proposal with its own number.

**Cost:** about 2% of a week once (unchecked). The test is reused by every later rewording.

**Sam would notice:** rule requests always come judged, never as a bare Y/N.
## For Sam
### Option 1: Test first, fix the one rule that disagrees
Of the five rules written twice, only one actually clashes with the others. The old "propose a new rule" line still tells a chat to just ask you, but the newer proposal route says every rule goes through judging first. On 16 Nov that clash let a bare "Y/N on the Hook Text rule" reach you.

First, a test (a fresh helper answering 10 past situations, with your known answers) checks how chats read all five pairs today. Then that one line is rewritten to match the route. The other four stay, because each covers a different moment and two were added after real mistakes.

You would notice: rule requests always arrive judged.
Lost: the instructions file stays about 0.2k words-worth longer than the target (about 0.06% of a week a film).
Added: one rewritten rule, a permanent 10-situation test, and a record of the rewording that the safety check accepts.
### Option 2: Merge all five pairs behind the test
The same test is built. Then each of the five pairs becomes one sentence that keeps every case either copy named, with one numbered Y/N each, all in one message. This saves about 130 words-worth per chat (about 0.04% of a week a film) and hits the size target.

It does not fix the clash any better than Option 1. It costs a little more, and it means five changes to rules that, apart from one, have caused no recorded mistake.
Lost: about 300 letters of repeated wording. Each merged sentence carries a small risk of losing a case nobody recorded.
Added: the 10-situation test, and a record of five rewordings that the safety check accepts.
