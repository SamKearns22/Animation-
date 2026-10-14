#!/bin/bash
# Installs the animation tools at the start of each cloud session.
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi
pip install -q pillow numpy imageio imageio-ffmpeg numba scipy >/dev/null 2>&1
# a robotic speech voice for stand-in lines in animatics before Sam records (polanski.py)
command -v espeak-ng >/dev/null || (apt-get install -y -q espeak-ng >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q espeak-ng >/dev/null 2>&1))
exit 0
