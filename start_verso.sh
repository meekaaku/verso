#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ -f "$ROOT/venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source "$ROOT/venv/bin/activate"
elif [[ -f "$ROOT/env/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source "$ROOT/env/bin/activate"
else
  echo "No venv found (expected venv/ or env/)"
  exit 1
fi

cleanup() {
  if [[ -n "${HTTP_PID:-}" ]] && kill -0 "$HTTP_PID" 2>/dev/null; then
    kill "$HTTP_PID" 2>/dev/null || true
    wait "$HTTP_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

python3 -m http.server --directory "$ROOT/web_control" 8000 &
HTTP_PID=$!
echo "Web UI: http://$(hostname):8000/"
echo "WebSocket server starting..."

python3 "$ROOT/websocket_server.py"
