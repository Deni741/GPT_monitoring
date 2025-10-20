#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/root/GPT_monitoring"
SERVICE_NAME="gpt-agent"

cd "$REPO_DIR"

# Підтягуємо токени/зміни з .env (не виводимо їх)
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Якщо є токен GitHub — гарантуємо, що remote використовує його
if [ -n "${GITHUB_TOKEN:-}" ]; then
  # не логимо URL, щоб не світити токен
  git remote set-url origin "https://${GITHUB_TOKEN}@github.com/Deni741/GPT_monitoring.git" || true
fi

# Оновлюємо індекс і порівнюємо HEAD з origin/main
git fetch --quiet origin

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

# Якщо є відставання — оновлюємось
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "[update] New commit detected. Updating..."
  # Чи змінювався requirements.txt?
  if git diff --name-only "$LOCAL" "$REMOTE" | grep -qx "requirements.txt"; then
    echo "[update] requirements.txt changed -> will reinstall deps after pull."
    REINSTALL_DEPS=1
  else
    REINSTALL_DEPS=0
  fi

  # Очищаємось і підтягуємо оновлення
  git reset --hard "$LOCAL"      >/dev/null
  git clean -fd                  >/dev/null
  git pull --ff-only origin main >/dev/null

  # Перевстановлюємо залежності за потреби
  if [ "$REINSTALL_DEPS" -eq 1 ]; then
    if [ -d ".venv" ]; then
      source .venv/bin/activate
    fi
    pip install -r requirements.txt --quiet
  fi

  # Перезапуск сервісу агента
  systemctl restart "$SERVICE_NAME"
  echo "[update] Done. Service restarted."
else
  echo "[update] No updates."
fi
