#!/usr/bin/env bash
set -euo pipefail

DISPLAY_NUM="${DISPLAY_NUM:-:1}"
SCREEN_GEOMETRY="${SCREEN_GEOMETRY:-1920x1080x24}"
VNC_PORT="${VNC_PORT:-5900}"
NOVNC_PORT="${NOVNC_PORT:-6080}"

PRD_SCRIPT="$(find /opt/prd -type f -name report-designer.sh | head -n 1 || true)"
if [[ -z "${PRD_SCRIPT}" ]]; then
  echo "Cannot locate report-designer.sh under /opt/prd" >&2
  exit 1
fi
chmod +x "${PRD_SCRIPT}"

Xvfb "${DISPLAY_NUM}" -screen 0 "${SCREEN_GEOMETRY}" &
XVFB_PID=$!

export DISPLAY="${DISPLAY_NUM}"
fluxbox &
FLUXBOX_PID=$!

x11vnc -display "${DISPLAY_NUM}" -forever -shared -nopw -rfbport "${VNC_PORT}" &
X11VNC_PID=$!

if [[ -x /usr/share/novnc/utils/novnc_proxy ]]; then
  /usr/share/novnc/utils/novnc_proxy --vnc "127.0.0.1:${VNC_PORT}" --listen "${NOVNC_PORT}" &
  NOVNC_PID=$!
else
  websockify --web /usr/share/novnc/ "${NOVNC_PORT}" "127.0.0.1:${VNC_PORT}" &
  NOVNC_PID=$!
fi

"${PRD_SCRIPT}" &
PRD_PID=$!

cleanup() {
  kill "${PRD_PID}" "${NOVNC_PID}" "${X11VNC_PID}" "${FLUXBOX_PID}" "${XVFB_PID}" 2>/dev/null || true
}

trap cleanup EXIT INT TERM
wait -n "${PRD_PID}" "${NOVNC_PID}" "${X11VNC_PID}" "${FLUXBOX_PID}" "${XVFB_PID}"
