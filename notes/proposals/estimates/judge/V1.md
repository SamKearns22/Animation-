# The chat's own idea (chat 1, written before the helpers)

Price from our own results, in the unit cost really follows, and check every price against its actual.

1. Every price given to Sam is written down as it is given: a ledger "quote" (film, stage or task; the % and the
   week size used; date; chat). ledger.py auto, at each chat's end, adds what the chat cost to the open quote it
   worked on. Unplanned work opens its own quote at 0, so it shows up as a miss instead of vanishing.
2. A calibration table, rebuilt from those pairs: for each kind of work (plan, cast, sets, moves, animatic, notes
   round, final, tool/proposal job) the measured ratio actual / quoted over the last 3 films or 10 quotes, and the
   typical number of chats and rounds. A new estimate is the table-based figure times that ratio, given as a range
   (typical to bad case), never a single number. Until a kind has 3 pairs, the price says "unmeasured".
3. Price chats, not things: a stage's price = expected chats x (start-up cost + expected steps x average history per
   step), using stepcost's measured steps and hist_k; the thing list only sets how many chats.
4. Notes rounds priced at the measured count per film (Remakes, Blessed, Protest Tiers: 2-4, not 1), each at its
   measured cost (~3-10%).
5. The unit: estimates kept in dollars and shown as % at the current week size; a week-size change re-states open
   estimates. Sam's meter reading is asked once a week (optional), to correct the week size.
6. ccusage is not needed (stepcost already reads the transcripts); /compact is a cost lever, a separate job.

Lost: a single confident number; Added: a range, one ledger field, a weekly table rebuild (cheap, by script).
