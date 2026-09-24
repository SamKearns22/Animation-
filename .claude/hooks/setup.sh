#!/bin/bash
# Installs the animation tools at the start of each cloud session.
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi
pip install -q pillow numpy imageio imageio-ffmpeg >/dev/null 2>&1
exit 0
