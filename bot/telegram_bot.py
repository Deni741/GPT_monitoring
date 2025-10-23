import os, json, logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
TASKS = BASE_DIR / "data" / "tasks.jsonl"
TASKS.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tg-bot")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    log.info(f"/start від @{user.username} (chat_id={chat_id})")
    await update.message.reply_text(
        f"Привіт, {user.first_name}! Я підключений.\n"
        f"Твій <code>chat_id</code>: <b>{chat_id}</b>\n"
        f"Встав його в TELEGRAM_CHAT_ID у .env і перезапусти сервіс."
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")

def enqueue_task(task: dict):
    with open(TASKS, "a", encoding="utf-8") as f:
        f.write(json.dumps(task, ensure_ascii=False) + "\n")

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Використання: /task <текст завдання>")
        return
    task = {"type": "note", "text": text, "priority": 2, "ts": datetime.utcnow().isoformat()}
    enqueue_task(task)
    await update.message.reply_text("✅ Додав у чергу: " + text)

async def echo_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команди: /start /ping /task <текст>")

def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN відсутній у .env")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("task", task))
    app.add_handler(MessageHandler(filters.ALL, echo_unknown))
    log.info("Telegram bot started (long-polling)")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
