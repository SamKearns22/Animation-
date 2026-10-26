# Notes for Netan-Yahoo! (brief: `prompts/netan-yahoo.md`; code to come: `source/netan_yahoo.py` from `source/satire_template.py`)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/netan-yahoo-handovers.md)
- **Done (26 Oct):** brief saved word for word; the kit checked for what can be reused. Nothing built, no pictures made, no render.
- **Next (stage, model, fresh chat):** PLANNING, Opus, high effort, new chat. Read this file, `prompts/netan-yahoo.md`,
  `guides/satire.md`, `guides/film-quality-rules.md`, `guides/kit-catalogue.md`. Send Sam the questions below in ONE message and
  ask for sound effects and references. Plan only; build nothing until Sam says go. Then BUILDING (new characters, new set,
  new effect): Opus, high effort, another fresh chat.
- **Found in the kit (26 Oct):** no Netanyahu, no Israeli news studio, no newsreader, no Darth Maul, no lightsaber or
  clean-cut effect in `guides/kit-catalogue.md`. The brief says the cast and set are "already built"; I could not find them.
  Closest reuse: reporters (`press_secretary.py`), steam (`prepper_fx.py`), the movement toolkit for the leap and roll
  (`moves.py`, `views.py`), the satire audit. Sam to say which film holds them, or they are new builds.
- **Losses and my additions Sam should know about:** none yet. Proposed additions (Sam to say no): presenter glances at the
  camera (his, shot 4: kept); a studio "ON AIR" light and desk props; a stinger on the logo; steam hiss under the chunks.
- **Ambition estimate (rule 24-26, a guess to confirm at planning):** new Maul, new presenter, probably new Netanyahu and
  studio, a lightsaber effect and a hard fast-action body-cut sequence: about 20-30% of a week, NOT the 10% Sam asked for
  elsewhere. Cheapest cuts: reuse any existing Netanyahu and studio; keep the cut to 3 strikes; one wide shot for the action.
- **Rule requests and proposals not yet in a guide:** none in the brief or notes.
- **Files to open:** `prompts/netan-yahoo.md`, this file, `story/status.md` (the Netan-Yahoo section only).

## Questions for Sam (one message, at planning; pick defaults myself where he does not mind)
1. **Cast and set "already built":** which film are they in? I cannot find Netanyahu, the studio, a presenter or Maul. If
   they do not exist: please send references (below) and say OK to build them new.
2. **References wanted:** Netanyahu (3-4 photos, face and usual suit); Darth Maul (face tattoos, horns, hood, robe, double-bladed
   saber); the presenter (age, hair, suit, mic?); an Israeli TV debate studio (desk, screens, lighting); the Hebrew words below.
3. **Hebrew text, exact wording** for the screens: the "News" logo (a made-up channel name, not a real channel?) and
   "Presidential Debate 2026". Correct Hebrew from you, so the letters are right and read right to left.
4. **"Presidential" and "President Netanyahu":** he is Prime Minister in real life (the President is a different office).
   Keep as written for the joke? (default: keep.)
5. **Seating:** the idea says everyone standing with chairs behind; shot 2 says Netanyahu "in his chair". Which? (default:
   all three stand behind their chairs in shots 1-4; Netanyahu sits in shot 5? or stands throughout.)
6. **"ignores his twin lightsaber":** do you mean "ignites" (he lights it up before the leap)? (default: yes, ignites mid-leap.)
7. **The cuts:** how many strikes, and where? (default: three: diagonal across the torso, one arm, the legs; pieces fall behind
   the desk into a pile.) No blood: clean, dark, glowing cauterised edges and steam, no insides shown (default).
8. **Sound effects** (script names them): lightsaber ignite and hum, swing whooshes, slice sizzle, leap and landing, chair
   thump as Maul lands on it, steam hiss, studio ambience, a news sting? Will you record or send them, or shall I make them
   in code? (Star Wars sounds are copyright: any you send stay off GitHub, as with the song in Shocking Behaviour.)
