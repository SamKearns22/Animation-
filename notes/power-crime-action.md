# Notes for Power Crime Action (one file, numbered; mark each done as it is fixed)

Satire-style TikTok film. Code (to come): `source/power_crime.py`, from `source/satire_template.py`.
Recordings: `source/audio/power-crime-1..6.m4a` (filed 20 Oct, see row 30).

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 | Title: "Power Crime Action" (working title; no title in the video by default) | |
| 2 | "A crowd of Protesters in Trafalgar Square, chanting, waving signs, in support of the Palestinian cause." | |
| 3 | "Many of them are elderly and middle aged." | |
| 4 | "One second to set up the scene." | |
| 5 | "We zoom in on one little old lady (use model from Wolves)." (Cry Minister's old lady: white curls, glasses, pink coat, white tights) | |
| 6 | "She raises a sign in trembling hands." | |
| 7 | Sign: "Stop the Genocide. I Support." (wording to confirm, Q1) | |
| 8 | "We do not see the rest of the sign. It says Palestine Action. And that is implied" (the words are never shown, not one letter) | |
| 9 | "Nearby, a group of Met police officers observe proceedings with serious neutrality or mild distaste." | |
| 10 | "A senior officer with sunglasses drops his mouth in horror." | |
| 11 | Senior officer: "Shit. a code red." | |
| 12 | "Mid shot on protesters. An object in the foreground covers the 'Palestine Action' part of the sign." | |
| 13 | "Armed response metropolitan police officers sweep in from all directions" | |
| 14 | "including two from ropes coming down into frame." | |
| 15 | "Some point their rifles at the old lady" | |
| 16 | "whilst two pick her up by the arms." | |
| 17 | "She is bodily taken towards the right" | |
| 18 | "and comically thrown 50ft into the back of a police van" (about 15 m) | |
| 19 | "that drives off." | |
| 20 | "Interrogation room." | |
| 21 | "Senior officer sits with old lady, who is trembling but otherwise unbothered." | |
| 22 | Senior officer: "Listen to me you filth. You're going to tell me everything. The location of your cells. The nature of your resources. The aims of your organisation." | |
| 23 | "We cut to the doorway. It opens and an officer walks in." | |
| 24 | Officer (Jenkins): "Err, excuse me sir. I need to speak to you outside. It's urgent." | |
| 25 | "We are outside in the corridor. The two officers." | |
| 26 | Jenkins: "I'm sorry to interrupt sir, but there's been a mass casualty attack in—" (cut off) | |
| 27 | "The senior officer points into his chest and leans forward aggressively." | |
| 28 | Senior officer: "I don't have time to be dealing with your small fry problems, Jenkins. Interrupt me again and see what happens." | |
| 29 | The joke: "policing old ladies with signs is more important than actual terrorism." | |
| 30 | "Please learn from lessons from previous round of videos. Please advise on references" | |

## Recordings (voices.py, 20 Oct: no duplicates; every length fits its line)
| line | file | who | speech (s) | note |
|---|---|---|---|---|
| 1 | power-crime-1.m4a (Chanting protestors) | crowd | 0.50-5.30, four phrases | words to confirm (Q3); to be layered into a crowd |
| 2 | power-crime-2.m4a (A code red) | senior officer | 0.64-1.03, 1.93-2.70 | "Shit." / "A code red." |
| 3 | power-crime-3.m4a (Tell me everything) | senior officer | 0.21-10.33, five phrases | one per sentence |
| 4 | power-crime-4.m4a (Excuse me sir) | Jenkins | 0.77-3.95, three phrases | |
| 5 | power-crime-5.m4a (Mass casualty) | Jenkins | 0.18-3.76, two phrases | quieter (-23.9 LUFS): levelled up |
| 6 | power-crime-6.m4a (Jenkins) | senior officer | 0.47-9.25, three phrases | |

## Facts checked (20 Oct)
- The real placard: "I OPPOSE GENOCIDE. I SUPPORT PALESTINE ACTION" (Defend Our Juries protests; Trafalgar Square,
  11 April 2026: over 1,000 gathered, over 500 arrested, many elderly; Margaret Owen, 94, arrested in Parliament
  Square). Sources: Al Jazeera 11 Apr 2026, Reuters Connect, Middle East Eye.
- Met armed response (ARV / MO19) officers: dark navy shirts and trousers, black body armour marked POLICE, blue
  baseball caps (or helmets), SIG MCX carbine as standard, pistol on the thigh (Met FOI disclosure, April 2024).

## Draft shot plan (about 43 s + the 2 s sign-off; judged on the first animatic)
| shot | time | camera | what happens |
|---|---|---|---|
| 1 | 0-1.2 | high wide from the National Gallery terrace, looking south down the square | the packed protest: Nelson's Column, two lions, fountains, flags, placards, chanting (line 1) |
| 2 | 1.2-3.4 | push in to the old lady in the crowd | she lifts her placard in trembling hands; heads in front hide its lower half; we read only the top |
| 3 | 3.4-4.6 | the police line at the edge of the square | officers in hi-vis watch, neutral or mildly sour; the senior officer in sunglasses among them |
| 4 | 4.6-7.4 | close-up, senior officer | his mouth drops in horror (strength sheet 1-6); "Shit. A code red." (line 2) |
| 5 | 7.4-12.0 | mid shot on the protesters, her in the middle | a foreground object covers the lower half of the sign; armed officers run in from left, right and behind; two slide down ropes into frame; carbines on her; two take her by the arms and lift her; she lets the sign fall face down |
| 6 | 12.0-15.0 | wide, side on, across the square | they carry her right, swing her, and throw her about 15 m in an arc into the open back of a police van; doors shut; it drives off right |
| 7 | 15.0-26.5 | interrogation room: two-shot, then close on him | he sits across from her; she trembles, unbothered; line 3 |
| 8 | 26.5-30.5 | the doorway | the door opens; Jenkins steps in; line 4 |
| 9 | 30.5-43.0 | the corridor, the same door from outside | line 5, cut off; the senior officer jabs Jenkins in the chest and leans in; line 6 |

## Reuse before building (guides/satire.md)
- Everyone: `views.py` (any angle) with the template's house style; crowds seen from behind varied as
  `press_secretary.reporter`.
- The old lady: Cry Minister's design (`cryminister.LADY`) rebuilt in `views.py`.
- Running in: `moves.travel` ('run'); sitting: `moves.seated`; the chest jab: `moves.pose` with a contact check.
- Being carried: Poker Mon's grip method (one grip point drives the officers' hands and her arms).
- The throw: Poker Mon's `launch` flight under gravity (3D bodies, spin, landing that stays).
- Sets: each place built once in 3D and shot with cameras (Poker Mon's `Cam3` room method).
- NEW (nothing fits): Trafalgar Square; the police van and its drive-off; carbines and the aiming pose; the rope
  slide; police uniforms (hi-vis, caps, armour); the interrogation room and corridor; flags and placards.

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
All in `references/power-crime-action/` (Sam's screenshots, 20 Oct).
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
| placard-1..2 | WHITE card, portrait (about 45 x 60 cm), black marker capitals in five lines filling it: I OPPOSE / GENOCIDE / I SUPPORT / PALESTINE / ACTION. Uneven hand lettering. Held flat to us at chest height, both hands on the sides or bottom corners. Most of the crowd hold the same card (ours: only she does, Sam Q9). Ours: top three lines only; the bottom two-fifths blank and always hidden; raised from chest to about head height. | |
| aerial-1..3 | Column at the south end, centred between two fountains just north of it; square stepped base, a lion at each corner. Fountains: four-leaf-clover basins, turquoise water, grey stone rim, round tiered bowl in the middle. Pale granite paving with darker diamond and square lines round each fountain. Raised north terrace, wide central staircase, stone wall and railings; National Gallery behind. Corner plinths with statues. Roads south, east, west (red buses, black cabs); roundabout with a statue to the south. Trees along east and west. | |
| gallery-1, gallery-lion, from-steps-1, fountain-1, from-portico | Gallery: long, low, pale stone, columns; central portico with pediment and dome; St Martin's white spire to its right. From the steps: the column dead centre, about 4x the buildings behind; pale grey fluted shaft, dark bronze capital, Nelson on top; bronze panels on the base; fountains low either side, tiered bowls spraying; cream and sandstone buildings with roof flags; trees left; red buses; black posts, ornate black lamp posts. From the portico: two huge fluted columns frame it, black iron railing of circles (not used: hides the crowd). Bright sky, big white clouds. | |
| protest-1..3, arrest, police-group-lion | April 2026: most of the crowd SITS on the paving in dense rows facing the gallery steps; steps packed; banners on the terrace wall; autumn coats, scarves, woolly hats, keffiyehs; grey and white hair; Palestinian flags, a big blue flag; Union flag on the gallery. Arrest: a grey-haired woman (sunglasses, red scarf, dark coat) goes limp; two officers each hook an arm under her armpit and hold her forearm, knees bent, feet trailing. Police: dozens by a lion, red bus behind, calm, hands by sides or on belts. ALL in flat peaked caps (no tall helmets). | |
| lion-1..4 | Four bronze lions, about 6 m long, nearly black with a green-grey sheen; lying like a sphinx, front legs straight out, paws together, head up, looking ahead, calm, mouth closed; back legs tucked, tail along the side; thick wavy mane over shoulders and chest. Each on its own long plain pale grey block at chest height, out from the base's corners, facing out (pairs north and south); lettered panel on the block. Black posts and lamp posts round them. | |
| column-1, column-fountain, column-lion | Proportions: base and pedestal the bottom fifth, fluted shaft three-fifths (tapering slightly), capital and statue the last fifth. Pedestal pale grey with a dark bronze panel each face, moulded ledge, round drum. Dark bronze leafy capital, round stand, Nelson in pale stone facing south. Fountains: warm golden SANDSTONE tiered bowls, tall jet; wide low stone rim people sit on; a bronze statue on a plinth nearby; cream buildings with Union flags. | |
| police-1..4 | Hi-vis: bright yellow; silver bands over the shoulders like braces and round the body (and round the arms on the jacket); blue-and-white chequered band near the hem; white POLICE on a blue chest patch; black collar; body camera centre chest; radio high on a shoulder; pouches. Black trousers, belts, boots. Flat peaked cap, black with chequered band, on everyone. Warm day: white short-sleeved shirt under a sleeveless vest; cold: full jacket. Standing in a loose cluster looking one way: arms folded, hands clasped at the belt, thumbs in the vest; faces flat, neutral, a little unimpressed. Crowd behind: many Palestinian flags on poles, white boards (FREE PALESTINE, GAZA), keffiyehs, headscarves. | |
| senior-1..5 | Real senior officers: uniform ONLY (our man's face is made up). White shirt, pointed collar, plain black tie, two chest pockets with buttoned flaps; stiff black shoulder boards pointed at the collar end with silver crown and pip; small black name badge over the right pocket, white capitals. Cap: wide flat black top overhanging, a deeper three-row chequered band, glossy black peak edged with a thick silver band of oak leaves, silver crowned badge. Black trousers and belt. | |
| armed-1..4 | SIG MCX: all black, long slotted handguard, small sight on top, pistol grip, slightly curved magazine, short stock, sling. Carried low across the body, muzzle down and to the side; aimed shouldered with gloved hands, left hand on a small foregrip. Black tops (or navy fleece), black armour with pouches, black POLICE patch with white letters, radio, body camera, small Union flag patch, yellow Taser at the front, pistol low on the right thigh, black cargo trousers, boots. Hats: flat chequered cap; navy baseball cap with chequered band and POLICE across the front; counter-terror: black cap with a chequered side band, black balaclava, black gloves. | |
| van-front, van-back, van-back-open (van-old not used) | Met TSG Mercedes Sprinter, tall: dark navy body; one row of big blue and yellow checks along the lower sides; POLICE in white along the top of the roof edge; TERRITORIAL SUPPORT GROUP in white on the rear side window; tinted windows; Met badge. Front: yellow bonnet with POLICE in blue, blue light bar on the roof, blue lights in the grille, black grille with the star, plate. Back: two tall doors, red and yellow chevrons on the lower half, POLICE in red across the top, fleet number, black bumper with a red reflective strip. Open: doors swing right round to the sides; grey interior with a caged cell, blue floor, fire extinguisher, seats. Ours: a made-up fleet number. | |
| interrogation-1..3 | Dark bare room; painted breeze-block walls, dark green-grey (or darker below, paler above); concrete floor with a painted blue line; one hanging cone lamp over the table: a bright pool, hard shadows, dark corners; grey metal table on steel legs; two chairs facing across it (wood on metal frames, or white metal); heavy grey metal door with a small square window in the back wall; a long dark one-way mirror along a side wall reflecting the table. | |
| corridor | A custody corridor: white walls, a row of heavy dark grey cell doors with hatches, panels and signs; red alarm bars along the walls; strip lights down the ceiling; pale grey speckled floor; a door at the far end. | |
| crowd-low-1..4 | Camera at head height inside the crowd, looking north to the gallery: everyone packed together, mostly sitting on the paving facing the camera, some on folding chairs, standing at the back; the steps full; banners on the terrace railings (LIFT THE BAN, PEACE, DROP THE CHARGES, DISARM); a few stewards in orange hi-vis; hi-vis police on the steps; autumn coats, keffiyehs, woolly hats; nearly everyone holds the white I OPPOSE GENOCIDE card (ours: only she does, Sam Q9; the others carry FREE PALESTINE / CEASEFIRE NOW boards and flags). | |
| rope-1..2 | Rope descent: rope through a harness at the hip; one gloved hand high on the rope above, the other hand holding the weapon out; knees bent, legs apart, boots braced (against a wall) or hanging; body tipped back or turned. All in black, helmet or cap. | |

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | cast | - | "Face number 3" (the senior officer's horror strength) | done: HORROR level 3 for "Shit. A code red." |
| 2 | cast | sign at her chest | "The sign raises into her physical body ... the upper edges cut into her shoulders." | fixed: the card is in front of her arms; only her hands show, over its edges |
| 3 | cast | hands behind back | "We don't see the arm coming down and around the back of the body, so he looks like he has no arms." | fixed: hands clasped in front at the belt instead (ref police-3) |
| 4 | cast | arms folded | "Can I check we are using the smooth fluid arms and leg styles? The police officer on the left seems to have blocky arms" | fixed: the cast file had not switched on the house style's smooth limbs (limbs.install); now on |
| 5 | all | - | "On all our character designs across our videos, the hips are possibly 15% too wide so the bottom of the body looks quite blocky" | done: burnham.HEM = 0.85 (the hem 15% narrower than the shoulders, tapering from the waist), front, three-quarter and back views; every film from now on |
| 6 | square | - | "In the crowd shots I see, everyone is very spaced out. In the references I have you, crowds are pushed together, side by side." | done: about 2,000 people in rough rows 0.6 m apart, rows 0.85 m; far ones drawn as simple figures in their own colours |
| 7 | square | - | (refs crowd-low-1..4) "The camera here is close up and we see the density of the crowd ... I don't think our shot of the square should go any higher than these angles" | done: the crowd turned to face south, the gallery's steps full of people, banners on the terrace (LIFT THE BAN, PEACE, DROP THE CHARGES: from Sam's photos); every square camera at head height or lower, inside the crowd, looking north to the gallery; she is carried west (screen right) and the van leaves west |

Decisions made (kept so a long session or a new session never has to rediscover them):
- Sam's answers (20 Oct): 1 the real wording "I OPPOSE GENOCIDE. I SUPPORT"; 2 "Palestine Action" never drawn, she
  drops the sign face down; 3 the chant is "Free Palestine" three times (subtitled); 4 voice as recorded, "Sh*t." in
  the subtitle; 5 senior officer as proposed (peaked cap, white shirt, mirrored aviators, kept on indoors) plus tough
  stubble; 6 Hollywood-style interrogation room; 7 NOT the upright landing: she flies head first through the van's
  open back doors, we never see her inside: a hilariously violent, urgent throw of a whole person, and the van speeds
  off urgently, lights flashing; 8 numbers as proposed (about 120 protesters, 5 officers + the senior officer, 8 armed:
  3 left, 3 right, 2 down ropes from an unseen helicopter); 9 only she has the placard; 10 sound effects: helicopter,
  van doors, van pulling away (and only those); 11 Hook Text "Met Police: Getting Priorities Right 🚔"; 12 build the
  solid look for people seen from high cameras.
- Changes from the references (Sam's "go", 20 Oct): the placard white and portrait; every hi-vis officer in the flat
  chequered cap (no tall helmets); the crowd mostly sits (a few rows standing at the back waving flags), autumn coats,
  scarves, woolly hats, more flags and headscarves; she stands, so she can raise her sign; the lift is the arrest
  photo's grip (arm under each armpit, hand on the forearm), then off the ground; the police wait by a lion with a
  red bus behind; fountains golden sandstone, people sit on the rims; senior officer: Chief Superintendent (crown and
  pip), badge reads CHIEF SUPERINTENDENT only, no hi-vis; armed: 3 flat caps, 3 navy POLICE baseball caps, the 2 on
  ropes in black caps, balaclavas and gloves; the van dark navy (current livery); interrogation room as the refs (table
  under one lamp, mirror left, door in the back wall; she faces the door, he has his back to it); corridor as the ref.
  My additions, named to Sam: the lamp swaying very slightly; people on the fountain rims.
- Sam (20 Oct): "Don't draw blind: request references from me if you get stuck." The photo sites were blocked by the
  network, so drawing stopped and the references were asked for. `source/power_crime_cast.py` is a first draft
  (uniforms, hats, placard, carbine), not yet drawn or checked; it is finished against Sam's photos.
