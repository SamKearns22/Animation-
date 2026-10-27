
# Handover replaced 27 Oct (planning chat)
## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/patriots-3-handovers.md)
- **Sounds are kept off GitHub:** `source/audio/patriots3-sfx/` (field artillery, battlefield ambience, distant shots,
  German "see enemy", German "fire at target"). First thing in the new chat: ask Sam to attach them again.
- **Done (27 Oct, building chat):** references filed; the Patriot rebuilt on the satire kit; the Gunner and the Loader
  (the brief's "spotter"); the MG42 as a 3D prop (belt, ammo box, flash, kick, falling cases); the bunker slit from
  three cameras; a silent firing test clip. Sam's one note (the Loader's reach read as a cuddle) is fixed. Sam's brief
  is in: `prompts/patriots-3.md` (word for word). No recordings yet.
- **Next: PLANNING, Opus high, fresh chat. Plan only until Sam says go.** Read `guides/satire.md`,
  `guides/film-quality-rules.md`, this file and the brief. Start `source/patriots3.py` from `source/satire_template.py`
  (reuse `patriots3_cast.py` and `patriots3_bunker.py`). Then in ONE message: the brief as a checklist (below), all
  questions with a recommended answer each, the missing references, the sound list, the ambition estimate (rule 24);
  then the plan in metres and the composition sheet (rule 11).
- **Points to raise at planning (my reading of the brief):**
  - New builds: the opening from high above the coast (black cliffs flashing with gunfire, artillery into sand and
    spray, six landing craft full of troops); the bunker's inside (back wall, the doorway the Patriot leans in, the
    room); the explosion hitting the lip of the slit and the soldiers stumbling back; the Patriot at the MG42 (gun pose
    for him); the camera in the slit facing in; the final push-in on the two soldiers' glance.
  - References still missing: a bunker interior with its doorway (from inside); the Normandy cliffs/bluffs from the sea
    or air; a person leaning in a doorway; the Nazi salute is in the brief (draw from a reference, ask Sam for one).
  - Bleep: "s***" (shit): ask whether he says the word or leaves a gap (rule 27).
  - Spelling on screen: the brief has "Furhër"; the usual spelling is "Führer". Ask which goes in the subtitle.
  - TikTok: a Nazi salute and "Heil!" may be limited or removed by moderation even as satire; ask Sam if he wants it
    as written, cut away mid-salute, or framed so it reads as the joke. Don't change it without his answer.
  - Voices: Sam records the Patriot, the Gunner's and Spotter's lines ("Who are you?", "Ah, you are with the
    Furhër?", "Heil!"). His two German game clips could cover the opening barks.
  - Sound effects the script names: machine-gun fire, artillery, the explosion, the howl of gunfire. Sam's three beach
    files cover artillery and ambience; there is no MG42 burst yet (ask).
  - Who says "Who are you?" (the brief doesn't say): recommend the Gunner.
- **Losses and my additions Sam should know about:** see "My additions" below (all still in).
- **Rule requests and proposals not yet in a guide:** none (searched this file: no "rule", "every film", "from now on",
  "proposed").
- **Files to open:** `prompts/patriots-3.md`; this file; `source/patriots3_cast.py` (people, MG42; `sheet`);
  `source/patriots3_bunker.py` (crew, slit, cameras; `sheet`, `clip`); `references/patriots-3/`.


# Handover replaced 27 Oct (end of planning)
## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/patriots-3-handovers.md)
- **Sounds are kept off GitHub:** `source/audio/patriots3-sfx/` (battlefield-ambience, distant-shots, german-angriff,
  german-see-enemy, german-fire-at-target). In a new chat, ask Sam to attach them again first thing.
- **27 Oct, planning chat (Opus):** Sam re-attached the five sounds (filed). `source/patriots3.py` started from the
  template (STORY: lines, nine shots, timings guessed; drawing below STORY still the template's); the plan in metres
  is `source/patriots3_plan.py` (`python3 source/plan.py patriots3 check`: clean); the rough composition sheet is
  `source/patriots3_compose.py` (review/patriots3-composition.jpg). Questions, sound list and ambition sent to Sam
  (below, "Planning"). **Waiting for Sam's answers and his go.** Plan only until he says go.
- **Next after his answers:** fold them in, then recordings (`python3 source/voices.py FILES` as they arrive) and the
  rehearsal clips (rule 8). Building is Opus high (new sets: the coast, the room's inside; new moves).
- **Rule requests and proposals not yet in a guide:** none.

## Handover to building (27 Oct, planning chat)
- **Sounds are kept off GitHub:** `source/audio/patriots3-sfx/` (battlefield-ambience, distant-shots, german-angriff,
  german-see-enemy, german-fire-at-target, explosion, mg42, rubble-slide). First thing in the new chat: ask Sam to
  attach all eight again.
- **Reference photos still missing (the photo sites are blocked here, 403):** a bunker inside looking back at its door;
  the Normandy cliffs (Pointe du Hoc) from the sea or air; a man leaning in a doorway, arms folded; a side-on photo of
  the salute (arm angle); a shell bursting on concrete (dust, debris). Ask Sam to attach them (or to allow the photo
  sites in the environment's network settings). Never draw these from memory (rule 3).
- **Done (27 Oct, planning, Opus):** Sam answered every question and said **go** (answers below, "Planning"). Plan in
  metres: `source/patriots3_plan.py` (check clean). Film file: `source/patriots3.py` (STORY in; drawing below STORY is
  still the template's). Composition sheet with Sam's notes 2-4 folded in: `source/patriots3_compose.py`
  (review/patriots3-composition.jpg; sent once, his notes applied, not re-sent).
- **Next: BUILDING, Opus high, fresh chat.** Read `guides/satire.md`, `guides/film-quality-rules.md`, this file. In
  order: (1) the rehearsal clips first (rule 8): the turn round; the front-on salute (arms foreshortened towards the
  lens, rule 21: the composition sheet shows the kit drawing it wrong, hands at the face) and the Patriot's flapping;
  the blast and stumble with debris settling (rules 32-33); firing from the slit with the push-in; (2) the coast (one
  painted shot: see "Usage" below) and the room's inside once the photos are in; (3) the Patriot's poses (lean, at the
  gun); (4) then `picture`/`scene` in patriots3.py on sets.Cam (copy power_crime / netan_yahoo's 3D pattern).
- **New rules (Sam, 27 Oct), apply from the start:** 38 front on by default (`plan.py` checks it from `SHOT_MARKS` in
  the plan; the views the shots demand are listed in patriots3.py's `THREE_QUARTER_OK`); 39 3D only when needed.
  For this film: 3D = the room (the shared `sets.house`, nothing new: six angles, people crossing it) and the MG42
  (already built). 2D = the coast (one painted shot in moving layers: craft, bursts, cliff flashes), the blast, dust,
  chips, muzzle flashes and room light, and the room's dressing (crates, range card, board marks as flat pictures).
  Ambition now about 15-20% of a week.
  Recordings come from Sam when he can (list below); `python3 source/voices.py FILES` as they arrive.
- **Rule requests and proposals not yet in a guide:** usage proposals 2 (a budget per film, logged at each handover)
  and 3 (the composition sheet sent once) from 27 Oct (below, "Usage"): waiting for Sam's numbers. Rules 38 and 39 are
  written (film-quality-rules, rule-register Q38, Q39).
