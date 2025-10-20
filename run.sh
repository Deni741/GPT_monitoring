#!/usr/bin/env bash
set -euo pipefail

cd /root/GPT_monitoring

# Підхопити змінні з .env, якщо файл існує
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

# Активувати venv
source .venv/bin/activate

# Один екземпляр: flock тримає замок на файлі main.lock
# якщо процес вже працює — новий не стартує
exec /usr/bin/flock -n /root/GPT_monitoring/main.lock \
  /usr/bin/env python agent/main.py
