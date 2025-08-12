from telegram import Update
from telegram.ext import ContextTypes

async def execute_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 /execute: виконання буде додано пізніше.")
