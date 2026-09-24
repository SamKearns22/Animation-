# Working with me

I don't know how to code. Please:

- **Explain everything in plain English.** Avoid jargon, and if you have to use a technical word, say what it means.
- **Make choices for me rather than listing options.** Pick what you think is best, do it, and briefly tell me what you chose and why.
- **Always tell me where to find the finished file.** When you make or change something, tell me exactly where it is and how to open it.

# Making animations

- Every file must stay **under 50 MB** so it uploads to GitHub without problems (GitHub rejects anything over 100 MB and warns above 50 MB). Aim well below that: shorten, shrink or compress the animation if needed, and tell me the final size.
- Aim for **a few MB per animation**. GitHub keeps every old version forever, so big files add up fast; the whole project should stay well under 1 GB.
- Only upload the **finished version** of an animation. Keep drafts and test renders off GitHub.
- Default to an **MP4 video** (small and plays everywhere). Only make a GIF if I ask for one, and keep GIFs short and small.
- Put finished animations in the `animations/` folder with a clear name.
- The tools (Python with Pillow, NumPy, imageio and a bundled ffmpeg) are installed automatically at the start of each session by `.claude/hooks/setup.sh`.
