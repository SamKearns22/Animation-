# Prompt: making videos on a small budget

Paste this into a new chat (on Sonnet, medium effort).

---

I make short animated TikTok parodies in this repository from my iPhone. I don't code. Read `CLAUDE.md` first and
follow it. My weekly usage is at about 85%, and I want to make two more short videos this week. Each must use at most
about **5% of my weekly Pro budget**. Please research and report back on the three questions below, in plain English,
choosing for me where there's a choice. **Do not render any video in this chat.** Reading files and drawing at most
one or two test stills is fine.

1. **Where are tokens being wasted?**
   Read `guides/best-practice.md` (especially Part 5), `guides/preflight.md`, `guides/pipeline.md`,
   `guides/figure-rig.md`, `story/status.md` and the git log (`git log --stat -30`).
   Estimate where our usage goes: re-reading long guides, very long source files (for example
   `source/russiadent.py` is about 3,000 lines), render-and-review loops, editing rounds, notes found late, and
   images sent back and forth. Name the five biggest wastes and the fix for each. Examples of fixes: a short
   per-film checklist instead of re-reading every guide, smaller files, fewer full renders, notes caught at
   storyboard stage, and cheaper still checks.

2. **What is the cheapest kind of video that still feels like ours?**
   Compare at least these options and recommend one:
   - **Reuse a finished film's format** (for example *The Salt*: same set, characters and pipeline, new script).
   - **A house stick-figure style** that fits our look (black outlines, flat colour, circle hands as in South Park).
   - **Mostly still frames:** one or two drawings with a camera move, captions and sound.
   For each option, estimate:
   - how many chat turns, renders and preview stills it needs;
   - which existing parts it can reuse (`burnham.py`, `figure.py`, `peepee.py` captions, the title, the sound tools);
   - what it would cost as a share of a weekly Pro budget.

   Then define a **5% recipe:** the steps, the maximum number of renders (for example one stills sheet, then one
   final with no animatic), the file sizes, and what I should send in my brief, so that nothing has to be asked
   twice.

3. **Make it reliable on Sonnet, medium effort.**
   Write the recipe as a short, self-contained guide, `guides/quick-video.md` (one page at most). It should hold:
   - a fill-in brief template;
   - the exact commands;
   - the checks to run before the one final render;
   - what to do if a check fails.

   It must not depend on the long guides, so that a medium-effort Sonnet chat can follow it start to finish without
   reading anything else. If a template script would help (for example `source/quick.py`, which takes a script,
   a background and two characters and makes the film), build it. Test it once with a 3-second, half-size render,
   and report how many tokens and how much time that took.

Finish with:
- the five wastes and their fixes;
- your recommended format;
- the recipe and where to find it;
- anything I should change in `CLAUDE.md` to stop waste.

Keep any changes to the guides short. Commit and push to the branch I give you.
