# Prompt: making the Satire style look less "AI generated"

Paste everything below the line into a new chat, on **Opus, high effort** (it is research and planning).

---

I make short animated TikTok parodies in this repository from my iPhone. I don't code. Read `CLAUDE.md` first and
follow it, then `guides/satire.md` (one page) and `source/satire_style.py` (the style kit). Do not open the other
long guides unless one of my questions below needs them.

**The problem.** Some viewers say our Satire-style films look AI generated. I want to know exactly which things in
the pictures give that impression, and how to change the style so they stop doing so, without losing what makes it
ours: flat colour, one black outline weight, circle hands (South Park style), deadpan faces, hard cuts, the made-up
TikTok screen.

**Step 1: gather a sample (cheaply).** Build ONE contact sheet (several small pictures side by side, opened once) of
about 16-20 tiles, taken from at least four Satire films: *Cry Minister* (`source/cryminister.py`), *The Park*
(`source/thepark.py`), *Russiadent Evil* (`source/russiadent.py`), *Mossad* (`source/mossad.py`), *The Patriots 2*
(`source/patriots2.py`) and *Hope Again*. Use each film's own `cast` or `stills` commands (or stills already in
`review/`); never render a film. Include a spread of:
- **characters**: main people (Andy the Prime Minister, the old lady, the man in the Man City shirt), background
  people (the shoppers, crowds, conference-goers), animals (the dire wolves);
- **items**: the wolfproof armour, the council wolf net, shop signs and posters, graffiti, phones, cups;
- **locations**: the high street, the alley, the pub front, interiors, skies and backgrounds.
Zoom into a detail only when a small tile can't show it.

**Step 2: find the tells.** Look at the sheet like a sceptical viewer and like an illustrator. List every visual
"tell" that makes it read as AI or computer generated, for example (check these, and find others):
- shapes too perfect or too evenly wobbly (the same `rough` jitter everywhere), symmetrical faces and bodies;
- every person built from the same template (same-face, same proportions, same pose);
- lettering that looks typed rather than painted or drawn; signs that are too clean;
- textures or patterns that repeat exactly; perfectly straight perspective; nothing worn, dirty or uneven;
- colours that are too even or "default", no colour logic across a scene;
- details that don't make sense when you look closely (a strap going nowhere, a limb joined wrongly, odd text);
- motion that is too smooth or too regular (on 12 fps, eased curves everywhere, idle loops).
For each tell: say what it is in plain English, how strongly it reads as AI (high, medium or low), which films and
tiles show it (refer to the tile numbers on the sheet), and what part of the code causes it.

**Step 3: options.** Propose **3 or 4 distinct ways** to adapt the style that remove the strongest tells. Examples
of directions to consider: a hand-inked line (varying thickness, overshoots, small gaps), a limited per-film colour
palette with printed-paper texture, deliberately different body shapes and faces for every character, hand-lettered
signs, "on twos" animation with held drawings. For each option:
- show it: ONE before-and-after sheet using the same three tiles (a main character, a background person, a
  location), built in a new test file (for example `source/style_lab.py`), never by changing the films;
- say which tells it removes and which it leaves;
- say what it costs: how much code would change, whether finished films could be re-rendered with it, how much
  slower renders would get, and roughly how much of my weekly plan it would take to adopt;
- give your recommendation and why.

**Rules for this chat.**
- Explain everything in plain English and pick a recommendation rather than just listing options.
- Keep test pictures to a minimum: two or three sheets in total, each opened once.
- Do not change `source/satire_style.py`, any film, or any guide. I will choose an option first.
- Never add a rule or lesson to a guide without showing me the wording and getting my yes.
- Send me each sheet in the chat, and a push notification when the report is ready or you need me.
- Work on a new branch called `claude/style-ai-tells`, and commit and push the test file and sheets' code there
  (the sheets themselves stay in `review/`, off GitHub).

**Finish with:** the list of tells (strongest first), the before-and-after sheets, the 3-4 options with costs, your
recommendation, and what you would do next if I pick it.
