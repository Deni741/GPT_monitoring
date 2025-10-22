#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/root/GPT_monitoring"
LOG_DIR="$BASE_DIR/logs"
LOCK_FILE="$BASE_DIR/update.lock"
AGENT_SERVICE="gpt-agent.service"

mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/update_$(date +'%Y%m%d_%H%M%S').log"

{
  echo "=== $(date -Iseconds) | git_update START ==="

  # 1) взаємне виключення (не запускаємося паралельно)
  exec 9>"$LOCK_FILE"
  if ! flock -n 9; then
    echo "Another update is running, exiting."
    exit 0
  fi

  cd "$BASE_DIR"

  # 2) чисте оновлення з відкатом локальних змін
  echo "-- git fetch --all"
  git fetch --all

  echo "-- git reset --hard origin/main"
  git reset --hard origin/main

  # 3) залежності (якщо є requirements.txt)
  if [[ -f "requirements.txt" ]]; then
    echo "-- pip install -r requirements.txt (venv)"
    source .venv/bin/activate
    pip install -r requirements.txt
  fi

  # 4) м’який рестарт агента, якщо сервіс існує
  if systemctl list-units --full -all | grep -q "$AGENT_SERVICE"; then
    echo "-- systemctl restart $AGENT_SERVICE"
    systemctl restart "$AGENT_SERVICE"
  else
    echo "-- agent service not found, skipping restart"
  fi

  echo "=== $(date -Iseconds) | git_update DONE ==="
} >>"$LOG_FILE" 2>&1
