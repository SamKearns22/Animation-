# Goals review, 14 Nov (did the 13 Nov goals land?)

Sources: CLAUDE.md Statement 1, `notes/overnight-run.md`, `notes/ranking-list.md`, `notes/morning-report.md`,
`notes/critic-bench.tsv`, the ledger, git log since 13 Nov, and the app's own cost for every job chat (get_session
usage, read 14 Nov ~21:05 UTC; WEEK_USD 171, so 1% = $1.71). Nothing in a tool or rule was changed by this review.

## Verdict per goal
| goal | verdict | evidence (one line) | what would prove it |
|---|---|---|---|
| **S1a: high quality** | can't tell yet | No new film has been made with the new tools. Face tool: Sam's notes drove it (chat 5 "not recognisable, off house style"; chat 12 "3/4 poses gaunt and weird"); Andy finished, Kemi "right". | Protest Tiers' animatic 1: Sam's taste notes on the cast and places vs Blessed's animatic 1 (52 notes on animatics 1-2). |
| **S1b: fewer notes and faults** | can't tell yet | Tools catch on old films only. Critic (Sonnet, close-ups) caught 4-9 of 12 Blessed fault notes and 2-3 of 7 Remakes; both critics always missed the judge's missing mouth and the neck join. | Protest Tiers: Sam's notes on animatic 1 split into "a check could have caught it" vs taste; target under Blessed's ~24 catchable of 63. |
| **S1c: a film within 15% of a week** | not yet, and Protest Tiers will not show it | Protest Tiers' own plan says 21.5%; it has spent ~14.7% (incl. ~4% framing research) before its cast is built. The ranking list itself says 15% is in reach only for a typical film (3 people, 2 places). | The first film planned AFTER the kits, with Job N's honest-fit line at its plan; measure total spend against it. |
| **Overnight order** (Q, bench, page, people, places, moves, rough) | achieved | Git log runs in that order, 13 Nov 23:26 to 14 Nov 07:45. | - |
| **Test only on Blessed** | achieved | Every kit test redraws Blessed; nothing touched Protest Tiers. | - |
| **150% hard stop per job** | partly (failed for 4 of 9) | People, places, moves stayed under their stops. Q, page, rough, bench went over on the app's figures (table below); the face tool ran 7x its stop with Sam's extensions. The stops did not fire because the chats' own cost readings were low. | Next tool job: the stop read from the app's figure, not the chat's own count. |
| **Chain opens the next chat itself** | partly | Broke three times: the 5-hour limit (chat 4b failed; the 02:40 wake-up resumed it: worked); chat 5d stopped at an "8-chat limit" 25 min after CLAUDE.md dropped the count (Sam started chat 7 by hand at 06:30, ~2 h idle); face chat 11 told Sam to "start a new chat and type". | No chat on Protest Tiers or the face chain asks Sam to start one. |
| **Every tool: kittest, MAP, catalogue row** | achieved | All ten new tools have all three. | - |
| **Old kittests all pass** | partly | 2 fail on the main line: `round_page` (page 16.4% of Blessed's code, bar 15%; a cleanup chat is on it) and `critique_helper_kind` (pack names a general helper). | Both green. |
| **Replication pass mark** (kits redraw Blessed) | achieved for people and places; moves all but 4 one-offs | People: 20 people and a 31-strong press pack, 0.00%. Places: 13 paintings, worst 0.008%. Moves: 16 people-in-shots 0.000%; jury, cot, two inmates, Walliams' struggle stay as code. | Done. But see "What it proves" below. |
| **Kits approved by Sam before any film uses them** | achieved | Sam's Y 14 Nov (people, places, moves, rough sheet). | - |

## Spend against estimate (app figures; the chats' own claims in brackets)
| job | estimate -> stop | real | verdict |
|---|---|---|---|
| Q handover check | 1.5 -> 2.25 | **2.8%** (claimed 2.2) | over the stop |
| Critic bench (4 chats) | 1.5 -> 2.25 | **10.4%** (claimed ~10.3 across chats) | 7x estimate; Sam asked for the Remakes and repeat tests |
| Rounds read a page | 0.5 -> 0.75 | **1.0%** (claimed 0.75) | over the stop |
| People kit (4 chats) | 8 -> 12 | **8.9%** (claimed 6.8) | over estimate, under stop |
| Places kit (4 chats) | 8 -> 12 | **9.1%** (claimed 7.1) | over estimate, under stop |
| Moves kit (3 chats) | 6 -> 9 | **5.5%** (claimed ~5) | under estimate |
| Rough command | 0.5 -> 0.75 | **1.9%** (claimed 0.45) | 3.7x estimate, over the stop |
| Face tool chats 1-5 | 3 -> 4.5 (Sam: 7.5) | **12.1%** (claimed 10.0) | over every stop |
| Face tool chats 6-11 (12, 13 running) | none (Sam: "don't limit") | **18.9%** | no stop by Sam's choice |
| Parent chats (ranking list, morning updates) | - | 4.6% | - |
| **Total** | ranking list "all built ~29%" | **~75% of a week ($128)** | about 2.6x the plan |

The chats under-reported their own cost by 20-75% (rough 0.45 claimed vs 1.9 real). This is the main reason the hard
stop failed: it was measured with the low reading.

## What the results prove, and what they don't
- **Replicating Blessed proves the kits can re-express Blessed's drawings, not that new films get fewer notes.** The
  kits were built by lifting Blessed's own parts ("lifted unchanged in look"), so a 0.00% match mostly shows the move
  from code to description lines lost nothing. It does not show that a new person or place drawn from 8 lines looks
  right, or that the 24 catchable Blessed notes would not happen again. Protest Tiers' cast is the first real test.
- **Line counts are real savings in reading, not yet in money.** Cast 1,661 -> ~250 lines, sets 1,491 -> 226, moves
  -> 173 lines. Whether a notes round therefore costs less is unmeasured.
- **The critic bench proves Sonnet is at least as good as Opus on 19 old notes, not that it catches enough.** Run-to-run
  spread (Blessed Sonnet 4, 9, 7 of 12) is as large as the gap between critics. About half of the catchable notes still
  get past both.
- **The face tool has not paid back and is the biggest overrun.** Promised: 3% to build, saving Walliams' five chats
  (18.6%). Real: 31% so far, still running; the 3-minute Walliams replay passed the automatic likeness check but Sam
  judged it not recognisable, and the house-style Kemi was not named in 3 blind name tests (chat 9). The automatic
  check is not yet a stand-in for Sam's eye. Payback now needs roughly two films with a new famous face each at no
  extra build.
- **The rough command and page are cheap and stand alone,** but each saving depends on Sam's look at the sheet and on
  the kits being used.

## What to measure on Protest Tiers (in progress)
1. **Cast stage cost** against its 3% budget and its estimate rows (protester 0.4, riot officer 0.7, rioter 0.7, moped
   0.7): the people kit's first real price. Lines per new person (aim ~10).
2. **Places stage cost** against 0.9% per painting (Blessed: 5.24% for 6) and pop-in/collision faults found by the kit.
3. **Sam's notes on animatic 1, split catchable vs taste,** and how many the Sonnet critic caught first (bench: ~half).
4. **Rebuild notes after the rough sheet** (Blessed had 6: notes 4, 5, 20, 22, 32, 39).
5. **Round chats:** start size (target near 100k, was 130-150k) and cost per round (Blessed: nine round chats, $40).
6. **Moves stage cost** (claimed ~0.5% with the kit, was ~1.5%) and arm/hand notes (Blessed: 7).
7. **Chain breaks:** count every time Sam has to start a chat or type a prompt (target 0).

## Recommendations (up to 3)
1. **The cost watch and budget stop read the app's figure, not the chat's own count.** Closest: rule 85 (cost watch)
   and `ledger.py app` (already imports app costs); new: the hard stop and the per-job lines in reports use
   get_session's cost at handover. Without it, every "under the stop" claim above was 20-75% low.
2. **Price every tool job against the next film before it grows.** Closest: Job N / rule 24 (`ledger.py estimate`);
   new: a tool job past 150% of its estimate states in one line how many films it now needs to pay back (the face tool:
   ~2 films with a new famous face), so Sam decides with the number.
3. **Make the chain-opening check a test.** Closest: CLAUDE.md "Chats open the next chat themselves" and `handover.py
   end`; new: `handover.py end` flags any reply that asks Sam to start a chat or type a prompt, and any limit or count
   that is not in CLAUDE.md (chat 5d's "8-chat limit", face chat 11's "start a new chat").

## Where things stand (goals review)
- **Rules that bite next:** 85 (cost watch), 24 (estimate and budget stop), 86 (tool kittests).
- **Done:** this review (verdicts, real spend from the app, what to measure on Protest Tiers).
- **Sam (14 Nov, ~22:40): Y to 1, 2 and 3.**
- **Next (Opus, medium; building from a clear plan):** write 1 and 2 into the rulebook at rules 85 and 24 (edit, not new rules; each with its check), build 1 in `ledger.py` (budget stop and report lines from get_session cost) and 3 in `handover.py end` (flag 'start a new chat' / 'type' asks and limits not in CLAUDE.md), kittests for both, catalogue rows; tell Sam the exact wording written. Also copy the 7 measures into Protest Tiers' notes.
- **Needs Sam:** nothing.
- **Read:** this file only.
- **Open rule requests:** 1-3 (Sam: Y), to be written by the next chat.
- **For Claude:** costs from get_session `external_metadata.usage.cost_usd`; face chats 12-13 were running (not counted).
