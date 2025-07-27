import os
import subprocess
from utils.logger import log_and_print

def update_code_from_github():
    log_and_print("🚀 Запускаю оновлення з GitHub...")

    try:
        output = subprocess.check_output(["git", "pull"], stderr=subprocess.STDOUT)
        log_and_print(f"✅ Код оновлено:\n{output.decode()}")
        
        # Після оновлення можна зробити рестарт бота, якщо потрібно:
        # os.system("systemctl restart telegram_bot.service")

    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ ПОМИЛКА при оновленні:\n{e.output.decode()}")
