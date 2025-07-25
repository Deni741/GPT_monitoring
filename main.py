import os
import sys
import signal
import psutil
import atexit

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, CommandHandler
)

from handlers.start_handler import start_handler
from handlers.ask_handler import ask_handler
from handlers.status_handler import status_handler
from handlers.push_handler import push_handler
from handlers.execute_handler import execute_handler
from handlers.confirm_handler import confirm_handler
from handlers.refresh_handler import refresh_handler

from utils.logger import log_and_print

# === Анти-дубль запуск ===
LOCK_FILE = "main.lock"

def is_process_running(pid):
    return psutil.pid_exists(pid)

def create_lock_file():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock_file():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def setup_signal_handlers():
    def handler(signum, frame):
        remove_lock_file()
        sys.exit(0)

    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, handler)

# === Якщо вже запущено — вийти ===
if os.path.exists(LOCK_FILE):
    with open(LOCK_FILE, "r") as f:
        old_pid = int(f.read())
        if is_process_running(old_pid):
            print("⚠️  Бот уже запущено. Вихід.")
            sys.exit(0)
        else:
            remove_lock_file()

create_lock_file()
setup_signal_handlers()
atexit.register(remove_lock_file)

# === Запуск Telegram-бота ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN не знайдено в .env")
    sys.exit(1)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("ask", ask_handler))
app.add_handler(CommandHandler("status", status_handler))
app.add_handler(CommandHandler("push", push_handler))
app.add_handler(CommandHandler("exec", execute_handler))
app.add_handler(CommandHandler("confirm", confirm_handler))
app.add_handler(CommandHandler("refresh", refresh_handler))

log_and_print("[MAIN] Бот запущено. Очікування команд...")
app.run_polling()
