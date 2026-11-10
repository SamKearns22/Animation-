# Notes for REMAKES (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (each new character alone beside its references, critiqued cold), 41 (every arm ends
  in a hand; KG's wings are arms), 38 (only the views the shots use: Link front, side, back; gunman front, side).
- **Done (10 Nov, build chat 1, Opus high; stopped on cost amber):** `source/remakes_cast.py` started: all five
  children (head, hair, outfit, sleeves, boots, faces), the gunman (Patriot balaclava + helmet, goggles, plate vest),
  milk bottle, ocarina, rifle; `alone WHO OUT.jpg` sheet. Only Link has been looked at.
- **Link's faults from my own look (fix before the critique):** 1 head too small for a 9-year-old, legs too long
  (aim about 4 heads tall: bigger hh or shorter legs); 2 long thin neck, and side on the head floats off the body;
  3 brows hidden under the fringe (draw them over it); 4 cap too small and flat, its tail reads as a leaf (ref 04:
  big floppy cap hanging to his left); 5 faces too alike at phone size (unsure, horror, deadpan need bigger brows and
  mouths); 6 side view shield sticks out like a slab; 7 the sheet's figure tiles are mostly empty (crop tighter).
- **Next:** Build, Opus high: fix Link's 7, check the same faults in Zelda, Malon, Saria, Ruto and the gunman
  (`alone` each), then `remakes_creatures.py` (KG, Navi, Goron), critique each (`critique.py pack`), cast sheet.
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references and Decisions; `source/remakes_cast.py` MAP.
- **Open rule requests:** none.
- **For Claude:** refs `references/remakes/`; MG42 `patriots3_cast.py`; fx `prepper_fx.py`; pieces `lying.py`;
  wall throw `patriots3_act.py`; `moves.GAITS['front_run']`. Kids draw at `height` via `scale_for`.

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

Rehearsal clips sent: (rule 8: the 4 risky moves above; not yet)
Composition sheet sent: (rule 11: not yet)

