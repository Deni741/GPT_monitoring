from telegram import Update
from telegram.ext import ContextTypes

async def refresh_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 /refresh: оновлення (заглушка).")
