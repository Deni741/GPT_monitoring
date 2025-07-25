from telegram import Update
from telegram.ext import ContextTypes
from core.ask_handler import handle_ask_instruction
from utils.logger import log_and_print

async def ask_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📩 Інструкція отримана. GPT обробляє запит...")
        log_and_print("[ASK] Інструкція отримана. GPT обробляє запит...")
        await handle_ask_instruction()
        await update.message.reply_text("✅ Інструкція оброблена й виконана.")
    except Exception as e:
        await update.message.reply_text(f"❌ Сталася помилка: {e}")
        log_and_print(f"[ASK] Помилка: {e}")
