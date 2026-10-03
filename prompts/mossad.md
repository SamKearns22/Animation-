# Prompt: "Mossad" - a coffee-shop TikTok parody (paste into a new Claude Code session on SamKearns22/Animation-)

Continue the animation project. First read these and follow them:
- CLAUDE.md;
- story/status.md;
- guides/best-practice.md: Part 1, plus **Part 2, the TikTok parody series**, which this film belongs to;
- guides/tiktok-design.md;
- guides/pipeline.md: the animatic-first rule.

The working rules:
- plain English for me;
- make the choices yourself;
- say how long each render will take and report how long it took;
- send a push notification when anything long finishes, fails or needs my decision;
- send pictures and videos in the chat.

**Before you make anything, ask me every question you need** (see the list at the end). Ask them in one
message, grouped, with your recommended answer for each, so I can just say yes.

## The format
- **TikTok, native 1080 x 1920.** Everything that matters stays inside the safe area (x 60-900,
  y 310-1500). Aim for **about 20-24 seconds**.
- **The opening:**
  - no held title card;
  - the first frame already moves (he is shuffling up to the counter), with café sound from the start;
  - **his first line starts within about half a second**, as he arrives at the counter;
  - the title **MOSSAD** in our standard treatment, gone by about 1 second, over background and never over
    a face.
