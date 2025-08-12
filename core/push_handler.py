import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import log_and_print

def push_to_github():
    log_and_print("☑ Виконую push до GitHub...")

    os.system("git add .")
    os.system('git commit -m "☑ Автоматичний push з сервера"')
    os.system("git push")

    log_and_print("☑ Push завершено.")

def handle_push_instruction():
    """
    Функція, яка виконується при отриманні команди 'push' від бота.
    """
    log_and_print("📤 Отримано команду push. Виконую...")
    push_to_github()
    log_and_print("✅ Push інструкція виконана.")
