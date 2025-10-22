from flask import Flask, request, jsonify
import hmac, hashlib, os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    signature = request.headers.get("X-Hub-Signature-256", "")
    data = request.data

    # Перевіряємо підпис
    expected_signature = "sha256=" + hmac.new(
        secret.encode(), data, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return jsonify({"error": "invalid signature"}), 403

    print("✅ Webhook event received and verified")
    os.system("cd /root/GPT_monitoring && git pull origin main")
    return jsonify({"status": "success"}), 200


@app.route('/', methods=['GET'])
def root():
    return "Webhook server running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
