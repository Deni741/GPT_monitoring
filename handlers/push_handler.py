from telegram import Update
from telegram.ext import ContextTypes
from core.push_handler import handle_push_instruction
from utils.logger import log_and_print

async def push_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📤 Інструкція на пуш отримана. GPT обробляє команду...")
        log_and_print("[PUSH] Отримано запит на пуш")

        await handle_push_instruction()

        await update.message.reply_text("✅ Код запушено на GitHub.")
        log_and_print("[PUSH] Пуш завершено успішно")

    except Exception as e:
        await update.message.reply_text(f"❌ Помилка при пуші: {e}")
        log_and_print(f"[PUSH] Помилка: {e}")
