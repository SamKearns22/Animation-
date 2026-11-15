# Helper B: what to measure next

## Leak
None. The problem file states the question and facts only.

## Root cause
We cannot see where the cost goes because nothing measures it. We only have guesses, and the two we have point at the wrong things.
- The two bills count tool calls by keyword and call their cost shares "call-count weighted guesses, not metered per action". They also say each call re-reads the whole history, so a late call costs several times an early one (bills-29-31.md). Counting calls hides the main cost driver, which is history length multiplied by the number of calls.
- Both chats measured are the same kind of work: late fix rounds and animatic 2, on the same day, in the same film (protest-tiers.md: chats 29 and 31, 2.57% and 2.36%). Neither covers the stages that overran most. From the ledger's running totals: round 1 moves spent about 14.0% against 4.45% planned, first moves about 11.3% against 3.07%, unplanned plan extras 10.08%, and cast about 6.0% against 2.09%.
- The ledger cannot link cost to rework. Every row has notes 0, repeated 0 and rounds 0, even through a notes round. The model column also says "sonnet" for chats titled "Opus medium" (chats 27, 30 and 31).
- The ledgers disagree with each other. The film line says 51.27% spent; its own "After the film" line says 33.55%. Blessed is 62.21% in its ledger but 80.02 in the comparison, and Remakes 35.96% against 51.54.
- Earlier audits failed for the same reason. They proposed fixes from guessed shares, and Sam heard that a tool might cost more than it saved (sam-to-case2.md, 19:11).

## Approaches weighed
1. **Sample by kind of work:** read one chat for each kind (plan, cast, sets, moves, fix, animatic, handover), giving 6-7 bills. Wider, but the shares are still guessed and cost is still not linked to rework.
2. **Meter every chat exactly:** take each call's real token usage from the transcripts, price it, and check each chat's total against the app's $. Every chat in all three films. This gives the true cost per call, per stage and per kind of action.
3. **Trace rework:** follow each overrun stage back to its cause, such as a redone fix, a note given twice or a stage rebuilt. This shows waste the per-call view cannot show.
4. **Controlled replay:** redo one stage under a changed process and compare. It tests a fix, so it belongs after we know which fix.

## Proposal
Do 2 and 3 together as one permanent measurement: a **cost meter** in the ledger. The closest existing tool is `source/ledger.py`, which already imports app figures per chat. What is new is cost per call, and a link from each call to the stage and the note it served.
- **What it records.** Every call in every chat gets a row: its real tokens and $, the history size when it ran, the kind of action, the stage, and whether that work was later redone. The redone flag comes from the notes ("repeated" and "notes" filled in for real). The model column is taken from the transcript, not the title.
- **Which films.** All 32 Protest Tiers chats first, because that film was made with today's tools. Then Blessed's 18 app-visible chats and all 19 Remakes chats, to separate what is new from what always costs.
- **The pass mark.** Every chat's metered total must match the app's $ within 5%. If it does not, the reading is incomplete and no change is chosen from it. The ledger disagreements above are fixed in the same pass.
- **What it delivers.** One page, ranked: the three causes behind most of the spend, each with its share and a real example. This is what later changes must target. For the next film, the meter shows whether each stage landed within its plan and whether the 15% aim was met.
- **Cost.** The figures are unchecked: about 3-4% to read 29 chats (problem file), so about 6-8% for all three films, plus about 2% to build. This is one tool job of about 8-10% of a week.
- **What Sam would notice.** A single answer: "X% of the cost is Y; here is the film moment." After that, fewer proposals that make things dearer, and a ledger he can trust.

## Sam test
- **Q1:** An expert measures before optimising: metered, reconciled to the bill, every chat.
- **Q2:** The evidence covers every chat and all three films, not two similar chats.
- **Q3:** The 5% match to the app's figures stops a guessed reading from passing, and the rework link shows the root cause.
- **Q4:** Four different methods were weighed; this one combines the two that find causes.
- **Q5:** It only reads and records, so it can be undone. No film is changed until Sam sees the ranked causes.
- **Q6:** Each number names its source; costs are marked unchecked.
- **Q7:** Sized to cover every chat, not the cheapest sample of two.
- **Q8:** A permanent ledger feature, reviewed when each film is complete.

## Lost / Added
- **Added:** the per-call cost meter, real model, notes and repeated columns, and the ranked causes page.
- **Added:** a one-off cost of about 8-10% of a week.
- **Lost:** nothing.

## Unchecked
- Whether the transcripts hold token counts for each call.
- The cost of reading the chats.
- Why the ledger totals disagree.
- How the Blessed 80.02 figure was made up.
