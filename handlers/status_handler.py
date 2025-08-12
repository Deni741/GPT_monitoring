from telegram import Update
from telegram.ext import CallbackContext

# Обробник команди /status
def status_handler(update: Update, context: CallbackContext):
    try:
        update.message.reply_text("✅ Бот працює та готовий приймати команди.")
    except Exception as e:
        update.message.reply_text(f"❌ Помилка у статусі: {e}")
