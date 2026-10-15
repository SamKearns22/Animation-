#!/usr/bin/env python3
"""The finishing step for every TikTok film (Sam, 15 Oct), so nothing is forgotten: from the clean, untitled final
render, add the Hook Text (if the film has one) and the CranbriJoos sign-off at the end.

    python3 finish.py CLEAN.mp4 OUT.mp4 ["Hook Text"]

Keep CLEAN.mp4 (in source/data/FILM/, not on GitHub) so the Hook Text can change without a re-render.
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()


def has_sound(path):
    return 'Audio:' in subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr


def main():
    src, dst = sys.argv[1], sys.argv[2]
    hook = ' '.join(sys.argv[3:])
    with tempfile.TemporaryDirectory() as tmp:
        step = src
        if not has_sound(step):                    # a silent film gets a silent track, so the sign-off's slurp can join on
            quiet = os.path.join(tmp, 'quiet.mp4')
            subprocess.run([FF, '-y', '-loglevel', 'error', '-i', step, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono',
                            '-shortest', '-c:v', 'copy', '-c:a', 'aac', quiet], check=True)
            step = quiet
        if hook:
            hooked = os.path.join(tmp, 'hooked.mp4')
            subprocess.run([sys.executable, os.path.join(HERE, 'hook_text.py'), step, hooked, hook], check=True)
            step = hooked
        subprocess.run([sys.executable, os.path.join(HERE, 'signoff.py'), 'add', step, dst], check=True)


if __name__ == '__main__':
    main()
