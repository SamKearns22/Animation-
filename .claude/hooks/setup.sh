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
# The newest main line (audit A14, 2 Nov: a chat once started on a stale 30 Oct copy). Fetch it and say so if this
# copy is not it; never overwrite anything here (the chat moves onto it, keeping any work).
(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/../.."
 MAIN=claude/create-claude-md-oe8z4g
 for i in 1 2 3; do git fetch -q origin "$MAIN" 2>/dev/null && break; sleep $((i * 2)); done
 if [ "$(git rev-parse HEAD 2>/dev/null)" != "$(git rev-parse "origin/$MAIN" 2>/dev/null)" ]; then
   echo "NOTE: this copy is not the newest main line. Before any work: if 'git status' is clean, run"
   echo "  git checkout --detach origin/$MAIN"
   echo "and push with: git push origin HEAD:$MAIN (merge first if this copy holds work not on GitHub)."
 fi)
(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/../.."; python3 -c "import sys; sys.path.insert(0, 'source'); import likeness as K; [K._model(n) for n in K.URLS]" >/dev/null 2>&1) &
exit 0
