from flask import Flask, request, jsonify
import asyncio
from core.executor import execute_instruction
from utils.logger import log_and_print

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        log_and_print(f"[WEBHOOK] Отримано дані: {data}")

        if not data:
            return jsonify({"status": "порожній запит"}), 400

        asyncio.run(execute_instruction(data))
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        log_and_print(f"[WEBHOOK] Помилка: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
