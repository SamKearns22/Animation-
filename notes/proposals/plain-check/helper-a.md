## Leak
Mild: "the test case that must fail" presumes an automatic text check, and the decision line narrows the scope to change asks only. Ignored both.

## Results
- Milburn lessons (10, sent 19 Nov): Sam answered "2. Explain", "6. Explain", "9. I don't know what you mean by brow cap!", then "2. I still don't understand. Are you suggesting permanently deleting checks?": 3 of 10 lessons needed 4 extra exchanges, one explained twice and still not understood (notes/ledger/sam/iqdpxykr.md).
- Sam's exact words (17:36): "Fix the simple communication tool now as I am struggling to follow all the other chats." Offered 1 (check on system asks) or 2 (overview of all chats), he picked 1 (same file; review chat record).
- Same chat, same day: the 1.1x answers (plain, short, no code words) drew no "explain" (chat record, 11:08 and 11:13).
- Across all 47 logged chats (13-19 Nov), confusion in Sam's own messages appears only on 19 Nov: the review chat and "Explain listed jobs ... in very plain language" (h3akq5qv.md). The let-through log has 10 entries dated 19 Nov, not 8 (notes/proposals/unrouted.md).
- The route's own Sam format (guides/proposal-route/judge.md "For Sam": 3-6 lines, Lost, Added) leaves out steps, why, what he'd notice and the other option: the route produces rule-breaking text by design.
- Gap: the record shows only confusion Sam voiced, not messages he skimmed without asking. Cost of the confusion rounds in % of a week: unchecked.

## The real decision
Can Sam follow every message from every chat without asking "explain"? Bigger levers than a check on change asks: the templates that write the messages (the judge's format) and the missing definition of "technical word", without which no check can work.

## Root cause
1. The nearest template wins: chats copy the judge's "For Sam" shape and the review's ad-hoc lesson shape, not the prose in CLAUDE.md.
2. "Technical word" is undefined (no word list), and the writer cannot see its own jargon: "guard", "kit", "brow cap" are everyday words to chats that read them all day.
3. The only hook checks paperwork (a verdict, the Critiqued line), never shape or words, and lets any reply through after one block.

## Approaches weighed
1. Words-and-shape gate in the existing end-of-reply hook (a script run each time a chat finishes a reply).
2. Fix at source: the route's Sam format becomes the full rule shape; the reply must carry it.
3. Reframe, a blind reader: a fresh helper with no project knowledge reads each system ask as Sam would and lists what it can't follow, added to the route as a step before the judge's text goes out.
4. Learn first: define "technical word" from the record and test any check on known-bad and known-good messages before switching it on.
5. Daily overview of all chats (Sam's option 2; he chose 1).

## Proposal
Learn first (no change, ~0.7% of a week, runs at once): build the project word list mechanically: every term in the rulebook, kit catalogue, file and tool names, minus words Sam has used himself in notes/ledger/sam (his words are his vocabulary: animatic, Hook Text, helpers, blind judge). Collect a test set: the 10 Milburn lessons and the front-on-focus Sam text (must fail); the 1.1x replies and 20 recent routine replies (animatic, clip, notes: must pass).
Then three separate Y/Ns in one message, each built and tested alone:
1. **Source** (~0.4%): the judge's "For Sam" and the route's print become: problem in 1-2 sentences, numbered steps, Why, You'd notice, Other option, Lost, Added. The recorder refuses a verdict missing a part. Beat: front-on-focus rewritten passes the gate below.
2. **Gate** (~1.2%): the end-of-reply hook, on every reply to Sam, blocks any listed word or code name (file name, backticks) not explained where it first appears (a gloss in brackets or "means"); on a system ask it also requires the shape parts. It blocks up to three times (counted per reply), not once, so a lazy second try cannot slip through; any let-through is logged and stops the handover check. Beat: 10/10 Milburn lessons blocked, 0 false blocks on the test set, a standing test (kittest) holding both.
3. **Blind reader** (~0.3% per routed ask): a route step that hands only the Sam text to a fresh helper; anything it can't follow is fixed before the judge's verdict is recorded. Catches jargon the list misses. Beat: it flags "brow cap" and "named lines" on the Milburn text.
Outcome measured in the end-of-film review: Sam's "explain / don't understand" messages per system ask, from his logged messages: Milburn 4 per 10; target 0. One-off total ~2.6% of a week; per film near zero.
Sam would notice: system asks always in one shape, every unfamiliar word explained on the spot; no change to animatics, clips or notes.

## Sam test
Q1: Yes; fixing the template and defining the vocabulary is what an expert does before adding a checker.
Q2: Scope is every chat's replies, evidence from all 47 logged chats, not one review.
Q3: Gate runs in every chat by hook, not by reading; blocks three times; outcome counted from Sam's own words.
Q4: Five approaches weighed; source plus gate plus blind reader beats any one alone.
Q5: Each piece undone alone; tested on known-bad and known-good before switching on.
Q6: Sources named; the 8-vs-10 count and costs flagged.
Q7: Sized to the result: a word list from the record, not a guess.
Q8: Permanent; reviewed at film end against the count.

## Lost / Added
Lost: a few seconds per reply; a rewrite when a word is unexplained.
Added: one message shape; a project word list; three checks.

## Unchecked
Review chat's cost of the confusion rounds; whether earlier messages confused Sam without his saying so; false-block rate until the test set is run.
