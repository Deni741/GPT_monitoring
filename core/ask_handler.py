import json
from pathlib import Path
from utils.logger import log_and_print
from core.executor import execute_instruction

INSTRUCTION_PATH = Path("instruction.json")

async def handle_ask_instruction():
    if not INSTRUCTION_PATH.exists():
        raise FileNotFoundError("Файл instruction.json не знайдено")

    with open(INSTRUCTION_PATH, "r") as file:
        instruction = json.load(file)

    log_and_print(f"[ASK] Прочитано instruction.json:\n{instruction}")
    await execute_instruction(instruction)