## The brief as a checklist (CLAUDE.md): every detail, ticked before the first animatic
News story: the Ocarina of Time remake (Switch 2, out 5 Nov 2026). The joke: modern gaming tropes in the charming classic.
| # | from the brief (word for word) | done? |
|---|------|------|
| 0 | Hook Text: "Ocarina of Time, remade for 2026" (Sam, Q9) | |
| 1 | All references from the 2026 remake, not the N64 game | |
| 2 | Cast: Young Link, Kaepora Gaebora (KG), Navi, militarised masked terrorists from generic Ubisoft games, Young Zelda, Malon, Princess Ruto, a Goron in a frilly dress | |
| 3 | Scene: Kokori Forest. The camera looks up where KG sits on a branch. | |
| 4 | KG: "Hey, Link, are you ready for a f******* adventure?" (bleep) | |
| 5 | Camera: looking down from KG's perspective at Link and Navi. Link: "Uh, yeah, I think so?" | |
| 6 | Camera: on KG. KG: "Great, here's some wisdom!" | |
| 7 | Link close up. He looks sceptical. Navi is gently nuzzling his cheek. Link: "Ok?" | |
| 8 | Close up on a masked Ubisoft terrorist looking into the forest with suspicious eyes. He holds a rifle into the trees. KG sweeps in behind him | |
| 9 | KG: "Press R1 for an EXECUTION MOVE." | |
| 10 | KG snaps the terrorist's neck using his wings with hostile glee. | |
| 11 | Camera back on Link, aghast, Navi floating: "Oh my god!" | |
| 12 | KG bursts into a walled compound in the forest, similar to an enemy encampment in Far Cry. Already opening up with a heavy machine gun furled in his wings. Warlike Rambo bandana. | |
| 13 | KG: "clear enemy encampments to control parts of the map!" | |
| 14 | Link scuttling in beside him: "I don't think I can do this." | |
| 15 | KG: "R2 FOR GRENADES." | |
| 16 | Navi goes danger-red and zips into a firing terrorist's torso, exploding on impact like a frag grenade, sending dirt and body parts flying. | |
| 17 | Link: "This is horrible." | |
| 18 | KG gesturing at a line-up in Hyrule town square: Young Zelda (unsure), Malon (dutiful, 'pick-me', kind), Princess Ruto (preening: see Lost), a slightly drooling Goron in a frilly dress. | |
| 18b | Sam, 10 Nov: add Saria to the line-up (spunky, confident, 'he's already picked me') | |
| 19 | KG: "FIVE ROMANCE OPTIONS TO CHOOSE FROM" (Sam, 10 Nov: was FOUR) | |
| 20 | Close up of Link, deadpan: "I am 9 years old." | |
| 21 | KG picks him up with his wings like a tough guy by the lapels, shoves him hard against a town square wall. KG furious, Link terrified. KG hissing and spitting. Navi watches, growing redder into grenade mode. | |
| 22 | KG: "Trust me, you're gonna grow up real f****** fast. And you've got some god-damn CHOICES to make." (bleep the f-word; "god-damn" heard) | |
| 23 | Close up on Link against the wall: "I want to go home." | |
| 24 | Energetic pace, exaggerated movements and enthusiasm, very little time between lines | |
| 25 | Navi always cutely floating, nuzzling, etc., depending on context | |
| 26 | Budget ideally 12%, stretch to 15% for quality | |

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

## Shots and the acting list (rule 74; faces wait on Sam's answers where marked)
Length: about 83 words at Sam's pace (25 s) + action beats (8 s) + tight gaps + sign-off: **about 38 s**.

| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "Hey, Link, are you ready..." | KG | S1 low angle up at the branch: he towers, wise old owl | big hype grin (Q3) | wings flung wide, bobbing on the branch | "adventure" |
| 2 "Uh, yeah, I think so?" | Link | S2 high angle from KG's eyes: small and unsure | eyebrows up, half smile | shrug, Navi circling | "think" |
| 3 "Great, here's some wisdom!" | KG | S3 single on the branch | kindly, eyes closed in a smile (Q3) | one wing raised like a teacher | "wisdom" |
| 4 "Ok?" | Link | S4 close-up: the doubt is the beat | one brow up, side-eye | still; Navi nuzzles his cheek | "Ok" |
| 5 "Press R1 for an EXECUTION MOVE." | KG | S5 close-up on the gunman, KG rises behind him | gunman: narrow suspicious eyes; KG: glee | KG's wings round the head, twist; R1 prompt (Q5) | "EXECUTION", snap after "MOVE" |
| 6 "Oh my god!" | Link | S6 close-up: the reaction | eyes huge, mouth wide | hands to cheeks, jolt back; Navi startled bob | "god" |
| 7 "clear enemy encampments..." | KG | S7 wide: gate bursts, firing; the set is the joke | war face, teeth bared | MG42 in wings, recoil, bandana ties flutter | gate on "clear", flash from "enemy" |
| 8 "I don't think I can do this." | Link | S7 same wide: scuttles in at KG's side, facing forward, in from off camera (Sam, 10 Nov) | wince | crouched front-on scuttle (`GAITS['front_run']`, low), hands over ears | "this" |
| 9 "R2 FOR GRENADES." | KG | S7 then S8 push to Navi going red | glee | wing points at a gunman; R2 prompt (Q5) | "GRENADES": Navi goes |
| 10 "This is horrible." | Link | S9 close-up, dirt falling past | flat horror | frozen, a bit of debris lands on his cap | "horrible" |
| 11 "FIVE ROMANCE OPTIONS..." | KG | S10 wide line-up: everyone must read | game-show grin | wing sweeps along the line | each reacts on "ROMANCE"; Saria winks at Link, already sure |
| 12 "I am 9 years old." | Link | S11 close-up: deadpan is the joke | dead flat, half-lidded | still | "9" |
| 13 "Trust me, you're gonna..." | KG | S12 two-shot side on at the wall | fury, hiss, spit flecks | grabs the collar, lifts, slams on "Trust"; shakes on "CHOICES"; Navi reddening behind | slam on "Trust", shake on "CHOICES" |
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
