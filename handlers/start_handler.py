from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import log_and_print

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = f"👋 Привіт, {user.first_name}! Я GPT_monitoring бот. Готовий до роботи!"
    await update.message.reply_text(text)
    log_and_print(f"[START] Привітання надіслано користувачу {user.first_name}")
