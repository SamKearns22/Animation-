# Proposal: A check that "could not test" passes as a line, so the fault it exists for reaches Sam

Status: open (un-parked 22 Nov, Sam: "Milburn: begin all"; his 19 Nov words below still stand)

## Problem
On Milburn the name cards were hidden by hands and cut by captions twice, and Sam had to note it twice (chat 13 and
chat 18). The clipping check (the check that sees one drawn thing pass through another) never ran on the film: it
printed "COULD NOT TEST" because the film gave it no solids or layers, and that line was carried from chat to chat as
one of the old "named" lines (lines a chat lists to Sam as known, instead of fixing). A check that cannot run looks the
same as a check that ran and found little. Milburn review lesson 1 (notes/proposals/milburn-review.md, section 3);
Sam put it first in the queue (19 Nov).

## Facts
- notes/archive/milburn.md line 11 (chat 13): name cards fixed; "Why the clipping check missed it: it never ran on this
  film ('COULD NOT TEST': the film gives it no solids or layers), and that line was carried as an old quick-check line."
- notes/archive/milburn.md line 14 (chat 18): Milburn's name card again; "clipcheck COULD NOT TEST on this film (no
  solids/layers), and chat 13 judged his card clear by eye on a still where his arm was away." That is a repeat note.
- notes/archive/milburn.md line 20 (chat 15): pre-flight's 48 quick-check lines included "clipcheck COULD NOT TEST";
  all 48 "named to Sam in the Checks line, not settled".
- Where "COULD NOT TEST" is printed: source/audit.py line ~447 (HEAD 'untested'), source/kitchecks.py lines ~619 and
  ~798; source/handover.py lines ~372-385 already count an undeclared-list COULD NOT TEST as a fault at handover.
- Rule 59 (guides/film-quality-rules.md): the final render waits for an animatic that passed the picture checks.
- Milburn cost 21.99% of a week against an estimate of 24% (notes/ledger/milburn.md).

## Record
notes/archive/milburn.md
notes/archive/milburn-handovers.md
source/audit.py
source/kitchecks.py
source/handover.py
source/clipcheck.py
guides/film-quality-rules.md
notes/proposals/milburn-review.md
notes/ledger/milburn.md
