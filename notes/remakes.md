# Notes for REMAKES (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (one critique round of every changed shot, with the fresh-eye helper: still not run),
  30 (note 58 is a changed decision; 44/57 missed the Job K head-acting rule), 85 (Sam's usage resets 3:41).
- **Done (11 Nov, Opus):** notes 43, 44, 45, 50, 51, 52, 57, 58 fixed; 3 clips sent (S1-S4, the snap, the wall).
- **Next (Opus, medium): notes 46, 47, 48, 49, 53, 54, 56 in order**, clips of each moved beat, then the critique round
  (fresh-eye helper), then open the Sonnet chat for the animatic. Type: "Remakes: read notes/remakes.md Where things
  stand. Do the open notes, then hand to Sonnet."
- **Needs Sam:** his look at the 3 clips; rule request below.
- **Read:** pack "Notes round" in `guides/job-packs.md`; source/remakes.py MAP.
- **Open rule requests:** none (11 Nov: Sam Y to the head-acting check; written into rule 74, preflight.head_life_faults).
- **For Claude:** HL['kg'/'link'] (headlife from the takes) in remakes.py; Link gets it in _kid; KG mood may be a dict
  (CR.kg); eyes='shut' blinks; RS.kg_on_branch(sway=); draw_subtitle/_pieces (note 51); camp work: _camp, _kg_camp.
  Note 54 (KG in the camp) should use HL['kg'] too. Clips in clips/ are drafts (not on GitHub).

## Open notes: animatic 1 (Sam, 10 Nov; Sam's numbers 1-6, then Claude's list Sam asked to be done)
| # | note | plan |
|---|------|------|
| 40 (Claude 1, 3, 5) | rehearsal clips; a critique round; watch and listen to the animatic before sending | clips of the snap, the camp burst, Navi's blast, the wall lift; one critique round; check the bleeps and gunfire against the voices | | **PART DONE 10 Nov:** clips made and sent (snap, wall lift; camp earlier). Critique round done 11 Nov. Still to do: watching and listening to animatic 2 before it is sent |
| 41 (Sam, 11 Nov) | at the wall Link stares, absolutely terrified, into KG's eyes | **DONE 11 Nov** (clip sent) |
| 42 (Sam, 11 Nov) | R1 and R2 flash silver at the exact moment of the action | **DONE 11 Nov** (at the snap; at Navi's zip; clips sent) |
| 43 (Sam 1) | the first "f******" needs a small beep in the middle, just over the "uck" | line 1's bleep is one span over the whole word (3.33-3.72): shorten to the "uck" only, short beep; same for line 13 | **DONE 11 Nov:** line 1 3.39-3.56, line 13 4.87-4.99 (found from the take's vowel and the k) |
| 44 (Sam 2) | KG too static in S1: eyes and arms frozen | blinks, eye darts, wing flaps and sways, head tilts; check S3 the same (rule: a fault in one is looked for in every piece of its kind) | **DONE 11 Nov** (clip sent): S1/S3 blinks, darts, wings flap/wag, rocks on his toes from headlife (Job K rule: missed when the film was built, see rule request) |
| 45 (Sam 3) | time the execution move with "execution move" in the dialogue | the snap now lands after "MOVE" (SNAP = end + 0.12): the grip and twist land on "execution", the snap on "move"; retime NECK_GRIP/_s5_wings and the crack | **DONE 11 Nov** (clip sent): grip on "ex-", snap and crack on "move" (its syllable beat) |
| 46 (Sam 4, 7) | the gate break-in: a frame of everything fine cutting to a frame of everything on the ground; a better explosion on the gate and the grenade | a real blast: flash, fireball, shockwave, planks and dust flying over several frames, the gate in pieces falling; the grenade blast the same (S7 start, S8) |
| 47 (Sam 5) | the soldier the grenade hits fires in KG's face for long seconds: move him off screen; bullets whip past KG; he is seen only when KG fires the grenade | the middle-right man (G2) off screen until the zip; tracers and whips past KG from off screen; on "GRENADES" he is revealed |
| 48 (Sam 6) | bullet impact and blood splatter in the camp is very rudimentary | hits with sparks and dirt puffs, a proper splatter arc on the tower man and the lower-left man |
| 49 (Sam 8) | zoom in on the line-up (S10): more background than foreground | a tighter camera on the six, the sweep still in frame |
| 50 (Sam 9) | add "Um," to "I am nine years old." | Sam: the take already has it (0.6-1.0 s, it plays); the subtitle now reads "Um, I am 9 years old." **DONE 11 Nov** |
| 51 (Sam 10a) | make all subtitles larger and match them tighter; 3-5 words at a time | caption_at / finish.py subtitles: larger type, re-split every line into pieces of 3-5 words, timed to the words | **DONE 11 Nov:** remakes draw_subtitle 66 px (was 50); _pieces never joins past 4-5 words, on the syllable beats |
| 52 (Sam 10b) | "shit" is not bleeped in the subtitle or the audio | changes the earlier decision (f-word only): bleep "shit" in the audio (line 13) and star it in the subtitle ("s***"); drop it from SWEARS_OK. Say so in the reply | **DONE 11 Nov:** the "it" bleeped (2.08-2.40), "s***" |
| 53 (Sam 11) | front-on Link at "I want to go home", with fuller mouth movements | S13 as a front-on close-up (terrified, front view), the mouth shapes per syllable from the recording |
| 54 (Sam 12) | KG needs more dynamic faces, eye and body movements in the camp storm | S7: eye darts, brow changes, grin and snarl beats, body sway and recoil on each burst |
| 55 | plus the usual critique rounds | rule 89: the fresh-eye helper this time |
| 56 (Sam, 11 Nov) | "I am nine" (S11): Link is further into the square; the camera should have turned 180 to him | S11 as a reverse shot: Link facing KG and the line-up, the other side of the square behind him (not the line-up's own background) |
| 58 (Sam, 11 Nov) | S4 "Ok?": Navi bouncing off Link's head over and over (the nuzzle too subtle); Link looking ahead, eyes slightly aside, brows flat, low, close over the eyes (Sam's correction of worried brows): unsure, sceptical, doubtful | **DONE 11 Nov** (clip sent): mood 'doubtful'; Navi bounces off the cap every 0.36 s, squashed on each hit. Seen before (note 31): a changed decision, not a failed fix |
| 59 (Sam, 11 Nov) | A Fable trial on animatic 3: a fresh-eye critique by Claude Fable 5.2 (about 1% of a week) | when animatic 3 is sent, open a Fable chat (claude-fable-5-2, high effort) for a cold critique of it; its findings saved in the ledger, NOT acted on or shown to Sam until his notes on animatic 3 are in; then a 5-line comparison: which of Sam's notes it caught, what else it found, its cost. Sam then decides if Fable earns a place |
| 57 (Sam, 11 Nov) | KG too still holding Link up at the wall (S12, S12b, S13) | head moves (jabs, tilts, shakes on the words), brow and eye changes, beak snaps per syllable, body heaving; the wings stay on the collar | **DONE 11 Nov** (clip sent): head tilts and jabs from headlife, rage/fury face on the stresses, a lean in after his last word |


## Plan extras: the estimate (rules 24, 44)
Budget: 12%, stretch 15% (Sam). Week at 43% at the start. Compared with MidTerminal 11% (3 likenesses, one room),
Terfwarts 9%, Elder Swindon 9%: this film has 8 new characters, 4 places and 4 action moves, all new.
No likenesses (game characters, from the remake's screenshots), no 3D bodies (flat, one painting per camera).

| thing, build or risky move | KNOWN (where) or NEW | why (parts the camera sees) | estimate (% of a week) | spent |
|---|---|---|---|---|
| Young Link (remake design) | NEW | front only (scuttle faces forward, Sam), side for the wall shot; faces: unsure, sceptical, aghast, deadpan, terrified | 1.1 | |
| Kaepora Gaebora | NEW creature | perched front, flying side, wings used as arms (gun, neck snap, lapel grab, gesture); faces: kindly, glee, fury, hiss | 1.9 | |
| Navi | NEW | glowing ball and wings; blue to red; float, nuzzle, zip | 0.5 | |
| Masked gunman (one design, 3 uses) | part KNOWN (Patriot's balaclava) | front and side; one blown apart (pieces from `lying.py`) | 0.6 | |
| Rifle | NEW prop | flat, two views | 0.2 | |
| Young Zelda, Malon, Saria | NEW | line-up only: front view, small idle acting | 1.2 | |
| Ruto, Goron in frilly dress | NEW (new body types) | line-up only: front view | 1.0 | |
| Bandana | NEW prop | on KG's head, ties flutter | 0.1 | |
| Kokiri Forest: up at the branch, down at Link, Link's close-up, the gunman's patch | NEW set | one painting per camera, 4 cameras from one plan | 0.9 | |
| The encampment (walls, gate, watchtower, crates, sandbags) | NEW set | one camera, one painting | 0.8 | |
| Castle Town square (line-up and the wall) | NEW set | two cameras, one painting style | 0.7 | |
| KG swoops behind the gunman and snaps his neck | NEW risky move (rehearse) | | 0.5 | |
| KG bursts in firing; Link scuttles in | NEW risky move (rehearse) | MG42, belt, flash, cases KNOWN (`patriots3_cast.py`) | 0.6 | |
| Navi turns red, zips into a gunman, blast, dirt and body parts | NEW risky move (rehearse) | flash, debris, smoke KNOWN (`prepper_fx.py`); pieces KNOWN (`lying.py`) | 0.6 | |
| KG lifts Link by the collar and slams him on the wall | NEW risky move (rehearse) | thrown against a wall KNOWN (`patriots3_act.py`) | 0.5 | |
| Hook Text, sign-off, subtitles, bleeps | KNOWN | | 0.1 | |
| Critique, check sheet, animatic, one notes round, final | | | 3.0 | |
| **Total** | | | **14.5** | |

12% version (Sam to choose): the encampment as a fence and tower in the forest painting (-0.5), the line-up waist up
only (-0.5), one notes round fewer (-1.0).

Rehearsal clips sent: none: Sam, 10 Nov, the week at 75%: straight to the animatic, simplest staging (holds and cuts), no rehearsals
Composition sheet sent: 10 Nov, the check sheet (every shot) with the animatic yes

## The brief as a checklist (CLAUDE.md): every detail, ticked before the first animatic
News story: the Ocarina of Time remake (Switch 2, out 5 Nov 2026). The joke: modern gaming tropes in the charming classic.
| # | from the brief (word for word) | done? |
|---|------|------|
| 0 | Hook Text: "Ocarina of Time, remade for 2026" (Sam, Q9) | yes: HOOK; finish.py adds it |
| 1 | All references from the 2026 remake, not the N64 game | yes: the remake designs (cast sheets) |
| 2 | Cast: Young Link, Kaepora Gaebora (KG), Navi, militarised masked terrorists from generic Ubisoft games, Young Zelda, Malon, Princess Ruto, a Goron in a frilly dress | yes: all in the film (S1-S13) |
| 3 | Scene: Kokori Forest. The camera looks up where KG sits on a branch. | yes: S1 |
| 4 | KG: "Hello, Link! Are you ready for a f******* adventure!" (bleep; Sam, with the recordings: was "Hey, Link, are you ready...") | yes: S1, the f-word bleeped |
| 5 | Camera: looking down from KG's perspective at Link and Navi. Link: "Uh, yeah, I think so?" | yes: S2 |
| 6 | Camera: on KG. KG: "Great, here's some wisdom!" | yes: S3 |
| 7 | Link close up. He looks sceptical. Navi is gently nuzzling his cheek. Link: "Ok?" | yes: S4 (Navi bobs in to his cheek) |
| 8 | Close up on a masked Ubisoft terrorist looking into the forest with suspicious eyes. He holds a rifle into the trees. KG sweeps in behind him | yes: S5 (KG rises up behind him: simplest staging, not a swoop) |
| 9 | KG: "Press R1 for an EXECUTION MOVE." | yes: S5, the R1 prompt |
| 10 | KG snaps the terrorist's neck using his wings with hostile glee. | yes: S5 (wings close round the head, head turned right round, crack; he slumps) |
| 11 | Camera back on Link, aghast, Navi floating: "Oh my god!" | yes: S6, Navi bobs up startled (named: no hands to cheeks) |
| 12 | KG bursts into a walled compound in the forest, similar to an enemy encampment in Far Cry. Already opening up with a heavy machine gun furled in his wings. Warlike Rambo bandana. | yes: S7 (gate blown in, MG42 firing, bandana) |
| 13 | KG: "Clear enemy encampments to clear segments of the map." (Sam, with the recordings: was "...to control parts of the map!") | yes: S7 |
| 14 | Link scuttling in beside him: "I don't think I can do this." | yes: S7 (named: slides in with a bob, hands at his ears, not a crouched run) |
| 15 | KG: "R2 FOR GRENADES." | yes: S7, the R2 prompt |
| 16 | Navi goes danger-red and zips into a firing terrorist's torso, exploding on impact like a frag grenade, sending dirt and body parts flying. | yes: S8 (red, zip, blast, pieces, splat) |
| 17 | Link: "This is horrible." | yes: S9 (bits falling, one onto his cap) |
| 18 | KG gesturing at a line-up in Hyrule town square: Young Zelda (unsure), Malon (dutiful, 'pick-me', kind), Princess Ruto (preening: see Lost), a slightly drooling Goron in a frilly dress. | yes: S10 |
| 18b | Sam, 10 Nov: add Saria to the line-up (spunky, confident, 'he's already picked me') | yes: S10, Saria winks on "ROMANCE" |
| 19 | KG: "FIVE ROMANCE OPTIONS TO CHOOSE FROM" (Sam, 10 Nov: was FOUR) | yes: S10 |
| 20 | Close up of Link, deadpan: "I am 9 years old." | yes: S11 |
| 21 | KG picks him up with his wings like a tough guy by the lapels, shoves him hard against a town square wall. KG furious, Link terrified. KG hissing and spitting. Navi watches, growing redder into grenade mode. | yes: S12 (lifted to the wall by the collar; fury, spit; Navi reddening) |
| 22 | KG: "Now listen here, you shit. You're gonna grow up really f****** fast." then "And you've got some god-damn CHOICES to make." (two recordings, 13 and 13b; bleep the f-word; "god-damn" heard; Sam, with the recordings: was "Trust me, you're gonna grow up real f****** fast...") | yes: S12, the f-word bleeped |
| 23 | Close up on Link against the wall: "I want to go home." | yes: S13 |
| 24 | Energetic pace, exaggerated movements and enthusiasm, very little time between lines | yes: gaps 0.15-0.6 s |
| 25 | Navi always cutely floating, nuzzling, etc., depending on context | yes: she floats and bobs in each of her shots |
| 26 | Budget ideally 12%, stretch to 15% for quality | noted (cost watch) |
| 27 | Sam, 11 Nov: the detail is excellent; keep the models from looking too chibi | yes: the cast as drawn |
| 28 | Sam, 11 Nov: Link has the Kokiri Sword and its sheath | drawn (sheathed; no shot draws it) |
| 29 | Sam, 11 Nov: KG has a mouth and a beaky nose; he needs a real beak, and the beak moves when he talks | done, build chat 11 (the beak IS the mouth: upper and lower halves, the lower hinges open on each syllable; no lips or tongue-mouth under it; the grin and fury carried by the eyes, brows and beak angle) |

## References as checklists (Sam's round one, 10 Nov; `references/remakes/`). Ours matches? is ticked at the cast sheet
| reference | what it shows (count, colours, positions, facing, proportions) | ours matches? |
|---|------|------|
| 01-kg (THE OPENING SHOT, Sam) | KG on a mossy branch, low camera, blue sky and white clouds; Link's woven green cap back-of-head in the left foreground, spiral pattern on it, orange hair edge. KG faces us: chunky round body, rust-brown chest, ochre-gold belly, two big swept "horn" crests of gold-tan feathers curling up and outwards, white face disc, big round blue-grey eyes in white rings with dark brows, small gold beak, white bib with two gold eye-spot circles, yellow taloned feet gripping the branch, long fanned brown tail hanging below | |
| 02-kg | full body three-quarter on white: same colours; wings folded at the sides, dark brown with paler edges; tail long, grey-brown, pointed; legs gold-feathered, yellow claws; the crest horns are long (about the body's height), one curling forward, one back. Kindly, tolerant eyes | |
| 03-link | crouching, arm up to a light; big blue eyes, blond bowl-cut hair to the jaw, long pointed ears; green woven tunic with frayed fringes at hem and sleeves, short sleeves; brown leather strap across the chest, belt with a round silver buckle; green floppy cap with a red/brown bead band; brown boots with folded tan cuffs; wooden shield on his back. (Possibly fan art: 04 wins where they differ) | |
| 04-link (MAIN) | front, in-game: very big blue eyes, small nose and mouth, a toddler-ish round face; blond hair over the forehead; cap with red beads and a woven band; green knit shirt with a collar under a darker green tunic; chest strap, belt, buckle | |
| 05-navi | a white-hot ball with a soft white glow, four wings like dragonfly wings, pale with pink-green shimmer and vein pattern, top pair long and upright, lower pair small | |
| 06-navi | the same: pink-white ball, glow, sparkles round it; wings with a feather-cell pattern | |
| 07-ruto | full body: pale grey-white smooth skin, a big teal domed fish head-fin sweeping back, purple eyes with lashes, small smile; teal fin "top" at the chest, teal fins hanging from forearms and hips; hands on hips; bare feet, pink toes. Child proportions | |
| 08-ruto | front, hands on hips, the same; confident, smug | |
| 09-zelda | with Link: white dress with purple hem band, purple tabard, blue sleeves, white head-cloth with purple band | |
| 10-zelda (MAIN) | seated three-quarter: green eyes, blond hair, pointed ears; white cloth veil and purple padded headband with a gold triforce plate; gold collar; purple tabard with embroidery; puffed pale-blue sleeves; white skirt; holds the blue ocarina. Gentle half smile | |
| 11-goron | full body: smooth, bright yellow-orange, egg-shaped head and body in one, short stubby arms and legs, rocky grey patches on the back, a small pale tuft on top of the head, big grin. About Link's height x 1.6 | |
| 12-goron (MAIN face) | close: round dark purple eyes, small black brows, a small nose, a wide smile line, a white goatee point under the chin, round belly | |
| 13-malon | white dress with a blue horse-pattern hem, yellow neckerchief, long red hair, hands clasped, kind face, slightly shorter than Link | |
| 14-malon (RIGHT HALF only: the left is the N64 game) | long red-orange hair, blue eyes; yellow neckerchief with a brooch; grey-brown knit blouse with blue embroidered short sleeves; brown belt; brown patterned apron over a purple skirt with a blue meander hem | |
| 15-saria | sitting on a stump playing the ocarina, eyes closed; green fairy beside her; green hair, green outfit, boots | |
| 16-saria (MAIN) | front: bright lime-green bob with a fringe, blue eyes, pointed ears; dark green high-collar top, lighter green tunic with a swirl pattern, a fringed shoulder; pendant; a brown belt with a bead; green shorts; holds a wooden ocarina; soft confident smile | |
| 17-soldiers | two masked soldiers in a grey-green woodland: dark balaclavas with goggle or glasses eyes; one in a tan boonie hat kneeling with a black rifle (scope, long magazine) aimed into the trees; one in a grey helmet with a gas-mask face; grey-black plate vests with pouches, camo trousers, knee pads, gloves | |
| 18-soldiers | three in a row in profile: dark helmets, black full-face masks with goggles, olive-grey jackets, sling straps, rifles held across the chest; a red star patch on the sleeve (ours: no real insignia, a plain invented patch) | |
| 19-forest | Kokiri Forest wide: huge rounded canopy trees in soft green-gold, misty light shafts, layered forest depths, a tree-house trunk lower right | |
| 20-forest | the forest floor: a pale stone path winding back through mist, mossy roots and rocks either side, a tree house in a giant mossy stump on the right with a round door and orange lanterns, purple flowers in the near corner, a big glowing orange bell flower on the right, tall dark trees behind | |
| 21-town | Castle Town square: grey cobbles, a stone fountain with statues in the middle, timber-framed houses with red-orange tiled roofs and balconies, a palm-like tree left, a red-striped market tent, barrels and sacks, townsfolk; the castle pale and hazy far behind | |
| 22-town | the town entrance: stone balustrades with blue-and-gold drapes, tall blue banners with a gold crest, flower boxes (red and purple), bunting across the street, pale stone walls left and right (the wall for KG's slam) | |
| 23-outpost | a Far Cry outpost from above: a dirt yard ringed by grey corrugated walls, blue and orange shipping containers, wooden shacks with tin roofs, crates, a flagpole, parked old cars; jungle round it | |
| 24-outpost | the same at ground level: a dirt track in, a plank-and-tin shack left, a watch post, rocks and palms, a blue flag far off; bright midday sun | |
| Look across all of them | the remake's puppet-theatre materials: woven, knitted, carved. In our flat style, kept as a few weave or feather strokes on the big areas (cap, tunic, KG's chest), not textures | |
| Still missing | nothing: Link's scuttle faces forward (Sam, 10 Nov), so no side view is needed | |

## The acting list: shots (rule 74)
Length: about 83 words at Sam's pace (25 s) + action beats (8 s) + tight gaps + sign-off: **about 38 s**.

| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Hello, Link! Are you ready..." | KG | S1 low angle up at the branch: he towers, wise old owl | big hype grin (Q3) | wings flung wide, bobbing on the branch | "adventure" |
| 2 "Uh, yeah, I think so?" | Link | S2 high angle from KG's eyes: small and unsure | eyebrows up, half smile | shrug, Navi circling | "think" |
| 3 "Great, here's some wisdom!" | KG | S3 single on the branch | kindly, eyes closed in a smile (Q3) | one wing raised like a teacher | "wisdom" |
| 4 "Ok?" | Link | S4 close-up: the doubt is the beat | one brow up, side-eye | still; Navi nuzzles his cheek | "Ok" |
| 5 "Press R1 for an EXECUTION MOVE." | KG | S5 close-up on the gunman, KG rises behind him | gunman: narrow suspicious eyes; KG: glee | KG's wings round the head, twist; R1 prompt (Q5) | "EXECUTION", snap after "MOVE" |
| 6 "Oh my god!" | Link | S6 close-up: the reaction | eyes huge, mouth wide | hands to cheeks, jolt back; Navi startled bob | "god" |
| 7 "Clear enemy encampments to clear segments..." | KG | S7 wide: gate bursts, firing; the set is the joke | war face, teeth bared | MG42 in wings, recoil, bandana ties flutter | gate on "clear", flash from "enemy" |
| 8 "I don't think I can do this." | Link | S7 same wide: scuttles in at KG's side, facing forward, in from off camera (Sam, 10 Nov) | wince | crouched front-on scuttle (`GAITS['front_run']`, low), hands over ears | "this" |
| 9 "R2 FOR GRENADES." | KG | S7 then S8 push to Navi going red | glee | wing points at a gunman; R2 prompt (Q5) | "GRENADES": Navi goes |
| 10 "This is horrible." | Link | S9 close-up, dirt falling past | flat horror | frozen, a bit of debris lands on his cap | "horrible" |
| 11 "FIVE ROMANCE OPTIONS..." | KG | S10 wide line-up: everyone must read | game-show grin | wing sweeps along the line | each reacts on "ROMANCE"; Saria winks at Link, already sure |
| 12 "I am 9 years old." | Link | S11 close-up: deadpan is the joke | dead flat, half-lidded | still | "9" |
| 13 "Now listen here, you shit. You're gonna..." + 13b "And you've got some god-damn CHOICES..." | KG | S12 two-shot side on at the wall | fury, hiss, spit flecks | grabs the collar, lifts, slams on "Now" (was "Trust"); jabs his face on "shit"; shakes on "CHOICES"; Navi reddening behind | slam on "Now", shake on "CHOICES" |
| 14 "I want to go home." | Link | S13 close-up pinned to the wall | terrified, wobbling lip | feet off the ground, held | "home" |

Decisions made (Sam, 10 Nov):
- 1 the full version (14.5%). 2 Ruto vain and pushy, not sexual. 3 KG warm wise-owl for lines 1-3, war mode from "Press R1".
- 4 Navi has a soft glow (style exception, like Cortana). 5 R1 / R2 button prompts pop up on screen ("lol yes").
- 6 Sound effects: gunfire, the neck crack, Navi's blast. NO hiss sound (KG still hisses and spits in the drawing).
- 7 Gore option 3: splattier (flat house-style splats and pieces, plenty of red). 8 Three gunmen in the camp: Navi blows one up, KG guns down the other two.
- 9 Hook Text: "Ocarina of Time, remade for 2026". 10 Our flat style with the remake's designs, not its puppet look.
- 11 Line-up: Zelda hands clasped in front, eyes down, unsure; the Goron happily absent (vacant smile, drool); Malon holds out a milk bottle, hopeful; Saria posing nonchalantly with her ocarina ("he's already picked me"); Ruto vain and pushy.
- 12 Showstopper: the camp burst (gate blown in, watchtower, tracers, gun flash, falling cases).
- Link's scuttle faces forward, in from off camera.
