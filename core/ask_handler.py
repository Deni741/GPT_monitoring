from core.executor import save_code_to_file
from core.instruction_queue import instruction_queue

def handle_ask_instruction(text: str) -> str:
    if not text.lower().startswith("/ask"):
        return "❌ Невідома інструкція."

    code_request = text[4:].strip()
    if not code_request:
        return "❌ Напиши, що треба зробити."

    # 🧠 Генеруємо код (імітація, замінити на реальний GPT call)
    if "перемножує два числа" in code_request:
        generated_code = "def multiply(a, b):\n    return a * b"
        file_path = "handlers/test_handler.py"
    else:
        return "❌ Не впізнав запит."

    # 📝 Зберігаємо код у файл
    result = save_code_to_file(generated_code, file_path)
    return result
