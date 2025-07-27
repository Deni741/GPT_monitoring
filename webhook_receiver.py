from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Читання тіла запиту (важливо для уникнення EOF)
        payload = request.data

        # Перевірка заголовка GitHub
        if request.headers.get('X-GitHub-Event') == 'push':
            # Pull з GitHub
            subprocess.run(['git', '-C', '/root/GPT_monitoring', 'pull'], check=True)

            # Перезапуск systemd-сервісу
            subprocess.run(['systemctl', 'restart', 'webhook_server.service'], check=True)

            return 'Webhook received and processed.\n', 200
        else:
            return 'Ignored.\n', 200
    except Exception as e:
        return f'Error: {e}\n', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
