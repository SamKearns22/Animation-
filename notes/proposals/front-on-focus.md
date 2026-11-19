# Proposal: Turned people lose detail, and better tools sit unused

Status: adopted (2026-11-19)

## Problem
Two linked faults, both against statement one (high quality, fewer notes and faults, a film within 15% of a week).

1. People seen turned (three-quarter, side) are the weakest drawings on screen: details go missing, necks look
   sunken, and the person stops looking like their front self. Sam (19 Nov): "our weakest post in terms of model
   quality, with weaker details, sunken necks". Sam (17 Nov): "our 3/4 characters still look like shit compared to our
   other poses". Sam would rather people stay posed towards the camera with the drawing showing a focus to the left
   or right, as BoJack Horseman does all the time, and as Milburn did for Pat in chat 11. The aim is every future
   character, not the four Milburn people.
2. Milburn's four invented people (goth, Swindon lad, thin lad, shy girl) and Milburn himself were drawn through an
   older, weaker route while the better one (the face tool's house head, about 17 chats of work) sat beside it.
   Sam (19 Nov): "We should always use our best tools and it's concerning that you found and chose a weaker tool.
   Could this be a systemic problem? Are expensive fixes and tools sitting unused and ignored throughout our two
   months of making films?" and "if weaker tools, processes and checks that we have long disregarded are sitting
   throughout our tools, confusing our system and creating waste, I'm not sure why they shouldn't be found and deleted
   so that we only have our best and most effective work all the time. Everything must be working towards statement
   one at all times." Sam's limit (CLAUDE.md): a step is removed only if it caught nothing in three films, with his Y
   on a "Lost:" line; nothing is deleted by this chat.

## Facts
**What BoJack does (labelled sheet: front-on-focus/bojack-sheet.jpg, 10 episode stills from TVmaze, human
characters).** Bodies stay square to the lens even when two people talk side by side (5x01, 6x02, 6x14). Direction is
carried by: both pupils pushed hard into the same corner of large eye whites (1x09, 3x06, 6x06); the head tilted on
the neck (2x12); the nose pointing toward the focus while the face outline stays near front (5x03); the features
nudged a little toward the focus inside a near-front outline; brows uneven, one up, one down (6x06, 4x04); the mouth
pushed off centre (4x04); a hand pointing or an open palm toward the focus (2x12, 5x03, 6x02). The most a human turns
is about 15 degrees (6x07), and glasses, beards and hair keep their front design while doing it.

**The Andy and Kemi test (front-on-focus/andy-kemi-test.jpg and andy-kemi-whole.jpg; scripts fronton.py, slide.py in
the same folder; neither person changed).** Drawn with the kit as it is: (a) NOW, turned 45 on the house head: Andy's
far lens edge and ear sit oddly at the cheek line; Kemi's braids become a blocky cap, her open collar narrows; on the
Milburn copy of Andy (whole sheet) his thick glasses turn into thin wire rims at 45. (b) Front, eyes only (`look`
0.9): the direction reads on Kemi (white eye whites), weakly on Andy (his glasses frame the eyes). (c) Eyes plus head
tilt (`head_roll` 6): reads clearly left or right on both. (d) A picture-warp mock of the features sliding toward the
focus inside the outline (not a kit piece): the strongest read of "looking right"; but the warp bends Andy's glasses,
so a real version must move whole pieces (eyes, nose, mouth, glasses), not warp pixels. `lean` front on did nothing
visible. The engine snaps every turn to 0, 45, 90, 135, 180 (source/views.py `snap`, VIEWS line 34): there is no
10-20 degree turn; there are no uneven brows, no off-centre mouth and no feature slide on any front head
(people_parts.front_head, facehouse front, people_famous; grep this chat).

**The famous heads turned today (front-on-focus/famous-turned-now.jpg, `facehouse.py turns`, 19 Nov; Sam asked for the
current one, not the 15 Nov picture).** Burnham, Badenoch, McFadden, Walliams at front, 3/4, side, 3/4 behind,
behind. Seen: glasses thin to a line on the far side at 3/4 and side (Burnham, McFadden); hair becomes flat grey or
brown slabs from the side and behind (Burnham's sides, McFadden's fringe of hair, Walliams); from behind the neck is a
long tube standing off the jaw (the "sunken neck"); Walliams' stubble a pale smear at 3/4; Kemi's braids a mass at side.

**Rule 38 already says front on.** guides/film-quality-rules.md row 38: "Front on by default (each person within about
25 degrees of the lens). A three-quarter view is a last resort (Sam, 3 Nov): only when no other way makes the shot
work, listed with that reason." Its check: plan.py `front_faults` reads the PLAN's facing for each SHOT_MARKS person;
the drawn angle is checked only for a film with no rooms plan (preflight.py line 409, posecheck `set_marks`). Milburn
has a rooms plan, so its drawn YAW3 = 40 (milburn.py line 478, scenes 3 and 6, 11.9 s of the film) passed with no
THREE_QUARTER_OK line. The comment there: "Sam (chat 6, the BoJack frames): turned three-quarter to screen right, the
camera at their side". Sam's chat 6 words (notes/archive/milburn.md line 243): "see them from the side rather than
from directly on"; "move that camera to their side"; "their focus is to something on the frame's other side".

