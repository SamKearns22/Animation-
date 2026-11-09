# Job E: measure and diagnose (9 Nov; rerun the same day on Opus high). Numbers and a cut list; nothing built.

Rerun method (what changed from the first pass): token counts measured from this chat's own steps (how many tokens
each file added when it was read), not guessed at 4 characters a token. Body notes: the notes of the seven films with
people read in full, every section (Ad-Vanced Notice, Islamocommunism, MidTerminal, Terfwarts, Halo No-No, Patriots 4,
Patriots 3); Elder Swindon's checklist rows read; Flying Whales and Newsdesk (no main cast) and the ten films'
handover files searched by keyword only (the cost watch went amber). Catches: all commit messages since 27 Oct and
every "Where things stand" section, not only the notes tables.

## 1. What a new chat loads (corrected)
- **Before anything is read: 80k tokens** (confirmed: 58k already stored + 21.5k newly written). CLAUDE.md is about
  **5k of it (6%), not 3k**; the other 75k is the app itself, which nothing in this project controls.
- **This project's files run at about 2.35 characters a token (2.4 tokens a word)**, measured three ways in this chat
  (the job list 2.4, the first Job E file 2.25, film code 2.35). The first pass used 4, so **every file figure it gave
  was about 70% low.** A notes file at the 4,000-word limit is about 9,600 tokens.

| File | Tokens (measured ratio) | First pass said |
|---|---|---|
| guides/satire.md | 16,000 | 9,400 |
| guides/best-practice.md | 15,100 | 8,900 |
| guides/kit-catalogue.md | 12,400 | 7,300 |
| guides/film-quality-rules.md (rulebook) | 11,100 | 6,500 |
| source/satire_template.py | 10,700 | 6,300 |
| guides/figure-rig.md | 8,400 | 4,900 |
| guides/tiktok-design.md | 4,900 | 2,900 |
| A film's notes | 7,000-14,000 (Elder Swindon 13,400; Ad-Vanced Notice was 25,000) | 4,000-8,000 |

- A typical film round reads about **40-55k tokens** of guides and notes on top of the 80k (first pass: 30-35k), so
  its history is about 55% bigger than a bare chat, not 40%. satire.md plus best-practice.md is **31k** together.
- The levers stay in the same order: (1) fewer steps per chat; (2) no resuming a long chat after an hour; (3) shorter
  reading lists, which now matter more than the first pass thought (a guide costs 70% more than it said).

## 2. Which rules ever caught anything (deepened)
- **No check sheet or pre-flight report is kept anywhere.** Check sheets were sent in the chat only; `report.py`'s
  full lists are not committed. So the only record is what a chat chose to write in notes or a commit message.
