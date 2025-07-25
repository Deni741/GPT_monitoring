import os
from pathlib import Path
from utils.logger import log_and_print

def save_code_to_file(code: str, path: str) -> str:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(code)

    message = f"[EXECUTOR] Код збережено у {path}"
    log_and_print(message)
    return message

async def execute_instruction(instruction: dict):
    action = instruction.get("action")
    file_path = instruction.get("file_path")
    content = instruction.get("content")

    if not action or not file_path or not content:
        log_and_print("[EXECUTOR] Неповна інструкція. Пропущено.")
        return

    if action == "create_or_update_file":
        result = save_code_to_file(content, file_path)
        log_and_print(f"[EXECUTOR] Результат виконання: {result}")
    else:
        log_and_print(f"[EXECUTOR] Невідома дія: {action}")
