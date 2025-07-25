from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import log_and_print

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Бот працює. GPT готовий до виконання інструкцій.")
    log_and_print("[STATUS] Перевірка статусу: OK")
