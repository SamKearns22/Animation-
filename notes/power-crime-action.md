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
All to be saved in `references/power-crime-action/`.
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
|   |      |      |

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 |      |      |      | open   |

Decisions made (kept so a long session or a new session never has to rediscover them):
- The words "Palestine Action" are never drawn anywhere in the film (proposed, Q2).
