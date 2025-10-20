#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/root/GPT_monitoring"
cd "$REPO_DIR"

# Підтягнути токен із .env (якщо є)
if [ -f ".env" ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Обов'язково має бути токен з правами repo
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "[autopush] GITHUB_TOKEN is empty. Exit."
  exit 0
fi

# Налаштуємо git під цього сервера (один раз не завадить)
git config user.name  "gpt-runner"
git config user.email "runner@local"

# Безпечно додамо remote з токеном на час пушу
# (ім'я користувача може бути будь-яким)
REMOTE_URL="https://${GITHUB_TOKEN}:x-oauth-basic@github.com/Deni741/GPT_monitoring.git"
git remote set-url origin "$REMOTE_URL"

# Поточна гілка
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

# Підтягнемо зміни з віддаленого
git fetch origin "$BRANCH"

# Спробуємо акуратно оновитися
if ! git pull --rebase origin "$BRANCH"; then
  echo "[autopush] Rebase failed, aborting rebase."
  git rebase --abort || true
fi

# Перевіримо, чи є локальні зміни
if git status --porcelain | grep -q .; then
  git add -A
  MSG="autopush: $(hostname) $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  git commit -m "$MSG" || true
  git push origin "$BRANCH"
  echo "[autopush] Pushed changes to $BRANCH."
else
  echo "[autopush] No local changes."
fi

# Повернемо нормальний remote без токена (не обов'язково, але акуратно)
git remote set-url origin "https://github.com/Deni741/GPT_monitoring.git"
