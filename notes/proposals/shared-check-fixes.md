# Proposal: Check fixes made inside one film's code are lost to the next film

Status: replaced:named-lines (22 Nov: merged into named-lines, same cause; Sam "Milburn: begin all")

## Problem
On Milburn, chat 18 removed 60 false lines from pre-flight (the checks run before every animatic) by making the film's
own code hand the checks the cleaned voice takes. The fix lives in that film's code only, so the next film starts with
the same 60 false lines. False lines bury real faults: Milburn's real clipping fault sat among 48 to 61 named lines.
Milburn review lesson 4 and section 1 item 5; Sam put it third in the queue (19 Nov).

## Facts
- notes/archive/milburn.md line 13 (chat 18): "milburn.py now hands the checks the cleaned takes (`_voice`,
  `_stretches`, `n` per line), which removed 60 false script/mouth lines; 60 lines left named".
- notes/proposals/milburn-review.md section 1 item 5: "Improved the film, not the tool ... only for this film".
- The shared checks: source/preflight.py (unchecked name; search), source/kitchecks.py, source/audit.py.
- The film template new films start from: source/satire_template.py (rule 75 names it).
- How many other check fixes went into film code instead of shared tools across Blessed and Milburn: unchecked.

## Record
notes/archive/milburn.md
notes/proposals/milburn-review.md
source/milburn.py
source/satire_template.py
source/kitchecks.py
source/audit.py
source/
guides/kit-catalogue.md
