#!/bin/bash
# Installs the animation tools at the start of each cloud session.
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi
pip install -q pillow numpy imageio imageio-ffmpeg numba scipy >/dev/null 2>&1
# a robotic speech voice for stand-in lines in animatics before Sam records (polanski.py)
command -v espeak-ng >/dev/null || (apt-get install -y -q espeak-ng >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q espeak-ng >/dev/null 2>&1))
# likeness.py (face measuring, 31 Oct): the face finder, OpenCV's detector, the graphics libraries they need, and their models
pip install -q mediapipe opencv-python-headless >/dev/null 2>&1
command -v ldconfig >/dev/null && (ldconfig -p | grep -q libEGL.so.1 || apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1))
(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/../.."; python3 -c "import sys; sys.path.insert(0, 'source'); import likeness as K; [K._model(n) for n in K.URLS]" >/dev/null 2>&1) &
exit 0