**Why the four (and Milburn himself) were not on the house head (Sam's question d).** Searched: notes/archive/
milburn.md, milburn-handovers.md, story/milburn-people.txt, and the Milburn plan chat's transcript (session
"Milburn screenplay", 17 Nov). No reason was ever recorded for the four. What the record shows:
- The plan chat's estimate table: "Alan Milburn ... NEW (people kit, `head: measured`)"; "4 NEETs ... NEW (people kit
  lines)". The words "facehouse", "house head" and "face tool" do not appear anywhere in that chat.
- It read people.py's MAP (lines 1-60, its own tool call). That MAP lists invented lines, `head: measured` (Brand's
  way) and `head: part walliams`, but not `head: house` (the house head is parsed at people.py line 361 and documented
  only in facehouse.py's MAP, "IN THE PEOPLE KIT (chat 11)").
- story/milburn-people.txt line 2: "Milburn is drawn as an invented head with the likeness card's pushes (x1.6)
  because the measured-head kit has only long curly hair (Brand's)". So for Milburn, a famous person with photos, the
  chat compared only against the older measured head, not the house head; Andy and Pat in the same film were on the
  house head (chat 5).
- guides/kit-catalogue.md line 68 names the house head "A famous person's head for any film, READY"; line 44 names
  the people kit "People from a description". The catalogue sorts by who someone is (famous or invented), not by
  which route draws best.
- The house head needs a face tool pick (references/faces/NAME/pick/NAME-pick.json: measures from photos, Sam's pick).
  An invented person has no photos, so today there is no input for it. Its hair pieces are `swept`, `braids`, `bald`;
  the people kit's cuts (shag, crop, long with fringe, streaks), pencil moustache, piercings and eye bags exist only on
  the people-kit front head (people_parts.front_head) and partly in people_turned.py (its MAP: 'shag' -> 'long').
- The 18 Nov proposal (notes/proposals/three-quarter-people.md) noted "Famous people (Andy, Pat) use facehouse's house
  head turned through turnhead" and chose one source per view; its steps 2 (torso) and 3 (cast sheet tile) still wait.

**Light survey: which tools the films use (this chat, 19 Nov; import map over source/, counting only drawing paths,
not checks; 39 film files; CLI tools that chats run by hand counted from guides and notes).** Note: the people kit
was approved for films on 16 Nov and the places kit on 14-16 Nov, so only the last two or three films could use them.

| stage | routes there | best now | used by (films) | weaker, superseded or unused |
|---|---|---|---|---|
| people: heads | house head (facehouse + facepick, likeness, beardkit, agelines: ~4,750 lines) / people kit invented lines (people_parts) / `head: measured` (people_famous) / `head: part walliams` (people_walliams, blessed_walliams) / per-film cast files (36 `*_cast.py`) | house head for detail; people kit for invented | house head: milburn (Andy, Pat), protest_tiers; people kit: milburn, protest_tiers; per-film casts: all older films | `head: measured` (superseded by house head; still read by Blessed's finished frames); `head: part walliams` (test only, its MAP says); per-film cast files (each older film's own people) |
| people: turned | turnhead (3D head) through facehouse (famous) / people_turned (invented) / views engine plain head | none is good enough (picture above) | turnhead: 6 films; people_turned: milburn, protest_tiers | people_turned loses parts (18 Nov proposal); the engine's plain turned head |
| people: bodies | figure + views + limbs (engine) / mhuman, rig, character, clothes, hair, sdf3d (3D MakeHuman stack) / hands3d | engine | engine: all films | 3D stack (~4,000 lines: sdf3d 1191, mother 456, shot 427, mhuman 394, graphite 392, hair 362, rig 312, daughter 284, kitchen 270, props 260, mh_lab 202, checks 178, character 173, clothes 137, horror_preflight 117, materials 90): 0 film files; hands3d "retired" (guides/figure-rig.md line 137) yet still in source |
| places | places kit (places, places_parts, places_rooms, places_tables, places_outside) / `sets` / per-film `*_sets.py`, `*_set.py`, `*_room.py` | places kit | places kit: milburn only (it reuses remakes_sets and blessed_sets as parts); sets: 10 films | per-film set files: finished films still render from them |
| props | places kit parts, held props per film, `props.py` (3D stack) | unclear (no props kit) | per film | props.py belongs to the 3D stack |
| effects | prepper_fx (used by 4 films, catalogue), flying_whales_fx (3), per-film `*_fx.py` | none named as best | per film | effects live in film-named files; no effects kit |
| movement and acting | moves kit (moves, acting, headlife, sitting, lying) | moves kit | moves: 19 films; headlife 4; acting via milburn | `duel` (1023 lines, 0 films), `series` (professional only) |
| sound | mossad_audio (cleaning; reached by all films through the engine), voices (timing, 4 films) | mossad_audio | all | the house cleaner is named after one film (findability) |
| finishing / posting | finish.py, signoff.py, follow_line.py | finish.py | every film (CLI) | none found |
| checks | preflight, kitchecks, audit, critique, posecheck, handcheck, clipcheck, viewchecks, plan, rough, page | preflight gate | every film (critique, rough, page called only by preflight and tests, not film code) | 48-61 "named, not settled" pre-flight lines carried through Milburn; kittests facehouse_whole_head and round_page red since 15 Nov (handover.py start, this chat); rule 38's drawn-angle check skipped when a film has a rooms plan |
| labs and one-offs | trial_lineup 886, trial_link 730, ll_looks 940, protest_tiers_roughs 699, ai_tells_lab 476, park 451, ed_variants 361, concept_mother 323, horror_trailer_music 944 | n/a | 0 film files | unused by any film; trial_lineup/trial_link named in notes (trial_lineup.md, trial_link.md) |

Unchecked: whether any finished film in animations/ would need a re-render from a 0-film tool (the 3D stack's films
"mother" and "daughter" are not in source as satire film files; unchecked whether they are posted); how many lines
in the 39 film files are copies of kit pieces.

**Cost record.** Milburn: 22% of a week (Sam, from the app) against the 15% aim; the 3/4 fix chat 3.6% (1.4 of it the
route's helpers and judge); turned people on screen 11.9 s of 65 s (notes/proposals/milburn-review.md section 2).
The kit catalogue lists things, not capabilities in a best-first order (guides/kit-catalogue.md, 156 lines).

## Record
notes/proposals/front-on-focus/bojack-sheet.jpg
notes/proposals/front-on-focus/andy-kemi-test.jpg
notes/proposals/front-on-focus/andy-kemi-whole.jpg
notes/proposals/front-on-focus/famous-turned-now.jpg
notes/proposals/front-on-focus/fronton.py
notes/proposals/front-on-focus/slide.py
notes/proposals/three-quarter-people.md
notes/proposals/milburn-review.md
notes/archive/milburn.md
notes/archive/milburn-handovers.md
notes/ledger/sam/h3akq5qv.md
story/milburn-people.txt
story/facetool-people.txt
guides/film-quality-rules.md
guides/kit-catalogue.md
guides/figure-rig.md
guides/job-packs.md
source/people.py
source/people_parts.py
source/people_turned.py
source/facehouse.py
source/turnhead.py
source/views.py
source/plan.py
source/posecheck.py
source/preflight.py
source/milburn.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 3dd21481eea1d2c2 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the facts lean to one build. Test (d) is called "the strongest read" and the file says "a real version must move whole pieces (eyes, nose, mouth, glasses), not warp pixels", which is a design spec; the survey table pre-sorts every stage into "best now" and "weaker, superseded or unused". Sam's own wish (front on, focus shown in the drawing, BoJack, Pat in chat 11) is his brief, not a leak. Also: V1 and V3 both say they glimpsed the chat's own idea (V2) while listing the folder; both named it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 3 | 4 | 4 | 19 |
| V2 | 4 | 3 | 3 | 2 | 3 | 15 |
| V3 | 4 | 5 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes, once patched. An expert closes the hole the fault came through (the angle check skipped on films with a rooms plan, preflight.py 409), gives the front head a way to show direction so turning is not needed, and guards the place the route is chosen (the plan's estimate table). V3 does all three; the patch puts focus on both front heads and keys the route guard to "famous person with photos" so it would have caught Milburn himself.
Q2: Evidence is wide enough for the decision: Sam's four turned-people notes (14, 17, 18, 19 Nov, ledger checked), the Andy and Kemi sheet, the survey of every stage. The blind route-pick test measures the systemic question directly instead of guessing it.
Q3: Root cause found with evidence (the check hole; turned heads rebuilt in 3D lose the front design, why the 18 Nov fix failed; the plan chat read a MAP that omits `head: house`). Enforced by pre-flight refusals and kit tests, not by a chat choosing to read. Success numbers: 0 unreasoned turned seconds (Milburn 11.9); a blind judge names left or right 10 of 10 at phone size; Sam picks focus over today's 45; the route test re-run scores every pick best.
Q4: Four different approaches weighed (rebuild the 3D turn, stage front on with a focus vocabulary, one head for everyone, learn first); the costly route that already failed is rejected with its reason.
Q5: Each change is its own numbered yes; focus is shown on a sheet before it reaches a film; retirements are archived, never deleted, each with its own Lost line. Weak spot: the focus piece touches two heads every film uses; its kit test and Blessed's pixel-match replicate guard old films.
Q6: Sources named and checked (rule 38 row, preflight 409-410, views.py 34, people.py MAP and line 361, catalogue lines 44 and 68, ledger quotes). Costs are estimates, not ledger figures: named.
Q7: Sized by the result: whole-piece focus, not the free eyes-only fix that reads weakly on Andy's glasses; route guard on every stage, not people only.
Q8: The learn steps are measurements, not trials; every change is permanent on Sam's yes and reviewed at the film's end.
## Pick
V3
## Why
V3 and V1 share the shape (learn, close rule 38's hole, a focus piece, a route guard, retirements one line each). V3 wins on three things: it explains why the 18 Nov fix failed (the 3D rebuild loses designed qualities, a rule 30 answer); its route guard covers every stage and sits where Milburn's choice was made (the estimate table); and its success numbers are blind and measurable. V1's guard ("a face-tool pick drawn on `head: measured`") would not have caught Milburn, who had a likeness card but no pick. V2 has good ideas but names tools for retirement before any count, bundles six changes, and sets no number to beat.
Taken in: focus on BOTH front heads, house head and people kit, from V1 and V2 (V3 left invented people without focus unless C4 passed, though "every future character" is the aim); the kit test "every part drawn at full focus, nothing warped" from V1; the shallow 10-15 degree turn drawn by the front head itself, never the 3D head, from V2 (BoJack's most is about 15); "focus, not turn" in the acting list from V2. Mine: C1 and C2 do not wait for the counts (rule 38 is already Sam's decision); the route guard keys on "has photos or a likeness card".
## Faults in the pick
- F1 [fixed] Focus only on the house head left invented people out; now on both front heads.
- F2 [fixed] The route guard would not have caught Milburn (no pick made); it now refuses a person with photos or a likeness card unless on the house head or listed with a reason.
- F3 [fixed] Closing rule 38's hole waited behind the learning; it now goes first.
- F4 [named] Costs are estimates, not taken from the ledger's real costs.
- F5 [named] Kittest facehouse_whole_head is red since 15 Nov (Sam: it covers only Andy and Kemi); the focus build must leave it green or say why.
- F6 [named] Unchecked whether any posted film renders from a tool up for retirement; archiving, not deleting, covers it.
## Final version
Learn (changes nothing, about 1% of a week, Sonnet):
- L1: for Milburn and protest_tiers, turned seconds, Sam's notes on them, and which turns a walk, exit or back truly needed (sets C1's exception list).
- L2: blind route-pick test: a fresh helper gets the planning pack and three briefs (people, places, effects, movement), records the route it picks per stage, scored against the best route. Baseline for C3.
- L3: one invented person (the goth) on both front heads, one sheet; Sam picks. Decides C4.

Changes, each its own yes:
- C1 (now, about 0.3%): pre-flight reads the drawn angle on every film, rooms plan or not. Anyone past 25 degrees without a THREE_QUARTER_OK reason stops the animatic. Side and behind stay for walks, exits and backs. To beat: 0 unreasoned turned seconds (Milburn 11.9).
- C2 (now, about 2%): a `focus` setting (-1 left to +1 right) on the house head and the people-kit front head. It moves whole pieces: both pupils into the corner, eyes, nose, mouth and glasses slid a little inside the unchanged outline, the nose tip turned, brows uneven, the mouth off centre, a tilt up to 6 degrees, and up to 15 degrees of shallow turn drawn by the front head. Glasses, beards, hair keep their front design. A move in the moves kit (eyes lead, tilt follows, gesture last); the acting list says "focus, not turn" for listeners. Kit test: every part drawn at full focus, nothing warped; old films' frames unchanged. Shown first on Andy and Kemi, then an invented person. To beat: blind judge 10 of 10 left or right at phone size; Sam picks it over today's 45.
- C3 (after L2, about 0.7%): one best-route line per stage at the top of the kit catalogue and each tool's MAP (people.py's MAP gains `head: house`). The plan's estimate table names a route per item; pre-flight refuses a superseded route, and a person with photos or a likeness card off the house head without a reason. To beat: L2 re-run picks the best route every time.
- C4 (only if L3 favours the house head, about 3%): a description-to-pick route so invented people use the house head; people-kit cuts move onto it.
- C5: from L2 and the ledger, each route unused in three films goes to Sam as its own line with a Lost line; archived, not deleted.
## For Sam
### Option 1: Face the camera, show the look, guard the best tools
People stay facing the camera and show where they look the BoJack way: eyes, brows, mouth and nose pushed toward the focus, a small tilt, a hand, at most a slight turn drawn on their own front face, so glasses, hair and necks keep their front detail. The check that let Milburn's turned people through is closed on every film. Every stage gets one named best tool, and the planning step must name it or say why not. First a short test of which tools a fresh chat picks, and a sheet of the goth on both heads for you to choose. Unused tools come to you one line each.
Lost: the true three-quarter look in new films, unless a reason is written; about 4% of a week once (3% more if invented people move to the house head).
Added: front-quality detail in every talking shot, direction that reads on a phone, and no film picking a weaker tool by accident.
### Option 2: Build it all in one go
The same focus on every front head, plus the slight turn, the best-tool table, invented people moved onto the house head, and a named list of tools to retire, all at once without measuring first.
Lost: the measuring that shows which tools are really unused, and separate yeses; about 6% of a week.
Added: everything sooner, but some tools may be retired that a film still needs.
