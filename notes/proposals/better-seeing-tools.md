# Proposal: Better ways for Claude to look at our images and animations

Status: open

## Problem
Claude can read only still frames, one at a time or on a sheet, and cannot watch motion. Judging hands, limbs, contact and movement from stills is the weak point: checks flag the wrong things or miss faults, and Sam (26 Nov, chat 36) asked whether any tools or programs would improve how Claude looks at the project's images and at its own drawings and animations, beyond what it does now. Checks must never block requested work (rule 93).

## Facts
- Chat 36 animatic: 9 picture-check faults from geometry checks (source/preflight.py picture_faults, plans depth); looking at three stills showed mostly intended overlap; the checks cannot read intent (notes/proposals/check-knows-intent.md).
- The films are drawn by our own engine (source/film_engine.py, brexit_is_done.py), so a second flat-colour copy of each frame (one colour per person, hand, prop) could be drawn by the same code: untested.
- Frame-to-frame motion measuring, person/hand cut-out picture models and pose finders exist outside the project: none tested on our drawings; pose finders are trained on photos, our people are flat drawings: unchecked.
- A container download of the people-building files failed on 26 Nov (preflight: git clone of makehuman blocked): network access to new tools is limited here.
- Existing seeing aids: critique.py (rule 89: a fresh helper reads a pack of pictures), stills and clips, body check and hand check, humancheck.
- Whether any video-watching model is available to this setup: unchecked.

## Record
notes/proposals/check-knows-intent.md
source/film_engine.py
source/preflight.py
source/critique.py
source/handcheck.py
source/humancheck.py
guides/film-quality-rules.md
