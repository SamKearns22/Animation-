# Job P: the ranked list (13 Nov, chat 2 of 8, Opus high), on the true week (WEEK_USD 171: 1% = $1.71)

The one aim: films at 15% of a week. Built from the real record: Blessed's 24 chats (app figures plus six estimated
11 Nov chats), its 63 notes (52 on animatics 1-2, N1-N11 on animatic 3), `notes/cost-diagnosis.md` (Jobs A-C),
`notes/preflight-audit.md`, the notes of the last 12 films (archive) and each film's own code. Nothing here trims a
joke or reuses old content (CLAUDE.md, Sam 13 Nov): every item makes new people, places and moves cheaper and surer.

## Where Blessed's $136.84 (80.0%) went
| cause | $ | % of a week | planned |
|---|---|---|---|
| Building people, places, moves before animatic 1 (six 11 Nov chats, estimated) | 36.05 | 21.1 | 10.5 (cast 4, sets 5, moves 1.5) |
| Walliams' face, five chats (app) | 31.74 | 18.6 | 0 |
| Chat 5, four stages bundled to 414k (app); ~$11 of it was size and a model switch | 27.73 | 16.2 | (in the rounds) |
| Notes rounds, fixes, clips, critique (nine chats, app) | 40.18 | 23.5 | 7.5 (animatic 1, two rounds, final) |
| Animatic renders on Sonnet (three chats) | 1.14 | 0.7 | |

**Sam's 63 notes:** about 24 were faults a check or a fresh eye could have caught (likeness 5: notes 1, 2, 25, 29,
47; people drawn wrong 9: blob press, inmates, ears, necks, missing mouths x4, the officer; bodies and arms 7: lying,
van limbs, elbow sniff, strangle hands, N1, N8, N10; sets 3: wall pop-in, Bible and pillow, chairs). About 39 were
taste and direction (staging, camera, acting, script, music), which no tool should remove. Repeats: 29, 32, 45, N1,
N6, N8, N11.
**The last 10 films:** their own code averages ~3,800 lines a film (Blessed 5,498; Remakes 6,817; Ad-Vanced Notice
5,524; Flying Whales 4,444; Elder Swindon 3,817; MidTerminal 2,942; Islamocommunism 2,551; Patriots 4 2,424; Halo
2,239; Terfwarts 2,002); about half is people and places. The people kit lives inside old films' files (Blessed's
cast imports Ad-Vanced Notice's, which imports MidTerminal's). Arms and hands are the busiest note subject in every
people film (Ad-Vanced Notice 65 mentions, Prepper 47, Elder Swindon 34, Patriots 3 30); likeness notes appear in 9 of
12. Older films' costs on the true week are not recorded, so their savings are not priced here.
**Already done (not ranked):** Job C 1-6 and the pre-flight audit cover chat 5's waste (~$11, 6.4%) and the caught
-but-waved faults N1 and N8 (~$11, 6.4%): about 13% of Blessed. Renders stay off the list: $0.3-0.5 each on Sonnet.

## The ranked list (by saving for each % spent, then by what it needs first)
Headline: **describe, don't code.** A new person, place or common move becomes a short description the engine draws
from tested parts (items 2, 4, 5, 7); staged people first. Savings: "Blessed" is measured from its chats above;
"typical" (3 new people, 2 places) is an estimate. Each tool is built at the stage of the next film that needs it,
with that film's own things as its test, so part of its cost is that film's own stage.

