#!/bin/bash
# Installs the animation tools at the start of each cloud session.
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi
# Only what is missing is installed, each step with a time limit (10 Nov: reinstalling everything every chat took
# about 1 min 45 s before Claude saw Sam's first message, and a slow download could hold a new chat up for good)
py_has() { python3 -c "import $1" >/dev/null 2>&1; }
need=""; for m in PIL:pillow numpy:numpy imageio:imageio imageio_ffmpeg:imageio-ffmpeg numba:numba scipy:scipy \
  mediapipe:mediapipe cv2:opencv-python-headless; do py_has "${m%%:*}" || need="$need ${m#*:}"; done
[ -n "$need" ] && timeout 150 python3 -m pip install -q $need >/dev/null 2>&1
# a robotic speech voice for stand-in lines in animatics before Sam records (polanski.py)
command -v espeak-ng >/dev/null || (timeout 60 apt-get install -y -q espeak-ng >/dev/null 2>&1 || (timeout 60 apt-get update -q >/dev/null 2>&1 && timeout 60 apt-get install -y -q espeak-ng >/dev/null 2>&1))
# likeness.py (face measuring, 31 Oct): the graphics libraries the face finder needs
command -v ldconfig >/dev/null && (ldconfig -p | grep -q libEGL.so.1 || timeout 60 apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1 || (timeout 60 apt-get update -q >/dev/null 2>&1 && timeout 60 apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1))
# The newest main line (audit A14, 2 Nov: a chat once started on a stale 30 Oct copy). Fetch it and say so if this
# copy is not it; never overwrite anything here (the chat moves onto it, keeping any work).
(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/../.."
 MAIN=claude/create-claude-md-oe8z4g
 for i in 1 2 3; do timeout 20 git fetch -q origin "$MAIN" 2>/dev/null && break; sleep $((i * 2)); done
 if [ "$(git rev-parse HEAD 2>/dev/null)" != "$(git rev-parse "origin/$MAIN" 2>/dev/null)" ]; then
   echo "NOTE: this copy is not the newest main line. Before any work: if 'git status' is clean, run"
   echo "  git checkout --detach origin/$MAIN"
   echo "and push with: git push origin HEAD:$MAIN (merge first if this copy holds work not on GitHub)."
 fi)
(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/../.."; python3 -c "import sys; sys.path.insert(0, 'source'); import likeness as K; [K._model(n) for n in K.URLS]" >/dev/null 2>&1) &
exit 0