9. **Bleep:** Sam said the word is SAID and bleeped at the S (rule 27, said not gap). Subtitle "S*** he's good" (default).
   Bleep sits on the "S" only.
10. **Title and sign-off:** no title (default); Hook Text "Israeli Presidential Debate"; CranbriJoos sign-off at the end.
11. **Length:** about 50 words of dialogue (about 15 s) plus the action: expect 28-35 s. First payoff by 8-10 s is the
    stare at the end of shot 3. OK?
12. **Recordings:** dialogue arrives later today. Stand-in voices time the animatic only and are never sent to Sam.
13. **Likeness:** Netanyahu and Maul as flat cartoon likenesses in the series style (circle hands). The presenter is a new,
    younger, energetic man: skin, hair, suit and glasses by default are my pick; I will say what I chose.

## Plan extras (film-quality-rules 24-26): eyelines and holds per shot; every sound effect (what, when, needed by);
bleeped words (said, or a gap left?)
- Bleep: the word is said, bleep on the "S" (Sam's brief). Sound effects: see question 8; none until Sam answers.
- Eyelines: shot 1 presenter to audience; shot 2 Netanyahu to presenter; shot 3 Maul to presenter, held and still; shot 4 all
  to presenter, then the presenter's eyes flick to the camera and back; shot 5 Netanyahu looking at Maul's chair (to confirm).

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py FILM sketch OUT.jpg`); places benchmarked against
references in `BENCHMARK` (rule 3, `python3 source/benchmark.py FILM OUT.jpg`)
(To do at planning: one studio set, screens upstage with the Hebrew text, three chairs, presenter's chair apart.)

Composition sheet sent: (rule 11: the 3-4 key shots, before building; write the date and file here once Sam has it.
Pre-flight refuses to run until this line has them, and while any "done?" box below is blank: rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note | done? |
|---|------|------|
| 1 | Satire style, TikTok; follow satire.md and film-quality-rules; start from `source/satire_template.py` | |
| 2 | Plan only until Sam says go; nothing built or shown before sound effects and references are requested and questions asked | |
| 3 | Israeli news presenter, younger and more energetic than the built one, serious in role | |
| 4 | Introduces two candidates in a "presidential debate"; everyone standing, chairs behind them | |
| 5 | Netanyahu introduced as "liberal moderate gently-gently incumbent President Netanyahu"; nods in acknowledgement | |
| 6 | Darth Maul introduced as "Sith Lord and Scourge of the Galaxy"; glowers from under his hood; bloody-eyed menace | |
| 7 | Presenter asks Maul about the West Bank; awkward silent beat while Maul stares | |
| 8 | Presenter's eyes flick to the camera briefly, then back | |
| 9 | Maul (ignores/ignites) his twin lightsaber, leaps acrobatically, forward roll, lands in a predatory crouch | |
| 10 | Presenter alarmed; Netanyahu mildly surprised | |
| 11 | Maul slices the presenter into a pile of steaming chunks: fluid, fast, cuts match where the strikes land | |
| 12 | Maul steals the presenter's seat, leaps on it like a cat guarding territory, menacing and triumphant | |
| 13 | Netanyahu, surprised and a bit impressed: "Shit, he's good"; subtitle "S***", said in audio, bleep at the S only | |
| 14 | Shock level 3; gravity, nothing fully cartoony; no blood; clean cuts; accurate lightsaber sound effects and visuals | |
| 15 | Screens in the background: News logo and "Presidential Debate 2026" in Hebrew | |
| 16 | Shot 1: zoom in across the studio to the presenter, mid-large to mid-close | |
| 17 | Shots 2, 3, 5: same close shot on Netanyahu; shot 3 is Maul staring still at the presenter (as written) | |
| 18 | Shot 4: mid shot with all three and the presenter's chair | |
| 19 | Hook Text: "Israeli Presidential Debate"; CranbriJoos sign-off at the end (standing rule) | |
| 20 | Dialogue recordings arrive later in the day | |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|---|---|
| (none yet: requested) | | |

## Notes from Sam (numbered; mark each done as it is fixed)
| # | shot | time | note | status |
|---|------|------|------|--------|
