# CLAUDE.md map (change 4, read-only; chat 6, 16 Nov)

Every sentence of CLAUDE.md (139 lines, as at main line f52e0055), by line number.
- **Rule**: the rulebook row (`guides/film-quality-rules.md`, last table "Working with Sam", old numbers M/P) or the rule number it points at. "none" = no rulebook row today.
- **Source fault**: the fault or ask that made it, only where a file says so (the sentence itself, the rulebook, a commit message, handover.py's notes). "not recorded" = no file names one; the line came in the 10 Nov shortening (Job J, commit ca2043905) from the older, longer file.
- **Date**: the date in the text if it has one; else (c) = the date of the commit that last set the line (the first writing is older).
- **Move** (the verdict's moves, word for word): **R** = the dated tag goes to the rulebook's last table; **P** = goes to a pack, one-line pointer stays; **K** = stays in CLAUDE.md.
- Nothing was reworded. Things that look like duplicates are marked **dup** (a later, separate proposal, per the verdict).

## Working with me (lines 1-7)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 3 | I don't know how to code. Explain in plain English | none (the person) | not recorded | (c) 10 Nov | K |
| 3-4 | Make choices for me ... say briefly what and why | none | not recorded | (c) 10 Nov | K |
| 4 | Always say where the finished file is | none | not recorded | (c) 10 Nov | K |
| 4-6 | iPhone only; send animations in the chat; no computer steps | none | not recorded | (c) 10 Nov | K |
| 6-7 | The rulebook / what each stage reads | rulebook header; job-packs | none | (c) 10 Nov | K |

## Messages to me (9-25)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 10-12 | Say only what matters; first line says what is needed; Done / Needs you / Next only with content; about 10 lines | M1, M2 | not recorded | (c) 10 Nov | K |
| 13 | No code names or file internals | M3 | not recorded | (c) 10 Nov | K |
| 14-15 | One line per note; Lost / Added lines | M4 | not recorded | (c) 10 Nov | K |
| 16-19 | Back-end proposals explained plainly (Sam, 16 Nov; replaces 14 Nov) | no rulebook row yet; **dup** in part with line 13 | Sam's 14 and 16 Nov asks (named in text) | 16 Nov (tag) | R (tag only) |
| 20-21 | Questions numbered, pick first; every open decision in one message | M7, P16 (old) | not recorded | (c) 10 Nov | K |
| 22-23 | "Checks:" line only when a check slipped; never send a flagged thing unsaid | Cost job C ("ready Checks: lines") | 13 Nov silent checks (rule 19) | (c) 13 Nov | K |
| 24 | A note given before is a warning; find why the first fix failed | rule 30, P5 | repeat notes (rule 30's text) | (c) 10 Nov | K |
| 25 | The handover's 3 lines at the bottom | M6, P17 | Sam, 9 Nov (rulebook table) | 9 Nov (rulebook); (c) 12 Nov | K; **dup** with 101-103 |

## Files (27-31)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 28 | Under 50 MB, a few MB; tell me the size | none | not recorded (GitHub's limit) | (c) 10 Nov | K |
| 28-30 | Only the finished version on GitHub in `animations/`; drafts off, except latest animatic + clean render | P16 | protest-tiers chat 31 (commit message) | 15 Nov (tag) | R (tag only) |
| 30 | MP4 by default; GIF only if asked | none | not recorded | (c) 15 Nov | K |
| 30-31 | Tools install at session start (`.claude/hooks/setup.sh`) | none | not recorded | (c) 10 Nov | K |

## Asking me before you go on (33-53)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 34-35 | Offer an animatic before any full render; ask before a final and wait for a clear yes | rule 47; P2 family | not recorded | (c) 10 Nov | K |
| 36-37 | Every animatic carries Hook Text and sign-off; a check sheet shows the Hook Text frame | P7; rules 70, 75, 52 | not recorded | (c) 10 Nov | K; **dup** with 70/75 |
| 38-39 | No check sheet before an animatic unless asked | rule 88 | Sam's Y, 12 Nov (Blessed) | 12 Nov (tag) | R (tag only) |
| 40 | No animatic while a shot is missing anyone the brief puts in it | P3, rule 14 | not recorded | earlier than 9 Nov | K |
| 41-42 | "Just go" skips the wait, never the checks or handover; at red the chat opens the next | P2 | not recorded | (c) 13 Nov | K |
| 43 | Unattended runs stop after one animatic | P4 | not recorded | (c) 10 Nov | K |
| 44-45 | Notes on movement get a short clip; clips need no yes | rules 47, 48 | not recorded | (c) 10 Nov | K |
| 46-47 | A question about the film is answered, not acted on (Sam, 13 Nov) | none in the table | Blessed notes N8-N11 missed (commit message) | 13 Nov (tag) | R (tag only) |
| 48-49 | "Hold" means collect, don't act; "Hold responses ..." no replies | none | not recorded | earlier than 9 Nov | K |
| 50-51 | Critique-fix rounds: three on your own | rule 89 | not recorded | (c) 10 Nov | K |
| 52-53 | The brief is a checklist | rule 14 | not recorded | (c) 10 Nov | K |

## Rules are permanent (55-71)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 56 | New rules are proposed first; wait for numbers | P1 | not recorded | (c) 10 Nov | K; **dup** with 67-70 |
| 57-59 | "I want a rule" means permanent, written in that chat; each rule once | P1 | not recorded | (c) 10 Nov | K |
| 60-62 | Three aims; improve the check, then merge, remove only after three clean films (Sam, 13 Nov) | "Never again 1-5" (commit 2dc55343e); rule 24 | Blessed (13 Nov) | 13 Nov (tag) | R (tag only) |
| 63-66 | Channel is topical satire; every film new; never suggest doing less (Sam, 13 Nov) | none in the table | Sam's 13 Nov ask (commit 1298a9eeb) | 13 Nov (tag) | R (tag only) |
| 67-70 | The proposal route (Sam, 15 Nov), ends `source/propose.py` | `propose.py hook / review` | Sam's 15 Nov ask (commit b6594f028); replaces "search before suggesting", 12/14 Nov | 15 Nov (tag) | R (tag only) |
| 71 | Before every handover, search notes for rule requests not yet written | P1; handover.py | not recorded | (c) 10 Nov | K |

## Models and chats (73-89)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 74-76 | Models by stage | 31, P14 | not recorded | (c) 10 Nov | K |
| 77-78 | Chats open the next chat themselves, no count (Sam, 13 Nov; was 8) | create_session rule | Sam, 13 Nov | 13 Nov (tag) | R (tag only) |
| 78 | First checks it can save to GitHub, else stops and tells me | rulebook "Models and chats" row | not recorded | (c) 13 Nov | K |
| 79-80 | The project is always attached; reply must list it (12 Nov: one opened without it) | P13 (automatic) | 12 Nov: a chat opened without the project (named) | 12 Nov (tag) | R (tag only) |
| 81-84 | Chain stops only at budget stop, a question, failed save, no new work; I never start a chat | rule 24, P14 | Sam, 12-13 Nov | (c) 13 Nov | K |
| 84-86 | Wrong model for the next stage opens one on the right model (Sam, 15 Nov; handover.py flags) | handover.py MODEL check | an Opus fix that carried on into the animatic (commit e2db044b7) | 15 Nov (tag) | R (tag only) |
| 86-87 | No scheduled check-ins unless asked; never "start a new chat" or "type ..." | rulebook table (12 Nov: never a "type this") | Sam, 12 Nov | (c) 15 Nov | K |
| 88-89 | One wait per render; push notifications; say how long each render takes | P10 | not recorded | (c) 10 Nov | K |

## Fresh chats and the handover (91-103)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 92-93 | A fresh chat for every round and every cost warning; change model only by a new chat | 31, P14 | not recorded | (c) 13 Nov | K |
| 93-95 | Cost watch (rule 85): amber, red, override; an hour away means handover only | rule 85 | Sam's 9 Nov cost watch; 13 Nov "Never again" | (c) 13 Nov | K |
| 96-99 | The handover is the ONE "Where things stand", 15 lines at most, in order; update `story/status.md` | P6 | not recorded | (c) 10 Nov | K |
| 99-101 | The handover check (Sam, 13 Nov): `handover.py end` / `start`; every fault fixed, noted or answered | handover.py | Blessed notes N8-N10 unread; note 47's second half dropped (handover.py's own text) | 13 Nov (tag) | R (tag only) |
| 101-103 | The 3 lines at the bottom; every handover names the next chat's model AND effort | M6, P14 | not recorded | (c) 13 Nov | K; **dup** with line 25 |

## Reading little (105-112)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 106-107 | Three layers; long printouts filtered to the faults | rule 19, P9 | Blessed, 13 Nov (clipcheck tested nothing) for rule 19 | (c) 10 Nov | K |
| 108-110 | Notes archived at each handover; notes under 4,000 words | P15, rule 30 | not recorded | (c) 10 Nov | K |
| 110 | Pictures: one labelled sheet, never an unchanged picture | rule 48 | not recorded | (c) 10 Nov | K |
| 111 | Code: a film's code opens with a MAP | rule 61 | not recorded | (c) 10 Nov | K |
| 112 | Fewer rounds: moves checked against the acting list | rule 74, P8 | not recorded | (c) 10 Nov | K |

## Making the films (114-134)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 115 | Every chat starts with the project selected | P13 | **dup** with 79-80 | (c) 10 Nov | K |
| 116-119 | One main line; merge or name every branch the start lists; push to the main line at the end | P11; `branches.py scan` | startup-fixes change 2 | (c) 16 Nov | K |
| 119 | If the main-line push is refused, say so | P11 | not recorded | (c) 10 Nov | K |
| 120-121 | Which film, which guide; reuse before building | `job-packs.md`, kit catalogue | quick-video guide retired (Sam, 11 Nov) | (c) 11 Nov | K |
| 122-126 | Reference photos (full network since 12 Nov); news first; one failed try per source | P12 | Sam, 12 Nov (tag) | 12 Nov (tag) | **P** (photo search order); pointer stays |
| 127-128 | Earlier chats can be read | none in the table | Sam, 12 Nov (tag) | 12 Nov (tag) | R (tag only) |
| 129-130 | Sound: voices only; I record every voice | S3, S9 | not recorded | (c) 10 Nov | K |
| 131-134 | TikTok: no title; Hook Text white box; sign-off with the `finish.py` command | rules 52, 70, 75 | not recorded | (c) 10 Nov | **P** (the `finish.py` command line); pointer stays; **dup** with 36 |

## My accounts (136-139)
| Line | Sentence | Rule | Source fault | Date | Move |
|---|---|---|---|---|---|
| 136-139 | Channel name, TikTok handle, YouTube Shorts second, profile picture, pinned comment | rule 52 (follow lines) | Sam's accounts message | 26 Oct (tag) | **P** (whole section); pointer stays |

## What the map shows chat 7
1. **R (dated tags to the rulebook's last table):** lines 16-19, 28-30, 38-39, 46-47, 60-62, 63-66, 67-70, 77-78, 79-80, 84-86, 99-101, 127-128. Only the bracketed tag moves; the rule sentence stays.
2. **P (to packs):** photo search order (122-126), the TikTok `finish.py` command (131-134), My accounts (136-139). Each leaves a one-line pointer.
3. **Duplicates noticed (no edits; a later proposal with the 10-situation test):** the 3 handover lines (25, 101-103); project attached (79-80, 115); Hook Text and sign-off (36-37, 131-134); new-rule proposals (56, 67-70); no code names (13, 16-19).
4. **"Not recorded":** about half the sentences have no fault named in any file; they survive from the 10 Nov shortening (older text: `git show ca2043905^:CLAUDE.md`). So the check must be word for word, not by fault.
5. **Word-for-word check:** split CLAUDE.md into sentences (bullet ends and ". ") before the move; after it, every old sentence must be found in CLAUDE.md, the rulebook or a pack, else refuse.
