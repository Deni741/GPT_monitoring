from core.ask_handler import handle_ask_instruction

# Тимчасова черга для демонстрації
instruction_queue = []

def add_instruction(instruction: str):
    instruction_queue.append(instruction)

def process_instruction():
    if not instruction_queue:
        return "❌ Черга пуста."

    instruction = instruction_queue.pop(0)

    if instruction.lower().startswith("/ask"):
        result = handle_ask_instruction(instruction)
        return result
    else:
        return "❌ Невідома команда: " + instruction
