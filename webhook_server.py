from flask import Flask, request
import subprocess
import os
import hmac
import hashlib

app = Flask(__name__)

# ==== [ Налаштування ] ====
REPO_PATH = "/root/GPT_monitoring"
GITHUB_SECRET = os.environ.get("GITHUB_SECRET", "")  # опціонально
BRANCH = "main"

# ==== [ Валідація webhook (опціонально) ] ====
def verify_signature(payload, signature):
    if not GITHUB_SECRET:
        return True
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

# ==== [ Webhook endpoint ] ====
@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    signature = request.headers.get('X-Hub-Signature-256')

    if not verify_signature(payload, signature):
        return "Invalid signature", 403

    try:
        os.chdir(REPO_PATH)
        subprocess.run(['git', 'fetch'], check=True)

        diff = subprocess.run(
            ['git', 'diff', f'HEAD..origin/{BRANCH}', '--name-only'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if diff.stdout.strip():
            subprocess.run(['git', 'pull'], check=True)
            print("✅ Repo updated from GitHub.")
        else:
            print("⏩ No changes detected. Skipping pull.")

        return "OK", 200

    except Exception as e:
        print(f"❌ Error in webhook: {e}")
        return "Internal error", 500

# ==== [ Запуск сервера ] ====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
