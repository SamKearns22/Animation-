# Proposal: Rules are written without a working check, so they fail without anyone seeing

Status: parked (Sam 19 Nov: "just the communication problem for now"; packed, helpers not run)

## Problem
Several of Sam's rules have nothing that makes them happen; they rely on a chat reading them and choosing to follow
them. The plain-language rule is the latest: no check, and it failed in the review chat (19 Nov). Sam (19 Nov): "A
rule should function. If it doesn't function, you built it wrong." Sam said Y to item 12: no rule without a working
check, an audit of every rule, a gate on new rules, and each check tested on a known-bad example.

## Facts
- guides/film-quality-rules.md has 89 table rows (lines starting "| "); 20 say "by hand" in the check column (counted
  19 Nov with grep). The rows from CLAUDE.md ("Working with Sam" table, lines ~96-106) list several rules per row with
  mixed checks.
- `source/sentences.py` checks the dates table word for word (rulebook line 108).
- The plain-language rule has no check (notes/proposals/plain-check.md).
- Checks that exist but did not work: clipcheck "COULD NOT TEST" on Milburn (notes/proposals/could-not-test.md);
  two kit tests red for the whole film (notes/proposals/named-lines.md).
- Kit tests are in source/kittests.py; the watcher (source/watcher.py PROMISES) lists what each tool promises and
  `handover.py start` prints unlisted ones (19 Nov: "cost_faults has no promise in the watcher").
- CLAUDE.md "Rules are permanent": each rule written once, in the rulebook with its check, or in CLAUDE.md if it is
  about working with Sam (listed in the rulebook's last table).
- How many existing checks have ever been run on a known-bad example: unchecked.

## Record
CLAUDE.md
guides/film-quality-rules.md
source/kittests.py
source/watcher.py
source/sentences.py
source/handover.py
source/propose.py
notes/proposals/milburn-review.md
