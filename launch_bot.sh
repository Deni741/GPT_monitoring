#!/bin/bash
cd /root/telegram-bot

# Завантаження .env вручну
set -a
source .env
set +a

python3 main.py