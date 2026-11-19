# Proposal: Turned people lose detail, and better tools sit unused

Status: open

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