- **The ending:** a hard cut to black about three-quarters of the way through the explosion: picture and
  sound cut together (with a few-millisecond fade so it doesn't click), then nothing.

## The look
- Our TikTok parody look: flat shapes, clean black outlines, almond eyes with small pupils, soft shading,
  deadpan staging, a still camera with hard cuts.
- Reuse the people, gesture, caption, title and film code from `source/burnham.py`, `burnham_film.py` and
  `peepee.py`, so it matches Hope Again and The Patriots.
- Everyone is fictional: no real person, no caricature of anyone real.

## Where: a clean, trendy London coffee shop
- **The room:** contemporary and airy, with pale wood, white surfaces and plants.
- **The front of the shop:** a wide bay window onto the street. Now and then a person or a car passes
  outside; this never pulls focus.
- **Before the window:** a low white coffee table with four plush white chairs, two on each side.
  - **Patron 1:** a Black student in a beanie and a sweater, typing frantically on a laptop, with an empty
    sandwich plate beside it.
  - **Patron 2:** a white man in a light navy suit with slicked-back black hair, relaxing over an
    espresso.
- **The counter**, from the staff side:
  - on the left, a stand of croissants;
  - on the right, a card machine (a generic one: no Zettle or Dojo logo) and a small stand of neatly
    packaged upmarket biscuits.
- **Behind the counter:**
  - an industrial espresso machine, milk jugs, steam wands, syrup bottles;
  - a stack of espresso cups, and a stack of large takeaway cups, **every one printed with the flag of
    Israel**;
  - the shop's name, **Coffee Queens**, somewhere small (the menu board or the apron).
- **One shared set for every camera** (as in The Patriots): build the whole shop once and point the
  cameras at it, so the counter, the cups, the croissants and the people never move between shots.

## The people
- **Customer:**
  - a man in his late forties: a light coat over a suit, reading glasses, a well-kept contemporary beard;
  - mildly weary, as if he's had a busy morning;
  - he speaks politely, then his eyebrows do the acting.
- **Customer 2:**
  - a nondescript man in his early thirties: a T-shirt and short brown hair;
  - waits patiently behind the customer, holding a black order buzzer (the restaurant kind with a small
    light);
  - he is in shot in every view of the customer, so the buzzer is planted from the first frame.
- **Cashier:**
  - a young white woman, nineteen, with wavy blue hair and a small, neat nose piercing: "alternative", but
    the kind that belongs in a fashionable café;
  - a white shirt and a blue apron; a tablet on a stand in front of her for taking payments;
  - she says everything with a bright, customer-service smile and never reacts to how strange it is.
- **Barista:**
  - an older Black woman working the espresso machine behind the cashier;
  - busy in Shot 2, frantically steaming milk in Shot 4.

## The scene, shot by shot
The shots cut back and forth between the customer and the cashier across the counter (shot,
reverse shot). Keep screen direction consistent: the customer always looks screen-left, the cashier
always looks screen-right.

1. **Over the counter, from the staff side** (the establishing shot, with the shop and the window
   behind). The customer shuffles up to the counter, with customer 2 waiting behind him, buzzer in hand.
   - **Customer:** *"Hi there, could I please order a caramel latte?"*
2. **Reverse onto the cashier.** The tablet is in front of her; behind her the barista is busy, and the
   flag cups are clearly visible.
   - **Cashier:** *"No problem at all. Just so you know, Israel has the right to defend itself."*
3. **The customer.** His eyebrows crease in alarm and confusion: he did not expect this transaction to
   become political.
   - **Customer:** *"Errm, excuse me?"*
4. **The cashier.** No reaction to what she has just said. Behind her, the barista steams milk
   frantically.
   - **Cashier:** *"Nothing to worry about, sir. Coffee Queens is currently doing a promotion with Mossad.
     Did you know that October 7th was, like, eleven 9/11s? And it's just my opinion, but if you start a
     war, you shouldn't complain when you can't finish it."*
5. **The customer.** His eyebrows stay alarmed and his mouth hangs a little open in offended outrage.
   Over his shoulder, the light on customer 2's buzzer starts flashing red.
   - **Customer 2** (pleased): *"Hey, my latte's ready!"*
   - The buzzer suddenly explodes in his hands. **Cut to black about three-quarters of the way through
     the explosion.**

## The explosion: impactful, never gory
- Make it a cartoon explosion:
  - a white-yellow flash;
  - a jagged burst shape;
  - a ball of grey smoke and a few flying plastic bits;
  - the frame shaking.
- No blood, no injury, no body parts and no screams. We cut before any aftermath, and nobody is shown
  hurt.
- Two or three frames of build-up first: the red light flashes faster and the buzzer rattles in his
  palm. Then the bang.

## The joke
Mossad's propaganda and talking points are so obvious and everywhere that they have stopped bothering to
hide them: the cashier recites them as cheerfully as a loyalty-card offer. The exploding buzzer is the
final step into absurdity, the "promotion" made real. Play every beat completely straight: the cashier
never winks, the camera never comments, and the customer's eyebrows are the audience.

## The sound
- **Sam's recordings:** I attach the audio files in the chat together with this prompt. Save them to
  `source/audio/` as `mossad-<who>-<n>.m4a`, listen to each one, and work out which line is which from what
  is said. Ask me only if a file is unclear.
  - Clean each one: reduce hiss, hum and room noise gently, so the voice never sounds underwater.
  - Level every line to the same loudness, so no line is quieter than another.
  - Master the film to about -14 LUFS, peaks no higher than -1 dBTP, as Part 1 of the master file says.
  - Otherwise play the voices exactly as recorded: volume only, no echo, no pitch change.
  - **Match the words to the recording, not to this script.** If I said something different, the captions
    follow what I said, and you tell me where it differs.
- **Café atmosphere, made in code:**
  - a soft murmur and cup clinks;
  - laptop typing from the student;
  - the espresso machine's hiss under Shot 2, and the steam wand screaming under Shot 4;
  - a faint street sound through the window;
  - no music.
- **The buzzer:** its normal buzz and rattle as the light flashes.
- **The explosion:** a short, punchy, slightly muffled boom (a deep thump with a crack on top).
  - No ringing in the ears, no debris rain, no screams. The sound cuts with the picture.
  - Make it impactful but not realistic gunfire or bomb audio. That keeps it cartoonish, and softer if
    TikTok's automatic checks listen for real-sounding explosions.

## Captions
- Our standard captions: bold white with a black outline, centred on the frame, wrapped to at most 700
  pixels in balanced rows, inside the safe area. Keep the rows short (aim for under about 42 characters).
- Split the cashier's long line into readable chunks, timed to her voice.
- Two words in the captions are under review: "October 7th" and "9/11" (see the questions).

## Things to handle carefully
- **The target is state propaganda, not Jewish people.**
  - No religious symbols beyond the national flag on the cups.
  - No caricatured features on anyone.
  - Nothing that could read as a trope about Jewish people in general.
  - The joke is a government's talking points being recited like a sales script.
- **Real tragedies:** October 7th, 9/11 and the pager attacks all killed real people. The comedy is aimed
  at people using those events as talking points, never at the victims. Nothing in the picture shows or
  mocks them.
- **No real brands:** Coffee Queens is fictional. Check that no well-known chain uses the name. No real
  card-machine or coffee brand logos.

## How to work
1. Ask your questions (below) and wait for my answers.
2. **Clean and level the audio,** and send me a short note of where my words differ from the script.
3. Make a **storyboard sheet**: one still per shot at phone size, plus a close-up of the cups and the
   buzzer. Send it and wait for my OK.
4. Make a quick **animatic** of the whole film, small and rough, with the real audio. Send it and wait for
   my OK.
5. **Render the final film:**
   - send it in the chat;
   - save it as animations/mossad-vertical.mp4 (under 25 MB);
   - check it against the safe-area guides on the title, the widest caption and the busiest frame;
   - update story/status.md;
   - suggest a cover frame, with no spoilers: not the buzzer, and ideally the cashier mid-smile with the
     flag cups behind her.
   Do not suggest post text or a pinned question; I write those. You may point out hashtags that would
   spoil the joke or are likely to limit reach.

## Questions to ask me (with your recommendation for each)
- **Audio:** confirm which attached file is which line and who voices whom (say what you heard in each
  file).
- **Captions:**
  - "October 7th" and "9/11": written plainly, or disguised (for example with emoji or "w@r")?
  - Recommend writing them plainly. TikTok automatically transcribes the speech and analyses the picture,
    so disguising the captions alone does little to its moderation, while it costs readability and makes
    the joke harder to follow.
- **The explosion:** how big? Recommend a cartoon flash and smoke ball that fills about a third of the
  frame, cut at three-quarters.
- **Customer 2 before the end:** does he glance up at anyone? Recommend that he stays completely neutral
  and just waits, so the end comes from nowhere.
- **The shop name:** Coffee Queens on the apron, the menu board or both? Recommend both, small.
- **Patron 2 in the navy suit:** a hint that he is the Mossad man (he watches the counter, raises his
  espresso as it ends)? Recommend one tiny beat: in the last frame before the bang he calmly sips.
- **Anything to avoid** (people, jokes, symbols)?