| # | job (heading) | closest rule / tool; what is new | build | saves: Blessed / typical | pays back | Lost |
|---|---|---|---|---|---|---|
| 1 | **A rough of every new thing** (catch faults before Sam) | Rule 11 (3-4 key shots, sent once); Protest Tiers' "pencil sketches" request. New: every new person, place and move gets a rough on one sheet before it is built (Sam: Y, 13 Nov) | 0.5% | ~4% (notes 4, 5, 20, 22, 32, 39 were rebuilds) / ~2% | under 1 film | none. Added: one sheet per film for Sam |
| 2 | **Likeness in one sitting** (people) | Rule 49, `likeness.py`, `nametest.py`, `beardkit.py`. New: one command makes three heads that differ on the card's unsure measures (Walliams' nose), beside the 3+ photos at phone size, with the name test; Sam picks one (item 1's rough) before any film wiring | 3% | ~15% (Walliams $31.74 in five chats -> about one chat) / ~3% a film with a famous face | 1 film | none |
| 3 | **Critique test bench; Sonnet as the critic** (catch faults; tools that work less hard) | Rule 89, `critique.py`, `guides/critique-checklist.md` (already built from Sam's notes). New: replay saved sheets from past films (Blessed animatics 1-3, Remakes, Elder Swindon) with Sam's real notes as the answer key; score Opus and Sonnet on the same packs; switch only if Sonnet catches as much; every missed note improves its checklist line. Protest Tiers' three proposed checks are tested here as lines | 1.5% | ~3% (critique ~a quarter of each build chat, ~$10 on Blessed; Sonnet ~half a word) plus whatever more it catches / ~2% | 1 film | the Opus critic, only if Sonnet scores as well |
| 4 | **People from a description** (people, stage 1) | `views.person`, `turnhead`, `lying`, `sitting`, pose gallery, rules 38, 41. New: one people kit lifted out of the film files; a person is ~15 lines (height, build, face card or invented, haircut, wardrobe pieces, things held, moods), drawn in every view with mouths, necks, ears and hands by default, cast sheet and checks free. First test: Protest Tiers' cast | 8% (3-4 chats; Protest Tiers' 3% cast inside it) | ~8% (cast code 1,661 lines -> ~150; the nine people notes) / ~4-5% | 1-2 films | none of the look; a person the kit can't describe still gets code, then joins the kit |
| 5 | **Places from a description** (places, stage 2) | `sets.py` (plan rooms in metres), rules 1, 2, 3, 5, 83. New: a place is rooms in metres plus a furniture and dressing library (seats, tables, beds, booths, desks, doors, TVs, signs), each a 3D box painted flat from any camera; rule 3's 8-10 things listed as items; every object is in the collision and pop-in checks without hand-made boxes (N8's kind) | 8% (3-4 chats) | ~7% (sets 1,491 lines; set notes) / ~3-4% | 2 films | hand-painted one-off views stay where the library has nothing |
| 6 | **A round reads a page, not a film** (reading less) | Rules 61 (MAP), 48, 19, `round.py`, rule 85. New: after 4, 5 and 7, a note changes a line in the film's description file (a few hundred lines in all), not 2,000-line code; round chats start near 100k, not 130-150k, and stay under 200k | 0.5% | ~6% (Blessed's nine round chats, $40, a third cheaper) / ~3% | under 1 film (after 4, 5, 7) | none |
| 7 | **Moves from the acting list** (moves, stage 3) | Rule 74 (acting list), `moves.py`, `perform.py`, `patriots3_act.py`, pose gallery. New: each acting-list row (face, body, the word it lands on) becomes named moves timed to the voice; a film's shot code is the list plus camera lines | 6% (2-3 chats) | ~2-3% / ~2% | 3 films | hand-tuned one-off moves stay as code where the library lacks them |
| N | **Honest fit at planning** (Job N) | Rule 24 (estimate, budget stop), `ledger.py estimate`. New: the plan says whether the film fits 15% on the true week, why not (people, places, a likeness face), and which items above close the gap; rule 24's size budgets restated (set on the old ruler) | 1-2% | no direct saving: stops surprise overruns (Blessed planned 19%, spent 80%) | n/a | none |

**Job N is not first.** It saves nothing by itself; it belongs at the start of the next new film's plan (Protest Tiers
is already planned), where it names the items above that film needs.

## Order and stages
- **Stage 1 (now, ~13%, partly Protest Tiers' own cast):** 1 (rule wording on Sam's Y, this chat), 3 (Opus medium,
  one chat), 4 built with Protest Tiers' cast as its test (Opus high design, medium build), 2 at the next film with a
  famous face.
- **Stage 2 (~8%):** 5 at the next film's sets (Protest Tiers' streets if timing fits).
- **Stage 3 (~6.5%):** 7, then 6.
- **All built: ~29% of a week**, partly paid inside films' own stages.

## What a Blessed-sized film would cost with everything done
80% (real) -> 67% (already done: Job C, pre-flight audit) -> 52% (2, likeness) -> 44% (4, people) -> 40% (1, roughs)
-> 33% (5, places) -> 30% (3, critic) -> 28% (7, moves) -> **about 22%** (6, rounds): **20-26% of a week** for
7 new people, 8 places and a new famous face. **A typical film (3 new people, 2 places, no new famous face): about
15-18%.** So 15% is in reach for a typical film and not for one of Blessed's size; Job N says so at planning.
Uncertain: the 11 Nov build split is estimated (the app can't show those chats); each saving is about +-30%.