- New catches found outside the notes tables (commit messages and "Where things stand"):
  - **Rule 41 (handcheck: every arm ends in a hand) is the busiest catcher on record, missed by the first pass:**
    Terfwarts (30 faults before the animatic: run hands into the sleeves, hands hidden by the boys' backs);
    MidTerminal (3: press palm, wave from the cut, mock wave); Patriots 4 (hands over the table, over-shoulder
    backs); Patriots 3 (the Loader's hand behind his head, found on the finished film the day before Sam named it as
    note 21: the check works, it just came after that film).
  - Rule 62 (subtitles): Terfwarts subtitles joined; Halo's 0.5 s "Sir," caption. Rule 65 (loudness mouths): very
    likely Terfwarts' "livelier mouths". Two pre-flight checks with no rule number now: voices 6 dB over music (Halo's
    music ducked) and line weight (Cortana's lids).
  - False alarms on record: the silhouette audit (rule 6) flagged MidTerminal's melt; the hand check flagged
    Ad-Vanced Notice's man on his own canvas; the mouth check over-reads drawn-out words (four films).
  - A check that missed silently: the touch check (S2) could not find Abdul's hand and said "not in the scene"
    (Islamocommunism note 9); fixed 7 Nov to say COULD NOT TEST.
- So **15 numbered rules** have a recorded catch (was 12: add 41, 62, 65), plus the two unnumbered checks. The 24
  never-mentioned rules and 25 by-hand rules stand as listed in the first pass; 81 (shoulder join, by hand) is still
  the clearest by-hand failure.

## 3. Sam's body notes, last ten films, regrouped (60 notes, was 47)
Added by the full read (13): Ad-Vanced 38 (neck, third try), 41b, 42c (arm round his back from behind), 57 (lying:
both arms on one side, no neck); Elder Swindon note 6 (lying arm curled); Islamocommunism 18 (rise too slow);
Terfwarts 7 (three-quarter turn), 15.1 (run arms, first try of 15.3), 17.2 (mouth); Halo 4 (head too small in the
helmet); Patriots 4 6 (pointing doesn't read), 19 (foreground pointing arm "terrible"); Patriots 3 11 (head snapped to
profile), 21 (arm with no hand from behind). Moved out: Ad-Vanced 51 (a painted portrait's neck, not a rig fault).

| Group | Notes | Where |
|---|---|---|
| **Hand on a prop or surface** | **10** | Islamocommunism 9, 11, 16, 19; Patriots 3 5, 9, 12, 18; Patriots 4 15; Ad-Vanced 47c |
| Elbow and arm shape | 8 | Ad-Vanced 16, 17; Terfwarts 15.1, 15.3, 14.6; Patriots 3 1; Patriots 4 19; MidTerminal 34 |
| Hand shape (fingers, pointing, hidden hands) | 7 | Ad-Vanced 37e, 39b, 42d; MidTerminal 33; Patriots 4 6; Terfwarts 9, 14.14 |
| **Shoulder-to-arm join** | **7** | Ad-Vanced 14, 18, 37c, 40, 41a; Patriots 3 17, 20 |
| Lying | 6 | Ad-Vanced 52a, 54c, 57, 58, 59a; Elder Swindon 6 |
| **Turned or seen from behind** (new group) | 5 | Ad-Vanced 41b, 42c; Terfwarts 7; Patriots 3 11, 21 |
| Standing, legs, bob | 4 | Ad-Vanced 15; Terfwarts 14.2, 14.3; Patriots 4 32 |
| Body through body (hits, steps) | 4 | Ad-Vanced 34, 36b, 37b, 54d |
| Neck and head fit | 4 | Ad-Vanced 37a, 38; Halo 2, 4 |
| Mouth | 3 | Ad-Vanced 52b; Terfwarts 14.1, 17.2 |
| Seated, rising | 2 | Islamocommunism 10, 18 |

- **Arms and hands: 34 of 60 (57%)** (the four arm groups plus 42c and Patriots 3 21). Still the first job.
- **New finding: the view causes faults across groups.** At least **9 of the 60** came from a body turned, seen from
  behind or drawn mirror-image: the new group's 5, plus Islamocommunism 9 (the mirror line swapped his hand),
  Terfwarts 14.14 (hands on hips read from behind), Patriots 3 17 and 20 (the shoulder from behind). Outside the
  60, Ad-Vanced 42e (turned faces) and MidTerminal 37 (pocket square mirrored) are the same cause. A front-on pose
  test alone would have passed all of them.
- **Lying is two films, not one** (Elder Swindon's man too), and the first fix of three lying notes failed.
- Repeats of a failed fix: 14 (was 13: add Ad-Vanced 38).
- Outside joints: likeness, faces and beards about 8; arm acting about 10 (taste, not faults); direction notes on the
  lying man (Ad-Vanced 55, 56) not counted.

## Cut list (revised; what the next jobs should spend on, in order)
1. **Job G, hands first:** grip and contact points (hand on prop or surface, 10) and the pointing finger (part of
   hand shape, 7). Then the automatic shoulder-seam test (rule 81, by hand, failed 4 times). **Every pose tested from
   the front, three-quarter, side, behind and mirrored** (9 notes the front alone misses). Then lying (6 notes, two
   films). Neck, mouth and seated (9 together) wait.
2. **Job F, the ledger keeps the evidence:** each round's pre-flight fault list (passed, caught, false alarm, could
   not test) and the check sheet's text are saved with the film, so catches stop living only in the chat.
3. **Job I:** the reading cut is bigger than first said: satire.md plus best-practice.md is 31k tokens, the rulebook
   11k. Sections marked so a chat can read one alone. The 25 by-hand and 24 never-mentioned rules are its list.
4. **Now, no build (Sam's Q1):** finished films' notes to the archive (Terfwarts, MidTerminal, Islamocommunism,
   Elder Swindon once posted; the sitting-kit notes).
5. **Habit, no build:** batch reads and checks into fewer steps.
6. **Small, for Job F's chat:** the cost watch's start figure (`FRESH` 90k) matches the measured 80k plus a little
   reading; leave it.

Estimate 0.7% of a week; first pass about 0.6%, this rerun about 0.7% (amber at the end, handed over).
