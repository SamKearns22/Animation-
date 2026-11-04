# Notes for MidTerminal (one file, numbered; mark each done as it is fixed)

## Where things stand
- **Rules that bite next:** 56 (a fault of its kind: every point hand, every U-shaped arm pose, every ghost layer), 27 (bleep both swears, from the sound), 14 (check sheet and Sam's yes before the animatic)
- **Done (4 Nov):** film built; test animatic (silent, estimated timings) sent; Sam's notes 31-43 logged in the Notes table; his answers in (below); meter 78% (stop 84%).
- **Sam's answers:** note 35 = palms flung up and out on "Yeah, because Bibi told me to", lean in and jab twice on "I thought he was one of yours!?" (yes). Note 40 = narrow eyes on "I know it's you", NO finger wag, arms folded with a smug sneer on "reflecting pool". Note 42 = Trump copies Epstein's silly ghost wave, smaller and floppier, pout, raised brows, head waggling (yes). Skeleton: no reference, draw from standard anatomy in the house style (yes).
- **Next:** Opus, medium effort, one chat: fix notes 31-43, short clips for the moves (`final OUT --small --span T0 T1`: shrug, breath-and-point, flame burst, melt), then file Sam's recordings when they arrive, place the bleeps, full pre-flight, check sheet, wait for Sam's yes. New chat, type: "MidTerminal: notes 31-43 from the handover in notes/midterminal.md".
- **Needs Sam:** the recordings (lines 1-5, 7-10, door slam, gentle fire sound), 2:30-3 pm 4 Nov; a clear Y/N that "T" meant Y on the pointing-finger rule.
- **Read:** guides/satire.md 'Movement', 'Before every render'; guides/kit-catalogue.md 'Effects' (burst, smoke, flash); only the lines each note touches in `source/midterminal*.py`.
- **Lost / Added:** Lost: the zoom out (note 38). Added (Sam's): a corridor in depth, camera flashes, flames and smoke on Epstein's entrance, flames on his body, a burning skeleton under the melt, Trump's breath and arm gestures.
- **Open rule requests:** "when anyone points, the hand shows a pointing finger" (note 33; Sam's 5th answer came as "T", read as Y, ask once to confirm, then write it in the rulebook with its check and list it in the last table).
- **For Claude:** film `source/midterminal.py` (MAP at top); audit "pops" at 2.17, 14.50, 15.58, 30.25 are the frame before each cut (audits() uses int(a*FPS); start at ceil). Point hand: `MV._install_point_finger`, `MV.point_at`. Skull: `MV.epstein_item` draws `under` straight on `im`, not through `MS.ghost`; its head box is measured with arms down. Pocket square: check `V.snap` near 13.58. Shrug: `moves.pose 'shrug'` U-shape; the film's `satan_j`. Door/corridor: `MV.door_open`, `CORRIDOR`. Wings: `MC.wings`. Flag and books: `midterminal_set.py`. Quick pre-flight: `python3 source/preflight.py midterminal OUT --text`.
## Shot list (Sam, 4 Nov: the camera turns 180 to Trump when he speaks; the opening joke lands by 3-5 s)
1. Door (key shot 1): Trump strides in, eyes right off-screen, "Thank you, everyone, no more questions." Eyes forward at the threshold; the door slams behind him. Quick: about 1.5-2 s.
2. Wide two-shot (key shot 2): walking fast to face the desk, angry: "Satan, what the f***? This isn't what you promised." Done by 3-5 s.
3. Satan floating before the desk, a small shrug: "I said don't invade Iran, you invade Iran."
4. Reverse (180) on Trump, accusing, pointing: "Yeah, because Bibi told me to. I thought he was one of yours!?"
5. Satan, chuckling: "Oh, no. We've got nothing on him."
6. Zoom out (key shot 3): Epstein's ghost fades in by the side of the desk; Satan's pupils go to him.
7. Epstein (key shot 4): "Don't worry, Donald. Why don't you come and join me? It's warm here. Nobody ever gouges out your eyes on an hourly basis."
8. Reverse on Trump: "F*** off, Jeffrey. I know it's you that keeps putting algae in the reflecting pool."
9. Epstein waves his arms like a silly ghost, fades, face melting into a flaming skull: "Releeeease the filessssss" (gentle fire sound).
10. Reverse on Trump, mocking: "release the fiilleees." Then: "If Satan had done his job, maybe I wouldn't have to."

## The brief as a checklist
| # | from the brief or a note | done? |
|---|------|------|
| 1 | Oval Office set from Sam's five photos: gold curtains, blue carpet (Sam's pick 1) | yes |
| 2 | Flat cartoon style (pick 2: Y) | yes |
| 3 | Satan: humanoid, suited (refs satan-1, -2); horns and wings from ref 2, kept modest (my pick; Sam didn't answer) | yes |
| 4 | Jeffrey Epstein (3 refs), dark polo (Sam's pick) | yes |
| 5 | Donald Trump (3 refs) | likeness 32%: needs photos |

| 6 | The joke: Trump has a go at Satan for not delivering the midterm results he wanted; the hellfire ghost of Epstein intervenes | drawn (film 4 Nov): shots 2-10 |
| 7 | Trump comes into the Oval Office from the corridor through the door; pupils look right at someone we don't see: "Thank you, everyone, no more questions." | drawn: shot 1, eyes right (look 0.9) until the threshold |
| 8 | Eyes face forward as he crosses the threshold; the door shuts behind him | drawn: eyes forward past 1.2 m; slam on the line's end |
| 9 | Angry face as he walks opposite the desk: "Satan, what the f***? This isn't what you promised." (1 bleep) | drawn: frowning, pointing as he walks in; bleep placed once the take is in |
| 10 | Satan floats before the desk, a small shrug: "I said don't invade Iran, you invade Iran." | drawn: shot 3, small shrug, floating |
| 11 | Trump, accusatory, angrier, pointing: "Yeah, because Bibi told me to. I thought he was one of yours!?" | drawn: shot 4 reverse, frown deeper, pointing |
| 12 | Satan, chuckling: "Oh, no. We've got nothing on him." | drawn: shot 5, smirk, shoulders bobbing |
| 13 | Zoom out. The hell ghost of Epstein fades in, floating by the side of the desk. Satan's pupils look at him | drawn: shot 6, zoom out, fade in, Satan's eyes to him |
| 14 | Epstein: "Don't worry, Donald. Why don't you come and join me? It's warm here. Nobody ever gouges out your eyes on an hourly basis." | drawn: shot 7 |
| 15 | Trump: "Fuck off, Jeffrey. I know it's you that keeps putting algae in the reflecting pool." (bleep: Q4) | drawn: shot 8; bleep placed once the take is in |
| 16 | Epstein waves his arms like a silly ghost, gently fades away, face melting into a flaming skull: "Releeeease the filessssss" | drawn: shot 9, arm wave, melt, fade; fire sound once Sam's file is in |
| 17 | Trump, childish mocking voice: "release the fiilleees." Then: "If Satan had done his job, maybe I wouldn't have to." | drawn: shot 10, brows up, head waggle on the mock, then the last line |
| 18 | Characters 2D first: front, side, back; three-quarter only if the script calls for it (Sam, 4 Nov) | yes (cast sheet) |

| 19 | Hook Text: "Trump after Midterm results" (Sam's words, exactly) | in the film (HOOK), put on by finish.py |
| 20 | Budget: 10% of a week at most for this film (Sam, 4 Nov, meter at 74%) | 77% at the build start (stop 84%) |

| 21 | Sam 4 Nov: budget stop at 84%; Trump's eyes a little more open; Satan floats, wings medium, horns small; bleep every swear; the ghost not too cartoony, in the house style; Sam supplies a gentle fire sound and a door slam | done (cast), rest in build |
| 22 | Sam 4 Nov (test clip): Trump behind the shut door until it opens; corridor wall and carpet fill the doorway; door swings into the room, on the left | done (moves) |
| 23 | Sam 4 Nov: in the walk-to-the-desk shot Trump right, Satan middle, Epstein left; Trump front-on and pointing at Satan as he walks in | done (moves) |
| 24 | Sam 4 Nov: Epstein's fire flames upwards; the skull larger, more grotesque, plainly screaming in terror and agony | done (moves) |
| 25 | Sam 4 Nov: in the Satan shot Trump comes in from the left, even if it breaks logic | done (moves) |
| 26 | Sam 4 Nov: Trump starts his accusing line (line 2) as soon as the door closes | moves: cut on the slam; film: line 2 timed to it |
| 27 | Sam 4 Nov: the skull full (no caving at the mouth; his ref), in the house style and colours; the flames end in a bed of embers, no hard line | done (moves) |
| 28 | Sam 4 Nov: Trump walks in from the RIGHT (not left); the skin melts down OVER the skull; the door has thickness side on; no stray line inside its thickness, top edge outlined (5 Nov) | done (moves) |

Composition sheet sent: 4 Nov, `python3 source/midterminal_set.py comp OUT.jpg` (4 key shots: door, two-shot, zoom out with the ghost, Epstein close)

## Plan extras: ambition estimate (rule 55)
| build or risky move | why | estimate (% of a week) | spent |
|---|---|---|---|
| Trump's entrance: a door that swings open and shuts, him walking through it | the set's doors are painted flat; one needs to open (one door, its leaf only) | 2 | |
| Satan floating: feet off the floor, a slow bob, the wings beating gently | small: a lift and the wings' spread over time | 1 | |
| Epstein's hellfire ghost: see-through orange-red, legs into a flame tail, fade in and out, silly ghost arms | new look on the existing Epstein; fire from flying_whales_fx | 3 | |
| The face melting into a flaming skull | new: a skull drawing, the face sliding down in drips, flames from fire_sprite | 3 | |
| Trump's walk to the desk, pointing; Satan's shrug and chuckle; the zoom out | reuse: moves walk, perform gestures, a camera move | 2 | |
| Shots, voices, subtitles, Hook Text, sign-off | template | 4 | |
| total (first estimate; over Sam's 10% cap: cut to 9%, see Decisions) | | 15 | |

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| oval-1 | gold swag valance, 3 windows, Resolute desk, leather chair, flags, navy carpet, seal, chairs, busts, alcove | yes (busts on side tables, not the desk) |
| oval-3 | fireplace with portrait, cream sofas, yellow armchairs, grandfather clock, flowers, phones | yes |
| oval-5 | room from above: oval, 4 pedimented doors, alcoves | yes |
| satan-1/2 | black suit, red tie, gold pin, pocket square, slicked black hair, red eyes; horns, red wings | yes |
| epstein-1..3 | grey swept hair, tanned lined face, half-smile, dark polo | yes |

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 29 | 1 | 0-2 s | open the door from the start so we see him (viewer retention) | fixed: open at 0.1 s; he stands in the doorway talking, then strides in 1.3 s before the slam |
| 30 | 9 | melt | the skull took over his whole body: skin sloughs off his FACE, a head-sized screaming skull (repeat of 27/28) | fixed: why the first fix failed: the head was measured from his drawing with the arms raised (the wave, new in the film), so the box spanned his arms; now measured with the arms down |
| 31 | 1 | 0.67 | corridor reads as a white void with a carpet: make it a 3D space; Trump looks LEFT, palm out "no, thank you"; a few camera flashes from the left | to do: corridor with side walls, ceiling, sconces, runner in perspective; flashes one frame each, lumpy (house style) |
| 32 | 2 | 2.00 | he stops for a beat, a quick breath, then visibly angry, looks at Satan and points | to do: walk ends early, breath (shoulders up/down 0.5 s), frown snaps on, then the point |
| 33 | 2 | 4.25 | Satan forward a bit, bigger in frame; a pointing finger whenever anyone points | to do: SATAN_AT nearer the lens; find why the point hand shows no finger (MV._install_point_finger) |
| 34 | 3 | 5.83 | Satan: red horns from his shoulders not needed (the wing tops); the shrug is wrong: shoulders and arms rise quickly and noticeably, not arms hanging in a U; wary of the U shape everywhere; folded flag strips have gaps (float) | to do: wing tips lowered behind the shoulders; shrug = shoulders up, forearms up, palms up near the hips; flag folds closed |
| 35 | 4 | 10.67 | Trump not expressive enough: arms for emphasis, exasperation, accusation | proposal sent (palms up then jabbing point) |
| 36 | 5 | 11.08 | the cut comes too soon (Satan speaks under the old subtitle); Satan smiles coyly as he speaks; see-through tears on his wings | to do: cut after the subtitle clears; coy smile mood; wing fill gaps closed |
| 37 | 5/6 | 13.58 | Satan's pocket square switches sides for a beat | to do: find the frame (view snap?) |
| 38 | 6 | 13.75 | no zoom out: hold the shot; Epstein appears in a burst of flames and light smoke | to do |
| 39 | 7 | 15.92 | occasional flames on his body; opacity up 50%; recognisable; arms open imploringly on "why don't you come and join me?" | to do |
| 40 | 8 | 23.75 | more variety in face and body on the second sentence | proposal sent |
| 41 | 9 | 28 | the skull is not ghostly like him (apply the ghost opacity to it); the melt spreads over hands, shoulders and body revealing a burning skeleton; trees outside have no trunks | to do (why it felt wrong: the skull was drawn under the ghost at full strength, not through MS.ghost); skeleton reference asked |
| 42 | 10 | 31 | "release the files": mocking and childish | proposal sent; books in the background are blobs: to do (spines with gaps and tops) |
| 43 | 10 | 32 | the last line cuts back to the shot 2 angle; Trump jabs his finger at Satan, furious; Satan flinches back a little, raised eyebrow, sceptical | to do |

Decisions made:
- Budget cut to 9% (Sam's 10% cap): door 1, Satan float 0.5, ghost 2, skull melt 2, moves and zoom 1.5, template 2; at most one critique round each; stills sheet instead of clips where possible.
- Carpet texture is 1 px a cm; close-ups on the seal look a little blocky: redraw it at 2 px a cm if a shot goes close.
