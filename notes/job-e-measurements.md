# Job E: measure and diagnose (9 Nov, Opus). Numbers and a cut list; nothing built.

Method in brief: token counts are this chat's own first step (the app's real figure) plus each file's size (about 4
characters a token). Rules: every mention of every rule number in all film notes (live and archive) and story/, and
the "Checks:" lines. Body notes: every notes-table line of the last ten films (Elder Swindon, Ad-Vanced Notice,
Islamocommunism, MidTerminal, Terfwarts, Flying Whales, Halo No-No, Patriots 4, Newsdesk, Patriots 3), 374 lines,
sorted by keyword and then read by hand to keep only Sam's notes about bodies.

## 1. What a new chat loads
- **Before anything is read: 79k tokens** (first step: 58k already stored + 21k newly written). CLAUDE.md is 3k of
  it (4%); the other 76k is the app itself (its instructions and tool list), which nothing in this project controls.
- Every step re-reads the whole history at the cheap stored price. With the cost watch's prices that base alone is
  **about 0.5% of a week per 100 steps**; a 10k-token guide read early adds about 0.06% per 100 steps. After an
  idle hour the whole history is written again at the dear price: a 200k chat costs about 0.55% just to resume.
- So the levers, in order: (1) fewer steps per chat (batch checks and reads into one step); (2) no resuming a long
  chat after an hour (CLAUDE.md already says hand over); (3) shorter reading lists. Guide size matters least.
- What film chats are told to read (from 25 handover "Read:" lines), tokens:

| File | Tokens | Read by |
|---|---|---|
| guides/satire.md | 9,400 | almost every film round (named sections, but sections are not marked to read alone) |
| guides/best-practice.md | 8,900 | rarely now (overlaps satire.md) |
| guides/kit-catalogue.md | 7,300 | most builds, "rows N-M" |
| guides/film-quality-rules.md (rulebook) | 6,500 | every film; usually by rule number |
| source/satire_template.py | 6,300 | every new film |
| guides/figure-rig.md | 4,900 | any film with people |
| guides/tiktok-design.md | 2,900 | new films |
| A film's notes | 4,000-8,000 | every round (Elder Swindon 7,900: over the 4,000-word limit) |
| A film's code | 14,000-45,000 per file | MAP plus the lines a note touches (rule 61) |

- A typical film round reads about 30-35k tokens of guides and notes on top of the 79k: about 40% more history,
  so about 0.2% of a week per 100 steps.

## 2. Which rules ever caught anything
- 83 rules: 53 held by a tool, 5 by a tool plus an eye, **25 by hand only**.
- **Catches are almost never written down.** CLAUDE.md asks for a "Checks:" line before every send; the notes of all
  films hold **3**. Only 12 rules are ever recorded as having caught something before Sam saw it: the collision
  audit (5, four times), the mouth/script audit (7, twice), pop-in (6), and once each 11, 13, 39, 43, 74, 78, 79, 80,
  S7. Silent passes leave no trace, so for the other 71 there is no evidence either way.
- **24 rules are never mentioned in any film's notes:** 17, 18, 22, 30, 34, 47, 50, 52, 57, 58, 63, 64, 65, 66, 72,
  85, S1, S2, S3, S4, S5, S6, S8, S9. Not a drop list (many are tools that pass quietly); Job I looks at each.
- **By-hand rules that Sam's notes show failing:** 81 (shoulder join is by hand: Sam flagged the join four more
  times after the rule was written: Ad-Vanced Notice 18, 37c, 40, 41a); 56 (fault of its kind: thumbs fixed, the
  fingers came back, 37e then 39b); 64 (standing bob, Patriots 4 note 32 then Terfwarts 14.3 the next day).

## 3. Sam's body notes, last ten films, grouped (47 notes; 13 of them repeats of a fix that failed)
| Group | Notes | Where |
|---|---|---|
| **Hand on a prop or surface** | **10** | Islamocommunism 9, 11, 16, 19; Patriots 3 5, 9, 12, 18; Patriots 4 15; Ad-Vanced 47c |
| **Shoulder-to-arm join** | **7** | Ad-Vanced 14, 18, 37c, 40, 41a; Patriots 3 17, 20 |
| Elbow and arm shape | 6 | Ad-Vanced 16, 17; Terfwarts 15.3, 14.6; Patriots 3 1; MidTerminal 34 |
| Hand shape (fingers, thumbs, hidden hands) | 6 | Ad-Vanced 37e, 39b, 42d; MidTerminal 33; Terfwarts 9, 14.14 |
| Lying | 4 | Ad-Vanced 52a, 54c, 58, 59a (one man on the ground) |
| Standing, legs, bob | 4 | Ad-Vanced 15; Terfwarts 14.2, 14.3; Patriots 4 32 |
| Body through body (hits, steps) | 4 | Ad-Vanced 34, 36b, 37b, 54d |
| Neck | 3 | Ad-Vanced 37a (three tries), 51; Halo No-No 2 |
| Mouth | 2 | Ad-Vanced 52b; Terfwarts 14.1 |
| Seated, rising | 1 | Islamocommunism 10 |

- **Arms and hands are 29 of the 47 (62%).** Ad-Vanced Notice alone gave 24. Flying Whales, Newsdesk and Elder
  Swindon (whales, cars, maps) gave none.
- Outside joints, but as heavy: likeness, faces and beards 8 notes (Ad-Vanced 1, 4, 7, 9, 42e; Patriots 4 13, 17;
  Halo 1) and arm acting ("arms hang static", "more expressive") about 10 (MidTerminal 35, 39, 40, 44, 48;
  Ad-Vanced 42f, 49, 54b; Terfwarts 8; Islamocommunism 15). The acting ones are taste, not faults.

## Cut list (what the next jobs should spend on, in order)
1. **Job G, hands first:** grip and contact points (hand on prop, on a table, on another person): 10 + 4 notes. Then
   an automatic shoulder-seam test (rule 81's join is by hand and failed 4 times). Then lying (4 notes, one film,
   and the lying tool itself made the "balloon" man). Neck, mouth and seated (6 notes together) wait.
2. **Job F, the ledger also writes each check's result per round** (passed, caught, could not test), so the
   question "which rules catch things" has an answer next time instead of 3 "Checks:" lines.
3. **Job I:** the 25 by-hand rules and the 24 never-mentioned rules are its list; satire.md plus best-practice.md
   (18k together) is the biggest reading cut; sections marked so a chat can read one alone.
4. **Now, no build:** move finished films' notes to the archive the day Sam says posted (Terfwarts, MidTerminal,
   Islamocommunism, Elder Swindon still sit in `notes/`), and the closed sitting-kit notes.
5. **Habit, no build:** batch reads and checks into fewer steps; it is the biggest single lever on cost.

Estimate 0.7% of a week; this chat about 0.6%.
