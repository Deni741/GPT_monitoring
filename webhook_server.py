from flask import Flask, request
import os
from core.executor import execute_instruction
from utils.logger import log_and_print

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    log_and_print(f"[WEBHOOK] Отримано дані: {data}")

    if not data:
        return {"status": "error", "message": "Пусте тіло запиту"}, 400

    # Перевіряємо ключові поля
    action = data.get("action")
    file_path = data.get("file_path")
    content = data.get("content")

    if not all([action, file_path, content]):
        return {"status": "error", "message": "Неповні дані"}, 400

    # Виконуємо інструкцію
    try:
        result = execute_instruction({
            "action": action,
            "file_path": file_path,
            "content": content
        })
        return {"status": "ok", "result": result}, 200
    except Exception as e:
        log_and_print(f"[WEBHOOK] Помилка: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    log_and_print(f"[WEBHOOK] Сервер запущено на порту {port}")
    app.run(host="0.0.0.0", port=port)
